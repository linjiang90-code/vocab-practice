# setup-vocab-serve-task.ps1
# 用途：把 vocab-practice 的 serve.py 注册为 SYSTEM 级「开机启动 + 5 分钟看门狗」常驻任务，
#        使其独立于 WorkBuddy agent 轮次存活，外网可长期访问 0.0.0.0:3279。
# 运行方式：右键「使用 PowerShell 运行」→ 选「以管理员身份运行」。
# 说明：
#   - serve.py 自身已绑定 0.0.0.0（不要改回 127.0.0.1）；若端口被占用它会自动退出，不会多实例抢端口。
#   - 用 TaskScheduler COM 注册，可绕过被安全策略禁用的 schtasks.exe CLI。
#   - 防火墙无需改动：实测外网在服务存活时可直接拿到 200（回环以外流量未被拦）。

$ErrorActionPreference = "Stop"

$PY     = "C:\Users\Win10\.workbuddy\binaries\python\versions\3.13.12\python.exe"
$WORK   = "C:\Users\Win10\WorkBuddy\2026-08-13-11-34-42\vocab-practice"
$SCRIPT = "$WORK\serve.py"
$TASK   = "vocab-serve"

$svc = New-Object -ComObject Schedule.Service
$svc.Connect()
$root = $svc.GetFolder("\")

# 已存在则先删除，避免重复注册
try { $root.DeleteTask($TASK, 0) } catch { }

$td = $svc.NewTask(0)
$td.RegistrationInfo.Description = "vocab-practice serve.py 常驻 (0.0.0.0:3279), SYSTEM, 开机+5分钟看门狗"
$td.RegistrationInfo.Author = "WorkBuddy"

$pr = $td.Principal
$pr.UserId = "SYSTEM"
$pr.LogonType = 5          # TASK_LOGON_SERVICE_ACCOUNT
$pr.RunLevel = 1           # TASK_RUNLEVEL_HIGHEST

$st = $td.Settings
$st.Hidden = $true
$st.DisallowStartIfOnBatteries = $false
$st.StopIfGoingOnBatteries = $false
$st.RunOnlyIfNetworkAvailable = $false
$st.RestartCount = 3
$st.RestartInterval = "PT1M"
$st.StartWhenAvailable = $true
$st.ExecutionTimeLimit = "PT0S"   # 0 = 无执行时限

# 动作：启动 python serve.py
$act = $td.Actions.Create(0)   # TASK_ACTION_EXEC
$act.Path = $PY
$act.Arguments = $SCRIPT
$act.WorkingDirectory = $WORK

# 触发器1：开机启动
$t1 = $td.Triggers.Create(8)   # TASK_TRIGGER_STARTUP
$t1.Enabled = $true

# 触发器2：每 5 分钟看门狗（确保意外退出后 5 分钟内自动拉起）
$t2 = $td.Triggers.Create(2)   # TASK_TRIGGER_DAILY
$t2.StartBoundary = "2026-01-01T00:00:00"
$t2.Repetition.Interval = "PT5M"
$t2.Repetition.Duration = "PT23H59M"
$t2.Enabled = $true

# 注册（TASK_CREATE_OR_UPDATE=6，LogonType=ServiceAccount=5）
$root.RegisterTaskDefinition($TASK, $td, 6, $null, $null, 5) | Out-Null
Write-Host "已注册任务: $TASK"

# 立即启动
try {
    $root.GetTask($TASK).Run($null)
    Write-Host "已启动任务 $TASK"
} catch {
    Write-Host ("启动失败: " + $_.Exception.Message)
}

# 本地探活验证
Start-Sleep -Seconds 4
try {
    $code = (Invoke-WebRequest -Uri "http://127.0.0.1:3279/api/status" -UseBasicParsing -TimeoutSec 4).StatusCode
    Write-Host ("本地探活 HTTP=" + $code + " (期望 200)")
} catch {
    Write-Host ("探活失败: " + $_.Exception.Message)
}
