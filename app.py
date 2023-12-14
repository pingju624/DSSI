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
# """

@st.cache_data
def GetProcessedData(file):
    df = pd.read_csv(file)
    del df['Unnamed: 0']
    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = df[df['Date'] >= date(2017,12,31)]
    df.sort_values(by='Date', inplace=True)
    return df

# select date here
@st.cache_data
def SelectDate(df, start_date, end_date):
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

def PressTimePlot(df, selected_presses):
    global media_color_map

    df_filtered = df[df['Press'].isin(selected_presses)]
    df_filtered['MonthYear'] = df_filtered['Date'].astype(str).str[:7]
    df_filtered = df_filtered.groupby(['Press', 'MonthYear']).agg({'IsClickbait': 'mean'}).reset_index()
    fig = px.line(df_filtered, x='MonthYear', y='IsClickbait',
                  color='Press', color_discrete_map=media_color_map, title='各媒體誘餌式標題比例')
    fig.update_layout(xaxis_title='Time (Monthly)',yaxis_title='Clickbait Ratio', legend_title='新聞媒體')
    # Customize the layout
    return st.plotly_chart(fig)

def CategoryTimePlot(df, selected_categories):
    global category_color_map

    df_filtered = df[df['Category'].isin(selected_categories)]
    df_filtered['MonthYear'] = df_filtered['Date'].astype(str).str[:7]
    df_filtered = df_filtered.groupby(['Category', 'MonthYear']).agg({'IsClickbait': 'mean'}).reset_index()
    fig = px.line(df_filtered, x='MonthYear', y='IsClickbait',
                  color='Category', color_discrete_map=category_color_map, title='各類別新聞誘餌式比例')
    fig.update_layout(xaxis_title='Time (Monthly)', yaxis_title='Clickbait Ratio', legend_title='新聞類別')
    return st.plotly_chart(fig)

def BaitMethodTimePlot(df, selected_baits):
    global bait_color_map

    df_filtered = df
    df_filtered['MonthYear'] = df['Date'].astype(str).str[:7]
    df_filtered = df_filtered.groupby('MonthYear')[selected_baits].mean().reset_index()
    df_melted = pd.melt(df_filtered, id_vars=['MonthYear'], value_vars=selected_baits, var_name='BaitType', value_name='BaitRatio')
    fig = px.line(df_melted, x='MonthYear', y='BaitRatio',
                  color='BaitType', color_discrete_map=bait_color_map, title='各誘餌式方法占全部新聞比例')
    fig.update_layout(xaxis_title='Time (Monthly)', yaxis_title='Bait Type Ratio', legend_title='釣魚方法')
    return st.plotly_chart(fig)

# Load the data
df = GetProcessedData('processed_data.csv')

# 因為會需要用到map，所以直接打出媒體，而非每次計算
# media_options = df['Press'].unique().tolist()
media_options = ['ETToday','報導者','今日新聞','TVBS','Storm Media','NewsLens','NewYorkTimes','TTVnews','鏡新聞','壹蘋新聞','三立','中天']
media_colors = ['#FFABAB','#B7BCC6','#FFD700','#28FF28','#FF0000','#83C9FF','#6D3FC0','#1AFD9C','#00477D','#FFA500','#228B22','#2828FF']
media_color_map = dict(zip(media_options, media_colors))
category_options = ['politics','finance','entertainment','health','life','tech','global']
category_colors = ['#FFFFFF','#FFD700','#FF0000','#FF69B4','#0D33FF','#00CED1','#7FFF00']
category_color_map = dict(zip(category_options, category_colors))
bait_options = ['forward-referencing','emotional','interrogative','surprise','ellipsis','list','how_to','interjection','spillthebeans','gossip','ending_words','netizen','exaggerated','uncertainty']
bait_colors = media_colors + ['#D94DFF', '#FFDAB9']
bait_color_map = dict(zip(bait_options, bait_colors))
# st.write(len(bait_colors), len(bait_options), len(media_colors))

def run():
    # Sidebar filters
    with st.sidebar:
        st.header('篩選選項')
        start_date = st.date_input('開始日期', df['Date'].min())
        end_date = st.date_input('結束日期', df['Date'].max())
        selected_presses = st.multiselect('選擇媒體', media_options, default=df['Press'].unique())
        selected_categories = st.multiselect("選擇新聞類別", category_options, default=df['Category'].unique())
        selected_bait = st.multiselect("選擇釣魚方法", bait_options, default=bait_options)
    st.title('新聞標題分析 Dashboard')
    # Filter data based on selections
    # Since the category,press effect each others, move the selection into plot function
    filtered_df = SelectDate(df, start_date, end_date)
    st.subheader('篩選日期後的資料格式')
    if st.checkbox('顯示篩選後的數據'):
        st.write(filtered_df.head())

    tab1, tab2, tab3 = st.tabs(["Pingru", "Ding", "Iting"])
    with tab1:
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
    with tab2:
        st.header('時間序列圖')
        PressTimePlot(filtered_df, selected_presses)
        CategoryTimePlot(filtered_df, selected_categories)
        BaitMethodTimePlot(filtered_df, selected_bait)
    with tab3:
        st.write('test')

if __name__ == "__main__":
    run()
