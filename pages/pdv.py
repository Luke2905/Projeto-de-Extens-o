import streamlit as st
from classes.produto import Produto
from classes.pedido import Pedido
from components.menu import menu

# 1. Configuração da Página
st.set_page_config(page_title="Ponto de Venda", layout="wide")
#Menu
menu()

# 2. Instancia os DAOs (Objetos de acesso ao banco)
dao_produto = Produto()
dao_pedido = Pedido()

# 3. Inicializa o Carrinho na Memória (Session State)
# Estrutura: { id_produto : quantidade }
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = {}

# --- FUNÇÕES AUXILIARES ---
def adicionar_item(id_produto):
    """ Adiciona +1 ao item no carrinho """
    if id_produto in st.session_state.carrinho:
        st.session_state.carrinho[id_produto] += 1
    else:
        st.session_state.carrinho[id_produto] = 1

def remover_item(id_produto):
    """ Remove o item do carrinho """
    if id_produto in st.session_state.carrinho:
        del st.session_state.carrinho[id_produto]

def limpar_carrinho():
    """ Zera o carrinho """
    st.session_state.carrinho = {}

# ====================================================
# INÍCIO DO LAYOUT
# ====================================================
st.title("Frente de Caixa")

# Divide a tela: 70% Vitrine (Esquerda) | 30% Caixa (Direita)
col_vitrine, col_caixa = st.columns([3, 1])

# Carrega todos os produtos do banco UMA vez
todos_produtos = dao_produto.listar_produtos()

# ----------------------------------------------------
# 🛍️ LADO ESQUERDO: VITRINE DE PRODUTOS
# ----------------------------------------------------
with col_vitrine:
    # Barra de Pesquisa
    termo = st.text_input("🔍 Buscar Produto", placeholder="Digite o nome ou código...", label_visibility="collapsed")
    
    # Filtro Python (Rápido e não acessa banco de novo)
    produtos_filtrados = [
        p for p in todos_produtos 
        if termo.lower() in p['nome'].lower()
    ]
    
    if not produtos_filtrados:
        st.warning("Nenhum produto encontrado.")
    else:
        # GRID SYSTEM: 3 produtos por linha
        colunas = st.columns(3)
        
        for i, produto in enumerate(produtos_filtrados):
            col_atual = colunas[i % 3] # Distribui: 0, 1, 2, 0, 1, 2...
            
            with col_atual:
                # O Container cria a borda do "Card"
                with st.container(border=True):
                    st.subheader(produto['nome'])
                    
                    # Controle Visual de Estoque
                    # Usa .get() para evitar erro se a coluna não existir
                    qtd_estoque = produto.get('estoque', 0)
                    
                    if qtd_estoque < 5:
                        cor_estoque = "red"
                    else:
                        cor_estoque = "green"
                        
                    st.markdown(f"Estoque: :{cor_estoque}[**{qtd_estoque}**]")
                    st.metric("Preço", f"R$ {produto['preco']:.2f}")
                    
                    # Botão de Adicionar
                    esgotado = qtd_estoque <= 0
                    texto_btn = "Esgotado 🚫" if esgotado else "Adicionar ➕"
                    
                    # Key única é obrigatória em loops
                    if st.button(texto_btn, key=f"add_{produto['id_produto']}", disabled=esgotado, use_container_width=True):
                        adicionar_item(produto['id_produto'])
                        st.toast(f"{produto['nome']} adicionado!", icon="🛒")

# ----------------------------------------------------
#  LADO DIREITO: O CUPOM / CAIXA
# ----------------------------------------------------
with col_caixa:
    with st.container(border=True):
        st.header("Pedido Atual")
        st.divider()
        
        # Campo para Nome do Cliente (Obrigatório para Gestão de Pedidos)
        cliente_nome = st.text_input("Nome do Cliente / Mesa", placeholder="Ex: Mesa 10")
        
        st.divider()

        if not st.session_state.carrinho:
            st.info("Carrinho vazio.")
            st.caption("Selecione produtos ao lado.")
        else:
            total_geral = 0
            lista_para_backend = [] # Lista formatada para a classe Pedido
            
            # Itera sobre os itens do carrinho
            for id_prod, qtd in st.session_state.carrinho.items():
                # Busca os dados originais do produto na lista carregada
                dados = next((p for p in todos_produtos if p['id_produto'] == id_prod), None)
                
                if dados:
                    subtotal = dados['preco'] * qtd
                    total_geral += subtotal
                    
                    # Layout da Linha do Item (Qtd | Nome | Botão Lixo)
                    c1, c2, c3 = st.columns([1, 3, 1])
                    c1.write(f"**{qtd}x**")
                    c2.write(f"{dados['nome']}")
                    
                    if c3.button("🗑️", key=f"rem_{id_prod}"):
                        remover_item(id_prod)
                        st.rerun()
                    
                    # Monta o objeto para salvar no banco
                    lista_para_backend.append({
                        'id_produto': id_prod,
                        'qtd': qtd,
                        'preco': dados['preco'] # Importante para a tabela item_pedido
                    })
            
            st.divider()
            # Mostra o Total Grande
            st.metric("TOTAL A PAGAR", f"R$ {total_geral:.2f}")
            
            # --- BOTÕES DE AÇÃO ---
            col_b1, col_b2 = st.columns(2)
            
            # Botão Cancelar
            if col_b1.button("Cancelar", use_container_width=True):
                limpar_carrinho()
                st.rerun()
            
            # Botão Finalizar
            if col_b2.button("Finalizar ✅", type="primary", use_container_width=True):
                # Validação
                if not cliente_nome:
                    st.warning("⚠️ Preencha o nome do cliente!")
                else:
                    # Chama a Classe Pedido para salvar tudo
                    # Isso cria o pedido, salva os itens e baixa o estoque
                    sucesso = dao_pedido.criar_pedido(cliente_nome, total_geral, lista_para_backend)
                    
                    if sucesso:
                        st.balloons() # Efeito de festa
                        st.success(f"Pedido de {cliente_nome} enviado para a cozinha!")
                        limpar_carrinho()
                        st.rerun() # Recarrega para atualizar estoques na vitrine
                    else:
                        st.error("Erro ao registrar o pedido. Tente novamente.")