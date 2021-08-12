from bson.objectid import ObjectId
from pymongo import MongoClient

from decouple import config


MONGO_DB_URL = config('DB_STRING_CONN', default=None)


def create_business(client):
    name = input('Informe o nome: ')
    rating = input('Informe a nota: ')
    cuisine = input('Informe o tipo da comida: ')

    business = {
        'name': name,
        'rating': rating,
        'cuisine': cuisine
    }
    db = client.business
    result = db.reviews.insert_one(business)

    return result.inserted_id


def get_business_by_rating(client):
    db = client.business
    rating = int(input("Informe uma nota para consultar de 1 a 5: "))
    business = db.reviews.find_one({'rating': rating})
    business_feedback = get_feedback_by_business_id(
        client, business_id=business._id)
    return (rating, business_feedback)


def create_feedback(client, business_id=None) -> None:
    if not business_id:
        business_id = create_business(client)

    feedback_content = input('Comentário: ')
    feedback = {
        'business_id': business_id,
        'feedback_content': feedback_content
    }
    db = client.feedback
    result = db.reviews.insert_one(feedback)
    print(f'Feedback ID {result.inserted_id}')


def get_feedback_by_business_id(client, business_id):
    db = client.feedback
    result = db.reviews.find_one({'business_id': ObjectId(business_id)})

    return result


def get_feedback_by_id(client, feedbackid):
    db = client.feedback
    result = db.reviews.find_one({'_id': ObjectId(feedbackid)})

    return result


def get_business_by_id(client, business_id):
    db = client.business
    result = db.reviews.find_one({'_id': ObjectId(business_id)})
    return result


def get_business_by_feedback(client):
    pass


if __name__ == '__main__':
    client = MongoClient(MONGO_DB_URL)
    # print(create_business(client))
    # print(get_business_by_rating(client))

    # 5create_feedback(client)

    # print(get_feedback_by_id(client, '61148c19809e2c669f6b34e3'))

    # print(get_business_by_rating(client))

    # result = create_business(client)
    # print(result)

    # create_feedback(client, result)
    # print(get_business_by_id(client, '611494bfb058734eb7678610'))
    print(get_feedback_by_business_id(client, '611494bfb058734eb7678610'))