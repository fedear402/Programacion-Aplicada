import pandas as pd 
import numpy as np 
import datetime as dt
import os, glob, credentials
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from templateReport import *


# abrimos el excel con la data a trabajar y limpiamos
data = pd.read_excel('A3337.xlsx')
data = data.fillna(value=0)
data = data[data['Departamento']!=0]
# re-asigno nombre columnas para más fácil acceso
data.columns = ['Nombre','Apellido','Mail','Departamento','Grupos']

today = dt.datetime.today().strftime("%d-%m-%Y %H:%M:%f") 

# First set the server
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()

# login account + password
server.login(credentials.account,credentials.password)

highlight = """<div class="header">
                <h5>&lt;Big Data/&gt;</h5>
              </div> """


for i in range(2):#len(file)):
  alumno = data.iloc[i,:].to_dict()


  text = f"""<h1>Buenos dias {alumno['Nombre']}, empecemos el Curso de Big Data.</h1><br />
  <h3>En el dia {today} quiero asegurarme que tienen las herramientas necesarias para seguir el curso.<br /></h3>
  <h3>Nota: con Python uno tambien puede manejar HTML, CSS y Javascript, ya que en este caso se los paso como texto siguiendo formato html<br />
  y el codificador SMTP protocolo de mails lo parsea a codigo y ustedes como usuario ven un mail autogenerado.</h3>"""

  details = """<h3>¿Que les pido?:
              <ul>
                <li>Captura de pantalla corriendo spyder, habiendo ejecutado "!pip install vaex" en la consola de la misma. Esta librería hace setup.</li>
                <li>Segundo, Francia, no aguante. El código de este mail va de yapa, para demostrar otro de los usos de Python.</li>
                <li>Avisenme a que tutorial van a asistir por temas de tps. Pueden cambiarse, pero avisenme.</li>
                <li>Si usan Mac vean <a href="https://www.youtube.com/watch?v=ezUCZiMXB20">este video</a>.</li>
                <li>Windows <a href="https://www.youtube.com/watch?v=m5i-Pq-z9w8">este es su link</a>.</li>
                <li>Asegurense de tener pip instalado también. Es el package manager de python y lo usamos para incorporar librerias</li>
                <li>Cualquier duda o problema pregunten. Aprovechen este espacio para probar, errar y en su suma aprender.</li>
              </ul></h3>"""


  signature = '<p>Disfruten la materia y los invito a que se adueñen de su contenido.<br /></p><p>Sin más, gracias por tanto, perdón por tan poco.</p>'
  signature += '<h1>Bienvenidos a Big Data. Lorenzo Reyes.</h1>'
  html_file = style + highlight + text + details + signature + end_html

  recipients = ['lreyes@udesa.edu.ar']#, f'{alumno['Mail']}']

  # In order to save & test the actual template we are sending
  if i == 0:
      e = open(f'template.html','w')
      e.write(html_file)
      e.close()

  def sendEmail(html_file):
      msg = MIMEMultipart('alternative')
      msg['X-Priority'] = '1'
      msg['Subject'] = f"Bienvenido a Big Data {alumno['Nombre']} {alumno['Apellido']} {today}"
      msg['From'] = credentials.account
      msg['To'] = ",".join(recipients)
      # Adjunto
      fp = open('welcome.py', 'rb')
      parte = MIMEBase('application','vnd.ms-excel')
      parte.set_payload(fp.read())
      encoders.encode_base64(parte)
      parte.add_header('Content-Disposition', 'attachment', filename='welcome.py')
      msg.attach(parte)
      fp = open('templateReport.py', 'rb')
      parte2 = MIMEBase('application','vnd.ms-excel')
      parte2.set_payload(fp.read())
      encoders.encode_base64(parte2)
      parte2.add_header('Content-Disposition', 'attachment', filename='template.py')
      msg.attach(parte2)
      part1 = html_file
      part1 = MIMEText(part1, 'html')
      msg.attach(part1)
      server.sendmail(credentials.account,
                    recipients,
                    msg.as_string())


  e = sendEmail(html_file)
  print(f"{dt.datetime.now().strftime('%H:%M:%S:%f')} Mail a {alumno['Nombre']} {alumno['Apellido']} Mandado!!!")
  e

server.quit()
