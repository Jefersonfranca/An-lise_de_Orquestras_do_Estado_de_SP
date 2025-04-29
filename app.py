import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🎻 Análise de Orquestras do Estado de SP")

# Upload do arquivo
uploaded_file = st.file_uploader("Faça upload da planilha (.xlsx)", type="xlsx")

if uploaded_file:
    # Carregar e limpar os dados
    df_raw = pd.read_excel(uploaded_file, sheet_name="Base SP", skiprows=6)
    df = df_raw.copy()
    df.columns = df.iloc[0]
    df = df.drop(index=0).reset_index(drop=True)
    df.columns.name = None

    df = df.rename(columns={
        "Cidade": "Cidade",
        "Região": "Região",
        "Tem orquestra?": "Tem Orquestra",
        "Modelo de Gestão": "Modelo de Gestão",
        "Entidade Gestora": "Entidade Gestora",
        "Status": "Status"
    })

    st.subheader("📊 Indicadores Gerais")
    col1, col2, col3 = st.columns(3)

    total_cidades = df["Cidade"].nunique()
    cidades_com_orquestra = df[df["Tem Orquestra"] == "Sim"]["Cidade"].nunique()
    percentual = (cidades_com_orquestra / total_cidades) * 100

    col1.metric("Total de Cidades", total_cidades)
    col2.metric("Cidades com Orquestra", cidades_com_orquestra)
    col3.metric("% com Orquestra", f"{percentual:.1f}%")

    # Filtros
    st.sidebar.header("Filtros")
    regioes = st.sidebar.multiselect("Região", options=df["Região"].dropna().unique(), default=df["Região"].dropna().unique())
    modelo_gestao = st.sidebar.multiselect("Modelo de Gestão", options=df["Modelo de Gestão"].dropna().unique(), default=df["Modelo de Gestão"].dropna().unique())

    df_filtros = df[
        df["Região"].isin(regioes) &
        df["Modelo de Gestão"].isin(modelo_gestao)
    ]

    # Gráfico de barras por região
    st.subheader("📍 Cidades com Orquestra por Região")
    fig1 = px.bar(
        df[df["Tem Orquestra"] == "Sim"].groupby("Região")["Cidade"].count().reset_index(),
        x="Região",
        y="Cidade",
        labels={"Cidade": "Quantidade de Cidades"},
        color="Região"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico de pizza - Modelos de Gestão
    st.subheader("🏛️ Distribuição por Modelo de Gestão")
    fig2 = px.pie(
        df_filtros[df_filtros["Tem Orquestra"] == "Sim"],
        names="Modelo de Gestão",
        title="Modelos de Gestão nas Orquestras",
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Tabela
    st.subheader("📋 Tabela de Dados Filtrados")
    st.dataframe(df_filtros[["Cidade", "Região", "Tem Orquestra", "Entidade Gestora", "Modelo de Gestão", "Status"]])
