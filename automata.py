class Automata():

    def __init__(self,nombre,terminales,estados,estado_inicial,transiciones):
        self.nombre = nombre
        self.terminales = terminales
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.transiciones = transiciones

    def crearTerminal(self,terminal):
        #declaracion de la variable para validar su existencia
        aux = True

        #verificar si el nombre del terminal ya se encuentra en el AFD
        for validar in self.terminales:
            if validar == terminal.lower():
                aux = False
        for validar in self.estados:
            if valida.nombre.lower() == terminal.lower():
                aux = False 

        #retorno de la validacion del terminal
        if aux == True:
            self.terminales.append(terminal.lower())
            return"\nSe ha agregrado el terminal al AFD\n"
        else:
            return"\nEl terminal ingresado ya se encuentra en el AFD\n"

    def cambiarAceptacion(self,noTerminal,estado):
        #variable para verificar si el estado existe
        aux = False

        #verificar si el estado existe y cambiarlo a estado de aceptacion
        for valor in self.estados:
            if valor.nombre == noTerminal.upper():
                valor.aceptacion = estado
                aux = True
                
        #retorno de la validacion del estado de aceptacion
        if aux == True:
            return"\nSe a establecido el estado de aceptacion\n"
        else:
            return"\nEl estado ingresado no se encuentra en el AFD\n"

    def crearEstado(self,valor,aceptacion):

        #declaracion de la variable para validar su existencia
        aux = True

        #verificar si el valor del estado ingresado ya se encuentra en el AFD
        for validar in self.estados:
            if validar.nombre == valor.upper():
                aux = False
        for validar in self.terminales:
            if validar == valor.lower():
                aux = False

        #retorno de la verificacion del estado
        if aux == True:
            self.estados.append(Estado(valor.upper(),aceptacion))
            return"\nSe ha agregrado el estado al AFD\n"
        else:
            return"\nEl estado ingresado ya se encuentra en el AFD\n"

    def crearTransicion(self,inicio,fin,terminal):
        #variable para validar
        validar = True
        validar1 = False
        validar2 = False
        validar3 = False

        #recorrido para validar la existencia de los estados
        for valor in self.estados:
            if inicio.upper() == valor.nombre:
                validar1 = True
                    
        for valor in self.estados:
            if fin.upper() == valor.nombre:
                validar2 = True

        #validacion de la existencia de los estados
        if validar1== False or validar2 == False:
            return"\nLos estados ingresados no se encuentran en el AFD\n"
        else:
            #recorrido para validar la existencia del terminal
            for valor in self.terminales:
                if valor == terminal.lower():
                    validar3 = True
                                
            #validacion del terminal
            if validar3 == False:
                return"\nEl terminal no se encuentra en el AFD\n"
            else:
                #recorrido para validar que no exista una transicion desde un estado con el mismo terminal 
                for tran in self.transiciones:
                    if tran.valor == terminal and inicio == tran.inicial:
                        validar = False

                #retorno de la validacion final
                if validar == True:
                    transicion = Transicion(inicio.upper(),fin.upper(),terminal.lower())
                    self.transiciones.append(transicion)
                    return"\nSe ha agregado la transicion\n"
                else:
                    return"\nLos estados solo pueden tener una transicion con cada terminal\n"    

class Estado():
    def __init__(self,nombre,aceptacion):
        self.nombre = nombre
        self.aceptacion = aceptacion

class Transicion():
    def __init__(self,inicial,final,valor):
        self.inicial = inicial
        self.final = final
        self.valor = valor
