import os
import time
import socketserver
import arabic_reshaper

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
from reportlab.lib.units import inch
from reportlab.lib import colors



class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    
    def handle(self):
        print("salam")
        # self.request is the TCP socket connected to the client
        try:
            self.data = self.request.recv(1024).strip()
            print("{} wrote:".format(self.client_address[0]))
            string = str(self.data).split(',')
            print(string)
            data_string = []
            for index in string:
                data_string.append(index.replace("'",""))
            if data_string[3] == "test_print":
                cmd = r"C:\pprint.exe C:\test_print.pdf"
                os.system(cmd)
                return
            self.persian_pdf(data_string[0].replace('b"',''), data_string[1], data_string[2], data_string[3], data_string[4], data_string[5], data_string[6], data_string[7].replace('\\n',' , '), data_string[8].rstrip('\\n').replace('\\n', ''))
            cmd = r"C:\pprint.exe C:\persianprint.pdf"
            os.system(cmd)  
        except Exception as e:
            print(e)

    def persian_pdf(self, scan_result_datetime, device, capacity, serial, total_file, infected, type_problem, av_engines, infected_files_report):
        print("@@@@@@@@@", scan_result_datetime, device, capacity, serial, total_file,
          infected, type_problem, av_engines, infected_files_report)

        doc = SimpleDocTemplate(r'C:/persianprint.pdf', pagesize=(3.16*inch, 8.27*inch),
                            rightMargin=10, leftMargin=10,
                            topMargin=0, bottomMargin=5)

        pdfmetrics.registerFont(
            TTFont('Vaziri', r'C:/fonts/Vazir.ttf'))
    
        def paragraphContext(contextText, contectStyle):
            titleP = Paragraph(contextText, styles[contectStyle])
            return titleP

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_RIGHT))
        styles.add(ParagraphStyle(
            name='titleParph',
            fontName='Vaziri',
            fontSize=7,
            leading=20,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_CENTER,
            spaceBefore=0,
            spaceAfter=1,
        ))
        styles.add(ParagraphStyle(
            name='titleParphEn',
            fontName='Vaziri',
            fontSize=7,
            leading=20,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=1,
        ))
        styles.add(ParagraphStyle(
            name='titleParphRight',
            fontName='Vaziri',
            fontSize=7,
            leading=20,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_RIGHT,
            spaceBefore=0,
            spaceAfter=1,
        ))
 
        def spaces():
            Story.append(paragraphContext('<br/>', 'titleParph'))
            Story.append(paragraphContext('<br/>', 'titleParph'))
            Story.append(paragraphContext('<br/>', 'titleParph'))
            Story.append(paragraphContext('<br/>', 'titleParph'))
            


        device_data = [[paragraphContext(get_display(arabic_reshaper.reshape(u'ظرفیت')), 'titleParph'), paragraphContext(get_display(arabic_reshaper.reshape(u'دستگاه ورودی')), 'titleParph'), paragraphContext(get_display(arabic_reshaper.reshape(u'تاریخ')), 'titleParph')],
                [paragraphContext(get_display(arabic_reshaper.reshape(str(capacity))), 'titleParph'), paragraphContext(get_display(arabic_reshaper.reshape(str(device)[:14])), 'titleParph'), paragraphContext(get_display(arabic_reshaper.reshape(str(scan_result_datetime))), 'titleParph')]]
        table = Table(device_data, 2*[1*inch], 2*[0.4*inch])
        table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (2, 1), 'CENTER'),
            ('INNERGRID', (0, 0), (2, 1), 0.25, colors.black),
            ('BOX', (0, 0), (2, 1), 0.25, colors.black),
            ]))
       
        data = [[paragraphContext(get_display(arabic_reshaper.reshape(u'#')), 'titleParph'), paragraphContext(get_display(arabic_reshaper.reshape(u'آلوده')), 'titleParph'), paragraphContext(get_display(arabic_reshaper.reshape(u'کل فایل ها')), 'titleParph')],
                [paragraphContext(get_display(arabic_reshaper.reshape('#')), 'titleParph'), paragraphContext(get_display(arabic_reshaper.reshape(str(infected))), 'titleParph'), paragraphContext(get_display(arabic_reshaper.reshape(str(total_file))), 'titleParph')]]
        t = Table(data, 2*[1*inch], 2*[0.4*inch])
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (2, 1), 'CENTER'),
            ('INNERGRID', (0, 0), (2, 1), 0.25, colors.black),
            ('BOX', (0, 0), (2, 1), 0.25, colors.black),
            ]))
        Story = []

        im = Image(r'C:/farafan2.JPG', 1.1*inch, 1.1*inch)
        Story.append(im)
        Story.append(table)
        spaces()
        spaces()
        Story.append(paragraphContext(get_display(
            arabic_reshaper.reshape(u'سریال : ' + str(serial))), 'titleParphRight'))
        Story.append(t)
        spaces()
        spaces()
        Story.append(paragraphContext(get_display(
            arabic_reshaper.reshape(u'آنتی ویروس ها : ')), 'titleParphRight'))
        Story.append(paragraphContext(str(av_engines), 'titleParphEn'))
        Story.append(paragraphContext(get_display(
            arabic_reshaper.reshape(u'فایل های آلوده : ')), 'titleParphRight'))
        Story.append(paragraphContext(
            str(infected_files_report).replace('*Infected Files:', ''), 'titleParphEn'))
        doc.build(Story)
  

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9989

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
