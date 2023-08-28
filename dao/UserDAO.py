import json

class UserDAO:
    def __init__(self, filename='db/users.json'):
        self.filename = filename
        # self.filename = 'db/users.json'
        
    def create(self, user_model):
        user = [user_model]
        with open(self.filename) as users_temp:
            users_loaded = json.load(users_temp)
        users_updated = users_loaded + user

        with open(self.filename, 'w') as users_readed:
            json.dump(users_updated, users_readed, indent=6)
    
    def delete(self, id):
        with open(self.filename) as users_temp:
            users_loaded = json.load(users_temp)
            for user in users_loaded:
                if id == user['id'] and id!=999:
                    users_loaded.remove(user)
                    with open(self.filename, 'w') as users_readed:
                        json.dump(users_loaded, users_readed, indent=6)
                        return True
        return False
    
    def find(self, id):
        with open(self.filename) as usersTemp:
            users = json.load(usersTemp)
            for user in users:
                if id == user['id']:
                    return user
        return None
    

    def to_string(self, id):
        with open(self.filename) as usersTemp:
            users = json.load(usersTemp)
            for user in users:
                if id == user['id']:
                    text = f'Id:{user["id"]}'.center(42)
                    text += f'Num Mec:{user["num_mec"]}'
                    text += f'Type:{user["type"]}'
                    return text
        return None


    def find_all(self):
        with open(self.filename) as usersTemp:
            users = json.load(usersTemp)
            print('*' * 42)
            i = 1
            for user in users:
                print(f'User [{i}]'.center(42))
                print(f'Id:{user["id"]}')
                print(f'Num Mec:{user["num_mec"]}')
                print(f'Type:{user["type"]}')
                i += 1
            print('*' * 42)


    

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
    
    def get_id_by_num_mec(self, num_mec):
        num_mec = num_mec.upper()
        print('Entrou na procura...')
        with open(self.filename) as usersTemp:
            users = json.load(usersTemp)
            for user in users:
                print(f"{user['num_mec']}")
                if num_mec == user['num_mec']:
                    return user['id']
        return -1
