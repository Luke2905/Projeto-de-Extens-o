from servise.database import get_conexao

class Pedido:

    def listar_pedidos(self):
        pedidos = []
        try:
            with get_conexao() as conexao:
                with conexao.cursor(dictionary=True) as cursor:
                    query = "SELECT * FROM pedido"
                    cursor.execute(query)
                    pedidos = cursor.fetchall()
            return pedidos
        except Exception as e:
            print(f"Erro ao Listar produtos: {e}")
            return []