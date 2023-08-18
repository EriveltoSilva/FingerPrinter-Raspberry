import RPi.GPIO as GPIO
from time import sleep

import util
from util import my_file_manager

from dao.UserDAO import UserDAO
from dao.ReportDAO import ReportDAO

from components.LED import LED
from components.Buzzer import Buzzer
from components.Biometric import Biometric

USER_FILENAME = 'db/users.json'
MY_LED = 17
MY_BUZZER = 27

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = LED(MY_LED)
buzzer = Buzzer(MY_BUZZER)
finger = Biometric(buzzer)

util.header('Sistema de Ponteiro Biometrico')
my_file_manager.json_model(USER_FILENAME)
user_dao = UserDAO(USER_FILENAME)

while True:
    option = util.menu(['Registrar Pessoa','Deletar Pessoa', 'Picar','Sair'])
    
    if(option==1):
        response = finger.enroll_finger()
        if response.isnumeric() == True and response >=0:
            id = response
            name = input('Digite o Nome da Pessoa:')
            if(input('ESTE USUARIO DEVE SER ADMIN?[S/N]:').upper() == 'S'):
                type ='ADMIN'
            else:
                type = 'FUNCIONARIO'
            function = input('Digite a sua Função na Empresa:')
            user_dao.create({ "id":id, "name":name, "type":type, "function":function })
        else:
            util.error(response)

    elif(option==2):
        name = input("Digite o nome:")
        id = user_dao.get_id(name)
        if id != -1: 
            resp = finger.delete_finger(id)
            if type(resp) == str:
                util.error(resp)
            else:
                if resp == False :
                    util.error('Falha Delectando Usuario.\nFalha:'+str(e)) 
                else:
                    util.change_color('green')
                    util.print_center('PESSOA DELECTADA!')
                    util.change_color()

    elif(option==3):
        resp = finger.find_finger()
        if type(resp) == str :
            util.error(resp)
        else:
            if resp == -1 :
                util.error('PESSOA NÃO DETECTADA!')
            else:
                user = user_dao.find(resp)
                if user == None:
                    util.error('PESSOA NÃO ENCONTRA')
                else:
                   report_dao = ReportDAO()
                   report_dao.insert_register(user)
                    
    else:
        print('==== Encerrar Programa ====')
        GPIO.cleanup()
        break
util.header('## Programa Encerrado ##')
