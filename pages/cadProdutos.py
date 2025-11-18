# pages/2_Cadastrar.py
import streamlit as st
from classes.produto import Produto
from decimal import Decimal

# Instancia o DAO
dao_produto = Produto()

# Menu
# ===============================================================
st.sidebar.title("Menu de Navegação")
st.sidebar.markdown("Escolha uma opção abaixo para começar.")

st.sidebar.divider()

st.sidebar.page_link(page="app.py", label="Home")
     
st.sidebar.page_link(page="pages/cadProdutos.py", label="Cadastro de Produtos")

st.sidebar.page_link(page="pages/produtosPage.py", label="Ver Produtos")

st.sidebar.page_link(page="pages/pdv.py", label="Ponto de Venda")
#======================================================================

st.title("Cadastrar Novo Produto")

# O MESMO formulário que tínhamos antes
with st.form(key="form_cadastro_produto", clear_on_submit=True):
    nome_input = st.text_input("Nome do Produto", placeholder="X-Exemplo")
    desc_input = st.text_input("Descrição do Produto", placeholder="Lanche X...")
    preco_input = st.number_input("Preço (R$)", min_value=0.01, step=0.01, format="%.2f")
    cat_input = st.number_input("Código da Categoria", min_value=1)
    
    submit_button = st.form_submit_button(label="Salvar Produto")

# A MESMA lógica de salvamento
if submit_button:
    if nome_input and preco_input > 0:
        try:
            preco_decimal = Decimal(f"{preco_input:.2f}")
            dao_produto.salvar(nome_input, desc_input, preco_decimal, cat_input)
            st.success(f"Produto '{nome_input}' salvo com sucesso!")
            
            # ATENÇÃO: Como a tabela está em OUTRA página,
            # não precisamos mais limpar o cache daqui.
            # O cache será limpo quando a página da lista for acessada.

        except Exception as e:
            st.error(f"Erro ao salvar o produto: {e}")
    else:
        st.warning("Por favor, preencha o nome e um preço válido.")