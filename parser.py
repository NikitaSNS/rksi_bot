

def main():
    print('lol')


if __name__ == '__main__':
    main()


# from bs4 import BeautifulSoup, NavigableString
# import requests
# from models import Group, Lesson
#
# group_name = 'ПОКС-42'
#
# siteHtml = requests.post('http://m.rksi.ru',
#                          {'group': group_name.encode('cp1251'), 'stt': u'Показать!'.encode('cp1251')})
#
# data = siteHtml.text
#
# soup = BeautifulSoup(data, "html.parser")
#
# content = soup.find("div", {"class": "text"}).find('div')
#
# lessons = []
# lessonIndex = 0
#
# Group.create(group_name)
#
# for tag in content.children:
#     if tag.name == 'h3' or tag.name == 'form' or tag.name == 'br' or type(tag) is NavigableString:
#         continue
#
#     if tag.name == 'hr':
#         lessonIndex += 1
#         continue
#
#     if len(lessons) != lessonIndex + 1:
#         lessons.append([])
#
#     lessons[lessonIndex].append(tag)
#
# classedLessons = []
#
# for data in lessons:
#
#     date = data.pop(0).text
#
#     currentInfoCounter = 0
#
#     for item in data:
#         time = ''
#         auditory = ''
#         lecturer = ''
#         name = ''
#         for lessonInfo in item.children:
#             if lessonInfo.name == 'br':
#                 continue
#
#             if type(lessonInfo) is NavigableString:
#                 if currentInfoCounter == 0:
#                     time = lessonInfo
#                     currentInfoCounter += 1
#                 elif currentInfoCounter == 1:
#                     lecturer, auditory = lessonInfo.split(', ')
#                     currentInfoCounter = 0
#             else:
#                 name = lessonInfo.text
#
#         classedLesson = []
#
#
#
