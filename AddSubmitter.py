import praw
import time
import sqlite3

# insert credentials below

print('Connecting...')
reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='python:script.AddSubmitter:v1.0.0 (by /u/utkarshmttl)',
                     username='',
                     password='')
print('Connected.')

KEY = ['asdfghjkl']

sql = sqlite3.connect('sql.db')
print('Loaded SQL Database')
cur = sql.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)')
cur.execute('CREATE INDEX IF NOT EXISTS oldpost_index ON oldposts(id)')
print('Loaded table')

sql.commit()



subreddit = reddit.subreddit('HashInclude')

def scanmessages():
    print('Getting HashInclude modmail')
    modmail = list(subreddit.mod.unread())
    for message in modmail:
        cur.execute('SELECT * FROM oldposts WHERE ID=?', [message.fullname])
        if not cur.fetchone():
            print(message.fullname)
            try:
                mauthor = message.author
                msubject = message.subject.lower()
                if any(keyword.lower() in msubject for keyword in KEY):
                    print('\tApproving ' + mauthor)
                    subreddit.contributor.add(mauthor)
                    message.mark_read()
            except AttributeError:
                print('Failed to fetch username')
            cur.execute('INSERT INTO oldposts VALUES(?)', [message.fullname])
            sql.commit()


while True:
    try:
        scanmessages()
    except Exception as e:
        print('ERROR: ' + str(e))
    sql.commit()
    print('Running again in 60 seconds \n_________\n')
    time.sleep(60)
# for contributor in subreddit.contributor():
#     print(contributor)

# subreddit.contributor.add('mttlutkarsh')


# print('added')

# for contributor in subreddit.contributor():
#     print(contributor)

# print ('done')