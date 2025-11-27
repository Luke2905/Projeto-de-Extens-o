-- CREATE DATABASE SGP_PRODUCAO

-- USE SGP_PRODUCAO

-- Tabela de Categorias 
CREATE TABLE categoria (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);


INSERT INTO categoria (nome) VALUES
('Lanche'),
('Bebida'),
('Sobremessa');


-- Tabela de Produtos 
CREATE TABLE produto (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL, 
    id_categoria INT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
);

INSERT INTO produto (nome, descricao, preco, id_categoria) VALUES
('X-Egg', 'Lanche de Hamburguer, ovo e salada', 15.00, 1),
('X-Bacon', 'Lanche de Hamburguer, bacon e salada', 25.00, 1),
('X-Salada', 'Lanche de Hamburguer e salada', 10.00, 1),
('Coca-Cola', 'Lata 350ml', 5.00, 2),
('Fanta Laranja', 'Lata 350ml', 5.00, 2),
('Suco de Uva', 'Garrafa 250ml', 4.50, 2),
('Sorvete', 'Casquinha', 6.00, 3),
('Cookie', 'Biscoito com gotas de chocolate', 7.00, 3), 

-- Tabela de Pedidos 
CREATE TABLE pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    nome_cliente VARCHAR(255),
    valor_total DECIMAL(10, 2) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDENTE', 
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabela de Itens do Pedido 
CREATE TABLE item_pedido (
    id_item_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL, 
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto);

-- Tabela de Usuario
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario 			INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario		VARCHAR(100) NOT NULL,
    email_usuario		VARCHAR(100) NOT NULL UNIQUE,
    senha_usuario 		VARCHAR(255) NOT NULL 
);

-- Tabela de registro da Venda
CREATE TABLE IF NOT EXISTS venda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10, 2),
    resumo_itens TEXT -- Aqui vai ficar o texto ex: "2x X-Salada, 1x Coca"
);

-- Tabela de Movimentações de Estoque
CREATE TABLE IF NOT EXISTS movimentacao_estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_produto INT NOT NULL,
    tipo VARCHAR(10) NOT NULL, -- Vai ser 'Entrada' ou 'Saida'
    quantidade INT NOT NULL,
    data_movimentacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    observacao VARCHAR(255), -- Ex: "Venda #123" ou "Compra Nota #55"
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);