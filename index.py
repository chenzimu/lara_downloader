import requests
import urllib.parse as urlparse
import os
from bs4 import BeautifulSoup

base_url = 'https://laracasts.com'

# 下载需要代理
proxies = {
  'https': 'http://127.0.0.1:1080',
}

def begin_download(urls):
    os.system('D:')
    os.system('cd Program Files (x86)/Thunder Network/Thunder/Program')
    os.system('Thunder.exe')
    print(urls)

def get_video_url(hrefs, session):
    """
    这个函数的作用是根据获取到的a链接得到视频真正的下载地址
    :param hrefs:
    :param session:
    :return:
    """
    download_video_urls = []
    for href in hrefs:
        series_page = session.get(href)
        series_page_soup = BeautifulSoup(series_page.text)
        video_src = base_url + series_page_soup.find('a', {'title' : 'Download Video'})['href']
        video_get_location = session.get(video_src, allow_redirects=False)
        video_location = 'https:' + video_get_location.headers['location']
        get_video = requests.get(video_location, allow_redirects=False, proxies=proxies)
        video_download_location = get_video.headers['location']
        download_video_urls.append(video_download_location)
    begin_download(download_video_urls)

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
download_init('sdlichen@gmail.com', 2668739128, 'https://laracasts.com/series/intermediate-laravel')
