# Projeto-de-Extens-o
# 📦 Sistema de Gestão de Pedidos & PDV

Este projeto é um sistema leve e eficiente para controle de produtos, estoque e realização de vendas (Ponto de Venda), desenvolvido em Python com interface web via Streamlit.

O foco é simplicidade: cadastre produtos, controle o estoque e realize vendas em uma interface visual estilo "frente de caixa".

## 🛠️ Tecnologias Utilizadas

* **Frontend:** Streamlit
* **Backend:** Python 3.10+
* **Banco de Dados:** MySQL
* **Bibliotecas:** `mysql-connector-python`, `pandas`, `bcrypt`

---

## 📝 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:

1.  **Python** (versão 3.9 ou superior)
2.  **MySQL Server** (rodando localmente ou em servidor)
3.  **Git** (opcional, para clonar o repositório)

---

## ⚙️ Passo a Passo de Instalação

Siga estas etapas na ordem para configurar o ambiente.

### 1. Preparar o Banco de Dados 🗄️

Abra seu gerenciador de banco de dados favorito (MySQL Workbench, DBeaver, HeidiSQL) e execute o script abaixo para criar a estrutura:

```Execute o arquivo .sql no font```

### 2. Instalar Dependências 📦
Abra o terminal na pasta raiz do projeto e instale as bibliotecas necessárias:

Bash

pip install streamlit mysql-connector-python pandas bcrypt
3. Configurar a Conexão 🔌
Verifique o arquivo servise/database.py. Certifique-se de que as credenciais batem com a configuração do seu MySQL local:

Host: localhost

User: root (ou seu usuário)

Password: sua_senha_aqui

Database: sistema_pedidos

🚀 Como Rodar o Projeto
No terminal, dentro da pasta do projeto, execute:

Bash

streamlit run app.py
(Caso o comando não seja reconhecido, tente: python -m streamlit run app.py)

O sistema abrirá automaticamente no seu navegador no endereço: http://localhost:8501
