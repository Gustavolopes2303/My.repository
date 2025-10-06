import streamlit as st
st.write("Hello world")
st.title("Saudação")
nome = st.text_input("Digite seu nome")
if nome:
   st.write(nome.upper())
import random
import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
# Biblioteca para Análise de Sentimento (Text Processing)
from textblob import TextBlob 
# Biblioteca para Visualização (Alternativa simples ao Altair/Plotly)
import matplotlib.pyplot as plt 

# --- Dicionários de Dados (Mantendo a Estrutura) ---

DADOS_CITACOES = {
    "SABIO": [
        "A simplicidade é o último grau de sofisticação.",
        "A vida é o que acontece enquanto você está ocupado fazendo outros planos.",
        "A verdadeira sabedoria está em reconhecer a própria ignorância."
    ],
    "IRRITADO": [
        "Por que você está me incomodando agora? Volte mais tarde.",
        "Se o seu problema tem solução, pare de se preocupar; se não tem, de que adianta?",
        "Este esforço não vale o tempo que gastamos aqui."
    ],
    "FILOSOFICO": [
        "Somos todos prisioneiros de nosso próprio modo de ver as coisas.",
        "Existir é resistir.",
        "Não tentes ser bem-sucedido, tenta antes ser um valor."
    ]
}

AUTORES_IRÔNICOS = {
    "SABIO": ["Um Esquilo Meditando", "O Café que Finalmente Aqueceu"],
    "IRRITADO": ["O Espírito da Segunda-feira às 8h", "Um Desenvolvedor que Esqueceu de Commitar"],
    "FILOSOFICO": ["A Última Fatia de Pizza", "Uma Meia Solitária na Lavanderia"]
}

HUMOR_MAP = {"SABIO": 1, "FILOSOFICO": 0, "IRRITADO": -1}

# --- FUNÇÕES COMPLEXAS ---

@st.cache_data
def gerar_dados_historicos(dias=30):
    """
    Simula 30 dias de interações do Oráculo.
    Isso substitui um banco de dados real.
    """
    dados = []
    data_fim = datetime.now().date()
    
    for i in range(dias):
        data = data_fim - timedelta(days=dias - 1 - i)
        
        # Simula uma regra de humor ligeiramente complexa
        if data.weekday() in [5, 6]: # Fim de semana é mais suave
            humor_gerado = random.choice(["SABIO", "FILOSOFICO"])
        elif data.day % 7 == 0: # Uma vez por semana fica irritado
            humor_gerado = "IRRITADO"
        else:
            humor_gerado = random.choice(["SABIO", "FILOSOFICO", "IRRITADO"])
            
        citacao_gerada = random.choice(DADOS_CITACOES[humor_gerado])
        
        # Análise de Sentimento (Complexidade de Processamento de Texto)
        blob = TextBlob(citacao_gerada)
        sentimento = blob.sentiment.polarity
        
        dados.append({
            'Data': data,
            'Humor_Nome': humor_gerado,
            'Humor_Valor': HUMOR_MAP[humor_gerado],
            'Citacao': citacao_gerada,
            'Sentimento': sentimento
        })
    
    # Cria o DataFrame para análise
    df = pd.DataFrame(dados)
    return df

def gerar_previsao(df_historico):
    """
    Faz uma 'previsão' simples do humor de amanhã
    baseada na média do sentimento dos últimos 7 dias.
    """
    df_ultimos_7 = df_historico.tail(7)
    sentimento_medio = df_ultimos_7['Sentimento'].mean()

    # Lógica de Previsão
    if sentimento_medio > 0.1:
        return "SABIO (Positivo: >0.1)", "A tendência aponta para um dia de calma e sabedoria."
    elif sentimento_medio < -0.1:
        return "IRRITADO (Negativo: <-0.1)", "Cuidado, a irritação está no ar. Evite perguntas complexas."
    else:
        return "FILOSOFICO (Neutro)", "O dia será de ponderação. O Oráculo estará em modo reflexivo."

# --- ESTRUTURA E LAYOUT STREAMLIT ---

st.set_page_config(
    page_title="Streamlit Time-Traveler 🔮",
    page_icon="🕰️",
    layout="wide"
)

# Geração de dados e cache
df_historico = gerar_dados_historicos()

st.title("🕰️ Oráculo Time-Traveler: Análise e Previsão")
st.markdown("Consulte o humor passado, presente e futuro do nosso Oráculo Temporal.")

tab_atual, tab_historico, tab_previsao = st.tabs(["**Consulta Atual**", "**Análise Histórica**", "**Previsão Futura**"])

# --- TAB 1: CONSULTA ATUAL ---
with tab_atual:
    col_input, col_output = st.columns([1, 2])
    
    with col_input:
        st.subheader("Fale com o Oráculo (Agora)")
        nome = st.text_input("Seu nome:", max_chars=30)
        
        if st.button("Gerar Citação do Dia", use_container_width=True):
            if nome:
                # Usa a lógica de humor do Oráculo anterior (mais simples para o HOJE)
                # O humor do Oráculo 'hoje' é baseado na média de Sentimento Histórico
                humor_base = df_historico['Humor_Nome'].mode().iloc[0] # Ex: o humor mais frequente
                
                citacao = random.choice(DADOS_CITACOES[humor_base])
                autor = random.choice(AUTORES_IRÔNICOS[humor_base])
                
                with col_output:
                    st.success(f"**Oráculo em modo '{humor_base}'**")
                    st.subheader(f"Para você, {nome.title()}:")
                    st.markdown(f'<h1 style="text-align: center; color: #1E8449;">"{citacao}"</h1>', unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: right; font-size: 1.2em; color: grey;">— <i>{autor}</i></p>', unsafe_allow_html=True)
                    st.balloons()
            else:
                st.warning("Preencha seu nome.")

# --- TAB 2: ANÁLISE HISTÓRICA ---
with tab_historico:
    st.header("Gráfico de Humor Histórico (Últimos 30 Dias)")
    st.markdown("Valor do Humor: `1` (Sábio), `0` (Filosófico), `-1` (Irritado).")
    
    # 1. Gráfico de Linha (Visualização de Dados)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_historico['Data'], df_historico['Humor_Valor'], marker='o', linestyle='-', color='teal')
    ax.set_title('Flutuação Diária do Humor do Oráculo')
    ax.set_ylabel('Valor do Humor')
    ax.set_xlabel('Data')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # 2. Tabela de Dados (Complexidade de UI - Tabela Interativa)
    st.subheader("Registro de Citações e Sentimentos")
    st.dataframe(df_historico[['Data', 'Humor_Nome', 'Citacao', 'Sentimento']].sort_values(by='Data', ascending=False), 
                 use_container_width=True)

# --- TAB 3: PREVISÃO FUTURA ---
with tab_previsao:
    st.header(f"Previsão para {datetime.now().date() + timedelta(days=1)}")
    
    # Executa a função de previsão
    humor_previsto, detalhe = gerar_previsao(df_historico)
    
    col_previsao_1, col_previsao_2 = st.columns([1, 3])
    
    with col_previsao_1:
        st.metric(label="Humor Previsto", value=humor_previsto.split(' ')[0], delta=humor_previsto.split(' ')[1] if len(humor_previsto.split(' ')) > 1 else None)

    with col_previsao_2:
        st.subheader("Análise da Tendência")
        st.info(detalhe)
        st.markdown(f"*(Baseado na média de sentimento dos **últimos 7 dias**.)*")
        
    st.markdown("---")
    st.dataframe(df_historico.tail(7)[['Data', 'Sentimento']].style.background_gradient(cmap='RdYlGn', subset=['Sentimento']), 
                 use_container_width=True)
