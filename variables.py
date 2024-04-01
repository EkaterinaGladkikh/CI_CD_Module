server = 'host.docker.internal'
database_name = 'AdventureWorks2012'
username = 'UserForRobotFR'
password = 'robotframework'
port = '1433'
ENCRYPT = 'no'

connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database_name};' \
                   f'UID={username};PWD={password};ENCRYPT={ENCRYPT}'
