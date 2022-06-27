import json
import math
from random import random
import re

#Esta funcion sirve para centrar las palabras en la tabla
def centradoPalabra(palabra,length):
    if len(palabra)%2 == 0:
        resultado = " " * int((length - len(palabra))/2) + palabra + " " * int((length - len(palabra))/2)
    else:
       resultado = " " * int((length - len(palabra))/2) + palabra + " " * int((length - len(palabra))/2) + " "
    return resultado

#Esta funcion sirve para crear el archivo que contiene la base de datos
def crearArchivo(data):
    #Lo primero que haremos sera encriptar la data de los materiales    
    dataEncriptada = []
    for material in data:
        elementoNombre = encriptado(material[1])
        elementoColor = encriptado(material[2])
        elementoOrigen = encriptado(material[3])
        dataEncriptada.append((material[0], elementoNombre, elementoColor, elementoOrigen))

    #Aqui se crea el archivo y se le da el formato de tabla, centrando las palabras y generando la division de celdas
    with open("basedatos.txt","w") as file:
        encabezado1 = centradoPalabra(encriptado("ID"),20)
        encabezado2 = centradoPalabra(encriptado("NOMBRE"),20)
        encabezado3 = centradoPalabra(encriptado("COLOR"),20)
        encabezado4 = centradoPalabra(encriptado("ORIGEN"),20)
        file.write("="*len("||{}\t|{}\t|{}\t|{}\t||\n".format(encabezado1,encabezado2,encabezado3,encabezado4))+"\n")
        file.write("||{}\t|{}\t|{}\t|{}\t||\n".format(encabezado1,encabezado2,encabezado3,encabezado4))
        file.write("="*len("||{}\t|{}\t|{}\t|{}\t||\n".format(encabezado1,encabezado2,encabezado3,encabezado4))+"\n")
        for fila in dataEncriptada:
            string1 = centradoPalabra(fila[0],20)
            string2 = centradoPalabra(fila[1],20)
            string3 = centradoPalabra(fila[2],20)
            string4 = centradoPalabra(fila[3],20)

            file.write("||{}\t|{}\t|{}\t|{}\t||\n".format(string1,string2,string3,string4))
            file.write("="*len("||{}\t|{}\t|{}\t|{}\t||\n".format(string1,string2,string3,string4))+"\n")

#Funcion para encriptar la data
def encriptado(palabra):
    palabraEncriptada = ""
    for letra in palabra:
        palabraEncriptada += claveEncriptacion[letra]
    return palabraEncriptada

#Funcion para desencriptar la data
def desencriptado(palabra):
    palabraDesencriptada = ""
    for letra in palabra:
        palabraDesencriptada += claveDesencriptacion[letra]
    return palabraDesencriptada

#Obtenemos la clave de encriptacion desde el archivo encrip.json
with open ("encrip.json") as file:
    claveEncriptacion = json.load(file)

#Generamos la clave de desencriptacion como un nuevo diccionario, invirtiendo los valores key y value de la clave de encriptacion
claveDesencriptacion = {}
for key, value in claveEncriptacion.items():
    claveDesencriptacion[value] = key

#Obtencion de la base de datos y eliminacion de las diviones horizontales de las celdas y los saltos de linea
with open("basedatos.txt") as file:
    texto = file.read()
texto_strip = texto.replace("=", "")
texto_strip = texto_strip.replace("\n", "")

#Hacemos un split por la cadena || para separar los valores por fila y eliminamos espacios en blanco
array = texto_strip.split("||")
for element in array: 
    element_strip = element.strip()
    if element_strip == '' : 
        array.remove(element)

data = []

#Hacemos un split por la cadena | para obtener los distintos atributos de cada fila, eliminamos espacios en blanco y agregamos cada registro al arreglo data
for element in array:
    element_strip = element.strip()
    objeto_agregar =  element_strip.split("|")
    elementoNombre = desencriptado(objeto_agregar[1].strip())
    elementoColor = desencriptado(objeto_agregar[2].strip())
    elementoOrigen = desencriptado(objeto_agregar[3].strip())
   
    data.append((objeto_agregar[0].strip(), elementoNombre, elementoColor, elementoOrigen))

#Eliminamos la cabecera de la tabla
data.pop(0)

print ("Bienvenido a la base de datos de la CIA indique que acción desea realizar:\n Ingrese 1 para AGREGAR un registro\n Ingrese 2 para ELIMINAR un registro\n Ingrese 3 para EDITAR un registro\n Ingrese 4 para CONSULTAR todos los registros")
tipoOperacion = input()

if tipoOperacion == "1":
    print ("Ingrese el nombre del material (Max. 20 caracteres - No se aceptan números ni caracteres especiales)")
    nombreMaterial = input ()
    print ("Ingrese el color del material (Max. 20 caracteres - No se aceptan números ni caracteres especiales)")
    colorMaterial = input ()
    print ("Ingrese el origen del material (Max. 20 caracteres - No se aceptan números ni caracteres especiales)")
    origenMaterial = input ()

    caracteresIngresados = nombreMaterial + colorMaterial + origenMaterial

    caracteresEspecial = re.findall("[+!@#$%^&*()_+~{\]}\=>?¿|:\"<>?;',./¡²³¤€¼½¾‘’¥×«»¬¶´çáéíóúÁÉÍÓÚ]", caracteresIngresados)
    numeros = re.findall("[0-9]", caracteresIngresados)
    if caracteresEspecial or numeros:
        print("Alguno de los datos ingresados contiene números o caracteres especial, su solicitud no puede ser procesada")
        exit()

    if len(nombreMaterial)>20 or len(colorMaterial)>20 or len(origenMaterial)>20:
        print ("Alguno de los datos ingresados superó el max. de caracteres permitidos, su solicitud no puede ser procesada")
        exit()

    idMaterial = str(math.trunc ((random()*100000000)))
    data.append ((idMaterial, nombreMaterial.upper(), colorMaterial.upper(), origenMaterial.upper()))
    crearArchivo(data)
    print ("El material ha sido agregado exitosamente")


elif tipoOperacion == "2":
    print ("Ingrese el ID del material que desea eliminar")
    idMaterial = input ()
    elemento = 0
    for material in data:
        if material[0] == idMaterial:
            elemento = material
    if elemento == 0 :
        print("El ID ingresado no coincide con ninguno de los materiales existentes")
    else :
        for elemento in data:
            if elemento[0] == idMaterial:
                data.remove (elemento)
                crearArchivo(data)
                print ("El material ha sido eliminado exitosamente")


elif tipoOperacion == "3":
    print ("Ingrese el ID del elemento que desea editar")
    idMaterial = input ()
    elemento = 0
    for material in data:
        if material[0] == idMaterial:
            elemento = material
    if elemento == 0 :
        print("El ID ingresado no coincide con ninguno de los materiales existentes")
    else :
        print ("Usted ingresó el ID que coincide con el siguiente material: NOMBRE:" + elemento[1] + ", COLOR:" + elemento[2] + ", ORIGEN:" + elemento[3])
        print ("Ingrese el nuevo nombre del material")
        nuevoNombre = input ()
        print ("Ingrese el nuevo color del material")
        nuevoColor = input ()
        print ("Ingrese el nuevo origen del material")
        nuevoOrigen = input ()

        caracteresIngresados = nuevoNombre + nuevoColor + nuevoOrigen

        caracteresEspecial = re.findall("[+!@#$%^&*()_+~{\]}\=>?¿|:\"<>?;',./¡²³¤€¼½¾‘’¥×«»¬¶´çáéíóúÁÉÍÓÚ]", caracteresIngresados)
        numeros = re.findall("[0-9]", caracteresIngresados)
        if caracteresEspecial or numeros:
            print("Alguno de los datos ingresados contiene números o caracteres especial, su solicitud no puede ser procesada")
            exit()

        if len(nuevoNombre)>20 or len(nuevoColor)>20 or len(nuevoOrigen)>20:
            print ("Alguno de los datos ingresados superó el max. de caracteres permitidos, su solicitud no puede ser procesada")
            exit()
        data.remove (elemento)
        data.append ((elemento[0],nuevoNombre.upper(), nuevoColor.upper(), nuevoOrigen.upper()))
        crearArchivo(data)
        print ("El material ha sido editado exitosamente")


elif tipoOperacion == "4":
    tablaMostrar = ""
    encabezado1 = centradoPalabra("ID",20)
    encabezado2 = centradoPalabra("NOMBRE",20)
    encabezado3 = centradoPalabra("COLOR",20)
    encabezado4 = centradoPalabra("ORIGEN",20)
    tablaMostrar += ("="*len("||{}\t|{}\t|{}\t|{}\t||\n".format(encabezado1,encabezado2,encabezado3,encabezado4))+"\n")
    tablaMostrar += ("||{}\t|{}\t|{}\t|{}\t||\n".format(encabezado1,encabezado2,encabezado3,encabezado4))
    tablaMostrar += ("="*len("||{}\t|{}\t|{}\t|{}\t||\n".format(encabezado1,encabezado2,encabezado3,encabezado4))+"\n")

    for fila in data:
            string1 = centradoPalabra(fila[0],20)
            string2 = centradoPalabra(fila[1],20)
            string3 = centradoPalabra(fila[2],20)
            string4 = centradoPalabra(fila[3],20)

            tablaMostrar += ("||{}\t|{}\t|{}\t|{}\t||\n".format(string1,string2,string3,string4))
            tablaMostrar += ("="*len("||{}\t|{}\t|{}\t|{}\t||\n".format(string1,string2,string3,string4))+"\n")
    print (tablaMostrar)
