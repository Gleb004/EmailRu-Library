url_log = 'https://account.mail.ru/login?page=https%3A%2F%2Fe.mail.ru%2Finbox%3Futm_" \
          "source%3Dportal%26utm_medium%3Dmailbox%26utm_campaign%3De.mail.ru%26mt_click_" \
          "id%3Dmt-veoz41-1649081406-1746181238&allow_external=1&from=octavius'

url_reg = 'https://account.mail.ru/signup?from=navi&lang=ru_RU'

names = open('names.txt', 'r')
vec = []
for name in names:
    vec.append(name)

months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
gender = ['Женский', 'Мужской']

bigL = [chr(i) for i in range(65, 91)]
smallL = [chr(i) for i in range(97, 123)]
specL = [chr(i) for i in range(33, 59)]
specL.remove(':')
rem = ["bigL"]

get = open("DB_in.txt", "r")

emails = []
for i in get:
    email, pas = i.split(":")[0], i.split(":")[1]
    emails.append({"email": email, "password": pas})

boxes = ["Inbox", '"&BB4EQgQ,BEAEMAQyBDsENQQ9BD0ESwQ1-"', '"&BCEEPwQwBDw-"', '"INBOX/Newsletters"']