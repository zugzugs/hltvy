#!/usr/bin/env python3
"""
Setup script for CS:GO/CS2 betting data collection automation.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_docker():
    """Check if Docker is available."""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Docker is not installed or not in PATH")
    print("Please install Docker to run FlareSolverr")
    return False

def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories."""
    directories = ['logs', 'archive', 'config']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def initialize_data_files():
    """Initialize empty data files if they don't exist."""
    data_files = {
        'upcoming.json': [],
        'results.json': [],
        'scrape_state.json': {
            'results_offset': 0,
            'enriched_match_ids': {}
        }
    }
    
    for filename, default_content in data_files.items():
        if not os.path.exists(filename):
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(default_content, f, indent=2)
            print(f"✅ Created: {filename}")
        else:
            print(f"📁 Exists: {filename}")

def test_flaresolverr():
    """Test FlareSolverr setup."""
    print("🐳 Testing FlareSolverr setup...")
    
    try:
        # Try to start FlareSolverr container
        subprocess.run([
            'docker', 'run', '-d', '--name', 'flaresolverr-test', 
            '-p', '8191:8191', 'flaresolverr/flaresolverr:latest'
        ], check=True, capture_output=True)
        
        print("✅ FlareSolverr container started successfully")
        
        # Clean up test container
        subprocess.run(['docker', 'stop', 'flaresolverr-test'], 
                      capture_output=True)
        subprocess.run(['docker', 'rm', 'flaresolverr-test'], 
                      capture_output=True)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start FlareSolverr: {e}")
        return False

def run_validation():
    """Run initial data validation."""
    print("🔍 Running data validation...")
    try:
        subprocess.run([sys.executable, 'scripts/validate_data.py'], check=True)
        print("✅ Data validation passed")
        return True
    except subprocess.CalledProcessError:
        print("⚠️ Data validation found issues (this is normal for initial setup)")
        return True  # Don't fail setup for validation issues

def print_next_steps():
    """Print next steps for the user."""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Start FlareSolverr container:")
    print("   docker run -d --name flaresolverr -p 8191:8191 flaresolverr/flaresolverr:latest")
    print("\n2. Run data collection:")
    print("   python datagatherer_odds.py      # Collect betting odds")
    print("   python datagatherer_results.py   # Collect match results")
    print("\n3. Generate reports:")
    print("   python scripts/generate_summary.py")
    print("   python scripts/quality_report.py")
    print("\n4. Enable GitHub Actions:")
    print("   - Push to GitHub repository")
    print("   - Enable Actions in repository settings")
    print("   - Automation will start automatically")
    print("\n📚 Documentation:")
    print("   - README.md: Complete documentation")
    print("   - config/automation_config.json: Configuration options")
    print("   - logs/: Execution logs and debugging info")

def main():
    """Main setup function."""
    print("🚀 CS:GO/CS2 Data Collection Setup")
    print("=" * 40)
    
    success = True
    
    # Check requirements
    if not check_python_version():
        success = False
    
    if not check_docker():
        success = False
    
    if not success:
        print("\n❌ Setup failed due to missing requirements")
        sys.exit(1)
    
    # Setup steps
    create_directories()
    
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    initialize_data_files()
    
    # Optional tests
    test_flaresolverr()
    run_validation()
    
    print_next_steps()

if __name__ == "__main__":
    main()