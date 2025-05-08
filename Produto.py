from abc import ABC, abstractmethod

class Produto(ABC):
    contador_id = 1  # contador de IDs únicos para cada produto

    def __init__(self, modelo, cor, preco, categoria, info_extra):
        self.id = Produto.contador_id
        Produto.contador_id += 1
        self.modelo = modelo
        self.cor = cor
        self.preco = preco
        self.categoria = categoria
        self.info_extra = info_extra

    def getInformacoes(self):
        return f"Modelo: {self.modelo}, Cor: {self.cor}, Preço: R${self.preco:.2f}, Categoria: {self.categoria}, Extra: {self.info_extra}"

    @abstractmethod
    def cadastrar(self):
        pass
