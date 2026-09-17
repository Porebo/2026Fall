$ErrorActionPreference = 'Stop'

try {
    $sourceFolder = Read-Host 'Enter the source folder path'
    if ([string]::IsNullOrWhiteSpace($sourceFolder)) {
        throw 'A source folder path is required.'
    }

    $sourceFolder = [Environment]::ExpandEnvironmentVariables($sourceFolder.Trim().Trim('"'))
    if (-not (Test-Path -LiteralPath $sourceFolder -PathType Container)) {
        throw "The folder does not exist: $sourceFolder"
    }

    $markdownFileName = Read-Host 'Enter the Markdown filename, including the .md extension'
    if ([string]::IsNullOrWhiteSpace($markdownFileName)) {
        throw 'A Markdown filename is required.'
    }

    $markdownFileName = $markdownFileName.Trim().Trim('"')
    if ([IO.Path]::GetExtension($markdownFileName) -ne '.md') {
        throw 'The filename must have a .md extension.'
    }

    $markdownPath = Join-Path -Path $sourceFolder -ChildPath $markdownFileName
    if (-not (Test-Path -LiteralPath $markdownPath -PathType Leaf)) {
        throw "The Markdown file does not exist: $markdownPath"
    }

    $pandocCommand = Get-Command pandoc -ErrorAction SilentlyContinue
    if (-not $pandocCommand) {
        Write-Host 'Pandoc was not found. Checking for winget...'
        $wingetCommand = Get-Command winget -ErrorAction SilentlyContinue
        if (-not $wingetCommand) {
            throw 'Pandoc is not installed, and winget is not available. Install Pandoc manually and run this script again.'
        }

        Write-Host 'Installing Pandoc...'
        & $wingetCommand.Source install --id JohnMacFarlane.Pandoc --exact --accept-source-agreements --accept-package-agreements
        if ($LASTEXITCODE -ne 0) {
            throw "Pandoc installation failed with exit code $LASTEXITCODE."
        }

        $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
        $pandocCommand = Get-Command pandoc -ErrorAction SilentlyContinue
        if (-not $pandocCommand) {
            throw 'Pandoc was installed, but it is not available in the current PowerShell session. Close and reopen PowerShell, then run this script again.'
        }
    }

    $docxPath = Join-Path -Path $sourceFolder -ChildPath ([IO.Path]::GetFileNameWithoutExtension($markdownFileName) + '.docx')
    if (Test-Path -LiteralPath $docxPath) {
        Remove-Item -LiteralPath $docxPath -Force
    }

    Write-Host "Converting $markdownPath to $docxPath..."
    & $pandocCommand.Source $markdownPath --output=$docxPath
    if ($LASTEXITCODE -ne 0) {
        throw "Pandoc conversion failed with exit code $LASTEXITCODE."
    }

    Write-Host "Conversion complete: $docxPath"
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
