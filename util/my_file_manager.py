import os
import json
import getpass

def alert(text):
    print('\033[31m', end='')
    print('#'*80)
    print(text.upper().center(80))
    print('#'*80)
    print('\033[m', end='')

def file_exists(filename):
    try:
        file = open(filename, 'rt')
        file.close()
    except FileNotFoundError:
        return False
    else:
        return True

def create_file(filename):
    try:
        file = open(filename, 'wt+')
        file.close()
    except Exception as e:
        alert(f'ERRO CRIANDO O ARQUIVO DE DB{e}')
        return False
    else:
        print(f'\033[32mARQUIVO {filename} CRIADO COM SUCESSO!\033[m')
        return True


def read_file(filename):
    try:
        file = open(filename, 'rt')
    except Exception as e:
        alert(f'ERRO AO LER O ARQUIVO {filename}\nErro:{e}!')
        return False
    else:
        text = file.read()
        file.close()
        return text


def write_in_file(filename, text):
    try:
        # file = open(filename, 'wt+')
        file = open(filename, 'a')
        file.write(text+str('\n'))
        file.close()
    except Exception as e:
        alert(f'ERRO AO ESCREVER NO ARQUIVO {filename}\nErro:{e}')
        return False
    else:
        return True
    
def append_in_file(filename, text):
    try:
        file = open(filename, 'a')
        file.write(text)
        file.write('\n')
        file.close()
    except:
        return False
    else:
        return True


def json_model(filename, id):
    if not file_exists(filename):
        if create_file(filename)==True :
            user_admin= [{"id": id,"num_mec" : 999,"type":"ADMIN"}]
            json_object = json.dumps(user_admin, indent = 5) 
            with open(filename, "w") as outfile:
                outfile.write(json_object)
                print('FICHEIRO JSON CRIADO'.center(42))   
    else: 
        print('\033[31mO FICHEIRO JSON JA EXISTE\033[m'.center(42))


def delete_json_model(filename):
    if os.path.exists(filename):
        os.remove(filename)
    else:
        print('\033[31mFICHEIRO JSON NÃO ENCONTRADO! IMPOSSIVEL EMOVER\033[m'.center(42))


def get_sheet_data(filename):
    try:
        file = open(filename, 'rt')
    except Exception as e:
        alert(f'ERRO AO LER O ARQUIVO {filename}\nErro:{e}!')
        return []
    else:
        text = file.read()
        return text
  
def get_report_path():
    try:
        moint_point = f'/media/{getpass.getuser()}'
        pendrives = os.listdir(moint_point)
        if len(pendrives)>0:
            return f'{moint_point}/{pendrives[0]}/'
        return None
    except Exception as e:
        print(f'Erro:{e}')
    return None


