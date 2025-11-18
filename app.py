import streamlit as st

st.sidebar.title("Menu de Navegação")
st.sidebar.markdown("Escolha uma opção abaixo para começar.")

st.sidebar.divider()

st.sidebar.page_link(page="app.py", label="Home")
     
st.sidebar.page_link(page="pages/cadProdutos.py", label="Cadastro de Produtos")

st.sidebar.page_link(page="pages/produtosPage.py", label="Ver Produtos")


st.title("Bem-vindo ao Sistema de Gestão de Pedidos")

st.markdown(
    """
    Este é o seu sistema de gestão de pedidos
    
    Use o menu na **barra lateral à esquerda** para navegar
    pelas funcionalidades.
    """
)
