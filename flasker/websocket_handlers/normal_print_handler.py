
import os

from .message_handler import MessageHandler
from .utils import persian_pdf


class NormalPrintHandler():

    def __init__(self):
        self.role = r'normal_print'

    def apply_handler(self, message):
       persian_pdf(
           message['scan_result_datetime'],
           message['device'],
           message['capacity'],
           message['serial'],
           message['total_file'],
           message['infected'],
           message['type_problem'],
           message['av_engines'],
           message['infected_files_report']
       ) 
