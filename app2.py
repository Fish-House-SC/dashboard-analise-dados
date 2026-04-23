import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt


st.set_page_config(page_title="Dashboard de Dados", layout="wide")

st.title("Dashboard Interativo")

# Upload do arquivo
st.sidebar.title("Configuração")
arquivo = st.sidebar.file_uploader("Envie um arquivo Excel ou CSV", type = ["xlsx", "csv"])

if arquivo:
    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    
    else:
        df = pd.read_excel(arquivo)

    st.subheader("Dados carregados")
    st.write(df)

    # Selecionar coluna para gráfico
    colunas = df.columns.tolist()
    coluna = st.selectbox("Escolha uma coluna para análise", colunas)

    tipo_grafico = st.selectbox(
        "Escolha o tipo de gráfico",
        ["Linha", "Barra", "Histograma"]
    )

    filtro = st.multiselect("filtrar valores", df[coluna].unique())
    if filtro:
        df = df[df[coluna].isin(filtro)]

    st.subheader("Gráfico")

    if tipo_grafico == "Linha":
        st.line_chart(df[coluna])

    elif tipo_grafico == "Barra":
        if df[coluna].dtype == "object":
            dados = df[coluna].value_counts()
            st.bar_chart(dados)
        else:
            st.bar_chart(df[coluna])
    elif tipo_grafico == "Histograma":
        fig, ax = plt.subplots()
        ax.hist(df[coluna], bins=10)
        st.pyplot(fig)


    # Insight simples
    st.subheader("Insight rápido")

    if df[coluna].dtype != "object":
        st.write(f"Média: {df[coluna].mean():.2f}")
        st.write(f"Máximo: {df[coluna].max()}")
        st.write(f"Mínimo: {df[coluna].min()}")

    


