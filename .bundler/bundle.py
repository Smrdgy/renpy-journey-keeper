import os
import shutil

if __name__ == "__main__":
    current_directory = os.getcwd()

    # Now, run the code to archive the collected .rpyc files
    from rpatool import RenPyArchive

    archive = RenPyArchive(version=3, verbose=True)

    # Add the collected .rpyc files to the archive
    for root, dirs, files in os.walk(current_directory):
        for file in files:
            if file.endswith(".rpyc") or "assets" in root:
                file_path = os.path.join(root, file)

                # Get the relative path by using os.path.relpath()
                relative_path = os.path.relpath(file_path, current_directory)

                with open(file_path, 'rb') as file_content:
                    archive.add(relative_path, file_content.read())

    # Save the archive
    dist_directory = os.path.join(current_directory, ".dist")
    if not os.path.exists(dist_directory):
        os.makedirs(dist_directory)
    
    archive_file = os.path.join(dist_directory, "SSSSS.rpa")

    if os.path.exists(archive_file):
        os.remove(archive_file)

    archive.save(archive_file)

    print("Archive created.")