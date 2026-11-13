$ErrorActionPreference='Stop'
$python='C:\workspace\TUltra-Project\LayerTime\tools\ai-training\.venv\Scripts\python.exe'
$root='C:\workspace\Notella'
$runtime=Join-Path $root 'runtime\scenario-model-v3'
$check=Get-Content (Join-Path $runtime 'memory-check-result.json') -Raw | ConvertFrom-Json
if ($check.applied -ne 2 -or $check.skipped -ne 0 -or -not $check.finite) { throw 'Longest-target hardware check did not pass.' }
& $python (Join-Path $PSScriptRoot 'train.py') *> (Join-Path $runtime 'training-runner.log')
if ($LASTEXITCODE -ne 0) { throw 'Scenario training failed; preserve the logs.' }
$result=Get-Content (Join-Path $runtime 'training-result.json') -Raw | ConvertFrom-Json
if ($result.applied -ne 80 -or $result.skipped -ne 0 -or -not $result.finite) { throw 'Inspect numerical records before evaluating.' }
$evaluator=Join-Path $root 'experiments\scenario-model-v1\evaluate.py'
& $python $evaluator --run scenario-model-v3 --condition base *> (Join-Path $runtime 'base-generation.log')
if ($LASTEXITCODE -ne 0) { throw 'Base generation failed; preserve partial journal.' }
& $python $evaluator --run scenario-model-v3 --condition adapted --adapter $result.adapter *> (Join-Path $runtime 'adapted-generation.log')
if ($LASTEXITCODE -ne 0) { throw 'Adapted generation failed; preserve partial journal.' }
Write-Output 'SCENARIO_COMPARISON_GENERATION_COMPLETE'
