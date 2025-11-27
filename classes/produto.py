from servise.database import get_conexao

#Classe dos Produtos
class Produto:

    #Metodo para listar produtos cadastrados
    def listar_produtos(self):
        produtos = []
        try:
            with get_conexao() as conexao:
                with conexao.cursor(dictionary=True) as cursor:
                    query = "SELECT * FROM produto"
                    cursor.execute(query)
                    produtos = cursor.fetchall()
            return produtos
        except Exception as e:
            print(f"Erro ao Listar produtos: {e}")
            return []
    
    #Metodo para Salva um novo produto ou atualiza um existente.
    def salvar(self, nome, descricao, preco, id_categoria):
        
        try:
            with get_conexao() as conexao:
                with conexao.cursor() as cursor:
                    query = "INSERT INTO produto (nome, descricao, preco, id_categoria) VALUES (%s, %s, %s, %s)"
                    dados = (nome, descricao, preco, id_categoria)
                    cursor.execute(query, dados)
                    
                    conexao.commit()
                    
                    print(f"Produto '{nome}' salvo com sucesso!")
                    return cursor.lastrowid # Retorna o ID do produto inserido

        except Exception as e:
            print(f"Erro ao salvar produto: {e}")
            return None

    # Atualiza um produto existente baseado no seu ID.
    def atualizar(self, id_produto, nome, descricao, preco, id_categoria):
        try:
            with get_conexao() as conexao:
                with conexao.cursor() as cursor:
                    query = """
                        UPDATE produto
                        SET nome = %s, descricao = %s, preco = %s, id_categoria = %s
                        WHERE id_produto = %s 
                    """
                    dados = (nome, descricao, preco, id_categoria, id_produto)
                    cursor.execute(query, dados)
                    
                    conexao.commit()
                    
                    print(f"Produto ID {id_produto} atualizado com sucesso!")
                    return cursor.rowcount 

        except Exception as e:
            print(f"Erro ao atualizar produto ID {id_produto}: {e}")
            return None

   # Deleta um produto do banco de dados usando seu ID.
    def deletar(self, id_produto):
        try:
            with get_conexao() as conexao:
                with conexao.cursor() as cursor:
                    query = "DELETE FROM produto WHERE id_produto = %s"
                    dados = (id_produto,) 
                    cursor.execute(query, dados)
                    
                    conexao.commit()
                    
                    print(f"Produto ID {id_produto} deletado com sucesso!")
                    return cursor.rowcount

        except Exception as e:
            print(f"Erro ao deletar produto ID {id_produto}: {e}")
            return None

    # Busca e retorna um produto específico pelo seu ID.
    def buscar_por_id(self, id_produto):

        produto = None
        try:
            with get_conexao() as conexao:
                with conexao.cursor(dictionary=True) as cursor:
                    query = "SELECT * FROM produto WHERE id_produto = %s LIMIT 1"
                    dados = (id_produto,)
                    cursor.execute(query, dados)
                    
                    produto = cursor.fetchone() 
            
            return produto # Retorna o dicionário do produto ou None
        
        except Exception as e:
            print(f"Erro ao buscar produto ID {id_produto}: {e}")
            return None
        
    # Registra venda 
    def realizar_venda(self, total_venda, itens_carrinho):
        try:
            with get_conexao() as conn:
                conn.start_transaction()
                cursor = conn.cursor()

                resumo_texto = ", ".join([f"{item['qtd']}x {item['nome']}" for item in itens_carrinho])
                
                cursor.execute("INSERT INTO venda (total, resumo_itens) VALUES (%s, %s)", (total_venda, resumo_texto))
                id_venda_gerada = cursor.lastrowid
                
                query_baixa = "UPDATE produto SET estoque = estoque - %s WHERE id_produto = %s"
                
                query_hist = """
                    INSERT INTO movimentacao_estoque (id_produto, tipo, quantidade, observacao) 
                    VALUES (%s, 'Saida', %s, %s)
                """
                
                for item in itens_carrinho:
  
                    # Baixa o Estoque
                    cursor.execute(query_baixa, (item['qtd'], item['id_produto']))
                    
                    # Registra no Histórico
                    obs = f"Venda PDV #{id_venda_gerada}"
                    cursor.execute(query_hist, (item['id_produto'], item['qtd'], obs))

                conn.commit()
                return True
                
        except Exception as e:
            print(f"Erro na venda: {e}")
            return False

    #Atualiza estoque
    def repor_estoque(self, id_produto, quantidade):
        """ Método para dar entrada manual (usar na gestão de produtos) """
        try:
            with get_conexao() as conn:
                conn.start_transaction()
                cursor = conn.cursor()
                
                cursor.execute("UPDATE produto SET estoque = estoque + %s WHERE id_produto = %s", (quantidade, id_produto))
                
                cursor.execute("""
                    INSERT INTO movimentacao_estoque (id_produto, tipo, quantidade, observacao) 
                    VALUES (%s, 'Entrada', %s, 'Reposição Manual')
                """, (id_produto, quantidade))
                
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao repor estoque: {e}")
            return False