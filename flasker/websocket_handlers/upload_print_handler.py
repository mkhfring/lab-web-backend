
import os
from datetime import datetime

from .message_handler import MessageHandler
from .utils import upload_pdf


class UploadPrintHandler():

    def __init__(self):
        self.role = r'upload_print'

    def apply_handler(self, message):
        date = datetime.now().strftime('%Y_%m_%d_%H_%M')
        upload_pdf(message['directory'], date)
