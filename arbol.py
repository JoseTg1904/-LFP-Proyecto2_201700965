class ArbolS():
    def __init__(self,tamanio,nodos):
        self.tamanio = 0
        self.nodos = []

    def agregar(self,valor,idenPadre,idenHijo):
        if self.tamanio == 0:
            self.nodos.append(Nodo(valor,idenPadre,[]))
            self.tamanio += 1
        else:
            for val in self.nodos:
                if val.identificador == idenPadre:
                    nodo = Nodo(valor,idenHijo,[])
                    val.hijos.insert(0,nodo)
                    self.nodos.append(nodo)
                    self.tamanio += 1
                    break
 

    def generarGrafo(self):
        dot = "digraph G{\nrankdir=TB\n"
        for val in self.nodos:
            dot += val.identificador +" [ label ="+'"'+val.valor+'" ]\n'
            for val1 in val.hijos:
                dot += val.identificador +"->"+ val1.identificador +"\n"        
        dot += "}"

        return dot

class Nodo():
    def __init__(self,valor,identificador,hijos):
        self.valor = valor
        self.identificador = identificador
        self.hijos = hijos
