from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

from time import sleep

class Biometrico:
    
    def __init__(self):
        #-------------------- Tries to initialize the sensor ----------------
        try:
            self.f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
            if ( self.f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('Falha na Inicialização do Sensor FingerPrint!')
            print('Falha: ' + str(e))
            exit(1)

    def get_number_finger_registed(self):
        return self.f.getTemplateCount()

    def get_total_finger_capacity(self):
        return self.f.getStorageCapacity()

    
def enroll_finger(self):
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
