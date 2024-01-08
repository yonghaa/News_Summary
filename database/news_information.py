import psycopg2
from kiwipiepy import Kiwi

def get_database_connection():
    return psycopg2.connect(
    host="localhost",
    dbname='final_project',
    user='postgres',
    password="password",
    port=5432
)

def fetch_news_information():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, create_dt, media_company, news_genre, news_image_path, news_title, news_url, news_summary
        FROM final_project.news_information
    """)
    news_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return news_items

def get_total_news_count(genre):
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM final_project.news_information WHERE news_genre = %s"
    cursor.execute(query, (genre,))
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count

def get_news_by_genre(genre, page=1, per_page=20, search_query=''):
    offset = (page - 1) * per_page
    connection = get_database_connection()
    cursor = connection.cursor()

    # 검색어가 있을 때만 검색 조건을 추가
    if search_query:
        search_terms = search_query.split()
        search_conditions = ["news_title LIKE %s" for _ in search_terms]
        search_query_part = " AND (" + " OR ".join(search_conditions) + ")"
        search_patterns = [f"%{term}%" for term in search_terms]
        query_parameters = [genre] + search_patterns + [per_page, offset]
    else:
        search_query_part = ""
        query_parameters = [genre, per_page, offset]

    query = f"""
        SELECT * FROM final_project.news_information
        WHERE news_genre = %s
        {search_query_part}
        ORDER BY create_dt DESC
        LIMIT %s OFFSET %s
    """

    cursor.execute(query, query_parameters)
    news_items = cursor.fetchall()
    cursor.close()
    connection.close()
    return news_items

kiwi = Kiwi()
def extract_keywords(text):
    analysis = kiwi.analyze(text)
    return [token[0] for token in analysis[0][0] if token[1] in ['NNG', 'NNP', 'NNB', 'NR', 'NP']]

def load_news_titles_by_genre_and_date(genre, start_date, end_date):
    with get_database_connection() as conn:
        with conn.cursor() as cur:
            query = """
            SELECT news_title 
            FROM final_project.news_information 
            WHERE news_genre = %s AND create_dt BETWEEN %s AND %s
            """
            cur.execute(query, (genre, start_date, end_date))
            return [row[0] for row in cur.fetchall()]

def calculate_similarity(title_keywords, other_title_keywords):
    intersection = len(set(title_keywords) & set(other_title_keywords))
    union = len(set(title_keywords) | set(other_title_keywords))
    return intersection / union if union != 0 else 0

def find_top_groups(title_keywords, threshold=0.25, top_n=10):
    groups = []
    for title, keywords in title_keywords.items():
        found_group = False
        for group in groups:
            if calculate_similarity(group['keywords'], keywords) >= threshold:
                group['titles'].append(title)
                group['keywords'] = list(set(group['keywords']) | set(keywords))
                found_group = True
                break
        if not found_group:
            groups.append({'titles': [title], 'keywords': keywords})
    # 상위 N개 그룹 선택
    groups.sort(key=lambda g: len(g['titles']), reverse=True)
    top_groups = groups[:top_n]
    # 각 그룹의 대표 제목 결정
    for group in top_groups:
        group['representative_title'] = max(group['titles'], key=lambda t: len(set(title_keywords[t]) & set(group['keywords'])))
    return top_groups
