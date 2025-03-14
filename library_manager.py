import streamlit as st # type: ignore
import pandas as pd # type: ignore
import json
import os
import datetime
import random
import plotly.express as px # type: ignore
import plotly.graph_objects as go # type: ignore
from streamlit_lottie import st_lottie # type: ignore
import requests # type: ignore

# Load Lottie Animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_books = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_x62chJ.json")

# Set Page Configuration
st.set_page_config(
    page_title="Personal Library System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Styling
st.markdown(
    """
    <style>
    .main-header { font-size: 3rem; color: #0D47A1; text-align: center; font-weight: 800; }
    .sub-header { font-size: 1.5rem; color: #1976D2; font-weight: 600; margin-bottom: 10px; }
    .book-card { background: #E3F2FD; border-radius: 10px; padding: 15px; margin: 10px 0; box-shadow: 2px 4px 10px rgba(0,0,0,0.2); }
    .sidebar .css-1d391kg { background-color: #0D47A1; }
    </style>
    """, unsafe_allow_html=True
)

# Initialize Library Storage
if 'library' not in st.session_state:
    st.session_state.library = []

# Add a Book Function
def add_book():
    st.markdown("<h2 class='sub-header'>📖 Add a New Book</h2>", unsafe_allow_html=True)
    title = st.text_input("Book Title:")
    author = st.text_input("Author:")
    year = st.number_input("Publication Year:", min_value=1800, max_value=2100, step=1)
    genre = st.text_input("Genre:")
    read_status = st.radio("Read Status:", ["Read", "Unread"], horizontal=True)
    
    if st.button("📚 Add Book", use_container_width=True):
        book = {"title": title, "author": author, "year": year, "genre": genre, "read": read_status == "Read"}
        st.session_state.library.append(book)
        st.success(f"✅ Book '{title}' added successfully!")

# Remove a Book Function
def remove_book():
    st.markdown("<h2 class='sub-header'>🗑 Remove a Book</h2>", unsafe_allow_html=True)
    title = st.text_input("Enter book title to remove:")
    
    if st.button("🗑 Remove Book", use_container_width=True):
        st.session_state.library = [b for b in st.session_state.library if b["title"].lower() != title.lower()]
        st.warning(f"❌ Book '{title}' removed.")

# Search a Book Function
def search_book():
    st.markdown("<h2 class='sub-header'>🔎 Search a Book</h2>", unsafe_allow_html=True)
    search_term = st.text_input("Enter title or author:")
    
    if st.button("🔍 Search", use_container_width=True):
        results = [b for b in st.session_state.library if search_term.lower() in b["title"].lower() or search_term.lower() in b["author"].lower()]
        
        if results:
            for book in results:
                st.markdown(f"<div class='book-card'><strong>{book['title']}</strong> - {book['author']} ({book['year']}) [{book['genre']}]</div>", unsafe_allow_html=True)
        else:
            st.error("❌ No books found.")

# Display All Books Function
def display_all_books():
    st.markdown("<h2 class='sub-header'>📚 All Books in Library</h2>", unsafe_allow_html=True)
    if not st.session_state.library:
        st.warning("⚠️ No books in the library.")
    else:
        for book in st.session_state.library:
            status = "✅ Read" if book["read"] else "❌ Unread"
            st.markdown(f"<div class='book-card'><strong>{book['title']}</strong> - {book['author']} ({book['year']}) [{book['genre']}] - {status}</div>", unsafe_allow_html=True)

# Display Library Statistics
def display_statistics():
    st.markdown("<h2 class='sub-header'>📊 Library Statistics</h2>", unsafe_allow_html=True)
    total_books = len(st.session_state.library)
    read_books = sum(book["read"] for book in st.session_state.library)
    unread_books = total_books - read_books
    
    if total_books > 0:
        fig = go.Figure(go.Pie(labels=["Read Books", "Unread Books"], values=[read_books, unread_books], hole=0.4))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("📉 No books to display statistics.")

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2232/2232688.png", width=150)
st.sidebar.title("📖 Library Menu")
menu = ["Home", "Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Library Statistics"]
choice = st.sidebar.radio("Navigate", menu)

# Main Content
def main():
    if choice == "Home":
        st.markdown("<h1 class='main-header'>📚 Personal Library Management</h1>", unsafe_allow_html=True)
        if lottie_books:
            st_lottie(lottie_books, height=300)
    elif choice == "Add a Book":
        add_book()
    elif choice == "Remove a Book":
        remove_book()
    elif choice == "Search for a Book":
        search_book()
    elif choice == "Display All Books":
        display_all_books()
    elif choice == "Library Statistics":
        display_statistics()

if __name__ == "__main__":
    main()

