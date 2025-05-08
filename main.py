import tkinter as tk
from Categoria import Categoria
from Desktop import Desktop
from Notebook import Notebook
from view import View

# Lista de categorias globais
categorias = [
    Categoria(1, "Uso Básico"),
    Categoria(2, "Estudo"),
    Categoria(3, "Trabalho Leve (Office, planilhas, e-mails)"),
    Categoria(4, "Trabalho Profissional (design gráfico, arquitetura, programação)"),
    Categoria(5, "Edição de Vídeo/Imagem"),
    Categoria(6, "Workstation")
]

produtos = []

# .strip() remove espaços em branco no início e no fim do texto digitado.
# Isso evita erros em comparações, buscas ou validações de campos de entrada.

def adicionar_categoria(nome_categoria):
    if nome_categoria.strip():
        novo_id = len(categorias) + 1
        nova = Categoria(novo_id, nome_categoria.strip())
        categorias.append(nova)
        return True
    return False

# Função para alternar entre os modos Desktop e Notebook
def atualizar_interface(tipo, view):
    view.limpar_campos()
    view.tipo = tipo
    if tipo == "Desktop":
        view.set_label_extra("Potência da Fonte (W):")
    else:
        view.set_label_extra("Tempo de Bateria (h):")
    view.verificar_campos()

def verificar_preco(view):
    try:
        preco = view.get_preco()
        if not preco.strip():
            view.lbl_erro_preco.config(text="")
            return False
        valor = float(preco)
        if valor < 0:
            view.lbl_erro_preco.config(text="O preço não pode ser negativo.")
            return False
        view.lbl_erro_preco.config(text="")
        return True
    except ValueError:
        view.lbl_erro_preco.config(text="Insira um valor numérico válido.")
        return False

def verificar_potencia(view):
    try:
        extra = view.get_extra()
        if not extra.strip():
            view.lbl_erro_extra.config(text="")
            return False
        valor = float(extra)
        if valor < 0:
            view.lbl_erro_extra.config(text="A potência não pode ser negativa.")
            return False
        view.lbl_erro_extra.config(text="")
        return True
    except ValueError:
        view.lbl_erro_extra.config(text="Insira um valor numérico válido.")
        return False

def verificar_tempo(view):
    try:
        extra = view.get_extra()
        if not extra.strip():
            view.lbl_erro_extra.config(text="")
            return False
        valor = float(extra)
        if valor < 0:
            view.lbl_erro_extra.config(text="O tempo não pode ser negativo.")
            return False
        view.lbl_erro_extra.config(text="")
        return True
    except ValueError:
        view.lbl_erro_extra.config(text="Insira um valor numérico válido.")
        return False

# Essa função só retorna True se todos os campos estiverem corretos:
# - Preço válido
# - Potência válida
# - Tempo válido
# Se algum deles for inválido, retorna False e bloqueia a ação.
def verificar_campos(view):
    if not verificar_preco(view):
        return False
    if not verificar_potencia(view):
        return False
    if not verificar_tempo(view):
        return False
    return True

def cadastrar_produto(view):
    try:
        tipo = view.tipo
        modelo = view.get_modelo()
        cor = view.get_cor()
        preco = float(view.get_preco())
        categoria_nome = view.get_categoria()
        extra = view.get_extra()
        info_extra = view.get_info_extra()

        if not modelo or not cor or not preco or not extra or categoria_nome == "Selecione uma categoria":
            raise ValueError("Todos os campos devem ser preenchidos!")

        # Busca na lista um item que corresponda ao valor informado.
        # Se encontrar, retorna esse item; caso contrário, retorna None.
        categoria = next((cat for cat in categorias if str(cat) == categoria_nome), None)

        if tipo == "Desktop":
            produto = Desktop(modelo, cor, preco, categoria, int(extra), info_extra)
        else:
            produto = Notebook(modelo, cor, preco, categoria, float(extra), info_extra)

        produtos.append(produto)
        view.mostrar_sucesso("Produto cadastrado com sucesso!")
        view.limpar_campos()

    except Exception as e:
        view.mostrar_erro(str(e))

# Lista os produtos já cadastrados
def listar_produtos():
    return produtos

# Função para deletar um produto pelo ID
def deletar_produto(view):
    try:
        produto_id = int(view.get_id_exclusao())

        if not produto_id:
            raise ValueError("Informe o ID do produto para deletar.")

        # Verifica se o objeto tem o atributo 'id' com hasattr antes de acessar.
        # Isso evita erro se algum objeto não tiver o atributo.
        # Em seguida, compara o valor com o que foi digitado para localizar o item.

        produto = next((p for p in produtos if hasattr(p, 'id') and p.id == produto_id), None)

        if produto:
            produtos.remove(produto)
            view.mostrar_sucesso(f"Produto com ID {produto_id} deletado com sucesso!")
            view.limpar_campos()
        else:
            raise ValueError("Produto com ID informado não foi encontrado.")
    except ValueError as ve:
        view.mostrar_erro(str(ve))
    except Exception as e:
        view.mostrar_erro("Erro ao deletar o produto.")

# Iniciar aplicação
# lambda cria uma função rápida (anônima) para passar argumentos.
# Útil quando você quer chamar uma função com parâmetros ao clicar em um botão.
if __name__ == "__main__":
    root = tk.Tk()
    app = View(
        root,
        categorias,
        adicionar_categoria,
        lambda tipo: atualizar_interface(tipo, app),
        lambda: app.verificar_campos(),
        verificar_preco,
        verificar_potencia,
        verificar_tempo,
        lambda: cadastrar_produto(app),
        listar_produtos,
        lambda: deletar_produto(app)
    )
    root.mainloop()
