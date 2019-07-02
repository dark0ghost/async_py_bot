class e_mail:
    def __init__(self, mail: str):
        self.mail = mail

    def is_e_mail(self):
        return True if (("@" in self.mail) and ("." in self.mail)) else False

    def is_gmail(self):
        return True if ("gamil.com" in (self.mail.split("@"))[1]) else False

    def is_mail(self):
        return True if ("mail.ru" in (self.mail.split("@"))[1]) else False

    def is_yandex(self):
        return True if ("yandex.ru" in (self.mail.split("@"))[1]) else False

    def is_yahoo(self):
        return True if ("yahoo.com" in (self.mail.split("@"))[1]) else False

    def get_mail(self):
        return self.mail