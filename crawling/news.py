from database.news_information import get_database_connection
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from urllib.request import urlretrieve
import re
from datetime import datetime



posts = []

news_category = {
    100: '정치',
    101: '경제',
    102: '사회',
    103: '생활/문화',
    104: '세계',
    105: 'IT/과학',
}

for i in range(100, 106):
    for j in range(1, 6):
        category = news_category.get(i)
        url = f'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={i}#&date=%2000:00:00&page={j}'

        driver = webdriver.Chrome()
        driver.get(url)
        post_list = driver.find_elements(By.XPATH, '//*[@id="section_body"]/ul/li')

        for k in post_list:
            time.sleep(0.5)

            try:
                post = k.find_element(By.XPATH, 'dl/dt[2]/a')
                news_title = post.text
            except:
                post = k.find_element(By.XPATH, 'dl/dt[1]/a')
                ews_title = post.text

            link = post.get_attribute('href')

            driver.execute_script(f"window.open('{link}', '_blank');")

            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)

            try:
                news_image = driver.find_element(By.ID, 'img1')
                news_image_url = news_image.get_attribute('src')

                match = re.search(r'/([^/]+\.(jpg|jpeg|png|gif|JPG|PNG))', news_image_url)
                news_image_name = match.group(1)
                news_image = news_image_url.replace('https', 'http')
                news_image_path = f'/static/images/news_image/{news_image_name}'
                print('.'+ news_image_path)
                urlretrieve(news_image, '..'+news_image_path)


            except Exception as e:
                print(news_image, e)
                try:
                    element_style = driver.find_element(By.XPATH,
                                                        '//*[@id="video_area_0"]/div/div[2]/style').get_attribute('innerHTML')
                    match = re.search(r'background-image: url\((.*?)\);', element_style)
                    if match:
                        news_image_url = match.group(1)
                        news_image = news_image_url.replace('https', 'http')
                        print(news_image_url)
                        news_image_path = '/static/images/news_image/' + news_image_url.split('/')[-1].split('?')[0]
                        print(news_image_path)
                        urlretrieve(news_image, '..' + news_image_path)

                    else:
                        news_image_path = '/static/images/none_image.png'
                except Exception as e:
                    print(e)
                    news_image_path = '/static/images/none_image.png'

            create_dt = driver.find_element(By.XPATH, '//*[@id="ct"]/div[1]/div[3]/div[1]/div/span').get_attribute(
                'data-date-time')

            news_name = driver.find_element(By.XPATH, '//*[@id="ct"]/div[1]/div[1]/a/img[1]').get_attribute('title')

            post_origin = driver.find_element(By.XPATH, '//*[@id="dic_area"]')
            post_origin_text = post_origin.text
            posts.append([create_dt, news_name, category, news_image_path, news_title, post_origin_text, link])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        driver.quit()

url = 'https://entertain.naver.com/now'
driver = webdriver.Chrome()
driver.get(url)
# 페이지 스크래핑 함수 정의
def scrape_page(driver):
    post_list = driver.find_elements(By.XPATH, '//*[@id="newsWrp"]/ul/li')
    for i in post_list:
        post = i.find_element(By.XPATH, 'div/a')
        news_title = post.text
        link = post.get_attribute('href')
        driver.execute_script(f"window.open('{link}', '_blank');")
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)

        try:
            news_image = driver.find_element(By.ID, 'img1')
            news_image_url = news_image.get_attribute('src')

            match = re.search(r'/([^/]+\.(jpg|jpeg|png|gif|JPG|PNG))', news_image_url)
            news_image_name = match.group(1)
            news_image = news_image_url.replace('https', 'http')
            news_image_path = f'/static/images/news_image/{news_image_name}'
            print('.' + news_image_path)
            urlretrieve(news_image, '..' + news_image_path)

        except Exception as e:
            print(news_image, e)
            try:
                element_style = driver.find_element(By.XPATH,
                                                    '//*[@id="video_area_0"]/div/div[2]/style').get_attribute(
                    'innerHTML')
                match = re.search(r'background-image: url\((.*?)\);', element_style)
                if match:
                    news_image_url = match.group(1)
                    news_image = news_image_url.replace('https', 'http')
                    print(news_image_url)
                    news_image_path = '/static/images/news_image/' + news_image_url.split('/')[-1].split('?')[0]
                    print(news_image_path)
                    urlretrieve(news_image, '..' + news_image_path)

                else:
                    news_image_path = '/static/images/none_image.png'
            except Exception as e:
                print(e)
                news_image_path = '/static/images/none_image.png'

        create_dt = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div[2]/span/em').text
        input_data = create_dt.replace("오후", "PM").replace("오전", "AM")
        create_dt = datetime.strptime(input_data, "%Y.%m.%d. %p %I:%M")
        print(create_dt)
        news_name = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div[1]/a/img').get_attribute('alt')
        print(news_name)
        post_origin_text = driver.find_element(By.XPATH, '//*[@id="articeBody"]').text
        posts.append([create_dt, news_name, '연예', news_image_path, news_title, post_origin_text, link])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


# 첫 페이지 스크래핑
scrape_page(driver)
driver.quit()






# 여러분의 데이터베이스 연결 정보
db_connection = get_database_connection()

# 데이터베이스 커서 생성
cursor = db_connection.cursor()

for news_item in posts:
    try:
        cursor.execute("""
            INSERT INTO final_project.news_information
            (create_dt, media_company, news_genre, news_image_path, news_title, news_origin, news_url, news_summary) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (news_url) DO NOTHING;
        """, (news_item[0], news_item[1], news_item[2], news_item[3], news_item[4], news_item[5], news_item[6], ''))
    except Exception as e:
        print(f"Error inserting news_item: {news_item}")
        print(f"Error message: {e}")
    time.sleep(0.3)
# 변경사항을 저장
db_connection.commit()

# 연결 종료
cursor.close()
db_connection.close()