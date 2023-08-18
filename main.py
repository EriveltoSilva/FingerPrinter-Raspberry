from dao.UserDAO import UserDAO
from models.UserModel import UserModel

user_model = UserModel(3)
#user_model.read_user_datas()

user_dao = UserDAO()
user = user_dao.find(user_model.get_id())
if user:
    print(user)