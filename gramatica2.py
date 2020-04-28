import string
    
class Gramatica2():
    

    def __init__(self,nombre,terminales,noTerminales,noTerminalInicial,producciones):
        self.nombre = nombre
        self.terminales = terminales
        self.noTerminales = noTerminales
        self.noTerminalInicial = noTerminalInicial
        self.producciones = producciones

    def crearTerminal(self,terminal):
        #variable para validar la existencia del terminal
        aux = False

        #recorrido para validar la existencia del terminal
        if terminal.lower() in self.terminales:
            aux = True
        
        #verificacion de la validacion
        if aux:
            return"El terminal ya se encuentra en la gramatica"
        else:
            #agregando el terminal a la gramatica
            self.terminales.append(terminal.lower())
            return"El terminal a sido ingresado exitosamente"

    def crearNoTerminal(self,noTerminal):
        mayusculas = string.ascii_uppercase

        #variable para validar la existencia del no terminal
        aux = False

        for it in mayusculas:
            if noTerminal.startswith(it):
                aux = True

        if aux:
            aux = False
            #recorrido para validar la existencia del no termianl
            if noTerminal.upper() in self.noTerminales:
                aux = True
            
            #verificacion de la validacion
            if aux:
                return"El no terminal ya se encuentra en la gramatica"
            else:
                self.noTerminales.append(noTerminal)
                return"El no terminal a sido ingresado con exito" 
        else:
            return"Los no terminales solo pueden empezar con letra mayuscula"
   
    def removerRecursividad(self,inicial,derecha):
        #variable para validar la existencia de la produccion sin recursividad
        aux = False

        #variable con el nuevo no terminal
        nuevoNoTerminal = inicial+"_P"

        #verificando si ya existe una produccion con el no terminal inicial
        for valor in self.producciones:
            if valor.inicial == nuevoNoTerminal:
                aux = True
                break
        
        if aux:
            aux = False

            #creando la nueva produccion
            derecha = derecha[2:len(derecha)]
            derecha += " "+nuevoNoTerminal

            #verificando que la produccion no este repetida
            if derecha in valor.ladoDerecho:
                aux = True
            
            if aux:
                return"La produccion ya se encuentra en la gramatica"
            else:
                #agregando el lado derecho de la produccion
                valor.ladoDerecho.append(derecha)

                #modificando la produccion asociada
                for valor in self.producciones:
                    if valor.inicial == inicial:
                        for it in range(len(valor.ladoDerecho)):
                            #verificando que la produccion asociada no haya sido modificada anteriormente
                            if valor.ladoDerecho[it].endswith(nuevoNoTerminal) == False:
                                valor.ladoDerecho[it] += " "+nuevoNoTerminal
                        break
                
                return"Se a creado la produccion"
        else:
            #creando la nueva produccion
            derecha = derecha[2:len(derecha)]
            derecha += " "+nuevoNoTerminal

            #agregando el no terminal y la produccion
            self.noTerminales.append(nuevoNoTerminal)
            self.producciones.append(Produccion2(nuevoNoTerminal,[derecha,"epsilon"]))

            #modificando la produccion asociada
            for valor in self.producciones:
                if valor.inicial == inicial:
                    for it in range(len(valor.ladoDerecho)):
                        #verificando que la produccion asociada no haya sido modificada anteriormente
                        if valor.ladoDerecho[it].endswith(nuevoNoTerminal) == False:
                            valor.ladoDerecho[it] += " "+nuevoNoTerminal
                    break

            return"Se a creado la produccion"

    def crearProduccion(self,produccion):
        #variable para validar la existencia de los terminales y no terminales
        aux = False

        #division de la produccion en lado izquierdo y lado derecho
        produccion = produccion.split(">")
        inicial = produccion[0].rstrip(" ")
        derecha = produccion[1].lstrip(" ")

        #validando la existencia del no terminal inicial
        if inicial in self.noTerminales:
            aux = True
        
        if aux:
            mayusculas = string.ascii_uppercase

            #variables para recorrer el arreglo, validar recursividad por la izquierda y 
            #la existencia de terminales y no terminales del lado derecho de la produccion
            it = 0
            recursividad = 0
            aux = False

            #conviertiendo el string en un arreglo
            der = derecha.split(" ")

            #validacion de la existencia de todos los terminales y no terminales del lado derecho
            while it < len(der):
                aux = False

                #verificando si es un terminal                
                if der[it].islower() or der[it].isdigit():
                    if der[it] in self.terminales:
                        aux = True
                #verificando si es un no terminal
                else:
                    if der[it] in self.noTerminales:
                        aux = True

                #verificando si la produccion es recursiva por la izquierda
                if der[it] in mayusculas:
                    if it == 0 and der[it] == inicial:
                        recursividad = 1

                #validando que el valor actual si exista en los terminales o no terminales
                if aux == False:
                    break

                #aumento del iterador
                it += 1

            if aux:
                if recursividad == 1:
                    #invocando el metodo para eliminar la recursividad
                   return self.removerRecursividad(inicial,derecha)
                else:
                    #variables para almacenar la produccion recursiva asociada,
                    #existencia de una produccion con el no terminal inicial,
                    #creacion del nuevo no terminal recursivo asociado
                    auxi = False
                    aux = False
                    nuevoNoTerminal = inicial+"_P"

                    #busqueda de produccion recursiva asociada
                    for asociada in self.producciones:
                        if asociada.inicial == nuevoNoTerminal:
                            auxi = True
                            break

                    #busqueda de produccion con el no terminal inicial
                    for valor in self.producciones:
                        if valor.inicial == inicial:
                            aux = True
                            break

                    if aux:
                        if auxi:
                            aux = False

                            #modificando el lado derecho de la produccion recursiva asociada
                            derecha +=" "+nuevoNoTerminal

                            #busqueda para evitar duplicidad
                            for derecho in valor.ladoDerecho:
                                if derecho == derecha:
                                    aux = True
                                    break

                            if aux:
                                return"La produccion ya se encuentra en la gramatica"
                            else:
                                #agregando la produccion
                                valor.ladoDerecho.append(derecha)
                                return"Se a creado la produccion"
                        else:
                            aux = False

                            #busqueda para evitar duplicidad
                            for derecho in valor.ladoDerecho:
                                if derecho == derecha:
                                    aux = True
                                    break

                            if aux:
                                return"La produccion ya se encuentra en la gramatica"
                            else:
                                #agregando la produccion
                                valor.ladoDerecho.append(derecha)
                                return"Se a creado la produccion"
                    else:
                        if auxi:
                            #modificando el lado derecho de la produccion
                            derecha += " "+nuevoNoTerminal

                            self.producciones.append(Produccion2(inicial,[derecha]))
                            return"Se a creado la produccion"
                        else:
                            self.producciones.append(Produccion2(inicial,[derecha]))
                            return"Se a creado la produccion"
            else:
                return"Alguno de los terminales o no terminales del lado derecho de la produccion no existe"
        else:
            return"El no terminal inicial no se encuentra en la gramatica"

    def eliminarProduccion(self,produccion):
        #variable para validar la existencia de la produccion
        aux = False
        
        #separacion de la produccion en lado izquierdo y derecho
        produccion = produccion.split(">")
        inicial = produccion[0].rstrip(" ")
        derecha = produccion[1].lstrip(" ")

        #recorrido para validar la existencia del no terminal inicial
        for valor in self.producciones:
            if valor.inicial == inicial:
                aux = True
                break

        if aux:
            aux = False
            #recorrido para validar la existencia del lado derecho de la produccion
            for derecho in valor.ladoDerecho:
                if derecho == derecha:
                    aux = True
                    break
            if aux:
                valor.ladoDerecho.remove(derecho)
                return"Se a eliminado la produccion de la gramatica"
            else:
                return"La produccion no existe en la gramatica"     
        else:
            return"La produccion no existe en la gramatica"

    def modificarInicial(self,inicial):
        aux = False

        if inicial in self.noTerminales:
            aux = True
        
        if aux:
            self.noTerminalInicial = inicial 
            return"Se a modificado el no terminal inicial"
        else:
            return"El no terminal ingresado no se encuentra en la gramatica"

class Produccion2():
    def __init__(self,inicial,ladoDerecho):
        self.inicial = inicial
        self.ladoDerecho = ladoDerecho