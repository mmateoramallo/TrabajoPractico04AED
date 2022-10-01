class Registro:
    def __init__(self,mes,estrellas,cant_proyectos):
        self.mes = mes
        self.estrellas = estrellas
        self.cant_proyectos = cant_proyectos

    def __str__(self):
        return f"Mes {str(self.mes)}, Cantidad De estrellas {str(self.estrellas)}, Cantidad De Proyectos {str(self.cant_proyectos)}"