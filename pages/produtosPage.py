# pages/produtosPage.py
import streamlit as st
import pandas as pd
from classes.produto import Produto
from components.menu import menu
from servise.auth import verificar_login # <--- Importe isso

# 1. VERIFICAÇÃO DE SEGURANÇA (Primeira coisa a rodar)
verificar_login()

# Instancia o DAO
dao_produto = Produto()

# Configuração da Página (Opcional, mas bom garantir)
st.set_page_config(page_title="Produtos", layout="wide")

# Menu da Aplicação
menu()

# Função de Carregar Dados
@st.cache_data
def carregar_dados():
    # print("BUSCANDO DADOS NO BANCO...") # Comentei para não poluir o terminal
    return dao_produto.listar_produtos()

# ----------------------------------------------------
# 1. DEFINIÇÃO DO MODAL (Igualzinho estava)
# ----------------------------------------------------
@st.dialog("Editar Produto")
def abrir_modal_edicao(produto_edit):
    """ Esta função desenha o formulário de edição dentro do modal. """
    st.subheader(f"Editando: {produto_edit['nome']}")
    
    with st.form("form_edicao"):
        nome = st.text_input("Nome", value=produto_edit['nome'])
        desc = st.text_area("Descrição", value=produto_edit.get('descricao', ''))
        preco = st.number_input("Preço", value=float(produto_edit['preco']), format="%.2f")
        cat_id = st.number_input("ID Categoria", value=int(produto_edit['id_categoria']), step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar Alterações", type="primary"):
                dao_produto.atualizar(produto_edit['id_produto'], nome, desc, preco, cat_id)
                st.success("Produto atualizado!")
                st.session_state.produto_para_editar = None
                st.cache_data.clear()
                st.rerun()

        with col2:
            if st.form_submit_button("Cancelar"):
                st.session_state.produto_para_editar = None
                st.rerun()

# ====================================================
# 🟦 HEADER ESTÁTICO (Fica fixo no topo)
# ====================================================
st.title("Produtos Cadastrados")

# Carrega dados
lista_produtos = carregar_dados()

# Layout: Barra de Pesquisa (Esquerda) + Botão Atualizar (Direita)
col_search, col_btn = st.columns([4, 1])

with col_search:
    termo_pesquisa = st.text_input("Buscar Produto", placeholder=" Digite o nome...", label_visibility="collapsed")

with col_btn:
    if st.button("🔄 Atualizar Lista", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.divider() # Linha separando o cabeçalho do corpo

# Lógica de Filtro
if termo_pesquisa:
    lista_filtrada = [
        prod for prod in lista_produtos 
        if termo_pesquisa.lower() in prod['nome'].lower()
    ]
else:
    lista_filtrada = lista_produtos

# Lógica de Chamada do Modal (Invisível, mas essencial)
if 'produto_para_editar' not in st.session_state:
    st.session_state.produto_para_editar = None

if st.session_state.produto_para_editar:
    abrir_modal_edicao(st.session_state.produto_para_editar)

# Body
# height=600 define a altura fixa. O que passar disso, cria barra de rolagem.
with st.container(height=450, border=True):
    
    if lista_filtrada:
        # Cabeçalho da Tabela
        # Dica: Coloquei DENTRO do container para alinhar com as colunas de dados
        col_header = st.columns([3, 2, 2])
        col_header[0].markdown("**Nome**")
        col_header[1].markdown("**Preço**")
        col_header[2].markdown("**Ações**")
        st.markdown("---")

        # Loop dos Dados
        for produto in lista_filtrada:
            col_data = st.columns([3, 2, 2])
            
            # Coluna 1: Nome
            col_data[0].write(produto['nome'])
            
            # Coluna 2: Preço
            col_data[1].write(f"R$ {produto['preco']:.2f}")
            
            # Coluna 3: Botões
            with col_data[2]:
                c_edit, c_del = st.columns(2)
                
                # Botão Editar (Compacto)
                if c_edit.button("✏️", key=f"edit_{produto['id_produto']}"):
                    st.session_state.produto_para_editar = produto
                    st.rerun()
                
                # Botão Deletar (Compacto e Vermelho)
                if c_del.button("🗑️", type="primary", key=f"del_{produto['id_produto']}"):
                    dao_produto.deletar(produto['id_produto'])
                    st.toast(f"Produto {produto['nome']} deletado!")
                    st.cache_data.clear()
                    st.rerun()
    else:
        st.info("Nenhum produto encontrado com esse filtro.")