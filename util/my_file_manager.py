import json
# import datetime


def alert(text):
    print('\033[31m', end='')
    print('#'*80)
    print(text.upper().center(80))
    print('#'*80)
    print('\033[m', end='')

def file_exists(filename):
    filename = filename.upper()
    try:
        file = open(filename, 'rt')
        file.close()
    except FileNotFoundError:
        return False
    else:
        return True

def create_file(filename):
    filename = filename.upper()
    try:
        file = open(filename, 'wt+')
        file.close()
    except:
        alert("ERRO CRIANDO O ARQUIVO DE DB")
        return False
    else:
        print(f'\033[32mARQUIVO {filename} CRIADO COM SUCESSO!\033[m')
        return True


def read_file(filename):
    filename = filename.upper()
    try:
        file = open(filename, 'rt')
    except:
        alert(f"ERRO AO LER O ARQUIVO {filename}!")
        return False
    else:
        text = file.read()
        file.close()
        return text


def write_in_file(filename, text):
    filename = filename.upper()
    try:
        # file = open(filename, 'wt+')
        file = open(filename, 'a')
        file.write(text+str('\n'))
        file.close()
    except:
        return False
    else:
        return True
    
def append_in_file(filename, text):
    filename = filename.upper()
    try:
        file = open(filename, 'a')
        file.write(text)
        file.write('\n')
        file.close()
    except:
        return False
    else:
        return True


def json_model(filename):
    filename = filename.upper()
    if not file_exists(filename):
        if create_file(filename)==True :
            user_admin= [{"id": 999,"name" : "ADMIN","type":"ADMIN","function":"ADMIN"}]
            json_object = json.dumps(user_admin, indent = 6) 
            with open(filename, "w") as outfile:
                outfile.write(json_object)
                print('FICHEIRO JSON CRIADO'.center(42))   
    else: 
        print('\033[31mO FICHEIRO JSON JA EXISTE\033[m'.center(42))


#print(read_file('erivelto.txt'))
# print(write_in_file('erivelto.txt', f'1*Erivelto*{datetime.datetime.now()}'))
# print(write_in_file('bank.json', f'{}'))
# print(append_in_file('erivelto.txt', f'2*Clenio*{datetime.datetime.now()}'))
# print(append_in_file('erivelto.txt', f'3*Costa*{datetime.datetime.now()}'))
# print(write_in_file('erivelto.txt', f'1*Erivelto*{datetime.datetime.now()}'))

# print('Running...')
# print(datetime.date.today())
# print(datetime.datetime.now())
# print(datetime.datetime.today())

# if not file_exists('erivelto.json'):
#     if create_file('erivelto.json')==True :
#         print('FICHEIRO CRIADO'.center(42))   
# else: 
#     print('\033[31mO FICHEIRO JA EXISTE\033[m'.center(42))   
