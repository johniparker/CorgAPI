import psycopg2 as pc2
from CorgAPI.config.config import db_config

def create_conn():
    try:
        connection_params = {**db_config}
        conn = pc2.connect(**connection_params)
        return conn
    except Exception as e:
        print(f'[+] RDS Connection Failed:\n{e}')
        return None
    
