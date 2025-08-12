import mobile_notice 
import streamlit as st 
import sys 
import os 
 
# Add current directory to Python path 
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
 
# Import and run the main app 
try: 
    exec(open('app.py').read()) 
except Exception as e: 
    st.error(f"Error loading app: {e}") 
