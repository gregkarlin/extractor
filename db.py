import psycopg2

connection_string = '''  host=localhost user=postgres password=lister dbname=extractor'''

conn = psycopg2.connect(connection_string)
cur = conn.cursor()

