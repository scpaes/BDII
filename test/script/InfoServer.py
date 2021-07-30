from pymongo import MongoClient
from pprint import pprint
from decouple import config

URL_CONN=config('DB_STRING_CONN', default=None)

client = MongoClient(URL_CONN)
db = client.admin
serverStatusResult = db.command("serverStatus")
pprint(serverStatusResult)
