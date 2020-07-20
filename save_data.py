from datetime import datetime
import re
import sqlalchemy
import os

DB_NAME = 'test_db.db'


def create_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    engine = sqlalchemy.create_engine('sqlite:///' + DB_NAME)
    engine.execute("""
        create table links (
            id integer primary key,
            title varchar,
            uploaded_date date,
            location varchar,
            salary integer,
            descr varchar,
            url varchar
        )
    """)


class Pipeline:

    def __init__(self, data):
        self.data = data
        self.engine = sqlalchemy.create_engine('sqlite:///' + DB_NAME)

    def prepare_data(self, row):
        prepared_data = {}
        for key, value in row.items():
            if not value:
                continue

            value = value.strip()
            # if key == 'uploaded_date':
            #     value = datetime.strptime(value, '%d.%m.%Y').date()
            if 'url' in key:
                value = 'https://trud.ua/' + value

            if key == 'salary':
                value = int(re.search(r'[0-9]+', value).group())

            if key == 'title' or key == 'text':
                value = value.replace("'", '').replace('’', '')

            prepared_data[key] = value
        return prepared_data

    def save_data(self):

        for data in self.data:
            data = self.prepare_data(data)
            sql = """insert into links (title, 
                                    uploaded_date,
                                    location,
                                    salary,
                                    descr,
                                    url) 
                                values (
                                '{title}',
                                '{uploaded_date}',
                                '{location}',
                                {salary},
                                '{text}',
                                '{url}'
                                )
            """.format(
                        title=data.get('title'),
                       uploaded_date=data.get('uploaded_date'),
                       location=data.get('location'),
                       salary=data.get('salary', 0),
                       text=data.get('text'),
                       url=data.get('url')
                       )
            self.engine.execute(sql)

