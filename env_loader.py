import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    """
    Load environment variables from .env file.
    
    Order of precedence:
    1. Existing environment variables
    2. .env file in current directory
    3. .env file in user's home directory
    """
    # Try loading from current directory
    if os.path.exists('.env'):
        load_dotenv('.env')
        print("Loaded API key from .env file in current directory")
        return True
    
    # Try loading from home directory
    home_env = os.path.join(str(Path.home()), '.env')
    if os.path.exists(home_env):
        load_dotenv(home_env)
        print(f"Loaded API key from {home_env}")
        return True
    
    # Check if the API key is already set in the environment
    if 'MATERIALS_PROJECT_API_KEY' in os.environ:
        print("Using Materials Project API key from environment variables")
        return True
    
    print("Warning: MATERIALS_PROJECT_API_KEY environment variable not found")
    print("Please set your API key by:")
    print("  1. Creating a .env file with MATERIALS_PROJECT_API_KEY=your_key")
    print("  2. Or setting it manually: export MATERIALS_PROJECT_API_KEY=your_key")
    print("\nGet your API key at: https://materialsproject.org/dashboard")
    
    return False