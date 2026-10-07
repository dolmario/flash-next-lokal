[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference='Stop'
if (Test-Path -LiteralPath $OutputDirectory) { throw 'Choose a NEW output directory' }
New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
$encoding=[Text.UTF8Encoding]::new($false)
foreach ($endpoint in @('health','v1/models')) {
 $value=Invoke-RestMethod -Uri ('http://127.0.0.1:8091/'+$endpoint) -Method Get -TimeoutSec 30
 $name=if ($endpoint -eq 'health') {'HEALTH.json'} else {'MODELS.json'}
 [IO.File]::WriteAllText((Join-Path $OutputDirectory $name),($value | ConvertTo-Json -Depth 30)+"`n",$encoding)
}
Write-Output 'Two read-only GET requests saved. No inference request or server start.'
