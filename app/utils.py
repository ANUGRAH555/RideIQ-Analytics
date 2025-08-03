import pandas as pd
import streamlit as st

# ------------------------------------------------------------
# Data Cleaning Part
# ------------------------------------------------------------
def clean_data(df):
    # 1: Remove duplicates
    df.drop_duplicates(inplace=True)

    # 2: Handle missing values
    if 'fare' in df.columns:
        df['fare'].fillna(df['fare'].median(), inplace=True)
    if 'distance_km' in df.columns:
        df['distance_km'].fillna(0, inplace=True)
    if 'ride_type' in df.columns:
        df['ride_type'].fillna('Unknown', inplace=True)

    # 3: Clean Date Column
    if 'ride_date' in df.columns:
        df['ride_date'] = pd.to_datetime(df['ride_date'], errors='coerce')
        df = df.dropna(subset=['ride_date'])
        df = df[df['ride_date'] <= pd.Timestamp.today()]
        df['ride_date_display'] = df['ride_date'].dt.strftime('%Y-%m-%d')

    # 4: Clean Time Column
    if 'ride_time' in df.columns:
        df['ride_time'] = pd.to_datetime(df['ride_time'], format='%H:%M:%S', errors='coerce')
        df = df.dropna(subset=['ride_time'])
        df['hour'] = df['ride_time'].dt.hour
        df['ride_time_display'] = df['ride_time'].dt.strftime('%H:%M:%S')

    # 5: Clean Text Columns
    if 'pickup_location' in df.columns:
        df['pickup_location'] = df['pickup_location'].astype(str).str.strip().str.title()
    if 'drop_location' in df.columns:
        df['drop_location'] = df['drop_location'].astype(str).str.strip().str.title()

    # 6: Numeric Columns Validation
    if 'fare' in df.columns:
        df = df[df['fare'] > 0]
    if 'distance_km' in df.columns:
        df = df[df['distance_km'] > 0]

    # 7: Remove Outliers
    if 'fare' in df.columns:
        df = df[df['fare'] < 10000]
    if 'distance_km' in df.columns:
        df = df[df['distance_km'] < 500]

    # 8: Add Derived Columns
    if 'ride_date' in df.columns:
        df['day_of_week'] = df['ride_date'].dt.day_name()

    return df


# ------------------------------------------------------------
# Data Analysis Part
# ------------------------------------------------------------
def perform_analysis(df):
    results = {}

    # 1. Key Metrics
    results['total_rides'] = len(df)
    results['avg_fare'] = df['fare'].mean()
    results['max_fare'] = df['fare'].max()
    results['min_fare'] = df['fare'].min()
    results['avg_distance'] = df['distance_km'].mean()
    results['total_revenue'] = df['fare'].sum()
    results['peak_hour'] = df['hour'].mode()[0] if 'hour' in df.columns else None

    # 2. Ride Trends
    results['rides_per_day'] = df.groupby('ride_date').size()
    results['rides_per_month'] = df.groupby(df['ride_date'].dt.to_period('M')).size()
    results['rides_per_day_of_week'] = df.groupby('day_of_week').size()
    results['weekend_vs_weekday'] = (
        df['day_of_week']
        .apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')
        .value_counts()
    )
    results['rides_per_hour'] = df.groupby('hour').size() if 'hour' in df.columns else pd.Series()

    # 3. Ride Types and Location
    results['ride_type_distribution'] = df['ride_type'].value_counts()
    results['top_pickup_locations'] = df['pickup_location'].value_counts().head(5)
    results['top_drop_locations'] = df['drop_location'].value_counts().head(5)

    # 4. Fare Analysis
    results['fare_stats'] = df['fare'].describe()
    results['avg_fare_by_ride_type'] = df.groupby('ride_type')['fare'].mean()
    results['avg_fare_by_day_of_week'] = df.groupby('day_of_week')['fare'].mean()

    # 5. Distance Analysis
    results['distance_stats'] = df['distance_km'].describe()
    results['avg_distance_by_ride_type'] = df.groupby('ride_type')['distance_km'].mean()
    results['top_longest_trips'] = df.nlargest(5, 'distance_km')[
        ['ride_date', 'pickup_location', 'drop_location', 'distance_km', 'fare']
    ]

    # 6. Combined Insights
    results['fare_distance_correlation'] = df[['fare', 'distance_km']].corr()
    results['revenue_per_day'] = df.groupby('ride_date')['fare'].sum()
    results['rides_by_pickup_ride_type'] = (
        df.groupby(['pickup_location', 'ride_type'])
        .size()
        .sort_values(ascending=False)
        .head(5)
    )
    results['avg_fare_per_hour'] = df.groupby('hour')['fare'].mean() if 'hour' in df.columns else pd.Series()

    return results
