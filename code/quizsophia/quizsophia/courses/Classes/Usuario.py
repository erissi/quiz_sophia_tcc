class Usuario:

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def set_nome(self, nome):
        self.nome = nome

    def set_email(self,  email):
        self.email = email

    def set_ID(self, id):
        self.id = id

    def get_nome(self):
        return self.nome

    def get_email(self):
        return self.email

    def get_ID(self):
        return self.id