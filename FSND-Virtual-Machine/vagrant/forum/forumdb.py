#
# Database access functions for the web forum.
#

import time, psycopg2

## Database connection

## Get posts from database.
def GetAllPosts():
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    s = c.execute("SELECT time, content from posts order by time desc")
    print (s)
    DB.close()


## Add a post to the database.
def AddPost(content):
    DB = psycopg2.connect("dbname=forum")
    c = DB.cursor()
    c.execute("INSERT INTO posts (content) values (%s)", (content,))
    DB.commit()
    DB.close()


AddPost('hwsdff')
GetAllPosts()