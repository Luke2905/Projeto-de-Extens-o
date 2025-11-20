# pages/2_Cadastrar.py
import streamlit as st
from classes.produto import Produto
from classes.categoria import Categoria
from decimal import Decimal
from components.menu import menu

# Instancia o DAO
dao_produto = Produto()
dao_categoria = Categoria()

# Menu
menu()

st.title("Cadastrar Novo Produto")

# O MESMO formulário que tínhamos antes
with st.form(key="form_cadastro_produto", clear_on_submit=True):
    nome_input = st.text_input("Nome do Produto", placeholder="X-Exemplo")
    desc_input = st.text_input("Descrição do Produto", placeholder="Lanche X...")
    preco_input = st.number_input("Preço (R$)", min_value=0.01, step=0.01, format="%.2f")
    
    list_cat = dao_categoria.listar_categorias() #Gera lista de categorias 

    mapa_categorias = {c['nome']: c['id_categoria'] for c in list_cat}#Exibe a lista no select para o user

    categoria_selecionada = st.selectbox("Categorias", options=list(mapa_categorias.keys())) # Select

    submit_button = st.form_submit_button(label="Salvar Produto")

# A MESMA lógica de salvamento
if submit_button:
    id_categoria_final = mapa_categorias[categoria_selecionada]
    if nome_input and preco_input > 0:
        try:
            preco_decimal = Decimal(f"{preco_input:.2f}")
            dao_produto.salvar(nome_input, desc_input, preco_decimal, id_categoria_final)
            st.success(f"Produto '{nome_input}' salvo com sucesso!")
            
            # ATENÇÃO: Como a tabela está em OUTRA página,
            # não precisamos mais limpar o cache daqui.
            # O cache será limpo quando a página da lista for acessada.

        except Exception as e:
            st.error(f"Erro ao salvar o produto: {e}")
    else:
        st.warning("Por favor, preencha o nome e um preço válido.")