from datetime import date
from pony.orm import *

db = Database()

# sql_debug(True)

# db.bind(provider='postgres', user='nikita', password='', host='', database='template1')


class Group(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str, unique=True)
    lessons = Set('Lesson')

    @staticmethod
    @db_session
    def create(name):
        group = Group(name=name)
        return group


class Lesson(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    lecturer = Optional(str)
    audience = Optional(str)
    date = Optional(date)
    time = Optional(str)
    group = Required(Group)

    @staticmethod
    @db_session
    def create(name, lecturer, audience, date, time, group_name):
        lesson = Lesson(name=name, lecturer=lecturer, audience=audience, date=date, time=time,
                        group=Group.get(name=group_name))
        return lesson

#
# db.generate_mapping(create_tables=True, check_tables=False)
