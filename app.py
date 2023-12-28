import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import numpy as np
from is_clickbait import is_clickbait

# 全域變數測試
# 因為會需要用到map，所以直接打出媒體，而非每次計算
# media_options = df['Press'].unique().tolist()
media_options = ['ETToday','報導者','今日新聞','TVBS','Storm Media','NewsLens','NewYorkTimes','TTVnews','鏡新聞','壹蘋新聞','三立','中天']
media_colors = ['#FFABAB','#B7BCC6','#FFD700','#28FF28','#FF0000','#83C9FF','#6D3FC0','#1AFD9C','#00477D','#FFA500','#228B22','#2828FF']
media_color_map = dict(zip(media_options, media_colors))
category_options = ['politics','finance','entertainment','health','life','tech','global']
category_colors = ['#B7BCC6','#FFD700','#FF0000','#FF69B4','#0D33FF','#00CED1','#7FFF00']
category_color_map = dict(zip(category_options, category_colors))
bait_options = ['forward-referencing','emotional','interrogative','surprise','ellipsis','list','how_to','interjection','spillthebeans','gossip','ending_words','netizen','exaggerated','uncertainty']
bait_colors = media_colors + ['#D94DFF', '#FFDAB9']
bait_color_map = dict(zip(bait_options, bait_colors))
alpha = 0.4 #移動平均最新資料的權重
criteria_list = [
        "前項指涉：(代名詞)'他', '他們', '你', '這'…",
        "問題式：'?!', '!', '?'",
        "刪節號：'......'",
        "how to：'如何', '該怎麼做', '該如何'",
        "感嘆詞：'嗯', '哎', '咦', '啊', '唉', '呦'",
        "爆料文體：'曝光', '自爆', '爆料', '再爆'",
        "群眾效果：包含'網'字(ex:「網」瘋傳)",
        "情緒性用詞：'瘋', '激', '慘', '哭', '酸', '諷', '飆罵', '怒批', '打臉'…",
        "驚奇：'居然', '竟然', '竟', '甚至', '沒想到', '驚'",
        "清單式：'十個', '三招'…",
        "八卦文體：'正妹', '老司機', '性感', '嫩', '型男'…",
        "句尾詞：'了'",
        "誇大：'最', '太', '狠', '極其', '非常', '神', '狂', '超'…",
        "不確定性：'傳', '瘋傳', '轉傳', '網傳', '誤傳', '疑', '恐'"]

st.set_page_config(
    page_title="新聞標題分析: Clickbait",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="expanded"
)

@st.cache_data
def GetProcessedData(file):
    df = pd.read_csv(file)
    try:
        del df['Unnamed: 0']
        # Convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        df = df[df['Date'] > date(2017,12,31)]
        df.sort_values(by='Date', inplace=True)
    except:
        pass
    return df

# select date here
@st.cache_data
def SelectDate(df, start_date, end_date):
    return df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Load the data
three_moth_df = GetProcessedData("panel_data_three_month.csv")
df = GetProcessedData("panel_data_weekly.csv")

#pingju's
def  media_count(df,selected_Categories,selected_Media):
    df_filtered = df[df['Press'].isin(selected_Media)]
    df_filtered = df_filtered[df_filtered['Category'].isin(selected_Categories)]
    df_filtered["Mean"] = df_filtered["IsClickbait"] / df_filtered["Count_News"]
    fig_clickbait_category = px.bar(df_filtered, x='Press', y='Count_News', color='Category', title='各類別新聞資料數',labels={'Mean':'Data Count'},barmode='group')
    fig_clickbait_category.update_layout(autosize=True)
    # 在 Streamlit 上顯示圖表
    st.plotly_chart(fig_clickbait_category, use_container_width=True)

def bait_count(df,selected_Media):
    df_filtered = df[df['Press'].isin(selected_Media)]
    df_group = df_filtered.groupby(["Press"]).sum().reset_index()
    df_group["Mean"] = df_group["IsClickbait"] / df_group["Count_News"]
    fig_clickbait_category = px.bar(df_group, x='Press', y='Mean', color='Mean', title='媒體間釣餌式標題比例',labels={'Mean':'Click-bait ratio'},barmode='group',hover_data={'Mean':':.2f'})
    fig_clickbait_category.update_traces(width=0.7)
    fig_clickbait_category.update_layout(autosize=True)
    # 在 Streamlit 上顯示圖表
    st.plotly_chart(fig_clickbait_category, use_container_width=True)
    
def  media_clickbait(df,selected_Categories,selected_Media):
    df_filtered = df[df['Press'].isin(selected_Media)]
    df_filtered = df_filtered[df_filtered['Category'].isin(selected_Categories)]
    df_filtered["Mean"] = df_filtered["IsClickbait"] / df_filtered["Count_News"]
    # df_filtered['Category'] = pd.Categorical(df_filtered['Category'], categories=category_order, ordered=True)
    # fig_clickbait_category = px.bar(df_filtered, x='Press', y='Mean', color='Category',color_discrete_map=category_color_map, title='各類別誘餌式標題比例',labels={'Mean':'Click bait ratio'},barmode='group')
    fig_clickbait_category = px.bar(df_filtered, x='Press', y='Mean', color='Category', title='各類別誘餌式標題比例',labels={'Mean':'Click bait ratio'},barmode='group',hover_data={'Mean':':.2f'})
    fig_clickbait_category.update_layout(autosize=True)
    # 在 Streamlit 上顯示圖表
    st.plotly_chart(fig_clickbait_category, use_container_width=True)
    
def category_bait_type(df,selected_Categories,selected_Bait):
    columns_to_aggregate = ["Count_News",'IsClickbait',*selected_Bait]

    aggregated_data = df.groupby(['Category'])[columns_to_aggregate].sum().reset_index()
    df_melted = aggregated_data.melt(id_vars=['Category', 'Count_News', 'IsClickbait'], value_vars=selected_Bait, var_name='Method', value_name='Method_Count')
    # Calculate the method percentage of the total news count
    df_melted['Method_Percentage'] = (df_melted['Method_Count'] / df_melted['Count_News'])
    
    df_melted = df_melted[df_melted['Category'].isin(selected_Categories)]
    
    # Create the scatter plot using Plotly Express
    fig = px.scatter(df_melted, x='Category', y='Method_Percentage',size='Method_Percentage',color='Method', color_discrete_map=bait_color_map,
                    hover_data={'Method_Percentage':':.2f'}, title='各誘餌方法佔類別比例')

    top_methods = df_melted.groupby('Category').apply(lambda x: x.nlargest(3, 'Method_Percentage')).reset_index(drop=True)
    for i in range(len(top_methods)):
        if (i+1)%3 ==1:y = -25
        elif (i+1)%3 ==2:y = -15
        else:y =5
        fig.add_annotation(
            x=top_methods.iloc[i]['Category'],
            y=top_methods.iloc[i]['Method_Percentage'],
            text=top_methods.iloc[i]['Method'],
            showarrow=True,
            arrowhead=0,
            ax=40,
            ay=y
        )

    fig.update_layout(autosize=True)
    # 在 Streamlit 上顯示圖表
    st.plotly_chart(fig, use_container_width=True)

# Ding & Iting: long term plot
def MediaTimePlot(df, selected_Media):
    From2018 = ['ETToday', '今日新聞', 'Storm Media', 'NewYorkTimes', 'NewsLens', 'TVBS', '報導者']
    df_filtered = df[df['Press'].isin(From2018)]
    df_filtered = df_filtered[df_filtered['Press'].isin(selected_Media)]
    df_filtered['MonthYear'] = df_filtered['Date'].astype(str).str[:7]
    df_filtered = df_filtered.groupby(['Press', 'MonthYear']).agg({'Count_News': 'sum','IsClickbait': 'sum'}).reset_index()
    df_filtered["ratio"] = df_filtered["IsClickbait"]/df_filtered["Count_News"]
    # 計算每個新聞媒體每個月的平均值

    df_filtered['SmoothedClickbait'] = df_filtered.groupby('Press')['ratio'].transform(lambda x: x.rolling(window=4).mean())
    fig = px.line(df_filtered, x='MonthYear', y='SmoothedClickbait',
                  color='Press', color_discrete_map=media_color_map, title='各媒體誘餌式標題比例')
    df_filtered = df[df['Press'].isin(selected_Media)]
    fig.update_layout(xaxis_title='Time (Monthly)',yaxis_title='Clickbait Ratio', legend_title='新聞媒體',autosize=True)
    # Customize the layout
    st.plotly_chart(fig, use_container_width=True)


def CategoryTimePlot(df, selected_categories):
    From2018 = ['ETToday', '今日新聞', 'Storm Media', 'NewYorkTimes', 'NewsLens', 'TVBS', '報導者']
    df_filtered = df[df['Press'].isin(From2018)]
    df_filtered = df_filtered[df_filtered['Category'].isin(selected_categories)]
    df_filtered['MonthYear'] = df_filtered['Date'].astype(str).str[:7]
    df_filtered = df_filtered.groupby(['Category', 'MonthYear']).agg({'Count_News': 'sum','IsClickbait': 'sum'}).reset_index()
    df_filtered["ratio"] = df_filtered["IsClickbait"]/df_filtered["Count_News"]
    df_filtered['SmoothedClickbait'] = (df_filtered.groupby('Category')['ratio'].transform(lambda x: x.ewm(alpha=alpha, adjust=False).mean()))
    fig = px.line(df_filtered, x='MonthYear', y='SmoothedClickbait',
                  color='Category', color_discrete_map=category_color_map, title='各類別新聞誘餌式比例')
    fig.update_layout(xaxis_title='Time (Monthly)', yaxis_title='Clickbait Ratio', legend_title='新聞類別',autosize=True)
    # Add a shaded region using add_shape
    if st.checkbox('顯示大選期間'):
        # st.write(', '.join(['2018-07-24','2018-11-30','2019-09-11','2020-01-31','2022-07-26','2022-11-30']))
        for start, end in [('2018-07-24','2018-11-30'),('2019-09-11','2020-01-31'),('2022-07-26','2022-11-30')]:
            if pd.to_datetime(start) <= pd.to_datetime(df['Date'].min()):
                continue
            fig.add_vrect(x0=start, x1=end,
                        fillcolor='LightSalmon', opacity=0.3, layer='below', line_width=0)
    st.plotly_chart(fig, use_container_width=True)

def BaitMethodTimePlot(df, selected_baits):
    From2018 = ['ETToday', '今日新聞', 'Storm Media', 'NewYorkTimes', 'NewsLens', 'TVBS', '報導者']

    df_filtered = df[df['Press'].isin(From2018)]
    # 新增"年-月"的列，以月份分組並平均，每周的權重都一樣，不管資料數
    df_filtered['MonthYear'] = df['Date'].astype(str).str[:7]
    li = ["Count_News"]+selected_baits
    df_filtered = df_filtered.groupby('MonthYear')[li].sum().reset_index()
    for category in selected_baits:
        df_filtered[category] = df_filtered[category]/df_filtered["Count_News"]
    print(df_filtered)
    # 處理資料以對"時間-BaitType"做圖
    df_melted = pd.melt(df_filtered, id_vars=['MonthYear'], value_vars=selected_baits, var_name='BaitType', value_name='BaitRatio')
    print(df_melted)
    df_melted['SmoothedClickbait'] = df_melted.groupby('BaitType')['BaitRatio'].transform(lambda x: x.rolling(window=4).mean())
    
    fig = px.line(df_melted, x='MonthYear', y='SmoothedClickbait',
                  color='BaitType', color_discrete_map=bait_color_map, title='各誘餌式方法占全部新聞比例')
    fig.update_layout(xaxis_title='Time (Monthly)', yaxis_title='Bait Type Ratio', legend_title='釣魚方法',autosize=True)
    st.plotly_chart(fig, use_container_width=True)
    
def run():
    # Sidebar filters
    with st.sidebar:
        st.header('篩選選項')
        start_date = st.date_input('開始日期', df['Date'].min())
        end_date = st.date_input('結束日期', df['Date'].max())
        selected_media = st.multiselect('選擇媒體', media_options, default=df['Press'].unique())
        selected_categories = st.multiselect("選擇新聞類別", category_options, default=df['Category'].unique())
        selected_bait = st.multiselect("選擇釣魚方法", bait_options, default=bait_options)
    st.title('台灣網路新聞釣餌式標題分析')
    # Filter data based on selections
    filtered_df = SelectDate(df, start_date, end_date)
    st.markdown("由於各家媒體的網站皆不同，每間媒體我們能抓取到的最早日期都不太一致，所以我們最終決定\n\n   ➔ 統一取2023.08~2023.10，用3個月內的資料做跨媒體的分析\n\n   ➔ 取資料完整的做2018~2023的時間趨勢分析（ ETToday、NewYorkTimes、NewsLens、Storm Media、今日新聞、報導者）")
    if st.checkbox('顯示篩選後的數據'):
        st.write(filtered_df)
    
    list_tab = ["三個月分析", "長期分析", "釣餌式標題識別器"]
    tab1, tab2,tab3 = st.tabs([s.center(16,"\u2001") for s in list_tab])
    with tab1:
        media_count(three_moth_df ,selected_categories,selected_media)
        with st.expander('## **我們的觀點：**'):
            st.markdown("這是我們搜集到從2023年8月到10月的資料數量，娛樂類、政治類新聞在各媒體間均佔比較高的比例\n\n需要注意的是三立我們是採用抽樣的數據取1/6筆，所以真正的數量應該為6倍")
        bait_count(three_moth_df ,selected_media)
        with st.expander('## **我們的觀點：**'):
            st.markdown("我們發現有政黨傾向的媒體以及以網路娛樂媒體起家的有較高的釣餌式比例\n\n 報導者近三個月內的新聞比數非常少，可能不具備參考性")
        media_clickbait(three_moth_df ,selected_categories,selected_media)
        with st.expander('## **我們的觀點：**'):
            st.markdown("- 多數媒體在娛樂類新聞的釣餌式比例最高、在財經類新 聞的釣餌式比例最低\n\n- 我們預期台灣政治類新聞的釣餌式比例也會偏高，但資料顯示並沒有特別高於其他類別\n\n- 單獨看政治類新聞的釣餌式標題比例。我們發現國內民眾普遍認為政治傾向強烈的兩家媒體，其釣餌式標題比 例排名在第二與第三名 (排除掉報導者後)")
            st.markdown("- 娛樂類新聞的閱聽者通常是為了跟上時事湊熱鬧\n\n   ➔ 媒體也更喜愛使用釣魚式標題吸引閱聽者的注意，進而點擊進去看更詳細的內容\n\n- 財經類新聞的閱聽者通常希望獲得正確且專業的資訊\n\n    ➔ 使用釣餌式標題反而會降低新聞專業度，使閱聽者點擊的機會下降，因此各媒體在財經類的釣餌式標題比例最低")
            
        category_bait_type(three_moth_df,selected_categories,selected_bait)
        with st.expander('## **我們的觀點：**'):
            st.markdown("情緒性用詞(emotional)與誇大用詞(exaggerate)都排名前段， 表示各類新聞皆偏愛將這兩類的字詞放在標題中")
            st.markdown("- 在釣餌式標題比例最高的娛樂類新聞中，前三高的誘餌方法為情緒性、誇大與結尾「了」\n\n   - Ex:「狠嗆媽媽太爛了 許老三挑戰小S九九乘法糗NG」(鏡新聞, 2022.03.17)\n\n   情緒性用詞為「嗆」，誇大用詞為「狠」，新聞標題存在結尾「了」字\n\n- 清單(list)為健康類常見的誘餌方式，這樣的標題無法提供有效資訊，需要點擊進去才能知道新聞的內容是什麼\n\n    - Ex:「脖子長腫塊怎麼辦？4類人小心甲狀腺結節 3症狀速就醫」(TVBS新聞網, 2023/12/19)")
        
    with tab2:
        st.subheader('時間趨勢分析')
        st.markdown("我們選取資料完整的做2018~2023的時間趨勢分析（ ETToday、NewYorkTimes、NewsLens、Storm Media、今日新聞、報導者）")
        MediaTimePlot(filtered_df, selected_media)
        with st.expander('## **我們的觀點：**'):
            st.markdown("- **風傳媒**的釣餌式新聞標題比例最高，為44%，但他的趨勢是最為明顯向下的\n\n- 再來第二名則是 ETToday 的 38% 且幾乎在5年內沒有太大的變化，釣餌式標題比例最低的媒體為 New York Times")
        CategoryTimePlot(filtered_df, selected_categories)
        with st.expander('## **我們的觀點：**'):
            st.markdown("- 「娛樂」類新聞的釣餌式標題比例高於其他類別，為 58%，「財經」類新聞則有最低比例的釣餌式標題，為 16%\n\n- 生活類和健康類新聞的釣餌式標題比例也較高，與預期結果相符；不同的是政治類新聞比例較預期低")
        BaitMethodTimePlot(filtered_df, selected_bait)
        with st.expander('## **我們的觀點：**'):
            st.markdown("前項指涉、強烈情緒字詞、誇大是所有的釣餌式標題樣本中最常被使用的手法")
    with tab3:
        st.header('判斷文字是否為釣餌式標題')
        user_input = st.text_area("請輸入新聞標題文字:")
        if st.button("Detect"):
            # Call the function to determine if it's clickbait
            result = is_clickbait(user_input)

            # Display the result based on the return value
            if result == 1:
                detect_result = '<p style="font-family:sans-serif; color:#FF6600; font-size: 22px;">可能是釣餌式標題</p>'
                st.markdown(detect_result, unsafe_allow_html=True)
            else:
                detect_result = '<p style="font-family:sans-serif; color:#FFA500; font-size: 22px;">應不是釣餌式標題</p>'
                st.markdown(detect_result, unsafe_allow_html=True)

        st.header("判斷是否為釣餌式標題之方法")
        for i, criterion in enumerate(criteria_list, start=1):
            st.write(f"{i}. {criterion}")
        criterion_note = '<p style="font-family:sans-serif; color:#FFA500; font-size: 18px;">根據論文研究結果1~7點較具判斷力，因此若符合一項即判定為釣餌式標題。而總共符合兩項以上特徵，我們也將判定為釣餌式標題。</p>'
        st.markdown(criterion_note, unsafe_allow_html=True)


if __name__ == "__main__":
    run()
