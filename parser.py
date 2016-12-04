import re
from urllib.request import urlopen, Request
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

regex = '// flash 오류를 우회하기 위한 함수 추가|function _flash_removeCallback\(\) \{\}|\n'
NEWS_CATEGORY = {
    'policy': 'http://news.naver.com/main/list.nhn?sid2=269&sid1=100&mid=shm&mode=LS2D&date=',
    'economy': 'http://news.naver.com/main/list.nhn?sid2=263&sid1=101&mid=shm&mode=LS2D&date=',
    'society': 'http://news.naver.com/main/list.nhn?sid2=257&sid1=102&mid=shm&mode=LS2D&date=',
    'culture': 'http://news.naver.com/main/list.nhn?sid2=245&sid1=103&mid=shm&mode=LS2D&date=',
    'world': 'http://news.naver.com/main/list.nhn?sid2=322&sid1=104&mid=shm&mode=LS2D&date=',
    'it/science': 'http://news.naver.com/main/list.nhn?sid2=228&sid1=105&mid=shm&mode=LS2D&date='
}


def parser(target_url):
    """Get news title and new body

    Args:
        :param target_url: url of news

    Returns:
        Title and body of news
    """
    bs = BeautifulSoup(urlopen(target_url).read(), 'html.parser')
    title = bs.find('h3', {'id': 'articleTitle'}).text
    body = bs.find('div', {'id': 'articleBodyContents'}).text
    body = re.sub(regex, '', body)
    return title, body


def get_url_list(target_date):
    """Get news urls of given date

    Args:
        :param target_date: date

    Return:
        List of news url
    """
    url_list = []
    for category, category_url in NEWS_CATEGORY.items():
        prev_page_num = 0
        while 1:  # TODO: 중간에 html 일부만 파싱되는 문제
            try:
                page_url = category_url + target_date + '&page=%d' % (int(prev_page_num) + 1)
                req = Request(page_url)
                # req = Request(page_url, headers='Mozilla/5.0')
                bs = BeautifulSoup(urlopen(req), 'html.parser')
                curr_page_num = bs.find('div', {'class': 'paging'}).find('strong').text
            except AttributeError:
                break

            if prev_page_num == curr_page_num:
                break

            for soup in bs.find('ul', {'class': 'type06_headline'}).find_all('a'):
                url_list.append(soup.attrs['href'])
            prev_page_num = curr_page_num
    return list(set(url_list))


if __name__ == '__main__':
    start = datetime(2016, 1, 1)
    end = datetime(2016, 11, 30)
    for day in range(int((end-start).days)+1):
        date = (start+timedelta(days=day)).strftime('%Y%m%d')
        for url in get_url_list(date):
            print(parser(url))
    # print(parser('http://news.naver.com/main/read.nhn?mode=LS2D&mid=shm&sid1=101&sid2=263&oid=001&aid=0008866177'))
