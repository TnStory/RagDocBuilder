import streamlit as st
import requests

st.title("🎈 RAG Doc Builder")
st.write(
    "RAG 구축을 위해 URL(WebPage 또는 Web File URL),  File(PDF, Word, PPT, CSV, TEXT)을 입력."
)

def call_api_1(url):
    # 여기에 API-1 호출을 처리하는 로직을 구현합니다.
    params = {'url': url}
    response = requests.get("https://example.com/api/build-from-url", params=params)
    if response.status_code == 200:
        return response.json()  # 응답을 JSON 형식으로 가정
    return {"error": "Failed to fetch data"}

def call_api_2(file):
    # 여기에 API-2 호출을 처리하는 로직을 구현합니다.
    files = {'file': file}
    response = requests.post("https://example.com/api/upload", files=files)
    if response.status_code == 200:
        return response.json()  # 응답을 JSON 형식으로 가정
    return {"error": "Failed to upload file"}

def main():

    # URL 입력 폼
    st.subheader("URL 입력")
    url = st.text_input("RAG 구축을 위한 URL을 입력하세요:")
    if st.button("Build RAG by URL"):
        if url:
            api_1_result = call_api_1(url)
            st.write("결과:")
            st.json(api_1_result)
        else:
            st.error("URL을 입력하세요.")

    # 파일 업로드 폼
    st.subheader("파일 업로드")
    uploaded_file = st.file_uploader("RAG 구축을 위한 파일을 업로드하세요 (최대 30MB):", type=["txt", "csv", "pdf", "doc", "docx", "ppt", "pptx"])
    if uploaded_file and uploaded_file.size <= 30 * 1024 * 1024:
        if st.button("Build RAG by File"):
            api_2_result = call_api_2(uploaded_file)
            st.write("결과:")
            st.json(api_2_result)
    elif uploaded_file and uploaded_file.size > 30 * 1024 * 1024:
        st.error("파일 크기가 30MB를 초과합니다.")

if __name__ == "__main__":
    main()

