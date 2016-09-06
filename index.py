import requests
import urllib.parse as urlparse
import os
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

base_url = 'https://laracasts.com'

# 下载需要代理
proxies = {
  'https': 'http://127.0.0.1:1080',
}

def begin_download(urls_dict):
    print('############################')
    print('############################')
    print('#######START DOWNLOAD#######')
    print('############################')
    print('############################')
    for filename,url in urls_dict.items():
        with open(filename, 'wb') as file_obj:
            print('Downloding %s ***********************' % filename)
            r = requests.get(url, stream=True)
            total_length = r.headers['content-type']

            if total_length is None:
                file_obj.write(r.content)
            else:
                for data in r.iter_content(chunk_size=4096):
                    file_obj.write(data)


def get_video_url(hrefs, session):
    """
    这个函数的作用是根据获取到的a链接得到视频真正的下载地址
    :param hrefs:
    :param session:
    :return:
    """
    download_video_dict = {}
    for href in hrefs:
        series_page = session.get(href)
        series_page_soup = BeautifulSoup(series_page.text)
        video_src = base_url + series_page_soup.find('a', {'title' : 'Download Video'})['href']
        video_get_location = session.get(video_src, allow_redirects=False)
        video_location = 'https:' + video_get_location.headers['location']
        get_video = requests.get(video_location, allow_redirects=False, proxies=proxies)
        video_download_location = get_video.headers['location']
        # 获取文件的文件名
        pased_location = urlparse(video_download_location)
        print(video_download_location)
        with open('url.txt', 'a') as o:
            o.write(video_download_location + '\n')
        pased_location_query = parse_qs(pased_location.query)
        download_video_dict[pased_location_query['filename'][0]] = video_download_location
    # begin_download(download_video_dict)

def download_init(username, password, down_url):
    """
    这个函数的作用是根据用户名和密码获取所有的链接地址
    :param username:
    :param password:
    :return:
    """
    hrefs = []
    session = requests.Session()
    index = session.get('https://laracasts.com')
    cookie = index.headers['set-cookie']
    index_soup = BeautifulSoup(index.content, 'html.parser')
    token = index_soup.find('login-button')['token']
    # Login
    payload = {
        'email': username,
        'password': password,
        '_token': token
    }
    url = 'https://laracasts.com/sessions'
    headers = {
        'cookie': cookie
    }
    r = session.post(url, data=payload, headers=headers)

    if r.status_code == 200:
        print('Login successfully!')
        response = requests.get(down_url)
        response_soup = BeautifulSoup(response.text)
        title_list = response_soup.find_all('span', {'class': 'Lesson-List__title'})
        for title in title_list:
            hrefs.append(base_url + title.a['href'])
        get_video_url(hrefs, session)
    else:
        print(r.text)


# init
download_init('sdlichen@gmail.com', 2668739128, 'https://laracasts.com/series/learning-vue-step-by-step')
