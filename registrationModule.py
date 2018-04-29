import sqlite3
import uuid
from flask import g

DATABASE = 'test.db'

def get_db():
    db = None
    if db is None:
        db = sqlite3.connect(DATABASE)
    return db


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def add_to_db(query,args=()):
    localdb = get_db()
    cur = localdb.cursor()
    cur.execute(query,args)
    localdb.commit()
    localdb.close()

def get_all_entries():

    cur = get_db().execute("SELECT * FROM tipbotassociations")
    result = cur.fetchall()
    for r in result:
        print(r)
    cur.close()
    return result


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def registerUser(username):

    user = query_db('select * from tipbotassociations where user_id = ?', [username], one=True)
    if user is not None:
    #if localdb.execute("SELECT count(*) FROM tipbotassociations WHERE user_id=?", (username, )).fetchone()[0] > 0:
        print("UserName Already Exists")
        return user[1], True


    add_to_db('''INSERT INTO tipbotassociations(user_id, address)
                      VALUES(:user_id,:address)''',
                      {'user_id':username, 'address':str(uuid.uuid4().hex)})

    user = query_db('select * from tipbotassociations where user_id = ?', [username], one=True)
    return user[1],True                 


# Call ALL Methods and see it works
# registerUser("Test3")
# print(get_all_entries())
