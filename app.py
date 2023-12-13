import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Load the data
df = pd.read_csv('processed_data.csv')

# Convert 'Date' column to datetime
df['Date'] = pd.to_datetime(df['Date']).dt.date

# Streamlit dashboard layout
st.title('新聞標題分析 Dashboard')

# Sidebar for user inputs
st.sidebar.header('篩選選項')

# Date range selector
start_date = st.sidebar.date_input('開始日期', df['Date'].min())
end_date = st.sidebar.date_input('結束日期', df['Date'].max())

# Media source selector
media_options = df['Press'].unique().tolist()
selected_media = st.sidebar.multiselect('媒體來源', options=media_options, default=media_options)

# Filter the dataset based on the selection
filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date) & (df['Press'].isin(selected_media))]

# Display interactive table with the filtered data
if st.checkbox('顯示篩選後的數據'):
    st.write(filtered_df)

# Create and display charts with responsive layout
# Bar chart for Clickbait Ratio by Category
st.header('各類別誘餌式標題比例')
clickbait_ratio_by_category = filtered_df.groupby('Category')['IsClickbait'].mean().reset_index()
fig_clickbait_category = px.bar(clickbait_ratio_by_category, x='Category', y='IsClickbait', title='各類別誘餌式標題比例')
fig_clickbait_category.update_layout(autosize=True, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_clickbait_category, use_container_width=True)

# Time series chart for Emotional Titles
st.header('情緒性標題的時間序列圖')
time_series_emotional = filtered_df.groupby('Date')['emotional'].mean().reset_index()
fig_time_series_emotional = px.line(time_series_emotional, x='Date', y='emotional', title='情緒性標題的時間趨勢')
fig_time_series_emotional.update_layout(autosize=True, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_time_series_emotional, use_container_width=True)

# Bar chart for Interrogative Titles by Category
st.header('詢問性標題的長條圖')
interrogative_titles_by_category = filtered_df.groupby('Category')['interrogative'].mean().reset_index()
fig_interrogative_category = px.bar(interrogative_titles_by_category, x='Category', y='interrogative', title='各類別詢問性標題比例')
fig_interrogative_category.update_layout(autosize=True, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_interrogative_category, use_container_width=True)
