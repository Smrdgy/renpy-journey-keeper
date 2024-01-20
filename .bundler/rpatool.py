#!/usr/bin/env python3

from __future__ import print_function

import sys
import os
import codecs
import pickle
import errno
import random
try:
    import pickle5 as pickle
except:
    import pickle
    if sys.version_info < (3, 8):
        print('warning: pickle5 module could not be loaded and Python version is < 3.8,', file=sys.stderr)
        print('         newer Ren\'Py games may fail to unpack!', file=sys.stderr)
        if sys.version_info >= (3, 5):
            print('         if this occurs, fix it by installing pickle5:', file=sys.stderr)
            print('             {} -m pip install pickle5'.format(sys.executable), file=sys.stderr)
        else:
            print('         if this occurs, please upgrade to a newer Python (>= 3.5).', file=sys.stderr)
        print(file=sys.stderr)


if sys.version_info[0] >= 3:
    def _unicode(text):
        return text

    def _printable(text):
        return text

    def _unmangle(data):
        if type(data) == bytes:
            return data
        else:
            return data.encode('latin1')

    def _unpickle(data):
        # Specify latin1 encoding to prevent raw byte values from causing an ASCII decode error.
        return pickle.loads(data, encoding='latin1')
elif sys.version_info[0] == 2:
    def _unicode(text):
        if isinstance(text, unicode):
            return text
        return text.decode('utf-8')

    def _printable(text):
        return text.encode('utf-8')

    def _unmangle(data):
        return data

    def _unpickle(data):
        return pickle.loads(data)

class RenPyArchive:
    file = None
    handle = None

    files = {}
    indexes = {}

    version = None
    padlength = 0
    key = None
    verbose = False

    RPA2_MAGIC = 'RPA-2.0 '
    RPA3_MAGIC = 'RPA-3.0 '
    RPA3_2_MAGIC = 'RPA-3.2 '

    # For backward compatibility, otherwise Python3-packed archives won't be read by Python2
    PICKLE_PROTOCOL = 2

    def __init__(self, version = 3, padlength = 0, key = 0xDEADBEEF, verbose = False):
        self.padlength = padlength
        self.key = key
        self.verbose = verbose

        self.version = version

    def __del__(self):
        if self.handle is not None:
            self.handle.close()

    # Determine archive version.
    def get_version(self):
        self.handle.seek(0)
        magic = self.handle.readline().decode('utf-8')

        if magic.startswith(self.RPA3_2_MAGIC):
            return 3.2
        elif magic.startswith(self.RPA3_MAGIC):
            return 3
        elif magic.startswith(self.RPA2_MAGIC):
            return 2
        elif self.file.endswith('.rpi'):
            return 1

        raise ValueError('the given file is not a valid Ren\'Py archive, or an unsupported version')

    # Extract file indexes from opened archive.
    def extract_indexes(self):
        self.handle.seek(0)
        indexes = None

        if self.version in [2, 3, 3.2]:
            # Fetch metadata.
            metadata = self.handle.readline()
            vals = metadata.split()
            offset = int(vals[1], 16)
            if self.version == 3:
                self.key = 0
                for subkey in vals[2:]:
                    self.key ^= int(subkey, 16)
            elif self.version == 3.2:
                self.key = 0
                for subkey in vals[3:]:
                    self.key ^= int(subkey, 16)

            # Load in indexes.
            self.handle.seek(offset)
            contents = codecs.decode(self.handle.read(), 'zlib')
            indexes = _unpickle(contents)

            # Deobfuscate indexes.
            if self.version in [3, 3.2]:
                obfuscated_indexes = indexes
                indexes = {}
                for i in obfuscated_indexes.keys():
                    if len(obfuscated_indexes[i][0]) == 2:
                        indexes[i] = [ (offset ^ self.key, length ^ self.key) for offset, length in obfuscated_indexes[i] ]
                    else:
                        indexes[i] = [ (offset ^ self.key, length ^ self.key, prefix) for offset, length, prefix in obfuscated_indexes[i] ]
        else:
            indexes = pickle.loads(codecs.decode(self.handle.read(), 'zlib'))

        return indexes

    # Generate pseudorandom padding (for whatever reason).
    def generate_padding(self):
        length = random.randint(1, self.padlength)

        padding = ''
        while length > 0:
            padding += chr(random.randint(1, 255))
            length -= 1

        return bytes(padding, 'utf-8')

    # Converts a filename to archive format.
    def convert_filename(self, filename):
        (drive, filename) = os.path.splitdrive(os.path.normpath(filename).replace(os.sep, '/'))
        return filename

    # Debug (verbose) messages.
    def verbose_print(self, message):
        if self.verbose:
            print(message)


    # List files in archive and current internal storage.
    def list(self):
        return list(self.indexes.keys()) + list(self.files.keys())

    # Check if a file exists in the archive.
    def has_file(self, filename):
        filename = _unicode(filename)
        return filename in self.indexes.keys() or filename in self.files.keys()

    # Read file from archive or internal storage.
    def read(self, filename):
        filename = self.convert_filename(_unicode(filename))

        # Check if the file exists in our indexes.
        if filename not in self.files and filename not in self.indexes:
            raise IOError(errno.ENOENT, 'the requested file {0} does not exist in the given Ren\'Py archive'.format(
                _printable(filename)))

        # If it's in our opened archive index, and our archive handle isn't valid, something is obviously wrong.
        if filename not in self.files and filename in self.indexes and self.handle is None:
            raise IOError(errno.ENOENT, 'the requested file {0} does not exist in the given Ren\'Py archive'.format(
                _printable(filename)))

        # Check our simplified internal indexes first, in case someone wants to read a file they added before without saving, for some unholy reason.
        if filename in self.files:
            self.verbose_print('Reading file {0} from internal storage...'.format(_printable(filename)))
            return self.files[filename]
        # We need to read the file from our open archive.
        else:
            # Read offset and length, seek to the offset and read the file contents.
            if len(self.indexes[filename][0]) == 3:
                (offset, length, prefix) = self.indexes[filename][0]
            else:
                (offset, length) = self.indexes[filename][0]
                prefix = ''

            self.verbose_print('Reading file {0} from data file {1}... (offset = {2}, length = {3} bytes)'.format(
                _printable(filename), self.file, offset, length))
            self.handle.seek(offset)
            return _unmangle(prefix) + self.handle.read(length - len(prefix))

    # Modify a file in archive or internal storage.
    def change(self, filename, contents):
        filename = _unicode(filename)

        # Our 'change' is basically removing the file from our indexes first, and then re-adding it.
        self.remove(filename)
        self.add(filename, contents)

    # Add a file to the internal storage.
    def add(self, filename, contents):
        filename = self.convert_filename(_unicode(filename))
        if filename in self.files or filename in self.indexes:
            raise ValueError('file {0} already exists in archive'.format(_printable(filename)))

        self.verbose_print('Adding file {0} to archive... (length = {1} bytes)'.format(
            _printable(filename), len(contents)))
        self.files[filename] = contents

    # Remove a file from archive or internal storage.
    def remove(self, filename):
        filename = _unicode(filename)
        if filename in self.files:
            self.verbose_print('Removing file {0} from internal storage...'.format(_printable(filename)))
            del self.files[filename]
        elif filename in self.indexes:
            self.verbose_print('Removing file {0} from archive indexes...'.format(_printable(filename)))
            del self.indexes[filename]
        else:
            raise IOError(errno.ENOENT, 'the requested file {0} does not exist in this archive'.format(_printable(filename)))

    # Load archive.
    def load(self, filename):
        filename = _unicode(filename)

        if self.handle is not None:
            self.handle.close()
        self.file = filename
        self.files = {}
        self.handle = open(self.file, 'rb')
        self.version = self.get_version()
        self.indexes = self.extract_indexes()

    # Save current state into a new file, merging archive and internal storage, rebuilding indexes, and optionally saving in another format version.
    def save(self, filename = None):
        filename = _unicode(filename)

        if filename is None:
            filename = self.file
        if filename is None:
            raise ValueError('no target file found for saving archive')
        if self.version != 2 and self.version != 3:
            raise ValueError('saving is only supported for version 2 and 3 archives')

        self.verbose_print('Rebuilding archive index...')
        # Fill our own files structure with the files added or changed in this session.
        files = self.files
        # First, read files from the current archive into our files structure.
        for file in list(self.indexes.keys()):
            content = self.read(file)
            # Remove from indexes array once read, add to our own array.
            del self.indexes[file]
            files[file] = content

        # Predict header length, we'll write that one last.
        offset = 0
        if self.version == 3:
            offset = 34
        elif self.version == 2:
            offset = 25
        archive = open(filename, 'wb')
        archive.seek(offset)

        # Build our own indexes while writing files to the archive.
        indexes = {}
        files_len = len(files)
        self.verbose_print('Writing ' + str(files_len) + ' files to archive file...')
        for file, content in files.items():
            # Generate random padding, for whatever reason.
            if self.padlength > 0:
                padding = self.generate_padding()
                archive.write(padding)
                offset += len(padding)

            archive.write(content)
            # Update index.
            if self.version == 3:
                indexes[file] = [ (offset ^ self.key, len(content) ^ self.key) ]
            elif self.version == 2:
                indexes[file] = [ (offset, len(content)) ]
            offset += len(content)

        # Write the indexes.
        self.verbose_print('Writing archive index to archive file...')
        archive.write(codecs.encode(pickle.dumps(indexes, self.PICKLE_PROTOCOL), 'zlib'))
        # Now write the header.
        self.verbose_print('Writing header to archive file... (version = RPAv{0})'.format(self.version))
        archive.seek(0)
        if self.version == 3:
            archive.write(codecs.encode('{}{:016x} {:08x}\n'.format(self.RPA3_MAGIC, offset, self.key)))
        else:
            archive.write(codecs.encode('{}{:016x}\n'.format(self.RPA2_MAGIC, offset)))
        # We're done, close it.
        archive.close()

        # Reload the file in our inner database.
        self.load(filename)

        self.verbose_print('Write completed')

    