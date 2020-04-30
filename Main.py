#importacion de librerias del sistema, randomizador, lector de teclas(windows), generador del pdf
import os
import subprocess
import random
import codecs
from msvcrt import getch
from reportlab.pdfgen import canvas

#importacion de las clases
from automata import Automata,Transicion,Estado
from gramatica import Gramatica,Produccion,LadoDerecho
from cadena import Cadena,Evaluacion
from gramatica2 import Gramatica2,Produccion2
from automataP import AutomataP,EstadoP,TransicionP
from arbol import ArbolS,Nodo

#mensaje de ayuda
ayuda = """\n
----------------------------------------
| Lenguajes formales y de programacion |
|              Seccion: B-             |
|   Catedratico: Inga. Zulma Aguirre   |
|          Auxiliar: Luis Yela         |
|           Ultimo digito: 5           |
----------------------------------------
\n"""

#arreglos para almacenar los AFD, las gramaticas y las cadenas evaluadas
automatas = []
gramaticas = []
cadenas = []
gramaticas2 = []
automatasDePila = []

#valor de la repeticion
repeticion = 0

def validarCadenaTipo2(automata,entrada):
    #simbolo que representa la letra griega lambda 
    #le puse alpha porque lambda es una palabra reservada
    alpha = "\u03BB"

    #creacion del arbol de derivacion (arbol sintactico)
    arbol = ArbolS(0,[])

    #arreglo que retorna la validacion de la cadena, el csv y el arbol
    respuesta = []

    #pila para validar la cadena
    pila = []

    #arreglo para contar la cantidad de producciones en las que deriva un no terminal
    noTransiciones = []

    #pila que almacena el id para generar los enlaces del arbol
    pilaNoTerminales = []

    #valor que almacena el no terminal actual
    actual = automata.noTerminalInicial

    #variable para recorrer la cadena de entrada
    it = 0
    
    #identificadores para los nodos del arbol
    idenTer = 0
    idenNoTer = 1
    idenAux = 0

    #variable que tendra el valor del identificador nodo actual del arbol
    cambio = ""

    #copiando la cadena de entrada para poder generar el csv
    entradaAux = entrada

    #cabeceras del csv
    csv = "PILA$ENTRADA$TRANSICION\n"

    #agregando el simbolo de aceptacion de cadena
    pila.append("#")

    
    csv += alpha+"$"+entradaAux+"$(i, "+alpha+", "+alpha+"; p, #)\n"
    
    #agregando el valor del no terminal actual a la pila
    pila.append(actual)

    csv += "#$"+entradaAux+"$(p, "+alpha+", "+alpha+"; q, "+actual+")\n"

    #buscando las transiciones asociadas al no terminal actual
    for transicion in automata.transiciones:
        if transicion.lecturaPila == actual:
            noTransiciones.append(transicion)
            
    #si tiene una sola produccion ingresarla a la pila si no verificar cual es la que se necesita
    if len(noTransiciones) == 1:

        #dando formato a la pila para el reporte csv
        val1 = str(pila).rstrip("]")
        val1 = val1.lstrip("[")
        val1 = val1.replace(", ","")
        val1 = val1.replace("'","")

        #obteniendo la produccion
        val2 = noTransiciones[0].guardarEnPila.split(" ")
        
        #destruyento y obteniendo el no terminal de la pila para ser ingresado al arbol
        value = pila.pop()
        arbol.agregar(value,"nt"+str(idenAux),"f")    

        #agregando los valores del lado derecho de la produccion a la pila y al arbol
        for val in reversed(val2):
            pila.append(val)
            if val.islower() == True or val.isdigit() == True:
                arbol.agregar(val,"nt"+str(idenAux),"t"+str(idenTer))
                idenTer += 1
            else:
                pilaNoTerminales.append( "nt"+str(idenNoTer) )
                arbol.agregar(val,"nt"+str(idenAux),"nt"+str(idenNoTer) )
                idenNoTer += 1

        idenAux+=1

        #dando formato al lado derecho de la produccion para ingresarla al reporte csv
        val2 = str(val2).rstrip("]")
        val2 = val2.lstrip("[")
        val2 = val2.replace(", ","")
        val2 = val2.replace("'","")
        csv += val1+"$"+entradaAux+"$"+"(q, "+alpha+", "+actual+"; q,"+val2+")\n"
    else:
        val1 = str(pila).rstrip("]")
        val1 = val1.lstrip("[")
        val1 = val1.replace(", ","")
        val1 = val1.replace("'","")
        
        pila.pop()
        aux = []
        
        for valor in noTransiciones:
            aux = valor.guardarEnPila.split(" ")
            if aux[0] == entrada[0]:
                break

        for val in reversed(valor.guardarEnPila.split(" ")):
            pila.append(val)
            if val.islower() == True or val.isdigit() == True:
                arbol.agregar(val,"nt"+str(idenAux),"t"+str(idenTer))
                idenTer += 1
            else:
                arbol.agregar(val,"nt"+str(idenAux),"mt"+str(idenNoTer))
                pilaNoTerminales.append( "nt"+str(idenNoTer) )
                idenNoTer += 1
  
        idenAux += 1

        val2 = str(aux).rstrip("]")
        val2 = val2.lstrip("[")
        val2 = val2.replace(", ","")
        val2 = val2.replace("'","")
        csv += val1+"$"+entradaAux+"$"+"(q, "+alpha+", "+actual+"; q,"+val2+")\n"

    #recorriendo la cadena de entrada    
    while it < len(entrada):
        noTransiciones = []

        #obteniendo el valor al tope de la pila
        actual = pila[len(pila)-1]

        #recorrer siempre que en la pila no quede unicamente el simbolo de aceptacion
        if pila[len(pila)-1] != "#":

            #verificando si al tope de la pila esta un terminal o un no terminal
            if pila[len(pila)-1].islower()==True or pila[len(pila)-1].isdigit()==True:
                #verificando que el terminal al tope de la pila sea el mismo que el 
                #terminal que se esta leyendo en la entrada
                if pila[len(pila)-1] == entrada[it]:
                    val1 = str(pila).rstrip("]")
                    val1 = val1.lstrip("[")
                    val1 = val1.replace(", ","")
                    val1 = val1.replace("'","")
                    csv += val1+"$"+entradaAux+"$(q, "+actual+", "+actual+"; q,"+alpha+")\n"
                    entradaAux = entradaAux[1:len(entradaAux)]
                    
                    #extrayendo el terminal de la pila
                    pila.pop()
                    it += 1
                else:  
                    respuesta.append("La cadena es invalida")
                    csv +="$"+"$Invalida"
                    respuesta.append(csv) 
                    respuesta.append(arbol)
                    return respuesta 
            else:
                #obteniendo las producciones del no terminal actual
                for transicion in automata.transiciones:
                    if transicion.lecturaPila == actual:
                        noTransiciones.append(transicion)

                if len(noTransiciones) == 0:
                    respuesta.append("La cadena es invalida")
                    csv +="$"+"$Invalida"
                    respuesta.append(csv) 
                    respuesta.append(arbol)
                    return respuesta 
                elif len(noTransiciones) == 1:
                    val1 = str(pila).rstrip("]")
                    val1 = val1.lstrip("[")
                    val1 = val1.replace(", ","")
                    val1 = val1.replace("'","")
                    val2 = noTransiciones[0].guardarEnPila.split(" ")

                    pila.pop()
                    cambio = pilaNoTerminales.pop(len(pilaNoTerminales)-1)

                    for val in reversed(val2):
                        pila.append(val)
                        if val.islower() == True or val.isdigit() == True:
                            arbol.agregar(val,cambio,"t"+str(idenTer))
                            idenTer += 1
                        else:
                            pilaNoTerminales.append("nt"+str(idenNoTer) )
                            arbol.agregar(val,cambio ,"nt"+str(idenNoTer))
                            idenNoTer += 1
              
                    idenAux += 1

                    val2 = str(val2).rstrip("]")
                    val2 = val2.lstrip("[")
                    val2 = val2.replace(", ","")
                    val2 = val2.replace("'","")
                    csv += val1+"$"+entradaAux+"$"+"(q, "+alpha+", "+actual+"; q,"+val2+")\n"
                else:
                    val1 = str(pila).rstrip("]")
                    val1 = val1.lstrip("[")
                    val1 = val1.replace(", ","")
                    val1 = val1.replace("'","")

                    aux = []
                    pila.pop()
                    cambio = pilaNoTerminales.pop(len(pilaNoTerminales)-1)
                    for valor in noTransiciones:
                        aux = valor.guardarEnPila.split(" ")
                        if aux[0] == entrada[it]:
                            break
                    for val in reversed(valor.guardarEnPila.split(" ")):
                        pila.append(val)
                        if val.islower() == True or val.isdigit() == True:
                            arbol.agregar(val,cambio,"t"+str(idenTer))
                            idenTer += 1
                        else:
                            pilaNoTerminales.append("nt"+str(idenNoTer))
                            arbol.agregar(val,cambio,"nt"+str(idenNoTer))
                            idenNoTer += 1
                
                    idenAux += 1

                    val2 = str(aux).rstrip("]")
                    val2 = val2.lstrip("[")
                    val2 = val2.replace(", ","")
                    val2 = val2.replace("'","")
                    csv += val1+"$"+entradaAux+"$"+"(q, "+alpha+", "+actual+"; q,"+val2+")\n"
        else:
            break

    #revisando que se haya leido toda la cadena y que la pila solo contenga el simbolo de aceptacion
    #si quedo algun valor en la pila revisar que sean no terminales y que deriven en epsilon
    if len(pila) == 1 and it == len(entrada):
        csv += "#$"+entradaAux+"$(q, "+alpha+", #; f, "+alpha+")\n"
        csv += "$"+"$Aceptacion"
        respuesta.append("La cadena es valida")
        respuesta.append(csv)
        respuesta.append(arbol)
        return respuesta
    else:
        for valor in pila:
            if valor.islower() == True or valor.isdigit() == True:
                respuesta.append("La cadena es invalida")
                csv +="$"+"$Invalida"
                respuesta.append(csv)
                respuesta.append(arbol)
                return respuesta

        while True:
            actual = pila[len(pila)-1]
            noTransiciones = []
            if pila[len(pila)-1] != "#":
                if pila[len(pila)-1] == "epsilon":
                    val1 = str(pila).rstrip("]")
                    val1 = val1.lstrip("[")
                    val1 = val1.replace(", ","")
                    val1 = val1.replace("'","")
                    csv += val1+"$"+entradaAux+"$(q, "+actual+", "+actual+"; q,"+alpha+")\n"
                    pila.pop()
                else:
                    for transicion in automata.transiciones:
                        if transicion.lecturaPila == actual:
                            noTransiciones.append(transicion)

                    if len(noTransiciones) == 0:
                        respuesta.append("La cadena es invalida")
                        csv +="$"+"$Invalida"
                        respuesta.append(csv)
                        respuesta.append(arbol)
                        return respuesta
                    else:
                        val1 = str(pila).rstrip("]")
                        val1 = val1.lstrip("[")
                        val1 = val1.replace(", ","")
                        val1 = val1.replace("'","")
                        auxi = False
                        
                    
                        
                        aux = []
                        pila.pop()
                        cambio = pilaNoTerminales.pop(len(pilaNoTerminales)-1)

                        for valor in noTransiciones:
                            aux = valor.guardarEnPila.split(" ")
                            if aux[0] == "epsilon":
                                auxi = True
                                break
                        if auxi == False:
                            break
                        for val in reversed(valor.guardarEnPila.split(" ")):
                            pila.append(val)
                            if val.islower() == True or val.isdigit() == True:
                                arbol.agregar(val,cambio,"t"+str(idenTer))
                                idenTer += 1
                            else:
                                pilaNoTerminales.append("nt"+str(idenNoTer))
                                arbol.agregar(val,cambio,"nt"+str(idenNoTer))
                                idenNoTer += 1

                        idenAux += 1
                        
                        val2 = str(aux).rstrip("]")
                        val2 = val2.lstrip("[")
                        val2 = val2.replace(", ","")
                        val2 = val2.replace("'","")
                        csv += val1+"$"+entradaAux+"$"+"(q, "+alpha+", "+actual+"; q,"+val2+")\n"
            else:
                break
        
        if len(pila) == 1:
            csv += "#$"+entradaAux+"$(q, "+alpha+", #; f, "+alpha+")\n"
            csv += "$"+"$Aceptacion"
            respuesta.append("La cadena es valida")
            respuesta.append(csv)
            respuesta.append(arbol)
            return respuesta
        else:
            respuesta.append("La cadena es invalida")
            csv +="$"+"$Invalida"
            respuesta.append(csv)
            respuesta.append(arbol)
            return respuesta

def generarCadenasValidas(gramatica,valo):
    #variable que guardara la cadena valida
    cadena = ""
    
    #obteniendo la produccion inicial
    actual = gramatica.no_terminal_inicial

    #generando un terminal random 
    terminal = gramatica.terminales[random.randint(0,(len(gramatica.terminales)-1))]
    
    while True:
        aux = False
        
        #validando si en la produccion actual se encuentra una una que deriva en epsilon o en un solo terminal
        for valor in gramatica.producciones:
            if valor.inicio == actual:
                for derecha in valor.ladoDerecho:
                    if derecha.siguiente == "no":
                        aux = True
                        #agregando el terminal a la cadena
                        if cadena=="":
                            cadena = derecha.terminal
                        else:
                            cadena += derecha.terminal
                    elif derecha.siguiente == "epsilon":
                        aux = True
        if aux == False:
            #verificando si el terminal se encuentra en alguna de las derivaciones de la produccion actual
            for produccion in gramatica.producciones:
                if produccion.inicio == actual:
                    for derecha in produccion.ladoDerecho:
                        if derecha.terminal == terminal:
                            #actualizando el no terminal actual
                            actual = derecha.siguiente
                            #agregando el terminal a la cadena
                            if cadena == "":
                                cadena = derecha.terminal
                            else:
                                cadena += derecha.terminal
                            break
                    break
            #randomizando otro terminal
            terminal = gramatica.terminales[random.randint(0,(len(gramatica.terminales)-1))]
        else:
            break

    #devolviendo la cadena valida
    return cadena

def validarCadenaGramatica(cadena,gramatica):

    #variable que almacenara la ruta en gramatica, afd y el resultado de la validacion
    auxi = []
    
    #variables para almacenar el valor de la ruta en gramatica, afd y el resultado de la validacion
    rutaEnAutomata = ""
    rutaEnGramatica = ""
    validacion = ""
    
    #iterador para comparar con la longitud de la cadena
    iterador = 0

    #obteniendo la produccion inicial
    actual = gramatica.no_terminal_inicial

    while True:
        #validando que el iterador sea menor a la longitud para evitar salirnos del index de la cadena
        if iterador < len(cadena):
            aux = False
            """
            verificando que el terminal de la cadena en la posicion iterador este en alguna de las producciones 
            del no terminal actual
            """
            for produccion in gramatica.producciones:
                if produccion.inicio == actual:
                    for derecha in produccion.ladoDerecho:
                        if derecha.terminal == cadena[iterador]:
                            aux = True
                            #agregando las rutas en afd y gramatica para cada caso particular
                            if derecha.siguiente=="no":
                                if rutaEnAutomata == "":
                                    rutaEnAutomata = actual+",Sumidero,"+derecha.terminal+";"
                                    rutaEnGramatica = actual+" -> "+cadena[0]+"(epsilon) -> "+ cadena[0]
                                else:
                                    rutaEnAutomata = rutaEnAutomata+actual+",Sumidero,"+derecha.terminal+";"
                                    rutaEnGramatica = rutaEnGramatica+" -> "+cadena[:iterador+1]+"(epsilon) -> " + cadena
                            else:
                                if rutaEnAutomata == "":
                                    rutaEnAutomata = actual+","+derecha.siguiente+","+derecha.terminal+";"
                                    rutaEnGramatica = actual+" -> "+derecha.terminal+derecha.siguiente
                                else:
                                    rutaEnAutomata = rutaEnAutomata+actual+","+derecha.siguiente+","+derecha.terminal+";"
                                    rutaEnGramatica = rutaEnGramatica+" -> "+cadena[:iterador+1]+derecha.siguiente
                            actual = derecha.siguiente
                            break
                    break
            #validando si en la produccion actual se encontraba el terminal 
            if aux == True:
                validacion = "Valida"
                #para el caso de que sea un solo terminal en la produccion retornar la cadena valida
                if actual == "no":
                    rutaEnAutomata = rutaEnAutomata.rstrip(";")
                    auxi.append(validacion)
                    auxi.append(rutaEnAutomata)
                    auxi.append(rutaEnGramatica)
                    return auxi
            else:
                #si no se encontro el terminal retornar cadena invalida
                auxi.append("Invalida")
                return auxi
        else:
            break
        iterador = iterador + 1
    
    aux = False
    #luego de terminal de verificar toda la cadena buscar si en la produccion actual esta tiene una que deriva en epsilon
    for produccion in gramatica.producciones:
        if produccion.inicio == actual:
            for derecha in produccion.ladoDerecho:
                if derecha.terminal == "epsilon":
                    aux = True
                    if rutaEnAutomata == "":
                        rutaEnAutomata = actual+","+actual+",epsilon"
                        rutaEnGramatica = actual +" -> (epsilon) -> cadena vacia"
                    else:
                        rutaEnGramatica = rutaEnGramatica+" -> "+cadena+"(epsilon) -> "+cadena                                    
                    break
            break
    if aux == True:
        validacion = "Valida"
    else:
        validacion = "Invalida"
    
    #agregando las rutas en afd, gramatica y la validacion al arreglo de retorno
    rutaEnAutomata = rutaEnAutomata.rstrip(";")
    auxi.append(validacion)
    auxi.append(rutaEnAutomata)
    auxi.append(rutaEnGramatica)
    return auxi

def traduccionHaciaGramatica(automata):
    #creando el nombre de la gramatica traducida
    nombre = automata.nombre+"_GramaticaTraducida"

    #obteniendo los no terminales
    noTerminales = []
    for valor in automata.estados:
        noTerminales.append(valor.nombre)

    #creando el objeto gramatica
    nueva_gramatica = Gramatica(nombre,automata.terminales,noTerminales,automata.estado_inicial,[],[])

    #transformando las transiciones en producciones
    for transicion in automata.transiciones:
        #NT>T NT(Gramatica) ; de NT1 a NT2 con T (AFD) 
        
        aux = False

        for producciones in nueva_gramatica.producciones:
            if producciones.inicio == transicion.inicial:
                aux = True
                break
        
        if aux == True:
            producciones.ladoDerecho.append(LadoDerecho(transicion.valor,transicion.final))
        else:
            nueva_gramatica.producciones.append(Produccion(transicion.inicial,[LadoDerecho(transicion.valor,transicion.final)],"0"))
    
    #transformando el estado de aceptacion en una produccion que deriva en epsilon
    for estado in automata.estados:
        if estado.aceptacion == "1":
            for producciones in nueva_gramatica.producciones:
                aux = False
                if producciones.inicio == estado.nombre:
                    aux = True
                    break
            if aux == True:
                producciones.ladoDerecho.append(LadoDerecho("epsilon","epsilon"))
            else:
                nueva_gramatica.producciones.append(Produccion(estado.nombre,[LadoDerecho("epsilon","epsilon")],"0"))

    #validando si ya se realizo la traduccion    
    aux = False

    for it in range(0,len(gramaticas)):
        if gramaticas[it].nombre == nombre:
            gramaticas[it] = nueva_gramatica
            aux = True
            break 
    
    if aux == False:
        gramaticas.append(nueva_gramatica)

def traduccionHaciaAutomata(gramatica):
    #creando el nombre del nuevo automata
    nombre = gramatica.nombre+"_AutomataTraducido"

    #convirtiendo los no terminales a estados
    estados = []
    for noTerminal in gramatica.no_terminales:
        estados.append(Estado(noTerminal,"0"))

    #creando el objeto AFD
    nuevo_automata = Automata(nombre,gramatica.terminales,estados,gramatica.no_terminal_inicial,[])
   

    #variable para validar la creacion de un estado sumidero
    iterador = 0

    #transformando las producciones que sean disntinas de epsilon y un solo terminal a transiciones
    for producciones in gramatica.producciones:
        for derecha in producciones.ladoDerecho:
            if derecha.siguiente != "no" and derecha.siguiente != "epsilon":
                nuevo_automata.transiciones.append(Transicion(producciones.inicio,derecha.siguiente,derecha.terminal))
            else:
                if derecha.siguiente=="no":
                    iterador = iterador + 1
    
    #verificando la existencia del estado sumidero y creandolo de ser necesario
    if iterador > 0:
        nuevo_automata.estados.append(Estado("Sumidero","1"))
    
    #transformando las producciones que sean de un solo terminal a transiciones hacia el estado sumidero
    for producciones in gramatica.producciones:
        for derecha in producciones.ladoDerecho:
            if derecha.siguiente == "no":
                nuevo_automata.transiciones.append(Transicion(producciones.inicio,"Sumidero",derecha.terminal))
    
    #transformando las producciones que sean epsilon a estados de aceptacion
    for producciones in gramatica.producciones:
        for derecha in producciones.ladoDerecho:
            if derecha.terminal == "epsilon":
                for estado in nuevo_automata.estados:
                    if estado.nombre == producciones.inicio:
                        estado.aceptacion = "1"
                        break
    
    #validando si ya se realizo la traduccion    
    aux = False

    for it in range(0,len(automatas)):
        if automatas[it].nombre == nombre:
            automatas[it] = nuevo_automata
            aux = True
            break 
    
    if aux == False:
        automatas.append(nuevo_automata)
    
def graphviz(afd,nombre):
    #encabezado del archivo .dot
    dot = "digraph G{\nrankdir=LR\n"

    #creando los identificadores del nodo, el valor que tendra el nodo y la forma del nodo
    for estados in afd.estados:
        if estados.aceptacion == "1":
            dot += estados.nombre + " [ label = "+ '"' + estados.nombre + '" shape = "doublecircle" ] \n'
        else:
            dot += estados.nombre + " [ label = "+ '"' + estados.nombre + '" shape = "circle" ] \n'
    
    #creando las aristas que corresponden a cada transicion
    for transiciones in afd.transiciones:
        dot += transiciones.inicial + " -> " + transiciones.final + "[ label = " + '"' + transiciones.valor + '" ]\n'

    #creando la flecha que apunta hacia el estado inicial
    dot += "init [label = " + '"' + "inicio" + '" shape =' + '"' + "plaintext" + '" ]\n' 
    dot += "init -> " + afd.estado_inicial + "\n"
    dot += "}"

    
    #craendo el archivo que almacenara el .dot
    path_dot = "C:\\Users\\chepe\\Desktop\\" + nombre +".dot"
    archivo_dot = open(path_dot,"w")
    archivo_dot.write(dot)
    archivo_dot.close()

    #compilando la imagen generada del .dot
    path_imagen = "C:\\Users\\chepe\\Desktop\\" + nombre +".png"
    comando = "dot " + path_dot + " -Tpng -o " + path_imagen
    os.system(comando)

    #retornando la ruta de la imagen para el reporte correspondiente
    return path_imagen

def menuAFD(nuevo_automata): 
    #limpiar pantalla
    os.system("cls")
    #impresion del menu
    print(" ")
    print("-------------Menu AFD------------")
    print("|                               |")
    print("| 1. Ingresar estado            |")
    print("| 2. Ingresar alfabeto          |")
    print("| 3. Estado inicial             |")
    print("| 4. Estados de aceptacion      |")
    print("| 5. Transiciones               |")
    print("| 6. Ayuda                      |")
    print("| 0. Regresar al menu principal |")
    print("|                               |")
    print("---------------------------------")
    print(" ")

    #lectura del teclado para direccionar a otro menu
    while True:
        lectura = input('Presione el numero de la accion a realizar: ')
        if lectura.isdigit() == True:
            lectura = int(lectura)
            if lectura == 1:
                #capturar el nombre del estado
                estado = input("\nIngrese el estado: ")

                #llamada al metodo para crear un estado
                print(nuevo_automata.crearEstado(estado,"0"))

                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuAFD(nuevo_automata)
            elif lectura == 2:
                #capturar el nombre del terminal
                terminal = input("\nIngrese el terminal: ")

                #llamada al metodo para crear terminales
                print(nuevo_automata.crearTerminal(terminal))

                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuAFD(nuevo_automata)
            elif lectura == 3:
                #capturar el estado inicial
                inicial = input("\nIngrese el estado inicial: ")

                #variable para verificar si el estado existe
                aux = False

                #verificar si el estado existe
                for verificar in nuevo_automata.estados:
                    if verificar.nombre == inicial.upper():
                        aux = True
                
                #retorno de la validacion del estado inicial
                if aux == True:
                    nuevo_automata.estado_inicial = inicial.upper()
                    print("\nSe a establecido el estado inicial\n")
                else:
                    print("\nEl estado ingresado no se encuentra en el AFD\n")

                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuAFD(nuevo_automata)
            elif lectura == 4:
                #capturar el estado de aceptacion
                aceptacion = input("\nIngrese el estado de aceptacion: ")

                #llamada del metodo para cambiar la aceptacion del estado
                print(nuevo_automata.cambiarAceptacion(aceptacion,"1"))
                
                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuAFD(nuevo_automata)
            elif lectura == 5:
                modo = input("\nSeleccione el numero del modo 1 o 2: ")
                if modo == "1":
                    #captura de la transicion
                    transicion = input("\nIngrese la transicion: ")
                    
                    #division en estado inicial, estado final y terminal (EI,EF;T)
                    div = transicion.split(";")
                    estados = div[0].split(",")

                    print(nuevo_automata.crearTransicion(estados[0],estados[1],div[1]) )
                    
                    #limpieza de pantalla
                    while True:
                        print("Presione enter para limpiar la pantalla")
                        limpieza = getch()
                        if limpieza == b'\r':
                            menuAFD(nuevo_automata)
                elif modo == "2":
                    #declaracion de la matriz que almacenara la tabla de transiciones
                    matriz_transiciones = []

                    #declaracion de la fila de cabeceras para la matriz de transiciones  
                    columnas = []

                    #captura de los terminales de la cabecera
                    terminales = input("\nIngrese los terminales: ")

                    #agregando un valor cualquiera para empezar desde 1 la fila de cabeceras
                    columnas.append("NT/T")

                    #agregando los terminales a la fila de cabeceras
                    for valor in terminales.split(","):
                        columnas.append(valor.lower())

                    #agregando la cabecera a la matriz de transiciones
                    matriz_transiciones.append(columnas)

                    #captura de los no terminales que son cabeceras de las filas
                    no_terminales = input("Ingrese los no terminales: ")

                    #captura de los valores internos de la matriz
                    interior = input("Ingrese los simbolos de destino: ")

                    #division de los valores internos de la matriz
                    aux = no_terminales.split(",")
                    particion = interior.split(";")
                    
                    #declaracion de la variable iterativa para recorrer la division
                    it = 0

                    #recorrido de las cabeceras de las filas
                    for noTerminal in aux:
                        
                        #declaracion del arreglo auxiliar que almacenara las filas
                        temp = []
                        
                        #agregando el valor de la cabecera de la fila
                        temp.append(noTerminal.upper())
                        
                        #validando que la variable iterativa no exceda la longitud del arreglo
                        if it < len(particion):

                            #recorriendo los valores internos de la matriz
                            for interior in range(it,len(particion)):
                                valor = particion[it].split(",")
                                for iterador in valor:
                                    temp.append(iterador.upper())
                                it = it + 1
                                break
                        #agregando la nueva fila a la matriz
                        matriz_transiciones.append(temp)

                    #recorrido obteniendo cada conjunto de terminales y no terminales para ingresarlor por el modo1
                    for i in range(1,len(matriz_transiciones)):
                        for j in range(1,len(matriz_transiciones[0])):
                            if matriz_transiciones[i][j] != "":
                                if matriz_transiciones[i][j] != "-":
                                    nuevo_automata.crearTransicion(matriz_transiciones[i][0],matriz_transiciones[i][j],matriz_transiciones[0][j])

                    #limpieza de pantalla
                    print("\nSe han agregado las transiciones")
                    while True:
                        print("\nPresione enter para limpiar la pantalla")
                        limpieza = getch()
                        if limpieza == b'\r':
                            menuAFD(nuevo_automata)
                else:
                    print("\nIngrese unicamente el numero 1 o 2\n")
                    while True:
                        print("\nPresione enter para limpiar la pantalla")
                        limpieza = getch()
                        if limpieza == b'\r':
                            menuAFD(nuevo_automata)
            elif lectura == 6:
                print(ayuda)
                #limpieza de la pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuAFD(nuevo_automata)
            elif lectura == 0:
                menuPrincipal()
            else:
                print("\nIngrese una opcion valida\n")
        else:
            print("\nIngrese una opcion valida \n")

def menuGramatica(nueva_gramatica):
    #limpiar pantalla y mostrar menu
    os.system("cls")
    print(" ")
    print("-----------Menu Gramatica------------")
    print("|                                   |")
    print("| 1. Ingresar NT                    |")
    print("| 2. Ingresar terminal              |")
    print("| 3. NT inicial                     |")
    print("| 4. Producciones                   |")
    print("| 5. Mostrar gramatica transformada |")
    print("| 6. Ayuda                          |")
    print("| 0. Regresar al menu principal     |")
    print("|                                   |")
    print("-------------------------------------")
    print(" ")

    #lectura del teclado para direccionar a otro menu
    while True:
        lectura = input('Presione el numero de la accion a realizar: ')
        if lectura.isdigit() == True:
            lectura = int(lectura)
            if lectura == 1:
                #captura del no terminal
                noTerminal = input("\nIngrese el nombre del no terminal: ")

                #invocando al metodo para la creacion del no terminal
                print(nueva_gramatica.crearNoTerminal(noTerminal))
                
                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuGramatica(nueva_gramatica)
            elif lectura == 2:
                #captura del no terminal
                terminal = input("\nIngrese el nombre del terminal: ")
                
                #llamando al metodo para crear el terminal
                print(nueva_gramatica.crearTerminal(terminal))
                    #crearTerminalGramatica(nueva_gramatica,terminal))

                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuGramatica(nueva_gramatica)
            elif lectura == 3:
                #captura del no terminal inicial
                inicial = input("\nIngrese el valor del no terminal inicial: ")

                #variable para validar la existencia del no terminal
                validar = False

                #recorrido para validar la existencia del no terminal
                for valor in nueva_gramatica.no_terminales:
                    if valor == inicial.upper():
                        validar = True
                
                #retorno de la validacion
                if validar == True:
                    nueva_gramatica.no_terminal_inicial = inicial.upper()
                    print("\nSe ha agregado el no terminal inicial\n")
                else:
                    print("\nEl no terminal ingresado no existe en la gramatica\n")
                
                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuGramatica(nueva_gramatica)
            elif lectura == 4:
                #captura de la produccion
                produccion = input("\nIngrese la produccion: ")
                
                #llamada del metodo para crear una produccion
                print(nueva_gramatica.crearProduccion(produccion))

                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuGramatica(nueva_gramatica)
            elif lectura == 5:
                #verificando que exista alguna produccion que sea recursiva
                aux = False
                for valor in nueva_gramatica.producciones:
                    if valor.recursividad=="1":
                        aux = True

                if aux == True:
                    print("\nGramatica sin transformar:\n")
                    #recorrido para mostrar la gramatica original
                    texto = ""
                    for valor in nueva_gramatica.transformacion:
                        if texto == "":
                            texto = valor.inicio+" -> "
                            for derecha in valor.ladoDerecho:
                                if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                    texto += derecha.terminal+" "+derecha.siguiente+"\n     "
                                else:
                                    texto += derecha.terminal+"\n     "
                            texto = texto.rstrip("     ")
                        else:
                            texto += valor.inicio+" -> "
                            for derecha in valor.ladoDerecho:
                                if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                    texto += derecha.terminal+" "+derecha.siguiente+"\n     "
                                else:
                                    texto += derecha.terminal+"\n     "
                            texto = texto.rstrip("     ")
                    print(texto)
                    print("Gramatica transformada:\n")
                    #recorrido para mostrar la gramatica transformada
                    texto = ""
                    itera = 0
                    for valor in nueva_gramatica.producciones:
                        if texto == "":
                            texto = valor.inicio + " -> "
                            for derecha in valor.ladoDerecho:
                                #validacion para mantener el formato del texto en la impresion 
                                if len(valor.inicio) >= 3: 
                                    itera = 1
                                    if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                        texto += derecha.terminal+" "+derecha.siguiente+"\n       " 
                                    else:
                                        texto+= derecha.terminal+"\n       "
                                else:
                                    itera = 0
                                    if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                        texto += derecha.terminal+" "+derecha.siguiente+"\n     "
                                    else:
                                        texto += derecha.terminal+"\n     "
                            if itera == 0:
                                texto = texto.rstrip("     ")
                            else:
                                texto = texto.rstrip("       ")
                        else:
                            texto += valor.inicio + " -> "
                            for derecha in valor.ladoDerecho:
                                #validacion para mantener el formato del texto en la impresion 
                                if len(valor.inicio) >= 3: 
                                    itera = 1
                                    if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                        texto += derecha.terminal+" "+derecha.siguiente+"\n       " 
                                    else:
                                        texto+= derecha.terminal+"\n       "
                                else:
                                    itera = 0
                                    if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                        texto += derecha.terminal+" "+derecha.siguiente+"\n     "
                                    else:
                                        texto += derecha.terminal+"\n     "
                            if itera == 0:
                                texto = texto.rstrip("     ")
                            else:
                                texto = texto.rstrip("       ")
                    print(texto)    
                else:
                    print("\nNo hay recursividad\n")
                
                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuGramatica(nueva_gramatica)
            elif lectura == 6:
                print(ayuda)
                
                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuGramatica(nueva_gramatica)
            elif lectura == 0:
                menuPrincipal()
            else:
                print("\nIngrese una opcion valida\n")
        else:
            print("\nIngrese una opcion valida \n")

def menuEvaluarCadenas(gramatica):
    #limpiar pantalla y mostrar menu
    os.system("cls")
    print(" ")
    print("-------Menu evaluar cadenas------")
    print("|                               |")
    print("| 1. Solo validar               |")
    print("| 2. Ruta en AFD                |")
    print("| 3. Expandir con gramatica     |")
    print("| 4. Ayuda                      |")
    print("| 0. Regresar al menu principal |")
    print("|                               |")
    print("---------------------------------")
    print(" ")

    #lectura del teclado para direccionar a otro menu
    while True:
        lectura = input('Presione el numero de la accion a realizar: ')
        if lectura.isdigit() == True:
            lectura = int(lectura)
            if lectura == 1:
                #captura de la cadena a validar
                cadena = input("Ingrese la cadena a validar: ")
                
                #almacenando el resultado de la validacion de la cadena
                resultado = validarCadenaGramatica(cadena,gramatica)

                #obteniendo el nombre de la gramatica o automata al cual pertenece la cadena
                div = gramatica.nombre.split("_GramaticaTraducida")
                nombre = ""
                if len(div) == 2:
                    nombre = div[0]
                else:
                    nombre = gramatica.nombre
                
                #guardando la cadena validada
                aux = False
                for valor in cadenas:
                    if valor.identificador == nombre:
                        valor.cadenas.append(Cadena(cadena,resultado[0]))
                        aux = True
                if aux == False:
                    cadenas.append(Evaluacion(nombre,[Cadena(cadena,resultado[0])]))
                print("\nLa cadena es: "+resultado[0])

                #limpieza de pantalla
                while True:
                    print("\nPresione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuEvaluarCadenas(gramatica)
            elif lectura == 2:
                #captura de la cadena a validar
                cadena = input("Ingrese la cadena a validar: ")

                #almacenando la validacion de la cadena
                resultado = validarCadenaGramatica(cadena,gramatica)

                #obteniendo el nombre de la gramatica o automata al cual pertenece la cadena 
                div = gramatica.nombre.split("_GramaticaTraducida")
                nombre = ""
                if len(div) == 2:
                    nombre = div[0]
                else:
                    nombre = gramatica.nombre
                
                #guardando la cadena validada
                aux = False
                for valor in cadenas:
                    if valor.identificador == nombre:
                        valor.cadenas.append(Cadena(cadena,resultado[0]))
                        aux = True
                if aux == False:
                    cadenas.append(Evaluacion(nombre,[Cadena(cadena,resultado[0])]))
                
                print("\nRuta en AFD : "+resultado[1]+" "+resultado[0])
                
                #limpieza de pantalla
                while True:
                    print("\nPresione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuEvaluarCadenas(gramatica)
            elif lectura == 3:
                #obteniendo la cadena a validar
                cadena = input("Ingrese la cadena a validar: ")

                #almacenando el resultado de la validacion
                resultado = validarCadenaGramatica(cadena,gramatica)

                #obteniendo el nombre de la gramatica o automata al cual pertenece la cadena
                div = gramatica.nombre.split("_GramaticaTraducida")
                nombre = ""
                if len(div) == 2:
                    nombre = div[0]
                else:
                    nombre = gramatica.nombre
                
                #guardando la cadena evaluada
                aux = False
                for valor in cadenas:
                    if valor.identificador == nombre:
                        valor.cadenas.append(Cadena(cadena,resultado[0]))
                        aux = True
                if aux == False:
                    cadenas.append(Evaluacion(nombre,[Cadena(cadena,resultado[0])]))
                
                print("\nExpansion en gramatica : "+resultado[2]+" "+resultado[0])

                #limpieza de pantalla
                while True:
                    print("\nPresione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuEvaluarCadenas(gramatica)
            elif lectura == 4:
                print(ayuda)
                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuEvaluarCadenas(gramatica)
            elif lectura == 0:
                menuPrincipal()
            else:
                print("\nIngrese una opcion valida\n")
        else:
            print("\nIngrese una opcion valida \n")

def menuArchivos(repeticion):
    #limpiar pantalla y mostrar menu
    os.system("cls")
    print(" ")
    print("-------Menu manejo de archivos------")
    print("|                                  |")
    print("| 1. Abrir AFD                     |")
    print("| 2. Abrir gramatica               |")
    print("| 3. Guardar AFD                   |")
    print("| 4. Guardar gramatica             |")
    print("| 0. Regresar al menu principal    |")
    print("|                                  |")
    print("------------------------------------")
    print(" ")

    #lectura del teclado para direccionar a otro menu
    while True:
        lectura = input('Presione el numero de la accion a realizar: ')
        if lectura.isdigit() == True:
            lectura = int(lectura)
            if lectura == 1:
                #capturando la ruta del archivo
                path_inicial = input("Ingrese la direccion del archivo .afd: ")
                
                #validando que la extension del archivo sea la correcta
                while True:
                    ruta,nombre = os.path.split(path_inicial)
                    division = nombre.split(".")
                    if division[1] == "afd":
                        break
                    else:
                        path_inicial = input ("\nIngrese la ruta del archivo .afd: ")

                #verificacion del nombre repetido
                aux = False
                for valor in gramaticas:
                    if valor.nombre == division[0]:
                        aux = True
                        break
                for valor in automatas:
                    if valor.nombre == division[0]:
                        aux = True
                        break

                #aumentando el valor para evitar repeticion de nombres
                if aux == True:
                    division[0] = division[0]+"("+str(repeticion)+")"
                    repeticion = repeticion + 1
                
                #creacion del automata
                nuevo_automata = Automata(division[0],[],[],"",[])
    
                #agregando el automata al arreglo
                automatas.append(nuevo_automata)

                #abriendo el archivo y obteniendo su contenido
                archivo_afd = open(path_inicial,"r")
                contenido = archivo_afd.read()

                #recorrido del archivo .afd
                for linea in contenido.split("\n"):

                    #division de la linea en EI,EF,Terminal;aceptacionEI,aceptacionEF
                    valor = linea.split(";")
                    transicion = valor[0].split(",")
                    aceptacion = valor[1].split(",")

                    #validar si el estado inicial ya se encuentra con un valor 
                    if nuevo_automata.estado_inicial == "":
                        nuevo_automata.estado_inicial = transicion[0].upper()
                    
                    #validar existencia del estado creandolo de ser necesario o cambiarle su estado de aceptacion
                    if aceptacion[0].lower() == "true": 
                        validar = nuevo_automata.crearEstado(transicion[0].upper(),"1")
                        if validar == "\nSe ha agregrado el estado al AFD\n":
                            pass
                        else:
                            nuevo_automata.cambiarAceptacion(transicion[0].upper(),"0")
                    else:
                        validar = nuevo_automata.crearEstado(transicion[0].upper(),"0") 
                        if validar == "\nSe ha agregrado el estado al AFD\n":
                            pass
                        else:
                            nuevo_automata.cambiarAceptacion(transicion[0].upper(),"0")
                    
                    if aceptacion[1].lower() == "true": 
                        validar = nuevo_automata.crearEstado(transicion[1].upper(),"1")
                        if validar == "\nSe ha agregrado el estado al AFD\n":
                            pass
                        else:
                            nuevo_automata.cambiarAceptacion(transicion[1].upper(),"1")
                    else:
                        validar = nuevo_automata.crearEstado(transicion[1].upper(),"0") 
                        if validar == "\nSe ha agregrado el estado al AFD\n":
                            pass
                        else: 
                            nuevo_automata.cambiarAceptacion(transicion[0].upper(),"0")

                    #agregando el terminal al automata
                    nuevo_automata.crearTerminal(transicion[2].lower())

                    #creando la transicion y agregandola al terminal
                    nuevo_automata.crearTransicion(transicion[0].upper(),transicion[1].upper(),transicion[2].upper())

                print("Se a cargado el archivo exitosamente")
                #limpieza de pantalla
                while True:
                    print("\nPresione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuArchivos(repeticion)
            elif lectura == 2:
                
                #capturando la ruta del archivo
                path_inicial = input("Ingrese la ruta del archivo .grm: ")

                #validando que la extension del archivo sea la correcta
                while True:
                    ruta,nombre = os.path.split(path_inicial)
                    division = nombre.split(".")
                    if division[1] == "grm":
                        break
                    else:
                        path_inicial = input ("\nIngrese la ruta del archivo .grm: ")
                
                #verificacion del nombre repetido
                aux = False
                for valor in automatas:
                    if valor.nombre == division[0]:
                        aux = True
                        break
                
                for valor in gramaticas:
                    if valor.nombre == division[0]:
                        aux = True
                        break
                
                if aux == True:
                    division[0] = division[0]+"("+str(repeticion)+")"
                    repeticion = repeticion + 1
                
                #creando la gramatica
                nueva_gramatica = Gramatica(division[0],[],[],"",[],[])

                #agregando la gramatica al arreglo 
                gramaticas.append(nueva_gramatica)

                #abriendo el archivo y obteniendo su contenido
                archivo_gramatica = open(path_inicial,"r")
                contenido = archivo_gramatica.read()
                
                #leyendo el contenido del archivo
                for linea in contenido.split("\n"):

                    #dividiendo la produccion en parte izquierda y derecha
                    produccion = linea.split(">")

                    #creando los no terminales y terminales de la gramatica
                    nueva_gramatica.crearNoTerminal(produccion[0])
                    
                    derecha = produccion[1].split(" ")
                    if len(derecha) == 1:
                        if derecha[0] == "epsilon":
                            pass
                        else:
                            nueva_gramatica.crearTerminal(derecha[0])
                    else:
                        if derecha[0].islower() == True:
                            nueva_gramatica.crearTerminal(derecha[0])
                            nueva_gramatica.crearNoTerminal(derecha[1])
                        elif derecha[0].isdigit() == True:
                            nueva_gramatica.crearTerminal(derecha[0])
                            nueva_gramatica.crearNoTerminal(derecha[1])
                        elif derecha[1].islower() == True:
                            nueva_gramatica.crearTerminal(derecha[1])
                            nueva_gramatica.crearNoTerminal(derecha[0])
                        elif derecha[1].isdigit() == True:
                            nueva_gramatica.crearTerminal(derecha[1])
                            nueva_gramatica.crearNoTerminal(derecha[0])

                    #agregando la produccion inicial
                    if nueva_gramatica.no_terminal_inicial == "":
                        nueva_gramatica.no_terminal_inicial = produccion[0].upper()

                    #creando la produccion
                    nueva_gramatica.crearProduccion(linea)

                print("Se a cargado el archivo exitosamente")
                #limpieza de pantalla
                while True:
                    print("\nPresione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuArchivos(repeticion)
            elif lectura == 3:
                #mostrando los nombres de los AFD disponibles
                print("\nAutomatas disponibles: ",end="\n  ")
                for it in range(0,len(automatas)):
                   print(str(it)+ ". "+ automatas[it].nombre,end="\n  ")
                
                #capturando el nombre del automata a guardar
                nombre = input("\nIngrese el nombre del automata a guardar: ")

                #obteniendo el automata correspondiente
                automata = None
                for valor in automatas:
                    if valor.nombre == nombre:
                        automata = valor

                #variable para almacenar el contenido del archivo
                transicionInicial = ""

                #obteniendo los valores de la transicion del no terminal inicial
                for transi in automata.transiciones:
                    if transi.inicial == automata.estado_inicial:
                        transicionInicial = transi.inicial+","+transi.final+","+transi.valor+";"
                        break

                #obteniendo si la transicion inicial son estados de aceptacion o no
                for estado in automata.estados:
                    if transi.inicial == estado.nombre:
                        if estado.aceptacion == "1":
                            transicionInicial = transicionInicial+"true"+","
                            break
                        else:
                            transicionInicial = transicionInicial+"false"+","
                            break
                for estado in automata.estados:
                    if transi.final == estado.nombre:
                        if estado.aceptacion == "1":
                            transicionInicial = transicionInicial+"true\n"
                            break
                        else:
                            transicionInicial = transicionInicial+"false\n"
                            break

                #creando el archivo que almacenara el afd seleccionado
                path_afd = "C:\\Users\\chepe\\Desktop\\"+ automata.nombre +".afd"
                archivo_afd = open(path_afd,"w")

                #cadena que guarda el valor de la transicion inicial
                validar = transi.inicial+","+transi.final+","+transi.valor

                #recorrido para agregar las transiciones restantes
                for tran in automata.transiciones:
                    actual = tran.inicial+","+tran.final+","+tran.valor
                    if validar != actual:
                        transicionInicial = transicionInicial + tran.inicial+","+tran.final+","+tran.valor+";"

                        for estado in automata.estados:
                            if tran.inicial == estado.nombre:
                                if estado.aceptacion == "1":
                                    transicionInicial = transicionInicial+"true"+","
                                else:
                                    transicionInicial = transicionInicial+"false"+","
                
                        for estado in automata.estados:
                            if tran.final == estado.nombre:
                                if estado.aceptacion == "1":
                                    transicionInicial = transicionInicial+"true\n"
                                else:
                                    transicionInicial = transicionInicial+"false\n"
                
                #eliminando el ultimo salto de linea y agregando el contenido del string al archivo 
                archivo_afd.write(transicionInicial.rstrip("\n"))
                
                #cerrando el archivo para dar por concluido el almacenamiento del string
                archivo_afd.close()

                print("\nSe a guardado el archivo del automata seleccionado con exito")

                #limpieza de pantalla
                while True:
                    print("\nPresione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuArchivos(repeticion)
            elif lectura == 4:
                #mostrando los nombres de las gramaticas disponibles
                print("\nGramaticas disponibles: ",end="\n  ")
                for it in range(0,len(gramaticas)):
                   print(str(it)+ ". "+ gramaticas[it].nombre,end="\n  ")
                
                #capturando el nombre de la gramatica a guardar
                nombre = input("\nIngrese el nombre del automata a guardar: ")

                #obteniendo el objeto gramatica seleccionado
                gramatica = None
                for valor in gramaticas:
                    if valor.nombre == nombre:
                        gramatica = valor

                #variable que almacenara el contenido del archivo
                contenido = ""

                #recorrido para obtener el la produccion inicial
                for valor in gramatica.producciones:
                    if valor.inicio == gramatica.no_terminal_inicial:
                        for derecha in valor.ladoDerecho:
                            if contenido == "":
                                if derecha.siguiente != "epsilon" and derecha.siguiente!="no":
                                    contenido = valor.inicio+">"+derecha.terminal+" "+derecha.siguiente+"\n"
                                else:
                                    contenido = valor.inicio+">"+derecha.terminal+"\n"
                            else:
                                if derecha.siguiente != "epsilon" and derecha.siguiente!="no":
                                    contenido = contenido+valor.inicio+">"+derecha.terminal+" "+derecha.siguiente+"\n"
                                else:
                                    contenido = contenido+valor.inicio+">"+derecha.terminal+"\n"
                        break

                #obteniendo el resto de producciones
                for valor in gramatica.producciones:
                    if valor.inicio!=gramatica.no_terminal_inicial:
                        for derecha in valor.ladoDerecho:
                            if derecha.siguiente!="epsilon" and derecha.siguiente!="no":
                                contenido = contenido+valor.inicio+">"+derecha.terminal+" "+derecha.siguiente+"\n"
                            else:
                                contenido = contenido+valor.inicio+">"+derecha.terminal+"\n"

                #creando el arhivo que almacenara la gramatica seleccionada
                path_gramatica = "C:\\Users\\chepe\\Desktop\\"+ gramatica.nombre +".grm"
                archivo_gramatica = open(path_gramatica,"w")
                
                #eliminando el salto de linea final, agregando su contenido al archivo y cerrando el archivo
                archivo_gramatica.write(contenido.rstrip("\n"))
                archivo_gramatica.close()

                print("\nSe a guardado el archivo del automata seleccionado con exito")

                #limpieza de pantalla
                while True:
                    print("\nPresione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuArchivos(repeticion)
            elif lectura == 0:
                menuPrincipal()
            else:
                print("\nIngrese una opcion valida\n")
        else:
            print("\nIngrese una opcion valida \n")

def menuReportes(gramatica,traduccion):
    #limpiar pantalla y mostrar menu
    os.system("cls")
    print(" ")
    print("----------Menu reportes----------")
    print("|                               |")
    print("| 1. Ver detalle                |")
    print("| 2. Generar reporte            |")
    print("| 3. Ayuda                      |")
    print("| 0. Regresar al menu principal |")
    print("|                               |")
    print("---------------------------------")
    print(" ")

    #lectura del teclado para direccionar a otro menu
    while True:
        lectura = input('Presione el numero de la accion a realizar: ')
        if lectura.isdigit() == True:
            lectura = int(lectura)
            if lectura == 1:
                
                nombre = ""
                aux = False
                
                #obteniendo el nombre de la gramatica o automata
                if traduccion == "1":
                    nombre = gramatica.nombre.split("_GramaticaTraducida")
                    aux = True
                else:
                    nombre = gramatica.nombre

                if aux == True:
                    for automata in automatas:
                        if automata.nombre == nombre[0]:
                            break
                else:
                    #si viene una gramatica pura realizar la traduccion
                    traduccionHaciaAutomata(gramatica)
                    for automata in automatas:
                        if automata.nombre == gramatica.nombre+"_AutomataTraducido":
                            break
                
                #obteniendo los estados que son de aceptacion
                aceptacion = []
                for estado in automata.estados:
                    if estado.aceptacion == "1":
                        aceptacion.append(estado.nombre)
                
                #obteniendo todos los estados
                estado = []
                for valor in automata.estados:
                    estado.append(valor.nombre)

                #obteniendo las transiciones del automata
                tran = " {"
                for transicion in automata.transiciones:
                    tran += transicion.inicial+","+transicion.final+","+transicion.valor+"\n         "
                tran = tran.rstrip("\n         ")
                tran += "}"

                #mostrando las partes del automata
                resultado_automata = "\nAutomata:\n"
                resultado_automata += "   \u03A3 = " + str(automata.terminales) + "\n"
                resultado_automata += "   S = " + str(estado) + "\n"
                resultado_automata += "   So = " + automata.estado_inicial + "\n"
                resultado_automata += "   F = " + str(aceptacion) + "\n"
                resultado_automata += "   T = " + tran
                print(resultado_automata)

                #obteniendo las producciones y dandoles el formato establecido
                producciones = ""
                for valor in gramatica.producciones:
                    if producciones == "":
                        producciones = valor.inicio+" -> "
                        for derecha in valor.ladoDerecho:
                            if len(valor.inicio) >= 3: 
                                if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                    producciones += derecha.terminal+" "+derecha.siguiente+"\n               "
                                else:
                                    producciones += derecha.terminal+"\n               " 
                            else:
                                if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                    producciones += derecha.terminal+" "+derecha.siguiente+"\n           "
                                else:
                                    producciones += derecha.terminal+"\n           "
                        producciones = producciones.rstrip("           ")
                    else:
                        producciones += "      "+valor.inicio+" -> "
                        for derecha in valor.ladoDerecho:
                            if len(valor.inicio) >= 3: 
                                if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                    producciones += derecha.terminal+" "+derecha.siguiente+"\n               "
                                else:
                                    producciones += derecha.terminal+"\n               " 
                            else:
                                if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                    producciones += derecha.terminal+" "+derecha.siguiente+"\n           "
                                else:
                                    producciones += derecha.terminal+"\n           "
                        producciones = producciones.rstrip("           ")

                #mostrando las partes de la gramatica
                resultado_gramatica = "Gramatica:\n"
                resultado_gramatica += "   NT = " + str(gramatica.no_terminales) + "\n"
                resultado_gramatica += "   \u03A3 = " + str(gramatica.terminales) + "\n"
                resultado_gramatica += "   Inicial = " + gramatica.no_terminal_inicial + "\n"
                resultado_gramatica += "   Producciones : \n      " + producciones
                print(resultado_gramatica)

                #limpieza de pantalla
                while True:
                    print("\nPresione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuReportes(gramatica,traduccion)
            elif lectura == 2:
                
                nombre = ""
                aux = False
                
                #obteniendo el nombre puro de la gramatica o el automata
                if traduccion == "1":
                    nombre = gramatica.nombre.split("_GramaticaTraducida")
                    aux = True
                else:
                    nombre = gramatica.nombre

                if aux == True:
                    for automata in automatas:
                        if automata.nombre == nombre[0]:
                            break
                else:
                    #si viene una gramatica pura traducirla hacia un automata
                    traduccionHaciaAutomata(gramatica)
                    for automata in automatas:
                        if automata.nombre == gramatica.nombre+"_AutomataTraducido":
                            break
                
                #obteniendo los estados de aceptacion
                aceptacion = []
                for estado in automata.estados:
                    if estado.aceptacion == "1":
                        aceptacion.append(estado.nombre)
                
                #obteniendo los estados
                estado = []
                for valor in automata.estados:
                    estado.append(valor.nombre)

                #obteniendo la ruta de la imagen del automata
                imagen = graphviz(automata,automata.nombre)

                #creando el reporte pdf correspondiente al afd y la gramatica con sus respectivas cadenas
                reporte_pdf = canvas.Canvas(nombre[0]+".pdf")
                reporte_pdf.setTitle("Reporte")
                
                #agregando los valores del automata
                texto = reporte_pdf.beginText(5,800)
                texto.textLine("Automata:")
                texto.textLine("   \u03A3 = " + str(automata.terminales))
                texto.textLine("   S = " + str(estado))
                texto.textLine("   So = " + automata.estado_inicial)
                texto.textLine("   F = " + str(aceptacion))
                reporte_pdf.drawText(texto)

                #agreagando la imagen del automata
                reporte_pdf.drawImage(imagen,5,565,400,150)
                
                #cambiando a una pagina nueva
                reporte_pdf.showPage()

                #agregando los datos de la gramatica
                texto1 = reporte_pdf.beginText(5,800)
                texto1.textLine("Gramatica:")
                texto1.textLine("   NT = " + str(gramatica.no_terminales))
                texto1.textLine("   \u03A3 = " + str(gramatica.terminales))
                texto1.textLine("   Inicial = " + gramatica.no_terminal_inicial)
                texto1.textLine("   Producciones :")
                for valor in gramatica.producciones:
                    for derecha in valor.ladoDerecho:
                        if len(valor.inicio) >= 3: 
                            if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                texto1.textLine("      "+valor.inicio+" -> "+derecha.terminal+" "+derecha.siguiente)
                            else:
                                texto1.textLine("      "+valor.inicio+" -> "+derecha.terminal)
                        else:
                            if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                texto1.textLine("      "+valor.inicio+" -> "+derecha.terminal+" "+derecha.siguiente)
                            else:
                                texto1.textLine("      "+valor.inicio+" -> "+derecha.terminal)

                #verificando si la gramatica tiene recursividad
                aux = False
                for valor in gramatica.producciones:
                    if valor.recursividad == "1":
                        aux = True
                        break
                texto1.textLine(" ")
                if aux == True:
                    texto1.textLine("Gramatica Original:")
                    for valor in gramatica.transformacion:
                        for derecha in valor.ladoDerecho:
                            if derecha.siguiente!="no" and derecha.siguiente!="epsilon": 
                                texto1.textLine("   "+valor.inicio+" -> "+derecha.terminal+" "+derecha.siguiente)
                            else:
                                texto1.textLine("   "+valor.inicio+" -> "+derecha.terminal)
                else:
                    texto1.textLine("La gramatica no tiene recursividad")    
                reporte_pdf.drawText(texto1)

                #cambiando de pagina
                reporte_pdf.showPage()
                texto2 = reporte_pdf.beginText(5,800)
                
                #algoritmo para obtener 3 cadenas validas
                arreglo = []
                iterador1 = 0
                while iterador1<900:
                    if len(arreglo)<3:
                        var = generarCadenasValidas(gramatica,0)
                        aux = False
                        for val in arreglo:
                            if var == val:
                                aux = True
                                break
                        if aux == False:
                            arreglo.append(var)
                    else:
                        break
                    iterador1 += 1
                
                #agregando las cadenas validas automaticas al reporte
                texto2.textLine("Cadenas Validas:")
                for var in arreglo:
                    if var == "epsilon":
                        texto2.textLine("   Cadena vacia")
                    else:
                        texto2.textLine("   "+var)
                texto2.textLine(" ")

                #agregando las cadenas invalidas automaticas al reporte
                texto2.textLine("Cadenas Invalidas:")
                for var in arreglo:
                    if len(var) == 1:
                        texto2.textLine("   Cadena vacia")
                    else:
                        texto2.textLine("   "+var[:len(var)-1])
                texto2.textLine(" ")
                
                #agregando las cadenas evaluadas correspondientes a la gramatica o automata
                texto2.textLine("Cadenas evaluadas:")
                if traduccion == "1":
                    for val in cadenas:
                        if val.identificador == nombre[0]:
                            for var in range(len(val.cadenas)):
                                if var < 10:
                                    texto2.textLine("   "+val.cadenas[var].valor+" "+val.cadenas[var].validacion)
                else:
                    for val in cadenas:
                        if val.identificador == nombre:
                            for var in range(len(val.cadenas)):
                                if var < 10:
                                    texto2.textLine("   "+val.cadenas[var].valor+" "+val.cadenas[var].validacion)
                reporte_pdf.drawText(texto2)    
                reporte_pdf.save()
                print("\nSe a generado el pdf con exito")
                
                #limpieza de pantalla
                while True:
                    print("\nPresione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuReportes(gramatica,traduccion)
            elif lectura == 3:
                print(ayuda)
                #limpieza de pantalla
                while True:
                    print("\nPresione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuReportes(gramatica,traduccion)
            elif lectura == 0:
                menuPrincipal()
            else:
                print("\nIngrese una opcion valida\n")
        else:
            print("\nIngrese una opcion valida \n")   

def menuPrincipal():
    #limpiar pantalla y mostrar menu
    os.system("cls")
    print(" ")
    print("-----Menu Principal------")
    print("|                       |")
    print("| 1. Crear AFD          |")
    print("| 2. Crear Gramatica    |")
    print("| 3. Evaluar cadenas    |")
    print("| 4. Reportes           |")
    print("| 5. Manejo de archivos |")
    print("| 6. Caratula           |")
    print("| 0. Salir              |")
    print("|                       |")
    print("-------------------------")
    print(" ")
    #lectura del teclado para direccionar a otro menu
    while True:
        lectura = input('Presione el numero de la accion a realizar: ')
        if lectura.isdigit() == True:
            lectura = int(lectura)
            if lectura == 1:
                print("\nListado de automatas existentes: ",end="\n  ")
                
                if len(automatas) == 0:
                    print("Aun no existen automatas en el sistema\n")
                else:
                    #mostrando solo los automatas que no se han traducido
                    for valor in automatas:
                        val = valor.nombre.split("_AutomataTraducido")
                        if len(val)<2:
                            print("- "+valor.nombre,end="\n  ")

                #captura del nombre del automata
                nombre = input("\nEscriba el nombre de un AFD del listado, o un nombre distinto para crear un nuevo AFD: ")
    
                automata = None
                #verificacion del nombre del automata
                for valor in automatas:
                    if valor.nombre == nombre:
                        automata = valor
                        break

                if automata == None:
                    #creacion del automata
                    nuevo_automata = Automata(nombre,[],[],"",[])
    
                    #agregando el automata al arreglo
                    automatas.append(nuevo_automata)
                    menuAFD(nuevo_automata)
                else:
                    menuAFD(automata)
            elif lectura == 2:
                print("\nListado de gramaticas existentes: ",end="\n  ")
                
                if len(gramaticas) == 0:
                    print("Aun no existen gramaticas en el sistema\n")
                else:
                    #mostrando solo las gramaticas que no se han traducido
                    for valor in gramaticas:
                        val = valor.nombre.split("_GramaticaTraducida")
                        if len(val)<2:
                            print("- "+valor.nombre,end="\n  ")

                #captura del nombre del automata
                nombre = input("\nEscriba el nombre de una gramatica del listado, o un nombre distinto para crear una nueva gramatica: ")
    
                gramatica = None

                #verificacion del nombre del automata
                for valor in gramaticas:
                    if valor.nombre == nombre:
                        gramatica = valor
                        break

                if gramatica == None:
                    #creacion de la gramatica
                    nueva_gramatica = Gramatica(nombre,[],[],"",[],[])
    
                    #agregando el automata al arreglo
                    gramaticas.append(nueva_gramatica)
                    menuGramatica(nueva_gramatica)
                else:
                    menuGramatica(gramatica)
            elif lectura == 3:
                print("\nListado de gramaticas existentes: ",end="\n  ")
               
                if len(gramaticas) == 0 and len(automatas)==0:
                    print("Aun no existen gramaticas en el sistema\n")
                else:
                    #mostrando las gramaticas y automatas que no se han traducido
                    for valor in gramaticas:
                        val = valor.nombre.split("_GramaticaTraducida")
                        if len(val) < 2:
                            print("- "+valor.nombre,end="\n  ")
                    for valor in automatas:
                        val = valor.nombre.split("_AutomataTraducido")
                        if len(val) < 2:
                            print("- "+valor.nombre,end="\n  ")

                    #captura del nombre del automata
                    nombre = input("\nEscriba el nombre de una gramatica del listado, para evaluar la cadena: ")
    
                    gramatica = None

                    #verificacion del nombre de la gramatica
                    for valor in gramaticas:
                        if valor.nombre == nombre:
                            gramatica = valor
                            break

                    if gramatica == None:
                        #traduccion de hacia gramatica
                        for valor in automatas:
                            if valor.nombre == nombre:
                                traduccionHaciaGramatica(valor)
                                break
                        for valor in gramaticas:
                            if valor.nombre == nombre+"_GramaticaTraducida":
                                menuEvaluarCadenas(valor)
                                break
                    else:
                        menuEvaluarCadenas(gramatica)
            elif lectura == 4:
                print("\nListado de gramaticas existentes: ",end="\n  ")
               
                if len(gramaticas) == 0 and len(automatas)==0:
                    print("Aun no existen gramaticas en el sistema\n")
                else:
                    #mostrando solo las gramaticas y automatas que no se han traducido
                    for valor in gramaticas:
                        val = valor.nombre.split("_GramaticaTraducida")
                        if len(val) < 2:
                            print("- "+valor.nombre,end="\n  ")
                    for valor in automatas:
                        val = valor.nombre.split("_AutomataTraducido")
                        if len(val) < 2:
                            print("- "+valor.nombre,end="\n  ")

                    #captura del nombre del automata
                    nombre = input("\nEscriba el nombre de una gramatica del listado para generar los reportes: ")
                    
                    gramatica = None

                    #verificacion del nombre de la gramatica
                    for valor in gramaticas:
                        if valor.nombre == nombre:
                            gramatica = valor
                            break

                    if gramatica == None:
                        #traduccion hacia gramatica
                        for valor in automatas:
                            if valor.nombre == nombre:
                                traduccionHaciaGramatica(valor)
                                break

                        for valor in gramaticas:
                            if valor.nombre == nombre+"_GramaticaTraducida":
                                menuReportes(valor,"1")
                                break
                    else:
                        menuReportes(gramatica,"0")
            elif lectura == 5:
                menuArchivos(repeticion)
            elif lectura == 6:
                caratula()
            elif lectura == 0:
                print("\nHasta la proxima c:\n")
                exit(0)
            else:
                print("\nIngrese una opcion valida\n")
        else:
            print("\nIngrese una opcion valida \n")

def menuGramaticaTipo2(gramatica2):
    #limpiar pantalla y mostrar menu
    os.system("cls")
    print(" ")
    print("----------Menu Gramatica---------")
    print("|                               |")
    print("| 1. Ingresar terminales        |")
    print("| 2. Ingresar no terminales     |")
    print("| 3. Ingresar producciones      |")
    print("| 4. Borrar producciones        |")
    print("| 5. No terminal inicial        |")
    print("| 0. Regresar al menu principal |")
    print("|                               |")
    print("---------------------------------")
    print(" ")
    #lectura del teclado para direccionar a otro menu
    while True:
        lectura = input('Presione el numero de la accion a realizar: ')
        if lectura.isdigit() == True:
            lectura = int(lectura)
            if lectura == 1:
                #captura del terminal
                terminal = input("Ingrese el valor del terminal: ")

                #invocacion del metodo para crear un terminal
                print(gramatica2.crearTerminal(terminal))

                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuGramaticaTipo2(gramatica2)
            elif lectura == 2:
                #captura del no terminal
                noTerminal = input("Ingrese el valor del no terminal: ")

                #invocacion del metodo para crear un no terminal
                print(gramatica2.crearNoTerminal(noTerminal))

                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuGramaticaTipo2(gramatica2)
            elif lectura == 3:
                #captura de la produccion
                produccion = input("Ingrese el valor de la produccion: ")

                #invocacion del metodo para crear una produccion
                print(gramatica2.crearProduccion(produccion))

                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuGramaticaTipo2(gramatica2)
            elif lectura == 4:
                #captura de la produccion
                produccion = input("Ingrese el valor de la produccion: ")

                #invocacion del metodo para crear una produccion
                print(gramatica2.eliminarProduccion(produccion))

                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuGramaticaTipo2(gramatica2)
            elif lectura == 5:
                #captura del no terminal
                noTerminal = input("Ingrese el valor del no terminal inicial: ")

                #invocacion del metodo para crear una produccion
                print(gramatica2.modificarInicial(noTerminal))

                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuGramaticaTipo2(gramatica2)
            elif lectura == 0:
                menuPrincipalTipo2()
            else:
                print("\nIngrese una opcion valida\n")
        else:
            print("\nIngrese una opcion valida \n")

def menuEvaluarCadenaTipo2(automata,response):
    #limpiar pantalla y mostrar menu
    os.system("cls")
    print(" ")
    print("-------Menu evaluar cadenas------")
    print("|                               |")
    print("| 1. Ingresar cadena            |")
    print("| 2. Resultado                  |")
    print("| 3. Reporte                    |")
    print("| 0. Regresar al menu principal |")
    print("|                               |")
    print("---------------------------------")
    print(" ")
    #lectura del teclado para direccionar a otro menu
    while True:
        lectura = input('Presione el numero de la accion a realizar: ')
        if lectura.isdigit() == True:
            lectura = int(lectura)
            if lectura == 1:
                cadena = input("Escriba la cadena a validar: ")
                response = validarCadenaTipo2(automata,cadena)
                print(response[0])
                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuEvaluarCadenaTipo2(automata,response)
            elif lectura == 2:
                if response[0] == "La cadena es invalida":
                    print("No se puede generar el arbol, por que la cadena es invalida")
                else:
                    grafo = response[2].generarGrafo()
                    path_dot = "C:\\Users\\chepe\\Desktop\\" + automata.nombre +".dot"
                    archivo_dot = codecs.open(path_dot,"w","utf-8")
                    archivo_dot.write(grafo)
                    archivo_dot.close()
                    
                    path_imagen = "C:\\Users\\chepe\\Desktop\\" + automata.nombre +".png"
                    comando = "dot " + path_dot + " -Tpng -o " + path_imagen
                    os.system(comando)
                    print("Se a generado el arbol de derivacion exitosamente")
                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuEvaluarCadenaTipo2(automata,response)
            elif lectura == 3:
                path_csv = "C:\\Users\\chepe\\Desktop\\" + automata.nombre +".csv"
                archivo_csv = codecs.open(path_csv,"w","utf-8")
                archivo_csv.write(response[1])
                archivo_csv.close()
                print("Se a generado el archivo csv exitosamente")
                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuEvaluarCadenaTipo2(automata,response)
            elif lectura == 0:
                menuPrincipalTipo2()
            else:
                print("\nIngrese una opcion valida\n")
        else:
            print("\nIngrese una opcion valida \n")

def menuPrincipalTipo2():
    #limpiar pantalla y mostrar menu
    os.system("cls")
    print(" ")
    print("------------Menu Principal-----------")
    print("|                                   |")
    print("| 1. Ingresar / modificar gramatica |")
    print("| 2. Generar automata de pila       |")
    print("| 3. Visualizar automata            |")
    print("| 4. Validar Cadena                 |")
    print("| 5. Regresar a la caratula         |")
    print("| 0. Salir                          |")
    print("|                                   |")
    print("-------------------------------------")
    print(" ")
    #lectura del teclado para direccionar a otro menu
    while True:
        lectura = input('Presione el numero de la accion a realizar: ')
        if lectura.isdigit() == True:
            lectura = int(lectura)
            if lectura == 1:
                print("\nListado de gramaticas disponibles:")

                if len(gramaticas2)==0:
                    print("   Aun no existen gramaticas en el sistema\n")
                else:
                    gramaticas = ""
                    #mostrando las gramaticas disponibles
                    for valor in gramaticas2:
                        if gramaticas == "":
                            gramaticas = "   "+valor.nombre+"\n"
                        else:
                            gramaticas += "   "+valor.nombre+"\n"
                    print(gramaticas)

                #captura del nombre del automata
                nombre = input("Escriba el nombre de una gramatica del listado, o un nombre distinto para crear una nueva gramatica: ")
    
                gramatica = None

                #verificacion del nombre del automata
                for valor in gramaticas2:
                    if valor.nombre == nombre:
                        gramatica = valor
                        break

                if gramatica == None:
                    #creacion de la gramatica
                    nueva_gramatica = Gramatica2(nombre,[],[],"",[])
    
                    #agregando la gramatica al arreglo
                    gramaticas2.append(nueva_gramatica)

                    menuGramaticaTipo2(nueva_gramatica)
                else:
                    menuGramaticaTipo2(gramatica)
            elif lectura == 2:
                print("\nListado de gramaticas disponibles:")

                if len(gramaticas2)==0:
                    print("   Aun no existen gramaticas en el sistema\n")
                else:
                    #mostrando las gramaticas disponibles
                    gramatica = ""
                    for valor in gramaticas2:
                        if gramatica == "":
                            gramatica = "   "+valor.nombre+"\n"
                        else:
                            gramatica += "   "+valor.nombre+"\n"
                    print(gramatica)

                    #captura del nombre del automata
                    nombre = input("Escriba el nombre de una gramatica del listado: ")
    
                    gramatica = None

                    #verificacion del nombre del automata
                    for valor in gramaticas2:
                        if valor.nombre == nombre:
                            gramatica = valor
                            break

                    if gramatica == None:
                        print("El nombre ingresado no existe en el listado")
                    else:
                        #variable que almacenara los simbolos de la pila
                        simbolos = []

                        #recorridos para agregar los simbolos de la pila
                        for valor in gramatica.terminales:
                            simbolos.append(valor)
                        for valor in gramatica.noTerminales:
                            simbolos.append(valor)
                        simbolos.append("#")

                        #creando el objeto del automata de pila asociado
                        nuevo_automata = AutomataP(gramatica.nombre,[],gramatica.noTerminalInicial,gramatica.terminales,simbolos,[])

                        #validando la existencia del automata de pila en el arreglo
                        for it in range(len(automatasDePila)):
                            if automatasDePila[it].nombre == gramatica.nombre:
                                automatasDePila.pop(it)
                                break

                        automatasDePila.append(nuevo_automata)
                        nuevo_automata.crearEstados()
                        print(nuevo_automata.crearTransiciones(gramatica))
                        
                #limpieza de pantalla
                while True:
                    print("Presione enter para limpiar la pantalla")
                    limpieza = getch()
                    if limpieza == b'\r':
                        menuPrincipalTipo2()
            elif lectura == 3:
                print("\nListado de automatas disponibles:")

                if len(automatasDePila)==0:
                    print("   Aun no existen automatas en el sistema\n")
                else:
                    #mostrando las gramaticas disponibles
                    gramatica = ""
                    for valor in automatasDePila:
                        if gramatica == "":
                            gramatica = "   "+valor.nombre+"\n"
                        else:
                            gramatica += "   "+valor.nombre+"\n"
                    print(gramatica)

                    #captura del nombre del automata
                    nombre = input("Escriba el nombre de un automata del listado: ")
    
                    automata = None

                    #verificacion del nombre del automata
                    for valor in automatasDePila:
                        if valor.nombre == nombre:
                            automata = valor
                            break

                    if automata == None:
                        print("El nombre ingresado no existe en el listado")
                    else:
                        print("Sextupla del automata: ")
                        print("   S: [i, p, q, f]")
                        print("   \u03A3: "+str(automata.alfabeto))
                        print("   \u0393: "+str(automata.simbolosPila))
                        print("   L: i")
                        print("   F: f")
                        print("   T:",end=" ")
                        trans = "{"
                        for tran in automata.transiciones:
                            trans += tran.actual+","+tran.entrada+","+tran.lecturaPila+";"+tran.nuevoEstado+","+tran.guardarEnPila+"\n       "
                        trans = trans.rstrip("\n       ")
                        trans += "}"
                        print(trans)

                        #craendo el archivo que almacenara el .dot
                        grafo = automata.generarGrafo()
                        #path_dot = os.path.join(ruta,automata.nombre+".dot")
                        path_dot = "C:\\Users\\chepe\\Desktop\\" + nombre +".dot"
                        archivo_dot = codecs.open(path_dot,"w","utf-8")
                        archivo_dot.write(grafo)
                        archivo_dot.close()

                        #compilando la imagen generada del .dot
                        #path_imagen = os.path.join(ruta,automata.nombre+".png") 
                        path_imagen = "C:\\Users\\chepe\\Desktop\\" + nombre +".png"
                        comando = "dot " + path_dot + " -Tpng -o " + path_imagen
                        os.system(comando)
                        os.system(path_imagen)
                    
                    #limpieza de pantalla
                    while True:
                        print("Presione enter para limpiar la pantalla")
                        limpieza = getch()
                        if limpieza == b'\r':
                            menuPrincipalTipo2()
            elif lectura == 4:
                print("\nListado de automatas disponibles:")

                if len(automatasDePila)==0:
                    print("   Aun no existen automatas en el sistema\n")
                else:
                    #mostrando las gramaticas disponibles
                    gramatica = ""
                    for valor in automatasDePila:
                        if gramatica == "":
                            gramatica = "   "+valor.nombre+"\n"
                        else:
                            gramatica += "   "+valor.nombre+"\n"
                    print(gramatica)

                    #captura del nombre del automata
                    nombre = input("Escriba el nombre de un automata del listado: ")
    
                    automata = None

                    #verificacion del nombre del automata
                    for valor in automatasDePila:
                        if valor.nombre == nombre:
                            automata = valor
                            break

                    if automata == None:
                        print("El nombre ingresado no existe en el listado")
                        
                        #limpieza de pantalla
                        while True:
                            print("Presione enter para limpiar la pantalla")
                            limpieza = getch()
                            if limpieza == b'\r':
                                menuPrincipalTipo2()
                    else:
                        menuEvaluarCadenaTipo2(automata,[])
            elif lectura == 5:
                caratula()
            elif lectura == 0:
                print("\nHasta la proxima c:\n")
                exit(0)
            else:
                print("\nIngrese una opcion valida\n")
        else:
            print("\nIngrese una opcion valida \n")

def caratula():
    #mostrar datos, recibir un enter y enviar al menu principal
    os.system("cls")
    print(" ")
    print("----------Datos del estudiante----------")
    print("|                                      |")
    print("| Lenguajes formales y de programacion |")
    print("|              Seccion: B-             |")
    print("|           Carne: 201700965           |")
    print("|                                      |")
    print("----------------------------------------")
    print(" ")
    input("Presione enter para continuar")
    #mostrar datos, recibir un enter y enviar al menu principal
    os.system("cls")
    print(" ")
    print("-------Menu eleccion-------")
    print("|                         |")
    print("| 1. Gramaticas regulares |")
    print("| 2. Gramaticas tipo 2    |")
    print("| 0. Salir                |")
    print("|                         |")
    print("---------------------------")
    print(" ")
    #lectura del teclado para direccionar a otro menu
    while True:
        lectura = input('Presione el numero de la accion a realizar: ')
        
        if lectura.isdigit() == True:
            lectura = int(lectura)
            if lectura == 1:
                menuPrincipal()
            elif lectura == 2:
                menuPrincipalTipo2()
            elif lectura == 0:
                print("\nHasta la proxima c:\n")
                exit(0)
            else:
                print("\nIngrese una opcion valida\n")
        else:
            print("\nIngrese una opcion valida\n")

caratula()