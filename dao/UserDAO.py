import json
from models.UserModel import UserModel

class UserDAO:
    def __init__(self):
        self.filename = 'db/users.json'

    def create(self, user_model):
        user = [{"id":user_model.get_id(), "name":user_model.get_name(), "type":user_model.get_type(), "function":user_model.get_function()}]
        with open(self.filename) as users_temp:
            users_loaded = json.load(users_temp)
        users_updated = users_loaded + user

        with open(self.filename, 'w') as users_readed:
            json.dump(users_updated, users_readed, indent=6)

    def find(self, id):
        with open(self.filename) as usersTemp:
            users = json.load(usersTemp)
            for user in users:
                if id == user['id']:
                    return user
        return False

    def find_all(self):
        with open(self.filename) as usersTemp:
            users = json.load(usersTemp)
            print('*' * 42)
            i = 1
            for user in users:
                print(f'User [{i}]'.center(42))
                print(f'Id:{user["id"]}')
                print(f'Nome:{user["name"]}')
                print(f'Type:{user["type"]}')
                print(f'Function:{user["function"]}')
                i += 1
            print('*' * 42)


    def delete(self, id):
        with open(self.filename) as users_temp:
            users_loaded = json.load(users_temp)
            for user in users_loaded:
                if id == user['id']:
                    users_loaded.remove(user)
                    with open('db/users.json', 'w') as users_readed:
                        json.dump(users_loaded, users_readed, indent=6)
                        return True
        return False

    def is_admin(self, id):
        with open(self.filename) as usersTemp:
            users = json.load(usersTemp)
            for user in users:
                if id == user['id'] and user['type'] == 'ADMIN':
                    return True
        return False

    def is_user(self, id):
        with open(self.filename) as usersTemp:
            users = json.load(usersTemp)
            for user in users:
                if id == user['id']:
                    return True
        return False