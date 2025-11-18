from servise.database import get_conexao

#Classe dos Produtos
class Produto:

    #Metodo para listar produtos cadastrados
    def listar_produtos(self):
        produtos = []
        try:
            with get_conexao() as conexao:
                with conexao.cursor(dictionary=True) as cursor:
                    # Boa prática: especifique as colunas
                    query = "SELECT id_produto, nome, descricao, preco, id_categoria FROM produto"
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
            # Se deu erro, o 'get_conexao' já deu rollback()
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
                    # A ordem dos dados importa! O 'id_produto' deve ser o último
                    dados = (nome, descricao, preco, id_categoria, id_produto)
                    cursor.execute(query, dados)
                    
                    conexao.commit()
                    
                    print(f"Produto ID {id_produto} atualizado com sucesso!")
                    # Retorna a contagem de linhas afetadas (deve ser 1)
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
                    # Precisa ser uma tupla, mesmo com um item (por isso a vírgula)
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
                    
                    # fetchone() pega apenas UM resultado, em vez de uma lista
                    produto = cursor.fetchone() 
            
            return produto # Retorna o dicionário do produto ou None
        
        except Exception as e:
            print(f"Erro ao buscar produto ID {id_produto}: {e}")
            return None