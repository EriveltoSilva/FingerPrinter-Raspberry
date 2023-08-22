import RPi.GPIO as GPIO
from time import sleep

import util
from util import my_file_manager

from dao.UserDAO import UserDAO
from dao.ReportDAO import ReportDAO

from components.LED import LED
from components.Buzzer import Buzzer
from components.Biometric import Biometric
from components.Keyboard import Keyboard

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

#---------- OLED Initialization ---------------
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

USER_FILENAME = 'db/users.json'
MY_LED = 17
MY_BUZZER = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = LED(MY_LED, False)
buzzer = Buzzer(MY_BUZZER, False)
keyboard = Keyboard([5,6,13,19],[26,16,20], False)
finger = Biometric(buzzer=buzzer, canvas=canvas, device=device)

util.header('SISTEMA DE PONTEIRO BIOMETRICO')
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((0,20), '#     PONTEIRO      #', fill="blue")
    draw.text((0,30), '#    BIOMETRICO     #', fill="blue")
    draw.text((0,40), '#   TECMICRO LDA    #', fill="blue")
            
            
my_file_manager.json_model(USER_FILENAME)
user_dao = UserDAO(USER_FILENAME)
sleep(3)

try:
    while True:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            y=5
            for text in ['1-Registrar Pessoa', '2-Deletar Pessoa', '3-Picar' ,'4-Sair', '', '']:
                draw.text((5,y), text, fill="white")
                y +=15
                
        option= keyboard.key_wait_pressed()
        if option.isnumeric():
            option = int(option)
            
        #option = util.menu(['Registrar Pessoa','Deletar Pessoa', 'Picar','Sair'])
        if option!='':
            print(f'\033[36m-------------Pressionada a Tecla:{option}------------------------')
        
        if(option==1):
            response = finger.enroll_finger()
            if response['status'] == 'success':
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'##### REGISTRO ######', fill="blue")
                    draw.text((0,20),'#     DIGITAIS      #', fill="blue")
                    draw.text((0,30),'#    REGISTRADAS    #', fill="blue")
                    draw.text((0,40),'#   COM SUCCESSO!   #', fill="blue")
                    draw.text((0,50),'#####################', fill="blue")
                buzzer.alarm()
                sleep(3)
                
                id = response['data']
                name = input('Digite o Nome da Pessoa:')
                if(input('ESTE USUARIO DEVE SER ADMIN?[S/N]:').upper() == 'S'):
                    type_user ='ADMIN'
                else:
                    type_user = 'FUNCIONARIO'
                    
                function = input('Digite a sua Função na Empresa:')
                user_dao.create({ "id":id, "name":name.upper(), "type":type_user.upper(), "function":function.upper()})
            else:
                util.error(response['message'])
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'#                   #', fill="blue")
                    draw.text((0,20),'#     REGISTRO      #', fill="blue")
                    draw.text((0,30),'# ERRO NA OPERAÇÃO  #', fill="blue")
                    draw.text((0,40),'#                   #', fill="blue")
                    draw.text((0,50),'#####################', fill="blue")
                buzzer.alarm()
                sleep(3)

        elif(option==2):
            name = input("Digite o nome:")
            print(name)
            id = user_dao.get_id_by_name(name)
            print(f'ID:{id}')
            if id != -1: 
                response = finger.delete_finger(id)
                if response['status'] =='error':
                    util.error(response['message'])
                    with canvas(device) as draw:
                        draw.rectangle(device.bounding_box, outline="white", fill="black")
                        draw.text((0,0), '#####################', fill="blue")
                        draw.text((0,10),'#                   #', fill="blue")
                        draw.text((0,20),'#  ERRO NO FINGER   #', fill="blue")
                        draw.text((0,30),'#   LOCALIZANDO     #', fill="blue")
                        draw.text((0,40),'#    A DIGITAL      #', fill="blue")
                        draw.text((0,50),'#####################', fill="blue")
                    buzzer.bip()
                    sleep(3)
                elif response['status'] =='success' and response['data'] == True:
                    util.change_color('green')
                    util.print_center('PESSOA DELECTADA!')
                    util.change_color()
                    with canvas(device) as draw:
                        draw.rectangle(device.bounding_box, outline="white", fill="black")
                        draw.text((0,0), '#####################', fill="blue")
                        draw.text((0,10),'#     DIGITAL       #', fill="blue")
                        draw.text((0,20),'#    DELECTADA      #', fill="blue")
                        draw.text((0,30),'#                   #', fill="blue")
                        draw.text((0,40),'#   COM SUCCESSO!   #', fill="blue")
                        draw.text((0,50),'#####################', fill="blue")
                    if user_dao.delete(id) == False:
                        util.error('Erro Apagando usuario do arquivo Json')
                    else:
                        util.print_center('Usuario apagado do Json')
                    buzzer.bip()
                    sleep(3)
                elif response['status'] =='success' and response['data'] == False:
                    util.change_color('green')
                    util.print_center('PESSOA NÃO DELECTADA!')
                    util.change_color()
                    with canvas(self.device) as draw:
                        draw.rectangle(device.bounding_box, outline="white", fill="black")
                        draw.text((0,0), '#####################', fill="blue")
                        draw.text((0,10),'#                   #', fill="blue")
                        draw.text((0,20),'#     DIGITAL       #', fill="blue")
                        draw.text((0,30),'#  NÃO ENCONTRADA   #', fill="blue")
                        draw.text((0,40),'#                   #', fill="blue")
                        draw.text((0,50),'#####################', fill="blue")
                    buzzer.bip()
                    sleep(3)

        elif(option==3):
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((0,0), '#####################', fill="blue")
                draw.text((0,10),'#   INSIRA O SEU    #', fill="blue")
                draw.text((0,20),'#       DEDO        #', fill="blue")
                draw.text((0,30),'#                   #', fill="blue")
                draw.text((0,40),'#        ###        #', fill="blue")
                draw.text((0,50),'#####################', fill="blue")
            buzzer.bip()
            response = finger.find_finger()
            
            if response['status'] == 'error':
                util.error(response['message'])
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'#                   #', fill="blue")
                    draw.text((0,20),'#  ERRO NO FINGER   #', fill="blue")
                    draw.text((0,30),'#   LOCALIZANDO     #', fill="blue")
                    draw.text((0,40),'#    A DIGITAL      #', fill="blue")
                    draw.text((0,50),'#####################', fill="blue")
                buzzer.bip(0.8)
                sleep(3)
            else:
                if response['status']=='success' and response['data']==-1:
                    util.error('PESSOA NÃO DETECTADA!')
                    with canvas(device) as draw:
                        draw.rectangle(device.bounding_box, outline="white", fill="black")
                        draw.text((0,0), '#####################', fill="blue")
                        draw.text((0,10),'#   UPS! DIGITAIS   #', fill="blue")
                        draw.text((0,20),'#   NÃO ENCONTRADA  #', fill="blue")
                        draw.text((0,30),'#  TENTE NOVAMENTE  #', fill="blue")
                        draw.text((0,40),'#                   #', fill="blue")
                        draw.text((0,50),'#####################', fill="blue")
                    buzzer.bip(0.8)
                    sleep(3)
                elif response['status'] == 'success' and response['data']>=0:
                    user = user_dao.find(response['data'])
                    if user == None:
                        util.error('PESSOA(ID) NÃO ENCONTRADO NO DB ')
                    else:
                        report_dao = ReportDAO()
                        report_dao.insert_register(user)
                        with canvas(device) as draw:
                            draw.rectangle(device.bounding_box, outline="white", fill="black")
                            draw.text((0,0), '#####################', fill="blue")
                            draw.text((0,10),'#     IMPRESSÃO     #', fill="blue")
                            draw.text((0,20),'#     DETECTADA     #', fill="blue")
                            draw.text((0,30),'#        OLA        #', fill="blue")
                            draw.text((0,40),f"{user['name']:^21}", fill="blue")
                            draw.text((0,50),'#####################', fill="blue")
                        buzzer.bip(0.8)
                        sleep(3)
                        
        elif option == 4:
            util.header('## Programa Encerrando... ##')
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((0,25), '#PROGRAMA ENCERRANDO#', fill="white")
            sleep(2)
            GPIO.cleanup()
            break
            
except KeyboardInterrupt:
    print('\033[31m\nSystem Stopped!\033[m')
    GPIO.cleanup()

