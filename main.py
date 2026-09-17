import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

# 제목
st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("1년간 박스오피스 10위권에 든 영화 216편의 데이터를 살펴봅니다.")

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)
    return df

try:
    df = load_data()

    # 장르가 여러 개 적힌 경우 첫 번째 장르만 사용
    df["genre_first"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 장르별 영화 편수
    genre_count = (
        df["genre_first"]
        .value_counts()
        .reset_index()
    )

    genre_count.columns = ["장르", "영화 편수"]

    # 그래프 구역
    st.divider()
    st.subheader("📊 그래프 1. 장르별 영화 편수")

    fig = px.pie(
        genre_count,
        names="장르",
        values="영화 편수",
        hole=0.55,
        title="장르별 영화 편수 분포",
    )

    fig.update_traces(
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>"
                      "영화 편수: %{value}편<br>"
                      "비율: %{percent}<extra></extra>"
    )

    fig.update_layout(
        height=500,
        legend_title="장르"
    )

    st.plotly_chart(fig, use_container_width=True)

    # 그래프로 알 수 있는 것
    st.info(
        "💡 이 그래프로 알 수 있는 것: "
        "1년간 박스오피스 10위권에 든 영화가 어떤 장르에 많이 분포했는지 한눈에 확인할 수 있습니다."
    )

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.write("오류 내용:", e)
# ── 그래프 2. 장르 안의 영화 (트리맵) ──
st.header("2. 장르 안의 영화 (트리맵)")
fig2 = px.treemap(df, path=["장르", "movieNm"], values="total_audi",
                  hover_data=["total_audi"])
st.plotly_chart(fig2, width="stretch")
st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")
