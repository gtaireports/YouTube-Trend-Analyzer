import sys
import os

# Add src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# Import the app module from src
from app import *

# The app will run automatically since all Streamlit commands are executed when the file is imported
