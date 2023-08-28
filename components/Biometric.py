from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

from time import sleep

from components import Buzzer
import util

SMALL_TIME = 1
MIDDLE_TIME = 2

class Biometric:
    
    def __init__(self, buzzer, canvas, device):
        self.buzzer = buzzer
        self.canvas = canvas
        self.device = device
        
        try:
            self.f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)
            if ( self.f.verifyPassword() == False ):
                with self.canvas(self.device) as draw:
                    draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                    draw.text((0,10), '#####################', fill="blue")
                    draw.text((0,20), '#       ERRO        #', fill="blue")
                    draw.text((0,30), '#   INICIALIZANDO   #', fill="blue")
                    draw.text((0,40), '#     O SENSOR      #', fill="blue")
                    draw.text((0,50), '#CHECK AS LIGAÇÕES  #', fill="blue")
                                
        except Exception as e:
            print('Falha na Inicialização do Sensor FingerPrint!')
            print('Falha: ' + str(e))
            with self.canvas(self.device) as draw:
                draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                draw.text((0,10), '#####################', fill="blue")
                draw.text((0,20), '#       ERRO        #', fill="blue")
                draw.text((0,30), '#   INICIALIZANDO   #', fill="blue")
                draw.text((0,40), '#     O SENSOR      #', fill="blue")
                draw.text((0,50), '#CHECK AS LIGAÇÕES  #', fill="blue")
                        

    def get_number_finger_registered(self):
        return self.f.getTemplateCount()

    def get_total_finger_capacity(self):
        return self.f.getStorageCapacity()

    
    def enroll_finger(self):
        util.change_color('blue')
        util.header("## Registo de uma Nova Pessoa ##")
        
        util.change_color()
        with self.canvas(self.device) as draw:
                draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                draw.text((0,10), '#####################', fill="blue")
                draw.text((0,20), '# OPCAO 1 ESCOLHIDA #', fill="blue")
                draw.text((0,30), '# REGISTRO DE NOVA  #', fill="blue")
                draw.text((0,40), '#      PESSOA       #', fill="blue")
                draw.text((0,50), '#####################', fill="blue")
        self.buzzer.bip()
        sleep(1.2)
        try:
            util.print_center('## Insira o Dedo no Sensor... ##')
            with self.canvas(self.device) as draw:
                draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                draw.text((0,10), '#####################', fill="blue")
                draw.text((0,20), '#   REGISTRANDO     #', fill="blue")
                draw.text((0,30), '# INSIRA O DEDO NO  #', fill="blue")
                draw.text((0,40), '#      SENSOR       #', fill="blue")
                draw.text((0,50), '#####################', fill="blue")
            self.buzzer.bip()
            while ( self.f.readImage() == False ):
                pass
            self.f.convertImage(FINGERPRINT_CHARBUFFER1)
            result = self.f.searchTemplate()
            positionNumber = result[0]
            accuracyScore = result[1]
            if ( positionNumber >= 0 ):
                error_text = ('## Está Pessoa já se encontra Registrada, com o ID:{0}'.format(positionNumber))
                print(error_text)
                with self.canvas(self.device) as draw:
                    draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'#      REGISTRO     #', fill="blue")
                    draw.text((0,20),'#    ESTA PESSOA    #', fill="blue")
                    draw.text((0,40),'#  JA SE ENCONTRA   #', fill="blue")
                    draw.text((0,30),'#     REGISTRADA    #', fill="blue")
                    draw.text((0,50),'#####################', fill="blue")
                self.buzzer.alarm()
                return {"status":"error", "message":error_text, "data":-1}
        
            print('## Retire o Dedo... ##')
            with self.canvas(self.device) as draw:
                draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                draw.text((0,0), '#####################', fill="blue")
                draw.text((0,10),'#                   #', fill="blue")
                draw.text((0,20),'#     REGISTRO      #', fill="blue")
                draw.text((0,30),'#   RETIRE O DEDO   #', fill="blue")
                draw.text((0,40),'#       ###         #', fill="blue")
                draw.text((0,50),'#####################', fill="blue")
            self.buzzer.alarm()
            print('## Insira o Mesmo Dedo no Sensor... ##')
            with self.canvas(self.device) as draw:
                draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                draw.text((0,0), '#####################', fill="blue")
                draw.text((0,10),'#     REGISTRO      #', fill="blue")
                draw.text((0,20),'#  INSIRA O MESMO   #', fill="blue")
                draw.text((0,30),'#       DEDO        #', fill="blue")
                draw.text((0,40),'#    NO SENSOR      #', fill="blue")
                draw.text((0,50),'#####################', fill="blue")
            
            self.buzzer.bip()
            while ( self.f.readImage() == False):
                pass
            self.f.convertImage(FINGERPRINT_CHARBUFFER2)
            #self.f.convertImage(0x02)
            if(self.f.compareCharacteristics() == 0 ):
                error_text = '## Os Dedos não Concidem..\n## Verifique se colocou o mesmo dedo, ou se posicionou da mesma maneira ##'
                util.error(error_text)
                with self.canvas(self.device) as draw:
                    draw.rectangle(self.device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'#     REGISTRO      #', fill="blue")
                    draw.text((0,20),'#   ERRO LENDO AS   #', fill="blue")
                    draw.text((0,30),'#  DIGITAIS DO DEDO #', fill="blue")
                    draw.text((0,40),'#   TENTE DE NOVO   #', fill="blue")
                    draw.text((0,50),'#####################', fill="blue")
                    
                self.buzzer.alarm()
                return {"status":"error", "message":error_text, "data":-1}
            
            self.f.createTemplate()
            positionNumber = self.f.storeTemplate()
            util.change_color('green')
            print('## Pessoa Registrada com Sucesso! ##')
            print('## ID:'+str(positionNumber))
            util.change_color()
            return {"status":"success", "message":"success", "data": positionNumber}
        
    
        except Exception as e:
            error_text = ('Erro na Operação.\nErro:'+ str(e))
            util.error(error_text)
            # exit(1)
            return {"status":"error", "message":error_text, "data":-1}



    def delete_finger(self, id):
        try:
            positionNumber = id
            if(self.f.deleteTemplate(positionNumber) == True):
                return {"status":"success", "message":"success", "data":True}
            else:
                util.error('Pessoa Não Encontrada')
                return {"status":"success", "message":"Digital Não Encontrada", "data":False}        
        except Exception as e:
            error_text = f'Falha Delectando Usuario.\nFalha:{e}' 
            return {"status":"error", "message":error_text, "data":False}
            
    def delete_all(self):
        try:
            capacity = self.f.getStorageCapacity()
            for id in range(capacity):               
                self.f.deleteTemplate(id)
            return {"status":"success", "message":"success", "data":True}
                    
        except Exception as e:
            error_text = f'Falha Delectando Todos os Usuarios.\nFalha:{e}' 
            return {"status":"error", "message":error_text, "data":False}
        



    def find_finger(self):
        try:
            print('## Esperando alguem inserir um dedo no sensor... ##')
            while self.f.readImage() == False :
                pass
            self.f.convertImage(FINGERPRINT_CHARBUFFER1)
            result = self.f.searchTemplate()
            positionNumber = result[0]
            accurancyScore = result[1]
            if positionNumber == -1 :
                error_text = '## Ups! Pessoa não encontrada ##\n## Tente posicionar melhor o dedo ##'
                print(error_text)
                return {"status":"success", "message":error_text, "data":-1}
            else:
                print(f'## Pessoa Encontrada ##\n# ID:{positionNumber}')
                return {"status":"success", "message":"Pessoa Não Encontrada", "data":positionNumber}
        except Exception as e:
            error_text = (f'Erro na Operação.\nErro{e}')
            print(error_text)
            return {"status":"error", "message":error_text, "data":-1}

        
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
