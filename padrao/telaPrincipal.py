import padrao.telaSecundaria
import psycopg2
import datetime
import tkinter as tk
from tkinter import Frame, Label, Entry, Button, ttk, messagebox, Toplevel
from ttkthemes import ThemedStyle
from padrao.telaSecundaria import GastosView


class ProdutoModel:
    @staticmethod
    def conectar_com_banco():
        try:
            conexao = psycopg2.connect(database='DBvendas', host='localhost', user='postgres', password='123456',
                                       port='5432')
            cursor = conexao.cursor()

            create = "CREATE TABLE IF NOT EXISTS produtos (id SERIAL PRIMARY KEY, nome_produto VARCHAR(255) , preco_produto DECIMAL , data_venda VARCHAR (255))"

            cursor.execute(create)

            return conexao, cursor

        except psycopg2.Error as err:
            print("Erro ao conectar ao banco de dados:", err)
            return None, None

    @staticmethod
    def inserir_produtos(dados):
        conexao, cursor = ProdutoModel.conectar_com_banco()
        if conexao and cursor:
            try:
                if all(dados):
                    insert = "INSERT INTO produtos(nome_produto, preco_produto, data_venda) VALUES (%s, %s ,%s)"
                    cursor.execute(insert, dados)
                    conexao.commit()
                    msg = "VENDA FINALIZADA!"
                    messagebox.showinfo("SUCESSO", msg)
                else:
                    msg = "preço e nome do produto são obrigatórios"
                    messagebox.showinfo("preencha todos os campos!", msg)
            except psycopg2.Error as err:
                print("Erro ao inserir dados no banco:", err)
            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")

    @staticmethod
    def obter_dados_do_banco():
        conexao, cursor = ProdutoModel.conectar_com_banco()
        if conexao and cursor:
            try:
                select = "SELECT * FROM produtos"
                cursor.execute(select)
                return cursor.fetchall()

            except psycopg2.Error as err:
                print("erro ao obter dados do banco", err)

            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()

        else:
            print("Não foi possível conectar ao banco de dados.")
            return None

    @staticmethod
    def editar_produtos(dados_atualizados):
        conexao, cursor = ProdutoModel.conectar_com_banco()
        if conexao and cursor:
            try:
                update = "UPDATE produtos SET nome_produto = %s, preco_produto = %s, data_venda = %s WHERE id = %s"
                cursor.execute(update, dados_atualizados)
                conexao.commit()
            except psycopg2.Error as err:
                print("Erro ao editar os dados do banco:", err)
            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")

    @staticmethod
    def excluir_produtos(dados):
        conexao, cursor = ProdutoModel.conectar_com_banco()
        if conexao and cursor:
            try:
                id_produto = dados[0]
                delete = "DELETE FROM produtos WHERE id = %s"
                cursor.execute(delete, (id_produto,))
                conexao.commit()
            except psycopg2.Error as err:
                print("Erro ao excluir dados do banco:", err)
            finally:
                if cursor:
                    cursor.close()
                if conexao:
                    conexao.close()
        else:
            print("Não foi possível conectar ao banco de dados.")


class ProdutoView:
    def __init__(self, root):
        self.fontepadrao = ("Arial", "20")
        self.fonteEntrys = ("Arial", "25")
        self.root = root
        self.root.title("Gerenciamento de Vendas em uma casa de ração")
        self.root.configure(background="#514d4d")
        self.root.geometry("1300x600")
        self.root.resizable(True, True)
        # self.root.maxsize(width=1500, height=450) # tamanho maximo
        # self.root.minsize(width=800, height=400) # tamanho minimo

        # highlightbackground cor da borda, highlightthickness largura da borda
        self.primeiroContainer = Frame(root, bd=4, bg="#081D3C", highlightbackground="#000000", highlightthickness=2)
        self.primeiroContainer["pady"] = 10  # espaçamento interno na vertical
        self.primeiroContainer.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.6)

        # criação do segundo container
        self.segundoContainer = Frame(root, bd=4, bg="#081D3C", highlightbackground="#000000", highlightthickness=2)
        self.segundoContainer["pady"] = 10
        self.segundoContainer.place(relx=0.1, rely=0.7, relwidth=0.8, relheight=0.3)

        self.titulo = Label(self.primeiroContainer, text="Gerenciamento de Vendas", bg="#081D3C", fg="white")
        self.titulo['font'] = ("Arial", "15", "bold", "italic")
        self.titulo.place(relx=0.5, rely=0.1, anchor="center")

        self.nomeProdutoLabel = Label(self.primeiroContainer, text="Nome do Produto", font=self.fontepadrao,
                                      bg="#081D3C", fg="white")
        self.nomeProdutoLabel.place(relx=0.2, rely=0.3, anchor="center")

        self.nomeProdutoEntry = Entry(self.primeiroContainer, font=self.fonteEntrys)
        self.nomeProdutoEntry["width"] = 25
        self.nomeProdutoEntry.place(relx=0.6, rely=0.3, anchor="center")

        self.precoProdutoLabel = Label(self.primeiroContainer, text="Preço do Produto", font=self.fontepadrao,
                                       bg="#081D3C", fg="white")
        self.precoProdutoLabel.place(relx=0.2, rely=0.5, anchor="center")

        self.precoProdutoEntry = Entry(self.primeiroContainer, font=self.fonteEntrys)
        self.precoProdutoEntry["width"] = 25
        self.precoProdutoEntry.place(relx=0.6, rely=0.5, anchor="center")

        self.dataAtual = datetime.datetime.now().strftime("%d/%m/%Y")

        self.dataLabel = Label(self.primeiroContainer, text="Data: " + self.dataAtual, font=("calibri", "25"),
                               bg="#081D3C", fg="white")
        self.dataLabel.place(relx=0.6, rely=0.7, anchor="e")

        self.vender = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.vender["text"] = "Vender"
        self.vender["font"] = self.fontepadrao
        self.vender["width"] = 10
        # usamos a expressão lambda pois queremos que a função só seja chamada no momento em que o botão e clicado, criando uma função anonima que chamada a função de inserir produtos
        self.vender["command"] = lambda: self.inserir_produtos()
        self.vender.place(relx=0.1, rely=0.9, anchor="center")

        self.editar = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.editar["text"] = "Editar"
        self.editar["font"] = self.fontepadrao
        self.editar["width"] = 10
        self.editar["command"] = self.editar_produtos
        self.editar.place(relx=0.3, rely=0.9, anchor="center")

        self.excluir = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.excluir["text"] = "Excluir"
        self.excluir["font"] = self.fontepadrao
        self.excluir["width"] = 10
        # usamos a expressão lambda pois queremos que a função só seja chamada no momento em que o botão e clicado, criando uma função anonima que chamada a função confimar exclusão
        self.excluir["command"] = lambda: self.confirmar_exclusao(self.dados_selecionados)
        self.excluir.place(relx=0.7, rely=0.9, anchor="center")

        self.limpar = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.limpar["text"] = "Limpar"
        self.limpar["font"] = self.fontepadrao
        self.limpar["width"] = 10
        self.limpar["command"] = self.limpar_entrys
        self.limpar.place(relx=0.9, rely=0.9, anchor="center")

        self.segundaTela = Button(self.primeiroContainer, bd=2, bg="#7f8fff")
        self.segundaTela["text"] = "Gastos"
        self.segundaTela["font"] = self.fontepadrao
        self.segundaTela["width"] = 10
        self.segundaTela["command"] = self.exibirSegundaTela
        self.segundaTela.place(relx=0.5, rely=0.9, anchor="center")

        style = ThemedStyle()
        style.configure("Treeview", font=("arial", 15), background="#081D3C", foreground="white",
                        fieldbackground="#081D3C")

        self.minha_lista = ttk.Treeview(self.segundoContainer, height=5, columns=("col1", "col2", "col3", "col4"))
        self.minha_lista.heading("col1", text="ID", )
        self.minha_lista.heading("col2", text="Nome do produto")
        self.minha_lista.heading("col3", text="Preço do produto")
        self.minha_lista.heading("col4", text="Data da venda")

        self.minha_lista.column("col1", width=50, anchor=tk.CENTER)
        self.minha_lista.column("col2", width=110, anchor=tk.CENTER)
        self.minha_lista.column("col3", width=110, anchor=tk.CENTER)
        self.minha_lista.column("col4", width=100, anchor=tk.CENTER)

        yscrollbar = ttk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.minha_lista.yview)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.minha_lista.configure(yscrollcommand=yscrollbar.set)

        self.minha_lista.pack(expand=True, fill=tk.BOTH)

        self.exibir_dados_do_banco()

        self.minha_lista.bind("<Double-1>", self.double_click)  # chama a função double click

    def exibirSegundaTela(self):
        root2 = tk.Toplevel(self.root)  # Toplevel serve para criar janelas separadas da tela principal
        tela_secundaria_instance = padrao.telaSecundaria.GastosView(root2)

    def limpar_entrys(self):
        self.nomeProdutoEntry.delete(0,
                                     tk.END)  # passamos o zero e o end pra dizer que ele vai excluir do inicio ao final
        self.precoProdutoEntry.delete(0,
                                      tk.END)  # passamos o zero e o end pra dizer que ele vai excluir do inicio ao final

    def confirmar_exclusao(self, dados_selecionados):
        if dados_selecionados:

            resposta = messagebox.askquestion("CONFIRMAÇÃO", "DESEJA REALMENTE EXCLUIR O PRODUTO ?")

            if resposta == "yes":
                id_produto = dados_selecionados[0]
                ProdutoController.excluir_produtos(dados_selecionados)
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso")
                self.exibir_dados_do_banco()
                self.limpar_entrys()
            else:
                messagebox.showinfo("Cancelado", "Exclusão cancelada")
                self.limpar_entrys()
        else:
            messagebox.showinfo("Erro", "Nenhum item selecionado para excluir.")

    def double_click(self, event=None):

        item_selecionado = self.minha_lista.selection()[0]  # obtem o primeiro item da lista

        self.dados_selecionados = self.minha_lista.item(item_selecionado,
                                                        "values")  # obtem o valor do primeiro item selecionado

        self.nomeProdutoEntry.delete(0, tk.END)  # deleta o nome do produto
        self.nomeProdutoEntry.insert(0, self.dados_selecionados[1])  # insere o nome do produto
        self.precoProdutoEntry.delete(0, tk.END)  # deleta o preco do produto
        self.precoProdutoEntry.insert(0, self.dados_selecionados[2])  # insere o preco do produto

    def exibir_dados_do_banco(self):
        dados_do_banco = ProdutoModel.obter_dados_do_banco()
        if dados_do_banco:
            for item in self.minha_lista.get_children():
                self.minha_lista.delete(item)  # deleta o item na lista
            for row in dados_do_banco:
                self.minha_lista.insert("", tk.END, values=row)  # insere o item na lista

    def obter_dados(self):
        nome_produto = self.nomeProdutoEntry.get()
        preco_produto = self.precoProdutoEntry.get()
        data_venda = self.dataAtual

        dados = (nome_produto, preco_produto, data_venda)
        return dados

    def inserir_produtos(self):
        dados = self.obter_dados()
        ProdutoController.inserir_produtos(dados)
        self.exibir_dados_do_banco()
        self.limpar_entrys()

    def editar_produtos(self):
        # Verifica se há dados selecionados
        if self.dados_selecionados:
            # Obtém os dados atualizados
            dados_atualizados = self.obter_dados()
            # Adiciona o id aos dados atualizados
            dados_atualizados += (self.dados_selecionados[0],)
            ProdutoController.editar_produtos(dados_atualizados)
            msg = "Os dados foram atualizados com sucesso"
            messagebox.showinfo("Dados Alterados", msg)
            self.exibir_dados_do_banco()
            self.limpar_entrys()
        else:
            messagebox.showinfo("Erro", "Nenhum item selecionado para editar.")

    def excluir_produtos(self):
        item_selecionado = self.minha_lista.selection()[0]
        dados_selecionados = self.minha_lista.item(item_selecionado, "values")
        ProdutoController.excluir_produtos(dados_selecionados)


class ProdutoController:

    @staticmethod
    def inserir_produtos(dados):
        ProdutoModel.inserir_produtos(dados)

    @staticmethod
    def editar_produtos(dados):
        ProdutoModel.editar_produtos(dados)

    @staticmethod
    def excluir_produtos(dados_selecionados):
        ProdutoModel.excluir_produtos(dados_selecionados)


if __name__ == "__main__":
    root = tk.Tk()
    ProdutoView(root)
    root.mainloop()


