param([Parameter(Mandatory=$true)][string]$Destination)
$ErrorActionPreference='Stop'
$manifest=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'MODELS.json') -Raw | ConvertFrom-Json
$target=[IO.Path]::GetFullPath($Destination)
New-Item -ItemType Directory -Path $target -Force | Out-Null
foreach($part in $manifest.files){
    $file=Join-Path $target $part.filename
    if(Test-Path -LiteralPath $file){
        if((Get-Item -LiteralPath $file).Length -eq $part.bytes -and (Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant() -eq $part.sha256){Write-Output "Already verified: $($part.filename)";continue}
        throw "Existing unverified file preserved: $file"
    }
    $partial=$file+'.part'
    if(Test-Path -LiteralPath $partial){throw "Partial download preserved: $partial"}
    Invoke-WebRequest -Uri $part.url -OutFile $partial
    if((Get-Item -LiteralPath $partial).Length -ne $part.bytes -or (Get-FileHash -LiteralPath $partial -Algorithm SHA256).Hash.ToLowerInvariant() -ne $part.sha256){throw 'Model checksum mismatch; partial file preserved.'}
    Move-Item -LiteralPath $partial -Destination $file
    Write-Output "Verified: $file"
}
