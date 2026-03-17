@echo off
REM Run TweetDuel from any folder.
REM If installed with "pip install -e .", use: tweetduel
REM Otherwise run this from the TweetDuel project folder, or set TWEETDUEL_HOME.

setlocal
if defined TWEETDUEL_HOME (
    set "ROOT=%TWEETDUEL_HOME%"
) else (
    set "ROOT=%~dp0"
    set "ROOT=%ROOT:~0,-1%"
)

pushd /d "%ROOT%" >nul 2>&1
if errorlevel 1 (
    echo Failed to change to TweetDuel folder: %ROOT%
    exit /b 1
)

python -m tweetduel %*
set EXIT_CODE=%errorlevel%
popd >nul 2>&1
exit /b %EXIT_CODE%
