from creds import db_credentials as DBcreds
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from io import StringIO
import csv
from models import Base, ConsultingServicesTouchpoint
import logging

class DatabaseManager:

    def __init__(self):
        connstring = 'mssql+pyodbc://{3}:{4}@{1}:1433/{2}?driver=ODBC+Driver+13+for+SQL+Server'
        self.engine = create_engine(connstring.format('{ODBC Driver 13 for SQL Server}',
                                                      DBcreds.host,
                                                      DBcreds.database,
                                                      DBcreds.user,
                                                      DBcreds.password))
        logging.debug('Database engine set up')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        logging.info('Database session initiated')