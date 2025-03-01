import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Constants
API_URL = "http://localhost:8000"  # FastAPI server address

st.set_page_config(
    page_title="URL Shortener",
    page_icon="🔗",
    layout="centered"
)

# Title and description
st.title("🔗 URL Shortener")
st.write("Enter a URL to create a shortened version.")

# Function to create a shortened URL
def create_short_url(original_url):
    response = requests.post(
        f"{API_URL}/api/shorten/",
        json={"original_url": original_url}
    )
    return response.json() if response.status_code == 200 else None

# Function to get URL statistics
def get_url_stats(short_url):
    response = requests.get(f"{API_URL}/api/stats/{short_url}")
    return response.json() if response.status_code == 200 else None

# Function to get all URLs
def get_all_urls():
    response = requests.get(f"{API_URL}/api/urls/")
    return response.json() if response.status_code == 200 else []

# URL input form
with st.form("url_form"):
    url_input = st.text_input("Enter your URL (including http:// or https://)")
    submit_button = st.form_submit_button("Shorten URL")
    
    if submit_button and url_input:
        if not (url_input.startswith("http://") or url_input.startswith("https://")):
            st.error("URL must start with http:// or https://")
        else:
            result = create_short_url(url_input)
            if result:
                shortened_url = f"{API_URL}/{result['short_url']}"
                st.success("URL shortened successfully!")
                st.code(shortened_url)
                
                # Display QR code for the shortened URL
                st.write("Scan this QR code to access the URL:")
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={shortened_url}"
                st.image(qr_url)
            else:
                st.error("Failed to shorten URL. Please try again.")

# URL statistics section
st.header("URL Statistics")
st.write("View statistics for your shortened URLs")

tab1, tab2 = st.tabs(["Single URL Stats", "All URLs"])

with tab1:
    short_code = st.text_input("Enter the short code to view statistics", key="stats_input")
    
    if st.button("Get Statistics") and short_code:
        stats = get_url_stats(short_code)
        if stats:
            st.write(f"Original URL: {stats['original_url']}")
            st.write(f"Shortened URL: {API_URL}/{stats['short_url']}")
            st.write(f"Clicks: {stats['clicks']}")
            st.write(f"Created at: {stats['created_at']}")
        else:
            st.error("URL not found or an error occurred")

with tab2:
    if st.button("Refresh URL List"):
        urls = get_all_urls()
        if urls:
            # Create a DataFrame for better display
            df = pd.DataFrame([{
                "Original URL": url['original_url'],
                "Short URL": f"{API_URL}/{url['short_url']}",
                "Clicks": url['clicks'],
                "Created": url['created_at']
            } for url in urls])
            
            st.dataframe(df)
        else:
            st.info("No URLs found or an error occurred")