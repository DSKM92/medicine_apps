import streamlit as st
import pandas as pd

# git-repository name : medicine_apps - https://github.com/DSKM92/medicine_apps/settings

# 1. 앱 기본 설정
st.set_page_config(page_title="약 위치 찾기", page_icon="💊", layout="centered")

# 2. 구글 스프레드시트 주소 설정
# ⚠️ 주의: 반드시 본인의 구글 시트 공유 링크 주소로 교체하세요!
dir_before = "https://docs.google.com/spreadsheets/d/1C1yJzFFM9czy3kQ6zEzM_g3_c-DoVHtP7DOToKyS14Y/edit?usp=sharing"
dir_after = "https://docs.google.com/spreadsheets/d/1C1yJzFFM9czy3kQ6zEzM_g3_c-DoVHtP7DOToKyS14Y/export?format=csv"
GOOGLE_SHEET_URL = dir_before

# 구글 시트 주소를 판다스(Pandas)가 읽을 수 있는 CSV 다운로드 형태로 변환하는 함수
def get_csv_url(url):
    try:
        base_url = url.split('/edit')[0]
        return f"{base_url}/export?format=csv"
    except:
        return url

# 3. 데이터 실시간 로딩 함수 (캐싱을 적용해 속도 최적화)
@st.cache_data(ttl=10)  # 10초마다 데이터 새로고침 허용
def load_data():
    csv_url = get_csv_url(GOOGLE_SHEET_URL)
    # 구글 시트의 A열(약이름), B열(위치) 데이터를 가져옵니다.
    df = pd.read_csv(csv_url)
    return df

# 데이터 불러오기
try:
    df = load_data()
    # 공백 제거 및 문자열 변환
    df['약이름'] = df['약이름'].astype(str).str.strip()
    df['위치'] = df['위치'].astype(str).str.strip()
except Exception as e:
    st.error("구글 스프레드시트를 불러오는 데 실패했습니다. 링크 공유 설정을 확인해 주세요.")
    st.stop()

# 4. 메인 화면 UI
st.title("💊 내 손안의 약 위치 찾기")
st.caption("구글 스프레드시트와 연동되어 약 정보를 실시간으로 검색합니다.")
st.write("---")

# 5. 검색어 입력창
search_query = st.text_input("🔍 약 이름 또는 위치 번호를 입력하세요:", value="").strip()

# 6. 검색 및 매칭 로직
if search_query:
    # 약이름이나 위치에 검색어가 포함되어 있는지 확인 (대소문자 구분 없음)
    matched_df = df[
        df['약이름'].str.contains(search_query, case=False, na=False) | 
        df['위치'].str.contains(search_query, case=False, na=False)
    ]
    
    # 7. 결과 화면에 팝업 형태로 띄우기
    if not matched_df.empty:
        st.subheader("📍 검색 결과")
        for index, row in matched_df.iterrows():
            st.success(
                f"**[{row['약이름']}]**의 위치를 찾았습니다!\n\n"
                f"* **위치 번호**: {row['위치']}"
            )
    else:
        st.error(f"❓ '{search_query}'에 매칭되는 약 정보가 없습니다.")

# 8. 전체 목록 보기 기능
with st.expander("📦 전체 등록된 약 목록 보기"):
    st.dataframe(df, use_container_width=True)