import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load the data
df = pd.read_csv('processed_data.csv')

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date']).dt.date

# Streamlit app layout
st.title('新聞標題分析 Dashboard')

# Sidebar filters
st.sidebar.header('篩選選項')
selected_press = st.sidebar.multiselect('選擇媒體', options=df['Press'].unique(), default=df['Press'].unique())
start_date, end_date = st.sidebar.date_input('選擇日期範圍', [datetime.strptime("2018-01-01", '%Y-%m-%d'), df['Date'].max()])
if not start_date:
    start_date = df['Date'].min()
if not end_date:
    end_date = df['Date'].max()

# Filter data based on selections
mask = (df['Press'].isin(selected_press)) & (df['Date'] >= start_date) & (df['Date'] <= end_date)
filtered_df = df[mask]

# Display interactive charts

# Clickbait Ratio by Category Bar Chart
st.header('各類別誘餌式標題比例')
clickbait_ratio_by_category = (
    filtered_df.groupby('Category')['IsClickbait'].mean().reset_index()
)
fig_clickbait_category = px.bar(clickbait_ratio_by_category, x='Category', y='IsClickbait', title='各類別誘餌式標題比例')
st.plotly_chart(fig_clickbait_category)

# Emotional Title Time Series Chart
st.header('標題情緒性隨時間變化')
emotional_timeseries = (
    filtered_df.groupby('Date')['emotional'].mean().reset_index()
)
fig_emotional_timeseries = px.line(emotional_timeseries, x='Date', y='emotional', title='標題情緒性隨時間變化')
st.plotly_chart(fig_emotional_timeseries)

# Clickbait Ratio by Press Bar Chart
st.header('不同媒體的誘餌式標題比例')
clickbait_ratio_by_press = (
    filtered_df.groupby('Press')['IsClickbait'].mean().reset_index()
)
fig_clickbait_press = px.bar(clickbait_ratio_by_press, x='Press', y='IsClickbait', title='不同媒體的誘餌式標題比例')
st.plotly_chart(fig_clickbait_press)
