@echo off
REM Quick setup script for Materials Research Aggregator (Windows)

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Please install Python 3.7 or higher.
    exit /b 1
)

REM Create a virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install the package and dependencies
echo Installing dependencies...
pip install -e .

REM Check for Materials Project API key
if "%MATERIALS_PROJECT_API_KEY%"=="" (
    echo.
    echo IMPORTANT: You need to set your Materials Project API key.
    echo Get your key from https://materialsproject.org/dashboard
    echo.
    echo Then set it with:
    echo set MATERIALS_PROJECT_API_KEY=your_api_key
    echo.
)

REM Run a simple test
echo Testing installation...
python -c "from materials_aggregator import MaterialsResearchAggregator; print('Installation successful!')"

echo.
echo ✓ Setup complete! Use the tool with: materials_aggregator
echo Example: materials_aggregator search Li,O --limit 5
echo.