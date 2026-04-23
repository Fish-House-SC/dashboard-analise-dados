import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

tema = st.sidebar.selectbox("Tema do gráfico", ["plotly", "plotly_dark", "ggplot2"])

px.defaults.template = tema


st.set_page_config(page_title="Dashboard Profissional", layout="wide")

#  Título
st.title("Dashboard de Análise de Dados")

# Sidebar
st.sidebar.header("⚙️ Configurações")
arquivo = st.sidebar.file_uploader("Envie um arquivo", type=["xlsx", "csv"])

if arquivo:
    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_excel(arquivo)

    st.subheader("Dados carregados")
    st.dataframe(df, use_container_width=True)

    # Escolher coluna
    coluna = st.selectbox("Escolha uma coluna", df.columns)

    # Filtro
    filtro = st.multiselect("Filtrar valores", df[coluna].unique())
    if filtro:
        df = df[df[coluna].isin(filtro)]

    # Tipo de gráfico
    tipo_grafico = st.selectbox(
        "Tipo de gráfico",
        ["Linha", "Barra", "Histograma"]
    )

    # MÉTRICAS (cards no topo)
    if df[coluna].dtype != "object":
        col1, col2, col3 = st.columns(3)

        col1.metric("Média", f"{df[coluna].mean():.2f}")
        col2.metric("Máximo", df[coluna].max())
        col3.metric("Mínimo", df[coluna].min())

    st.divider()

    # GRÁFICO CENTRAL
    st.subheader("Visualização Interativa")

    if tipo_grafico == "Linha":
        fig = px.line(df, y=coluna, title=f"{coluna} ao longo dos dados")
        st.plotly_chart(fig, use_container_width=True)

    elif tipo_grafico == "Barra":
        if df[coluna].dtype == "object":
            dados = df[coluna].value_counts().reset_index()
            dados.columns = [coluna, "Quantidade"]
            fig = px.bar(dados, x=coluna, y="Quantidade", title="Frequência")
        else:
            fig = px.bar(df, y=coluna, title=f"Valores de {coluna}")

        st.plotly_chart(fig, use_container_width=True)

    elif tipo_grafico == "Histograma":
        dados_numericos = pd.to_numeric(df[coluna], errors="coerce").dropna()

        fig = px.histogram(
            dados_numericos,
            nbins=10,
            title=f"Distribuição de {coluna}",
            color_discrete_sequence=["#00BFFF"]  # cor bonita
        )

        st.plotly_chart(fig, use_container_width=True)