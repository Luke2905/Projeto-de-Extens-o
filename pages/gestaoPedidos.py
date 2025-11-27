# pages/gestaoPedidos.py
import streamlit as st
from classes.pedido import Pedido
from components.menu import menu # (Se usar menu)

st.set_page_config(layout="wide", page_title="Cozinha / Gestão")
menu() 

st.title("Gestão de Pedidos")

dao = Pedido()

# Botão de refresh manual (útil para cozinha)
if st.button("🔄 Atualizar Pedidos"):
    st.rerun()

pedidos = dao.listar_todos()

if not pedidos:
    st.info("Nenhum pedido na fila.")
else:
    # Cria colunas para organizar visualmente (estilo Kanban simples vertical)
    status_cores = {
        'Aguardando': 'red',
        'Fazendo': 'orange',
        'Pronto': 'green',
        'Entregue': 'grey'
    }

    for p in pedidos:
        cor = status_cores.get(p['status'], 'blue')
        
        # O Expander cria uma caixa que abre e fecha
        with st.expander(f"#{p['id_pedido']} - {p['nome_cliente']} | Status: :{cor}[{p['status']}]"):
            
            c1, c2 = st.columns([2, 1])
            
            with c1:
                st.markdown("**Itens do Pedido:**")
                # Busca os itens desse pedido na hora (Lazy Loading)
                itens = dao.buscar_itens_por_pedido(p['id_pedido'])
                for item in itens:
                    st.text(f"- {item['quantidade']}x {item['nome']}")
                
                st.caption(f"Total: R$ {p['valor_total']:.2f} ...")

            with c2:
                st.markdown("**Mudar Status:**")
                
                # Botões de Ação Rápida
                if p['status'] == 'Aguardando':
                    if st.button("Começar a Fazer", key=f"faz_{p['id_pedido']}"):
                        dao.atualizar_status(p['id_pedido'], 'Fazendo')
                        st.rerun()
                
                elif p['status'] == 'Fazendo':
                    if st.button("Pronto!", key=f"pronto_{p['id_pedido']}"):
                        dao.atualizar_status(p['id_pedido'], 'Pronto')
                        st.rerun()

                elif p['status'] == 'Pronto':
                    if st.button("Entregue", key=f"ent_{p['id_pedido']}"):
                        dao.atualizar_status(p['id_pedido'], 'Entregue')
                        st.rerun()
                
                else:
                    st.write("✅ Pedido Finalizado.")