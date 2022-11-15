rm db.sqlite3
rm -rf ./rareserverapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations rareserverapi
python3 manage.py migrate rareserverapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata members
python3 manage.py loaddata reactions
python3 manage.py loaddata categories
python3 manage.py loaddata tags
python3 manage.py loaddata subscriptions
python3 manage.py loaddata posts
python3 manage.py loaddata comments