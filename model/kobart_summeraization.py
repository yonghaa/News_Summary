import psycopg2
from transformers import PreTrainedTokenizerFast, BartForConditionalGeneration
from database.news_information import get_database_connection


# 파인 튜닝한 모델 가져오기
saved_model_path = "bart_summarization_model_v2"
tokenizer = PreTrainedTokenizerFast.from_pretrained('gogamza/kobart-summarization')
model = BartForConditionalGeneration.from_pretrained(saved_model_path)


# 요약 함수 설정
def summarize(text):
    inputs = tokenizer.encode_plus(text, return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = model.generate(inputs['input_ids'], length_penalty=1.0, num_beams=4, max_length=250, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# 나의 postgresql 연결하기
db_connection = get_database_connection()
cursor = db_connection.cursor()

# 뉴스 요약문이 빈 행의 id와 본문 만 가져오기
cursor.execute("SELECT id, news_origin FROM final_project.news_information WHERE news_summary = ''")
rows = cursor.fetchall()

for row in rows:
    news_id, news_text = row
    summary = summarize(news_text)  # 뉴스 요약 함수로 요약 실행
    # 요약된 뉴스를 id가 같은 행에 news_summary 업데이트 하기
    cursor.execute(
        "UPDATE final_project.news_information SET news_summary = %s WHERE id = %s",
        (summary, news_id)
    )

# 변경 사항 커밋 및 연결 종료
    db_connection.commit()
cursor.close()