import os
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

import streamlit as st
from streamlit.web.server import Server
from streamlit.web.cli import main

# Configure Streamlit for Vercel
os.environ['STREAMLIT_SERVER_PORT'] = '8501'
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'

# Vercel serverless function handler
def handler(request):
    """Vercel serverless function handler for Streamlit"""
    try:
        # Set up environment
        os.environ['REQUEST_METHOD'] = request.method
        os.environ['QUERY_STRING'] = request.query_string.decode('utf-8')
        
        # Run Streamlit
        sys.argv = ['streamlit', 'run', 'src/streamlit_app.py', '--server.port=8501', '--server.address=0.0.0.0']
        
        # Initialize and run the app
        main()
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error: {str(e)}',
            'headers': {
                'Content-Type': 'text/plain'
            }
        }

# For local testing
if __name__ == "__main__":
    class MockRequest:
        method = "GET"
        query_string = b""
    
    handler(MockRequest())
