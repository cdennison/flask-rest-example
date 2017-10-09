from sqlalchemy import *

db = create_engine('sqlite:///file::memory:')

db.echo = True  # Try changing this to True and see what happens

metadata = MetaData(db)

import csv
import traceback

rows_for_insert = []

DELIM1='|'
DELIM2=','

with open('code_challenge_question_dump.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)

    for index,row in enumerate(csvReader):
        row_to_insert = {
            'question':'',
            'answer':'',
            'distraction1':'',
            'distraction2':'',
            'distraction3':'',
            'distraction4':'',
            'distraction5':''
        }

        #Skip header
        if index==0:
            continue
        try:
            row_to_insert['question']=row[0].split(DELIM1)[0]
            row_to_insert['answer']=row[0].split(DELIM1)[1]
            row_to_insert['distraction1']=row[0].split(DELIM1)[2]
            for i,d in enumerate(row[1:]):
                    row_to_insert['distraction%s'%(i+2)]=d
        except:
            print ('Failed to parse row: '+str(row))
            print (traceback.format_exc())

        # print(row_to_insert)
        rows_for_insert.append(row_to_insert)


# class Company(db.Model):
#     __tablename__ = 'companies'
#
#     id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
#     name = db.Column(db.String(20), nullable=False)
#     country_code = db.Column(db.String(2), nullable=False)
#     website = db.Column(db.String(100))
#     enabled = db.Column(db.Boolean(), nullable=False, default=True)
#     updated_at = db.Column(db.DateTime(), nullable=False, default=lambda: datetime.utcnow())
#     created_at = db.Column(db.DateTime(), nullable=False, default=lambda: datetime.utcnow())

class Problems(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    country_code = db.Column(db.String(2), nullable=False)
    website = db.Column(db.String(100))
    enabled = db.Column(db.Boolean(), nullable=False, default=True)
    updated_at = db.Column(db.DateTime(), nullable=False, default=lambda: datetime.utcnow())
    created_at = db.Column(db.DateTime(), nullable=False, default=lambda: datetime.utcnow())

problems = Table(
    'problems', metadata,
     Column('id', Integer, primary_key=True, nullable=False),  # defaults to auto inc
     Column('question', String(100), nullable=False),
     Column('answer', String(100), nullable=False),
     Column('distraction1', String(100)),
     Column('distraction2', String(100)),
     Column('distraction3', String(100)),
     Column('distraction4', String(100)),
     Column('distraction5', String(100))
   )
# problems.drop()

problems.create()

# i = users.insert()
# i.execute(question='Q?', answer="A")
# i.execute(question='', answer="A")

i = problems.insert()
for row in rows_for_insert:
    i.execute(**row)



for i in users.query.all():
    print (i)

    # s = users.select()
    # rs = s.execute()
    #
    # row = rs.fetchall()
    #
    # for row in rs:
    #     print (row)
