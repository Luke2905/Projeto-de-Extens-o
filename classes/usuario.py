import bcrypt
from servise.database import get_conexao

class Usuario:

    # Metodo do login
    def login(self, email, senha_original):

        try:
            with get_conexao() as conexao:
                with conexao.cursor(dictionary=True) as cursor:
                    # Verifica se o email existe
                    query = "SELECT * FROM usuario WHERE email_usuario = %s"
                    cursor.execute(query, (email,))
                    usuario_encontrado = cursor.fetchone()
            
            if usuario_encontrado:
                senha_hash = usuario_encontrado['senha_usuario']

                #Encripta a senha 
                if bcrypt.checkpw(senha_original.encode('utf-8'), senha_hash.encode('utf-8')):
                    return usuario_encontrado
                
            return None # Email não existe
        
        except Exception as e:
            print(f"Erro o login: {e}")
            return None

    # Cadastro de usario
    def cadastrar(self, nome, email, senha_orinal):
        """ Cria um novo usuário criptografando a senha antes de salvar. """
        try:
            # 1. Gera o 'sal' e o hash da senha
            salt = bcrypt.gensalt()
            senha_hash = bcrypt.hashpw(senha_orinal.encode('utf-8'), salt)

            # 2. Salva no banco (o hash, não a senha pura!)
            with get_conexao() as conexao:
                with conexao.cursor() as cursor:
                    query = "INSERT INTO usuario (nome_usuario, email_usuario, senha_usuario) VALUES (%s, %s, %s)"
                    # .decode('utf-8') transforma os bytes do hash de volta em string pro MySQL ler
                    cursor.execute(query, (nome, email, senha_hash.decode('utf-8')))
                    conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao cadastrar usuário: {e}")
            return False