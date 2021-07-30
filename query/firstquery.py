from pymongo import MongoClient
from decouple import config


MONGO_DB_URL=config('DB_STRING_CONN', default=None)

if __name__ == '__main__':
    client = MongoClient(MONGO_DB_URL)
    db = client.business
    fivestar = db.reviews.find_one({'rating': 5})
    print(fivestar)