from Proyecto import Proyecto
import random
import pickle
import os
import os.path
import io
from datetime import *
from Registro_Punto_4 import Registro

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


def tiene_lenguaje(proyecto):
    tiene_len = False
    if proyecto.lenguaje != "":
        tiene_len = True

    return tiene_len


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
                # No deben repetirse los repositorios | Las líneas que tengan el lenguaje en blanco no deben ser procesadas.
                if busq_repo(vec, proyecto) or proyecto.lenguaje == "":
                    regs_omitidos += 1
                else:
                    # Agregamos el objeto al vector de registros
                    add_in_order(vec, proyecto)
                    regs_cargados += 1

        c += 1
    #print(c-regs_cargados)
    #Los registros omitidos van a ser los registros que no se logran cargar, es decir el total seria c(contador de iteraciones que se realizan sobre el vector, iterando linea a linea el archivo, menos la cantidad de registros que se caragan correctamente, dado esto nosotros para obtener los regs_omitidos, restaremos ambas cantidades y obtendremos el numero correcto, pudiendo asi corregir un error a la hora de mostrar los regs_omitidos
    regs_omitidos = (c - regs_cargados)
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
    print('-' * 11, '>Repositorio:', proyecto.repositorio, 'Fecha De Actualizacion:', str(proyecto.fecha_actualizacion),
          'Cantidad De estrellas:', str(estrellas))


def filtrar_tag(vec):
    # Abrir el archivo
    m = abrir_archivo()
    # Solicitamos por teclado el tag al usuario
    tag = validar_tag()
    # Consultamos al usuario si desea almacenar el listado de registros en un archivo de texto
    save_it = input('Desea almacenar el listado que se le brindara, en un archivo de texto (S/N): ').lower()
    # En caso de que se decida almacenarlo, inicializamos un vector vacio
    vec_file = []
    # Ciclo for para buscar proyectos que coincidan con el tag provisto por el usuario
    for i in vec:
        if tag in i.tags:
            # Mostramos la cantidad de estrellas del proyecto segun la cantidad de likes del mismo
            estrella_proyecto = cant_estrellas(i)
            # Una vez que determinamos la cantidad de estrellas que tiene1 el proyecto lo mostramos
            display_project(i, estrella_proyecto)
            if save_it == "s":
                vec_file.append(i)

    # Creamos el fileobject
    mf = open("proyectos_filtrados.csv", mode="wt", encoding="utf8")
    # Almacenamos los datos en el archivo
    main_line = 'nombre_usuario|repositorio|descripcion|fecha_actualizacion|lenguaje|estrellas|tags|url\n'
    mf.write(main_line)
    for v in range(len(vec_file)):
        # Itero cada objeto que tengo en el registro de objetos Y Obtengo los valores de los objetos del vector
        nombre = vec_file[v].nombre_usuario
        rep = vec_file[v].repositorio
        fecha = vec_file[v].fecha_actualizacion
        leng = vec_file[v].lenguaje
        likes = vec_file[v].likes
        tags = vec_file[v].tags
        url = vec_file[v].url
        # Los escribo en el archivo
        txt_line = nombre + '|' + rep + '|' + fecha + '|' + leng + '|' + likes + '|' + tags + '|' + url
        mf.write(txt_line)

    # Cerrar el archivo
    m.close()
    mf.close()


# A partir del vector determinar la cantidad de proyectos por cada lenguaje de programación. Mostrar los lenguajes de programación y su cantidad ordenados de mayor a menor por cantidad.
def lenguajes(vec):
    # Vector para almacenar los lenguajes de programacion
    vec_leng = []
    vec_cont = []
    # Por cada lenguaje, del vector, lo busco en el vector de lenguaje, y si existe incrementamos el vec_cont +1, en caso de que no lo agregamos al vec_leng, y hacemos append de 1 al vec_cont
    for i in range(len(vec)):
        # Preguntamos si el lenguaje existe en el vector de lenguajes
        existe, pos_leng = buscar_lenguaje(vec_leng, vec[i])
        if existe:
            # Si existe accedemos a la posicion i y incrementamos en 1
            vec_cont[pos_leng] += 1
        else:
            # Si no existe lo agregamos al vec_leng, y agregamos 1 al vec_cont
            vec_leng.append(vec[i].lenguaje)
            vec_cont.append(1)

    return vec_cont, vec_leng


def buscar_lenguaje(vec_len, i):
    pos_leng = None
    existe = False
    for j in range(len(vec_len)):
        if vec_len[j] == i.lenguaje:
            pos_leng = j
            existe = True

    return existe, pos_leng


def sort_leng(vec_leng, vec_cont):
    pos_l = None
    n = len(vec_cont)
    for i in range(n - 1):
        ordenado = True
        for j in range(n - i - 1):
            if vec_cont[j] > vec_cont[j + 1]:
                ordenado = False
                vec_cont[j], vec_cont[j + 1] = vec_cont[j + 1], vec_cont[j]
                vec_leng[j], vec_leng[j + 1] = vec_leng[j + 1], vec_leng[j]
                if ordenado:
                    break


# Popularidad: Se quiere conocer los meses en los que se actualizan los proyectos, de acuerdo a la cantidad de estrellas. Para ello se pide, a partir del vector, generar una matriz donde cada fila sea un mes de actualización (no importa de qué año corresponde)  y cada columna una cantidad de estrellas. Cada celda deberá contener la cantidad de proyectos que tengan ese mes de actualización y esa cantidad de estrellas. Las estrellas representan los rangos de likes indicados en el punto 2.

def popularidad(vec):
    # Generamos la matriz
    matriz = [[0] * 5 for f in range(12)]
    # Recorro el vector
    for i in vec:
        fecha = i.fecha_actualizacion

        mes = fecha[5] + fecha[6]

        if mes[0] != '0':
            mes = fecha[5] + fecha[6]
        else:
            mes = fecha[6]

        mes = int(mes)

        matriz[mes - 1][cant_estrellas(i) - 1] += 1

    # Mostrar Matriz
    mostrar_matriz(matriz)

    return matriz


def mostrar_matriz(mat):
    vec_meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    print('   |1★| 2★| 3★| 4★| 5★|')
    for i in range(len(mat)):
        fila = str(vec_meses[i])+" | "
        for j in range(len(mat[i])):
            fila += str(mat[i][j]) + " | "
        print(fila)


# Buscar proyecto actualizado: A partir del vector, buscar un repositorio con el nombre rep, siendo rep  un valor ingresado por teclado. Si existe mostrar sus datos y permitir reemplazar la URL del proyecto que se ingrese por teclado  y cambiar la fecha de actualización por la fecha actual (la fecha no se carga por teclado, investigue la manera de obtener la fecha actual y formatearla de igual manera en la que se encuentra en el archivo. Si no existe indicar con un mensaje de error.
def sol_rep():
    rep = input('Ingrese el nombre del repositorio a buscar: ')
    while not rep:
        rep = input('Ingrese el nombre del repositorio CORRECTAMENTE!!: ')

    return rep


def buscar_rep(rep, vec):
    existe = False
    pos = None
    for i in range(len(vec)):
        if vec[i].repositorio == rep:
            existe = True
            pos = i
    return existe, pos


def search_project_up(vec):
    rep = sol_rep()

    # Buscamos el repositorio en el vector
    existe, pos = buscar_rep(rep, vec)
    # En caso de que exista, mostramos sus datos
    if existe:
        print('*' * 21, 'Datos Del Proyecto', '*' * 21)
        print(vec[pos])
        # Reemplazar la URL del proyecto que se ingrese por teclado  y cambiar la fecha de actualización por la fecha actual
        url = input('Ingrese la URL a modificar del proyecto: ')
        # Modificamos la url
        vec[pos].url = url
        # Modificamos la fecha, a la fecha actual
        now = datetime.now()
        format = now.strftime('%Y-%m-%d')
        # print(format)
        vec[pos].fecha_actualizacion = format
        # Mostramos el registro Actualizado
        print('*' * 21, 'Datos Del Proyecto Actualizado', '*' * 21)
        print(vec[pos])


# Guardar populares: A partir de la matriz generada en el punto 4, almacenar su contenido (sólo los elementos mayores a cero) en un archivo binario en el que cada elemento sea un registro en el que se representen los campos: mes del año.estrellas (El rango indicado en el punto 2).cantidad de proyectos.
def save_populars(matriz):
    print('*' * 21, 'Grabando los datos en el archivo binario', '*' * 21)
    mf = open('matriz.dat', 'wb')
    # un recorrido por filas
    for f in range(len(matriz)):
        for c in range(len(matriz[f])):
            #Si la celda es mayor a cero
            if matriz[f][c] > 0:
                #Generar Instancia de Clase para luego guardarla en el archivo binario
                mes = f + 1
                estrellas = c + 1
                #print('El mes es:',mes)
                #print('La cantidad de estrellas es:',estrellas)
                #print(cant_proyectos)
                cant_proyectos = matriz[f][c]
                #Generamos el objeto
                reg = Registro(mes,estrellas,cant_proyectos)
                #Guardar los registros en el archivo binario
                pickle.dump(reg,mf)

    #Cierro el archivo
    mf.close()

#Mostrar archivo: Leer el contenido del archivo binario y volver a generar la matriz. Mostrarla en formato de tabla.
def leer_file():

    print('*' * 21, 'Grabando los datos del archivo binario', '*' * 21)

    #Abrir archivo
    mf = open('matriz.dat', 'wb')
    #Recorremos el archivo




def principal():
    print('*' * 21, 'Gestión de Proyectos', '*' * 21)
    # Vector
    vec = []
    #Matriz
    matriz = [[]]
    # Solicitamos una opcion al usuario
    mostrar_menu()
    opcion = int(input('Ingrese la opcion elegida: '))

    print()
    print()
    print()

    # Iniciamos el ciclo
    while opcion != 8:
        if opcion == 1:
            print()
            vec, regs_cargados, regs_omitidos = cargar_registros(vec)
            print('-' * 15, '>La cantidad de registros cargados en nuestro vector es:', regs_cargados)
            print('-' * 15, '>La cantidad de registros omitidos de la carga es:', regs_omitidos)

            for v in vec:
                print(v)
            print()

        elif opcion == 2:
            if not (vec != []):
                print('*', 'Psss, Primero pasa por la opcion 1, sino queres que el programa EXPLOTE')
            else:
                print()
                filtrar_tag(vec)
                print()
        elif opcion == 3:
            if not (vec != []):
                print('*', 'Psss, Primero pasa por la opcion 1, sino queres que el programa EXPLOTE')
            else:
                print()
                vec_cont, vec_leng = lenguajes(vec)
                # print(vec_leng)
                # print(vec_cont)
                sort_leng(vec_leng, vec_cont)
                for j in range(len(vec_cont)):
                    print('-' * 15, '>Hay ', str(vec_cont[j]), 'proyectos escritos en el lenguaje', vec_leng[j])
                print()
        elif opcion == 4:
            if not (vec != []):
                print('*', 'Psss, Primero pasa por la opcion 1, sino queres que el programa EXPLOTE')
            else:
                print()
                matriz = popularidad(vec)
                print()
        elif opcion == 5:
            if not (vec != []):
                print('*', 'Psss, Primero pasa por la opcion 1, sino queres que el programa EXPLOTE')
            else:
                print()
                search_project_up(vec)
                print()
        elif opcion == 6:
            if not(matriz != [[]]):
                print('*', 'Psss, Primero pasa por la opcion 4, sino queres que el programa EXPLOTE')
            else:
                print()
                save_populars(matriz)
                print()
        elif opcion == 7:
            pass

        # Solicitamos nuevamente la opcion al usuario
        mostrar_menu()
        opcion = int(input('Ingrese la opcion elegida: '))


# Control de ejecuccion del programa
if __name__ == '__main__':
    principal()
