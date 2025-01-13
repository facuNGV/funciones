import csv
import random

'''
Interacción con Usuario
'''
def solicitar_y_validar_numero(mensaje:str)->int|float:
    """
    Esta función pide un dato por consola y valida que su valor sea numérico
    Recibe: El mensaje a imprimir al usuario
    Retorna: El numero validado
    """
    numero = input(mensaje)
    while determinar_numero(numero) == False:
        numero = input(mensaje)
    numero = castear_dato(numero)
    return numero


def solicitar_y_validar_numero_en_rango(mensaje:str, minimo:int, maximo:int)->int:
    """
    Esta función pide un numero al usuario y valida que se encuentre
    dentro de un rango numérico determinado (inclusive)
    Recibe: Un mensaje que se imprimira al usuario, un rango numérico
    Retorna: El mismo número validado y casteado
    """
    numero = input(mensaje)
    while comprobar_numero_dentro_de_rango(numero, minimo, maximo) != True:
        numero = input(mensaje)
    numero = castear_dato(numero)
    return numero


def solicitar_y_validar_cadena(
        mensaje:str, opciones:list|str, longitud:int=None, 
        mensaje_error:str="[Error]"
        )->str:
    """
    Esta función pide al usuario que ingrese una cadena, valida que el usuario
    ingrese un dato dentro de las opciones disponibles, y de la longitud que se
    indique por parametro si es el caso.
    Recibe: El mensaje a mostrar al usuario, un iterable con las opciones
    disponibles, opcionalmente una longitud para la cadena, y opcionalmente un 
    mensaje de error para el usuario
    Retorna: El dato elegido por el usuario validado.
    """
    cadena = input(mensaje)
    if longitud != None:
        while medir_coleccion(cadena) != longitud:
            cadena = input(f"{mensaje_error} {mensaje}")

    while (cadena in opciones) == False:
        cadena = input(f"{mensaje_error}\n{mensaje}")
    
    return cadena


def generar_menu(
        items:str, opciones:list,
        mensaje:str=f"\nSeleccione una de las opciones disponibles: ",
        mensaje_error:str=""       
        ):
    """
    Esta función muestra por consola un menú de opciones que el usuario puede
    seleccionar, y solicita al usuario que seleccione una de las disponibles.
    Recibe: Los items de cada una de las opciones, las opciones en sí, un 
    mensaje opcional que mostrar al usuario, y un mensaje opcional en caso de error.
    Retorna: La opcion seleccionada por el usuario una vez validada.
    """
    print("-------------------------MENÚ-------------------------------------")
    print("Opciones disponibles: ")
    print()
    for i in range(len(opciones)):
        print(f"|               {items[i]}) {opciones[i]}")
    print("------------------------------------------------------------------")
    opcion_seleccionada = solicitar_y_validar_cadena(mensaje,items,1,mensaje_error)
    print("------------------------------------------------------------------")
    print(f"\n\n")
    return opcion_seleccionada


def solicitar_y_validar_numero_entero(mensaje:str)->int:
    """
    Esta función pide un dato por consola y valida que sea un número entero.
    Recibe: El mensaje a imprimir al usuario.
    Retorna: El numero validado.
    """
    numero = input(mensaje)
    while (determinar_numero(numero) == False) or (determinar_numero(numero) == 'float'):
        numero = input(mensaje)
    numero = castear_dato(numero)
    return numero


def solicitar_y_validar_numero_flotante(mensaje:str)->int:
    """
    Esta función pide un dato por consola y valida que sea un número entero.
    Recibe: El mensaje a imprimir al usuario.
    Retorna: El numero validado.
    """
    numero = input(mensaje)
    while (determinar_numero(numero) == False) or (determinar_numero(numero) == 'int'):
        numero = input(mensaje)
    numero = castear_dato(numero)
    return numero


def solicitar_y_validar_numero_entero_en_rango(
        mensaje:str, minimo:int, maximo:int
        )->int:
    """
    Esta función pide un entero al usuario y valida que se encuentre
    dentro de un rango numérico determinado (inclusive)
    Recibe: Un mensaje que se imprimira al usuario, un rango numérico
    Retorna: El mismo número validado y casteado
    """
    numero = input(mensaje)
    while (comprobar_numero_dentro_de_rango(numero, minimo, maximo) != True) or (
            determinar_numero(numero) != 'int'
            ):
        numero = input(f"[ERROR] {mensaje}")
    numero = castear_dato(numero)
    return numero


def solicitar_y_añadir_a_lista(mensaje:str="Ingrese un elemento: ",lista:list=[])->list:
    
    cantidad_elementos = solicitar_y_validar_numero_entero("¿Cuantos elementos añade?: ")
    for _ in range(cantidad_elementos):
        elemento = input(mensaje)
        castear_dato(elemento)
        lista.append(elemento)
    return lista
'''
Situacionales
'''
def cortar_iterable(iterable:str|list, desde:int, hasta:int)->str|list:
    """
    Esta función recorta un iterable según las posiciones que se le
    pasen por parametro (0, n). Entre esas dos posiciones (inclusive) 
    es que se recortara el iterable. 
    Recibe: El iterable y las posiciones en las que queremos cortar
    Retorna: El iterable recortado
    """
    contador = 0
    if type(iterable) == list:
        resultado = []
        for letra in iterable:
            if contador >= desde and contador < hasta:
                resultado += [letra]
            contador += 1
    else:
        resultado = ""
        for letra in iterable:
            if contador >= desde and contador < hasta:
                resultado += letra
            contador += 1

    return resultado


def comprobar_numero_dentro_de_rango(
        numero:int|float, minimo:int|float, maximo:int|float
        )->bool:
    """
    Esta función valida si un determinado numero se encuentra dentro de un 
    rango determinado (inclusive)
    Recibe: Un numero, un determinado rango numérico
    Retorna: True en caso de que el numero se encuentre dentro del rango
    False caso contrario o None caso de que no se haya ingresado un numero
    """
    retorno = None
    if determinar_numero(numero) != False:
        numero = castear_dato(numero)
        if numero >= minimo and numero <= maximo: 
            retorno = True
        else:
            retorno = False
    return retorno


def determinar_numero(dato:str)->bool|str:
        '''
        Esta función determina si el dato ingresado es un número y su tipo.
        Permite la coma o el punto para decimales indistintamente (cuidado en los flaots).
        Recibe: un str cualquiera
        Retorna: el tipo de dato en caso de que sea un número, caso contrario
        devuelve False
        '''
        retorno = False
        # Verificar si se ingreso algo o no se ingreso nada
        if not dato:
            return False
        # Variables para controlar mas adelante si tiene coma y digitos
        tiene_coma = False
        tiene_digitos = False
        # Contador de Iteraciónes
        pos = 0
        # Recorrer cada carácter en la cadena
        dato = str(dato)
        for char in dato:
            if char == '-':
                # Si el signo negativo no está primero no es un número
                if pos != 0:
                    return False
            elif char == ',' or char == ".":
                # La coma no puede estar al principio, ni al final, no pueden
                # haber dos y el caracter anterior no puede ser "-"
                if pos == 0 or pos == (len(dato)-1) or tiene_coma == True or caracter_anterior == "-":
                    return False
                tiene_coma = True
            # Todos los demás caracteres deben ser dígitos.
            elif ord(char) >= 48 and ord(char)<= 57:
                tiene_digitos = True
            else:
                return False
            pos += 1
            caracter_anterior = char
        # Determinar que tipo es
        if tiene_digitos == True and tiene_coma == True:
            retorno = "float"
        elif tiene_digitos == True and tiene_coma == False:
            retorno = "int"
        return retorno


def castear_dato(dato:str|int|float)->str|int|float:
    """
    Esta función castea un dato determinado al tipo que le corresponda
    Recibe: un dato
    Retorna: el mismo dato casteado a su tipo correspondiente
    """
    retorno = None
    # determinar_numero devolverá float aunque el decimal tenga un punto (.) o una coma (,)
    # Transformo en un punto (.) independientemente de como este el decimal:
    if determinar_numero(dato) == "float":
        float_coma_string = str(dato)
        float_punto_string = ""
        for digito in float_coma_string:
            if digito == ",":
                float_punto_string += "."
            else:
                float_punto_string += digito
        retorno = float(float_punto_string)
    elif determinar_numero(dato) == "int":
        retorno = int(dato)
    elif type(dato) == str:
        retorno = str(dato)
    elif type(dato) == bool:
        retorno = bool(dato)

    return retorno


def medir_coleccion(coleccion:str|list|int|float)->int:
    """
    Esta función determina de cuantos caracteres esta compuesta una cadena
    Recibe: una cadena cualquiera
    Retorna: el numero de caracteres que compone la cadena
    """
    contador = 0
    for _ in coleccion:
        contador += 1
    return contador


# Matemáticas

def determinar_primo(numero:int)->bool:
    """
    Esta función determina si un número es primo o no
    Recibe: un numero 
    Retorna: True en caso de ser primo, caso contrario False
    """
    contador_divisores = 0
    contador_resto_0 = 0
    while contador_divisores < numero:
        contador_divisores += 1
        if numero % contador_divisores == 0:
            contador_resto_0 += 1
    if contador_resto_0 == 2:
        return True
    else: 
        return False


def calcular_factorial(numero:int)->int:
    """
    Esta funcion calculara el factorial de un numero 
    Recibe: Un número entero
    Retorna: El factorial de dicho número
    """
    acumulador = 1
    for i in range(numero, 0, -1):
        acumulador *= i
    return acumulador


def rellenar_cadena(
        mensaje:str, minimo_digitos:int=8, elemento_relleno:str="0"
        )->str:
    cadena = input(mensaje)
    cantidad_a_rellenar = minimo_digitos - medir_coleccion(cadena)
    relleno = ""
    for _ in range(cantidad_a_rellenar):
        relleno += elemento_relleno
    return relleno + cadena


def calcular_factorial(numero:int)->int:
    if numero == 0:
        resultado = 1
    else:
        resultado = numero * calcular_factorial(numero - 1)
        return resultado


def calcular_fibonacci(numero:int)->int: #7
    if numero < 2:
        resultado = numero
    else:
        resultado = calcular_fibonacci(numero - 1) + calcular_fibonacci(numero - 2)
    return resultado


def mostrar_serie_fibonacci(numero:int)->None:
    for i in range(0, numero + 1):
        print(f"{i}={calcular_fibonacci(i)}") 

# Listas
def append_casero(
        append_casero_lista:list, elemento:str|int|float|bool|list=None,
        mensaje:str=None
        )->None:
    """
    Un elemento solicitado al usuario o pasado por parámetro se añade a una lista
    Recibe: O bien... el elemento por parámetro o bien... el mensaje para 
    solicitar el elemento al usuario. Y la lista que se desea modificar.
    Retorna: None
    """
    if mensaje != None:
        elemento = input(mensaje)
        elemento = castear_dato(elemento)
    append_casero_lista += [elemento]


def solicitar_subir_elementos_en_indice(lista:list)->None:
    """
    Esta función pide al usuario índices y elementos determinados y los sube a una lista pasada
    por parámetro. No inserta, por lo que si ya hay un elemento en la posición lo reemplazará.
    Pedirá datos hasta que el usuario lo quiera
    Recibe: La lista a modificar, los mensajes para solicitar los datos al usuario
    Retorna: None 
    """
    mensaje_indice = "¿En que posición desea agregar el elemento?: "
    mensaje_elemento = "Ingrese el elemento a añadir: "
    while True:
        indice_ingresado = solicitar_y_validar_numero_en_rango(mensaje_indice, 0, (len(lista)-1))
        
        elemento_ingresado = input(mensaje_elemento)
        if determinar_numero(elemento_ingresado) == "int":
            elemento_ingresado = int(elemento_ingresado)
        elif determinar_numero(elemento_ingresado) == "float":
            elemento_ingresado = float(elemento_ingresado)
 
        lista[indice_ingresado] = elemento_ingresado

        respuesta = input("Desea seguir ingresando datos? S/N: ")        
        if respuesta == "N":
            break

# here
def buscar_elemento_en_lista(lista:list, dato:int)->list|None:
    coincidencias = []
    for i in range(medir_coleccion(lista)):
        if dato == lista[i]:
            coincidencias += [i]
    if medir_coleccion(coincidencias) == 0:
        coincidencias = None
    return coincidencias

#le agregaria una validacion que me valide si son numeros lo que ingresa el usuario
def pedir_elementos_para_lista(cantidad:int, mensaje:str, tipo:str)->list:
    """
    """
    lista = []
    for _ in range(cantidad):
        dato = input(mensaje)
        if tipo == "int":
            dato = int(dato)
        elif tipo == "float":
            dato = float(dato)
        lista += [dato]
    return lista


def cargar_lista(cantidad:int, mensaje:str, tipo:str)->list:
    """
    """
    lista = []
    for _ in range(cantidad):
        dato = input(mensaje)
        if tipo == "int":
            dato = int(dato)
        elif tipo == "float":
            dato = float(dato)
        lista += [dato]
    return lista


def generar_lista_aleatoria_numeros(
        cantidad_numeros:int, minimo:int, maximo:int
        )->list:
    """
    """
    lista_numeros = []
    for _ in range(cantidad_numeros):
        lista_numeros += [random.randint(minimo, maximo)]
    return lista_numeros


def generar_lista_aleatoria_letras_mayusculas(
        cantidad_elementos:int, minimo:int, maximo:int
        )->list:
    """
    """
    lista_letras_aleatorias = []
    for _ in range(cantidad_elementos):
        numero_aleatorio = random.randint(minimo, maximo)
        letra = chr(numero_aleatorio)
        lista_letras_aleatorias += [letra]
    return lista_letras_aleatorias


def mostrar_lista(lista:list, mensaje:str="")->None:
    """
    """
    if mensaje != "":
        print(mensaje)
    for elemento in lista:
        if elemento == lista[-1]:
            print(elemento)
        else:
            print(f"{elemento}", end=" , ")


def ordenar_lista(lista:list, criterio:str="ASC")->bool:
    bandera = False
    for i in range(len(lista)-1):
        for j in range(i+1, len(lista)):
            if (criterio == "ASC" and lista[i] > lista[j]) or (criterio == "DESC" and lista[i] < lista[j]):
                aux = lista[j]
                lista[j] = lista[i]
                lista[i] = aux
                bandera = True
    return bandera


def swapear(lista:list, indice_a=int, indice_b=int)->bool:
        retorno = False
        if len(lista) > 1 and indice_a < len(lista) and indice_b < len(lista):
            aux = lista[indice_a]
            lista[indice_a] = lista[indice_b]
            lista[indice_b] = aux
            retorno = True
        return retorno

# Matrices
def crear_matriz(
        cantidad_filas:int, cantidad_columnas:int, valor_inicial:any=0
        )->list:
    """
    Esta función se encarga de crear una matriz vacía
        Recibe:
            cantidad_filas (int): representa las filas que va a tener la matriz
            cantidad_columans (int): representa las columnas que va a tener la matriz

        Devuelve:
            matriz (list): la matriz creada a través de los parámetros
    """
    matriz = []
    for _ in range(cantidad_filas):
        fila = [valor_inicial] * cantidad_columnas
        matriz += [fila]

    return matriz


def cargar_matriz_secuencialmente(matriz:list):
    # Le pido al usuario los datos de la matriz
    # como es secuencial debo controlar que 
    # ingrese todos los datos
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz[i][j] = int(input(f"Fila {i} columna {j}"))


def verificar_numero_repetido_en_matriz(matriz:list, numero:int)->bool:
    """
    """
    bandera_numero_repetido = False
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == numero:
                bandera_numero_repetido = True
                break
        if bandera_numero_repetido == True:
            break
    return bandera_numero_repetido


def cargar_matriz_elementos_aleatorios_rango_1_9(
        matriz:list, minimo:int = 1, maximo:int = 9
        )->None:
    """
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            numero_random = random.randint(minimo, maximo)
            while verificar_numero_repetido_en_matriz(matriz, numero_random) == True:
                numero_random = random.randint(minimo, maximo)
            matriz[i][j] = numero_random


def llenar_matriz_aleatoriamente(matriz_vacia:list, desde:int=0, hasta:int=9)->None:
    for i in range(len(matriz_vacia)):
        for j in range(len(matriz_vacia[i])):
            matriz_vacia[i][j] = str(random.randint(desde,hasta))


def mostrar_matriz(matriz:list)->None:
    """
    """
        # [ [ 4, 3, 5, 7 ], [ 5, 6, 8, 7 ], [ 5, 6, 1, 6 ], [ 5, 9, 3, 5 ], [ 2, 1, 2, 6 ] ]

        #        [ 0, 1, 2, 3, 4 ]
    for i in range(len(matriz)):
        #               [ 0, 1, 2, 3 ]
        for j in range(len(matriz[i])):
            if j < (len(matriz[i])-1):
                print(f"{matriz[i][j]}", end="|")
            else:
                print(f"{matriz[i][j]}", end="")
        print()
        #        [ 5 ]    - 1 = 4
        if i < (len(matriz)-1):
            print (("-" * len(matriz[i]))*2)


"""
Archivos
"""
def contar_dato_csv(ruta_archivo:str, clave_o_columna):
    """
    Suma las filas de un csv en una columna cuyos datos sean numéricos y obtiene
    el total de esa columna en todas las filas.
    Recibe: ruta del csv, 
    """
    with open(ruta_archivo) as csvfile:
        data = list(csv.DictReader(csvfile))
    total_acumulado = 0
    for i in range(len(data)):
        cantidad_fila = float(data[i][clave_o_columna])
        total_acumulado += cantidad_fila
    return total_acumulado


def contar_ambientes_csv(ambientes, archivo):
    """
    Esta funcion abre un csv y segun el tipo de ambiente seleccionado por parametro
    determina cuantos hay en el archivo
    Recibe: tipo de ambiente, ruta del csv
    Retorna: cantidad de departamentos con ese tipo de ambiente
    """

    with open(archivo) as csvfile:
        data= list(csv.DictReader(csvfile))
    cantidad_2ambientes = 0
    cantidad_3ambientes = 0
    retorno = None
    for fila in data:
        try:
            tipo_ambiente = int(fila.get("ambientes", 0.0))
        except:
            tipo_ambiente = 0
        if tipo_ambiente == 2:
            cantidad_2ambientes += 1
        elif tipo_ambiente == 3:
            cantidad_3ambientes += 1
    print(cantidad_2ambientes, cantidad_3ambientes)
    if ambientes == "2_ambientes":
        retorno = cantidad_2ambientes        
    elif ambientes == "3_ambientes":
        retorno = cantidad_3ambientes
    return retorno