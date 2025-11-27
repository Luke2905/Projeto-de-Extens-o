import streamlit as st

def menu():
    st.sidebar.title("Menu de Navegação")
    st.sidebar.markdown("Escolha uma opção abaixo para começar.")

    st.sidebar.divider()

    st.sidebar.page_link(page="app.py", label="Home")

    st.sidebar.page_link(page="pages/pdv.py", label="Ponto de Venda")
        
    st.sidebar.page_link(page="pages/cadProdutos.py", label="Cadastro de Produtos")

    st.sidebar.page_link(page="pages/produtosPage.py", label="Ver Produtos")

    st.sidebar.page_link(page="pages/gestaoPedidos.py", label="Gestão de pedidos")
