# 🎈 RAG Doc Builder
- RAG : Retrieval-Augmented Generation
- AI의 할루시네이션을 막고, AI가 아직 학습하지 못한 최신 자료에 즉시 적용 

## RAG Sample 구축

- PDF와 WebSite Url을 입력 받아서,
- 입력받은 File은 AWS S3에 저장하고,
- AWS RDS Postgres에 구축 이력을 생성한다.
- 입력 받은 자료를 이용해 VectorDB를 구축하고,
- VectorDB 구축시 구축 자료에 대한 소스원 정보인 Postgres의 Index도 같이 저장한다.
- RAG를 이용하여 유사도 상위 2개를 검색을 한다.
- VectorDB 검색결과에서 Postgres DB Index를 확인 할수 있고, 원 소스와 비교 검증 할수 있다.

- sample data : 만개의 레시피 ( https://www.10000recipe.com/ )
  요리 레시피가 잘 정리 되어 있고, PDF로도 제공되어서 선정함.
  기업용으로 구축시 사내에 존재하는 PPT, Word, Notion, Jira 등의 자료가 소스원이 될것이고, 입력 자료의 형태와 종료, 사용 방법은 다양할 것.

## TODO 
- 증강 검색 결과( 구축한 원 소스 )를 기반으로 AI와 대화.
- 원문 요약, 원문에서 특정 자료 검색등
- 검색결과와 사용자가 입력한 Query를 하나의 Prompt로 작성하여 Chating을 구현.
- 시작 Prompt 예시 : 
```
System : 당신은 한국 요리에 정통한 AI 비서입니다. 사용자가 한국 요리 레시피에 대해 질문하면, 다음 두 가지 정보를 활용하여 정확하고 상세한 답변을 제공합니다.
레시피 정보에 없는 정보는 제공하지 말것.

User :
1. **사용자의 입력:** 사용자가 질문한 내용.
2. **검색한 레시피 정보:** 증강검색을 통해 얻은 관련 한국 요리 레시피 데이터.

사용자의 입력과 검색한 레시피 정보를 종합하여, 요리 방법, 재료, 조리 시간 등 필요한 모든 정보를 포함한 친절한 답변을 작성해 주세요.

```





### input : URL(Web Page), FileUpload
### fileType : PDF, CSV, Text

### 1. LangChain 0.3.3 for Framework
### 1. Pinecone for Vector DB
### 2. OpenAI  for Enbedding
### 3. AWS RDS Postgre for build source history  
### 4. AWS ECS Fargate (2 Container) for App hosting
- UI : Public ( rag.tnstory.co.kr : 고정IP가 아님 주의 )
- BE : Private ( AWS ECS Fargate - FastAPI ) 

[![Open in Web](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://rag.tnstory.co.kr/)

### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```



## Docker 이미지 빌드 및 ECR 푸시
1. ECR 리포지토리 생성
- aws ecr create-repository --repository-name rag_doc_builder

2. Docker 로그인(AWS ECR에 로그인)
- aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-northeast-2.amazonaws.com

3. 이미지 빌드 및 태그 지정
- ** docker daemon up 
- docker build  --compress   -t rag_doc_builder .

- docker tag rag_doc_builder:latest <ACCOUNT_ID>.dkr.ecr.ap-northeast-2.amazonaws.com/rag_doc_builder:latest


4. 이미지 푸시
- docker push <ACCOUNT_ID>.dkr.ecr.ap-northeast-2.amazonaws.com/rag_doc_builder:latest
