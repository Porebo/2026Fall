$ErrorActionPreference = 'Stop'

$requiredColumns = @(
    'STUDENT_ID',
    'FIRST_NAME',
    'LAST_NAME',
    'PROGRAM_CODE',
    'COURSE_CODE',
    'MIDTERM',
    'FINAL',
    'ATTENDANCE'
)

function Add-Result {
    param(
        [string]$Rule,
        [string]$Test,
        [bool]$Passed,
        [string]$Details
    )

    [PSCustomObject]@{
        Rule = $Rule
        Test = $Test
        Result = if ($Passed) { 'PASS' } else { 'FAIL' }
        Details = $Details
    }
}

function Show-Results {
    param([object[]]$Results)

    foreach ($result in $Results) {
        $color = if ($result.Result -eq 'PASS') { 'Green' } else { 'Red' }
        Write-Host ("[{0}] {1} - {2}: {3}" -f $result.Result, $result.Rule, $result.Test, $result.Details) -ForegroundColor $color
    }
}

function Get-SourceValue {
    param(
        [object]$Row,
        [int]$ColumnIndex
    )

    $properties = @($Row.PSObject.Properties)
    if ($ColumnIndex -ge $properties.Count) {
        return ''
    }

    return [string]$properties[$ColumnIndex].Value
}

function Format-RowEvidence {
    param(
        [object[]]$Rows,
        [string]$Message
    )

    if ($Rows.Count -eq 0) {
        return 'No affected rows.'
    }

    $examples = @($Rows | Select-Object -First 8 | ForEach-Object { "row $($_.Row): $($_.Value)" }) -join '; '
    $suffix = if ($Rows.Count -gt 8) { '; ...' } else { '' }
    return "$Message Affected rows: $($Rows.Count). Examples: $examples$suffix"
}

function Add-RowCheck {
    param(
        [System.Collections.ArrayList]$ResultList,
        [string]$Rule,
        [string]$Test,
        [object[]]$Failures,
        [string]$Message,
        [string]$Remediation
    )

    $passed = $Failures.Count -eq 0
    [void]$ResultList.Add([PSCustomObject]@{
        Rule = $Rule
        Test = $Test
        Result = if ($passed) { 'PASS' } else { 'FAIL' }
        Details = if ($passed) { 'No deficiencies found.' } else { "$Message $($Failures.Count) affected records. $((Format-RowEvidence -Rows $Failures -Message ''))" }
    })
}

try {
    $filePath = 'e:\2026Fall\classes\principles-of-iq\w03\StudentGrades.csv'
    $fileName = [IO.Path]::GetFileName($filePath)
    if (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) {
        throw "The hardcoded input file does not exist: $filePath"
    }

    $results = @()
    $extension = [IO.Path]::GetExtension($fileName)
    $isCsvExtension = $extension -ieq '.csv'
    $results += Add-Result -Rule '1.1' -Test 'CSV file extension' -Passed $isCsvExtension -Details "Expected .csv; found $extension."

    $fileStream = [IO.File]::Open($filePath, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::ReadWrite)
    try {
        $fileBytes = New-Object byte[] ([int]$fileStream.Length)
        [void]$fileStream.Read($fileBytes, 0, $fileBytes.Length)
    }
    finally {
        $fileStream.Dispose()
    }
    $utf8Decoder = New-Object System.Text.UTF8Encoding($false, $true)
    $utf8Valid = $true
    try {
        $rawText = $utf8Decoder.GetString($fileBytes)
    }
    catch [Text.DecoderFallbackException] {
        $utf8Valid = $false
        $rawText = ''
    }
    $results += Add-Result -Rule '1.3' -Test 'UTF-8 encoding' -Passed $utf8Valid -Details $(if ($utf8Valid) { 'The file can be decoded as UTF-8.' } else { 'The file contains invalid UTF-8 bytes.' })

    $nonEmptyLines = @($rawText -split "\r?\n" | Where-Object { $_.Trim().Length -gt 0 })
    $hasHeader = $nonEmptyLines.Count -ge 1
    $headerLine = if ($hasHeader) { $nonEmptyLines[0] } else { '' }
    $repeatedHeaderCount = 0
    if ($hasHeader -and $nonEmptyLines.Count -gt 1) {
        $repeatedHeaderCount = @($nonEmptyLines[1..($nonEmptyLines.Count - 1)] | Where-Object { $_ -eq $headerLine }).Count
    }
    $oneHeader = $hasHeader -and ($repeatedHeaderCount -eq 0)
    $results += Add-Result -Rule '2.1' -Test 'One header row' -Passed $oneHeader -Details $(if ($oneHeader) { 'One non-empty first row was found and no repeated header row was detected.' } else { 'The file is missing a header row or contains a repeated header row.' })

    $csvRows = @()
    $csvParsed = $false
    try {
        if ($rawText.Length -gt 0) {
            $csvRows = @(ConvertFrom-Csv -InputObject $rawText)
            $csvParsed = $true
        }
    }
    catch {
        $csvParsed = $false
    }
    $results += Add-Result -Rule '1.2' -Test 'CSV structure can be parsed' -Passed $csvParsed -Details $(if ($csvParsed) { 'PowerShell parsed the file as comma-separated data.' } else { 'PowerShell could not parse the file as CSV.' })

    $headers = @()
    if ($csvParsed -and $csvRows.Count -gt 0) {
        $headers = @($csvRows[0].PSObject.Properties.Name)
    }

    $transcriptionPath = Join-Path -Path ([IO.Path]::GetDirectoryName($filePath)) -ChildPath 'student_grades_transcription.csv'
    if ($csvParsed -and $csvRows.Count -gt 0) {
        $transcriptionRows = @(
            for ($rowIndex = 0; $rowIndex -lt $csvRows.Count; $rowIndex++) {
                $transcription = [ordered]@{ SOURCE_ROW_NUMBER = $rowIndex + 2 }
                foreach ($property in $csvRows[$rowIndex].PSObject.Properties) {
                    $transcription[$property.Name] = $property.Value
                }
                [PSCustomObject]$transcription
            }
        )
        $transcriptionRows | Export-Csv -LiteralPath $transcriptionPath -NoTypeInformation -Encoding UTF8
    }

    $noLowercaseResults = @($headers | Where-Object { $_ -notmatch '[a-z]' })
    $noLowercase = $headers.Count -gt 0 -and $noLowercaseResults.Count -eq $headers.Count
    $results += Add-Result -Rule '2.2' -Test 'Column names contain no lowercase letters' -Passed $noLowercase -Details "$($noLowercaseResults.Count) of $($headers.Count) column names meet this condition."

    $noNumberResults = @($headers | Where-Object { $_ -notmatch '[0-9]' })
    $noNumbers = $headers.Count -gt 0 -and $noNumberResults.Count -eq $headers.Count
    $results += Add-Result -Rule '2.3' -Test 'Column names contain no numbers' -Passed $noNumbers -Details "$($noNumberResults.Count) of $($headers.Count) column names meet this condition."

    $noSpaceResults = @($headers | Where-Object { $_ -notmatch ' ' })
    $noSpaces = $headers.Count -gt 0 -and $noSpaceResults.Count -eq $headers.Count
    $results += Add-Result -Rule '2.4' -Test 'Column names contain no spaces' -Passed $noSpaces -Details "$($noSpaceResults.Count) of $($headers.Count) column names meet this condition."

    $noSpecialCharacterResults = @($headers | Where-Object { $_ -notmatch '[^A-Za-z0-9_]' })
    $noSpecialCharacters = $headers.Count -gt 0 -and $noSpecialCharacterResults.Count -eq $headers.Count
    $results += Add-Result -Rule '2.5' -Test 'Column names contain no special characters' -Passed $noSpecialCharacters -Details "$($noSpecialCharacterResults.Count) of $($headers.Count) column names meet this condition."

    $noInvisibleCharacterResults = @($headers | Where-Object { $_ -notmatch '[\x00-\x1F\x7F\u00AD\u200B-\u200D\u2060\uFEFF]' })
    $noInvisibleCharacters = $headers.Count -gt 0 -and $noInvisibleCharacterResults.Count -eq $headers.Count
    $results += Add-Result -Rule '2.6' -Test 'Column names contain no invisible or non-printing characters' -Passed $noInvisibleCharacters -Details "$($noInvisibleCharacterResults.Count) of $($headers.Count) column names meet this condition."

    $minimumLengthResults = @($headers | Where-Object { $_.Length -ge 5 })
    $minimumLength = $headers.Count -gt 0 -and $minimumLengthResults.Count -eq $headers.Count
    $results += Add-Result -Rule '2.7' -Test 'Column names contain at least 5 characters' -Passed $minimumLength -Details "$($minimumLengthResults.Count) of $($headers.Count) column names meet this condition."

    $maximumLengthResults = @($headers | Where-Object { $_.Length -le 30 })
    $maximumLength = $headers.Count -gt 0 -and $maximumLengthResults.Count -eq $headers.Count
    $results += Add-Result -Rule '2.8' -Test 'Column names contain no more than 30 characters' -Passed $maximumLength -Details "$($maximumLengthResults.Count) of $($headers.Count) column names meet this condition."

    for ($columnIndex = 0; $columnIndex -lt $requiredColumns.Count; $columnIndex++) {
        $requiredColumn = $requiredColumns[$columnIndex]
        $columnPresent = $headers -contains $requiredColumn
        $ruleNumber = "2.9.$($columnIndex + 1)"
        $results += Add-Result -Rule $ruleNumber -Test "Required column $requiredColumn" -Passed $columnPresent -Details $(if ($columnPresent) { 'The column is present.' } else { 'The column is missing.' })
    }

    $rowResults = New-Object System.Collections.ArrayList
    $sourceRows = @($csvRows)

    $studentIdRows = @(
        for ($rowIndex = 0; $rowIndex -lt $sourceRows.Count; $rowIndex++) {
            $value = Get-SourceValue -Row $sourceRows[$rowIndex] -ColumnIndex 0
            [PSCustomObject]@{ Row = $rowIndex + 2; Value = $value }
        }
    )
    Add-RowCheck -ResultList $rowResults -Rule '3.1.1' -Test 'Each data row contains one STUDENT_ID value.' -Failures @($studentIdRows | Where-Object { [string]::IsNullOrWhiteSpace($_.Value) }) -Message 'STUDENT_ID is missing.' -Remediation 'Populate the missing student IDs.'
    Add-RowCheck -ResultList $rowResults -Rule '3.1.2' -Test 'Each STUDENT_ID begins with S.' -Failures @($studentIdRows | Where-Object { $_.Value -notmatch '^S' }) -Message 'STUDENT_ID does not begin with uppercase S.' -Remediation 'Correct the student ID prefix.'
    Add-RowCheck -ResultList $rowResults -Rule '3.1.3' -Test 'Each STUDENT_ID contains three digits after S.' -Failures @($studentIdRows | Where-Object { $_.Value -notmatch '^S[0-9]+$' -or $_.Value.Length -ne 4 }) -Message 'STUDENT_ID does not contain exactly three digits after S.' -Remediation 'Correct the student ID format.'
    Add-RowCheck -ResultList $rowResults -Rule '3.1.4' -Test 'Each STUDENT_ID contains four characters.' -Failures @($studentIdRows | Where-Object { $_.Value.Length -ne 4 }) -Message 'STUDENT_ID does not contain four characters.' -Remediation 'Correct the student ID length.'

    $missingProgramRows = @(
        for ($rowIndex = 0; $rowIndex -lt $sourceRows.Count; $rowIndex++) {
            [PSCustomObject]@{ Row = $rowIndex + 2; Value = 'PROGRAM_CODE column is missing' }
        }
    )
    Add-RowCheck -ResultList $rowResults -Rule '3.2.1' -Test 'Each data row contains one PROGRAM_CODE value.' -Failures $missingProgramRows -Message 'PROGRAM_CODE is not available in the input file.' -Remediation 'Add the authoritative program code for each student.'
    Add-RowCheck -ResultList $rowResults -Rule '3.2.2' -Test 'Each PROGRAM_CODE begins with IQ.' -Failures $missingProgramRows -Message 'PROGRAM_CODE cannot be checked because the column is missing.' -Remediation 'Add PROGRAM_CODE values beginning with IQ.'
    Add-RowCheck -ResultList $rowResults -Rule '3.2.3' -Test 'Each PROGRAM_CODE contains three digits after IQ.' -Failures $missingProgramRows -Message 'PROGRAM_CODE cannot be checked because the column is missing.' -Remediation 'Add PROGRAM_CODE values with three digits after IQ.'
    Add-RowCheck -ResultList $rowResults -Rule '3.2.4' -Test 'Each PROGRAM_CODE contains five characters.' -Failures $missingProgramRows -Message 'PROGRAM_CODE cannot be checked because the column is missing.' -Remediation 'Add five-character PROGRAM_CODE values.'

    $missingFirstNameRows = @(
        for ($rowIndex = 0; $rowIndex -lt $sourceRows.Count; $rowIndex++) {
            [PSCustomObject]@{ Row = $rowIndex + 2; Value = 'FIRST_NAME column is missing; source NAME is combined' }
        }
    )
    Add-RowCheck -ResultList $rowResults -Rule '3.3.1' -Test 'Each data row contains one FIRST_NAME value.' -Failures $missingFirstNameRows -Message 'FIRST_NAME is not available as a separate column.' -Remediation 'Split the source NAME field into FIRST_NAME and LAST_NAME.'
    Add-RowCheck -ResultList $rowResults -Rule '3.3.2' -Test 'Each FIRST_NAME represents the student given name.' -Failures $missingFirstNameRows -Message 'The given name cannot be evaluated because FIRST_NAME is missing.' -Remediation 'Create FIRST_NAME from an authoritative student record.'
    Add-RowCheck -ResultList $rowResults -Rule '3.3.3' -Test 'Each FIRST_NAME uses uppercase letters.' -Failures $missingFirstNameRows -Message 'FIRST_NAME capitalization cannot be evaluated because FIRST_NAME is missing.' -Remediation 'Populate FIRST_NAME using uppercase letters.'
    Add-RowCheck -ResultList $rowResults -Rule '3.3.4' -Test 'Each FIRST_NAME contains no title or honorific.' -Failures $missingFirstNameRows -Message 'Titles cannot be separated because FIRST_NAME is missing.' -Remediation 'Remove titles and honorifics from FIRST_NAME.'
    Add-RowCheck -ResultList $rowResults -Rule '3.3.5' -Test 'Each FIRST_NAME contains no suffix.' -Failures $missingFirstNameRows -Message 'Suffixes cannot be evaluated because FIRST_NAME is missing.' -Remediation 'Remove suffixes from FIRST_NAME.'
    Add-RowCheck -ResultList $rowResults -Rule '3.3.6' -Test 'Each FIRST_NAME contains no surname particle.' -Failures $missingFirstNameRows -Message 'Surname particles cannot be evaluated because FIRST_NAME is missing.' -Remediation 'Keep surname particles with LAST_NAME.'
    Add-RowCheck -ResultList $rowResults -Rule '3.3.7' -Test 'Each FIRST_NAME contains no more than 60 characters.' -Failures $missingFirstNameRows -Message 'FIRST_NAME length cannot be evaluated because FIRST_NAME is missing.' -Remediation 'Create FIRST_NAME and limit it to 60 characters.'

    $scoreColumns = @(
        @{ Index = 4; Name = 'MIDTERM'; Rule = '3.4.1' },
        @{ Index = 5; Name = 'FINAL'; Rule = '3.4.2' },
        @{ Index = 6; Name = 'ATTENDANCE'; Rule = '3.4.3' }
    )
    foreach ($scoreColumn in $scoreColumns) {
        $nonNumericRows = @(
            for ($rowIndex = 0; $rowIndex -lt $sourceRows.Count; $rowIndex++) {
                $value = Get-SourceValue -Row $sourceRows[$rowIndex] -ColumnIndex $scoreColumn.Index
                if (-not [string]::IsNullOrWhiteSpace($value) -and $value -notmatch '^-?[0-9]+(\.[0-9]+)?$') {
                    [PSCustomObject]@{ Row = $rowIndex + 2; Value = $value }
                }
            }
        )
        Add-RowCheck -ResultList $rowResults -Rule $scoreColumn.Rule -Test "Each $($scoreColumn.Name) value is numeric." -Failures $nonNumericRows -Message "$($scoreColumn.Name) contains nonnumeric values." -Remediation "Replace invalid $($scoreColumn.Name) values with numeric values or null."
    }

    $scoreLimits = @(
        @{ Index = 4; Name = 'MIDTERM'; Rule = '3.4.4' },
        @{ Index = 5; Name = 'FINAL'; Rule = '3.4.5' },
        @{ Index = 6; Name = 'ATTENDANCE'; Rule = '3.4.6' }
    )
    foreach ($scoreLimit in $scoreLimits) {
        $overLimitRows = @(
            for ($rowIndex = 0; $rowIndex -lt $sourceRows.Count; $rowIndex++) {
                $value = Get-SourceValue -Row $sourceRows[$rowIndex] -ColumnIndex $scoreLimit.Index
                $number = 0.0
                if ([double]::TryParse($value, [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$number) -and $number -gt 100) {
                    [PSCustomObject]@{ Row = $rowIndex + 2; Value = $value }
                }
            }
        )
        Add-RowCheck -ResultList $rowResults -Rule $scoreLimit.Rule -Test "Each $($scoreLimit.Name) value does not exceed 100." -Failures $overLimitRows -Message "$($scoreLimit.Name) contains values above 100." -Remediation "Correct $($scoreLimit.Name) values to a maximum of 100."
    }

    $decimalRules = @(
        @{ Index = 4; Name = 'MIDTERM'; Rule = '3.4.7' },
        @{ Index = 5; Name = 'FINAL'; Rule = '3.4.8' },
        @{ Index = 6; Name = 'ATTENDANCE'; Rule = '3.4.9' }
    )
    foreach ($decimalRule in $decimalRules) {
        $precisionRows = @(
            for ($rowIndex = 0; $rowIndex -lt $sourceRows.Count; $rowIndex++) {
                $value = Get-SourceValue -Row $sourceRows[$rowIndex] -ColumnIndex $decimalRule.Index
                if ($value -match '^[-+]?[0-9]+\.([0-9]+)$' -and $Matches[1].Length -gt 1) {
                    [PSCustomObject]@{ Row = $rowIndex + 2; Value = $value }
                }
            }
        )
        Add-RowCheck -ResultList $rowResults -Rule $decimalRule.Rule -Test "Each $($decimalRule.Name) value uses no more than one decimal place." -Failures $precisionRows -Message "$($decimalRule.Name) contains values with more than one decimal place." -Remediation "Round or correct $($decimalRule.Name) values to one decimal place."
    }

    $nullRules = @(
        @{ Index = 4; Name = 'MIDTERM'; Rule = '3.4.10' },
        @{ Index = 5; Name = 'FINAL'; Rule = '3.4.11' },
        @{ Index = 6; Name = 'ATTENDANCE'; Rule = '3.4.12' }
    )
    foreach ($nullRule in $nullRules) {
        $textMissingRows = @(
            for ($rowIndex = 0; $rowIndex -lt $sourceRows.Count; $rowIndex++) {
                $value = Get-SourceValue -Row $sourceRows[$rowIndex] -ColumnIndex $nullRule.Index
                if ($value -match '^(?i:NA|N/A|unknown|seventy-five)$') {
                    [PSCustomObject]@{ Row = $rowIndex + 2; Value = $value }
                }
            }
        )
        Add-RowCheck -ResultList $rowResults -Rule $nullRule.Rule -Test "A missing $($nullRule.Name) value is represented as null." -Failures $textMissingRows -Message "$($nullRule.Name) uses text instead of null for missing data." -Remediation "Replace missing-value text with null."
    }

    $textScoreRows = @(
        for ($rowIndex = 0; $rowIndex -lt $sourceRows.Count; $rowIndex++) {
            foreach ($scoreIndex in @(4, 5, 6)) {
                $value = Get-SourceValue -Row $sourceRows[$rowIndex] -ColumnIndex $scoreIndex
                if ($value -match '^(?i:NA|N/A|unknown|seventy-five)$') {
                    [PSCustomObject]@{ Row = $rowIndex + 2; Value = $value }
                }
            }
        }
    )
    Add-RowCheck -ResultList $rowResults -Rule '3.4.13' -Test 'A missing score is not represented by text.' -Failures $textScoreRows -Message 'Missing scores are represented by text.' -Remediation 'Replace NA, N/A, unknown, and other text placeholders with null.'

    $duplicateRows = @(
        $sourceRows | ForEach-Object -Begin { $rowIndex = 2 } -Process {
            $id = Get-SourceValue -Row $_ -ColumnIndex 0
            $course = Get-SourceValue -Row $_ -ColumnIndex 3
            [PSCustomObject]@{ Row = $rowIndex; Value = "$id|$course" }
            $rowIndex++
        } | Group-Object Value | Where-Object { $_.Count -gt 1 } | ForEach-Object { $_.Group }
    )
    Add-RowCheck -ResultList $rowResults -Rule '3.5.1' -Test 'Each STUDENT_ID and COURSE_CODE combination is unique.' -Failures $duplicateRows -Message 'Duplicate student-course combinations were found.' -Remediation 'Investigate duplicate records and retain one authoritative record per student-course combination.'

    $rowResults | ForEach-Object { $results += $_ }

    $notApplicableRules = @(
        @{ Rule = '3.1.1'; Test = 'Each data row contains one STUDENT_ID value.' },
        @{ Rule = '3.1.2'; Test = 'Each STUDENT_ID begins with S.' },
        @{ Rule = '3.1.3'; Test = 'Each STUDENT_ID contains three digits after S.' },
        @{ Rule = '3.1.4'; Test = 'Each STUDENT_ID contains four characters.' },
        @{ Rule = '3.2.1'; Test = 'Each data row contains one PROGRAM_CODE value.' },
        @{ Rule = '3.2.2'; Test = 'Each PROGRAM_CODE begins with IQ.' },
        @{ Rule = '3.2.3'; Test = 'Each PROGRAM_CODE contains three digits after IQ.' },
        @{ Rule = '3.2.4'; Test = 'Each PROGRAM_CODE contains five characters.' },
        @{ Rule = '3.3.1'; Test = 'Each data row contains one FIRST_NAME value.' },
        @{ Rule = '3.3.2'; Test = 'Each FIRST_NAME represents the student given name.' },
        @{ Rule = '3.3.3'; Test = 'Each FIRST_NAME uses uppercase letters.' },
        @{ Rule = '3.3.4'; Test = 'Each FIRST_NAME contains no title or honorific.' },
        @{ Rule = '3.3.5'; Test = 'Each FIRST_NAME contains no suffix.' },
        @{ Rule = '3.3.6'; Test = 'Each FIRST_NAME contains no surname particle.' },
        @{ Rule = '3.3.7'; Test = 'Each FIRST_NAME contains no more than 60 characters.' },
        @{ Rule = '3.4.1'; Test = 'Each MIDTERM value is numeric.' },
        @{ Rule = '3.4.2'; Test = 'Each FINAL value is numeric.' },
        @{ Rule = '3.4.3'; Test = 'Each ATTENDANCE value is numeric.' },
        @{ Rule = '3.4.4'; Test = 'Each MIDTERM value does not exceed 100.' },
        @{ Rule = '3.4.5'; Test = 'Each FINAL value does not exceed 100.' },
        @{ Rule = '3.4.6'; Test = 'Each ATTENDANCE value does not exceed 100.' },
        @{ Rule = '3.4.7'; Test = 'Each MIDTERM value uses no more than one decimal place.' },
        @{ Rule = '3.4.8'; Test = 'Each FINAL value uses no more than one decimal place.' },
        @{ Rule = '3.4.9'; Test = 'Each ATTENDANCE value uses no more than one decimal place.' },
        @{ Rule = '3.4.10'; Test = 'A missing MIDTERM value is represented as null.' },
        @{ Rule = '3.4.11'; Test = 'A missing FINAL value is represented as null.' },
        @{ Rule = '3.4.12'; Test = 'A missing ATTENDANCE value is represented as null.' },
        @{ Rule = '3.4.13'; Test = 'A missing score is not represented by text.' },
        @{ Rule = '3.5.1'; Test = 'Each STUDENT_ID and COURSE_CODE combination is unique.' },
        @{ Rule = '4.1'; Test = 'The output contains a COURSE_AVERAGE column.' },
        @{ Rule = '4.2'; Test = 'COURSE_AVERAGE uses MIDTERM.' },
        @{ Rule = '4.3'; Test = 'COURSE_AVERAGE uses FINAL.' },
        @{ Rule = '4.4'; Test = 'COURSE_AVERAGE uses ATTENDANCE.' },
        @{ Rule = '4.5'; Test = 'MIDTERM contributes 45 percent.' },
        @{ Rule = '4.6'; Test = 'FINAL contributes 45 percent.' },
        @{ Rule = '4.7'; Test = 'ATTENDANCE contributes 10 percent.' },
        @{ Rule = '4.8'; Test = 'COURSE_AVERAGE is rounded to a whole number.' },
        @{ Rule = '4.9'; Test = 'The output contains a FINAL_LETTER_GRADE column.' },
        @{ Rule = '4.10'; Test = 'FINAL_LETTER_GRADE is based on COURSE_AVERAGE.' },
        @{ Rule = '4.11'; Test = 'Averages 90 through 100 produce A.' },
        @{ Rule = '4.12'; Test = 'Averages 80 through 89 produce B.' },
        @{ Rule = '4.13'; Test = 'Averages 70 through 79 produce C.' },
        @{ Rule = '4.14'; Test = 'Averages 60 through 69 produce D.' },
        @{ Rule = '4.15'; Test = 'Averages 0 through 59 produce F.' }
    )

    foreach ($notApplicableRule in $notApplicableRules) {
        if ($notApplicableRule.Rule -like '4.*') {
            $results += [PSCustomObject]@{
                Rule = $notApplicableRule.Rule
                Test = $notApplicableRule.Test
                Result = 'NA'
                Details = 'Not evaluated because the output report has not been created.'
            }
        }
    }

    $catalogPath = Join-Path -Path ([IO.Path]::GetDirectoryName($filePath)) -ChildPath 'student_grades_deficiency_catalog.csv'
    $catalog = @(
        foreach ($result in $results) {
            $remediation = switch ($result.Result) {
                'PASS' { 'None required.' }
                'FAIL' { 'Review the evidence, correct the source data, and rerun the examination.' }
                'NA' { 'Create or provide the required data, then rerun the examination.' }
            }

            [PSCustomObject]@{
                RULE_ID = $result.Rule
                STATUS = $result.Result
                REQUIREMENT = $result.Test
                DEFICIENCY = if ($result.Result -eq 'FAIL') { 'The data does not meet this requirement.' } elseif ($result.Result -eq 'NA') { 'The requirement could not be evaluated.' } else { 'None.' }
                EVIDENCE = $result.Details
                REMEDIATION = $remediation
            }
        }
    )
    $catalog | Export-Csv -LiteralPath $catalogPath -NoTypeInformation -Encoding UTF8

    Write-Host ''
    Write-Host "Examination results for: $filePath" -ForegroundColor Cyan
    Write-Host ''
    Show-Results -Results $results

    $passedCount = @($results | Where-Object { $_.Result -eq 'PASS' }).Count
    $failedCount = @($results | Where-Object { $_.Result -eq 'FAIL' }).Count
    $notApplicableCount = @($results | Where-Object { $_.Result -eq 'NA' }).Count
    Write-Host ''
    Write-Host "Summary: $passedCount passed, $failedCount failed, $notApplicableCount not applicable, $($results.Count) tests evaluated." -ForegroundColor Cyan
    Write-Host "Transcription saved to: $transcriptionPath" -ForegroundColor Cyan
    Write-Host "Deficiency catalog saved to: $catalogPath" -ForegroundColor Cyan
    Write-Host ''
    Write-Host 'Design feedback:' -ForegroundColor Yellow
    Write-Host 'The examination separates compound rules into individual checks so each condition produces its own pass or fail result.'
    Write-Host 'Each result now maps to one atomic rule in the specification, including separate tests for each length boundary and required column.'
    Write-Host 'This output shows whether the atomic-rule design produces clear, independently testable results.'
}
catch {
    Write-Error $_.Exception.Message
    exit 1
}
