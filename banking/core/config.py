import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv(Path(__file__).resolve().parents[2] / '.env')

def database_url():
    if os.getenv('DATABASE_URL'):
        return os.environ['DATABASE_URL']
    return URL.create('mysql+pymysql', username=os.getenv('MYSQL_USER', 'root'),
                      password=os.getenv('MYSQL_PASSWORD', ''),
                      host=os.getenv('MYSQL_HOST', 'localhost'),
                      port=int(os.getenv('MYSQL_PORT', '3306')),
                      database=os.getenv('MYSQL_DATABASE', 'banking_system'))
