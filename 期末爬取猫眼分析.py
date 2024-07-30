# _*_coding:UTF-8 _*_
# @Time : 2024/5/29 11:37
# @Author:lupeng
# @File : 测试3
import time
import csv
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random


driver = webdriver.Edge()
def parse_one_page3(html):
    soup = BeautifulSoup(html, 'lxml')
    movie_dds = soup.select('dl.movie-list dd')
    movies = []
    index = 1
    for movie_dd in movie_dds:

        # 提取电影名和评分
        name_score_div = movie_dd.select_one('.movie-hover-info .movie-hover-title:first-child')
        name = name_score_div.find('span', class_='name').text.strip()
        score = float(name_score_div.find('i', class_='integer').text.strip() + name_score_div.find('i', class_='fraction').text.strip())

        # 提取类型
        type_div = movie_dd.select_one('.movie-hover-info .movie-hover-title:nth-child(2)')
        m_type = type_div.text.strip() if type_div else '未知类型'
        m_type = m_type.replace('类型:', '').strip() if '类型:' in m_type else m_type

        # 提取主演
        stars_div = movie_dd.select_one('.movie-hover-info .movie-hover-title:nth-child(3)')
        stars_text = stars_div.text.replace('主演:', '').strip()
        stars_list = stars_text.split('／')
        stars = '／'.join(star.strip() for star in stars_list)

        # 提取上映时间
        release_time_div = movie_dd.select_one('.movie-hover-info .movie-hover-title:last-child')
        release_time = release_time_div.text.replace('上映时间:', '').strip()


        thumb = movie_dd.select_one('.movie-hover-img')['src']

        # 存储信息到字典
        movie_info = {
            'index': index,
            'name': name,
            'score': score,
            'type': m_type,
            'stars': stars,
            'time': release_time,
            'thumb': thumb,
        }
        #time.sleep(random.uniform(1, 2))

        link_element = movie_dd.select_one('.channel-detail.movie-item-title a')
        href = link_element['href']
        base_url = "https://maoyan.com"
        full_url = urljoin(base_url, href)

        # 访问详细页面
        driver.get(full_url)
        #time.sleep(random.uniform(1, 2))
        try:
            wait = WebDriverWait(driver, 5)
            #提取发行公司
            production_distribution_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), '出品发行')]")))
            parent_div = production_distribution_title.find_element(By.XPATH, "..").find_element(By.XPATH, "..")
            production_company_element = parent_div.find_element(By.CSS_SELECTOR, ".attribute-item-content.ellipsis")
            production_company = production_company_element.text.strip()
            movie_info['company'] = production_company
            try:
                production_company = production_company_element.text.strip()
                movie_info['company'] = production_company
            except Exception as e:
                movie_info['company'] = '未找到公司信息'

            box_office_container = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.mod-content div.film-mbox')))
            # 提取首周票房
            first_week_box_office = box_office_container.find_elements(By.CSS_SELECTOR, '.film-mbox-item .mbox-name')
            first_week_value = first_week_box_office[0].text.strip()

            # 提取累计票房
            total_box_office = box_office_container.find_elements(By.CSS_SELECTOR,'.film-mbox-item:nth-child(2) .mbox-name')
            total_value = total_box_office[0].text.strip()

            # 存储到movie_info字典
            movie_info['first_week_box_office'] = first_week_value
            movie_info['total_box_office'] = total_value

            movie_brief_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.movie-brief-container')))
            country_time_li = movie_brief_container.find_element(By.CSS_SELECTOR, 'li.ellipsis:nth-of-type(2)')
            if country_time_li:
                country_time_text = country_time_li.text.strip()
                country, time_with_unit = country_time_text.split('/', 1)
                time = time_with_unit.split('分钟')[0].strip()
                movie_info['country'] = country
                movie_info['runtime'] = time
            else:
                movie_info['country'] = '未知国家'
                movie_info['runtime'] = '未知时长'

            index += 1
            movies.append(movie_info)

            if "猫眼验证中心" in driver.page_source:
                print("信息界面美团验证")
                # 添加等待处理验证的逻辑
                while "猫眼验证中心" in driver.page_source:
                    print("请手动处理验证页面...")
                    time.sleep(10)  # 足够的时间处理验证
            else:
                pass
        except Exception as e:
            print(f"Error processing movie {index}: {e}")

    return movies


seen_movies = set()
def write_to_file(items):
    global seen_movies
    if not items:
        print("No movies to write to the file.")
        return
    try:
        with open('猫眼2.csv', 'a', encoding='utf_8_sig', newline='') as f:
            fieldnames = ['index', 'name', 'score', 'type', 'stars', 'time', 'thumb', 'country', 'runtime','company','first_week_box_office','total_box_office']
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            # 只在文件为空时写入表头
            if f.tell() == 0:
                writer.writeheader()

            for item in items:
                if item['name'] not in seen_movies:
                    seen_movies.add(item['name'])
                    writer.writerow(item)
                    print(f"Writing movie {item['name']} to CSV.")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


def main(num_pages):
    edge_options = webdriver.EdgeOptions()
    driver = webdriver.Edge(options=edge_options)

    start_page = 10

    for i in range(start_page, start_page + num_pages):  # 循环指定的次数，对应特定数量的页面
        offset = i * 30
        url = f'https://www.maoyan.com/films?showType=3&sortId=3&offset={offset}'
        driver.get(url)
        html = driver.page_source

        time.sleep(random.uniform(1, 2))

        if html:
            items = list(parse_one_page3(html))
            write_to_file(items)

    driver.quit()


def check_csv_has_data(filename):
    try:
        with open(filename, 'r', encoding='utf_8_sig') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过表头
            return any(reader)  # 检查是否有数据行
    except FileNotFoundError:
        with open(filename, 'w', encoding='utf_8_sig', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['index', 'name', 'score', 'type', 'stars', 'time', 'thumb', 'country', 'runtime','company','first_week_box_office','total_box_office'])  # 包含index字段的表头
        return False
    except Exception as e:
        print(f"Error checking CSV: {e}")
        return False



if __name__ == '__main__':
    print("Starting single process run...")
    main(10)
    time.sleep(4)
    if check_csv_has_data('猫眼2.csv'):
        print("CSV contains data, starting multiprocessing...")
    else:
        print("CSV is empty after single process run. Check the code and try again.")





