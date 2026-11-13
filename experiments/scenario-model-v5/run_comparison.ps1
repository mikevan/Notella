$ErrorActionPreference='Stop'
$root='C:\workspace\Notella'
$python='C:\workspace\TUltra-Project\LayerTime\tools\ai-training\.venv\Scripts\python.exe'
$run=Join-Path $root 'runtime\scenario-model-v5'
$deadline=(Get-Date).AddHours(2)
while (-not (Test-Path (Join-Path $run 'training-result.json'))) {
 if ((Get-Date) -gt $deadline) { throw 'Training wait limit reached; inspect preserved job.' }
 $launchPath=Join-Path $run 'launch.json'
 if (Test-Path $launchPath) {
  $launch=Get-Content $launchPath -Raw | ConvertFrom-Json
  $jobPath=Join-Path $run ('store\jobs\'+$launch.id+'\job.json')
  if (Test-Path $jobPath) {
   $job=Get-Content $jobPath -Raw | ConvertFrom-Json
   if ($job.status -in @('failed','cancelled')) { throw 'Training did not complete; preserve failure.' }
  }
 }
 Start-Sleep -Seconds 2
}
$result=Get-Content (Join-Path $run 'training-result.json') -Raw | ConvertFrom-Json
if ($result.applied -ne 80 -or $result.skipped -ne 0 -or -not $result.finite) { throw 'Training numerical gate failed.' }
$evaluator=Join-Path $root 'experiments\scenario-model-v5\evaluate.py'
& $python $evaluator --condition base *> (Join-Path $run 'base-generation.log')
if ($LASTEXITCODE -ne 0) { throw 'Base evaluation failed; preserve journal.' }
& $python $evaluator --condition adapted --adapter $result.adapter *> (Join-Path $run 'adapted-generation.log')
if ($LASTEXITCODE -ne 0) { throw 'Adapted evaluation failed; preserve journal.' }
& $python (Join-Path $root 'experiments\scenario-model-v5\report.py') *> (Join-Path $run 'report.log')
if ($LASTEXITCODE -ne 0) { throw 'Report failed; preserve all generation evidence.' }
Write-Output 'RETRACTION_COMPARISON_COMPLETE'
