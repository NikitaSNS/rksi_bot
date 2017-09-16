from models import *

if db.provider is None:  # is work ok?
    sql_debug(True)
    db.bind(provider='postgres', user='postgres', password='', host='', database='nikita')
    db.generate_mapping(create_tables=True, check_tables=True)
