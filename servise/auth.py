# servise/auth.py
import streamlit as st

def verificar_login():
    """
    Função para ser colocada no TOPO de todas as páginas.
    Se o usuário não estiver na sessão, chuta ele para a tela de login.
    """
    if 'usuario_logado' not in st.session_state or st.session_state['usuario_logado'] is None:
        st.warning("🔒 Você precisa fazer login para acessar essa página.")
        st.stop() # Para a execução do script da página imediatamente