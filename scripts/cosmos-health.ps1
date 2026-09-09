$ErrorActionPreference = "Continue"
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
function Probe($name, $url) {
  try {
    $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3
    Write-Host ("{0,-12} OK  {1}" -f $name, $r.StatusCode)
  } catch {
    Write-Host ("{0,-12} DOWN" -f $name)
  }
}
Probe "Ollama" "http://127.0.0.1:11434/api/tags"
Probe "ToolServer" "http://127.0.0.1:8767/health"
Probe "OpenWebUI" "http://127.0.0.1:8080/health"
try {
  $s = Invoke-RestMethod -Uri "http://127.0.0.1:8767/get_ship_status" -Method POST -ContentType "application/json" -Body "{}"
  Write-Host ("Ship sim     zone={0} alert={1} cantina={2}@{3}" -f $s.active_zone, $s.alert_level, $s.lighting.zones.Cantina.preset, $s.lighting.zones.Cantina.brightness)
} catch { Write-Host "Ship sim     unreachable" }
try {
  $tags = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags"
  $names = ($tags.models | ForEach-Object { $_.name }) -join ", "
  Write-Host "Models       $names"
} catch {}