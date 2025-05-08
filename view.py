import tkinter as tk
from tkinter import ttk, messagebox

class View:
    def __init__(self, root, categorias, adicionar_categoria_cb, atualizar_interface_cb, verificar_cb, verificar_preco_cb, verificar_potencia_cb, verificar_tempo_cb, cadastrar_cb, listar_cb, deletar_cb):
        self.root = root
        self.categorias = categorias
        self.adicionar_categoria_cb = adicionar_categoria_cb
        self.atualizar_interface_cb = atualizar_interface_cb
        self.verificar_cb = verificar_cb
        self.verificar_preco_cb = verificar_preco_cb
        self.verificar_potencia_cb = verificar_potencia_cb
        self.verificar_tempo_cb = verificar_tempo_cb
        self.cadastrar_cb = cadastrar_cb
        self.listar_cb = listar_cb
        self.deletar_cb = deletar_cb
        self.tipo = "Desktop"

        self.root.title("Cadastro de Produtos")
        self.root.geometry("750x600")
        self.root.configure(bg="#f8f9fa")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self._montar_interface()

    def _montar_interface(self):
        self.frame_top = tk.Frame(self.root, bg="#f8f9fa", pady=10)
        self.frame_top.pack(fill="x")

        self.btn_desktop = self._botao_topo("Desktop", lambda: self.atualizar_interface_cb("Desktop"))
        self.btn_notebook = self._botao_topo("Notebook", lambda: self.atualizar_interface_cb("Notebook"))

        self.frame_inputs = ttk.Frame(self.root, padding=10)
        self.frame_inputs.pack(fill="x", pady=15)

        self.entry_modelo = self._entrada("Modelo:", 0)
        self.entry_cor = self._entrada("Cor:", 1)
        self.entry_preco = self._entrada("Preço:", 2)
        self.lbl_erro_preco = tk.Label(self.frame_inputs, text="", fg="red", bg="#f8f9fa", font=("Helvetica", 8))
        self.lbl_erro_preco.grid(row=2, column=2, sticky="w")

        ttk.Label(self.frame_inputs, text="Categoria:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.categoria_var = tk.StringVar(value="Selecione uma categoria")
        self.combo_categoria = ttk.Combobox(self.frame_inputs, textvariable=self.categoria_var, state="readonly", width=25)
        self._atualizar_categorias()
        self.combo_categoria.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self.frame_inputs, text="Nova Categoria:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.entry_nova_categoria = ttk.Entry(self.frame_inputs)
        self.entry_nova_categoria.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        tk.Button(self.frame_inputs, text="Adicionar", command=self._adicionar_categoria, bg="#007bff", fg="white", relief="flat", font=("Helvetica", 10)).grid(row=4, column=2, padx=5)

        self.lbl_extra = ttk.Label(self.frame_inputs, text="Potência da Fonte (W):")
        self.lbl_extra.grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.entry_extra = ttk.Entry(self.frame_inputs)
        self.entry_extra.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        self.lbl_erro_extra = tk.Label(self.frame_inputs, text="", fg="red", bg="#f8f9fa", font=("Helvetica", 8))
        self.lbl_erro_extra.grid(row=5, column=2, sticky="w")

        ttk.Label(self.frame_inputs, text="Informação Extra (opcional):").grid(row=6, column=0, sticky="w", padx=10, pady=5)
        self.entry_info_extra = ttk.Entry(self.frame_inputs)
        self.entry_info_extra.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        # Campo para o ID (para exclusão)
        ttk.Label(self.frame_inputs, text="ID do Produto (para exclusão):").grid(row=7, column=0, sticky="w", padx=10, pady=5)
        self.entry_exclusao = ttk.Entry(self.frame_inputs)
        self.entry_exclusao.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        self.frame_inputs.columnconfigure(1, weight=1)

        # Frame para os botões de ação (Cadastrar e Deletar lado a lado)
        self.frame_botoes = tk.Frame(self.root, bg="#f8f9fa")
        self.frame_botoes.pack(pady=10)

        self.btn_cadastrar = tk.Button(self.frame_botoes, text="Cadastrar Produto", command=self.cadastrar_cb, state="disabled",
                               bg="#28a745", fg="white", font=("Helvetica", 10), relief="flat")
        self.btn_cadastrar.pack(side="left", padx=10, ipadx=10, ipady=4)

        self.btn_deletar = tk.Button(self.frame_botoes, text="Deletar Produto", command=self.deletar_cb,
                                     bg="#dc3545", fg="white", font=("Helvetica", 10), relief="flat")
        self.btn_deletar.pack(side="left", padx=10, ipadx=10, ipady=4)

        # Botão Listar acima da caixa de texto
        self.btn_listar = tk.Button(self.root, text="Listar Produtos", command=self._listar_produtos,
                                    bg="#17a2b8", fg="white", font=("Helvetica", 10), relief="flat")
        self.btn_listar.pack(pady=(20, 5), ipadx=10, ipady=4)

        # Criando a tela de listagem com scrollbar
        self.output_frame = tk.Frame(self.root)  # Um frame para conter o Text e a Scrollbar
        self.output_frame.pack(pady=(0, 10))

        self.scrollbar = tk.Scrollbar(self.output_frame, orient=tk.VERTICAL)  # Scrollbar vertical
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output = tk.Text(self.output_frame, height=20, width=85, font=("Helvetica", 10), wrap="word", state=tk.DISABLED, yscrollcommand=self.scrollbar.set)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Preenche todo o espaço disponível

        # Vinculando a scrollbar ao Text
        self.scrollbar.config(command=self.output.yview)

        # Eventos para validar cadastro
        self.entry_modelo.bind("<KeyRelease>", lambda e: self.verificar_cb())
        self.entry_cor.bind("<KeyRelease>", lambda e: self.verificar_cb())
        self.combo_categoria.bind("<<ComboboxSelected>>", lambda e: self.verificar_cb())
        self.entry_preco.bind("<FocusOut>", lambda e: self.verificar_cb())
        self.entry_extra.bind("<FocusOut>", lambda e: self.verificar_cb())

    def _entrada(self, label, row):
        ttk.Label(self.frame_inputs, text=label).grid(row=row, column=0, sticky="w", padx=10, pady=5)
        entry = ttk.Entry(self.frame_inputs)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        return entry

    def _botao_topo(self, texto, comando):
        btn = tk.Button(self.frame_top, text=texto, command=comando,
                        bg="#007bff", fg="white", font=("Helvetica", 10), relief="flat", padx=10, pady=6)
        btn.pack(side="left", padx=10, expand=True)
        btn.bind("<Enter>", lambda e: btn.config(bg="#0056b3"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#007bff"))
        return btn

    def _atualizar_categorias(self):
        self.combo_categoria['values'] = ["Selecione uma categoria"] + [str(cat) for cat in self.categorias]

    def _adicionar_categoria(self):
        nome = self.entry_nova_categoria.get()
        if self.adicionar_categoria_cb(nome):
            self.entry_nova_categoria.delete(0, tk.END)
            self._atualizar_categorias()
            messagebox.showinfo("Categoria", f"Categoria '{nome}' adicionada!")
        else:
            messagebox.showwarning("Categoria", "Digite um nome válido.")

    def mostrar_sucesso(self, mensagem):
        messagebox.showinfo("Sucesso", mensagem)

    def mostrar_erro(self, mensagem):
        messagebox.showerror("Erro", mensagem)

    def _listar_produtos(self):
        self.output.config(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        produtos = self.listar_cb()
        if produtos:
            for p in produtos:
                tipo = p.__class__.__name__.upper()
                self.output.insert(tk.END, f"{tipo}:\n{p.getInformacoes()}\n")
                self.output.insert(tk.END, "="*60 + "\n")
        else:
            self.output.insert(tk.END, "Nenhum produto cadastrado.")
        self.output.config(state=tk.DISABLED)
        self.output.yview(tk.END)

    def deletar_cb(self):
        self.deletar_produto_cb(self)

    # Métodos de acesso
    def get_modelo(self):
        return self.entry_modelo.get().strip()

    def get_cor(self):
        return self.entry_cor.get().strip()

    def get_preco(self):
        return self.entry_preco.get().strip()

    def get_categoria(self):
        return self.categoria_var.get()

    def get_extra(self):
        return self.entry_extra.get().strip()

    def get_info_extra(self):
        return self.entry_info_extra.get().strip()

    def get_id_exclusao(self):
        return self.entry_exclusao.get().strip()

    def set_label_extra(self, texto):
        self.lbl_extra.config(text=texto)

    def limpar_campos(self):
        self.entry_modelo.delete(0, tk.END)
        self.entry_cor.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_extra.delete(0, tk.END)
        self.entry_info_extra.delete(0, tk.END)
        self.entry_exclusao.delete(0, tk.END)
        self.categoria_var.set("Selecione uma categoria")
        self.btn_cadastrar.config(state="disabled")

    def verificar_campos(self):
        modelo = self.get_modelo()
        cor = self.get_cor()
        preco = self.get_preco()
        categoria = self.get_categoria()
        extra = self.get_extra()

        # Verifica se todos os campos obrigatórios estão preenchidos
        if not (modelo and cor and preco and categoria != "Selecione uma categoria" and extra):
            self.btn_cadastrar.config(state="disabled")
            return

        # Só valida os campos se já estiverem preenchidos (evita erro enquanto digita)
        if preco.strip() and not self.verificar_preco_cb(self):
            self.btn_cadastrar.config(state="disabled")
            return

        if extra.strip():
            if self.tipo == "Desktop" and not self.verificar_potencia_cb(self):
                self.btn_cadastrar.config(state="disabled")
                return
            elif self.tipo == "Notebook" and not self.verificar_tempo_cb(self):
                self.btn_cadastrar.config(state="disabled")
                return

        self.btn_cadastrar.config(state="normal")


