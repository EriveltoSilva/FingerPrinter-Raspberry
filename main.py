import os
import getpass
import RPi.GPIO as GPIO

from time import sleep

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

import util
from util import my_file_manager
from dao.UserDAO import UserDAO
from dao.ReportDAO import ReportDAO

from components.LED import LED
from components.Buzzer import Buzzer
from components.Biometric import Biometric
from components.Keyboard import Keyboard
from components.SpreadSheetGenerator import SpreadSheetGenerator




#---------- OLED Initialization ---------------
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

USER_FILENAME = 'db/users.json'
MY_LED = 17
MY_BUZZER = 27

MENU_RESET = -1
MENU_ADMIN = 0
MENU_REGISTER = 1
MENU_LIST_USERS = 2
MENU_DELETE = 3
MENU_FINGER = 4
MENU_SPREAD_SHEET = 5
MENU_LOGOUT = 6
MENU_TURN_OFF = 7 
menu_options=[MENU_REGISTER, MENU_LIST_USERS, MENU_DELETE, MENU_FINGER, MENU_SPREAD_SHEET,MENU_LOGOUT, MENU_TURN_OFF]

DELAY=2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = LED(MY_LED, False)
buzzer = Buzzer(MY_BUZZER, False)
keyboard = Keyboard([5,6,13,19],[26,16,20], False)
finger = Biometric(buzzer=buzzer, canvas=canvas, device=device)

def get_num_mec():
    global buzzer
    global keyboard
    global canvas
    global device
    digit = ''
    num=''
    
    while len(num)<3 or digit!='#':
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((0,0), '#####################', fill="blue")
            draw.text((0,10),'#       NUMERO      #', fill="blue")
            draw.text((0,20),'#    MECANOGRAFICO  #', fill="blue")
            draw.text((0,30),'#NOTA: 3 DIGITOS    #', fill="blue")
            draw.text((0,40),f'#DIGITE O NUMERO:{num}  ', fill="blue")
            draw.text((0,50),'#####################', fill="blue")
        buzzer.bip()
        digit = keyboard.wait_key_pressed()
        if(digit.isnumeric()):
            num +=digit 
        elif digit=='*':
            num = ''        
    return num
    
util.header('SISTEMA DE PONTEIRO BIOMETRICO')
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((0,20), '#     PONTEIRO      #', fill="blue")
    draw.text((0,30), '#    BIOMETRICO     #', fill="blue")
    draw.text((0,40), '#   TECMICRO LDA    #', fill="blue")


user_dao = UserDAO(USER_FILENAME)
report_dao = ReportDAO()
sleep(3)

     
try:
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((0,30),'#  SOLTE O BOTÃO    #', fill="blue")
    if keyboard.key_pressed()=='1':
        with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0),'#####################', fill="blue")
        buzzer.bip()
                
        if keyboard.wait_key_pressed() == '8':
            with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'#####################', fill="blue")
            buzzer.bip()
                
            if keyboard.wait_key_pressed() == '0':
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'#####################', fill="blue")
                    draw.text((0,20),'#####################', fill="blue")
                buzzer.bip()
                if keyboard.wait_key_pressed() == '3':
                    option = MENU_RESET
                else:
                    option= MENU_TURN_OFF
            else:
                option= MENU_TURN_OFF
        else:
            option= MENU_TURN_OFF
    
    elif finger.get_number_finger_registered() == 0:
        option = MENU_ADMIN
    else:
        option = MENU_FINGER
        
    while True:
        if(option==MENU_RESET):
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((0,0), '#####################', fill="blue")
                draw.text((0,10),'#   REINICIANDO...  #', fill="blue")
                draw.text((0,20),'#                   #', fill="blue")
                draw.text((0,30),'# APAGANDO OS DADOS #', fill="blue")
                draw.text((0,40),'#                   #', fill="blue")
                draw.text((0,50),'#####################', fill="blue")
            buzzer.alarm(1)
            if finger.delete_all()['status'] == 'success':
                my_file_manager.delete_json_model(USER_FILENAME)
            else:
                util.error('falha apagando os dados do usuario e reiniciando')
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'#  FALHA APAGANDO   #', fill="blue")
                    draw.text((0,20),'#     OS DADOS      #', fill="blue")
                    draw.text((0,30),'#   DOS USUARIOS    #', fill="blue")
                    draw.text((0,40),'#        ###        #', fill="blue")
                    draw.text((0,50),'#####################', fill="blue")
                buzzer.alarm(2)
            option = MENU_TURN_OFF
        
        
        elif(option==MENU_ADMIN):
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((0,0), '#####################', fill="blue")
                draw.text((0,10),'##### REGISTRO ######', fill="blue")
                draw.text((0,20),'#    DE USUARIO     #', fill="blue")
                draw.text((0,30),'#    ROOT ADMIN     #', fill="blue")
                draw.text((0,40),'#CLIQUE EM UMA TECLA#', fill="blue")
                draw.text((0,50),'#####################', fill="blue")
            buzzer.bip()
            keyboard.wait_key_pressed()
                
            response = finger.enroll_finger()
            if response['status'] == 'success':
                id = response['data']
                my_file_manager.json_model(USER_FILENAME, id)
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'##### REGISTRO ######', fill="blue")
                    draw.text((0,20),'#     ROOT ADMIN    #', fill="blue")
                    draw.text((0,30),'#   COM SUCCESSO!   #', fill="blue")
                    draw.text((0,40),'#CLIQUE EM UMA TECLA#', fill="blue")
                    draw.text((0,50),'#####################', fill="blue")
                buzzer.bip()
                keyboard.wait_key_pressed()
                option = MENU_FINGER
            else:
                util.error(response['message'])
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'#     REGISTRO      #', fill="blue")
                    draw.text((0,20),'#     ROOT ADMIN    #', fill="blue")
                    draw.text((0,30),'# ERRO NA OPERAÇÃO  #', fill="blue")
                    draw.text((0,40),'#                   #', fill="blue")
                    draw.text((0,50),'#####################', fill="blue")
                buzzer.alarm()
                sleep(DELAY)
                
        elif(option==MENU_REGISTER):
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
                sleep(DELAY)
                
                id = response['data']
                
                num_mec = get_num_mec()
                util.header(f'Retornou:{num_mec}')
                
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'##### REGISTRO ######', fill="blue")
                    draw.text((0,20),'DEVE SER ADMIN?      ', fill="blue")
                    draw.text((0,30),'  *-NÃO              ', fill="blue")
                    draw.text((0,40),'  #-SIM              ', fill="blue")
                    draw.text((0,50),'#####################', fill="blue")
                buzzer.bip()
                
                
                if(keyboard.wait_key_pressed().upper() == '#'):
                    type_user ='ADMIN'
                else:
                    type_user = 'FUNCIONARIO'
                    
                user_dao.create({ "id":id, "num_mec":num_mec, "type":type_user.upper()})
                option = MENU_FINGER
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
            option = MENU_FINGER
        
        elif(option==MENU_LIST_USERS):
            with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'#                   #', fill="blue")
                    draw.text((0,20),'#     OPCAO         #', fill="blue")
                    draw.text((0,30),'#   INDISPONIVEL    #', fill="blue")
                    draw.text((0,40),'#   NESTA VERSÃO    #', fill="blue")
                    draw.text((0,50),'#####################', fill="blue")
            buzzer.bip()
            sleep(DELAY)
            option = MENU_FINGER 
        
        elif(option==MENU_DELETE):
            num_mec = get_num_mec()
            print(num_mec)
            id = user_dao.get_id_by_num_mec(num_mec)
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
                    sleep(DELAY)
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
                    sleep(DELAY)
                    
                elif response['status'] =='success' and response['data'] == False:
                    util.change_color('green')
                    util.print_center('PESSOA NÃO DELECTADA!')
                    util.change_color()
                    with canvas(device) as draw:
                        draw.rectangle(device.bounding_box, outline="white", fill="black")
                        draw.text((0,0), '#####################', fill="blue")
                        draw.text((0,10),'#                   #', fill="blue")
                        draw.text((0,20),'#     DIGITAL       #', fill="blue")
                        draw.text((0,30),'#  NÃO ENCONTRADA   #', fill="blue")
                        draw.text((0,40),'#                   #', fill="blue")
                        draw.text((0,50),'#####################', fill="blue")
                    buzzer.bip()
                    sleep(DELAY)
                option = MENU_FINGER
        elif(option==MENU_FINGER):
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
                sleep(DELAY)
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
                    sleep(DELAY)
                elif response['status'] == 'success' and response['data']>=0:
                    user = user_dao.find(response['data'])
                    if user == None:
                        util.error('PESSOA(ID) NÃO ENCONTRADO NO DB ')
                    else:
                        report_dao.insert_register(user)
                        with canvas(device) as draw:
                            draw.rectangle(device.bounding_box, outline="white", fill="black")
                            draw.text((0,0), '#####################', fill="blue")
                            draw.text((0,10),'#     IMPRESSÃO     #', fill="blue")
                            draw.text((0,20),'#     DETECTADA     #', fill="blue")
                            draw.text((0,30),'#        OLA        #', fill="blue")
                            if(user['type']!='ADMIN'):
                                t =f"Nº{user['num_mec']}"
                                draw.text((0,40),f'{t:^21}', fill="blue")
                            else:    
                                draw.text((0,40),'#       ADMIN       #', fill="blue")
                            draw.text((0,50),'#####################', fill="blue")
                        buzzer.bip(0.8)
                        sleep(DELAY)
                        
                        if(user['type']=='ADMIN'):
                            with canvas(device) as draw:
                                draw.rectangle(device.bounding_box, outline="white", fill="black")
                                y=0
                                for text in [f'{menu_options[0]}-REGISTRAR PESSOA', f'{menu_options[1]}-LISTAR PESSOAS',f'{menu_options[2]}-DELETAR PESSOA', f'{menu_options[3]}-PICAR' ,f'{menu_options[4]}-RETIRAR FOLHA', f'{menu_options[5]}-SAIR', f'{menu_options[6]}-DESLIGAR']:
                                    draw.text((0,y), text, fill="white")
                                    y +=9
                                    
                            option= keyboard.wait_key_pressed()
                            if option.isnumeric():
                                option = int(option)
                                
                        
        elif option == MENU_SPREAD_SHEET:
            util.header('## Retirar Folha ##')
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((0,0), '#####################', fill="blue")
                draw.text((0,10),'#                   #', fill="blue")
                draw.text((0,20),'# RETIRO DE EXTRATO #', fill="blue")
                draw.text((0,30),'#       DO MES      #', fill="blue")
                draw.text((0,40),'#                   #', fill="blue")
                draw.text((0,50),'#####################', fill="blue")
            buzzer.bip()
            sleep(DELAY)
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((0,0), '#####################', fill="blue")
                draw.text((0,10),'#                   #', fill="blue")
                draw.text((0,20),'#   ESCOLHA O MES   #', fill="blue")
                draw.text((0,30),'# QUE DESEJA TIRAR  #', fill="blue")
                draw.text((0,40),'#                   #', fill="blue")
                draw.text((0,50),'#####################', fill="blue")
            buzzer.bip()
            sleep(DELAY)
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white", fill="black")
                draw.text((0,0), '1-JANEIRO  2-FEVEREI', fill="blue")
                draw.text((0,10),'3-MARÇO    4-ABRIL', fill="blue")
                draw.text((0,20),'5-MAIO     6-JUNHO', fill="blue")
                draw.text((0,30),'7-JULHO    8-AGOSOTO', fill="blue")
                draw.text((0,40),'9-SETEM    0-OUTUBRO', fill="blue")
                draw.text((0,50),'*-NOVEM    #-DEZEMBR', fill="blue")
            months= ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '*', '#']
            key = keyboard.wait_key_pressed()
            resp = report_dao.read_register(months.index(key))
            if len(resp) <1:
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((0,0), '#####################', fill="blue")
                    draw.text((0,10),'#        UPS!       #', fill="blue")
                    draw.text((0,20),'#      NÃO TEM      #', fill="blue")
                    draw.text((0,30),'#REGISTROS GUARDADOS#', fill="blue")
                    draw.text((0,40),'#     DESTE MES     #', fill="blue")
                    draw.text((0,50),'#####################', fill="blue")
                buzzer.alarm()
            else:
                pendrive_path = my_file_manager.get_report_path()
                if pendrive_path!= None:
                    spread_sheet_generator = SpreadSheetGenerator()
                    if spread_sheet_generator.generate_spread_sheet(resp, pendrive_path) == True:
                        with canvas(device) as draw:
                                draw.rectangle(device.bounding_box, outline="white", fill="black")
                                draw.text((0,0), '#####################', fill="blue")
                                draw.text((0,10),'#  EXTRATO MENSAL   #', fill="blue")
                                draw.text((0,20),'#     RETIRADO      #', fill="blue")
                                draw.text((0,30),'#       COM         #', fill="blue")
                                draw.text((0,40),'#     SUCCESSO!     #', fill="blue")
                                draw.text((0,50),'#####################', fill="blue")
                        buzzer.alarm(3)
                        with canvas(device) as draw:
                                draw.rectangle(device.bounding_box, outline="white", fill="black")
                                draw.text((0,0), '#####################', fill="blue")
                                draw.text((0,10),'# PRESSIONE QUALQUER#', fill="blue")
                                draw.text((0,20),'#    TECLA PARA     #', fill="blue")
                                draw.text((0,30),'#     CONTINUAR     #', fill="blue")
                                draw.text((0,40),'#        ###        #', fill="blue")
                                draw.text((0,50),'#####################', fill="blue")
                        keyboard.wait_key_pressed()
                    else:
                        with canvas(device) as draw:
                            draw.rectangle(device.bounding_box, outline="white", fill="black")
                            draw.text((0,0), '#####################', fill="blue")
                            draw.text((0,10),'# ERRO GRAVANDO NA  #', fill="blue")
                            draw.text((0,20),'#     PENDRIVE!     #', fill="blue")
                            draw.text((0,30),'#VERIFIQUE O ESPAÇO #', fill="blue")
                            draw.text((0,40),'#    E PERMISSÕES   #', fill="blue")
                            draw.text((0,50),'#####################', fill="blue")
                        buzzer.alarm(3)
                else:
                    with canvas(device) as draw:
                            draw.rectangle(device.bounding_box, outline="white", fill="black")
                            draw.text((0,0), '#####################', fill="blue")
                            draw.text((0,10),'#  ERRO LOCALIZANDO #', fill="blue")
                            draw.text((0,20),'#     A PENDRIVE    #', fill="blue")
                            draw.text((0,30),'# VERIFIQUE SE ESTÁ #', fill="blue")
                            draw.text((0,40),'#    BEM INSERIDA   #', fill="blue")
                            draw.text((0,50),'#####################', fill="blue")
                    buzzer.alarm(3)
            
            option = MENU_FINGER
        elif option == 6:
            option = MENU_FINGER
            
        elif option == MENU_TURN_OFF :
            break
except KeyboardInterrupt:
    print('\033[31m\nSystem Stopped!\033[m')
    GPIO.cleanup()


util.header('## Programa Encerrando... ##')
with canvas(device) as draw:
    draw.rectangle(device.bounding_box, outline="white", fill="black")
    draw.text((0,25), '#PROGRAMA ENCERRANDO#', fill="white")
sleep(DELAY)
GPIO.cleanup()
                        
