# E-Shop Brasil — Sistema Inteligente de Gestão de E-commerce

## Sobre o projeto

O E-Shop Brasil é uma aplicação desenvolvida para demonstrar o uso de bancos de dados NoSQL e tecnologias de Big Data na gestão de uma empresa de comércio eletrônico.

O sistema permite gerenciar produtos, registrar pedidos, acompanhar informações logísticas e visualizar indicadores para apoiar a tomada de decisões.

## Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento.
- **Streamlit:** construção da interface web.
- **MongoDB:** armazenamento dos dados.
- **PyMongo:** integração entre Python e MongoDB.
- **Pandas:** manipulação e integração de dados.
- **Plotly:** criação de gráficos e visualizações.
- **Docker:** conteinerização da aplicação.
- **Docker Compose:** gerenciamento dos serviços.

## Funcionalidades

- Dashboard com indicadores e gráficos.
- Cadastro, consulta, edição e exclusão de produtos.
- Registro e gerenciamento de pedidos.
- Atualização do status dos pedidos.
- Controle de estoque.
- Consultas e análises de dados.
- Visualização de informações logísticas.
- Inserção de dados de demonstração.

## Estrutura do projeto

```text
E-Shop-Brasil/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Como executar o projeto

### Pré-requisitos

- Docker Desktop instalado.
- Git instalado (opcional, para clonar o repositório).

### 1. Clonar o repositório

```bash
git clone https://github.com/KauanIzaias22/E-Shop-Brasil.git
```

### 2. Entrar na pasta

```bash
cd E-Shop-Brasil
```

### 3. Construir e iniciar os containers

```bash
docker compose up --build
```

### 4. Acessar a aplicação

Abra o navegador no endereço:

http://localhost:8501

Para encerrar os serviços, utilize `Ctrl + C` no terminal.

## Banco de dados

O projeto utiliza MongoDB como banco de dados NoSQL, organizado em coleções para armazenar produtos e pedidos.

Os dados são persistidos por meio de um volume Docker, permitindo sua manutenção mesmo após a recriação dos containers.

## Objetivo acadêmico

Demonstrar como tecnologias de bancos de dados NoSQL, integração de dados, visualização analítica e conteinerização podem contribuir para melhorar a gestão de informações, o controle de estoque e os processos logísticos de uma empresa de comércio eletrônico.

## Autor

Kauan Izaias

Projeto acadêmico — UniFECAF.