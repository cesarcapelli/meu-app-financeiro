import streamlit as st
import pandas as pd

if "gastos" not in st.session_state:
    st.session_state.gastos = pd.DataFrame(columns=["Data", "Categoria", "Descrição", "Valor"])

# BARRA LATERAL
st.sidebar.header("Adicionar Novo Gasto")
with st.sidebar.form("form_adicionar", clear_on_submit=True):
    data = st.date_input("Data")
    categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Outros"])
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")

    botao_adicionar = st.form_submit_button("Adicionar")

if botao_adicionar:
    novo_gasto = pd.DataFrame([{
        "Data": data,
        "Categoria": categoria,
        "Descrição": descricao,
        "Valor": valor
    }])
    st.session_state.gastos = pd.concat([st.session_state.gastos, novo_gasto], ignore_index=True)
    st.toast("Gasto adicionado com sucesso!", icon="✅")

st.title("My Grana")

#CALCULANDO E EXIBINDO O TOTAL DE GASTOS
total_gastos = st.session_state.gastos["Valor"].sum()
st.metric(label="Total de Gastos", value=f"R$ {total_gastos:.2f}")

st.dataframe(st.session_state.gastos)
