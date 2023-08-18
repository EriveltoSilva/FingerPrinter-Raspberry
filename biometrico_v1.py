# Libraries Imports
#import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

#Import Time, and set up the GPIO, stop warnings, and activate the LED GPIO as an output (defaults to LOW Voltage) 
import time
import RPi.GPIO as GPIO


#LED is attached to the GPIO numbered below
LED1 = 17
BUZZER = 27

SMALL_TIME = 1
MIDDLE_TIME = 2
LONG_TIME = 15

#------------------------ GPIO Configuration ------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

GPIO.output(LED1, GPIO.HIGH)
GPIO.output(BUZZER, GPIO.LOW)

#-------------------- Tries to initialize the sensor ----------------
try:
    f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
    if ( f.verifyPassword() == False ):
        raise ValueError('The given fingerprint sensor password is wrong!')

except Exception as e:
    print('Falha na Inicialização do Sensor FingerPrint!')
    print('Falha: ' + str(e))
    exit(1)


## Gets some sensor information
#print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))


#---------------Functions Declarations and Definitions-----------
def get_number_finger_registered():
    return f.getTemplateCount()

def get_total_finger_capacity():
    return f.getStorageCapacity()

def bip():
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(0.3)
    GPIO.output(BUZZER, GPIO.LOW)
    
def alarm():
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(BUZZER, GPIO.LOW)


def enroll_finger():
    change_color('blue')
    header("## Registo de uma Nova Pessoa ##")
    bip()
    change_color()
    
    ## Tries to search the finger and calculate hash
    try:
        show('## Insira o Dedo no Sensor... ##')
        bip()
        ## Wait that finger is read
        while ( f.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(FINGERPRINT_CHARBUFFER1)
        #f.convertImage(0x01)

        ## Searchs template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if ( positionNumber >= 0 ):
            print('## Está Pessoa já se encontra Registrada, com o ID:{0}'.format(positionNumber))
            alarm()
            return
    
        print('## Retire o Dedo... ##')
        bip()
        time.sleep(MIDDLE_TIME)
        print('## Insira o Mesmo Dedo no Sensor... ##')
        bip()
        while ( f.readImage() == False):
            pass
        f.convertImage(FINGERPRINT_CHARBUFFER2)
        #f.convertImage(0x02)
        if(f.compareCharacteristics() == 0 ):
            error('## Os Dedos não Concidem..\n## Verifique se colocou o mesmo dedo, ou se posicionou da mesma maneira ##')
            alarm()
            time.sleep(MIDDLE_TIME)
            return
        
        f.createTemplate()
        positionNumber = f.storeTemplate()
        change_color('green')
        print('## Pessoa Registrada com Sucesso! ##')
        print('## ID:'+str(positionNumber))
        change_color()
        alarm()
        time.sleep(MIDDLE_TIME)
    
    except Exception as e:
        error('Erro na Operação.\nErro:'+ str(e))
        exit(1)


def find_finger():
    try:
        print('## Esperando alguem inserir um dedo no sensor... ##')
        bip()
        while ( f.readImage() == False ):
            pass
        
        
        #f.convertImage(0x01)
        f.convertImage(FINGERPRINT_CHARBUFFER1)
        
        result = f.searchTemplate()
        positionNumber = result[0]
        accurancyScore = result[1]
        
        if ( positionNumber == -1 ):
            print('## Ups! Pessoa não Encontrada! ##')
            print('## Tente posicionar melhor o dedo ##')
            alarm()
            time.sleep(MIDDLE_TIME)
            return
        else:
            print('## Pessoa Encontrada ##')
            print('## ID:'+ str(positionNumber))
            alarm()
    
    except Exception as e:
        print('Erro na Operação.\nErro:'+ str(e))
        exit(1)

def delete_finger():
    try:
        positionNumber = int(input('Insira o ID da pessoa a remover:'))
        if(f.deleteTemplate(positionNumber) == True):
            change_color('green')
            header('Pessoa Delectada com Sucesso!')
            change_color()
    except Exception as e:
        error('Falha Delectando Usuario.\nFalha:'+str(e))
        exit(1)
    '''
    positionNumber = 0
    count = 0
    print('## Apagar Pessoa ##')
    print('ID:'+str(count))
    #while GPIO.input(BTN_DELETE) == True:
        #if( GPIO.input(BTN_INC) == False:
    while (GPIO.input(BTN_OK) == True):
        if( GPIO.input(BTN_INC) == False):
            count = count +1
            if count > 1000:
                count = 1000
            print('## Nº: '+str(count))
        elif GPIO.input(BTN_DEC) == False:
            count = count -1
            if( count < 0):
                count = 0
            print('## Nº:'+str(count))
            bip()
            time.sleep(2)
    positionNumber = count
    if f.deleteTemplate(positionNumber) == True:
        print('## Pessoa Delectada ##')
        alarm()
        time.sleep(SMALL_TIME)
'''

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

def show(txt=''):
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
                    
def begin():
    header('Sistema de Ponteiro Biometrico')
    while True:
        option = menu(['Registrar Pessoa','Deletar Pessoa', 'Picar','Sair'])
        if(option==1):
            enroll_finger()
        elif(option==2):
            delete_finger()
        elif(option==3):
            find_finger()
        else:
            print('==== Encerrar Programa ====')
            GPIO.cleanup()
            break
    header('## Programa Encerrado ##')

begin()