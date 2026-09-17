
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

    # 장르가 여러 개 적혀 있는 경우 첫 번째 장르만 사용
    df["장르"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 숫자 데이터는 숫자형으로 변환
    number_columns = [
        "first_scrn",
        "first_show",
        "first_week_audi",
        "total_audi",
        "days_in_top10"
    ]

    for column in number_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


try:
    df = load_data()

    # ---------------------------------------
    # 그래프 1. 장르별 영화 편수
    # ---------------------------------------
    st.divider()
    st.subheader("📊 그래프 1. 장르별 영화 편수")

    genre_count = (
        df["장르"]
        .value_counts()
        .reset_index()
    )

    genre_count.columns = ["장르", "영화 편수"]

    fig1 = px.pie(
        genre_count,
        names="장르",
        values="영화 편수",
        hole=0.55,
        title="장르별 영화 편수 분포"
    )

    fig1.update_traces(
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "영화 편수: %{value}편<br>"
            "비율: %{percent}<extra></extra>"
        )
    )

    fig1.update_layout(
        height=500,
        legend_title="장르"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # 그래프로 알 수 있는 것
    st.info(
        "💡 이 그래프로 알 수 있는 것: "
        "1년간 박스오피스 10위권에 든 영화가 어떤 장르에 많이 분포했는지 확인할 수 있습니다."
    )


    # ---------------------------------------
    # 그래프 2. 장르별 총 관객 트리맵
    # ---------------------------------------
    st.divider()
    st.subheader("📊 그래프 2. 장르별 총 관객 분포")

    # 영화명이나 장르가 비어 있는 행 제거
    treemap_df = df[
        (df["장르"].notna()) &
        (df["movieNm"].notna()) &
        (df["movieNm"].astype(str).str.strip() != "")
    ].copy()

    # 총 관객수가 0보다 큰 영화만 사용
    treemap_df = treemap_df[treemap_df["total_audi"] > 0]

    fig2 = px.treemap(
        treemap_df,
        path=["장르", "movieNm"],
        values="total_audi",
        hover_data=["total_audi"],
        title="장르별 영화의 총 관객 수"
    )

    fig2.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "총 관객: %{value:,.0f}명"
            "<extra></extra>"
        )
    )

    fig2.update_layout(
        height=650
    )

    st.plotly_chart(fig2, use_container_width=True)

    # 그래프로 알 수 있는 것
    st.info(
        "💡 이 그래프로 알 수 있는 것: "
        "장르별로 어떤 영화가 많은 관객을 모았는지와 영화별 관객 규모의 차이를 한눈에 비교할 수 있습니다."
    )


except Exception as e:
    st.error("데이터를 불러오거나 그래프를 만드는 중 문제가 발생했습니다.")
    st.write("오류 내용:", e)
# ── 그래프 2. 장르 안의 영화 (트리맵) ──
st.header("2. 장르 안의 영화 (트리맵)")
fig2 = px.treemap(df, path=["장르", "movieNm"], values="total_audi",
                  hover_data=["total_audi"])
st.plotly_chart(fig2, width="stretch")
st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")
# ── 그래프 3. 총 관객의 분포 (히스토그램) ──
st.header("3. 총 관객의 분포 (히스토그램)")
fig3 = px.histogram(df, x="total_audi", nbins=40)
st.plotly_chart(fig3, width="stretch")
under_1m = (df["total_audi"] < 1_000_000).sum()
best = df.loc[df["total_audi"].idxmax()]
st.write(f"216편 가운데 {under_1m}편이 100만 명 미만입니다. "
         f"가장 많이 본 영화는 {best['movieNm']}({best['total_audi']:,}명)입니다.")
st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")
