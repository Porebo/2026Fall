# Import dataset and extract row count & column names
$dataset = Import-Csv -Path "MovieDataset.csv"
$totalRows = $dataset.Count
$columns = $dataset[0].psobject.properties.Name

foreach ($col in $columns) {
    # Extract values for the current column
    $values = $dataset.$col

    # Identify missing/blank values and group by distinct entries
    $nullCount = ($values | Where-Object { [string]::IsNullOrWhiteSpace($_) }).Count
    $grouped = $values | Group-Object
    $distinctCount = $grouped.Count

    # Calculate frequency metrics
    $minFreq = ($grouped | Measure-Object -Property Count -Minimum).Minimum
    $maxFreq = ($grouped | Measure-Object -Property Count -Maximum).Maximum
    $cardinalityRatio = ($distinctCount / $totalRows)

    # Format output according to the 3-point framework
    Write-Host "Column: $col"
    Write-Host "1. Distribution Variance: Frequency range is $minFreq to $maxFreq."
    Write-Host "2. Sequencing & Format: Inferred data type is 'String'. Contains $nullCount missing entries."
    Write-Host ("3. Domain Cardinality: {0} distinct choices out of {1} rows (Cardinality Ratio: {2:P2}).`n" -f $distinctCount, $totalRows, $cardinalityRatio)
}
