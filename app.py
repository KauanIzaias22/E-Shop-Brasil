
import streamlit as st
import pandas as pd
import plotly.express as px
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÕES DA APLICAÇÃO
# ==========================================

st.set_page_config(
    page_title="E-Shop Brasil | Gestão Inteligente",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 E-Shop Brasil")
st.subheader("Sistema Inteligente de Gestão de Dados e Logística")

st.caption(
    "Painel administrativo para gerenciamento de produtos, "
    "pedidos, estoque e análise de dados."
)

# ==========================================
# 2. CONEXÃO COM O MONGODB
# ==========================================

@st.cache_resource
def conectar_mongodb():
    cliente = MongoClient(
        "mongodb://mongodb:27017/",
        serverSelectionTimeoutMS=5000
    )
    cliente.admin.command("ping")
    return cliente["eshop_brasil"]

try:
    db = conectar_mongodb()
    produtos = db["produtos"]
    pedidos = db["pedidos"]
    st.success("Conectado ao MongoDB com sucesso!")
except Exception as erro:
    st.error(f"Não foi possível conectar ao MongoDB: {erro}")
    st.info("Verifique se os containers estão em execução.")
    st.stop()


# ==========================================
# 3. FUNÇÕES AUXILIARES
# ==========================================

def carregar_produtos():
    dados = list(produtos.find())
    for item in dados:
        item["_id"] = str(item["_id"])
    return dados


def carregar_pedidos():
    dados = list(pedidos.find())
    for item in dados:
        item["_id"] = str(item["_id"])
        item["produto_id"] = str(item["produto_id"])
    return dados


def inserir_dados_exemplo():
    if produtos.count_documents({}) == 0:
        lista_produtos = [
            {
                "nome": "Notebook Dell",
                "categoria": "Eletrônicos",
                "preco": 3500.00,
                "estoque": 15
            },
            {
                "nome": "Smartphone Samsung",
                "categoria": "Eletrônicos",
                "preco": 2200.00,
                "estoque": 25
            },
            {
                "nome": "Fone Bluetooth",
                "categoria": "Acessórios",
                "preco": 180.00,
                "estoque": 50
            },
            {
                "nome": "Tênis Esportivo",
                "categoria": "Moda",
                "preco": 299.90,
                "estoque": 8
            },
            {
                "nome": "Mochila",
                "categoria": "Acessórios",
                "preco": 149.90,
                "estoque": 30
            }
        ]
        produtos.insert_many(lista_produtos)

    if pedidos.count_documents({}) == 0:
        catalogo = list(produtos.find())

        exemplos = [
            ("Cliente 001", "São Paulo", "Entregue", 2),
            ("Cliente 002", "Rio de Janeiro", "Em transporte", 1),
            ("Cliente 003", "Bahia", "Em separação", 1),
            ("Cliente 004", "Minas Gerais", "Entregue", 3),
            ("Cliente 005", "Amazonas", "Em transporte", 1),
            ("Cliente 006", "Paraná", "Entregue", 2),
            ("Cliente 007", "Ceará", "Em separação", 1),
            ("Cliente 008", "São Paulo", "Entregue", 1)
        ]

        novos_pedidos = []

        for i, exemplo in enumerate(exemplos):
            cliente, regiao, status, quantidade = exemplo
            produto = catalogo[i % len(catalogo)]

            novos_pedidos.append({
                "cliente": cliente,
                "produto_id": produto["_id"],
                "produto_nome": produto["nome"],
                "quantidade": quantidade,
                "valor_total": produto["preco"] * quantidade,
                "regiao": regiao,
                "status": status,
                "data": datetime.now()
            })

        pedidos.insert_many(novos_pedidos)


# ==========================================
# 4. MENU PRINCIPAL
# ==========================================

menu = st.sidebar.radio(
    "NAVEGAÇÃO",
    [
        "Dashboard",
        "Produtos",
        "Pedidos",
        "Consultas e Análises",
        "Logística"
    ]
)

st.sidebar.divider()
st.sidebar.subheader("Dados de demonstração")

if st.sidebar.button("Inserir dados de exemplo", use_container_width=True):
    inserir_dados_exemplo()
    st.sidebar.success("Dados de demonstração inseridos!")
    st.rerun()


# ==========================================
# 5. DASHBOARD
# ==========================================

if menu == "Dashboard":

    st.header("📊 Visão Geral do E-commerce")

    lista_produtos = carregar_produtos()
    lista_pedidos = carregar_pedidos()

    df_produtos = pd.DataFrame(lista_produtos)
    df_pedidos = pd.DataFrame(lista_pedidos)

    total_produtos = len(lista_produtos)
    total_pedidos = len(lista_pedidos)

    faturamento = sum(
        p.get("valor_total", 0) for p in lista_pedidos
    )

    estoque_total = sum(
        p.get("estoque", 0) for p in lista_produtos
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Produtos cadastrados", total_produtos)
    col2.metric("Total de pedidos", total_pedidos)
    col3.metric("Faturamento simulado", f"R$ {faturamento:,.2f}")
    col4.metric("Unidades em estoque", estoque_total)

    st.divider()

    if not df_pedidos.empty:

        esquerda, direita = st.columns(2)

        with esquerda:
            st.subheader("Pedidos por status")

            grafico_status = px.pie(
                df_pedidos,
                names="status",
                title="Distribuição dos pedidos",
                hole=0.4
            )
            st.plotly_chart(grafico_status, use_container_width=True)

        with direita:
            st.subheader("Pedidos por região")

            grafico_regiao = px.bar(
                df_pedidos.groupby("regiao").size().reset_index(
                    name="quantidade"
                ),
                x="regiao",
                y="quantidade",
                title="Volume de pedidos por região"
            )
            st.plotly_chart(grafico_regiao, use_container_width=True)

    else:
        st.info("Insira os dados de exemplo para visualizar os indicadores.")

    st.caption("Valores demonstrativos, baseados em dados fictícios.")


# ==========================================
# 6. GERENCIAMENTO DE PRODUTOS
# ==========================================

elif menu == "Produtos":

    st.header("📦 Gerenciamento de Produtos")

    with st.expander("Cadastrar novo produto", expanded=True):

        with st.form("form_produto"):
            nome = st.text_input("Nome do produto")
            categoria = st.selectbox(
                "Categoria",
                ["Eletrônicos", "Moda", "Acessórios", "Casa", "Outros"]
            )
            preco = st.number_input(
                "Preço (R$)",
                min_value=0.01,
                value=100.00
            )
            estoque = st.number_input(
                "Quantidade em estoque",
                min_value=0,
                step=1
            )

            cadastrar = st.form_submit_button("Cadastrar produto")

            if cadastrar:
                if nome.strip():
                    produtos.insert_one({
                        "nome": nome.strip(),
                        "categoria": categoria,
                        "preco": float(preco),
                        "estoque": int(estoque)
                    })
                    st.success("Produto cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.warning("Informe o nome do produto.")

    st.divider()
    st.subheader("Produtos cadastrados")

    lista = carregar_produtos()

    if lista:
        df = pd.DataFrame(lista)
        st.dataframe(
            df[["_id", "nome", "categoria", "preco", "estoque"]],
            use_container_width=True,
            hide_index=True
        )

        opcoes = {p["nome"] + " | " + p["_id"]: p for p in lista}

        selecionado = st.selectbox(
            "Selecione um produto para editar ou excluir",
            list(opcoes.keys())
        )

        produto = opcoes[selecionado]

        with st.form("editar_produto"):
            novo_nome = st.text_input(
                "Nome",
                value=produto["nome"]
            )
            nova_categoria = st.selectbox(
                "Categoria",
                ["Eletrônicos", "Moda", "Acessórios", "Casa", "Outros"],
                index=["Eletrônicos", "Moda", "Acessórios", "Casa", "Outros"].index(
                    produto["categoria"]
                )
            )
            novo_preco = st.number_input(
                "Preço",
                min_value=0.01,
                value=float(produto["preco"])
            )
            novo_estoque = st.number_input(
                "Estoque",
                min_value=0,
                value=int(produto["estoque"])
            )

            atualizar = st.form_submit_button("Salvar alterações")

            if atualizar:
                produtos.update_one(
                    {"_id": ObjectId(produto["_id"])},
                    {"$set": {
                        "nome": novo_nome.strip(),
                        "categoria": nova_categoria,
                        "preco": float(novo_preco),
                        "estoque": int(novo_estoque)
                    }}
                )
                st.success("Produto atualizado!")
                st.rerun()

        if st.button("Excluir produto", type="secondary"):
            existe_pedido = pedidos.count_documents({
                "produto_id": ObjectId(produto["_id"])
            })

            if existe_pedido:
                st.error(
                    "Não é possível excluir: existem pedidos vinculados a este produto."
                )
            else:
                produtos.delete_one({
                    "_id": ObjectId(produto["_id"])
                })
                st.success("Produto excluído!")
                st.rerun()

    else:
        st.info("Nenhum produto cadastrado.")


# ==========================================
# 7. GERENCIAMENTO DE PEDIDOS
# ==========================================

elif menu == "Pedidos":

    st.header("🛍️ Gerenciamento de Pedidos")

    catalogo = carregar_produtos()

    with st.expander("Registrar novo pedido", expanded=True):

        if catalogo:

            opcoes_produtos = {
                p["nome"] + " | " + p["_id"]: p for p in catalogo
            }

            with st.form("form_pedido"):

                cliente = st.text_input("Identificação fictícia do cliente")

                produto_escolhido = st.selectbox(
                    "Produto",
                    list(opcoes_produtos.keys())
                )

                quantidade = st.number_input(
                    "Quantidade",
                    min_value=1,
                    step=1
                )

                regiao = st.selectbox(
                    "Região de entrega",
                    [
                        "São Paulo",
                        "Rio de Janeiro",
                        "Minas Gerais",
                        "Paraná",
                        "Bahia",
                        "Ceará",
                        "Amazonas",
                        "Outros"
                    ]
                )

                status = st.selectbox(
                    "Status",
                    ["Em separação", "Em transporte", "Entregue", "Cancelado"]
                )

                registrar = st.form_submit_button("Registrar pedido")

                if registrar:

                    produto = opcoes_produtos[produto_escolhido]

                    if not cliente.strip():
                        st.warning("Informe a identificação do cliente.")

                    elif quantidade > produto["estoque"]:
                        st.error("Estoque insuficiente para este pedido.")

                    else:
                        pedidos.insert_one({
                            "cliente": cliente.strip(),
                            "produto_id": ObjectId(produto["_id"]),
                            "produto_nome": produto["nome"],
                            "quantidade": int(quantidade),
                            "valor_total": produto["preco"] * quantidade,
                            "regiao": regiao,
                            "status": status,
                            "data": datetime.now()
                        })

                        produtos.update_one(
                            {"_id": ObjectId(produto["_id"])},
                            {"$inc": {"estoque": -int(quantidade)}}
                        )

                        st.success("Pedido registrado com sucesso!")
                        st.rerun()

        else:
            st.warning("Cadastre produtos antes de registrar pedidos.")

    st.divider()
    st.subheader("Pedidos registrados")

    lista = carregar_pedidos()

    if lista:

        df = pd.DataFrame(lista)

        st.dataframe(
            df[[
                "_id", "cliente", "produto_nome",
                "quantidade", "valor_total", "regiao", "status"
            ]],
            use_container_width=True,
            hide_index=True
        )

        opcoes = {p["_id"]: p for p in lista}

        pedido_id = st.selectbox(
            "Selecione o ID do pedido para atualizar ou excluir",
            list(opcoes.keys())
        )

        pedido = opcoes[pedido_id]

        with st.form("editar_pedido"):
            novo_status = st.selectbox(
                "Atualizar status",
                ["Em separação", "Em transporte", "Entregue", "Cancelado"],
                index=[
                    "Em separação",
                    "Em transporte",
                    "Entregue",
                    "Cancelado"
                ].index(pedido["status"])
            )

            atualizar = st.form_submit_button("Atualizar pedido")

            if atualizar:
                pedidos.update_one(
                    {"_id": ObjectId(pedido_id)},
                    {"$set": {"status": novo_status}}
                )
                st.success("Status atualizado!")
                st.rerun()

        if st.button("Excluir pedido"):
            if pedido["status"] != "Cancelado":
                produtos.update_one(
                    {"_id": ObjectId(pedido["produto_id"])},
                    {"$inc": {"estoque": pedido["quantidade"]}}
                )

            pedidos.delete_one({"_id": ObjectId(pedido_id)})

            st.success("Pedido excluído e estoque ajustado!")
            st.rerun()

    else:
        st.info("Nenhum pedido registrado.")


# ==========================================
# 8. CONSULTAS E CONCATENAÇÃO DE DADOS
# ==========================================

elif menu == "Consultas e Análises":

    st.header("🔎 Consultas e Análises de Dados")

    lista_produtos = carregar_produtos()
    lista_pedidos = carregar_pedidos()

    if lista_produtos and lista_pedidos:

        df_produtos = pd.DataFrame(lista_produtos)
        df_pedidos = pd.DataFrame(lista_pedidos)

        # Concatenação lógica por meio de JOIN entre as coleções
        df_concatenado = pd.merge(
            df_pedidos,
            df_produtos,
            left_on="produto_id",
            right_on="_id",
            suffixes=("_pedido", "_produto")
        )

        st.subheader("Concatenação de produtos e pedidos")

        st.write(
            "Combinação dos registros das duas coleções utilizando "
            "o identificador do produto como chave."
        )

        resultado = df_concatenado[[
            "cliente",
            "nome",
            "categoria",
            "quantidade",
            "preco",
            "valor_total",
            "regiao",
            "status"
        ]].rename(columns={
            "nome": "produto"
        })

        st.dataframe(
            resultado,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Filtros de consulta")

        categoria = st.selectbox(
            "Filtrar por categoria",
            ["Todas"] + sorted(df_produtos["categoria"].unique().tolist())
        )

        if categoria != "Todas":
            resultado_filtro = df_produtos[
                df_produtos["categoria"] == categoria
            ]
        else:
            resultado_filtro = df_produtos

        st.dataframe(
            resultado_filtro[["nome", "categoria", "preco", "estoque"]],
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Produtos mais vendidos")

        vendas = df_pedidos.groupby("produto_nome")[
            "quantidade"
        ].sum().reset_index()

        vendas = vendas.sort_values(
            by="quantidade",
            ascending=False
        )

        grafico = px.bar(
            vendas,
            x="produto_nome",
            y="quantidade",
            title="Quantidade de unidades vendidas por produto"
        )

        st.plotly_chart(grafico, use_container_width=True)

    else:
        st.info("Cadastre produtos e pedidos ou insira os dados de exemplo.")


# ==========================================
# 9. CONTROLE DE ESTOQUE E LOGÍSTICA
# ==========================================

elif menu == "Logística":

    st.header("🚚 Controle de Estoque e Logística")

    lista_produtos = carregar_produtos()
    lista_pedidos = carregar_pedidos()

    if lista_produtos:

        df = pd.DataFrame(lista_produtos)

        estoque_baixo = df[df["estoque"] <= 10]

        st.subheader("Alertas de estoque")

        st.metric(
            "Produtos com estoque baixo",
            len(estoque_baixo)
        )

        if not estoque_baixo.empty:
            st.warning("Atenção: produtos precisam de reposição.")
            st.dataframe(
                estoque_baixo[["nome", "categoria", "estoque"]],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("Todos os produtos possuem estoque acima de 10 unidades.")

    if lista_pedidos:

        df_pedidos = pd.DataFrame(lista_pedidos)

        st.divider()
        st.subheader("Acompanhamento das entregas")

        pendentes = df_pedidos[
            df_pedidos["status"].isin(
                ["Em separação", "Em transporte"]
            )
        ]

        col1, col2 = st.columns(2)

        col1.metric("Pedidos em andamento", len(pendentes))
        col2.metric(
            "Pedidos entregues",
            len(df_pedidos[df_pedidos["status"] == "Entregue"])
        )

        entregas_regiao = df_pedidos.groupby(
            ["regiao", "status"]
        ).size().reset_index(name="pedidos")

        grafico = px.bar(
            entregas_regiao,
            x="regiao",
            y="pedidos",
            color="status",
            barmode="group",
            title="Pedidos por região e situação da entrega"
        )

        st.plotly_chart(grafico, use_container_width=True)

    else:
        st.info("Insira pedidos para visualizar a logística.")


# ==========================================
# 10. RODAPÉ
# ==========================================

st.divider()

st.caption(
    "E-Shop Brasil | Projeto acadêmico de Banco de Dados e Big Data"
)
st.caption(
    "Aplicação demonstrativa com dados fictícios. "
    "Desenvolvida com Python, MongoDB, Streamlit e Docker."
)
