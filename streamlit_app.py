import streamlit as st
import requests
import pandas as pd

st.title("🎈 RAG Doc Builder")
st.write(
    "RAG 구축을 위해 URL(WebPage 또는 Web File URL),  File(PDF, CSV, TEXT)을 입력."
)

def call_api_1(url):
    # 여기에 API-1 호출을 처리하는 로직을 구현합니다.
    params = {'url': url}
    response = requests.get("http://127.0.0.1:8080/api/rag/url_build", params=params)
    if response.status_code == 200:
        return response.json()  # 응답을 JSON 형식으로 가정
    return {"error": "Failed to fetch data"}

def call_api_2(file):
    # 여기에 API-2 호출을 처리하는 로직을 구현합니다.
    files = {'file': (file.name, file)}
    response = requests.post("http://127.0.0.1:8080/api/rag/file_build", files=files)
    if response.status_code == 200:
        return response.json()  # 응답을 JSON 형식으로 가정
    return {"error": "Failed to upload file"}

def call_build_list(build_type=None, page=1, page_size=10):
    params = {'build_type': build_type, 'page': page, 'page_size': page_size}
    response = requests.get("http://127.0.0.1:8080/api/rag/build_list", params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch build list"}


def main():

    # URL 입력 폼
    st.subheader("URL 입력")
    url = st.text_input("RAG 구축을 위한 URL을 입력하세요. https://www.10000recipe.com/recipe/print.html?seq=6887226")
    if st.button("Build RAG by URL"):
        if url:
            api_1_result = call_api_1(url)
            st.write("결과:")
            st.json(api_1_result)
        else:
            st.error("URL을 입력하세요.")

    # 파일 업로드 폼
    st.subheader("파일 업로드")
    uploaded_file = st.file_uploader("RAG 구축을 위한 파일을 업로드하세요 (최대 30MB):", type=["txt", "csv", "pdf"])
    if uploaded_file and uploaded_file.size <= 30 * 1024 * 1024:
        if st.button("Build RAG by File"):
            api_2_result = call_api_2(uploaded_file)
            st.write("결과:")
            st.json(api_2_result)
    elif uploaded_file and uploaded_file.size > 30 * 1024 * 1024:
        st.error("파일 크기가 30MB를 초과합니다.")

    # 구축된 목록
    st.subheader("Build List 조회")
    build_type = st.selectbox("Build Type 선택", (None, 'FILE', 'URL'))
    page = st.number_input("페이지 번호", min_value=1, value=1)
    page_size = st.number_input("페이지 크기", min_value=1, value=10)
    if st.button("Fetch Build List"):
        build_list_result = call_build_list(build_type=build_type, page=page, page_size=page_size)
        if "error" not in build_list_result:
            df = pd.DataFrame(build_list_result)
            if 'source_url' in df.columns:
                df['source_url'] = df['source_url'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
            st.write("결과:")
            st.write(df.to_html(escape=False), unsafe_allow_html=True)
        else:
            st.error(build_list_result["error"])


if __name__ == "__main__":
    main()

