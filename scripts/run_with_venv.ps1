"""
File: run_with_venv.ps1
Location: ./scripts/run_with_venv.ps1
Created: 2024-11-03
Purpose: Run Python scripts while maintaining virtual environment state
"""

# Save current location
$currentLocation = Get-Location

# Activate virtual environment if not already activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "Activating virtual environment..."
    & "./venv/Scripts/Activate.ps1"
}

try {
    # Run the cleanup script
    Write-Host "Running cleanup script..."
    python scripts/safe_cleanup_structure.py

    # Ensure we're still in the virtual environment
    if (-not $env:VIRTUAL_ENV) {
        Write-Host "Reactivating virtual environment..."
        & "./venv/Scripts/Activate.ps1"
    }
} finally {
    # Restore location
    Set-Location $currentLocation
    
    # Make sure we're still in the venv
    if (-not $env:VIRTUAL_ENV) {
        & "./venv/Scripts/Activate.ps1"
    }
}

Write-Host "Script completed. Virtual environment is maintained."