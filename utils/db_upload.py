import sqlite3
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError

# Database
class DatabaseApp:
    def __init__(self, db_type, **kwargs):
        self.db_type = db_type
        self.conn = None
        self.cursor = None

        if db_type == 'sqlite':
            self.connect_sqlite(**kwargs)
        elif db_type == 'mysql':
            self.connect_mysql(**kwargs)
        else:
            raise ValueError("Database unsupported")

    def connect_sqlite(self, **kwargs):
        db_file = kwargs.get('local_db_file')
        try:
            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()
            print('Connect successful')
        
        except Exception as e:
            print(f'Connect failed: {e}')

    def connect_mysql(self, **kwargs):
        self.host = kwargs.get('host', '')
        self.port = kwargs.get('port', )
        self.user = kwargs.get('user', '')
        self.password = kwargs.get('password', '')
        self.database = kwargs.get('database', '')

        try:
            '''
            self.conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )'''
            self.conn = sqlalchemy.create_engine(f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")
            print(f'======================{self.conn}===================')
            self.conn.connect()
            #self.cursor = self.conn.cursor()
            if self.conn:
                print('Connect successful')
            else:
                self.connect_sqlite(**kwargs)
            
        except SQLAlchemyError as e:
            print(f'Connect failed: {e}')
            print('Trying connect to SQLite')
            self.connect_sqlite(**kwargs)

    def create_table(self, table_name, columns, db_type):
        try:
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
            if db_type == 'sqlite':
                self.cursor.execute(create_table_sql)
            print(f'Form created: {table_name}')
        except Exception as e:
            print(f'Form create failed: {e}')

    def drop_table(self, table_name):
        try:
            drop_table_sql = f"DROP TABLE IF EXISTS {table_name}"
            self.cursor.execute(drop_table_sql)
            self.conn.commit()
            print(f'Table dropped: {table_name}')
        except Exception as e:
            print(f'Delete table failed: {e}')

    def insert_dataframe(self, table_name, dataframe):
        try:
            dataframe.to_sql(table_name, self.conn, index=False, if_exists='append')
            print(f'Table inserted: {table_name}')
        except Exception as e:
            print(f'Insert table failed: {e}')

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f'Query failed: {e}')
            return []

    def disconnect(self, db_type):
        if self.conn:
            if db_type == 'sqlite':
                self.cursor.close()
                self.conn.close()
            print('Disconnect from database')

# Update to database
def update_database(permission, sql_df):
    # Database
    #db_app = DatabaseApp(db_type='sqlite', local_db_file='Cathay_Autotest')
    db_type = 'mysql' if permission == 'ADMIN' else 'sqlite'
    db_app = DatabaseApp(db_type = db_type,
                         host = <'HOST'>,
                         port = <'PORT'>,
                         user = <'USER'>,
                         password = <'PASSWORD'>,
                         database = <'DB'>,
                         local_db_file = <'LOCAL DB'>)

    # Login to database
    #db_app.connect()

    # Manipulate tables
    table_name = 'Test_report'
    columns = ('Start_time TEXT, Platform TEXT, Device TEXT,'
               'Test_case TEXT, Test_item TEXT, Test_title TEXT,'
               'End_time TEXT, Elapsed_time TEXT, Test_result BOOLEAN,'
               'Issue_track TEXT')
    db_app.create_table(table_name, columns, db_type)
    db_app.insert_dataframe(table_name, sql_df)
    #query = 'SELECT * FROM autotest.result_list;'
    # Disconnect from database
    db_app.disconnect(db_type)
