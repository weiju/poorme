import sys

from MySQLdb import OperationalError
import MySQLdb

DB_DRIVER = "MySQLdb"

DB_ARGS = {
    'db': 'poopreporter',
    'user': 'dj_ango',
    'passwd': 'django',
    'host': 'superfiretruck.com'
}   

def simpleConnect():
    global DB_ARGS
    print "simple connect"
    print DB_ARGS
    return MySQLdb.connect(DB_ARGS['host'], DB_ARGS['user'], DB_ARGS['passwd'], DB_ARGS['db'])

filename = sys.argv[1]

lines = open(filename).readlines()

db = simpleConnect()
print "connected"
cur = db.cursor()

print db, cur

for line in lines:
    data = eval(line)

    # step 1: figure out who the user is 
    cur.execute("insert ignore into auth_user (username, first_name, last_name) values (%s, %s, %s)", (data['firstname'], data['firstname'], data['lastname']))

    user_id = cur.lastrowid

    print "user made", user_id

    if user_id:
        # step 2: make a sickness episode with user_id, date, and zipcode

        cur.execute("insert into poopreporter_episode (user_id, started, zipcode) values (%s, %s, %s)", (user_id, data['date'], data['zipcode']))

        episode_id = cur.lastrowid

        cur.execute("insert into poopreporter_loggedincomment (user_id, episode_id, text) values (%s, %s, 'i am sick')", (user_id, episode_id))

        print "episode made", episode_id

        # step 3: make an update for that episode and provide a comment

        cur.execute("insert into poopreporter_update (episode_id, time) values (%s, %s)", (episode_id, data['date']))

        update_id = cur.lastrowid

        print "update id", update_id

        # step 4: add symptoms to that update

        symptoms = data['symptoms'].split(",")
        for s in symptoms:
            print "symptom", s
            cur.execute("insert into poopreporter_update_symptoms (update_id, symptom_id) values (%s, %s)", (update_id, s))    
    
    
    #cur.execute(q)

db.commit()