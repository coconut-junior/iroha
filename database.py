import sqlite3
import os

con = None
c = None

files = os.listdir('.')

if not 'users.db' in files:
    con = sqlite3.connect('users.db')
    c = con.cursor()
    c.execute("create table users (uid,user_name,iroha_name, last_message, last_response)")
else:
    con = sqlite3.connect('users.db')
    c = con.cursor()


def addUser(uid):
    global con
    global c
    c.execute("select * from users where uid=:uid",{"uid":uid})
    if c.fetchone() == None:
        print('creating entry for ' + str(uid) + "...")
        c.execute("insert into users values (:uid, :user_name, :iroha_name, :last_message, :last_response)", {"uid":uid, "user_name":"dude", "iroha_name":"iroha", "last_message":"", "last_response":""})

    con.commit()

def updateUser(uid, user_name, iroha_name, last_message, last_response):
    global con
    global c
    c.execute("select * from users where uid=:uid",{"uid":uid})
    c.execute("update users set user_name=:user_name where uid=:uid",{"uid":uid,"user_name":user_name})
    c.execute("update users set iroha_name=:iroha_name where uid=:uid",{"uid":uid,"iroha_name":iroha_name})
    c.execute("update users set last_message=:last_message where uid=:uid",{"uid":uid,"last_message":last_message})
    c.execute("update users set last_response=:last_response where uid=:uid",{"uid":uid,"last_response":last_response})
    con.commit()

def getUser(uid):
    global con
    global c
    addUser(uid)
    c.execute("select * from users where uid=:uid",{"uid":uid})
    return c.fetchone()

print("loading database...")
