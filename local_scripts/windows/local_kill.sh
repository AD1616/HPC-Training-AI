net stop MongoDB

Get-Process | Where-Object {$_.ProcessName -like 'ollama'} | Stop-Process