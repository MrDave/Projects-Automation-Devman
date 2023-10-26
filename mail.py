import smtplib
import os

sender_email = 'DevmanYourProject@yandex.ru'
sender_name = 'Devman'
recepient_email = 'student_email'
recepient_name = 'student_name'
website = 'https://dvmn.org/makeschedule'

letter_template = '''Привет, %student_name%! 

Наступает пора командных проектов. Будет вместо учебного плана.

Будет что-то вроде урока на девмане, только без шагов, зато втроём (очень редко вдвоем) + с ПМом. Созвоны будут по 20 минут каждый день в течение недели.
Быть у компьютера не обязательно.

Выбери здесь %website% неделю и удобное время для созвонов.'''.replace('%student_name%', recepient_name).replace('%website%', website)

letter_heading = 'Командный проект'
content_type = 'text/plain; charset="UTF-8";'

letter = '''\
From: {sender_email}
To: {recepient_email}
Subject: {letter_heading}
Content-Type: {content_type}


{letter_template}.'''.format(sender_email=sender_email,recepient_email=recepient_email,
letter_heading=letter_heading,content_type=content_type,letter_template=letter_template)

letter = letter.encode("UTF-8")

server = smtplib.SMTP_SSL('smtp.yandex.ru:465')
login = os.environ['YANDEX_LOGIN']
password = os.environ['YANDEX_PASSWORD']
server.login(login, password)
server.sendmail(sender_email, recepient_email, letter)
server.quit()