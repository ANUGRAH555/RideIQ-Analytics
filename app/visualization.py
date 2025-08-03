import os
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import folium
from streamlit_folium import st_folium

# Utility to ensure 'plots/' exists
def ensure_plots_dir():
    os.makedirs("plots", exist_ok=True)

# 1. Line Plot (Rides per Day)
def plot_rides_per_day(rides_per_day):
    ensure_plots_dir()
    fig, ax = plt.subplots(figsize=(8, 4))
    rides_per_day.plot(kind='line', marker='o', color='#C71585', ax=ax)
    ax.set_title("Rides per Day")
    ax.set_xlabel("Date")
    ax.set_ylabel("No. of Rides")
    fig.savefig("plots/rides_per_day.png", bbox_inches='tight')
    st.pyplot(fig)

# 2. Bar Plot (Hourly Distribution)
def plot_hourly_distribution(rides_per_hour):
    ensure_plots_dir()
    fig, ax = plt.subplots(figsize=(8, 4))
    rides_per_hour.plot(kind='bar', color='orange', ax=ax)
    ax.set_title("Hourly Ride Distribution")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Number of Rides")
    fig.savefig("plots/rides_per_hour.png", bbox_inches='tight')
    st.pyplot(fig)

# 3. Pie Chart (Ride Type Distribution)
def plot_ride_type_distribution(ride_type_distribution):
    ensure_plots_dir()
    fig, ax = plt.subplots()
    ride_type_distribution.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_ylabel('')
    ax.set_title("Ride Type Distribution")
    fig.savefig("plots/ride_type_distribution.png", bbox_inches='tight')
    st.pyplot(fig)

# 4. Histogram (Fare & Distance)
def plot_histograms(df):
    ensure_plots_dir()
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.histplot(df['fare'], bins=20, ax=axes[0], color='green')
    axes[0].set_title("Fare Distribution")
    sns.histplot(df['distance_km'], bins=20, ax=axes[1], color='purple')
    axes[1].set_title("Distance Distribution")
    fig.savefig("plots/histograms.png", bbox_inches='tight')
    st.pyplot(fig)

# 5. Scatter Plot (Fare vs Distance)
def plot_fare_vs_distance(df):
    ensure_plots_dir()
    fig = px.scatter(df, x='distance_km', y='fare', title="Fare vs Distance", color='fare')
    fig.write_image("plots/fare_vs_distance.png")
    st.plotly_chart(fig)

# 6. Revenue Trend Line Chart
def plot_revenue_trend(revenue_per_day):
    ensure_plots_dir()
    fig, ax = plt.subplots(figsize=(8, 4))
    revenue_per_day.plot(kind='line', marker='o', color='red', ax=ax)
    ax.set_title("Revenue Per Day")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Revenue (₹)")
    fig.savefig("plots/revenue_per_day.png", bbox_inches='tight')
    st.pyplot(fig)

# 7. Correlation Heatmap
def plot_correlation_heatmap(df):
    ensure_plots_dir()
    corr = df[['fare', 'distance_km', 'duration_mins']].corr()
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Correlation Heatmap")
    fig.savefig("plots/correlation_heatmap.png", bbox_inches='tight')
    st.pyplot(fig)

# 8. Bar Chart (Top Locations)
def plot_top_locations(top_pickup, top_drop):
    ensure_plots_dir()
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    top_pickup.plot(kind='bar', color='blue', ax=axes[0])
    axes[0].set_title("Top Pickup Locations")
    top_drop.plot(kind='bar', color='green', ax=axes[1])
    axes[1].set_title("Top Drop Locations")
    fig.savefig("plots/top_locations.png", bbox_inches='tight')
    st.pyplot(fig)
