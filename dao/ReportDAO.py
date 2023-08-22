import datetime
import util
from util import my_file_manager


class ReportDAO:
    def __init__(self):
        months = ['JANEIRO', 'FEVEREIRO', 'MARÇO', 'ABRIL', 'MAIO', 'JUNHO', 'JULHO', 'AGOSTO', 'SETEMBRO', 'OUTUBRO', 'NOVEMBRO', 'DEZEMBRO']
        self.REPORT_NAME = f'db/reports/RELATORIO-DE-{months[datetime.date.today().month-1]}.txt'
    
    def insert_register(self, user):
        text = f'{user["id"]}*{user["name"]}*{user["type"]}*{user["function"]}*{datetime.datetime.now()}'
        if my_file_manager.append_in_file(self.REPORT_NAME, text) == True:
            util.change_color('green')
            util.print_center('REGISTRO INSERIDO!')
            util.change_color()            
