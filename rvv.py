# Bibliotecas

import streamlit as st
import pandas as pd
import plotly.express as px

# Titulo do dash

st.set_page_config(layout="wide")

st.sidebar.image("logo.png", width=150)

st.title("💰 Dashboard Campanha de Incentivo")
st.caption("Desenvolvido por: Guilherme Henrique Torres Lima")

# Carregamento de Base de dados

df = pd.read_excel("rvv.xlsx")

# cria coluna premio

def calcular_premio(ating):

    if ating >= 1.2:
        return 3000
    
    elif ating >= 1.0:
        return 1500
    
    elif ating >= 0.8:
        return 500
    
    else:
        return 0

df["Premio"] = df["Ating%"].apply(calcular_premio)

gerentes = st.sidebar.multiselect(
    "Filtrar Gerente",
    df["Gerente"].unique(),
    default=df["Gerente"].unique()
)

ating = st.sidebar.slider(
    "Filtrar Atingimento (%)",
    0.0,
    2.0,
    (0.0, 200.0),
    format="%.0f%%"
)

df_filtrado = df[
    (df["Gerente"].isin(gerentes)) &
    (df["Ating%"] >= ating[0]) &
    (df["Ating%"] <= ating[1])
]

# calcular a meta total

meta_total = df_filtrado["Meta"].sum()
realizado_total = df_filtrado["Realizado"].sum()
atingimento_geral = realizado_total / meta_total
premio_total = df_filtrado["Premio"].sum()

# Criar colunas no dashboard

col1, col2, col3, col4 = st.columns(4)

col1.metric("Meta Total", f"R$ {meta_total:,.0f}")
col2.metric("Realizado Total", f"R$ {realizado_total:,.0f}")
col3.metric("Atingimento Geral", f"{atingimento_geral:.0%}")
col4.metric("Premiação Total", f"R$ {premio_total:,.2f}")

# formata as colunas

st.dataframe(
    df_filtrado.style.format({
        "Meta": "{:,.0f}",
        "Realizado": "{:,.0f}",
        "Ating%": "{:.0%}",
        "Premio": "R$ {:,.2f}"
    })
)