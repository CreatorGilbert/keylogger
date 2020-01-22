from werkzeug.security import check_password_hash, generate_password_hash

import sqlite3
import sys

# Get username and password
conn = sqlite3.connect('instance/commandr.sqlite')
db = conn.cursor()
username = sys.argv[1]
password = sys.argv[2]

# Add fake data to the database for testing purposes
db.execute(
    'INSERT INTO user (username, password) VALUES (?, ?)',
    (username, generate_password_hash(password))
)
'''
db.execute(
    'INSERT INTO trojan (ip, port) VALUES (?, ?)',
    ('127.0.0.1', 5000)
)
db.execute(
    'INSERT INTO trojan (ip, port) VALUES (?, ?)',
    ('192.168.0.1', 50000)
)
'''

# Check data was successfully added
print('SELECT * FROM user:')
for row in db.execute('SELECT * FROM user'):
    print(row)
print()
print('SELECT * FROM trojan:')
for row in db.execute('SELECT * FROM trojan'):
    print(row)

# Commit changes to database and close
conn.commit()
conn.close()
