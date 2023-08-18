from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

from time import sleep

from components import Buzzer
import util

SMALL_TIME = 1
MIDDLE_TIME = 2

class Biometric:
    
    def __init__(self, buzzer):
        self.buzzer = buzzer
        try:
            self.f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
            if ( self.f.verifyPassword() == False ):
                raise ValueError('The given fingerprint sensor password is wrong!')

        except Exception as e:
            print('Falha na Inicialização do Sensor FingerPrint!')
            print('Falha: ' + str(e))
            exit(1)

    def get_number_finger_registered(self):
        return self.f.getTemplateCount()

    def get_total_finger_capacity(self):
        return self.f.getStorageCapacity()

    
    def enroll_finger(self):
        util.change_color('blue')
        util.header("## Registo de uma Nova Pessoa ##")
        self.buzzer.bip()
        util.change_color()
        
        ## Tries to search the finger and calculate hash
        try:
            util.print_center('## Insira o Dedo no Sensor... ##')
            self.buzzer.bip()

            while ( self.f.readImage() == False ):
                pass

            ## Converts read image to characteristics and stores it in charbuffer 1
            self.f.convertImage(FINGERPRINT_CHARBUFFER1)
            #self.f.convertImage(0x01)

            ## Searches template
            result = self.f.searchTemplate()

            positionNumber = result[0]
            accuracyScore = result[1]

            if ( positionNumber >= 0 ):
                print('## Está Pessoa já se encontra Registrada, com o ID:{0}'.format(positionNumber))
                self.buzzer.alarm()
                return
    
            print('## Retire o Dedo... ##')
            self.buzzer.bip()
            sleep(MIDDLE_TIME)
            print('## Insira o Mesmo Dedo no Sensor... ##')
            self.buzzer.bip()
            while ( self.f.readImage() == False):
                pass
            self.f.convertImage(FINGERPRINT_CHARBUFFER2)
            #self.f.convertImage(0x02)
            if(self.f.compareCharacteristics() == 0 ):
                util.error('## Os Dedos não Concidem..\n## Verifique se colocou o mesmo dedo, ou se posicionou da mesma maneira ##')
                self.buzzer.alarm()
                sleep(MIDDLE_TIME)
                return
            
            self.f.createTemplate()
            positionNumber = f.storeTemplate()
            util.change_color('green')
            print('## Pessoa Registrada com Sucesso! ##')
            print('## ID:'+str(positionNumber))
            util.change_color()
            self.buzzer.alarm()
            sleep(MIDDLE_TIME)
    
        except Exception as e:
            util.error('Erro na Operação.\nErro:'+ str(e))
            exit(1)
    
    
    def find_finger(self):
        try:
            print('## Esperando alguem inserir um dedo no sensor... ##')
            self.buzzer.bip()
            while ( self.f.readImage() == False ):
                pass
            
            #self.f.convertImage(0x01)
            self.f.convertImage(FINGERPRINT_CHARBUFFER1)
            
            result = f.searchTemplate()
            positionNumber = result[0]
            accurancyScore = result[1]
            
            if ( positionNumber == -1 ):
                print('## Ups! Pessoa não Encontrada! ##')
                print('## Tente posicionar melhor o dedo ##')
                self.buzzer.alarm()
                sleep(MIDDLE_TIME)
                return
            else:
                print('## Pessoa Encontrada ##')
                print('## ID:'+ str(positionNumber))
                self.buzzer.alarm()
        
        except Exception as e:
            print('Erro na Operação.\nErro:'+ str(e))
            exit(1)


    def delete_finger(self):
        try:
            positionNumber = int(input('Insira o ID da pessoa a remover:'))
            if(self.f.deleteTemplate(positionNumber) == True):
                util.change_color('green')
                util.header('Pessoa Delectada com Sucesso!')
                util.change_color()
        except Exception as e:
            util.error('Falha Delectando Usuario.\nFalha:'+str(e))
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