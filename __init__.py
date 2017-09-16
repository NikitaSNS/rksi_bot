__all__ = [
    'db', 'Group'
]

db.bind(provider='postgres', user='nikita', password='', host='', database='template1')

db.generate_mapping(create_tables=True, check_tables=False)

print('__init__')

