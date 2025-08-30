"""
========================================================================
                    auth.py - מערכת אימות יפה עם רישום והתחברות
========================================================================
מערכת רישום והתחברות פשוטה ויפה עבור DataBot Analytics
תומכת ברישום עם email וסיסמה, התחברות מאובטחת וממשק משתמש מודרני
"""

import streamlit as st
import json
import os
import hashlib
import re
from datetime import datetime

# File to store user data
USERS_FILE = "users.json"

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def register_user(email, password, name):
    """Register new user"""
    if not validate_email(email):
        return False, "Invalid email format"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    users = load_users()
    if email in users:
        return False, "User already exists"
    
    users[email] = {
        "name": name,
        "password": hash_password(password),
        "created_at": datetime.now().isoformat()
    }
    save_users(users)
    return True, "Registration successful"

def authenticate_user(email, password):
    """Authenticate user"""
    users = load_users()
    if email not in users:
        return False, "User not found"
    
    if users[email]["password"] != hash_password(password):
        return False, "Incorrect password"
    
    return True, users[email]["name"]

def show_auth_ui():
    """Show beautiful authentication UI"""
    
    # Custom CSS for beautiful styling
    st.markdown("""
    <style>
    .auth-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        color: white;
    }
    .auth-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .auth-form {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.9);
        border: none;
        border-radius: 8px;
        color: #333;
        font-size: 1rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 0;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(255,107,107,0.3);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="auth-title">🚀 DataBot Analytics</h1>', unsafe_allow_html=True)
    
    # Add back button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("← Back to App"):
            st.session_state.show_auth_ui = False
            st.rerun()
    
    # Tab selection
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login", key="login_tab"):
            st.session_state.auth_tab = "login"
    with col2:
        if st.button("📝 Register", key="register_tab"):
            st.session_state.auth_tab = "register"
    
    # Initialize tab
    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "login"
    
    st.markdown('<div class="auth-form">', unsafe_allow_html=True)
    
    if st.session_state.auth_tab == "login":
        show_login_form()
    else:
        show_register_form()
    
    st.markdown('</div></div>', unsafe_allow_html=True)

def show_login_form():
    """Show login form"""
    st.markdown("### 🔐 Welcome Back!")
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("🚀 Login")
        
        if submitted:
            if email and password:
                success, message = authenticate_user(email, password)
                if success:
                    st.session_state.authenticated = True
                    st.session_state.user_email = email
                    st.session_state.user_name = message
                    st.session_state.show_auth_ui = False  # Hide auth UI
                    st.success(f"Welcome back, {message}! 🎉")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("❌ Please fill in all fields")

def show_register_form():
    """Show registration form"""
    st.markdown("### 🎯 Join DataBot!")
    
    with st.form("register_form"):
        name = st.text_input("👤 Full Name", placeholder="Enter your full name")
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔒 Password", type="password", placeholder="Choose a strong password")
        password_confirm = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
        submitted = st.form_submit_button("✨ Create Account")
        
        if submitted:
            if name and email and password and password_confirm:
                if password != password_confirm:
                    st.error("❌ Passwords don't match")
                else:
                    success, message = register_user(email, password, name)
                    if success:
                        st.success(f"✅ {message}! Please login now.")
                        st.session_state.auth_tab = "login"
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
            else:
                st.error("❌ Please fill in all fields")

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)

def logout():
    """Logout user"""
    st.session_state.authenticated = False
    st.session_state.user_email = None
    st.session_state.user_name = None
    st.rerun()

def show_user_info():
    """Show logged in user info"""
    if check_authentication():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**👋 Welcome, {st.session_state.user_name}!**")
        with col2:
            if st.button("🚪 Logout"):
                logout()