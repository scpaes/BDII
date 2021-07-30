import pymongo


client = pymongo.MongoClient(
    "mongodb+srv://admin:LKjHXncRXZKA6zPM@clustermongdb.vgusz.mongodb.net/ClusterMongDB?retryWrites=true&w=majority")
db = client.admin
