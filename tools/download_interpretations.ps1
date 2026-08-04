<#
.SYNOPSIS
    批量下载《企业会计准则解释》第1~18号中仍需补全正文的附件（官方来源）。

.DESCRIPTION
    - 仅下载"通知正文壳"里还缺解释正文的 13 个：#1 #2 #3 #9 #10 #11 #12 #13 #14 #15 #16 #17 #18
      （#4 #5 #6 #7 #8 与 #19 #20 的正文已在本地 .md 中，无需下载）
    - 官方直链优先（kjs.mof.gov.cn / m.mof.gov.cn / www.mof.gov.cn / www.gov.cn）；
      直链失败自动回退 Wayback Machine（用户已授权）；#2 #6 因官网直链不可得，走 Wayback CDX 解析。
    - 下载结果保存到 interpretations-pages 目录，命名为 解释第NN号_附件.<ext>。
    - 已存在的文件会跳过，可重复运行。

.NOTES
    运行环境：Windows PowerShell；目标目录按脚本所在仓库解析。
    用法：
        powershell -ExecutionPolicy Bypass -File download_interpretations.ps1
#>

$ErrorActionPreference = 'Continue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OutDir = Join-Path $RepoRoot 'knowledge-base\CPA-ZH\raw\standards\accounting\interpretations-pages'
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }

$UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
$log = @()

# 每个待下载项：编号、附件文件名、扩展名、官方直链候选（可为空）
$Items = @(
    @{ N='01'; File='P020081118406702247293.doc';  Ext='doc';  URLs=@('https://kjs.mof.gov.cn/zhengcefabu/200805/P020081118406702247293.doc') },
    @{ N='02'; File='P020080912540661805201.doc';  Ext='doc';  URLs=@() },  # 官网直链不可得 -> Wayback CDX
    @{ N='03'; File='P020090625556829994230.doc';  Ext='doc';  URLs=@('https://kjs.mof.gov.cn/zhengcefabu/200906/P020090625556829994230.doc') },
    @{ N='09'; File='P020170621605521628417.docx'; Ext='docx'; URLs=@('https://m.mof.gov.cn/zcfb/201706/P020170621605521628417.docx') },
    @{ N='10'; File='P020170621607055685277.docx'; Ext='docx'; URLs=@('https://m.mof.gov.cn/czxw/201706/P020170621607055685277.docx') },
    @{ N='11'; File='P020170621608562170360.docx'; Ext='docx'; URLs=@('https://kjs.mof.gov.cn/zhengcefabu/201706/P020170621608562170360.docx') },
    @{ N='12'; File='P020170621609794986303.docx'; Ext='docx'; URLs=@('https://kjs.mof.gov.cn/zhengwuxinxi/zhengcefabu/201706/P020170621609794986303.docx') },
    @{ N='13'; File='P020191213606003885528.pdf';  Ext='pdf';  URLs=@('https://kjs.mof.gov.cn/zhengcefabu/201912/P020191213606003885528.pdf') },
    @{ N='14'; File='P020210202577424347532.pdf';  Ext='pdf';  URLs=@('https://www.gov.cn/zhengce/zhengceku/2021-02/02/5584443/files/f92187bc53924ec584577ecd77daa1b8.pdf') },
    @{ N='15'; File='P020211231565531647850.pdf';  Ext='pdf';  URLs=@('https://m.mof.gov.cn/zcfb/202112/P020211231565531647850.pdf') },
    @{ N='16'; File='P020221213437987613379.pdf';  Ext='pdf';  URLs=@('https://kjs.mof.gov.cn/gongzuotongzhi/202212/P020221213437987613379.pdf') },
    @{ N='17'; File='P020231109301950429806.pdf';  Ext='pdf';  URLs=@('https://kjs.mof.gov.cn/zhengcefabu/202311/P020231109301950429806.pdf') },
    @{ N='18'; File='P020241223624330738971.pdf';  Ext='pdf';  URLs=@('https://m.mof.gov.cn/zcfb/202412/P020241223624330738971.pdf') }
)

function Resolve-ViaWayback {
    param([string]$Filename)
    # 通过 Wayback CDX 找到原始 mof.gov.cn 直链，再取其归档快照
    $cdx = "http://web.archive.org/cdx/search/cdx?url=*/$Filename&output=json&limit=10&filter=original:.*mof\.gov\.cn.*&fl=timestamp,original,statuscode"
    try {
        $resp = Invoke-RestMethod -Uri $cdx -UserAgent $UA -TimeoutSec 30
        foreach ($row in $resp) {
            if ($row -is [string]) { continue }  # 跳过表头
            $ts = $row[0]; $orig = $row[1]; $st = $row[2]
            if ($st -eq '200' -and $orig -match 'mof\.gov\.cn' -and $orig -match '\.(doc|docx|pdf)$') {
                return "http://web.archive.org/web/$ts/$orig"
            }
        }
    } catch {
        Write-Warning "  Wayback CDX 查询失败: $_"
    }
    return $null
}

function Try-Download {
    param([string]$Url, [string]$Dest)
    try {
        $r = Invoke-WebRequest -Uri $Url -UserAgent $UA -OutFile $Dest -TimeoutSec 60 -MaximumRedirection 5 -PassThru -ErrorAction Stop
        if (Test-Path $Dest) {
            $sz = (Get-Item $Dest).Length
            if ($sz -gt 1024) { return $true }
        }
        return $false
    } catch {
        return $false
    }
}

Write-Host "=== 开始批量下载（共 $($Items.Count) 个附件）===" -ForegroundColor Cyan
Write-Host "目标目录: $OutDir`n"

foreach ($it in $Items) {
    $dest = Join-Path $OutDir ("解释第{0}号_附件.{1}" -f $it.N, $it.Ext)
    if (Test-Path $dest) {
        $sz = (Get-Item $dest).Length
        if ($sz -gt 1024) {
            Write-Host "[跳过] #$($it.N) 已存在 ($sz 字节)" -ForegroundColor DarkGray
            $log += "[SKIP] #$($it.N) -> $dest"
            continue
        } else {
            Remove-Item $dest -Force
        }
    }

    $ok = $false
    $used = ''
    # 1) 官方直链（含同路径 Wayback 兜底）
    $candidates = @()
    foreach ($u in $it.URLs) {
        $candidates += $u
        $candidates += ("http://web.archive.org/web/2020/" + $u)
    }
    foreach ($u in $candidates) {
        if (Try-Download -Url $u -Dest $dest) { $ok = $true; $used = $u; break }
    }
    # 2) 若直链为空或全失败，走 Wayback CDX（#2 #6 走这里）
    if (-not $ok) {
        $wb = Resolve-ViaWayback -Filename $it.File
        if ($wb -and (Try-Download -Url $wb -Dest $dest)) { $ok = $true; $used = $wb }
    }

    if ($ok) {
        $sz = (Get-Item $dest).Length
        Write-Host "[成功] #$($it.N) <- $used ($sz 字节)" -ForegroundColor Green
        $log += "[OK]   #$($it.N) -> $dest ($sz B) src=$used"
    } else {
        Write-Host "[失败] #$($it.N) 所有来源均不可用，请手动下载附件 $($it.File)" -ForegroundColor Red
        $log += "[FAIL] #$($it.N) 附件名=$($it.File)"
    }
}

Write-Host "`n=== 下载完成 ===" -ForegroundColor Cyan
$log | ForEach-Object { Write-Host $_ }
$okCount = ($log | Where-Object { $_ -like '[OK]*' -or $_ -like '[SKIP]*' }).Count
$failCount = ($log | Where-Object { $_ -like '[FAIL]*' }).Count
Write-Host "`n成功/已存在: $okCount ，失败: $failCount"
if ($failCount -gt 0) {
    Write-Host "失败项需手动处理（见上方 [FAIL]）。" -ForegroundColor Yellow
}
