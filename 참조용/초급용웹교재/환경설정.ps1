param(
    [ValidateSet('Setup', 'Check', 'Verify', 'Launch')]
    [string]$Mode = 'Setup'
)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
Set-Location -LiteralPath $PSScriptRoot

function Refresh-ProcessPath {
    # 설치 직후에도 현재 창에서 찾도록 PATH를 새로 읽습니다. 영구 설정은 변경하지 않습니다.
    $machinePath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = "$machinePath;$userPath;$env:Path"
}

function Find-Python {
    $candidates = New-Object 'System.Collections.Generic.List[string]'
    $launcher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($launcher) {
        try {
            $found = & $launcher.Source -3 -c 'import sys; print(sys.executable)' 2>$null
            if ($LASTEXITCODE -eq 0 -and $found) { $candidates.Add([string]($found | Select-Object -Last 1)) }
        } catch {}
    }
    foreach ($base in @('HKCU:\Software\Python\PythonCore', 'HKLM:\Software\Python\PythonCore', 'HKLM:\Software\WOW6432Node\Python\PythonCore')) {
        if (Test-Path -LiteralPath $base) {
            foreach ($version in Get-ChildItem -LiteralPath $base) {
                $key = Join-Path $version.PSPath 'InstallPath'
                if (Test-Path -LiteralPath $key) {
                    $install = Get-Item -LiteralPath $key
                    $exe = $install.GetValue('ExecutablePath')
                    if (-not $exe -and $install.GetValue('')) { $exe = Join-Path $install.GetValue('') 'python.exe' }
                    if ($exe) { $candidates.Add([string]$exe) }
                }
            }
        }
    }
    foreach ($cmd in @(Get-Command python.exe -All -ErrorAction SilentlyContinue)) {
        # Microsoft Store 실행 별칭을 실행하면 설치 화면이 열릴 수 있어 제외합니다.
        if ($cmd.Source -notlike '*\Microsoft\WindowsApps\*') { $candidates.Add($cmd.Source) }
    }
    foreach ($base in @("$env:LOCALAPPDATA\Programs\Python", "$env:ProgramFiles")) {
        foreach ($folder in @(Get-ChildItem -LiteralPath $base -Directory -Filter 'Python3*' -ErrorAction SilentlyContinue)) {
            $candidates.Add((Join-Path $folder.FullName 'python.exe'))
        }
    }
    foreach ($candidate in ($candidates | Select-Object -Unique)) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            try {
                $version = & $candidate -c 'import sys; print(sys.version_info.major,sys.version_info.minor,sep=chr(46))' 2>$null
                if ($LASTEXITCODE -eq 0 -and [version]([string]$version) -ge [version]'3.10') { return $candidate }
            } catch {}
        }
    }
    return $null
}

function Find-DotNet {
    $candidates = @()
    $cmd = Get-Command dotnet.exe -ErrorAction SilentlyContinue
    if ($cmd) { $candidates += $cmd.Source }
    $candidates += @("$env:ProgramFiles\dotnet\dotnet.exe", "${env:ProgramFiles(x86)}\dotnet\dotnet.exe", "$env:LOCALAPPDATA\Microsoft\dotnet\dotnet.exe", "$env:USERPROFILE\.dotnet\dotnet.exe")
    foreach ($candidate in ($candidates | Select-Object -Unique)) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            try {
                $sdks = & $candidate --list-sdks 2>$null
                if ($LASTEXITCODE -eq 0 -and ($sdks | Where-Object { $_ -match '^(?:[1-9]\d+)\.\d+\.\d+\s' })) { return $candidate }
            } catch {}
        }
    }
    return $null
}

function Install-Prerequisite([string]$PackageId) {
    Write-Host "설치 중: $PackageId (인터넷과 설치 권한이 필요할 수 있습니다.)"
    & winget.exe install --id $PackageId --exact --source winget --accept-source-agreements --accept-package-agreements
    $installCode = $LASTEXITCODE
    Refresh-ProcessPath
    # 설치 종료 코드는 출력하되 실제 사용 가능 여부는 다시 검사합니다.
    Write-Host "설치 프로그램 종료 코드: $installCode"
}

function Run-Verification([string]$PythonPath) {
    Write-Host '실제 C# 컴파일·한글 입출력 검증 중...'
    & $PythonPath (Join-Path $PSScriptRoot '설치검증.py')
    if ($LASTEXITCODE -ne 0) { throw '실행 검증에 실패했습니다. 위 오류를 확인한 뒤 setup.bat을 다시 실행하세요.' }
}

try {
    Write-Host '=== C# 초급용웹교재 환경 검사 ==='
    foreach ($file in @('server.py', 'index.html', 'exercises.json', '설치검증.py')) {
        if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot $file) -PathType Leaf)) {
            throw "필수 파일이 없습니다: $file. ZIP 안에서 실행하지 말고 폴더 전체를 압축 해제하세요."
        }
    }
    if ([Environment]::OSVersion.Version.Major -lt 10) { throw 'Windows 10/11 환경을 사용하세요.' }
    Refresh-ProcessPath
    $pythonPath = Find-Python
    $dotnetPath = Find-DotNet
    if ($Mode -eq 'Setup' -and (-not $pythonPath -or -not $dotnetPath)) {
        $winget = Get-Command winget.exe -ErrorAction SilentlyContinue
        if (-not $winget) {
            Write-Host 'WinGet이 없습니다. App Installer를 설치하거나 아래 도구를 직접 설치하세요.'
            Write-Host 'Python 3.10 이상: https://www.python.org/downloads/windows/'
            Write-Host '.NET SDK: https://dotnet.microsoft.com/download/dotnet/10.0'
            throw '설치 후 setup.bat을 다시 실행하세요. .NET Runtime만 설치하면 안 됩니다.'
        }
        if (-not $pythonPath) { Install-Prerequisite 'Python.Python.3.13' }
        if (-not $dotnetPath) { Install-Prerequisite 'Microsoft.DotNet.SDK.10' }
        $pythonPath = Find-Python
        $dotnetPath = Find-DotNet
    }
    if ($pythonPath) { Write-Host "Python: $pythonPath" } else { Write-Host 'Python 3.10 이상: 없음' }
    if ($dotnetPath) { Write-Host ".NET SDK: $dotnetPath" } else { Write-Host '.NET SDK 10 이상: 없음' }
    if (-not $pythonPath -or -not $dotnetPath) {
        throw '필요한 도구를 찾지 못했습니다. setup.bat을 실행하세요. 설치 직후라면 새 창에서 다시 실행하거나 PC를 재시작하세요.'
    }
    $env:Path = "$(Split-Path -Parent $dotnetPath);$env:Path"
    if ($Mode -in @('Setup', 'Verify')) { Run-Verification $pythonPath }
    if ($Mode -eq 'Launch') {
        & $pythonPath (Join-Path $PSScriptRoot 'server.py')
        exit $LASTEXITCODE
    }
    Write-Host '환경 확인 완료. 실습시작.bat으로 교재를 시작할 수 있습니다.' -ForegroundColor Green
    exit 0
} catch {
    Write-Host "`n[실패] $($_.Exception.Message)" -ForegroundColor Red
    if ($Mode -eq 'Setup') {
        Write-Host '자동 설치가 차단되면 Python과 .NET SDK를 직접 설치하거나 PC 관리자에게 문의하세요.'
    }
    exit 1
}
