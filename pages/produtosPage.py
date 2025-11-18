# pages/produtosPage.py
import streamlit as st
import pandas as pd
from classes.produto import Produto

# Instancia o DAO
dao_produto = Produto()

# --- Menu (Seu código, mantido) ---
st.sidebar.title("Menu de Navegação")
st.sidebar.markdown("Escolha uma opção abaixo para começar.")
st.sidebar.divider()
st.sidebar.page_link(page="app.py", label="Home")
st.sidebar.page_link(page="pages/cadProdutos.py", label="Cadastro de Produtos")
st.sidebar.page_link(page="pages/produtosPage.py", label="Ver Produtos")
st.sidebar.page_link(page="pages/pdv.py", label="Ponto de Venda")
# --- Fim do Menu ---

# Função de Carregar Dados
@st.cache_data
def carregar_dados():
    print("BUSCANDO DADOS NO BANCO...")
    return dao_produto.listar_produtos()

# ----------------------------------------------------
# ⬇️ NOVO: 1. DEFINIÇÃO DA FUNÇÃO DO MODAL ⬇️
# ----------------------------------------------------
# Usamos o decorador @st.dialog para transformar esta
# função em um pop-up.
@st.dialog("Editar Produto")
def abrir_modal_edicao(produto_edit):
    """ Esta função desenha o formulário de edição dentro do modal. """
    st.subheader(f"Editando: {produto_edit['nome']}")
    
    # O formulário fica DENTRO da função do dialog
    with st.form("form_edicao"):
        # Pré-preenchemos o formulário com os dados atuais
        nome = st.text_input("Nome", value=produto_edit['nome'])
        desc = st.text_area("Descrição", value=produto_edit.get('descricao', ''))
        preco = st.number_input("Preço", value=float(produto_edit['preco']), format="%.2f")
        cat_id = st.number_input("ID Categoria", value=int(produto_edit['id_categoria']), step=1)
        
        # Botões de ação do formulário
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("Salvar Alterações", type="primary"):
                # Chamamos o método de ATUALIZAR do DAO
                dao_produto.atualizar(produto_edit['id_produto'], nome, desc, preco, cat_id)
                st.success("Produto atualizado com sucesso!")
                
                # Limpa o state para fechar o modal
                st.session_state.produto_para_editar = None
                st.cache_data.clear() # Limpa o cache
                st.rerun() # Recarrega a página

        with col2:
            if st.form_submit_button("Cancelar"):
                # Apenas fecha o modal limpando o state
                st.session_state.produto_para_editar = None
                st.rerun()

# --- Fim da Definição do Modal ---


st.title("Produtos Cadastrados")

# ----------------------------------------------------
# ⬇️ LÓGICA DE PESQUISA (Igual) ⬇️
# ----------------------------------------------------
lista_produtos = carregar_dados()
termo_pesquisa = st.text_input("Buscar Produto", placeholder="Digite o nome do produto para filtrar...")

if termo_pesquisa:
    lista_filtrada = [
        prod for prod in lista_produtos 
        if termo_pesquisa.lower() in prod['nome'].lower()
    ]
else:
    lista_filtrada = lista_produtos
    
# ----------------------------------------------------
# ⬇️ NOVO: 2. LÓGICA DE CHAMADA DO MODAL ⬇️
# ----------------------------------------------------
# Verificamos se precisamos ABRIR o modal
if 'produto_para_editar' not in st.session_state:
    st.session_state.produto_para_editar = None

# Se um produto foi colocado no state...
if st.session_state.produto_para_editar:
    produto_para_chamar = st.session_state.produto_para_editar
    # ...nós simplesmente CHAMAMOS a função que definimos lá em cima
    abrir_modal_edicao(produto_para_chamar)

# ----------------------------------------------------
# ⬇️ TABELA MANUAL (Quase igual) ⬇️
# ----------------------------------------------------
if lista_filtrada:
    col_header = st.columns([3, 2, 2])
    col_header[0].subheader("Nome")
    col_header[1].subheader("Preço")
    col_header[2].subheader("Ações")
    st.divider()

    for produto in lista_filtrada:
        col_data = st.columns([3, 2, 2])
        col_data[0].write(produto['nome'])
        col_data[1].write(f"R$ {produto['preco']:.2f}")
        
        with col_data[2]:
            # O código dos botões "Editar" e "Deletar" fica IDÊNTICO
            if st.button("Editar", key=f"edit_{produto['id_produto']}", use_container_width=True):
                st.session_state.produto_para_editar = produto
                st.rerun()
            
            if st.button("Deletar", type="primary", key=f"del_{produto['id_produto']}", use_container_width=True):
                dao_produto.deletar(produto['id_produto'])
                st.success(f"Produto {produto['nome']} deletado!")
                st.cache_data.clear()
                st.rerun()
else:
    st.info("Nenhum produto encontrado com esse filtro.")

# Botão de recarregar (Igual)
if st.button("Atualizar Lista"):
    st.cache_data.clear()
    st.rerun()