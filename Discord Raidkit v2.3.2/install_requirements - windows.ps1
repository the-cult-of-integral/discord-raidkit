try {

  $testgit = git --version
  Write-Output "Git Version $testgit is already installed."

} catch [System.Management.Automation.CommandNotFoundException] {
    
    Write-Output "Git does not appear to be installed. Installing now. . ."
    
    try {
        $testchoco = choco -v
        Write-Output "Chocolatey Version $testchoco is already installed."
    } catch [System.Management.Automation.CommandNotFoundException] {
        Write-Output "Chocolatey does not appear to be installed. Installing now. . ."
        Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    }
 
    powershell choco install -y git
    $env:Path += ';C:\Program Files\Git\cmd'
    Stop-Process -Name Chocolatey
}

pip install git+https://github.com/Rapptz/discord.py selenium colorama requests bs4