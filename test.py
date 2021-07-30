import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://admin:LKjHXncRXZKA6zPM@clustermongdb.vgusz.mongodb.net/BDII?retryWrites=true&w=majority")
db = client.test
