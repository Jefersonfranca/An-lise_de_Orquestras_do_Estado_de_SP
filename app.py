import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🎻 Análise de Orquestras do Estado de SP")

# Upload do arquivo
uploaded_file = st.file_uploader("Faça upload da planilha (.xlsx)", type="xlsx")

if uploaded_file:
    # Leitura apenas das linhas relevantes da aba "Base SP"
    df_raw = pd.read_excel(uploaded_file, sheet_name="Base SP", header=None)
    df_raw = df_raw.iloc[7:687].reset_index(drop=True)  # Pega linhas 8 a 688 (índice 7:688)

    # Define os nomes das colunas com base na primeira linha válida
    df_raw.columns = df_raw.iloc[0]
    df = df_raw.drop(index=0).reset_index(drop=True)
    df.columns.name = None

    # Padronização dos nomes das colunas
    df = df.rename(columns={
        "Cidade": "Cidade",
        "Região": "Região",
        "Tem orquestra?": "Tem Orquestra",
        "Modelo de Gestão": "Modelo de Gestão",
        "Entidade Gestora": "Entidade Gestora",
        "Status": "Status"
    })

    # Limpeza e padronização dos dados de "Modelo de Gestão"
    df["Modelo de Gestão"] = df["Modelo de Gestão"].astype(str).str.strip().str.title()
    df["Modelo de Gestão"] = df["Modelo de Gestão"].replace({
        "Particular": "Particular",
        "Particular ": "Particular"
    })
    
    # 🔸 Substituir valores 'nan' por "Não identificado"
    df["Modelo de Gestão"] = df["Modelo de Gestão"].replace("Nan", pd.NA)
    df["Modelo de Gestão"] = df["Modelo de Gestão"].fillna("Não identificado")

    # Substituir strings vazias ou valores 'nan' em "Cidade" para NaN do pandas
    df["Cidade"] = df["Cidade"].replace(["Nan", "nan", ""], pd.NA)

    # Remover linhas onde "Cidade" está nulo (NaN)
    df = df.dropna(subset=["Cidade"]).reset_index(drop=True)
    

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

    # Gráfico de pizza - Modelos de Gestão
    st.subheader("🏛️ Distribuição por Modelo de Gestão")
    fig2 = px.pie(
        df_filtros[df_filtros["Tem Orquestra"] == "Sim"],
        names="Modelo de Gestão",
        title="Modelos de Gestão nas Orquestras",
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Ranking das top 5 cidades com mais orquestras
    st.subheader("🏙️ Top 5 Cidades com Mais Orquestras")
    ranking_cidades = df[df["Tem Orquestra"] == "Sim"].groupby("Cidade").size().reset_index(name="Nº de Orquestras")
    ranking_cidades = ranking_cidades.sort_values(by="Nº de Orquestras", ascending=False).head(5)
    fig1 = px.bar(ranking_cidades, x="Cidade", y="Nº de Orquestras", color="Cidade")
    st.plotly_chart(fig1, use_container_width=True)

    # Ranking das entidades gestoras com mais cidades atendidas
    st.subheader("🏢 Top 5 Entidades Gestoras com Maior Abrangência")
    entidades = df[df["Tem Orquestra"] == "Sim"].groupby("Entidade Gestora")["Cidade"].nunique().reset_index(name="Nº de Cidades Atendidas")
    entidades = entidades.sort_values(by="Nº de Cidades Atendidas", ascending=False).head(5)
    fig3 = px.bar(entidades, x="Entidade Gestora", y="Nº de Cidades Atendidas", color="Entidade Gestora")
    st.plotly_chart(fig3, use_container_width=True)

    # Lista de cidades com maior número de orquestras
    st.subheader("📄 Lista: Cidades com Maior Número de Orquestras")
    st.dataframe(ranking_cidades)

    # Tabela final
    st.subheader("📋 Tabela de Dados Filtrados")
    st.dataframe(df_filtros[["Cidade", "Região", "Tem Orquestra", "Entidade Gestora", "Modelo de Gestão", "Status"]])
