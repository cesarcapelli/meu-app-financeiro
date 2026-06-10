import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import io




if "gastos" not in st.session_state:
    st.session_state.gastos = pd.DataFrame(columns=["Data", "Categoria", "Descrição", "Valor", "Forma de Pagamento"])

if "gastos_fixos" not in st.session_state:
    st.session_state.gastos_fixos = pd.DataFrame(columns=["Dia do Vencimento","Categoria","Descrição","Valor","Forma de Pagamento"])

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

#IMPORTAR VIA EXCEL
st.sidebar.divider()
st.sidebar.header("Importar via Excel")

#CRIAR MODELO DE EXCEL PARA DOWNLOAD
buffer = io.BytesIO()
modelo_df = pd.DataFrame(columns=["Data","Categoria","Descrição","Valor","Forma de Pagamento"])
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    modelo_df.to_excel(writer, index=False)

st.sidebar.download_button(
    label="📥 Baixar Modelo Excel para preenchimento",
    data=buffer.getvalue(),
    file_name="modelo_gastos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

arquivo_excel = st.sidebar.file_uploader("Selecione um arquivo Excel (.xls)", type=["xlsx"])

if arquivo_excel is not None:
    if st.sidebar.button("Processar Arquivo"):
        try:
            df_importado = pd.read_excel(arquivo_excel)
            colunas_esperadas = ["Data","Categoria","Descrição","Valor","Forma de Pagamento"]
            if all(col in df_importado.columns for col in colunas_esperadas):
                #CONVERTE A COLUNA DE DATA PARA O FORMATO CORRETO E REMOVE HORAS SE HOUVER
                df_importado["Data"] = pd.to_datetime(df_importado["Data"]).dt.date
                #ADICIONA OS NOVOS DADOS AO QUE JÁ EXISTE NO APP
                st.session_state.gastos = pd.concat([st.session_state.gastos, df_importado[colunas_esperadas]], ignore_index=True)
                #ADICIONA OS NOVOS DADOS AO QUE JÁ EXISTE NO APP    
                st.toast("Arquivo Excel processado com sucesso", icon= "📊")
                st.rerun()
            else:
                st.sidebar.error(f"O Excel precisa conter as colunas:{','.join(colunas_esperadas)}")
        except Exception as e:
            st.sidebar.error(f"Erro ao ler o arquivo:{e}")                

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

# FILTROS POR MES
st.sidebar.divider()
st.sidebar.header("Filtros")
if not st.session_state.gastos.empty:
    gastos_df = st.session_state.gastos.copy()
    gastos_df["Data"] = pd.to_datetime(gastos_df["Data"]) #GARANTE QUE A COLUNA SEJA VISTA COMO DATA
    gastos_df["Mês/Ano"] = gastos_df["Data"].dt.strftime("%m/%Y") #CRIA UMA COLUNA TEMPORÁRIA MM/AAAA

    meses_disponiveis = ["Todos"] + list(gastos_df["Mês/Ano"].unique())
    mes_filtro = st.sidebar.selectbox("Filtrar por Mês", meses_disponiveis)

    if mes_filtro !="Todos":
        gastos_filtrados = gastos_df[gastos_df["Mês/Ano"] == mes_filtro]
    else:
        gastos_filtrados = gastos_df
else:
    gastos_filtrados = st.session_state.gastos

st.title("My Grana")

#CALCULANDO E EXIBINDO O TOTAL DE GASTOS
total_gastos = gastos_filtrados["Valor"].sum()
st.metric(label="Total de Gastos", value=f"R$ {total_gastos:.2f}")

#GRAFICO DE GASTO POR CATEGORIA
st.subheader("Gastos por Categoria")
if not gastos_filtrados.empty:
    gastos_por_categoria = gastos_filtrados.groupby("Categoria")["Valor"].sum().reset_index()
    fig_categoria = px.pie(gastos_por_categoria, values="Valor", names="Categoria", hole=0.4)
    st.plotly_chart(fig_categoria, use_container_width=True)

#GRAFICO DE GASTO POR FORMA DE PAGAMENTO
st.subheader("Gastos por Forma de Pagamento")
if not gastos_filtrados.empty:
    gastos_por_pagamento = gastos_filtrados.groupby("Forma de Pagamento")["Valor"].sum()
    st.bar_chart(gastos_por_pagamento)

st.subheader("Tabela de Detalhes")
st.session_state.gastos = st.data_editor(st.session_state.gastos, num_rows="dynamic")

#EXIBINDO OS GASTOS FIXOS
st.subheader("Meus Gastos Fixos")
if not st.session_state.gastos_fixos.empty:
    st.session_state.gastos_fixos = st.data_editor(st.session_state.gastos_fixos, num_rows="dynamic")

    if st.button("🪄 Lançar Gastos Fixos no Mês"):
        hoje = datetime.date.today()
        gastos_para_lancar = st.session_state.gastos_fixos.copy()

        def montar_data(dia):
            try:
                return hoje.replace(day=int(dia))
            except ValueError:
                return hoje #SE O DIA DO VENCIMENTO FOR 31 E ESTIVERMOS EM FEV. ELE LANÇA PRO DIA DE HOJE PARA NÃO DAR ERRO.
            
        gastos_para_lancar["Data"] = gastos_para_lancar["Dia do Vencimento"].apply(montar_data)
        gastos_para_lancar = gastos_para_lancar.drop(columns=["Dia do Vencimento"])

        st.session_state.gastos = pd.concat([st.session_state.gastos, gastos_para_lancar], ignore_index=True)
        st.toast("Gastos fixos lançados com sucesso!", icon="🪄")
        st.rerun()