import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        self._listYear = self._model.getAnni()#lista di anni
        self._listColor = self._model.getColori()#lista di colori

        for anno in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(anno))

        for colore in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(colore))



    def handle_graph(self, e):
        colore = self._view._ddcolor.value
        anno = int(self._view._ddyear.value)

        if colore == "" or anno == "":
            self._view.create_alert("Non hai compilato tutti i campi")
            return

        self._model.creaGrafo(colore, anno)
        self.fillDDProduct()
        self._view.btn_search.disabled = False

        self._view.txtOut.clean()
        self._view.txtOut.controls.append(ft.Text(f"Numero di vertici: {len(self._model.getNodes())}"))
        self._view.txtOut.controls.append(ft.Text(f"Numero di archi: {len(self._model.getEdges())}"))

        nodiRipetuti, stringhe = self._model.getPesiMaggiori()
        for stringa in stringhe:
            self._view.txtOut.controls.append(ft.Text(stringa))


        listaNodiRipetuti = []
        for key in nodiRipetuti:
            if nodiRipetuti[key] >= 2:
                listaNodiRipetuti.append(key.Product_number)
        self._view.txtOut.controls.append(ft.Text(f'Nodi ripetuti: {listaNodiRipetuti}'))
        self._view.update_page()





    def fillDDProduct(self):
        listaProdotti = self._model.getNodes()
        for prodotto in listaProdotti:
            self._view._ddnode.options.append(ft.dropdown.Option(prodotto))


    def handle_search(self, e):

        nodoOrigine = self._view._ddnode.value

        sequenzaOttima = self._model.chiamaRicorsione(nodoOrigine)
        self._view.txtOut2.controls.append(ft.Text(f'Numero archi percorso più lungo: {len(sequenzaOttima)}'))
        self._view.update_page()



