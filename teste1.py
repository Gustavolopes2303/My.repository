import streamlit as st
st.write("Hello world")
st.title("Saudação")
nome = st.text_input("Digite seu nome")
if nome: 
   st.write(nome.upper())
import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np

# --- DADOS DO SISTEMA: TERMOS E SIMULAÇÃO DE JURISPRUDÊNCIA ---

# Termos Jurídicos que serão contados
TERMOS_JURIDICOS = [
    "Dano Moral", "Indenização", "Recurso", "Petição", "Contrato",
    "Sentença", "Jurisprudência", "Reconvenção", "Precedente", "Citação"
]

# Definição de "Áreas do Direito" e como elas influenciam a frequência dos termos
# O valor é o FATOR que será multiplicado pela frequência base (para simular prevalência)
AREAS_DO_DIREITO = {
    "Direito do Consumidor": {
        "Dano Moral": 3, "Indenização": 2, "Contrato": 1.5, "Petição": 1, "Recurso": 0.8
    },
    "Direito Civil (Contratos)": {
        "Contrato": 3, "Reconvenção": 2, "Sentença": 1.5, "Indenização": 0.5, "Petição": 1
    },
    "Direito Processual": {
        "Recurso": 3, "Petição": 2.5, "Sentença": 2, "Precedente": 1.5, "Citação": 1
    }
}

# --- FUNÇÃO COMPLEXA: SIMULAÇÃO DE PROCESSAMENTO DE TEXTO ---

@st.cache_data
def simular_analise_frequencia(area_selecionada):
    """
    Simula o processamento de um grande corpo de jurisprudência
    e retorna a contagem de termos baseada na área do direito selecionada.
    """
    # 1. Frequência Base (Comum a todas as áreas - ruído)
    frequencia_base = {termo: random.randint(50, 150) for termo in TERMOS_JURIDICOS}
    
    # 2. Aplica o Fator de Prevalência da Área Selecionada
    frequencia_final = frequencia_base.copy()
    fator_previo = AREAS_DO_DIREITO.get(area_selecionada, {})
    
    for termo, fator in fator_previo.items():
        # Aumenta a contagem de termos relevantes para a área (complexidade)
        aumento = int(frequencia_base[termo] * fator * np.random.uniform(1.5, 2.5))
        frequencia_final[termo] += aumento
    
    # 3. Cria o DataFrame para Visualização
    df = pd.DataFrame(
        list(frequencia_final.items()), 
        columns=['Termo', 'Frequência']
    ).sort_values(by='Frequência', ascending=False).reset_index(drop=True)
    
    return df

# --- ESTRUTURA E LAYOUT STREAMLIT ---

st.set_page_config(
    page_title="Streamlit Lexicographer ⚖️",
    page_icon="📜",
    layout="wide"
)

st.title("⚖️ Lexicographer: Análise de Frequência de Termos Jurídicos")
st.markdown("Simulação da análise de jurisprudência. Escolha a área para ver a prevalência dos termos.")

# --- ENTRADA DE DADOS E CONTROLES ---
col_select, col_metric = st.columns([1, 2])

with col_select:
    st.subheader("Configurações de Análise")
    area_selecionada = st.selectbox(
        "Selecione a Área do Direito para Análise:",
        list(AREAS_DO_DIREITO.keys())
    )

# --- PROCESSAMENTO E GERAÇÃO DO DATAFRAME ---
# A função é chamada aqui, e o cache garante que não recalcule se a área não mudar
df_frequencia = simular_analise_frequencia(area_selecionada)

# --- RESULTADOS MÉTRICOS E GERAIS ---
total_termos = df_frequencia['Frequência'].sum()
termo_mais_frequente = df_frequencia.iloc[0]['Termo']
frequencia_top = df_frequencia.iloc[0]['Frequência']

with col_metric:
    st.subheader("Visão Geral da Análise")
    col_m1, col_m2 = st.columns(2)
    
    col_m1.metric(label="Total de Termos Analisados (Simulado)", value=f"{total_termos:,}", delta="Total de ocorrências")
    col_m2.metric(label="Termo Mais Frequente", value=termo_mais_frequente, delta=f"{frequencia_top} ocorrências")

st.markdown("---")

# --- VISUALIZAÇÃO DE DADOS ---
st.header(f"Frequência de Termos em **{area_selecionada}**")

col_graph, col_data = st.columns([2, 1])

with col_graph:
    st.subheader("Gráfico de Frequência (Top 10)")
    
    # Criação do Gráfico de Barras (Visualização Jurídica)
    fig, ax = plt.subplots(figsize=(10, 5))
    df_frequencia_top10 = df_frequencia.head(10)
    
    # Escolhe cores para destaque: o top 1 é diferente
    cores = ['#2E86C1'] * len(df_frequencia_top10)
    cores[0] = '#E74C3C' # Destaque vermelho para o termo mais frequente

    ax.bar(df_frequencia_top10['Termo'], df_frequencia_top10['Frequência'], color=cores)
    
    ax.set_title(f'Top 10 Termos em {area_selecionada}', fontsize=14)
    ax.set_ylabel('Contagem (Simulada)')
    ax.set_xlabel('Termo Jurídico')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

with col_data:
    st.subheader("Dados Detalhados")
    # Tabela de dados brutos
    st.dataframe(df_frequencia, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Nota: Os dados de frequência são gerados por um modelo de simulação para fins de demonstração.")
