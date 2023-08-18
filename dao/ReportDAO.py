import datetime
import util
from util import my_file_manager


class ReportDAO:
    def __init__(self):
        self.REPORT_NAME = f'reports/{datetime.date.today()}.txt'.upper()
    
    def insert_register(self, user):
        self.REPORT_NAME = f'reports/{datetime.date.today()}.txt'.upper()
        text = f'{user["id"]}*{user["name"]}*{user["type"]}*{user["function"]}'
        if my_file_manager.append_in_file(self.REPORT_NAME, text) == True:
            util.change_color('green')
            util.print_center('REGISTRO INSERIDO!')
            util.change_color()            
