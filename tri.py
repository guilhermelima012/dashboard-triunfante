import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.sidebar.image("logo.png", width=150)

st.title("📊 Dashboard Comercial - Triunfante")
st.caption("Desenvolvido por: Guilherme Henrique Torres Lima")

# Carregar dados

df = pd.read_excel("dados.xlsx")

df["Data"] = pd.to_datetime(df["Data"])

df["Receita"] = df["Quantidade"] * df["Preco"]

# SIDEBAR - FILTROS

st.sidebar.header("Filtros")

data = st.sidebar.date_input(
    "Período",
    [df["Data"].min(), df["Data"].max()]
)

regiao = st.sidebar.multiselect(
    "Região",
    df["Regiao"].unique(),
    default=df["Regiao"].unique()
)

categoria = st.sidebar.multiselect(
    "Categoria",
    df["Categoria"].unique(),
    default=df["Categoria"].unique()
)

cliente = st.sidebar.multiselect(
    "Cliente",
    df["Cliente"].unique(),
    default=df["Cliente"].unique()
)

marca = st.sidebar.multiselect(
    "Marca",
    df["Marca"].unique(),
    default=df["Marca"].unique()
)

# Aplicar filtros

data_inicio, data_fim = data

df_filtrado = df[
    (df["Data"] >= pd.to_datetime(data_inicio)) &
    (df["Data"] <= pd.to_datetime(data_fim)) &
    (df["Regiao"].isin(regiao if regiao else df["Regiao"].unique())) &
    (df["Categoria"].isin(categoria if categoria else df["Categoria"].unique())) &
    (df["Cliente"].isin(cliente if cliente else df["Cliente"].unique())) &
    (df["Marca"].isin(marca if marca else df["Marca"].unique()))
]

# KPIs

receita_total = df_filtrado["Receita"].sum()

quantidade_total = df_filtrado["Quantidade"].sum()

ticket_medio = receita_total / quantidade_total if quantidade_total > 0 else 0

clientes_unicos = df_filtrado["Cliente"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Receita Total", f"R$ {receita_total:,.2f}")
col2.metric("📦 Quantidade Vendida", quantidade_total)
col3.metric("🧾 Ticket Médio", f"R$ {ticket_medio:,.2f}")
col4.metric("👥 Nº Clientes", clientes_unicos)

st.divider()

# GRÁFICOS

col1, col2 = st.columns(2)

# Receita por categoria

categoria_receita = df_filtrado.groupby("Categoria")["Receita"].sum().reset_index()

fig_categoria = px.pie(
    categoria_receita,
    names="Categoria",
    values="Receita",
    title="Receita por Categoria"
)

col1.plotly_chart(fig_categoria, use_container_width=True)

# Top produtos

top_produtos = df_filtrado.groupby("Produto")["Receita"].sum().reset_index()

top_produtos = top_produtos.sort_values("Receita", ascending=False).head(10)

fig_produtos = px.bar(
    top_produtos,
    x="Receita",
    y="Produto",
    orientation="h",
    title="Top 10 Produtos"
)

col2.plotly_chart(fig_produtos, use_container_width=True)

# Segunda linha

col3, col4 = st.columns(2)

# Vendas por região

regiao_vendas = df_filtrado.groupby("Regiao")["Receita"].sum().reset_index()

fig_regiao = px.bar(
    regiao_vendas,
    x="Regiao",
    y="Receita",
    title="Vendas por Região"
)

# Evolução mensal

col3.plotly_chart(fig_regiao, use_container_width=True)

df_filtrado["Mes"] = df_filtrado["Data"].dt.to_period("M").astype(str)

mensal = df_filtrado.groupby("Mes")["Receita"].sum().reset_index()

fig_mensal = px.line(
    mensal,
    x="Mes",
    y="Receita",
    markers=True,
    title="Evolução Mensal de Vendas"
)

col4.plotly_chart(fig_mensal, use_container_width=True)

df = df.copy()

df_filtrado = df_filtrado.copy()
df_filtrado["Mes"] = df_filtrado["Data"].dt.to_period("M").astype(str)

st.divider()

st.subheader("📋 Base de Dados Filtrada")

st.dataframe(
    df_filtrado,
    use_container_width=True
)

csv = df_filtrado.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Baixar dados filtrados",
    csv,
    "dados_filtrados.csv",
    "text/csv"

)
