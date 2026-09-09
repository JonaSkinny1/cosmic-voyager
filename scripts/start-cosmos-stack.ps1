# COSMOS local stack for SpaceshipDesktop
# Starts tool server + Open WebUI (Ollama assumed installed as app/service)
$ErrorActionPreference = "Stop"
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$root = Join-Path $env:USERPROFILE "Documents\cosmic-voyager"
Set-Location $root

function Wait-Url($url, $seconds=30) {
  $deadline = (Get-Date).AddSeconds($seconds)
  while ((Get-Date) -lt $deadline) {
    try { Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 2 | Out-Null; return $true } catch { Start-Sleep -Seconds 1 }
  }
  return $false
}

Write-Host "Checking Ollama..."
if (-not (Wait-Url "http://127.0.0.1:11434/api/tags" 5)) {
  Write-Host "Ollama not responding on :11434 - start the Ollama app, then re-run."
  exit 1
}
Write-Host "Ollama OK"

# Tool server
$toolUp = $false
try { Invoke-WebRequest -Uri "http://127.0.0.1:8767/health" -UseBasicParsing -TimeoutSec 2 | Out-Null; $toolUp = $true } catch {}
if (-not $toolUp) {
  Write-Host "Starting tool server on :8767..."
  Start-Process -FilePath "python" -ArgumentList "-m","orchestrator.tool_server" -WorkingDirectory $root -WindowStyle Minimized
  if (-not (Wait-Url "http://127.0.0.1:8767/health" 20)) { Write-Host "Tool server failed to start"; exit 1 }
}
Write-Host "Tool server OK http://127.0.0.1:8767"

# Open WebUI
$uiUp = $false
try { Invoke-WebRequest -Uri "http://127.0.0.1:8080/health" -UseBasicParsing -TimeoutSec 2 | Out-Null; $uiUp = $true } catch {}
if (-not $uiUp) {
  Write-Host "Starting Open WebUI on :8080..."
  $env:OLLAMA_BASE_URL = "http://127.0.0.1:11434"
  $env:WEBUI_AUTH = "False"
  Start-Process -FilePath "open-webui" -ArgumentList "serve","--host","127.0.0.1","--port","8080" -WindowStyle Minimized
  if (-not (Wait-Url "http://127.0.0.1:8080/health" 60)) { Write-Host "Open WebUI failed to start"; exit 1 }
}
Write-Host "Open WebUI OK http://127.0.0.1:8080"
Write-Host ""
Write-Host "Ready: select model cosmos, enable COSMOS Ship Tools, chat."
Write-Host "Docs: $root\open_webui\README.md"
Write-Host "Runbook: $root\docs\COSMOS-RUNBOOK.md"