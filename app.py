import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
# import matplotlib.pyplot as plt
# plt.rcParams['font.family'] = 'Microsoft JhengHei'

st.set_page_config(
    page_title="新聞標題分析: Clickbait",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# custom_theme = """
# [theme]
# base="dark"
# primaryColor="#b04bff"
# """

@st.cache_data
def GetProcessedData(file):
    df = pd.read_csv(file)
    # Convert 'Date' column to datetime
    # df = df.iloc[:,1:]
    del df['Unnamed: 0']
    # df.set_index('Date', inplace=True)
    # st.write(df.head())
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = df[df['Date'] >= date(2017,12,31)]
    df.sort_values(by='Date', inplace=True)
    return df

# select date here
@st.cache_data
def SelectDate(df, start_date, end_date):
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

def PressTimePlot(df, selected_presses):
    fig = px.line(title='Clickbait Ratio: Press')
    df_filtered = df[df['Press'].isin(selected_presses)]
    for press, group in df_filtered.groupby('Press'):
        # Monthly average
        Monthly = group.groupby('Date')['IsClickbait'].mean()
        Monthly.index = pd.to_datetime(Monthly.index)
        Monthly = Monthly.resample('M').mean()
        Monthly = Monthly.rolling(4).mean()
        # fig.add_trace(px.line(Monthly, x=Monthly.index, y=Monthly.values, hover_name=press).data[0])
        fig.add_trace(px.line(Monthly, x=Monthly.index, y=Monthly.values).data[0])

    fig.update_layout(xaxis_title='Time (Monthly)',yaxis_title='Clickbait Ratio', legend_title='Press')
    # Customize the layout
    return st.plotly_chart(fig)

def CategoryTimePlot(df, selected_categories):
    fig = px.line(title='Clickbait Ratio: Category')
    df_filtered = df[df['Category'].isin(selected_categories)]
    for category, group in df_filtered.groupby("Category"):
        Monthly = group.groupby('Date')['IsClickbait'].mean()
        Monthly.index = pd.to_datetime(Monthly.index)
        Monthly = Monthly.resample('M').mean()
        Monthly = Monthly.rolling(4).mean()
        fig.add_trace(px.line(Monthly, x=Monthly.index, y=Monthly.values).data[0])
        # next line cause error
        # fig.add_trace(px.line(Monthly, x=Monthly.index, y=Monthly.values, name=category, line_dash='dash').data[0])
    fig.update_layout(xaxis_title='Time (Monthly)', yaxis_title='Clickbait Ratio', legend_title='Category')
    return st.plotly_chart(fig)

# Load the data
df = GetProcessedData('processed_data.csv')

media_options = df['Press'].unique().tolist()
Category_options = ['politics','finance','entertainment','health','life','tech','global']

def run():
    # Sidebar filters
    with st.sidebar:
        st.header('篩選選項')
        selected_presses = st.multiselect('選擇媒體', media_options, default=df['Press'].unique())
        selected_categories = st.multiselect("Select Categories", Category_options, default=df['Category'].unique())
        start_date = st.date_input('開始日期', df['Date'].min())
        end_date = st.date_input('結束日期', df['Date'].max())
    st.title('新聞標題分析 Dashboard')
    # Filter data based on selections
    # Since the category,press effect each others, move the selection into plot function
    filtered_df = SelectDate(df, start_date, end_date)
    st.subheader('篩選日期後的資料格式')
    if st.checkbox('顯示篩選後的數據'):
        st.write(filtered_df.head())

    t1, t2 = st.tabs(["Pingru", "Ding"])
    with t1:
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
    with t2:
        st.header('新畫的圖')
        st.write('遇到問題:無法用plotly.express標註每條線的hover_name,color等資訊。')
        st.write("ValueError: Value of 'hover_name' is not the name of a column in 'data_frame'. Expected one of ['IsClickbait'] but received: ETToday")
        st.write('error in line 48, in PressTimePlot')
        PressTimePlot(filtered_df, selected_presses)
        CategoryTimePlot(filtered_df, selected_categories)

if __name__ == "__main__":
    run()