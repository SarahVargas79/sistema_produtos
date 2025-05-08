from Produto import Produto

class Notebook(Produto):
    def __init__(self, modelo, cor, preco, categoria, tempoDeBateria, info_extra):
        super().__init__(modelo, cor, preco, categoria, info_extra)
        self.__tempoDeBateria = tempoDeBateria

    def getInformacoes(self):
        base_info = super().getInformacoes()
        info = f"ID: {self.id}\n"
        info += f"Modelo: {self.modelo}\n"
        info += f"Cor: {self.cor}\n"
        info += f"Preço: R${self.preco:.2f}\n"
        info += f"Categoria: {self.categoria}\n"
        info += f"Tempo de Bateria: {self.__tempoDeBateria}h\n"
        if self.info_extra:
            info += f"Info Extra: {self.info_extra}\n"
        return info

    def cadastrar(self):
        pass  # Cadastro será feito pela interface gráfica

    @property
    def tempoDeBateria(self):
        return self.__tempoDeBateria

    @tempoDeBateria.setter
    def tempoDeBateria(self, valor):
        self.__tempoDeBateria = valor
