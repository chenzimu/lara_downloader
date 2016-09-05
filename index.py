import requests
import urllib.parse as urlparse
from bs4 import BeautifulSoup

base_url = 'https://laracasts.com'
srcs = []

def get_video_url(href, session):
    series_page = session.get(href)
    # print(series_page.text)
    series_page_soup = BeautifulSoup(series_page.text)
    video_src = 'http:' + series_page_soup.find('source', {'data-quality' : 'HD'})['src']
    # video_src_dic = dict(urlparse.parse_qs(urlparse.urlsplit(video_src).query))
    # data = {'profile_id' : video_src_dic['profile_id'][0], 's' : video_src_dic['s'][0]}
    # video_res = requests.get(video_src, allow_redirects=False)







# Get Csrf Token
session = requests.Session()
index = session.get('https://laracasts.com')
cookie = index.headers['set-cookie']
index_soup = BeautifulSoup(index.content, 'html.parser')
token = index_soup.find('login-button')['token']
# Login
payload = {
    'email': 'sdlichen@gmail.com',
    'password': 2668739128,
    '_token': token
}
url = 'https://laracasts.com/sessions'
headers = {
    'cookie': cookie
}
r = session.post(url, data=payload, headers=headers)

if r.status_code == 200:
    print('Login successfully!')
    response = requests.get('https://laracasts.com/series/vim-mastery')
    response_soup = BeautifulSoup(response.text)
    title_list = response_soup.find_all('span', {'class' : 'Lesson-List__title'})
    for title in title_list:
        href = base_url + title.a['href']
        get_video_url(href, session)
else:
    print(r.text)


