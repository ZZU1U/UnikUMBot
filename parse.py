from bs4 import BeautifulSoup as bs
import datetime as dt
import rutimeparser as rt
import requests


LESSONS_WEEKDAY = {
    1: ('8:30', '10:00'),
    2: ('10:20', '11:50'),
    4: ('15:20', '16:50'),
    5: ('17:00', '18:30'),
    6: ('18:40', '20:10')
}

LESSONS_WEEKEND = {
    1: ('9:00', '10:30'),
    2: ('10:40', '12:10'),
    3: ('12:30', '14:00'),
    4: ('14:10', '15:40'),
    5: ('16:00', '17:30'),
    6: ('17:40', '19:10')
}


def getLessons(group: str, date: str = 'now') -> str:
    url = "https://genius-school.kuzstu.ru/расписание/"

    r = requests.get(url)
    r.encoding = 'utf-8'

    soup = bs(r.text, "html.parser")
    groupsurl = soup.find_all('a', string=group)

    url = groupsurl[0]['href']

    r = requests.get(url)
    r.encoding = 'utf-8'

    soup = bs(r.text, "html.parser")
    lines = soup.find_all('tr')
    lessons = []

    for line in lines:
        soupTemp = bs(str(line), "html.parser")
        spans = soupTemp.find_all('span', class_='s1')
        lineDate = rt.parse(spans[0].text)
        if lineDate != None:
            if date == 'now':
                if lineDate.month == dt.datetime.now().month and lineDate.day == dt.datetime.now().day:
                    lessons = [(i, j.replace('/n', '').replace('/xa0', '')) for i, j in enumerate([span.text for span in spans]) if j]
                    break
            if date == 'anywhen':
                if lineDate.month >= dt.datetime.now().month and lineDate.day >= dt.datetime.now().day and len([1 for span in spans if span.text.replace('\n', '').replace('\xa0', '')]) > 1:
                    lessons = [(i, j.replace('\n', '').replace('\xa0', '')) for i, j in enumerate([span.text for span in spans]) if j]
                    break
    message = ""

    if len(lessons) > 1:
        lessonsDict = {}

        for id, lesson in lessons[1:]:
            lessonsDict[lesson] = lessonsDict.get(lesson, []) + [id]

        if lineDate.weekday() < 5:
            lessonsInfo = '\n'.join([f" - {lesson}: {LESSONS_WEEKDAY[times[0]][0]}-{LESSONS_WEEKDAY[times[-1]][1]}" for lesson, times in lessonsDict.items()])
        else:
            lessonsInfo = '\n'.join([f" - {lesson}: {LESSONS_WEEKEND[times[0]][0]}-{LESSONS_WEEKEND[times[-1]][1]}" for lesson, times in lessonsDict.items()])

        message = f"{lineDate.strftime('%Y.%m.%d')} 📚\n{lessonsInfo}"

    return message


def isGroup(group: str) -> bool:
    url = "https://genius-school.kuzstu.ru/расписание/"

    r = requests.get(url)
    r.encoding = 'utf-8'

    soup = bs(r.text, "html.parser")
    groups = soup.find_all('a')
    
    groups = filter(lambda y: '-' in y, map(lambda x: x.text, groups))

    return group in groups
