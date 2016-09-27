import requests
import urllib.parse as urlparse
import sys
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
    for filename, url in urls_dict.items():
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
        video_src = base_url + \
            series_page_soup.find('a', {'title': 'Download Video'})['href']
        video_get_location = session.get(video_src, allow_redirects=False)
        video_location = 'https:' + video_get_location.headers['location']
        get_video = requests.get(
            video_location, allow_redirects=False, proxies=proxies)
        video_download_location = get_video.headers['location']
        # 获取文件的文件名
        pased_location = urlparse(video_download_location)
        print(video_download_location)
        with open('url.txt', 'a') as o:
            o.write(video_download_location + '\n')
        pased_location_query = parse_qs(pased_location.query)
        download_video_dict[
            pased_location_query['filename'][0]] = video_download_location
    # begin_download(download_video_dict)


def download_init():
    """
    这个函数的作用是根据用户名和密码获取所有的链接地址
    :param username:
    :param password:
    :return:
    """
    username = sys.argv[1]
    password = sys.argv[2]
    down_url = sys.argv[3]
    hrefs = []
    session = requests.Session()
    index = session.get('https://laracasts.com', proxies=proxies)
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
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': cookie,
        'origin': 'https://laracasts.com',
        'pragma': 'no-cache',
        'referer': 'https://laracasts.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
        'x-csrf-token': token,
        'x-requested-with': 'XMLHttpRequest'
    }

    r = session.post(url, data=payload, headers=headers)

    if r.status_code == 200:
        print('Login successfully!')
        response = requests.get(down_url)
        response_soup = BeautifulSoup(response.text)
        title_list = response_soup.find_all(
            'span', {'class': 'Lesson-List__title'})
        for title in title_list:
            hrefs.append(base_url + title.a['href'])
        get_video_url(hrefs, session)
    else:
        print(r.headers)
        print(r)


# init
download_init()
