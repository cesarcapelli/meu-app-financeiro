import streamlit as st
import pandas as pd

if "gastos" not in st.session_state:
    st.session_state.gastos = pd.DataFrame(columns=["Data", "Categoria", "Descrição", "Valor", "Forma de Pagamento"])

if "gastos_fixos" not in st.session_state:
    st.session_state.gastos_fixos = pd.DataFrame(columns=["Dia do Vencimento","Descrição","Forma de Pagamento"])

# BARRA LATERAL
st.sidebar.header("Adicionar Novo Gasto")
with st.sidebar.form("form_adicionar", clear_on_submit=True):
    data = st.date_input("Data")
    categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Moradia", "Lazer", "Saúde", "Outros"])
    forma_pagamento = st.selectbox("Forma de Pagamento",["Débito","Crédito","PIX","Dinheiro"])
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")

    botao_adicionar = st.form_submit_button("Adicionar")

if botao_adicionar:
    novo_gasto = pd.DataFrame([{
        "Data": data,
        "Categoria": categoria,
        "Descrição": descricao,
        "Valor": valor,
        "Forma de Pagamento": forma_pagamento

    }])
    st.session_state.gastos = pd.concat([st.session_state.gastos, novo_gasto], ignore_index=True)
    st.toast("Gasto adicionado com sucesso!", icon="✅")

# SEÇÃO DE GASTOS FIXOS NA BARRA LATERAL
st.sidebar.divider()
st.sidebar.header("Meus Gastos Fixos")
with st.sidebar.expander("Cadastrar Novo Fixo"):
    with st.form("form_fixo", clear_on_submit=True):
        dia_vencimento = st.number_input("Dia do Vencimento", min_value=1, max_value=31, step=1)
        categoria_fixo = st.selectbox("Categoria",["Alimentação","Transporte","Moradia","Lazer","Saúde","Outros"])
        pagamento_fixo = st.selectbox("Pagamento", ["Débito","Crédito","PIX","Dinheiro"])
        descricao_fixo = st.text_input("Descrição")
        valor_fixo = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")

        botao_fixo = st.form_submit_button("Salvar Gasto Fixo")

if botao_fixo:
    novo_fixo = pd.DataFrame([{
        "Dia do Vencimento": dia_vencimento,
        "Categoria": categoria_fixo,
        "Descrição": descricao_fixo,
        "Valor": valor_fixo,
        "Forma de Pagamento": pagamento_fixo
    }])
    st.session_state.gastos_fixos = pd.concat([st.session_state.gastos_fixos, novo_fixo], ignore_index=True)
    st.toast("Gasto fixo cadastrado com sucesso!", icon="📌")

st.title("My Grana")

#CALCULANDO E EXIBINDO O TOTAL DE GASTOS
total_gastos = st.session_state.gastos["Valor"].sum()
st.metric(label="Total de Gastos", value=f"R$ {total_gastos:.2f}")

#GRAFICO DE GASTO POR CATEGORIA
st.subheader("Gastos por Categoria")
if not st.session_state.gastos.empty:
    gastos_por_categoria = st.session_state.gastos.groupby("Categoria")["Valor"].sum()
    st.bar_chart(gastos_por_categoria)

#GRAFICO DE GASTO POR FORMA DE PAGAMENTO
st.subheader("Gastos por Forma de Pagamento")
if not st.session_state.gastos.empty:
    gastos_por_pagamento = st.session_state.gastos.groupby("Forma de Pagamento")["Valor"].sum()
    st.bar_chart(gastos_por_pagamento)

st.subheader("Tabela de Detalhes")
st.dataframe(st.session_state.gastos)

#EXIBINDO OS GASTOS FIXOS
st.subheader("Meus Gastos Fixos")
if not st.session_state.gastos_fixos.empty:
    st.dataframe(st.session_state.gastos_fixos)
