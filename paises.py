import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Dashboard de Volumetria Processual",
    page_icon="📊",
    layout="wide"
)

# --- FUNÇÃO DE SIMULAÇÃO DE DADOS (O 'Banco de Dados') ---
@st.cache_data
def carregar_dados_simulados(num_processos=1500):
    """Gera um DataFrame simulando processos judiciais ao longo de 4 anos."""
    
    # Gera datas aleatórias entre 2021 e hoje
    datas = pd.to_datetime(pd.to_datetime('2021-01-01') + np.random.rand(num_processos) * (date.today() - date(2021, 1, 1)))

    # Gera ramos e status aleatórios
    ramos = np.random.choice(['Cível', 'Trabalhista', 'Tributário', 'Consumidor'], num_processos, p=[0.4, 0.3, 0.15, 0.15])
    status = np.random.choice(['Ativo', 'Arquivado', 'Suspenso', 'Em Recurso'], num_processos, p=[0.5, 0.25, 0.15, 0.1])
    
    # Gera valores de causa aleatórios (simulação)
    valores = np.round(np.random.lognormal(mean=9, sigma=1.5, size=num_processos), 2)

    df = pd.DataFrame({
        'Data Abertura': datas,
        'Ramo': ramos,
        'Status': status,
        'Valor Causa': valores
    })
    
    return df.sort_values('Data Abertura').reset_index(drop=True)

# Carrega os dados uma única vez (graças ao @st.cache_data)
df_original = carregar_dados_simulados()

# --- INTERFACE STREAMLIT ---

st.title("📊 Jurimetria: Dashboard de Volumetria")
st.markdown("### Análise de Processos Ativos e Tendências (Dados Simulados)")
st.caption("Filtre por Ramo do Direito e Período para visualizar o comportamento do portfólio de casos.")

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("⚙️ Filtros de Análise")

# Filtro 1: Ramo do Direito
ramos_unicos = ['Todos'] + list(df_original['Ramo'].unique())
filtro_ramo = st.sidebar.selectbox(
    "Escolha o Ramo do Direito:",
    ramos_unicos
)

# Filtro 2: Período (Slider de Anos)
min_ano = df_original['Data Abertura'].dt.year.min()
max_ano = df_original['Data Abertura'].dt.year.max()
filtro_anos = st.sidebar.slider(
    "Selecione o Intervalo de Anos:",
    min_value=min_ano,
    max_value=max_ano,
    value=(min_ano, max_ano)
)

# --- APLICAÇÃO DE FILTROS ---
df_filtrado = df_original.copy()

# Filtro de Ramo
if filtro_ramo != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Ramo'] == filtro_ramo]

# Filtro de Anos
df_filtrado = df_filtrado[
    (df_filtrado['Data Abertura'].dt.year >= filtro_anos[0]) & 
    (df_filtrado['Data Abertura'].dt.year <= filtro_anos[1])
]

# Exibe o status da filtragem (feedback visual)
st.sidebar.metric(
    "Processos Filtrados", 
    f"{len(df_filtrado):,}", 
    help="Número total de processos após aplicar os filtros."
)

# Verifica se há dados após a filtragem
if df_filtrado.empty:
    st.warning("Não há dados para os filtros selecionados.")
    st.stop() # Interrompe o restante da execução se não houver dados

# --- MÉTRICAS DE DESTAQUE (Métricas Gerenciais) ---
col1, col2, col3 = st.columns(3)

# Métrica 1: Total Ativo
total_ativos = len(df_filtrado[df_filtrado['Status'] == 'Ativo'])
col1.metric("Processos Ativos", f"{total_ativos:,}")

# Métrica 2: Valor Total das Causas
valor_total_causas = df_filtrado['Valor Causa'].sum()
col2.metric("Valor Total das Causas", f"R$ {valor_total_causas:,.2f}")

# Métrica 3: Processos Em Recurso
em_recurso = len(df_filtrado[df_filtrado['Status'] == 'Em Recurso'])
col3.metric("Em Recurso", f"{em_recurso:,}")


# --- VISUALIZAÇÕES (O Efeito UAU) ---

st.markdown("---")

# 1. Gráfico de Tendência (Volumetria Mensal)
st.subheader("Tendência de Abertura de Processos (Mensal)")
df_tendencia = df_filtrado.set_index('Data Abertura').resample('M').size().rename('Contagem')
st.line_chart(df_tendencia, use_container_width=True)


# 2. Distribuição por Status
st.subheader("Distribuição Atual por Status")
df_status = df_filtrado['Status'].value_counts().reset_index()
df_status.columns = ['Status', 'Contagem']

# Exibe o gráfico de barras simples do Streamlit
st.bar_chart(df_status.set_index('Status'), use_container_width=True)


st.markdown("---")
st.caption("Projeto de Jurimetria Simples criado com Python, Pandas e Streamlit.")
