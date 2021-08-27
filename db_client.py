import re
from typing import Dict
from bson.objectid import ObjectId
from pymongo import MongoClient

from decouple import config


MONGO_DB_URL = config('DB_STRING_CONN', default=None)

COMMAND_SOPTIONS = [
    ('Cadastro de restaurante', 'business-create', 'c'),
    ('Cadastro de review', 'business-feedback', 'bf'),
    ('Consultar reviews de restaurante', 'get-business-info', 'gbi'),
    ('Consultar restaurante', 'get-business', 'gb'),
    ('Encerrar execução do client', 'exit', '')
]
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


def get_business_by_info(client):
    db = client.business
    name = input("Informe o nome do restaurante: ")
    business = db.reviews.find_one({'name': name})
    business_id = business.get('_id')
    if business_id:
        business_feedback = get_feedback_by_business_id(
            client, business_id=business_id)
        return (business, business_feedback)
    else:
        return 'business not found'


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


def main_menu() -> None:
    print('{:40} | {:^20} | {:^9}'.format('', 'Commands', 'Options'))
    fmt = '{:40} | {:^20} | {:^9}'

    for description, command, option in COMMAND_SOPTIONS:
        print(fmt.format(description, command, option))

    print('\n')


def get_business_by_name(client):
    db = client.business
    name = input('Informe o nome do restaurante: ')
    name = re.compile(f'.*{name}.*', re.IGNORECASE)
    count_result = db.reviews.count_documents({'name': name})
    if count_result > 1:
        print(f'Foram encontrados {count_result}, resultados para pesquisa.')   
        choice = input('Deseja exibir todos?: [Y/N] \n')
        if choice.upper() == 'Y':
            result = db.reviews.find({'name': name})
            return result
        else:
            return None
    elif count_result == 1:
        result = db.reviews.find({'name': name})
        return result
    else:
        return None


def show_business_info(business: Dict) -> None:
    print(f'Nome do restaurante: {business.get("name")}')
    print(f'Nota do restaurante: {business.get("rating")}')
    print(f'Tipo do restaurante: {business.get("cuisine")}')
    print('\n')


def show_feedback_info(feedback: Dict) -> None:
    print(f'Comentário: {feedback.get("feedback_content")}, restaurante: {feedback.get("business_id")}')


def find_all(client):
    db_business = client.business
    db_feedback = client.feedback

    business_result = db_business.reviews.find({})
    feedback_result = db_feedback.reviews.find({})

    return business_result, feedback_result


def update_business(client):
    result = get_business_by_name(client)
    if result is not None:
        show_business_info(result[0])
        print('Informe o campo e o novo valor para o registro (separados por :).')
        new_field_value = input()
        new_field_value = new_field_value.split(':')
        business_id = result[0].get('_id')


        db = client.business
        updated = db.reviews.update_one({"_id": business_id}, {"$set":{new_field_value[0]:new_field_value[1]}})
        print (updated)


def delete_business(client):
    result = get_business_by_name(client)
    if result is not None:
        show_business_info(result[0])
        print('Deseja deletar o estabelecimento informado acima? [y/n]')
        choice = input().lower()
        if choice == 'y':
            business_id = result[0].get('_id')
            db = client.business
            deleted = db.reviews.delete_one({"_id": business_id})
            print(deleted)
        else:
            print('operação cancelada')
            return None



if __name__ == '__main__':
    client = MongoClient(MONGO_DB_URL)
    
    while(True):
        main_menu()
        command = input('comando: ')

        if command == 'exit':
            break
        
        if command == 'business-create' or command == 'c':
            create_business(client)
        elif command == 'business-feedback' or command == 'bf':
            create_feedback(client)
        elif command == 'get-business-info' or command == 'gbi':
            result = get_business_by_info(client)
            show_business_info(result[0])
            show_feedback_info(result[1])
        elif command == 'gb':
            result = get_business_by_name(client)
            if result is not None:
                for business in result:
                    show_business_info(business)
            else:
                print('Nenhum resultado para exibir.')
        elif command == 'all':
            results = find_all(client)
            for business in results[0]:
                show_business_info(business)
            for feedback in results[1]:
                show_feedback_info(feedback)
        elif command == 'update':
            update_business(client)
        elif command == 'delete':
            delete_business(client)
        else:
            print('Comando inválido')
