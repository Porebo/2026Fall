$svg = 'c:\repos\2026Fall\classes\graduate-project\06-study\sample-uic\diagrams\U01.svg'
$out = 'c:\repos\2026Fall\classes\graduate-project\06-study\design\figures\U01-atomic-map.pdf'
$html = Join-Path $PSScriptRoot 'print_u01.html'
$uri = ([System.Uri]$svg).AbsoluteUri
Set-Content -Path $html -Encoding utf8 -Value "<!doctype html><html><head><style>@page{size:8.5in 11in;margin:0}html,body{margin:0;padding:0}img{display:block;width:8.5in;height:11in}</style></head><body><img src='$uri'></body></html>"
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$before = (Get-Item $out -ErrorAction SilentlyContinue).LastWriteTime
$prof = Join-Path $PSScriptRoot 'edgeprof'
$p = Start-Process -FilePath $edge -PassThru -ArgumentList @('--headless=new', '--disable-gpu', "--user-data-dir=$prof", '--no-pdf-header-footer', '--print-to-pdf-no-header', "--print-to-pdf=$out", ([System.Uri]$html).AbsoluteUri)
for ($i = 0; $i -lt 60; $i++) {
  Start-Sleep -Milliseconds 500
  $t = (Get-Item $out -ErrorAction SilentlyContinue).LastWriteTime
  if ($t -and $t -ne $before) { Start-Sleep -Milliseconds 1000; break }
}
Get-Process msedge -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'edgeprof' } | Stop-Process -Force -Confirm:$false
Get-Item $out | Select-Object Length, LastWriteTime
