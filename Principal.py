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


# Primer Punto
def abrir_archivo():
    m = open("proyectos.csv", mode="r", encoding="utf8")
    filename = "proyectos.csv"
    c = 0
    # Mostramos algunos datos de prueba
    for linea in m:
        if c == 1:
            print(linea, end='')
        c += 1


def cargar_registros(vec):
    # Abrimos el archivo
    m = open("proyectos.csv", mode="rt", encoding="utf8")
    filename = "proyectos.csv"
    c = 0
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
                # Agrego
                vec.append(proyecto)

        c += 1

    return vec



def principal():
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
            vec = cargar_registros(vec)
            for v in vec:
                print(v)

            print(len(vec))


        elif opcion == 2:
            pass
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
