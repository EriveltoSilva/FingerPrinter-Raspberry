import datetime
import util
from util import my_file_manager


class ReportDAO:

    def __init__(self):
        months_of_year = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO',
                          'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']
        
        self.REPORT_NAME = f'db/reports/RELATORIO-DE-{months_of_year[datetime.date.today().month-1]}-{datetime.date.today().year}.txt'
    
    def insert_register(self, user):
        days_of_week =['SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO', 'DOMINGO']
        day = datetime.date.today().day
        month = datetime.date.today().month
        year = datetime.date.today().year
        time = datetime.datetime.now().time() 
        dow = days_of_week[datetime.date.today().weekday()]
        #ID | Numero Mecano.. | Type | DIA_SEMANA | DIA | MES | ANO | HORARIO
        text = f'{user["id"]}*{user["num_mec"]}*{user["type"]}*{dow}*{day}*{month}*{year}*{time}'
        if my_file_manager.append_in_file(self.REPORT_NAME, text) == True:
            util.change_color('green')
            util.print_center('REGISTRO INSERIDO!')
            util.change_color()       
    
    def read_register(self, month, year=datetime.date.today().year):
        months_of_year = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO',
                          'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']

        filename = f'db/reports/RELATORIO-DE-{months_of_year[month]}-{year}.txt'
        response = my_file_manager.get_sheet_data(filename)
        if(len(response)>0):
            lines = response.split("\n")
            my_list_data = []
            for line in lines:
                text_splitted = line.split('*')
                register = []
                for item in text_splitted:
                    register.append(item)
                my_list_data.append(register)
            return my_list_data
        return [] 
