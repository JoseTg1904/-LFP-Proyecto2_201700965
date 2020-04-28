class Gramatica():
    def __init__(self,nombre,terminales,no_terminales,no_terminal_inicial,producciones,transformacion):
        self.nombre = nombre
        self.terminales = terminales 
        self.no_terminales = no_terminales
        self.no_terminal_inicial = no_terminal_inicial
        self.producciones = producciones
        self.transformacion = transformacion

    def crearTerminal(self,terminal):
        #variable para validar la existencia del no terminal
        validar = False

        #recorrido para validar la existencia del no terminal
        for valor in self.terminales:
            if valor == terminal.lower():
                validar = True
        for valor in self.no_terminales:
            if valor == terminal.upper():
                validar = True
                
        #retorno de la validacion
        if validar == False:
            self.terminales.append(terminal.lower())
            return"\nSe ha agregado el terminal a la gramatica\n"
        else:
            return"\nEl valor del terminal ya se encuentra en la gramatica\n"

    def crearNoTerminal(self,noTerminal):
        #variable para validar la existencia del no terminal
        validar = False

        #recorrido para validar la existencia del no terminal
        for valor in self.no_terminales:
            if valor == noTerminal.upper():
                validar = True
        for valor in self.terminales:
            if valor == noTerminal.lower():
                validar = True
                
        #retorno de la validacion
        if validar == False:
            self.no_terminales.append(noTerminal.upper())
            return"\nSe ha agregado el no terminal a la gramatica\n"
        else:
            return"\nEl valor del no terminal ya se encuentra en la gramatica\n"
    
    def removerRecursividad(self,inicial,final,siguiente):
        #creando el nuevo no terminal que tendra la produccion recursiva
        nuevoNoTerminal = inicial+"_P"
        aux = False

        #buscando si ya existe una produccion recursiva
        for produccion in self.producciones:
            if produccion.inicio == nuevoNoTerminal:
                aux = True 
                break

        if aux == False:
            #creando la produccion recursiva, agregandola a la self como tambien el nuevo no terminal
            prod = Produccion(nuevoNoTerminal,[LadoDerecho(siguiente,nuevoNoTerminal),LadoDerecho("epsilon","epsilon")],"1")
            self.producciones.append(prod)
            self.no_terminales.append(nuevoNoTerminal)
        
            #agregando la produccion original para mostrar la self con y sin recursividad
            aux = False
            for var in self.transformacion:
                if var.inicio == inicial:
                    aux = True
                    break
            if aux == True:
                var.ladoDerecho.append(LadoDerecho(inicial,siguiente))
            else: 
                self.transformacion.append(Produccion(inicial,[LadoDerecho(inicial,siguiente)],"0"))
        
            #si existe una produccion con el no terminal original dirigir sus derivados a la produccion recursiva
            for valor in self.producciones:
                if valor.inicio == inicial:
                    for derecha in valor.ladoDerecho:
                        derecha.siguiente = nuevoNoTerminal
                    break
            return"\nLa produccion a sido ingresada con exito\n"
        else:
            aux = False
            #validacion de la repeticion de la produccion
            for valor in produccion.ladoDerecho:
                if valor.terminal == siguiente:
                    aux = True
                    break
            if aux == False:
                #si la produccion no esta repetida agregandola a la produccion recursiva
                produccion.ladoDerecho.append(LadoDerecho(siguiente,nuevoNoTerminal))
                for valor in self.transformacion:
                    if valor.inicio == inicial:
                        valor.ladoDerecho.append(LadoDerecho(inicial,siguiente))
                        break
                return"\nLa produccion a sido ingresada con exito\n"
            else:
                return"\nLa produccion ya se encuentra en la gramatica\n"

    def crearProduccion(self,produccion):
        #separacion de la produccion 
        valor = produccion.split(">")
                
        #variable para validar la existencia del no terminal
        aux = False

        #validando existencia del no terminal inicial
        for noTerminal in self.no_terminales:
            if valor[0].upper() == noTerminal:
                aux = True

        if aux == True:
            #revisar que el valor producido sea o no epsilon
            if valor[1].lower() == "epsilon":
                       
                aux = False
                #verificando que la produccion no este ya en la gramatica
                for veri in self.producciones:
                    if veri.inicio == valor[0].upper():
                        for derecho in veri.ladoDerecho:
                            if derecho.terminal == "epsilon": 
                                aux = True
                                break

                if aux == True:
                    return"\nLa produccion ya se encuentra en la gramatica\n"
                else:
                    aux = False
                    aux1 = False
                            
                    #verificando si ya existe una produccion con el no terminal inicial
                    for produccion in self.producciones:
                        if produccion.inicio == valor[0].upper():
                            aux = True
                            break
                    for trans in self.transformacion:
                        if trans.inicio == valor[0].upper():
                            aux1 = True
                            break
                            
                    if aux1 == True:
                        trans.ladoDerecho.append(LadoDerecho("epsilon","epsilon"))
                    else:
                        self.transformacion.append(Produccion(valor[0].upper(),[LadoDerecho("epsilon","epsilon")],"0"))
                    if aux == True:
                        produccion.ladoDerecho.append(LadoDerecho("epsilon","epsilon"))
                        return"\nLa produccion se ha agregado a la gramatica\n"
                    else:
                        self.producciones.append(Produccion(valor[0].upper(),[LadoDerecho("epsilon","epsilon")],"0"))
                        return"\nLa produccion se ha agregado a la gramatica\n"
            else:
                aux = False

                #dividiendo el lado derecho de la produccion
                derecho = valor[1].split(" ")

                #verificando si existe recursividad por la izquierda
                for noTerminal in self.no_terminales:
                    if noTerminal == derecho[0].upper():
                        aux = True
                        break

                if aux == True and len(derecho)>1:
                            
                    aux = False

                    #verificando que el terminal exista en la gramatica
                    for terminal in self.terminales:
                        if terminal == derecho[1].lower():
                            aux = True
                            break
                        
                    if aux == True:
                        return self.removerRecursividad(valor[0].upper(),"no",derecho[1].lower())
                    else:
                        return"\nEl terminal no se encuentra en la gramatica\n"
                else:
                            
                    aux = False

                    if len(derecho) == 1:
                        aux = False

                        #verificando la existencia del terminal en la self
                        for terminal in self.terminales:
                            if terminal == derecho[0].lower():
                                aux = True
                                break

                        if aux == True:
                                    
                            aux = False
                            #verificando que exista una produccion con el no terminal inicial
                            for produccion in self.producciones:
                                if produccion.inicio == valor[0].upper():
                                    aux = True
                                    break

                            #Si existe una produccion verificar si la que existe es recursiva por la izquierda
                            if aux == True:
                                aux = False
                                nuevoNoTerminal = valor[0].upper()+"_P"
                                        
                                #verificando si existe una produccion recursiva asociada
                                for prod in self.producciones:
                                    if prod.inicio == nuevoNoTerminal:
                                        aux = True
                                        break
                                aux1 = False
                                for tran in self.transformacion:
                                    if tran.inicio == valor[0].upper():
                                        aux1 = True
                                        break
                                    
                                if aux == True:
                                    aux = False

                                    #verificando si ya esta la produccion en la self
                                    for val in produccion.ladoDerecho:
                                        if val.terminal ==  derecho[0].lower() and val.siguiente == nuevoNoTerminal:
                                            aux = True
                                            break

                                    if aux == False:
                                        produccion.ladoDerecho.append(LadoDerecho(derecho[0].lower(),nuevoNoTerminal))
                                        produccion.recursividad = "1"
                                        if aux1 == True:
                                            tran.ladoDerecho.append(LadoDerecho(derecho[0].lower(),"no"))
                                        else:
                                            self.transformacion.append(Produccion(valor[0].upper(),[LadoDerecho(derecho[0].lower(),"no")],"0"))
                                        return"\nSe ha agregado la produccion\n"
                                    else:
                                        return"\nLa produccion ya se encuentra en la gramatica\n"
                                else:
                                    aux = False

                                    #verificando si la produccion ya esta en la self
                                    for val in produccion.ladoDerecho:
                                        if val.terminal ==  derecho[0].lower() and val.siguiente == "no":
                                            aux = True
                                            break

                                    if aux == False:
                                        produccion.ladoDerecho.append(LadoDerecho(derecho[0].lower(),"no"))
                                        if aux1 == True:
                                            tran.ladoDerecho.append(LadoDerecho(derecho[0].lower(),"no"))
                                        else:
                                            self.transformacion.append(Produccion(valor[0].upper(),[LadoDerecho(derecho[0].lower(),"no")],"0"))
                                        return"\nSe ha agregado la produccion\n"
                                    else:
                                        return"\nLa produccion ya se encuentra en la gramatica\n"
                            else:
                                aux = False
                                aux1 = False
                                nuevoNoTerminal = valor[0].upper()+"_P"
                                        
                                #verificando si existe una produccion recursiva asociada
                                for prod in self.producciones:
                                    if prod.inicio == nuevoNoTerminal:
                                        aux = True
                                        break
                                for tran in self.transformacion:
                                    if tran.inicio == valor[0].upper():
                                        aux1 = True
                                        break

                                if aux == True:
                                    self.producciones.append(Produccion(valor[0].upper(),[LadoDerecho(derecho[0].lower(),nuevoNoTerminal)],"1"))
                                    if aux1 == True:
                                        tran.ladoDerecho.append(LadoDerecho(derecho[0].lower(),"no"))
                                    else:
                                        self.transformacion.append(Produccion(valor[0].upper(),[LadoDerecho(derecho[0].lower(),"no")],"0"))
                                    return"\nSe ha agregado la produccion\n"
                                else:
                                    self.producciones.append(Produccion(valor[0].upper(),[LadoDerecho(derecho[0].lower(),"no")],"0"))
                                    if aux1 == True:
                                        tran.ladoDerecho.append(LadoDerecho(derecho[0].lower(),"no"))
                                    else:
                                        self.transformacion.append(Produccion(valor[0].upper(),[LadoDerecho(derecho[0].lower(),"no")],"0"))
                                    return"\nSe ha agregado la produccion\n"
                        else:
                            return"\nEl terminal no existe en la gramatica\n"
                    else:
                        aux = False

                        #verificando la existencia del no terminal en la self
                        for noTerminal in self.no_terminales:
                            if noTerminal == derecho[1].upper():
                                aux = True
                                break

                        if aux == True:

                            aux = False

                            #verificando la existencia del terminal en la self
                            for termi in self.terminales:
                                if termi == derecho[0].lower():
                                    aux = True
                                    break

                            if aux == True:
                                aux = False
                                #verificando que no se repita la produccion
                                for produccion in self.producciones:
                                    if produccion.inicio == valor[0].upper():
                                        for val in produccion.ladoDerecho:
                                            if val.terminal == derecho[0].lower():
                                                aux = True
                                                break
                                        
                                if aux == True:
                                    return"\nLa produccion ya se encuentra en la gramatica\n"
                                else:
                                    aux = False
                                
                                    #verificando si existe una produccion con el no terminal inicial
                                    for produccion in self.producciones:
                                        if produccion.inicio == valor[0].upper():
                                            #agregando el lado derecho a la produccion existente
                                            produccion.ladoDerecho.append(LadoDerecho(derecho[0].lower(),derecho[1].upper()))
                                            aux = True
                                            break
                                
                                    aux1 = False  
                                    for tran in self.transformacion:
                                        if tran.inicio == valor[0].upper():
                                            aux1 = True
                                            break

                                    if aux == True:
                                        if aux1 == True:
                                            tran.ladoDerecho.append(LadoDerecho(derecho[0].lower(),derecho[1].upper()))
                                        else:
                                            self.transformacion.append(Produccion(valor[0].upper(),[LadoDerecho(derecho[0].lower(),derecho[1].upper())],"0"))
                                        return"\nSe ha agregado la produccion a la gramatica\n"
                                    else:
                                        self.producciones.append(Produccion(valor[0].upper(),[LadoDerecho(derecho[0].lower(),derecho[1].upper())],"0"))
                                        if aux1 == True:
                                            tran.ladoDerecho.append(LadoDerecho(derecho[0].lower(),derecho[1].upper()))
                                        else:
                                            self.transformacion.append(Produccion(valor[0].upper(),[LadoDerecho(derecho[0].lower(),derecho[1].upper())],"0"))
                                        return"\nSe ha agregado la produccion a la gramatica\n"                                   
                            else:
                                return"\nEl terminal ingresado no existe en la gramatica\n"
                        else:
                            return"\nEl no terminal ingresado no existe en la gramatica\n"
        else:
            return"\nEl no terminal inicial no exite en la gramatica\n"

class Produccion():
    def __init__(self,inicio,ladoDerecho,recursividad):
        self.inicio = inicio
        self.ladoDerecho = ladoDerecho
        self.recursividad = recursividad
        
class LadoDerecho():
    def __init__(self,terminal,siguiente):
        self.siguiente = siguiente
        self.terminal = terminal