[CmdletBinding()]
param([switch]$Execute,[switch]$Push,[switch]$ResumeStaged)
$ErrorActionPreference='Stop'
$root=$PSScriptRoot
function Invoke-MorphologyGit {
 param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Arguments)
 & git.exe -C $root @Arguments
 if ($LASTEXITCODE -ne 0) { throw "Git failed: $($Arguments -join ' ')" }
}
if ($Push -and -not $Execute) { throw '-Push requires -Execute.' }
$manifest=Get-Content (Join-Path $root 'checkpoint/morphology-v1-manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$head=Invoke-MorphologyGit rev-parse HEAD
if ($head -ne $manifest.parent) { throw 'Checkpoint parent differs from HEAD.' }
if ((Invoke-MorphologyGit branch --show-current) -ne 'main') { throw 'Expected main branch.' }
$origin=Invoke-MorphologyGit remote get-url origin
if ($origin -notin @('https://github.com/mikevan/Notella.git','git@github.com:mikevan/Notella.git')) { throw 'Unexpected origin.' }
$staged=@(Invoke-MorphologyGit diff --cached --name-only)
if ($staged.Count -and -not $ResumeStaged) { throw 'Inspect existing staged changes first.' }
if ($ResumeStaged) {
 $allowed=@($manifest.files | ForEach-Object {$_.path})+'checkpoint/morphology-v1-manifest.json'
 foreach ($path in $staged) { if ($path -notin $allowed) { throw 'Unexpected pre-existing staged path.' } }
}
foreach ($file in $manifest.files) {
 $full=[IO.Path]::GetFullPath((Join-Path $root $file.path))
 if (-not $full.StartsWith([IO.Path]::GetFullPath($root).TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Manifest path escapes project.' }
 if ((Get-FileHash -LiteralPath $full -Algorithm SHA256).Hash.ToLowerInvariant() -ne $file.sha256) { throw "File changed since review: $($file.path)" }
}
$paths=@($manifest.files | ForEach-Object {$_.path})+'checkpoint/morphology-v1-manifest.json'
Write-Output "Verified $($paths.Count) explicit checkpoint paths."
Invoke-MorphologyGit -c 'core.whitespace=cr-at-eol,blank-at-eol,space-before-tab' diff --check -- . ':(exclude)experiments/**' ':(exclude)archive/**'
if (-not $Execute) { Write-Output 'Preview complete; no Git mutation performed.'; return }
if ($Push) {
 $remote=Invoke-MorphologyGit ls-remote origin refs/heads/main
 if ($remote -ne ($manifest.parent+"`trefs/heads/main")) { throw 'Remote changed; inspect before publication.' }
}
$pathspecFile=[IO.Path]::GetTempFileName()
try {
 $literalPaths=@($paths | ForEach-Object { ':(literal)'+$_ })
 $bytes=[Text.UTF8Encoding]::new($false).GetBytes([string]::Join([char]0,$literalPaths)+[char]0)
 [IO.File]::WriteAllBytes($pathspecFile,$bytes)
 Invoke-MorphologyGit add --pathspec-from-file=$pathspecFile --pathspec-file-nul
} finally { Remove-Item -LiteralPath $pathspecFile }
Invoke-MorphologyGit -c 'core.whitespace=cr-at-eol,blank-at-eol,space-before-tab' diff --cached --check -- . ':(exclude)experiments/**' ':(exclude)archive/**'
$actual=@(Invoke-MorphologyGit diff --cached --name-only)
foreach ($path in $actual) { if ($path -notin $paths) { throw "Unexpected staged path: $path" } }
Invoke-MorphologyGit commit -F (Join-Path $root 'checkpoint/MORPHOLOGY-V1-COMMIT.txt')
if ($Push) {
 Invoke-MorphologyGit push origin main
 $sha=Invoke-MorphologyGit rev-parse HEAD
 $remote=Invoke-MorphologyGit ls-remote origin refs/heads/main
 if ($remote -ne ($sha+"`trefs/heads/main")) { throw 'Push verification failed.' }
 Write-Output "Verified remote main at $sha"
}
