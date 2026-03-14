# 1. Create virtual environment if it does not exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

# 2. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
Write-Host "Checking dependencies..."
pip install -r requirements.txt

# 4. Load .env variables
$PORT_SERVER = 3000
if (Test-Path ".env") {
    Write-Host "Loading .env variables..."
    Get-Content ".env" | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]*?)\s*=\s*`"?([^`"]*)`"?\s*$") {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
            if ($key -eq "PORT") { $PORT_SERVER = $value }
        }
    }
}

# 5. Start FastAPI server
Write-Host "Starting FastAPI server on port $PORT_SERVER..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT_SERVER --reload --reload-dir app
