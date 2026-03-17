# Run TweetDuel from any folder.
# Usage: .\run.ps1 [args]
# Or from anywhere: & "C:\inetpub\wwwroot\TweetDuel\run.ps1" --url "https://..."
# If installed with "pip install -e .", you can just run: tweetduel

$ProjectRoot = if ($env:TWEETDUEL_HOME) { $env:TWEETDUEL_HOME } else { $PSScriptRoot }
Push-Location $ProjectRoot
try {
    python -m tweetduel @args
} finally {
    Pop-Location
}
