$svg = 'c:\repos\2026Fall\classes\graduate-project\06-study\sample-uic\diagrams\U01.svg'
$out = 'c:\repos\2026Fall\classes\graduate-project\06-study\sample-uic\diagrams\U01.png'
$html = Join-Path $PSScriptRoot 'wrap_u01.html'
$uri = ([System.Uri]$svg).AbsoluteUri
Set-Content -Path $html -Encoding utf8 -Value "<!doctype html><html><body style='margin:0'><img src='$uri' style='width:816px;height:1056px;display:block'></body></html>"
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$before = (Get-Item $out -ErrorAction SilentlyContinue).LastWriteTime
$prof = Join-Path $PSScriptRoot 'edgeprof'
$p = Start-Process -FilePath $edge -PassThru -ArgumentList @('--headless=new', '--disable-gpu', '--hide-scrollbars', "--user-data-dir=$prof", '--force-device-scale-factor=2', '--window-size=816,1056', "--screenshot=$out", ([System.Uri]$html).AbsoluteUri)
for ($i = 0; $i -lt 60; $i++) {
  Start-Sleep -Milliseconds 500
  $t = (Get-Item $out -ErrorAction SilentlyContinue).LastWriteTime
  if ($t -and $t -ne $before) { Start-Sleep -Milliseconds 800; break }
}
Get-Process msedge -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match 'edgeprof' } | Stop-Process -Force -Confirm:$false
Get-Item $out | Select-Object Length, LastWriteTime
