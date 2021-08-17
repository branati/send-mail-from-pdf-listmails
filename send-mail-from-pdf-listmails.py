#!/usr/bin/python3

# importa as bibliotecas necessárias
import PyPDF2
import re
import smtplib, ssl
from email.mime.text import MIMEText
from email.message import EmailMessage
import getpass
import time
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('send-mail-from-pdf-listmails.cfg')

#datahora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')


# Abre o arquivo pdf 
# lembre-se que para o windows você deve usar essa barra -> / 
# lembre-se também que você precisa colocar o caminho absoluto

arquivo = config['DEFAULT']['arquivo'] #Caminho do arquivo
quantidadedestinatarios = int(config['DEFAULT']['quantidadedestinatarios']) # Quantidade de destinatários em cada email enviado.
quantidadedestinatariosignorados = int(config['DEFAULT']['quantidadedestinatariosignorados']) # Quantidade de destinatários da lista que serão ignorados. Normalmente excluir os que já foram enviados anteriormente.
# Enviados: 341 + 300 + 300 + 300 + 300
delay =  int(config['DEFAULT']['delayenvio'])


message = "Olá\nEscreva a mensagem aqui."



pdf_file = open(arquivo, 'rb')

#Faz a leitura usando a biblioteca
read_pdf = PyPDF2.PdfFileReader(pdf_file)

# pega o numero de páginas
number_of_pages = read_pdf.getNumPages()

pagina = 0
listadeemails = []
print("%s: Iniciando leitura no arquivo." % (datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
while pagina < number_of_pages :
	page = read_pdf.getPage(pagina)
	page_content = page.extractText()
	parsed = ''.join(page_content)
	match = re.findall(r'[\w\.\-]+@[\w\-\.]+\b', parsed)
	for m in match:
		listadeemails.append(m)

	pagina += 1
	print(pagina)


listadeemails = listadeemails[quantidadedestinatariosignorados::]

#import pdb; pdb.set_trace()
#print(listadeemails)


#-----------------------------

# FROM = 'renato@branati.com.br'

# TO = ["jon@mycompany.com"] # must be a list

# SUBJECT = "Assunto"

# TEXT = "This message was sent with Python's smtplib."

# # Prepare actual message

# message = """\
# From: %s
# To: %s
# Subject: %s

# %s
# """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

# # Send the mail

# server = smtplib.SMTP('myserver')
# server.sendmail(FROM, TO, message)
# server.quit()


# send = smtplib.SMTP('smtp.zoho.com', 587)
#     send.starttls()
#     send.login('from_user@domain.com', 'password')
#     send.sendmail(FROM, TO, msg.as_string())

senha = getpass.getpass(prompt='Digite a Senha do email:', stream=None)

def send_mail(to_email, subject, message, server=config['EMAIL']['server'],
	porta=config['EMAIL']['porta'],
	from_email= config['EMAIL']['from'],
	senha=senha):
    # import smtplib
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    #msg['To'] = ', '.join(to_email)
    msg['Bcc'] = ', '.join(to_email)
    msg.set_content(message)
    #print(msg)
    #server = smtplib.SMTP_SSL(server, 587)
    server = smtplib.SMTP(server, porta)
    #context = ssl.create_default_context()
    #server.starttls(context=context)

    server.set_debuglevel(1)
    
    server.login(from_email, senha)  # user & password
    server.send_message(msg)
    server.quit()
    print('%s: Email enviado com sucesso.' % (datetime.now().strftime('%d/%m/%Y %H:%M:%S')))


quantprocessados = quantidadedestinatariosignorados
listaemailsquebrado = []
quantidade = int(quantidadedestinatarios)

#import pdb; pdb.set_trace()

for e in listadeemails:
	quantidade -= 1
	listaemailsquebrado.append(e)
	if quantidade == 1:
		#print(listaemailsquebrado)
		print("%s: Lista com %s destinatarios que é o número máximo. Enviando mensagem..." % (datetime.now().strftime('%d/%m/%Y %H:%M:%S'), quantidadedestinatarios))
		if config['PROCESSADOS']['testes'] == "N":
			print("NAO")

		print("aaa")
		
			
		############################### send_mail(to_email=listaemailsquebrado,subject='Ideia Legislativa 08/2018', message=message)
		quantidade = quantidadedestinatarios
		listaemailsquebrado = []
		print("%s: Servidor limita a 350 por hora. Aguardando 60 minutos para continuar o envio." % (datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
		quantprocessados += quantidadedestinatarios
		config['PROCESSADOS']['quantidade'] = str(quantprocessados)
		with open('send-mail-from-pdf-listmails.cfg', 'w') as configfile:
			config.write(configfile)
		time.sleep(delay)


#1541
#print(message)


	


#send_mail(to_email=['renato@branati.com.br'], subject='Ideia Legislativa 08/2018', message=message)


#-----------------------------------------------




#lê a primeira página completa
#page = read_pdf.getPage(10)

#extrai apenas o texto
#page_content = page.extractText()

# faz a junção das linhas 
#parsed = ''.join(page_content)

#print("Sem eliminar as quebras")
#print(parsed)

# remove as quebras de linha
#parsed = re.sub('n', '', parsed)
#print("Após eliminar as quebras")
#print(parsed)

#print("nPegando apenas as 20 primeiras posições")
#novastring = parsed[0:20]
#print(novastring)

#match = re.findall(r'[\w\.-]+@[\w\.-]+', parsed)
#match = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', parsed)
#match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', parsed)
#match = re.findall(r'[\w\.-]+@[\w\.-]+', parsed)
#match = re.findall(r'[\w\.\-]+@[\w\-\.]+\b', parsed)
#import pdb; pdb.set_trace()
#print(match)


