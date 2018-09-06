import pyodbc
import sqlalchemy
from creds import db_credentials as DBcreds
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class DatabaseManager:

    def __init__(self):
        # connstring = 'Driver={0};Server={1};Database={2};Uid={3};Pwd={4};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
        connstring = 'mssql+pyodbc://{3}:{4}@{1}:1433/{2}?driver=ODBC+Driver+13+for+SQL+Server'
        # TODO: Fix less privileged user in database
        self.engine = create_engine(connstring.format('{ODBC Driver 13 for SQL Server}',
                                                     DBcreds.host,
                                                     DBcreds.database,
                                                     DBcreds.user,
                                                     DBcreds.password))
        self.session = sessionmaker(bind=self.engine)




if __name__ == '__main__':
    db = DatabaseManager()
    print(db.engine)
    print(db.session)
    import pickle
    with open('dump.pkl', 'rb') as f:
        dump = pickle.load(f)

