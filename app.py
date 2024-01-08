from flask import Flask, render_template, request, jsonify
from database.news_information import get_news_by_genre, get_total_news_count, load_news_titles_by_genre_and_date, extract_keywords, find_top_groups, get_database_connection
import collections
from datetime import datetime, timedelta
from collections import Counter
from wordcloud import WordCloud


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    genres = ['정치', '경제', '사회', '생활/문화', '세계', 'IT/과학', '연예']
    selected_genre = request.form.get('genre') or '정치'
    selected_date = request.form.get('date') or datetime.now().strftime('%Y-%m-%d')

    # 지정된 날짜의 모든 뉴스 제목 로드
    start_date = datetime.strptime(selected_date, '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
    end_date = (datetime.strptime(selected_date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
    news_titles = load_news_titles_by_genre_and_date(selected_genre, start_date, end_date)

    # 키워드 추출 및 빈도수 계산
    all_keywords = []
    for title in news_titles:
        keywords = extract_keywords(title)
        filtered_keywords = [word for word in keywords if len(word) >= 2]
        all_keywords.extend(filtered_keywords)

    keyword_counts = Counter(all_keywords)

    # 워드클라우드 생성
    wordcloud = WordCloud(font_path= 'C:/Windows/Fonts/malgun.ttf',width=800, height=400, background_color='white').generate_from_frequencies(keyword_counts)
    wordcloud_path = 'static/wordcloud.png'
    wordcloud.to_file(wordcloud_path)

    # 각 날짜에 대한 TOP 10 결과를 저장할 리스트
    top_10_groups_each_day = []

    for days_ago in range(3):
        current_date_dt = datetime.strptime(selected_date, '%Y-%m-%d') - timedelta(days=days_ago)
        start_date = current_date_dt.strftime('%Y-%m-%d 00:00:00')
        end_date = (current_date_dt + timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')
        news_titles = load_news_titles_by_genre_and_date(selected_genre, start_date, end_date)
        title_keywords = {title: extract_keywords(title) for title in news_titles}
        similar_groups = find_top_groups(title_keywords)
        top_groups = collections.Counter({group['representative_title']: len(group['titles']) for group in similar_groups}).most_common(10)
        similer_titles = [titles['titles'] for titles in similar_groups]

        combined_info = []
        for i in range(10):
            combined_info.append([top_groups[i], similer_titles[i]])

        top_10_groups_each_day.append((current_date_dt, combined_info))
    print(top_10_groups_each_day)
    return render_template('home.html', genres=genres, top_10_groups_each_day=top_10_groups_each_day, selected_genre=selected_genre, selected_date=selected_date, wordcloud_path=wordcloud_path)

@app.route('/get_news_details', methods=['POST'])
def get_news_details():
    data = request.get_json()
    titles = data['titles']
    print(titles)

    similar_news = []

    with get_database_connection() as conn:
        with conn.cursor() as cur:
            for title in titles:
                query = """SELECT * FROM final_project.news_information WHERE news_title = %s"""
                cur.execute(query, (title,))
                similar_news.extend(cur.fetchall())
    print(similar_news)
    return jsonify(similar_news)


@app.route('/news/<genre>')
@app.route('/news/<genre>/<int:page>')
def show_news(genre, page=1):
    genre = genre.replace('_', '/')
    per_page = request.args.get('per_page', default=20, type=int)
    search_query = request.args.get('search_query', '')
    total_news_count = get_total_news_count(genre)
    total_pages = (total_news_count + per_page - 1) // per_page
    news_items = get_news_by_genre(genre, page, per_page, search_query)
    genre = genre.replace('/', '_')
    genres = ['정치', '경제', '사회', '생활/문화', '세계', 'IT/과학', '연예']
    page_range = 10
    start_page = max(1, ((page - 1) // page_range) * page_range + 1)
    end_page = min(start_page + page_range - 1, total_pages)

    return render_template('news.html', news_items=news_items, current_genre=genre, genres=genres, page=page, per_page=per_page, total_pages=total_pages, start_page=start_page, end_page=end_page)


if __name__ == '__main__':
    app.run(debug=True)