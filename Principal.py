from Proyecto import Proyecto
import random
import pickle
import os
import os.path
import io


def mostrar_menu():
    print("1. Cargar Datos")
    print("2. Filtrar Por Tag")
    print("3. Cantidad De Proyectos por Lenguaje")
    print("4. Popularidad")
    print("5. Buscar Proyecto Actualizado")
    print("6. Guardar Populares")
    print("7. Mostrar Archivo")
    print("8. Salir")


#  Cargar: Cargar el contenido del archivo en un vector de registros de proyectos (defina la clase Proyecto), donde cada registro tenga los siguientes campos: nombre_usuario: cadena de caracteres.
def abrir_archivo():
    m = open("proyectos.csv", mode="rt", encoding="utf8")
    filename = "proyectos.csv"
    return m


def busq_repo(vec, proyecto):
    existe = False
    for i in range(len(vec)):
        if vec[i].repositorio == proyecto.repositorio:
            existe = True

    return existe


def cargar_registros(vec):
    # Abrimos el archivo
    m = abrir_archivo()
    filename = "proyectos.csv"
    c = 0
    regs_cargados = 0
    regs_omitidos = 0
    # Recorro el archivo
    for linea in m:
        if c > 0:
            # En este punto tenemos en la variable txt_line, un array compuesto por los campos que necesitaremos para poder cargarlo a los objetos
            txt_line = linea.split('|')
            # Almaceno los valores
            for p in txt_line:
                nombre = txt_line[0]
                repo = txt_line[1]
                fecha_actualizacion = txt_line[3]
                lenguaje = txt_line[4]
                likes = txt_line[5]
                tags = txt_line[6]
                url = txt_line[7]

                # Creo el objeto
                proyecto = Proyecto(nombre, repo, fecha_actualizacion, lenguaje, likes, tags, url)
                # Agregamos el objeto al vector de registros
                if busq_repo(vec, proyecto) or proyecto.lenguaje == " ":
                    regs_omitidos += 1
                else:
                    add_in_order(vec, proyecto)
                    regs_cargados += 1

        c += 1
    m.close()
    return vec, regs_cargados, regs_omitidos


def add_in_order(vec, proyecto):
    n = len(vec)
    pos = n
    izq, der = 0, n - 1
    while izq <= der:
        c = (izq + der) // 2
        if vec[c].repositorio == proyecto.repositorio:
            pos = c
            break
        if proyecto.repositorio < vec[c].repositorio:
            der = c - 1
        else:
            izq = c + 1
    if izq > der:
        pos = izq
    vec[pos:pos] = [proyecto]


# Filtrar por tag: Cargar por teclado un tag (cadena de caracteres) y a partir del vector de proyectos, mostrar todos aquellos registros que contengan al tag en alguno de los elementos del vector alojado en el campo tag. Los proyectos deben mostrarse a razón de un registro por línea mostrando solamente el nombre del repositorio, la fecha de actualización y  cantidad de estrellas.
def validar_tag():
    tag = input('Ingrese el tag a filtrar por proyectos: ')
    while tag == "":
        tag = input('Ingrese el tag a filtrar por proyectos: ')

    return tag


def convert_likes(proyecto):
    likes = proyecto.likes
    pos_p = None
    pos_k = None
    # Recorro el string likes
    for i in range(len(likes)):
        if likes[i] == ".":
            pos_p = i
        elif likes[i] == "k":
            pos_k = i

    if "." in proyecto.likes:
        # Obtengo los numeros delante de la coma
        nros_adelante = likes[:pos_p]
        # Obtengo los numeros despues de la coma
        nros_detras = likes[pos_p:pos_k]
        # Asumimos que nos quedamos con el indice (1) del string nros_detras, y le agrego dos ceros
        nros_detras = nros_detras[1]
        nro_final = nros_adelante + nros_detras + '00'
        likes = int(nro_final)
    else:
        likes = proyecto.likes
        for i in range(len(likes)):
            if likes[i] == "k":
                pos_k = i
                nros_delante = likes[:pos_k]
                nros = nros_delante + '000'
                likes = int(nros)

    return likes


def cant_estrellas(proyecto):
    estrellas = 0

    likes = convert_likes(proyecto)

    if 0 <= likes <= 10000:
        estrellas = 1
    elif 10001 <= likes <= 20000:
        estrellas = 2
    elif 20001 <= likes <= 30000:
        estrellas = 3
    elif 30001 <= likes <= 40000:
        estrellas = 4
    elif likes > 40000:
        estrellas = 5

    return estrellas


def display_project(proyecto, estrellas):
    print('-' * 11, '>Repositorio:', proyecto.repositorio, 'Fecha De Actualizacion:', str(proyecto.fecha_actualizacion), 'Cantidad De estrellas:', str(estrellas))


def filtrar_tag(vec):
    # Abrir el archivo
    m = abrir_archivo()
    # Solicitamos por teclado el tag al usuario
    tag = validar_tag()
    # Ciclo for para buscar proyectos que coincidan con el tag provisto por el usuario
    for i in vec:
        if tag in i.tags:
            # Mostramos la cantidad de estrellas del proyecto segun la cantidad de likes del mismo
            estrella_proyecto = cant_estrellas(i)
            # Una vez que determinamos la cantidad de estrellas que tiene1 el proyecto lo mostramos
            display_project(i,estrella_proyecto)

    # Cerrar el archivo
    m.close()


# Punto 3
def lenguajes(vec):
    # Abrir el archivo
    m = abrir_archivo()
    # Vector para almacenar los lenguajes de programacion
    vec_leng = []
    vec_cont = []
    # Recorro el vec
    for v in range(len(vec)):
        for g in range(len(vec_leng)):
            # Veo si el lenguaje del v.lenguaje esta en el vec_leng?
            if vec[v].lenguaje == vec_leng[g]:
                pass
            else:
                vec_leng.append(vec[v].lenguaje)


def principal():
    print('*' * 21, 'Gestión de Proyectos', '*' * 21)
    # Vector
    vec = []
    # Solicitamos una opcion al usuario
    mostrar_menu()
    opcion = int(input('Ingrese la opcion elegida: '))

    print()
    print()
    print()

    # Iniciamos el ciclo
    while opcion != 8:
        if opcion == 1:
            vec, regs_cargados, regs_omitidos = cargar_registros(vec)
            """
            for v in vec:
                print(v)
                print(type(v.likes))
            """
            print('-' * 15, '>La cantidad de registros cargados en nuestro vector es:', regs_cargados)
            print('-' * 15, '>La cantidad de registros omitidos de la carga es:', regs_omitidos)
        elif opcion == 2:
            filtrar_tag(vec)
        elif opcion == 3:
            pass
        elif opcion == 4:
            pass
        elif opcion == 5:
            pass
        elif opcion == 6:
            pass
        elif opcion == 7:
            pass

        # Solicitamos nuevamente la opcion al usuario
        mostrar_menu()
        opcion = int(input('Ingrese la opcion elegida: '))


# Control de ejecuccion del programa
if __name__ == '__main__':
    principal()
