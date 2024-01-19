# 뉴스요약 사이트
![image](https://github.com/yonghaa/News_Summary/assets/145304155/02f86d1c-b67b-45a0-9b04-1df1fdaac21c)

## 프로젝트 소개
- 바쁜 현대 사회, 정보화시대로 대량의 정보가 쏟아짐
- 뉴스 요약 사이트의 필요성을 느낌
- 기존(네이버, 연합뉴스, KBS등 뉴스 요약봇 제공 사이트들이 많으나
- 대부분 추출적 요약만을 이용해 원문에서 핵심문장을 추출하지 못하는 경우 요약 품질하락
- 모델의 언어 표현 능력이 제한되어 자연스럽지 않은 요약문 생성
- 뉴스를 직접 클릭해서 들어가 확인해야하는 번거로움을 느낌 -> 거의 이용하지 않음

## 데이터 수집
![image](https://github.com/yonghaa/News_Summary/assets/145304155/0456daa7-faf0-4374-acb2-cee9162d131f)
-웹 크롤링으로 데이터를 수집하여 데이터베이스에 테이블 형식으로 저장
## 개발 언어
- HTML
- CSS
- JavaScript
- python
## 개발 환경
- python 3.11
- PhCharm
- colab
- jupyter
- Framework: Flask
- 라이브러리: Selenium, pandas
- DBMS: PostgreSQL
## 주요기능
![image](https://github.com/yonghaa/News_Summary/assets/145304155/74cc7c99-8fa5-4d87-82be-3b0b0f4ec279)
- 최신 트렌드 파악
![image](https://github.com/yonghaa/News_Summary/assets/145304155/1749e8e0-d531-42f7-83b1-92a617cfa4ee)
- 분야별 가독성 향상 및 기존의 추출적 요약이 아닌 추출적과 추상적 모델을 결합한 모델인 BART를 활용
  그 중 SKT에서 공개한 한국어에 특화된 모델인 KoBART를 파인튜닝하여 요약문 성능 향상
