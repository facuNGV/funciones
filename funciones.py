import csv
import random
import requests
import json
import matplotlib.pyplot as plt


'''
Interacción con Usuario
'''
def solicitar_y_validar_numero(mensaje:str, mensaje_error:str)->int|float:
    """
    Esta función pide un dato por consola y valida que su valor sea numérico
    Recibe: El mensaje a imprimir al usuario
    Retorna: El numero validado
    """
    numero = input(mensaje)
    while determinar_numero(numero) == False:
        numero = input(mensaje_error)
    numero = castear_dato(numero)
    return numero


def solicitar_y_validar_numero_en_rango(
        mensaje:str, mensaje_error:str, minimo:int, maximo:int
                                        )->int:
    """
    Esta función pide un numero al usuario y valida que se encuentre
    dentro de un rango numérico determinado (inclusive)
    Recibe: Un mensaje que se imprimira al usuario, un rango numérico
    Retorna: El número seleccionado por el usuario, validado y casteado
    """
    numero = input(mensaje)
    while comprobar_numero_dentro_de_rango(numero, minimo, maximo) != True:
        numero = input(mensaje_error)
    numero = castear_dato(numero)
    return numero


def solicitar_string_y_validar_con_opciones_y_longitud(
        mensaje:str, opciones:list|str, 
        mensaje_error:str, longitud:int=None
        )->str:
    """
    Pide al usuario que ingrese un string, valida que sea una de las opciones
    dadas, y de la longitud que se indique por parametro si es el caso.
    Recibe: El mensaje a mostrar al usuario, un iterable con las opciones
    disponibles, opcionalmente una longitud maxima qude debe tener la cadena, 
    y opcionalmente un mensaje de error para el usuario.
    Retorna: La cadena elegida por el usuario validada.
    """
    string_seleccionado = input(mensaje)
    if longitud != None:
        while len(string_seleccionado) != longitud:
            string_seleccionado = input(mensaje_error)
    while (string_seleccionado in opciones) == False:
        string_seleccionado = input(mensaje_error)
    return string_seleccionado


def mostrar_menu(items:str, opciones:list):
    """
    Muestra por consola un menú de opciones disponibles para el usuario.
    Recibe: Los items de cada una de las opciones ("abcd..."), y las opciones
    en sí.
    Retorna: La opcion seleccionada por el usuario una vez validada.
    """
    print("-------------------------MENÚ-------------------------------------")
    print("Opciones disponibles: ")
    print()
    for i in range(len(opciones)):
        print(f"|               {items[i]}) {opciones[i]}")
    print("------------------------------------------------------------------")
    print(f"\n\n")


def solicitar_y_validar_numero_entero(mensaje:str, mensaje_error:str)->int:
    """
    Pide un número entero por consola y valida que lo sea.
    Recibe: Mensaje a imprimir al usuario, mensaje de error.
    Retorna: El número validado.
    """
    numero = input(mensaje)
    while (determinar_numero(numero) == False) or (determinar_numero(numero) == 'float'):
        numero = input(mensaje_error)
    numero = castear_dato(numero)
    return numero


def solicitar_y_validar_numero_flotante(mensaje:str, mensaje_error:str)->int:
    """
    Pide un flotante por consola y valida que lo sea.
    Recibe: El mensaje a imprimir al usuario, el mensaje de error.
    Retorna: El numero validado.
    """
    numero = input(mensaje)
    while (determinar_numero(numero) == False) or (determinar_numero(numero) == 'int'):
        numero = input(mensaje_error)
    numero = castear_dato(numero)
    return numero


def solicitar_elementos_para_lista( usuario_define_cantidad_elementos:bool,
        lista:list=[], mensaje:str="Elemento a añadir: ", cantidad_elementos:int=4
        )->list:
    """
    Segun se indique por parametro, pide(o no) al usuario la cantidad de 
    elementos a añadir a una lista, pide al usuario cuales añadir, y los añade.
    Recibe: True si el usuario define la cantidad de elementos sino False y 
    opcionales.
    Retorna: la lista 
    """
    if usuario_define_cantidad_elementos == True:
        cantidad_elementos = solicitar_y_validar_numero_entero("¿Cuantos elementos añade?: ")
    for _ in range(cantidad_elementos):
        elemento = input(mensaje)
        castear_dato(elemento)
        lista.append(elemento)
    return lista


def solicitar_y_rellenar_cadena(
        mensaje:str, posicion:str, minimo_caracteres:int=8, 
        elemento_relleno:str="0"
        )->str:
    """
    Solicita una cadena y la rellena con algun caracter hasta llegar a una
    determinada cantidad de caracteres minimos. Se puede indicar si rellenar
    la cadena adelante o detras.
    Recibe: mensaje a mostrar al usuario, posicion(antes/despues) en la que
    se colocara el relleno, minimo de caracteres, el elemento de relleno
    Retorna: la cadena rellenada 
    """
    cadena = input(mensaje)
    cantidad_a_rellenar = minimo_caracteres - len(cadena)
    relleno = ""
    for _ in range(cantidad_a_rellenar):
        relleno += elemento_relleno
    if posicion == "antes":
        retorno = relleno + cadena
    elif posicion == "despues":
        retorno = cadena + relleno
    return retorno




"""
Validaciones
"""
def comprobar_numero_dentro_de_rango(
        numero:int|float, minimo:int|float, maximo:int|float
        )->bool:
    """
    Valida si un determinado número se encuentra dentro de un rango (inclusive)
    Recibe: Un número, un determinado rango numérico
    Retorna: True en caso de que el número se encuentre dentro del rango, caso
    contrario False o None caso de que no se haya ingresado un número
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
    Determina si el dato ingresado es un número y su tipo.
    Permite la coma o el punto para decimales indistintamente (cuidado en 
    los floats).
    Recibe: un string cualquiera
    Retorna: el tipo de dato en caso de que sea un número, caso contrario
    devuelve False
    '''
    retorno = True
    # Verificar que no sea un string vacio
    if not dato:
        retorno = False
    # Variables para controlar mas adelante si tiene coma y dígitos
    tiene_coma = False
    tiene_digitos = False
    # Contador de Iteraciones
    pos = 0
    # Recorrer cada carácter en la cadena
    dato = str(dato)
    for char in dato:
        if char == '-':
            # Si el signo negativo no está primero no es un número
            if pos != 0:
                retorno = False
        elif char == ',' or char == ".":
            # La coma no puede estar al principio, ni al final, no pueden
            # haber dos y el caracter anterior no puede ser "-"
            if pos == 0 or pos == (len(dato)-1) or tiene_coma == True or caracter_anterior == "-":
                retorno = False
            tiene_coma = True
        # Todos los demás caracteres deben ser dígitos.
        elif ord(char) >= 48 and ord(char)<= 57:
            tiene_digitos = True
        else:
            retorno = False
        pos += 1
        caracter_anterior = char
    # Determinar que tipo es y que el retorno no haya entrado en ningun False
    if tiene_digitos == True and tiene_coma == True and retorno == True:
        retorno = "float"
    elif tiene_digitos == True and tiene_coma == False and retorno == True:
        retorno = "int"
    return retorno




'''
Situacionales
'''
def obtener_valor_por_clave(clave:any)->function:
    """
    Sirve cuando aplicamos sort a una lista de diccionarios, para establecer
    como criterio de ordenamiento una clave determinada. Pasar esta funcion
    como valor del key=
    Recibe: la clave a partir de la cual se ordenara la lista
    Retorna: una función que será recibida y utilizada por key= 
    """
    # tambien se podria hacer solo un return lambda como abajo
    # return lambda diccionario: diccionario.get(clave, None)
    def extractor(diccionario):
        return diccionario.get(clave, None)
    return extractor


def descuento_condicionado(importe_venta, montos_descuentos:dict):
    """
    A partir de un diccionario(clave=tupla, valor=numero) y un importe, segun
    en que rango(clave) se encuentre el importe, aplicará el descuento(valor) 
    correspondiente.
    Recibe: el importe de la venta, el diccionario con los rangos vinculados
    a los descuentos.
    Retorna: el importe final a pagar con el descuento aplicado 
    """
    importe_final = importe_venta
    for clave, valor in montos_descuentos.items():
        if importe_venta > clave[0] and importe_venta < clave[1]:
            importe_final = importe_venta - (importe_venta * valor)
    return importe_final


def obtener_menor_y_mayor_en_lista(lista_numeros:list)->list:
    """
    Encuentra el número más chico y el número más grande dentro de una lista
    de números.
    Recibe: la lista de números
    Retorna: una lista con el número más pequeño y más grande respectivamente.
    """
    if lista_numeros[0] > lista_numeros[1]:
        mayor = lista_numeros[0]
        menor = lista_numeros[1]
    elif lista_numeros[0] < lista_numeros[1]:
        menor = lista_numeros[0]
        mayor = lista_numeros[1]
    elif lista_numeros [0] == lista_numeros[1]:
        mayor = lista_numeros[0]
        menor = lista_numeros [1]
    for x in lista_numeros:      
        if x > mayor:
            mayor = x
        elif x < menor:
            menor = x
    return [menor, mayor]


def castear_dato(dato:str|int|float)->str|int|float:
    """
    Castea un dato determinado al tipo que le corresponda, si es un float con
    coma decimal, lo transforma a punto decimal.
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


def compra_combinada(P, M, D):
    """
    Escala de precios según el usuario combine; Procesador, Memoria y si desea
    extender el Disco.
    Recibe: opciones seleccionadas por el usuario.
    Retorna: El precio total a pagar 
    """
    match P:
        case 1:
            match M:
                case 1:
                    p = 800
                case 2:
                    p = 900
                case 3:
                    p = 1000
        case 2:
            match M:
                case 1:
                    p = 900
                case 2:
                    p = 1000
                case 3:
                    p = 1400
        case 3:
            match M:
                case 1:
                    p = 1200
                case 2:
                    p = 1400
                case 3:
                    p = 2000
    if D == 1:
        p = p + 300
    return p


def dibujar_grafico_matplotlib(
        x:list,y:list, marker: str = 'o', c: str = 'blue',
        set_facecolor: str = 'white', set_xlabel: str = 'Eje X',
        set_ylabel: str = 'Eje Y'
                    )->None:
    """
    Dibuja un grafico con matplotlib
    Recibe: valores del eje y, valores del eje x
    Retorna: None
    """

    fig = plt.figure()
    ax= fig.add_subplot()

    ax.plot(x, y, marker= marker, c= c)
    ax.set_facecolor(set_facecolor)
    ax.set_xlabel(set_xlabel)
    ax.set_ylabel(set_ylabel)
    plt.show()


def reordenar_letras_de_una_palabra(palabra:str)->str:
  """
  La funcion recibe una palabra cualquiera y reordena sus letras segun:
  Primero todas las letras minúsculas ordenadas de menor a mayor.
  Luego todas las letras mayúsculas ordenadas de menor a mayor.
  Todos los dígitos impares ordenados de menor a mayor.
  Todos los dígitos pares ordenados de menor a mayor.
  La palabra OrDenar1234 debería formar la siguiente nueva palabra según el
  criterior anterior: --> aenrrDO1324
  Recibe: una palabra
  Retorna: la misma palabra reordenada
  """
  resultado = ""
  lista_objetivo = []
  pre_resultado = []
  lista_minusculas = []
  lista_mayusculas = []
  lista_impares = []
  lista_pares = []

  for i in palabra:
      lista_objetivo.append(i)

  #Guardar en pre_resultado las letras ordenadas de menor a mayor 
  while len(lista_objetivo) != 0:
    min_caracter = "}"
    for i in lista_objetivo:
      if i < min_caracter:
        min_caracter = i
    pre_resultado.append(min_caracter)
    lista_objetivo.remove(min_caracter)

  #lista de minusculas
  for minusc in pre_resultado:
    minusc_int = False
    for j in range(10):
      j = str(j)
      if minusc == j:
        minusc_int = True
    if minusc_int == False:
      if minusc.islower() == True:
        lista_minusculas.append(minusc)

  #lista de mayusculas
  for may in pre_resultado:
    may_int = False
    for j in range(10):
      j = str(j)
      if may == j:
        may_int = True
    if may_int == False:
      if may.isupper() == True:
        lista_mayusculas.append(may)


  #lista de impares
  for i in pre_resultado:
    es_par = False
    for j in range(10):
      j = str(j)
      if i == j:
        i = int(i)
        if i % 2 == 0:
          es_par = True
        elif es_par == False:
          i = str(i)
          lista_impares.append(i)

  #lista de pares
  for i in pre_resultado:
    for j in range(10):
      j = str(j)
      if i == j:
        i = int(i)
        if i % 2 == 0:
          i = str(i)
          lista_pares.append(i)

  unir_lista = lista_minusculas + lista_mayusculas + lista_impares + lista_pares

  for i in unir_lista:
      resultado += i

  return resultado




'''
Matemáticas
'''
def determinar_multiplo(numero1:int|float, numero2:int|float)->bool:
    """
    Determina si un numero (1) es múltiplo de otro (2).
    Recibe: los dos numeros
    Retorna: True en caso que (1) sea múltiplo de (2), caso contrario; False.
    """
    if numero1 % numero2 == 0:
        es_multiplo = True
    else:
        es_multiplo = False
    return es_multiplo


def multiplicar_por_varios_numeros(numero:int|float, desde:int, hasta:int)->list:
    """
    Multiplica un número por un rango numérico indicado por parámetro,
    y devuelve una lista con los resultados.
    Recibe: número, un rango de números.
    Retorna: una lista con los resultados de la multiplicacion del número con
    cada uno de los números dentro del rango numérico indicado.
    """
    resultados = [numero * x for x in range(desde, hasta)]
    return resultados


def calcular_promedio(numeros:list)->int|float:
    """
    Calcula cual es el número promedio en una lista de números.
    Recibe: Una lista de números.
    Retorna: el promedio de estos números. 
    """
    if len(numeros) != 0:
        promedio = sum(numeros) / len(numeros)
    elif numeros == 0:
        promedio = 0
    return promedio


def convertir_a_porcentaje(cantidades:dict)->dict:
    """
    Recibe unas cantidades (un total de algo y porciones de el total), transforma
    las partes a su equivalente en porcentaje. Tambien crea una nueva clave-valor
    con la suma de todos los porcentajes.
    Recibe: las cantidades (total y porciones)
    Retorna: las mismas transformadas a porcentajes, y la suma de los
    porcentajes en una nueva clave-valor.
    """
    diccionario_transformado = {}
    porcentaje_total = 0
    for total_o_porcion, cantidad in cantidades.items():
        if total_o_porcion == "total":
            diccionario_transformado[total_o_porcion] = cantidad
        else:
            cantidad_en_porcentaje = (cantidad * 100)/cantidades["total"]
            diccionario_transformado[total_o_porcion] = cantidad_en_porcentaje
            porcentaje_total += cantidad_en_porcentaje
    diccionario_transformado["porcentaje total"] = porcentaje_total
    return diccionario_transformado


def detectar_primo_con_while(numero:int)->bool:
    """
    Determina si un número es primo o no.
    Recibe: un numero.
    Retorna: True en caso de ser primo, caso contrario False.
    """
    retorno = None
    contador_divisores = 0
    contador_resto_0 = 0
    while contador_divisores < numero:
        contador_divisores += 1
        if numero % contador_divisores == 0:
            contador_resto_0 += 1
    if contador_resto_0 == 2:
        retorno = True
    else:
        retorno = False
    return retorno


def detectar_primo_con_for(numero:int)->bool:
    """
    Determina si un número es primo o no.
    Recibe: un numero.
    Retorna: True en caso de ser primo, caso contrario False.
    """
    retorno = None
    acu = 0
    for x in range(1, numero+1):
        if (numero % x) == 0:
            acu += 1
    if acu == 2:
        retorno = True
    else:
        retorno = False
    return retorno


def calcular_factorial(numero:int)->int:
    """
    Calculara el factorial de un número. 
    Recibe: Un número entero
    Retorna: El factorial de dicho número
    """
    acumulador = 1
    for i in range(numero, 0, -1):
        acumulador *= i
    return acumulador


def calcular_factorial_recursividad(numero:int)->int:
    """
    Calculara el factorial de un número. 
    Recibe: Un número entero
    Retorna: El factorial de dicho número
    """
    if numero == 0:
        resultado = 1
    else:
        resultado = numero * calcular_factorial_recursividad(numero - 1)
        return resultado


def calcular_fibonacci(numero:int)->int:
    """
    Calculara cual sería el equivalente de un número en la sucesión de fibonacci
    Recibe: Un número entero
    Retorna: su equivalente en la sucesión de fibonacci.
    """
    if numero < 2:
        resultado = numero
    else:
        resultado = calcular_fibonacci(numero - 1) + calcular_fibonacci(numero - 2)
    return resultado


def mostrar_serie_fibonacci(numero:int)->None:
    """
    Calcula y muestra la sucesión de fibonacci hasta la cantidad que se pase por
    parámetro.
    Recibe: Un número entero
    Retorna: None.
    """
    for i in range(0, numero + 1):
        print(f"{i}={calcular_fibonacci(i)}") 




"""
Diccionarios
"""
def cortar_diccionario(diccionario:dict, desde:int, hasta:int)->dict:
    """
    Actúa como si los ítems de un diccionario fueran indexables y recorta el
    diccionario dejando solo desde el ítem, hasta el ítem que se le indique
    (no incluye al último).
    Recibe: El diccionario y las posiciones en las que queremos cortar
    Retorna: El diccionario recortado
    """
    slice_diccionario = dict(list(diccionario.items())[desde:hasta])
    return slice_diccionario




"""
Listas
"""
def hallar_indice_en_lista(lista:list, elemento:any)->list|None:
    """
    Determina si un valor es elemento de una lista y retorna sus índices.
    Recibe: la lista y el elemento.
    Retorna: una lista con los índices coincidentes. None en caso de no encontrar
    ninguno.
    """
    coincidencias = []
    for i in range(len(lista)):
        if elemento == lista[i]:
            coincidencias += [i]
    if len(coincidencias) == 0:
        coincidencias = None
    return coincidencias


def generar_lista_numeros_aleatorios(
        cantidad_numeros:int, minimo:int, maximo:int
        )->list:
    """
    Genera una lista aleatoria de números.
    Recibe: cantidad de números a generar, rango numérico para cada número.
    Retorna: la lista generada.
    """
    lista_numeros = []
    for _ in range(cantidad_numeros):
        lista_numeros += [random.randint(minimo, maximo)]
    return lista_numeros


def generar_lista_ASCII(
        primer_caracter:int, ultimo_caracter:int
        )->list:
    """
    Genera una lista de números dentro de un rango, los convierte a ASCII.
    Recibe: rango numérico.
    Retorna: lista con los caracteres ASCII.
    """
    lista_caracteres = []
    for numero in range(primer_caracter, ultimo_caracter+1):
        caracter = chr(numero)
        lista_caracteres += [caracter]
    return lista_caracteres


def generar_lista_ASCII_aleatorios(
        cantidad_elementos:int, minimo:int, maximo:int
        )->list:
    """
    Genera lista de numeros aleatorios, los convierte a ASCII.
    Recibe: cantidad de elementos, rango numérico para los números aleatorios.
    Retorna: lista con los caracteres ASCII.
    """
    lista_letras_aleatorias = []
    for _ in range(cantidad_elementos):
        numero_aleatorio = random.randint(minimo, maximo)
        letra = chr(numero_aleatorio)
        lista_letras_aleatorias += [letra]
    return lista_letras_aleatorias


def convertir_lista_ASCII(numeros:list[int])->list:
    """
    Convierte los numeros de una lista a ASCII.
    Recibe: lista de enteros.
    Retorna: misma lista con elementos transformados a su equivalente en ASCII.
    """
    lista_elementos_transformados = []
    retorno = None
    for numero in numeros:
        if determinar_numero(numero) == False:
            retorno = "La lista solo debe contener enteros"
            break
        numero_en_ascii = chr(numero)
        lista_elementos_transformados += [numero_en_ascii]
    retorno = lista_elementos_transformados
    return retorno


def mostrar_lista(lista:list, mensaje:str="")->None:
    """
    Imprime ordenadamente una lista por consola.
    Recibe: una lista, un mensaje opcional.
    Retorna: None.
    """
    if mensaje != "":
        print(mensaje)
    for elemento in lista:
        # No se agrega coma al final del último elemento.
        if elemento == lista[-1]:
            print(elemento)
        else:
            print(f"{elemento}", end=" , ")


def ordenar_lista(lista:list, criterio:str="ASC")->bool:
    """
    Ordena ascendiente o descendientemente una lista basandose en ASCII.
    Recibe: una lista, y un criterio para ordenar asecendientemente (ASC) o
    descendientemente (DESC).
    Retorna: True en caso de haber ordenado la lista, caso contrario; False.
    """
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
        """
        Toma dos elementos de una lista e intercambia posición (uno asume
        posición del otro).
        Recibe: una lista, dos índices.
        Retorna: True en caso swappeo realizado correctamente, caso contrario
        False.
        """
        retorno = False
        # Verifica más de un elemento, y que los índices estén dentro del largo de la lista.
        if len(lista) > 1 and indice_a < len(lista) and indice_b < len(lista):
            aux = lista[indice_a]
            lista[indice_a] = lista[indice_b]
            lista[indice_b] = aux
            retorno = True
        return retorno


"""
Matrices
"""
def crear_matriz(
        cantidad_filas:int, cantidad_columnas:int, valor_inicial:any=0
        )->list:
    """
    Crea una matriz.
    Recibe: cantidad de filas, cantidad de columnas, valor inicial de cada
    elemento.
    Retorna: La matriz.
    """
    matriz = []
    for _ in range(cantidad_filas):
        fila = [valor_inicial] * cantidad_columnas
        matriz += [fila]
    return matriz


def cargar_matriz_secuencialmente(matriz:list)->None:
    """
    Solicita por consola elementos para rellenar la matriz, secuencialmente.
    Recibe: una matriz.
    Retorna: None.
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            matriz[i][j] = castear_dato(input(f"Fila {i} columna {j}: "))


def buscar_elemento_en_matriz(matriz:list, elemento:any)->bool:
    """
    Comprueba que un elemento se encuentre (o no) en una matriz.
    Recibe: una matriz, un elemento.
    Retorna: True en caso de que el elemento se encuentre en la matriz, caso
    contrario False.
    """
    bandera_numero_repetido = False
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == elemento:
                bandera_numero_repetido = True
                break
        if bandera_numero_repetido == True:
            break
    return bandera_numero_repetido


def cargar_matriz_numeros_aleatorios_rango_1_9(
        matriz:list, minimo:int = 1, maximo:int = 9
        )->None:
    """
    Carga una matriz con números. Cada número será aleatorio e irrepetible dentro
    de la matriz, y estará dentro de un rango numérico indicado por parámetro. 
    Recibe: una matriz, un rango numérico.
    Retorna: None.
    """
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            numero_random = random.randint(minimo, maximo)
            while buscar_elemento_en_matriz(matriz, numero_random) == True:
                numero_random = random.randint(minimo, maximo)
            matriz[i][j] = numero_random


def llenar_matriz_aleatoriamente(matriz_vacia:list, desde:int=0, hasta:int=9)->None:
    """
    Carga una matriz con números aleatorios dentro de un rango indicado.
    Recibe: una matriz, un rango numérico.
    Retorna: None.
    """
    for i in range(len(matriz_vacia)):
        for j in range(len(matriz_vacia[i])):
            matriz_vacia[i][j] = random.randint(desde,hasta)


def mostrar_matriz(matriz:list)->None:
    """
    Visualizacion más gráfica de la matriz en la consola.
    Recibe: una matriz
    Retorna: None.
    """
        # [ [ 4, 3, 5, 7 ], [ 5, 6, 8, 7 ], [ 5, 6, 1, 6 ], [ 5, 9, 3, 5 ], [ 2, 1, 2, 6 ] ]
        #        [ 0, 1, 2, 3, 4 ]
    for i in range(len(matriz)):
        #               [ 0, 1, 2, 3 ]
        for j in range(len(matriz[i])):
            if j < (len(matriz[i])-1):
                print(f"{matriz[i][j]}", end="|")
            else:
                print(f"{matriz[i][j]}")
        #        [ 5 ]    - 1 = 4
        if i < (len(matriz)-1):
            # Un guión por columna y un guión por pipe (*2)
            print (("-" * len(matriz[i]))*2)


"""
Archivos
"""
def acumular_datos_de_columna_csv(ruta_archivo:str, clave_o_columna):
    """
    Suma los valores numéricos de la columna de un csv y obtiene el total
    de esa columna en todas las filas.
    Recibe: ruta del csv, la columna (clave en python) de los valores que van
    a sumarse
    Retorna: El acumulado total
    """
    with open(ruta_archivo) as csvfile:
        data = list(csv.DictReader(csvfile))
    total_acumulado = 0
    for i in range(len(data)):
        cantidad_fila = float(data[i][clave_o_columna])
        total_acumulado += cantidad_fila
    return total_acumulado


def contar_ocurrencias_csv(path_archivo:str, columna:str)->dict:
    """
    Arma un diccionario vinculando cada tipo de dato que hay en una columna
    determinada de un csv con la cantidad de filas en las que aparece.
    Recibe: la ruta del csv, la columna a analizar.
    Retorna: Un diccionario donde las claves son los valores únicos de la columna
    y los valores son la cantidad de veces que aparecen en el CSV.
    """
    diccionario_retorno = {}
    with open(path_archivo) as csvfile:
        data= list(csv.DictReader(csvfile))
    for i in range(len(data)):
        tipo_actual = data[i][columna]
        if tipo_actual not in diccionario_retorno:
            diccionario_retorno[tipo_actual] = 0
        diccionario_retorno[tipo_actual] += 1
    return diccionario_retorno


def convertir_json_a_dict(url:str)->dict:
    """
    Extrae un json de la nube a partir del link y lo convierte a diccionario
    Recibe: La url del json.
    Retorna: Los datos del json convertidos a diccionario.
    """
    response = requests.get(url= url)
    if response.ok:
        data = response.json()
        return data


def contar_ocurrencias_json(url:str,cantidad_id:int,clave:str,condicion:any)->dict:
    """
    Toma un Json. Cuenta la cantidad de veces que cada id tiene una clave que
    cumple una condicion. 
    Recibe: url del json. La cantidad de ids. La clave y condicion a buscar.
    Retorna: un dict vinculando cada id a su cantidad.
    """
    data = convertir_json_a_dict(url=url)
    cantidad_de_cada_id = {}
    for i in range(cantidad_id):
        contador = 0
        for user in data:            
            if user["id"] == i and user[clave] == condicion:
                contador += 1
        cantidad_de_cada_id[i] = contador
    return cantidad_de_cada_id