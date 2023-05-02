import asyncio
import httpx
import rutimeparser as rt
import datetime as dt
from bs4 import BeautifulSoup as bs

# All functions

async def get_list_of_unikum_groups() -> list:
    url = 'https://genius-school.kuzstu.ru/расписание/'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    soup = bs(response.text, "html.parser")

    groups_urls = soup.find_all('a')

    return [i.text for i in groups_urls if '-' in i.text]


async def get_list_of_kuzgtu_groups() -> list:
    url = 'https://kuzstu.ru/web-content/sitecontent/studentu/raspisanie/raspisan.html'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    soup = bs(response.text, "html.parser")

    groups_urls = soup.find_all('a')

    return [i.text for i in groups_urls if i.text]


async def get_unikum_url(group: str) -> str:
    url = 'https://genius-school.kuzstu.ru/расписание/'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    soup = bs(response.text, "html.parser")

    groups_urls = soup.find_all('a', string=group)

    if groups_urls:
        async with httpx.AsyncClient() as client:
            response = await client.get(groups_urls[0]['href'])

        return response.headers['location']
    
    return ''


def get_kuzgtu_url(group: str) -> str:
    url = f'https://kuzstu.ru/web-content/sitecontent/studentu/raspisanie/{group}.html'
    return url


async def get_unikum_lessons(group: str, search_type: str) -> list:
    url = await get_unikum_url(group)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    soup = bs(response.text, "html.parser")
    lines = soup.find_all('tr')

    lessons = []

    for line in lines:
        little_soup = bs(str(line), "html.parser")
        spans = little_soup.find_all('span', class_='s1')
        line_date = rt.parse(spans[0].text)
        if line_date != None:
            line_date = line_date.replace(year=dt.datetime.now().year)
            if search_type == 'today':
                if line_date == dt.datetime.now().date():
                    lessons = [(i, j.replace('/n', '').replace('/xa0', '')) for i, j in enumerate([span.text for span in spans]) if j]
                    break
            elif search_type == 'coming':
                if line_date >= dt.datetime.now().date() and len(list(filter(lambda x: x.text.replace('\n', '').replace('\xa0', ''), spans))) > 1:
                    lessons = [(i, j.replace('/n', '').replace('/xa0', '')) for i, j in enumerate([span.text for span in spans]) if j]
                    break
            elif search_type == 'week':
                if line_date.isocalendar().week == dt.datetime.now().isocalendar().week and len(list(filter(lambda x: x.text.replace('\n', '').replace('\xa0', ''), spans))) > 1:
                    lessons.append([line_date] + [(i, j.replace('/n', '').replace('/xa0', '')) for i, j in enumerate([span.text for span in spans[1:]]) if j])
                elif line_date.isocalendar().week > dt.datetime.now().isocalendar().week:
                    break
    
    
    if search_type != 'week':
        lessons[0] = line_date

    return lessons


async def get_kuzgtu_lessons(group: str, search_type: str) -> list:
    url = get_kuzgtu_url(group)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    soup = bs(response.text, "html.parser")
    lines = soup.find_all('tr')

    lessons = []

    for line in lines:
        little_soup = bs(str(line), "html.parser")
        ps = little_soup.find_all('p')
        line_date = rt.parse(ps[0].text)
        if line_date != None:
            line_date = line_date.replace(year=dt.datetime.now().year)
            if search_type == 'today':
                if line_date == dt.datetime.now().date():
                    lessons = [(i, j.replace('_', '').strip()) for i, j in enumerate([p.text for p in ps]) if j.replace('_', '').strip()]
                    break
            elif search_type == 'coming':
                if line_date >= dt.datetime.now().date() and len(list(filter(lambda x: x.text.replace('_', '').strip(), ps))) > 1:
                    lessons = [(i, j.replace('_', '').strip()) for i, j in enumerate([p.text for p in ps]) if j.replace('_', '').strip()]
                    break
            elif search_type == 'week':
                if line_date.isocalendar().week == dt.datetime.now().isocalendar().week and len(list(filter(lambda x: x.text.replace('_', '').strip(), ps))) > 1:
                    lessons.append([line_date] + [(i, j.replace('_', '').strip()) for i, j in enumerate([p.text for p in ps[1:]]) if j.replace('_', '').strip()])
                elif line_date.isocalendar().week > dt.datetime.now().isocalendar().week:
                    break
    
    if search_type != 'week' and len(lessons):
        lessons[0] = line_date

    return lessons

# Functions with organization choice (KuzGTU or UnikUm) for more comfort

async def get_groups(organization: str) -> list:
    if organization == 'КузГТУ':
        return await get_list_of_kuzgtu_groups()
    
    elif organization == 'УникУм':
        return await get_list_of_unikum_groups()
    
    return []


async def get_url(group: str, organiztion: str) -> str:
    if organiztion == 'КузГТУ':
        return get_kuzgtu_url(group)
    # You may think thats a mistake, but all kuzgtu urls are constants unlike UnikUm
    # So we don't have to parse urls from site
    # I checked and every group workew without any errors or mistakes
    
    elif organiztion == 'УникУм':
        return await get_unikum_url(group)
    
    return ''


async def get_lessons(organization: str, group: str, search_type: str) -> list:
    if organization == 'КузГТУ':
        return await get_kuzgtu_lessons(group, search_type)
    
    elif organization == 'УникУм':
        return await get_unikum_lessons(group, search_type)
    
    return []


async def main():
    a = await get_lessons('КузГТУ', 'ТАт-202', 'coming')
    print(a)

asyncio.run(main())