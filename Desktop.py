from Produto import Produto

class Desktop(Produto):
    def __init__(self, modelo, cor, preco, categoria, potenciaDaFonte, info_extra):
        super().__init__(modelo, cor, preco, categoria, info_extra)
        self._potenciaDaFonte = potenciaDaFonte

    def getInformacoes(self):
        base_info = super().getInformacoes()
        info = f"ID: {self.id}\n"
        info += f"Modelo: {self.modelo}\n"
        info += f"Cor: {self.cor}\n"
        info += f"Preço: R${self.preco:.2f}\n"
        info += f"Categoria: {self.categoria}\n"
        info += f"Potência da Fonte: {self._potenciaDaFonte}W\n"
        if self.info_extra:
            info += f"Info Extra: {self.info_extra}\n"
        return info


    def cadastrar(self):
        pass  # Cadastro será feito pela interface gráfica

    @property
    def potenciaDaFonte(self):
        return self._potenciaDaFonte

    @potenciaDaFonte.setter
    def potenciaDaFonte(self, valor):
        self._potenciaDaFonte = valor
