class AutomataP():
    def __init__(self,nombre,estados,noTerminalInicial,alfabeto,simbolosPila,transiciones):
        self.nombre = nombre
        self.estados = estados
        self.noTerminalInicial = noTerminalInicial
        self.alfabeto = alfabeto
        self.simbolosPila = simbolosPila
        self.transiciones = transiciones

    def crearEstados(self):
        self.estados.append(EstadoP("i",0))
        self.estados.append(EstadoP("p",0))
        self.estados.append(EstadoP("q",0))
        self.estados.append(EstadoP("f",1))

    def crearTransiciones(self,gramatica):
        self.transiciones = []
        
        alpha = "\u03BB"

        self.transiciones.append(TransicionP("i",alpha,alpha,"p","#"))
        
        if gramatica.noTerminalInicial == "":
            return"La gramatica no posee un no terminal inicial"
        else:
            self.transiciones.append(TransicionP("p",alpha,alpha,"q",gramatica.noTerminalInicial))

        if len(gramatica.terminales) == 0:  
            return"No existen terminales en la gramatica"
        else:
            for terminal in gramatica.terminales:
                self.transiciones.append(TransicionP("q",terminal,terminal,"q",alpha))
    
        if len(gramatica.producciones) == 0:
            return"No existen producciones en la gramatica"
        else:
            for produccion in gramatica.producciones:
                for derecha in produccion.ladoDerecho:
                    self.transiciones.append(TransicionP("q",alpha,produccion.inicial,"q",derecha))

        self.transiciones.append(TransicionP("q",alpha,"#","f",alpha))
        
        return"Se a creado el automata de pila de forma exitosa"

    def generarGrafo(self):
        dot = "digraph G{\nrankdir=LR\n"

        #creando los identificadores del nodo, el valor que tendra el nodo y la forma del nodo
        for estados in self.estados:
            if estados.aceptacion == 1:
                dot += estados.valor + " [ label = "+ '"' + estados.valor + '" shape = "doublecircle" ] \n'
            else:
                dot += estados.valor + " [ label = "+ '"' + estados.valor + '" shape = "circle" ] \n'
    
        #creando las aristas que corresponden a cada transicion
        for transicion in self.transiciones:
            valor = transicion.entrada+","+transicion.lecturaPila+";"+transicion.guardarEnPila
            dot += transicion.actual + " -> " + transicion.nuevoEstado + "[ label = " + '"' + valor + '" ]\n'

        #creando la flecha que apunta hacia el estado inicial
        dot += "init [label = " + '"' + "inicio" + '" shape =' + '"' + "plaintext" + '" ]\n' 
        dot += "init -> i \n }"

        return dot

class EstadoP():
    def __init__(self,valor,aceptacion):
        self.valor = valor
        self.aceptacion = aceptacion

class TransicionP():
    def __init__(self,actual,entrada,lecturaPila,nuevoEstado,guardarEnPila):
        self.actual = actual
        self.entrada = entrada
        self.lecturaPila = lecturaPila
        self.nuevoEstado = nuevoEstado
        self.guardarEnPila = guardarEnPila