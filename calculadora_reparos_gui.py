#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculadora de Reparos - Equipe Death Row Garage
Aplicativo com interface gráfica para calcular custos de reparos automotivos
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter.font import Font
import json
import threading
try:
    from atualizador import AtualizadorApp
    ATUALIZADOR_DISPONIVEL = True
except ImportError:
    ATUALIZADOR_DISPONIVEL = False

class CalculadoraReparosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Reparos - Equipe Death Row Garage")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        
        # Configurar estilo
        self.setup_styles()
        
        # Dados
        self.carrinho = []
        self.desconto_ativo = False  # Controla se desconto de 10% está ativo
        self.setup_data()
        
        # Interface
        self.setup_interface()
        
    def setup_styles(self):
        """Configura os estilos da interface"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar cores
        self.style.configure('Title.TLabel', 
                           font=('Arial', 16, 'bold'),
                           background='#2c3e50',
                           foreground='#ecf0f1')
        
        self.style.configure('Header.TLabel',
                           font=('Arial', 12, 'bold'),
                           background='#34495e',
                           foreground='#ecf0f1')
        
        self.style.configure('Custom.TButton',
                           font=('Arial', 10, 'bold'),
                           padding=(10, 5))
        
        self.style.configure('Treeview',
                           background='#ecf0f1',
                           foreground='#2c3e50',
                           fieldbackground='#ecf0f1')
        
        self.style.configure('Treeview.Heading',
                           background='#34495e',
                           foreground='#ecf0f1',
                           font=('Arial', 10, 'bold'))
    
    def setup_data(self):
        """Configura os dados de preços"""
        self.tabela_precos = {
            "Porta": 350,
            "Porta-Mala": 600,
            "capô": 850,
            "Para-Brisa": 1200,
            "Pneu": 500,
            "Para-Choque": 400,
            
        }
        
        self.pecas = {
            "Motor": 4000,
            "Kit de Motor": 2500,
            "kit de Reparo": 3000,
            
        }
        
        # Combinar todos os itens
        self.todos_itens = {}
        self.todos_itens.update(self.tabela_precos)
        self.todos_itens.update(self.pecas)
    
    def setup_interface(self):
        """Configura a interface principal"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título com botão de atualização
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))
        title_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(title_frame, 
                               text="🔧 CALCULADORA DE REPAROS 🔧",
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Botão verificar atualizações
        self.btn_atualizar = ttk.Button(title_frame, 
                                        text="🔄 Verificar Atualizações",
                                        command=self.verificar_atualizacoes_manual,
                                        style='Custom.TButton')
        self.btn_atualizar.grid(row=0, column=1, sticky=tk.E, padx=(10, 0))
        
        # Frame esquerdo - Seleção de itens
        left_frame = ttk.LabelFrame(main_frame, text="Selecionar Itens", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Categoria
        ttk.Label(left_frame, text="Categoria:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.categoria_var = tk.StringVar()
        self.categoria_combo = ttk.Combobox(left_frame, textvariable=self.categoria_var, 
                                          values=["Todas", "Peças Individuais", "Peças Genéricas"],
                                          state="readonly", width=20)
        self.categoria_combo.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.categoria_combo.set("Todas")
        self.categoria_combo.bind('<<ComboboxSelected>>', self.filtrar_itens)
        
        # Campo de busca
        ttk.Label(left_frame, text="Buscar produto:", style='Header.TLabel').grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.busca_var = tk.StringVar()
        self.busca_entry = ttk.Entry(left_frame, textvariable=self.busca_var, width=20)
        self.busca_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.busca_var.trace('w', self.filtrar_por_busca)
        
        # Lista de itens
        ttk.Label(left_frame, text="Itens Disponíveis:", style='Header.TLabel').grid(row=4, column=0, sticky=tk.W, pady=(0, 5))
        
        # Frame para lista e scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.itens_listbox = tk.Listbox(list_frame, height=8, font=('Arial', 9))
        self.itens_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.itens_listbox.bind('<Double-1>', self.on_double_click)  # Duplo clique
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.itens_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.itens_listbox.configure(yscrollcommand=scrollbar.set)
        
        # Quantidade
        ttk.Label(left_frame, text="Quantidade:", style='Header.TLabel').grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        self.quantidade_var = tk.StringVar(value="1")
        quantidade_entry = ttk.Entry(left_frame, textvariable=self.quantidade_var, width=10)
        quantidade_entry.grid(row=7, column=0, sticky=tk.W, pady=(0, 10))
        
        # Botão adicionar
        add_button = ttk.Button(left_frame, text="➕ Adicionar ao Carrinho", 
                               command=self.adicionar_item, style='Custom.TButton')
        add_button.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botão desconto
        self.btn_desconto = ttk.Button(left_frame, text="🎁 Aplicar Desconto 10%", 
                                       command=self.toggle_desconto, style='Custom.TButton')
        self.btn_desconto.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botão limpar carrinho
        clear_button = ttk.Button(left_frame, text="🗑️ Limpar Carrinho", 
                                 command=self.limpar_carrinho, style='Custom.TButton')
        clear_button.grid(row=10, column=0, sticky=(tk.W, tk.E))
        
        # Frame direito - Carrinho e total
        right_frame = ttk.LabelFrame(main_frame, text="Carrinho de Compras", padding="10")
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Treeview para carrinho
        columns = ('Item', 'Quantidade', 'Preço Unit.', 'Subtotal')
        self.carrinho_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=8)
        
        # Configurar colunas
        self.carrinho_tree.heading('Item', text='Item')
        self.carrinho_tree.heading('Quantidade', text='Qtd')
        self.carrinho_tree.heading('Preço Unit.', text='Preço Unit.')
        self.carrinho_tree.heading('Subtotal', text='Subtotal')
        
        self.carrinho_tree.column('Item', width=200)
        self.carrinho_tree.column('Quantidade', width=60, anchor='center')
        self.carrinho_tree.column('Preço Unit.', width=100, anchor='e')
        self.carrinho_tree.column('Subtotal', width=120, anchor='e')
        
        self.carrinho_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Scrollbar para carrinho
        carrinho_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.carrinho_tree.yview)
        carrinho_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.carrinho_tree.configure(yscrollcommand=carrinho_scrollbar.set)
        
        # Interações no carrinho: duplo clique e tecla Delete para decrementar
        self.carrinho_tree.bind('<Double-1>', self._on_tree_double_click)
        self.carrinho_tree.bind('<Delete>', self._on_delete_key)

        # Frame do total
        total_frame = ttk.Frame(right_frame)
        total_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        total_frame.columnconfigure(1, weight=1)
        
        ttk.Label(total_frame, text="TOTAL:", style='Header.TLabel').grid(row=0, column=0, sticky=tk.W)
        self.total_var = tk.StringVar(value="$ 0,00")
        self.total_label = ttk.Label(total_frame, textvariable=self.total_var, 
                                   font=('Arial', 14, 'bold'),
                                   foreground='#e74c3c')
        self.total_label.grid(row=0, column=1, sticky=tk.E)
        
        # Valor do baú (50% do total)
        ttk.Label(total_frame, text="Valor da Mecânica:", style='Header.TLabel').grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.bau_var = tk.StringVar(value="$ 0,00")
        self.bau_label = ttk.Label(total_frame, textvariable=self.bau_var, 
                                  font=('Arial', 12, 'bold'),
                                  foreground='#3498db')
        self.bau_label.grid(row=1, column=1, sticky=tk.E, pady=(5, 0))
        
        # Botão calcular
        calc_button = ttk.Button(total_frame, text="💰 Calcular Total", 
                                command=self.calcular_total, style='Custom.TButton')
        calc_button.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Frame inferior - Tabela de preços
        bottom_frame = ttk.LabelFrame(main_frame, text="Tabela de Preços", padding="10")
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.rowconfigure(0, weight=1)
        
        # Text widget para tabela de preços
        self.precos_text = scrolledtext.ScrolledText(bottom_frame, height=8, font=('Courier', 9))
        self.precos_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Carregar dados iniciais
        self.carregar_itens()
        self.atualizar_tabela_precos()
        self.atualizar_total()
        
        # Verificar atualizações em background
        if ATUALIZADOR_DISPONIVEL:
            self.verificar_atualizacoes()
    
    def carregar_itens(self):
        """Carrega itens na lista baseado na categoria selecionada"""
        self.itens_listbox.delete(0, tk.END)
        
        categoria = self.categoria_var.get()
        
        if categoria == "Todas":
            itens = self.todos_itens
        elif categoria == "Peças Individuais":
            itens = self.tabela_precos
        elif categoria == "Peças Genéricas":
            itens = self.pecas
        else:
            itens = {}
        
        # Filtrar por busca se houver texto
        busca_texto = self.busca_var.get().lower()
        itens_filtrados = {}
        
        for item, preco in itens.items():
            if not busca_texto or busca_texto in item.lower():
                itens_filtrados[item] = preco
        
        # Ordenar alfabeticamente
        for item, preco in sorted(itens_filtrados.items()):
            self.itens_listbox.insert(tk.END, f"{item} - $ {preco:,}")
    
    def filtrar_itens(self, event=None):
        """Filtra itens baseado na categoria selecionada"""
        self.carregar_itens()
    
    def filtrar_por_busca(self, *args):
        """Filtra itens baseado no texto de busca"""
        self.carregar_itens()
    
    def on_double_click(self, event):
        """Manipula o duplo clique na lista de itens"""
        # Obter item selecionado
        selection = self.itens_listbox.curselection()
        if not selection:
            return
        
        # Selecionar o item na lista
        self.itens_listbox.selection_clear(0, tk.END)
        self.itens_listbox.selection_set(selection[0])
        self.itens_listbox.activate(selection[0])
        
        # Adicionar ao carrinho automaticamente
        self.adicionar_item()
    
    def adicionar_item(self):
        """Adiciona item selecionado ao carrinho"""
        try:
            # Obter item selecionado
            selection = self.itens_listbox.curselection()
            if not selection:
                messagebox.showwarning("Aviso", "Selecione um item da lista!")
                return
            
            item_text = self.itens_listbox.get(selection[0])
            item_name = item_text.split(" - $")[0]
            
            # Obter quantidade
            quantidade = int(self.quantidade_var.get())
            if quantidade <= 0:
                messagebox.showwarning("Aviso", "Quantidade deve ser maior que zero!")
                return
            
            # Obter preço
            preco = self.todos_itens.get(item_name)
            if preco is None:
                messagebox.showerror("Erro", "Item não encontrado!")
                return
            
            # Adicionar ao carrinho
            self.carrinho.append({
                'item': item_name,
                'preco': preco,
                'quantidade': quantidade,
                'subtotal': preco * quantidade
            })
            
            # Atualizar interface
            self.atualizar_carrinho()
            self.atualizar_total()
            
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número válido!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar item: {e}")
    
    def atualizar_carrinho(self):
        """Atualiza a exibição do carrinho"""
        # Limpar treeview
        for item in self.carrinho_tree.get_children():
            self.carrinho_tree.delete(item)
        
        # Adicionar itens
        for item in self.carrinho:
            self.carrinho_tree.insert('', 'end', values=(
                item['item'],
                item['quantidade'],
                f"$ {item['preco']:,}",
                f"$ {item['subtotal']:,}"
            ))
    
    def atualizar_total(self):
        """Atualiza o total do carrinho"""
        total = sum(item['subtotal'] for item in self.carrinho)
        
        # Aplicar desconto de 10% se estiver ativo
        if self.desconto_ativo:
            total = total * 0.9  # 10% de desconto
        
        self.total_var.set(f"$ {total:,.0f}")
        
        # Calcular valor do baú (50% do total)
        valor_bau = total * 0.5
        self.bau_var.set(f"$ {valor_bau:,.0f}")
    
    def calcular_total(self):
        """Calcula e exibe o total final"""
        if not self.carrinho:
            messagebox.showwarning("Aviso", "Carrinho vazio!")
            return
        
        total_bruto = sum(item['subtotal'] for item in self.carrinho)
        desconto_valor = 0
        
        # Aplicar desconto se estiver ativo
        if self.desconto_ativo:
            desconto_valor = total_bruto * 0.1
            total = total_bruto - desconto_valor
        else:
            total = total_bruto
        
        valor_bau = total * 0.5
        
        # Criar relatório
        relatorio = "="*50 + "\n"
        relatorio += "    ORÇAMENTO DE REPAROS - EQUIPE Death Row Garage\n"
        relatorio += "="*50 + "\n\n"
        
        for item in self.carrinho:
            relatorio += f"• {item['quantidade']}x {item['item']}\n"
            relatorio += f"  Preço unitário: $ {item['preco']:,}\n"
            relatorio += f"  Subtotal: $ {item['subtotal']:,}\n\n"
        
        relatorio += "-"*50 + "\n"
        relatorio += f"SUBTOTAL: $ {total_bruto:,.0f}\n"
        
        if self.desconto_ativo:
            relatorio += f"DESCONTO (10%): -$ {desconto_valor:,.0f}\n"
        
        relatorio += f"TOTAL GERAL: $ {total:,.0f}\n"
        relatorio += f"Valor da Mecânica: $ {valor_bau:,.0f}\n"
        relatorio += "="*50 + "\n"
        relatorio += "Atenciosamente, Equipe Death Row Garage."
        
        # Mostrar relatório
        messagebox.showinfo("Orçamento Calculado", relatorio)

    def remover_item_selecionado(self):
        """Decrementa a quantidade do item selecionado; remove se chegar a 0"""
        selection = self.carrinho_tree.selection()
        if not selection:
            return
        item_id = selection[0]
        index_na_view = self.carrinho_tree.index(item_id)
        if 0 <= index_na_view < len(self.carrinho):
            item = self.carrinho[index_na_view]
            nova_qtd = max(0, int(item['quantidade']) - 1)
            if nova_qtd == 0:
                self.carrinho.pop(index_na_view)
            else:
                item['quantidade'] = nova_qtd
                item['subtotal'] = item['preco'] * nova_qtd
            self.atualizar_carrinho()
            self.atualizar_total()

    def _on_delete_key(self, event):
        """Atalho Delete para decrementar quantidade do item selecionado"""
        self.remover_item_selecionado()

    def _on_tree_double_click(self, event):
        """Duplo clique no carrinho para decrementar quantidade"""
        # Identificar item na posição do clique
        region = self.carrinho_tree.identify('region', event.x, event.y)
        if region != 'cell':
            return
        item_id = self.carrinho_tree.identify_row(event.y)
        if not item_id:
            return
        # Selecionar o item clicado para unificar comportamento com remoção
        self.carrinho_tree.selection_set(item_id)
        self.remover_item_selecionado()
 
    def limpar_carrinho(self):
        """Limpa o carrinho e aplica desconto se houver itens"""
        if not self.carrinho:
            messagebox.showinfo("Info", "Carrinho já está vazio!")
            return
        
        # Calcular total antes de limpar
        total_bruto = sum(item['subtotal'] for item in self.carrinho)
        desconto_valor = 0
        total_final = total_bruto
        
        if self.desconto_ativo:
            desconto_valor = total_bruto * 0.1
            total_final = total_bruto - desconto_valor
        
        valor_bau = total_final * 0.5
        
        if messagebox.askyesno("Confirmar", "Deseja limpar o carrinho?"):
            # Mostrar resumo antes de limpar
            resumo = "="*50 + "\n"
            resumo += "    RESUMO DO ORÇAMENTO\n"
            resumo += "="*50 + "\n\n"
            resumo += f"SUBTOTAL: $ {total_bruto:,.0f}\n"
            
            if self.desconto_ativo:
                resumo += f"DESCONTO (10%): -$ {desconto_valor:,.0f}\n"
            
            resumo += f"TOTAL: $ {total_final:,.0f}\n"
            resumo += f"Valor da Mecânica: $ {valor_bau:,.0f}\n"
            resumo += "="*50
            
            messagebox.showinfo("Orçamento Final", resumo)
            
            # Limpar carrinho
            self.carrinho = []
            self.desconto_ativo = False  # Resetar desconto
            self.btn_desconto.config(text="🎁 Aplicar Desconto 10%")
            self.atualizar_carrinho()
            self.atualizar_total()
            messagebox.showinfo("Sucesso", "Carrinho limpo!")
    
    def toggle_desconto(self):
        """Ativa ou desativa o desconto de 10%"""
        if not self.carrinho:
            messagebox.showwarning("Aviso", "Adicione itens ao carrinho primeiro!")
            return
        
        self.desconto_ativo = not self.desconto_ativo
        
        if self.desconto_ativo:
            self.btn_desconto.config(text="❌ Remover Desconto 10%")
            messagebox.showinfo("Desconto", "Desconto de 10% aplicado!")
        else:
            self.btn_desconto.config(text="🎁 Aplicar Desconto 10%")
            messagebox.showinfo("Desconto", "Desconto removido!")
        
        # Atualizar total com/ sem desconto
        self.atualizar_total()
    
    def atualizar_tabela_precos(self):
        """Atualiza a exibição da tabela de preços"""
        self.precos_text.delete(1.0, tk.END)
        
        tabela = "TABELA DE PREÇOS - EQUIPE Death Row Garage\n"
        tabela += "="*50 + "\n\n"
        
        # Peças individuais
        tabela += "PEÇAS INDIVIDUAIS:\n"
        for item, preco in sorted(self.tabela_precos.items()):
            tabela += f"  {item:<20} = $ {preco:,}\n"
        
        tabela += "\nPEÇAS GENÉRICAS:\n"
        for item, preco in sorted(self.pecas.items()):
            tabela += f"  {item:<20} = $ {preco:,}\n"
        
        self.precos_text.insert(1.0, tabela)
    
    def verificar_atualizacoes(self):
        """Verifica atualizações ao iniciar"""
        def check():
            try:
                atualizador = AtualizadorApp()
                
                # Verificar se MTA está rodando ANTES de tentar verificar atualizações
                if atualizador.mta_esta_rodando():
                    # Se MTA estiver rodando, não verificar atualizações automaticamente
                    # para evitar problemas com anti-cheat
                    print("MTA detectado. Verificação automática de atualizações cancelada para evitar ban.")
                    return
                
                resultado = atualizador.verificar_atualizacao_completo()
                
                sucesso, dados = resultado
                
                if not sucesso:
                    # Se o erro for porque MTA está rodando, não mostrar nada (silencioso)
                    erro = dados.get('erro', 'Erro desconhecido') if dados else 'Erro desconhecido'
                    if 'MTA' not in str(erro):
                        # Outros erros podem ser mostrados em modo debug
                        print(f"Erro ao verificar atualizações: {erro}")
                    return
                
                # Verificar se há atualização
                tem_atualizacao = dados.get('tem_atualizacao', False)
                versao_remota = dados.get('versao_remota', '')
                changelog = dados.get('changelog', '')
                url_download = dados.get('url_download', '')
                arquivo_existe = dados.get('arquivo_existe', False)
                
                if tem_atualizacao and arquivo_existe:
                    # Mostrar diálogo de atualização
                    self.root.after(0, lambda: self.mostrar_dialogo_atualizacao(
                        versao_remota, changelog, atualizador, url_download))
                elif tem_atualizacao and not arquivo_existe:
                    # Há atualização mas arquivo não encontrado - não mostrar (silencioso)
                    print(f"Atualização {versao_remota} disponível mas arquivo não encontrado na release")
            except Exception as e:
                print(f"Erro ao verificar atualizações: {e}")
        
        threading.Thread(target=check, daemon=True).start()
    
    def verificar_atualizacoes_manual(self):
        """Verifica atualizações manualmente (botão)"""
        # Desabilitar botão durante verificação
        self.btn_atualizar.config(state='disabled', text="🔄 Verificando...")
        
        def check():
            try:
                atualizador = AtualizadorApp()
                
                # Verificar se MTA está rodando ANTES de tentar verificar atualizações
                if atualizador.mta_esta_rodando():
                    self.root.after(0, lambda: self.mostrar_aviso_mta())
                    self.root.after(0, lambda: self.btn_atualizar.config(state='normal', text="🔄 Verificar Atualizações"))
                    return
                
                resultado = atualizador.verificar_atualizacao_completo()
                
                self.root.after(0, lambda: self.processar_resultado_verificacao(resultado, atualizador))
            except Exception as e:
                self.root.after(0, lambda: self.mostrar_erro_verificacao(f"Erro: {e}"))
                self.root.after(0, lambda: self.btn_atualizar.config(state='normal', text="🔄 Verificar Atualizações"))
        
        threading.Thread(target=check, daemon=True).start()
    
    def mostrar_aviso_mta(self):
        """Mostra aviso quando MTA está rodando"""
        messagebox.showwarning(
            "⚠️ MTA Detectado",
            "O MTA (Multi Theft Auto) está rodando no momento.\n\n"
            "Para evitar problemas com o anti-cheat do servidor, "
            "a verificação de atualizações foi cancelada.\n\n"
            "Por favor, feche o MTA antes de verificar atualizações."
        )
    
    def processar_resultado_verificacao(self, resultado, atualizador):
        """Processa o resultado da verificação"""
        self.btn_atualizar.config(state='normal', text="🔄 Verificar Atualizações")
        
        sucesso, dados = resultado
        
        if not sucesso:
            # Mostrar erro detalhado
            erro = dados.get('erro', 'Erro desconhecido')
            detalhes = dados.get('detalhes', '')
            self.mostrar_erro_verificacao(erro, detalhes)
            return
        
        # Verificar se há atualização
        tem_atualizacao = dados.get('tem_atualizacao', False)
        versao_remota = dados.get('versao_remota', '')
        versao_atual = dados.get('versao_atual', '')
        changelog = dados.get('changelog', '')
        url_download = dados.get('url_download', '')
        arquivo_existe = dados.get('arquivo_existe', False)
        
        if tem_atualizacao:
            if arquivo_existe:
                self.mostrar_dialogo_atualizacao(versao_remota, changelog, atualizador, url_download)
            else:
                messagebox.showwarning(
                    "Atualização Disponível",
                    f"Versão {versao_remota} disponível!\n\n"
                    f"Porém, o arquivo executável não foi encontrado na release.\n\n"
                    f"Verifique se o arquivo foi enviado corretamente na release do GitHub."
                )
        else:
            messagebox.showinfo(
                "Atualização",
                f"Você está usando a versão mais recente!\n\n"
                f"Versão atual: {versao_atual}\n"
                f"Versão no GitHub: {versao_remota}"
            )
    
    def mostrar_erro_verificacao(self, erro, detalhes=""):
        """Mostra erro na verificação"""
        mensagem = f"Erro ao verificar atualizações:\n\n{erro}"
        if detalhes:
            mensagem += f"\n\nDetalhes:\n{detalhes}"
        messagebox.showerror("Erro", mensagem)
    
    def mostrar_dialogo_atualizacao(self, versao, changelog, atualizador, url_download):
        """Mostra diálogo de atualização"""
        mensagem = f"🆕 Nova versão {versao} disponível!\n\n"
        if changelog:
            mensagem += f"O que há de novo:\n{changelog}\n\n"
        mensagem += "Deseja atualizar agora?"
        
        resposta = messagebox.askyesno(
            "Atualização Disponível",
            mensagem,
            icon='question'
        )
        
        if resposta:
            self.baixar_e_instalar_atualizacao(atualizador, url_download)
    
    def baixar_e_instalar_atualizacao(self, atualizador, url_download):
        """Baixa e instala a atualização"""
        # Criar janela de progresso
        progress_window = tk.Toplevel(self.root)
        progress_window.title("Atualizando...")
        progress_window.geometry("400x150")
        progress_window.configure(bg='#2c3e50')
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Centralizar janela
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (150 // 2)
        progress_window.geometry(f"400x150+{x}+{y}")
        
        label = tk.Label(progress_window, 
                        text="Baixando atualização...\nPor favor, aguarde.",
                        bg='#2c3e50', fg='#ecf0f1',
                        font=('Arial', 10))
        label.pack(pady=20)
        
        progress_window.update()
        
        def download():
            try:
                caminho_novo = atualizador.baixar_atualizacao(url_download)
                if caminho_novo:
                    progress_window.after(0, lambda: label.config(
                        text="Instalando atualização...\nO aplicativo será reiniciado."
                    ))
                    progress_window.update()
                    
                    if atualizador.instalar_atualizacao(caminho_novo):
                        progress_window.after(0, lambda: messagebox.showinfo(
                            "Atualização",
                            "Atualização concluída!\nO aplicativo será reiniciado."
                        ))
                        self.root.after(1000, self.root.quit)
                    else:
                        progress_window.after(0, lambda: messagebox.showerror(
                            "Erro",
                            "Erro ao instalar atualização."
                        ))
                        progress_window.after(0, progress_window.destroy)
                else:
                    progress_window.after(0, lambda: messagebox.showerror(
                        "Erro",
                        "Erro ao baixar atualização.\nVerifique sua conexão com a internet."
                    ))
                    progress_window.after(0, progress_window.destroy)
            except Exception as e:
                progress_window.after(0, lambda: messagebox.showerror(
                    "Erro",
                    f"Erro durante atualização:\n{e}"
                ))
                progress_window.after(0, progress_window.destroy)
        
        threading.Thread(target=download, daemon=True).start()

def main():
    """Função principal"""
    root = tk.Tk()
    app = CalculadoraReparosGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
