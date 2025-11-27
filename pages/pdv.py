# pages/pdv.py
import streamlit as st
from classes.produto import Produto
from components.menu import menu
# from components.menu import menu # (Se não estiver usando o router.py)

# 1. Configuração da Página
# layout="wide" é OBRIGATÓRIO para PDV ficar bom
st.set_page_config(page_title="Ponto de Venda", layout="wide")

st.title("Frente de Caixa 🏪")

menu()
# 2. Instancia o Banco
dao = Produto()

# 3. Inicializa o Carrinho na Memória
# Usaremos um dicionário: { id_produto : quantidade }
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = {}

# --- FUNÇÕES AUXILIARES DA TELA ---
def adicionar_item(id_produto):
    # Se já tem, aumenta +1. Se não tem, vira 1.
    if id_produto in st.session_state.carrinho:
        st.session_state.carrinho[id_produto] += 1
    else:
        st.session_state.carrinho[id_produto] = 1

def limpar_carrinho():
    st.session_state.carrinho = {}

def remover_item(id_produto):
    if id_produto in st.session_state.carrinho:
        del st.session_state.carrinho[id_produto]

# ====================================================
# LAYOUT: DIVISÃO DA TELA
# ====================================================
col_vitrine, col_caixa = st.columns([3, 1]) # 3 partes pra vitrine, 1 pro caixa

# Busca produtos do banco
todos_produtos = dao.listar_produtos()

# ----------------------------------------------------
# LADO ESQUERDO: VITRINE DE PRODUTOS
# ----------------------------------------------------
with col_vitrine:
    # Barra de Pesquisa
    termo = st.text_input("🔍 Buscar Produto", placeholder="Digite o nome...", label_visibility="collapsed")
    
    # Filtra a lista
    produtos_filtrados = [p for p in todos_produtos if termo.lower() in p['nome'].lower()]
    
    if not produtos_filtrados:
        st.warning("Nenhum produto encontrado.")
    else:
        # GRID SYSTEM: Vamos fazer 3 produtos por linha
        colunas = st.columns(3)
        
        for i, produto in enumerate(produtos_filtrados):
            col_atual = colunas[i % 3] # Lógica matemática para distribuir nas 3 colunas
            
            with col_atual:
                # O Container cria a borda do "Card"
                with st.container(border=True):
                    # Se tiver imagem no banco: st.image(produto['imagem'])
                    st.subheader(produto['nome'])
                    
                    # Mostra Estoque com cor
                    estoque = produto.get('estoque', 0)
                    cor_estoque = "red" if estoque < 5 else "green"
                    st.markdown(f"Estoque: :{cor_estoque}[**{estoque}**]")
                    
                    st.metric("Preço", f"R$ {produto['preco']:.2f}")
                    
                    # Botão de Adicionar
                    # Desabilita se não tiver estoque
                    esgotado = estoque <= 0
                    texto_btn = "Esgotado 🚫" if esgotado else "Adicionar ➕"
                    
                    # A key precisa ser única para cada botão!
                    if st.button(texto_btn, key=f"add_{produto['id_produto']}", disabled=esgotado, use_container_width=True):
                        adicionar_item(produto['id_produto'])
                        st.toast(f"{produto['nome']} adicionado!", icon="🛒")

# ----------------------------------------------------
# LADO DIREITO: O CAIXA (CUPOM)
# ----------------------------------------------------
with col_caixa:
    with st.container(border=True):
        st.header("Cupom Fiscal 🧾")
        st.divider()
        
        if not st.session_state.carrinho:
            st.info("Carrinho vazio.")
            st.caption("Clique nos produtos ao lado.")
        else:
            total_geral = 0
            lista_para_salvar = [] # Lista formatada para mandar pro banco
            
            # Loop pelos itens do carrinho
            for id_prod, qtd in st.session_state.carrinho.items():
                # Precisamos achar os dados do produto (nome, preço) baseado no ID
                # next() é um jeito rápido de achar um item numa lista
                dados = next((p for p in todos_produtos if p['id_produto'] == id_prod), None)
                
                if dados:
                    subtotal = dados['preco'] * qtd
                    total_geral += subtotal
                    
                    # Mostra na tela bonitinho
                    c1, c2, c3 = st.columns([3, 2, 1])
                    c1.write(f"**{qtd}x** {dados['nome']}")
                    c2.write(f"R$ {subtotal:.2f}")
                    if c3.button("🗑️", key=f"rem_{id_prod}"):
                        remover_item(id_prod)
                        st.rerun()
                    
                    # Prepara para salvar
                    lista_para_salvar.append({
                        "id_produto": id_prod,
                        "nome": dados['nome'],
                        "qtd": qtd
                    })
            
            st.divider()
            st.metric("TOTAL A PAGAR", f"R$ {total_geral:.2f}")
            
            # Botões de Ação
            col_b1, col_b2 = st.columns(2)
            
            if col_b1.button("Cancelar", use_container_width=True):
                limpar_carrinho()
                st.rerun()
            
            if col_b2.button("Finalizar ✅", type="primary", use_container_width=True):
                # Chama o backend
                sucesso = dao.realizar_venda(total_geral, lista_para_salvar)
                
                if sucesso:
                    st.balloons() # Festa!
                    st.success("Venda Realizada!")
                    limpar_carrinho()
                    st.rerun() # Recarrega pra atualizar o estoque na vitrine
                else:
                    st.error("Erro ao registrar venda.")