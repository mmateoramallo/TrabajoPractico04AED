class Proyecto:
    def __init__(self, nombre_usuario, repositorio, fecha_actualizacion, lenguaje, likes, tags, url):
        self.nombre_usuario = nombre_usuario
        self.repositorio = repositorio
        self.fecha_actualizacion = fecha_actualizacion
        self.lenguaje = lenguaje
        self.likes = likes
        self.tags = tags
        self.url = url

    def __str__(self):
        return f"Nombre Del Usuario {self.nombre_usuario}, repositorio {self.repositorio}, fecha {str(self.fecha_actualizacion)}, lenguaje de desarrollo {self.lenguaje}, likes {str(self.likes)}, tags {str(self.tags)}, url: {str(self.url)}"



