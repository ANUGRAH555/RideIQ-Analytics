import streamlit as st
import pandas as pd
import os
import requests
from utils import clean_data, perform_analysis
from visualization import (
    plot_rides_per_day, plot_hourly_distribution, plot_ride_type_distribution,
    plot_histograms, plot_fare_vs_distance, plot_revenue_trend,
    plot_correlation_heatmap, plot_top_locations
)
from pdf_generator import generate_pdf_report

# -------------------------------------------------
# Page Config with Dark Theme
# -------------------------------------------------
st.set_page_config(
    page_title="RideIQ – Intelligent Ride Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for dark mode and styling
st.markdown("""
    <style>
    html, body, [class*="css"]  {
        background-color: #0e1117;
        color: #e1e1e1;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #C71585;
    }
    .stButton > button {
        background-color: #C71585;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.2em;
    }
    .stDownloadButton button {
        background-color: #444;
        color: white;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Animated Title
# -------------------------------------------------
st.markdown("""
    <h1 style='text-align: center; animation: pulse 2s infinite;'>🚖 RideIQ – <span style="color:#C71585">Intelligent Ride Analytics</span></h1>
    <style>
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.6; }
            100% { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Welcome Message / Feature Highlights
# -------------------------------------------------
st.markdown("""
### ✨ Welcome to RideIQ Dashboard
RideIQ is an intelligent and interactive platform that empowers users to:
            
- Upload or choose ride data
- Automatically clean and analyze your dataset,Visualize important trends and metrics
- Download beautiful summary reports in PDF format
            
Whether you're a data analyst, business owner, or student, RideIQ gives you the edge with actionable ride insights 🚀
""")

# -------------------------------------------------
# Sidebar - Data Source
# -------------------------------------------------
st.sidebar.header("📊 Select Data Source")
data_mode = st.sidebar.radio("Mode", ["Upload CSV", "Use Sample Dataset"])

df = None

# Upload CSV
if data_mode == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload Uber Ride Data", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success("✅ Uploaded successfully!")
            df = clean_data(df)
        except Exception as e:
            st.sidebar.error(f"❌ Failed to read file: {e}")
    else:
        st.sidebar.warning("📂 Please upload a CSV file.")

# Use Sample Dataset
elif data_mode == "Use Sample Dataset":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sample_dir = os.path.join(base_dir, "data")
    try:
        available_files = [f for f in os.listdir(sample_dir) if f.endswith(".csv")]
        if available_files:
            selected_file = st.sidebar.selectbox("Choose Sample File:", available_files)
            sample_path = os.path.join(sample_dir, selected_file)
            df = pd.read_csv(sample_path)
            df = clean_data(df)
            st.sidebar.success(f"✅ Loaded: {selected_file}")
        else:
            st.sidebar.warning("⚠️ No sample files in 'data/' folder.")
    except FileNotFoundError:
        st.sidebar.error("❌ 'data/' folder not found.")

# -------------------------------------------------
# Main Page Content
# -------------------------------------------------
if df is not None and not df.empty:
    st.subheader("📋 Dataset Preview")

    columns_to_show = [
        'ride_id', 'ride_date_display', 'ride_time_display',
        'pickup_location', 'drop_location',
        'fare', 'distance_km', 'ride_type', 'duration_mins', 'day_of_week']
    columns_to_show = [col for col in columns_to_show if col in df.columns]

    st.dataframe(df[columns_to_show].head(20), use_container_width=True)
    st.markdown(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")

    # Perform Analysis
    analysis = perform_analysis(df)

    # KPIs
    st.subheader("📌 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Rides", analysis['total_rides'])
    col2.metric("Avg Fare (₹)", round(analysis['avg_fare'], 2))
    col3.metric("Total Revenue (₹)", round(analysis['total_revenue'], 2))
    col4.metric("Peak Hour", analysis['peak_hour'])

    # Charts
    st.subheader("📊 Visualizations")

    st.subheader("1.📈 Rides Per Day")
    plot_rides_per_day(analysis['rides_per_day'])

    st.subheader("2.⏰ Hourly Ride Distribution")
    plot_hourly_distribution(analysis['rides_per_hour'])

    
    plot_ride_type_distribution(analysis['ride_type_distribution'])
    plot_histograms(df)
    plot_revenue_trend(analysis['revenue_per_day'])
    plot_fare_vs_distance(df)
    plot_top_locations(analysis['top_pickup_locations'], analysis['top_drop_locations'])
    plot_correlation_heatmap(df)

    # Auto Insights
    st.subheader("🔍 Auto Insights")
    avg_fare = df['fare'].mean() if 'fare' in df.columns else 0.0
    peak_hour = df['hour'].value_counts().idxmax() if 'hour' in df.columns and not df['hour'].empty else "N/A"
    popular_ride_type = df['ride_type'].value_counts().idxmax() if 'ride_type' in df.columns else "N/A"
    top_pickup = df['pickup_location'].value_counts().idxmax() if 'pickup_location' in df.columns else "N/A"
    top_drop = df['drop_location'].value_counts().idxmax() if 'drop_location' in df.columns else "N/A"
    highest_revenue_day = (
        df.groupby('ride_date')['fare'].sum().idxmax()
        if 'ride_date' in df.columns and 'fare' in df.columns else "N/A"
    )

    st.success(f"💸 Average Fare: ₹{avg_fare:.2f}")
    st.info(f"⏰ Peak Hour: {peak_hour}:00")
    st.success(f"🛺 Most Popular Ride: {popular_ride_type}")
    st.warning(f"📅 Highest Revenue Day: {highest_revenue_day}")
    st.info(f"📍 Top Pickup → Drop: {top_pickup} → {top_drop}")

    # PDF Report
    insights = [
        f"Average Fare: ₹{avg_fare:.2f}",
        f"Peak Ride Hour: {peak_hour}:00",
        f"Most Popular Ride Type: {popular_ride_type}",
        f"Highest Revenue Day: {highest_revenue_day}",
        f"Top Pickup: {top_pickup} → Top Drop: {top_drop}"
    ]
    plot_files = [
        "plots/rides_per_day.png", "plots/rides_per_hour.png",
        "plots/ride_type_distribution.png", "plots/histograms.png",
        "plots/revenue_per_day.png", "plots/fare_vs_distance.png",
        "plots/correlation_heatmap.png", "plots/top_locations.png"
    ]
    output_pdf = "RideIQ_Report.pdf"
    generate_pdf_report(analysis, insights, plot_files, output_path=output_pdf)

    with open(output_pdf, "rb") as f:
        pdf_data = f.read()
    st.download_button("📥 Download PDF Report", data=pdf_data, file_name=output_pdf, mime="application/pdf")

else:
    st.info("No dataset loaded yet. Please select a data source.")

# -------------------------------------------------
# Footer: Contact Info Section
# -------------------------------------------------
st.markdown("""
---
### 📞 Contact Me
- 🔗 [LinkedIn](https://www.linkedin.com/in/anugrah-pratap-singh-48249028b/)
- 💻 [GitHub](https://github.com/ANUGRAH555)
- ✉️ Email: anugrahcse12@gmail.com
- 📱 Phone: +91-7068464328
""", unsafe_allow_html=True)
