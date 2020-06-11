class RequisitoTrofeu:

    def __init__(self, perc_ouro, perc_prata, perc_bronze):
        self.perc_ouro = perc_ouro
        self.perc_prata = perc_prata
        self.perc_bronze = perc_bronze

    def set_perc_ouro(self, ouro):
        self.perc_ouro = ouro

    def set_perc_prata(self, prata):
        self.perc_prata = prata

    def set_perc_bronze(self, bronze):
        self.perc_bronze = bronze

    def get_perc_ouro(self):
        return self.perc_ouro

    def get_perc_prata(self):
        return self.perc_prata

    def get_perc_bronze(self):
        return self.perc_bronze