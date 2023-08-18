class UserModel:
    def __init__(self):
        self.id = None
        self.name = None
        self.type = None
        self.function = None

    def __init__(self, id):
        self.id = id
        self.name = None
        self.type = None
        self.function = None

    def __int__(self, id, name, type="FUNCIONARIO", function="DESCONHECIDA"):
        self.id = id
        self.type = type.upper()
        self.name = name.upper()
        self.function = function.upper()

    def set_id(self, id):
        self.id = id

    def set_name(self, name):
        self.name = name

    def set_type(self, user_type):
        self.type = user_type

    def set_function(self, function):
        self.function = function

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_function(self):
        return self.function

    def read_user_datas(self):
        self.name = input('Digite o Nome da Pessoa:')
        self.type = input('Digite o tipo de Usuario[ADMIN/FUNCIONARIO]:')
        self.function = input('Digite a sua Função na Empresa:')

    def to_string(self):
        print('-'*42)
        print('DADOS DO USUARIO'.center(42).upper())
        print('-' * 42)
        print(f'ID:{self.id}')
        print(f'Nome:{self.name}')
        print(f'Type:{self.type}')
        print(f'Função:{self.function}')
        print('-' * 42, end='\n\n')