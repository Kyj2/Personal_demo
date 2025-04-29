import streamlit as st
import pandas as pd
#import plotly.express as px
#import plotly.graph_objects as go
import matplotlib.pyplot as plt
import base64





def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 이미지를 base64로 변환
img_base641 = get_image_base64("./01.png")
img_base642 = get_image_base64("./02.png")
img_base643 = get_image_base64("./03.png")

# 메인 제목 (Streamlit 기본 스타일링)
st.title('Investment Portfolio Dashboard')


#---------------------------chart 함수 정의-------------------------
import matplotlib.pyplot as plt
import streamlit as st
import ast

# 파스텔 색상 정의
pastel_colors = [
    "#FFB5E8", "#B5EAD7", "#C7CEEA", "#FFDAC1", "#E2F0CB",
    "#FF9AA2", "#FFB347", "#AEC6CF", "#D5AAFF",
    "#FFD6E0", "#CBF1F5", "#D9D7F1", "#FFF5BA", "#F3C5C5",
    "#C8E7ED", "#F6DFEB", "#D0F4DE", "#FDE2E4"
]

def plot_donut_chart(row, key):
 
    mp_row = row[row['MP'] == key]
    if mp_row.empty:
        print(f"{key}에 해당하는 데이터가 없습니다.")
        return None

    # 포트폴리오 딕셔너리 추출
    mp_data = mp_row.iloc[0]['Portfolio']  # 이미 dict 형태
    if isinstance(mp_data, str):
        mp_data = ast.literal_eval(mp_data)
    # 정렬
    sorted_items = sorted(mp_data.items(), key=lambda x: x[1], reverse=True)
    labels = [item[0] for item in sorted_items]
    sizes = [item[1] for item in sorted_items]
    colors = pastel_colors[:len(sizes)]
    sizes_rounded = [round(item, 2) for item in sizes]
    explanation_df = pd.DataFrame({
        "보유 펀드": labels,
        "비중(%)": sizes_rounded,
        "색상": colors
    })
    explanation_df = explanation_df.drop(columns=["색상"])

    # 도넛 차트
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(
        sizes,
        autopct='%.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops=dict(width=0.45),
        textprops={'color': 'black', 'fontsize': 14}
    )
    ax.axis('equal')
    #ax.set_title(f"{mp_row.iloc[0]['CustomerID']} - {key}", fontsize=14)
    plt.tight_layout()
    plt.show()
    for autotext in autotexts:
        autotext.set_fontsize(18)
        autotext.set_fontweight('bold')
        autotext.set_position((autotext.get_position()[0]*1.3, autotext.get_position()[1]*1.5))

    # 설명 테이블 반환
   
    return fig, explanation_df, colors

   
#--------------------------------------------------------------
# 입력 필터

col1, col2 = st.columns([1, 1])


# 데이터 로드---------------------------------------------------------

df = pd.read_csv('./df_rivi_.csv', index_col=False)
#df.index= range(1,len(df)+1)

df_chart=pd.read_csv('./df_chart_.csv', index_col=False)
#df_chart.index=range(1,len(df)+1)
df_meta=pd.read_csv('./cluster_meta.csv')

#-------------------------------------------------------------------------------------


with col1:
    ID_input = st.text_input('Enter portfolio ID(1~5000)', placeholder=f'Enter your ID (1~{len(df)})', key='id_input')

# 입력값이 있을 때만 실행
if ID_input.isdigit():


    ID = int(ID_input)
    if ID > 5000:
        st.warning("Please enter a portfolio ID between 1 ~ 5.", icon="⚠️")
    else:
        filtered_df = df[df['CustomerID'] == ID]
        chart_filter=df_chart[df_chart['CustomerID'] == ID]
    # filtered_df
        st.dataframe(filtered_df)

        # 📦 큰 박스(컨테이너)
    with st.container():
        st.subheader("Portfolio Profile")

        # 컬럼 3개로 분할
        col1, col2, col3 = st.columns(3)

        # 각 컬럼에 원그래프 넣기
        with col1:
            st.write(f"적합도{chart_filter[chart_filter['MP']=='MP_A']['Suitability'].iloc[0]} %")
            fig_a, df_a, colors_a = plot_donut_chart(chart_filter, 'MP_A')
            st.pyplot(fig_a)
            sub=chart_filter[chart_filter['MP']=='MP_A']['sub_cluster'].iloc[0]
            mpa_ex=df_meta[df_meta['sub_cluster']==sub]

            # 2️⃣ 설명 출력
            st.markdown(
                f"""
                <div style="
                    background-color:#F8F8FF;
                    padding:10px;
                    border-radius:6px;
                    border: 1px solid #eeeeee;
                    margin-top: 5px;
                    margin-bottom : 10px;
                    height: 200px;
                ">
                <span style="font-weight: bold; color: black;">{mpa_ex.iloc[0]['portfolio_name']}</span><br>
                {mpa_ex.iloc[0]['portfolio_description']}<br><br>  

                
                <span style="font-size: 10px; color: black; font-weight: bold;">다소 낮은 위험</span>
                </div>
                """,
                unsafe_allow_html=True
        )

        
            styled_df_a = (
            df_a
            .style
            .apply(lambda x: [f'background-color: {c}' for c in colors_a], subset=["비중(%)"])
            .format({"비중(%)": "{:.1f}"})  
                    # 색상 컬럼 숨기기
            )
            st.dataframe(styled_df_a, use_container_width=True, hide_index=True)
            
            
        with col2:
            st.write(f"적합도{chart_filter[chart_filter['MP']=='MP_B']['Suitability'].iloc[0]} %")
            fig_b, df_b, colors_b = plot_donut_chart(chart_filter, 'MP_B')
            st.pyplot(fig_b)
            sub=chart_filter[chart_filter['MP']=='MP_B']['sub_cluster'].iloc[0]
            mpa_ex=df_meta[df_meta['sub_cluster']==sub]


            st.markdown(
                f"""
                <div style="
                    background-color:#F8F8FF;
                    padding:10px;
                    border-radius:6px;
                    border: 1px solid #eeeeee;
                    margin-top: 5px;
                    margin-bottom : 10px;
                    height: 200px;
                ">
                <span style="font-weight: bold; color: black;">{mpa_ex.iloc[0]['portfolio_name']}</span><br>
                {mpa_ex.iloc[0]['portfolio_description']}<br><br>  

                
                <span style="font-size: 10px; color: black; font-weight: bold;">다소 낮은 위험</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            styled_df_b = (
                df_b
                .style
                .apply(lambda x: [f'background-color: {c}' for c in colors_b], subset=["비중(%)"])
                .format({"비중(%)": "{:.1f}"})
            )
            st.dataframe(styled_df_b, use_container_width=True, hide_index=True)

        # -----------------------------------

        with col3:
            st.write(f"적합도{chart_filter[chart_filter['MP']=='MP_C']['Suitability'].iloc[0]} %")
            fig_c, df_c, colors_c = plot_donut_chart(chart_filter, 'MP_C')
            st.pyplot(fig_c)
            sub=chart_filter[chart_filter['MP']=='MP_C']['sub_cluster'].iloc[0]
            mpa_ex=df_meta[df_meta['sub_cluster']==sub]

            st.markdown(
                f"""
                <div style="
                    background-color:#F8F8FF;
                    padding:10px;
                    border-radius:6px;
                    border: 1px solid #eeeeee;
                    margin-top: 5px;
                    margin-bottom : 10px;
                    height: 200px;
                "> 
                <span style="font-weight: bold; color: black;">{mpa_ex.iloc[0]['portfolio_name']}</span><br>
                {mpa_ex.iloc[0]['portfolio_description']}<br><br>  

                
                <span style="font-size: 10px; color: black; font-weight: bold;">다소 낮은 위험</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            styled_df_c = (
                df_c
                .style
                .apply(lambda x: [f'background-color: {c}' for c in colors_c], subset=["비중(%)"])
                .format({"비중(%)": "{:.1f}"})
            )
            st.dataframe(styled_df_c, use_container_width=True, hide_index=True)
    

     
        
        







