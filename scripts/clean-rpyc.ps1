<#
.SYNOPSIS
    Deletes all compiled Ren'Py cache files (*.rpyc, *.rpymc) under src/.
#>

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$srcDir = Join-Path $root 'src'

$files = Get-ChildItem -Path $srcDir -Recurse -Include '*.rpyc', '*.rpymc' -File

if ($files.Count -eq 0) {
    Write-Host 'No .rpyc/.rpymc files found.'
    exit 0
}

foreach ($file in $files) {
    Remove-Item -LiteralPath $file.FullName -Force
    Write-Host "Removed $($file.FullName.Substring($root.Length + 1))"
}

Write-Host "`nRemoved $($files.Count) file(s)."
