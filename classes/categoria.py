from servise.database import get_conexao

class Categoria:

    def listar_categorias(self):
        try:
            with get_conexao() as conn:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM categoria ORDER BY nome ASC")
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao listar categorias: {e}")
            return []