from servise.database import get_conexao

class Pedido:
    
    # 1. CRIAR PEDIDO (O Novo método do PDV)
    def criar_pedido(self, nome_cliente, total, itens_carrinho):
        try:
            with get_conexao() as conn:
                conn.start_transaction()
                cursor = conn.cursor()

                query_pedido = "INSERT INTO pedido (nome_cliente, valor_total, status) VALUES (%s, %s, 'Aguardando')"
                cursor.execute(query_pedido, (nome_cliente, total))
                id_pedido_gerado = cursor.lastrowid # Pega o ID novo

                query_item = """
                    INSERT INTO item_pedido (id_pedido, id_produto, quantidade, preco_unitario)
                    VALUES (%s, %s, %s, %s)
                """
                
                query_estoque = "UPDATE produto SET estoque = estoque - %s WHERE id_produto = %s"

                for item in itens_carrinho:
                    # Salva o item ligado ao pedido
                    cursor.execute(query_item, (id_pedido_gerado, item['id_produto'], item['qtd'], item['preco']))
                    
                    # Atualiza estoque
                    cursor.execute(query_estoque, (item['qtd'], item['id_produto']))

                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao criar pedido: {e}")
            return False

    # 2. LISTAR PEDIDOS 
    def listar_todos(self):
        try:
            with get_conexao() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM pedido ORDER BY field(status, 'Aguardando', 'Fazendo', 'Pronto', 'Entregue'), criado_em DESC")
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar: {e}")
            return []

    # 3. PEGAR ITENS DE UM PEDIDO 
    def buscar_itens_por_pedido(self, id_pedido):
        try:
            with get_conexao() as conn:
                cursor = conn.cursor(dictionary=True)
                query = """
                    SELECT i.quantidade, i.preco_unitario, p.nome 
                    FROM item_pedido i
                    JOIN produto p ON i.id_produto = p.id_produto
                    WHERE i.id_pedido = %s
                """
                cursor.execute(query, (id_pedido,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar itens: {e}")
            return []

    # 4. ATUALIZAR STATUS
    def atualizar_status(self, id_pedido, novo_status):
        try:
            with get_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE pedido SET status = %s WHERE id_pedido = %s", (novo_status, id_pedido))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao atualizar status: {e}")
            return False