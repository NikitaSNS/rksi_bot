from database import *
from bs4 import BeautifulSoup, NavigableString
from datetime import date, datetime
import requests
import locale
import sys

if sys.platform == 'win32':
    locale.setlocale(locale.LC_ALL, 'rus_rus')
else:
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

site = 'http://m.rksi.ru'
groupsHtml = BeautifulSoup(
    requests.post(site).text,
    'html.parser'
).find('select', {'name': 'group'}).findAll('option')


def parse_prefix(line, fmt):
    try:
        t = datetime.strptime(line, fmt)
    except ValueError as v:
        if len(v.args) > 0 and v.args[0].startswith('unconverted data remains: '):
            line = line[:-(len(v.args[0]) - 26)]
            t = datetime.strptime(line, fmt)
        else:
            raise
    return t


for group_name in groupsHtml:
    group_name = group_name.text

    with db_session:
        if len(Group.select(lambda x: x.name == group_name)) == 0:
            Group.create(group_name)

    siteHtml = requests.post(site, {'group': group_name.encode('cp1251'), 'stt': u'Показать!'.encode('cp1251')})

    data = siteHtml.text

    soup = BeautifulSoup(data, "html.parser")

    content = soup.find("div", {"class": "text"}).find('div')

    lessons = []
    lessonIndex = 0

    for tag in content.children:
        if tag.name == 'h3' or tag.name == 'form' or tag.name == 'br' or type(tag) is NavigableString:
            continue

        if tag.name == 'hr':
            lessonIndex += 1
            continue

        if len(lessons) != lessonIndex + 1:
            lessons.append([])

        lessons[lessonIndex].append(tag)

    classedLessons = []

    for data in lessons:

        dat = data.pop(0).text.split(', ')[0]

        dt = parse_prefix(dat, '%d %b').replace(year=2017).date()
        with db_session:
            Lesson.select(lambda l: l.date == dt and l.group.name == group_name).delete()
        currentInfoCounter = 0

        for item in data:
            time = ''
            audience = ''
            lecturer = ''
            name = ''
            for lessonInfo in item.children:
                if lessonInfo.name == 'br':
                    continue

                if type(lessonInfo) is NavigableString:
                    if currentInfoCounter == 0:
                        time = lessonInfo
                        currentInfoCounter += 1
                    elif currentInfoCounter == 1:
                        lecturer, audience = lessonInfo.split(', ')
                        currentInfoCounter = 0
                        audience = audience.split('. ')[1]
                else:
                    name = lessonInfo.text
            Lesson.create(name, lecturer, audience, dt, time, group_name)
            classedLesson = []
