param([int]$Port=8765,[string]$Python='python',[string]$TrainingPython='', [string]$ModelPath='')
$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not $env:NOTELLA_API_TOKEN) {
    $env:NOTELLA_API_TOKEN = & $Python -c 'import secrets; print(secrets.token_urlsafe(32))'
    if ($LASTEXITCODE -ne 0) { throw 'Python could not generate an API token.' }
    Write-Host 'Created a token in this process environment. Set NOTELLA_API_TOKEN before starting if another client needs a known token.'
}
$notellaArguments=@('-m','notella','serve','--store',(Join-Path $PSScriptRoot 'data'),'--port',"$Port")
if ($TrainingPython -and $ModelPath) {
    $notellaArguments+=@('--engine',(Join-Path $PSScriptRoot 'training_engine'),'--python',$TrainingPython,'--model',('qwen3-4b='+$ModelPath))
}
& $Python @notellaArguments
if ($LASTEXITCODE -ne 0) { throw "Notella exited with code $LASTEXITCODE" }
