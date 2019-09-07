class e_mail:
    def __init__(self, mail: str):
        self.mail = mail

    def is_e_mail(self):
        return (("@" in self.mail) and ("." in self.mail))

    def is_gmail(self):
        return  ("gmail.com" in (self.mail.split("@"))[1])

    def is_mail(self):
        return  ("mail.ru" in (self.mail.split("@"))[1])

    def is_yandex(self):
        return ("yandex.ru" in (self.mail.split("@"))[1])

    def is_yahoo(self):
        return ("yahoo.com" in (self.mail.split("@"))[1])

    def get_mail(self):
        return self.mail