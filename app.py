# app.py
import streamlit as st
from classes.usuario import Usuario
from components.menu import menu # Supondo que você tenha criado aquele componente de menu
import time

# Configuração Inicial
st.set_page_config(page_title="Sistema Login", layout="centered")

# Inicializa a Sessão (Memória do navegador)
if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = None

# --- FUNÇÃO DA TELA DE LOGIN ---
def mostrar_login():
    st.title("Bem-vindo!")
    
    # Criamos abas para Login e Cadastro (pra facilitar seu teste)
    tab1, tab2 = st.tabs(["Entrar", "Criar Conta"])

    # ABA 1: LOGIN
    with tab1:
        with st.form("form_login"):
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            submit = st.form_submit_button("Acessar Sistema", type="primary")

            if submit:
                usuario_dao = Usuario()
                user = usuario_dao.login(email, senha)

                if user:
                    st.success(f"Login realizado! Olá, {user['nome_usuario']}")
                    st.session_state['usuario_logado'] = user # Salva na memória!
                    time.sleep(1)
                    st.rerun() # Recarrega a página para sumir com o login e mostrar o menu
                else:
                    st.error("E-mail ou senha incorretos.")

    # ABA 2: CADASTRO (Primeiro uso)
    with tab2:
        with st.form("form_cadastro"):
            st.write("Novo por aqui?")
            nome_new = st.text_input("Seu Nome")
            email_new = st.text_input("Seu E-mail")
            senha_new = st.text_input("Sua Senha", type="password")
            submit_new = st.form_submit_button("Cadastrar")

            if submit_new:
                usuario_dao = Usuario()
                if usuario_dao.cadastrar(nome_new, email_new, senha_new):
                    st.success("Conta criada com sucesso! Agora faça login na outra aba.")
                else:
                    st.error("Erro ao criar conta (talvez o e-mail já exista).")

# --- LÓGICA PRINCIPAL ---

if st.session_state['usuario_logado']:
    # === USUÁRIO ESTÁ LOGADO ===
    # Aqui carregamos o "Sistema Real"
    
    # Chama o menu lateral (que agora vai mostrar o botão de Sair)
    menu() 
    
    st.title("Sistema de Gerenciamento de Pedidos")
    st.write(f"Bem-vindo, **{st.session_state['usuario_logado']['nome_usuario']}**!")
    st.info("Use o menu lateral para navegar no sistema.")
    
else:
    # === USUÁRIO NÃO ESTÁ LOGADO ===
    mostrar_login()