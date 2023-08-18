def change_color(txt='WHITE'):
    txt = txt.upper()
    if(txt == 'WHITE'):
        print('\033[m', end='')
    elif(txt == 'RED'):
        print('\033[31m', end='')
    elif(txt == 'GREEN'):
        print('\033[32m', end='')
    elif(txt == 'BLUE'):
        print('\033[36m', end='')
    
def line(tam = 42):
    return '-' * tam

def print_center(txt=''):
    print(txt.center(42))

def header(txt):
    print(line())
    print(txt.center(42).upper())
    print(line())

def error(txt):
    change_color('red')
    print(line())
    print(txt.center(42).upper())
    print(line())
    change_color()

def menu(itens=[]):
    while True:
        header('MENU')
        line()
        i=1
        for item in itens:
            print('\033[33m{0}\033[m -\033[35m{1}\033[m'.format(i, item))
            i += 1 
        line()
        change_color('green')
        option = input('R:')
        change_color()
        if(option.isnumeric() == True):
            return int(option)
        else:
            change_color('red')
            error('ERRO A RESPOSTA DEVE SER UM NÚMERO')
            change_color()
                    

