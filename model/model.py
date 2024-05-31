import copy

import networkx as nx

from database.DAO import DAO
import operator

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}
        self._listaSequenzaOttima = []
        self._lunghezzaMax = 0





    def creaGrafo(self, colore, anno):
        nodi = DAO.getAllNodes(colore)
        self._graph.add_nodes_from(nodi)
        for n in self._graph.nodes():
            self._idMap[n.Product_number] = n
        archiDaFiltrare = DAO.getAllEdges(anno, colore)

        for c in archiDaFiltrare:
            p1 = self._idMap[c.p1]
            p2 = self._idMap[c.p2]
            peso = c.peso

            if self._graph.has_edge(p1, p2):
                self._graph[p1][p2]["weight"] += peso

            else:
                self._graph.add_edge(p1, p2, weight=peso)




    def getPesiMaggiori(self):
        pesi = []
        archiPesiMaggiori = []
        nodiRipetuti = {}
        for n1, n2 in self._graph.edges():
            print(self._graph[n1][n2]['weight'])
            pesi.append(self._graph[n1][n2]['weight'])
        pesi.sort(reverse=True)


        for n1, n2 in self._graph.edges():
            if self._graph[n1][n2]['weight'] in pesi[:3]:
                stringa = f"Arco da {n1} a {n2}, peso: {self._graph[n1][n2]['weight']}"
                if len(archiPesiMaggiori) <= 2:
                    archiPesiMaggiori.append(stringa)
                    if n1 not in nodiRipetuti:
                        nodiRipetuti[n1] = 1
                    else:
                        nodiRipetuti[n1] += 1

                    if n2 not in nodiRipetuti:
                        nodiRipetuti[n2] = 1
                    else:
                        nodiRipetuti[n2] = nodiRipetuti[n2] + 1
                else:
                    break

        return nodiRipetuti, archiPesiMaggiori

    def chiamaRicorsione(self, nodoOrigine):
        parziale = []
        self._listaSequenzeSalvate = []
        nodo = self._idMap[int(nodoOrigine)]
        self.ricorsione(nodo, parziale)
        print(self._listaSequenzaOttima)
        return self._listaSequenzaOttima
    '''def chiamaRicorsione(self, nodoOrigine):
        parziale = []
        self._listaSequenzaOttima = []

        nodo = self._idMap[int(nodoOrigine)]
        parziale.append(nodo)

        for n in self._graph.neighbors(parziale[-1]):
            parziale.append(n)#inizio la ricorsione con parziale contenente due nodi, quello origine e uno dei vicini
            self.ricorsione(parziale)

        return self._listaSequenzaOttima

    def ricorsione(self, parziale):
        if len(parziale) > len(self._listaSequenzaOttima):
            self._listaSequenzaOttima = copy.deepcopy(parziale)

        for n in self._graph.neighbors(parziale[-1]):
            if self._graph[parziale[-1]][n]['weight'] >= self._graph[parziale[-2]][parziale[-1]]['weight']:
                if n in parziale:
                    if parziale[parziale.index(n)-1] == parziale[-1]:
                        continue
                parziale.append(n)
                self.ricorsione(parziale)
        if len(parziale) > 1:
            parziale.pop()
            return

        if len(parziale) == 1:
            return'''








    def ricorsione(self, nodo, parziale):
        if len(parziale) > len(self._listaSequenzaOttima):
            self._listaSequenzaOttima = copy.deepcopy(parziale)


        for vicino in self._graph.neighbors(nodo):
            if len(parziale) == 0:
                parziale.append((nodo, vicino, self._graph[nodo][vicino]['weight']))
                self.ricorsione(vicino, parziale)
                parziale.pop()
            else:
                arcoCorrente = (nodo, vicino, self._graph[nodo][vicino]['weight'])
                arcoCorrenteSpecchiato = (vicino, nodo, self._graph[nodo][vicino]['weight'])
                if arcoCorrente not in parziale and arcoCorrenteSpecchiato not in parziale:
                    pesoNuovo = self._graph[nodo][vicino]['weight']
                    ultimoPeso = parziale[-1][2]
                    if pesoNuovo >= ultimoPeso:
                        parziale.append((nodo, vicino, self._graph[nodo][vicino]['weight']))
                        self.ricorsione(vicino, parziale)
                        parziale.pop()



    def getArchiGrafo(self):
        listaArchi = []
        for n1, n2 in self._graph.edges():
            listaArchi.append((n1, n2, self._graph[n1][n2]['weight']))
        return listaArchi




    def getNodes(self):
        return self._graph.nodes
    def getEdges(self):
        return self._graph.edges

    def getAnni(self):
        return DAO.getAnni()

    def getColori(self):
        return DAO.getColori()