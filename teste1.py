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

# --- DADOS DO SISTEMA: TAREFAS E SEUS ATRIBUTOS ---

# Cada tarefa é mapeada para o nível que ela exige de cada "humor" (0 a 10)
# A soma dos humores não precisa ser 10, mas indica a intensidade da tarefa
DADOS_TAREFAS = {
    'Revisão de Código Detalhada': {'Analitico': 9, 'Criatividade': 2, 'Organizacao': 7},
    'Brainstorming de Novo Recurso': {'Analitico': 4, 'Criatividade': 10, 'Organizacao': 3},
    'Organização de Documentação Técnica': {'Analitico': 5, 'Criatividade': 1, 'Organizacao': 10},
    'Desenvolvimento de Landing Page (Design)': {'Analitico': 3, 'Criatividade': 9, 'Organizacao': 5},
    'Debugging de Erro Crítico': {'Analitico': 10, 'Criatividade': 1, 'Organizacao': 6},
    'Preparação de Relatório Semanal': {'Analitico': 7, 'Criatividade': 2, 'Organizacao': 9},
    'Leitura e Pesquisa de Mercado': {'Analitico': 8, 'Criatividade': 4, 'Organizacao': 4},
}

# Criando um DataFrame para facilitar o manuseio e a análise
df_tarefas = pd.DataFrame.from_dict(DADOS_TAREFAS, orient='index')
df_tarefas.index.name = 'Tarefa'

# --- FUNÇÃO COMPLEXA: SIMULAÇÃO DE POPULARIDADE HISTÓRICA ---

@st.cache_data
def simular_popularidade():
    """Simula o histórico de popularidade de cada tarefa."""
    # Gera um fator de popularidade aleatório (para simular interações passadas)
    popularidade = {}
    for tarefa in df_tarefas.index:
        popularidade[tarefa] = random.randint(10, 100)
    return pd.Series(popularidade, name='Popularidade')

df_popularidade = simular_popularidade()

# --- FUNÇÃO COMPLEXA: ALGORITMO DE RECOMENDAÇÃO PONDERADA ---

def calcular_afinidade(df_tarefas_com_popularidade, pesos_usuario):
    """
    Calcula a pontuação de afinidade de cada tarefa.

    Pontuação = (Afinidade_Humor * Peso_Humor) + (Fator_Popularidade * Peso_Extra)
    """
    df = df_tarefas_com_popularidade.copy()
    
    # 1. CÁLCULO DO FATOR DE AFINIDADE DO HUMOR (baseado na preferência do usuário)
    # Exemplo: (Tarefa.Analitico * Peso_Usuario.Analitico) + (Tarefa.Criatividade * Peso_Usuario.Criatividade)
    df['Afinidade_Humor'] = (
        df['Analitico'] * pesos_usuario['Analitico'] +
        df['Criatividade'] * pesos_usuario['Criatividade'] +
        df['Organizacao'] * pesos_usuario['Organizacao']
    )
    
    # 2. NORMALIZAÇÃO DA POPULARIDADE (para que não domine a pontuação)
    max_pop = df['Popularidade'].max()
    df['Popularidade_Normalizada'] = df['Popularidade'] / max_pop
    
    # 3. PONTUAÇÃO FINAL PONDERADA
    # O peso de 0.2 é um fator fixo para garantir que a preferência do usuário (Afinidade_Humor) 
    # seja mais importante que a popularidade histórica.
    df['Pontuacao_Final'] = (df['Afinidade_Humor'] * 0.8) + (df['Popularidade_Normalizada'] * 0.2 * df['Afinidade_Humor'].max())
    
    return df.sort_values(by='Pontuacao_Final', ascending=False)

# --- ESTRUTURA E LAYOUT STREAMLIT ---

st.set_page_config(
    page_title="Oráculo de Afinidade e Tarefas ⚙️",
    page_icon="🧠",
    layout="wide"
)

st.title("⚙️ Oráculo de Afinidade: Encontre Sua Tarefa Ideal")
st.markdown("Ajuste seu humor atual para descobrir qual tarefa tem mais afinidade com você.")

# Combina os dados de atributos da tarefa com a popularidade simulada
df_tarefas_completo = df_tarefas.join(df_popularidade)

# --- SIDEBAR: CONTROLES DE AFINIDADE DO USUÁRIO ---
with st.sidebar:
    st.header("Seu Estado Mental (Pesos)")
    st.markdown("Defina sua afinidade com os humores de trabalho (0 = Baixo, 10 = Alto).")

    # Sliders para definir os pesos do usuário (Variável de Entrada Complexa)
    peso_analitico = st.slider('Foco Analítico / Racional', 0, 10, 5)
    peso_criatividade = st.slider('Criatividade / Inovação', 0, 10, 5)
    peso_organizacao = st.slider('Organização / Detalhismo', 0, 10, 5)

    pesos_usuario = {
        'Analitico': peso_analitico,
        'Criatividade': peso_criatividade,
        'Organizacao': peso_organizacao,
    }

    # Visualização da Distribuição dos Pesos (Gráfico de Pizza)
    st.subheader("Distribuição do Seu Humor")
    if sum(pesos_usuario.values()) > 0:
        fig, ax = plt.subplots()
        labels = pesos_usuario.keys()
        sizes = pesos_usuario.values()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#F4D03F', '#5DADE2', '#58D68D'])
        ax.axis('equal') # Garante que o gráfico de pizza seja circular
        st.pyplot(fig)
    else:
        st.info("Ajuste os sliders para ver a distribuição!")


# --- CORPO PRINCIPAL: RESULTADOS E RECOMENDAÇÃO ---
st.header("Resultado da Análise de Afinidade")

# Executa o algoritmo de recomendação
df_resultado = calcular_afinidade(df_tarefas_completo, pesos_usuario)

# 1. A Tarefa Mais Recomendada (Highlight)
tarefa_top = df_resultado.iloc[0]

st.info(f"""
### 🥇 RECOMENDAÇÃO TOP: {tarefa_top.name}
**Pontuação de Afinidade:** {tarefa_top['Pontuacao_Final']:.2f}
> Esta tarefa alinha-se perfeitamente com o seu foco em **Analítico ({tarefa_top['Analitico']}), Criatividade ({tarefa_top['Criatividade']}), e Organização ({tarefa_top['Organizacao']})**.
""")

st.markdown("---")

# 2. Tabela Detalhada com os Resultados
st.subheader("Ranking Completo das Tarefas")
st.markdown("A pontuação final é uma combinação do **Seu Humor** e da **Popularidade Histórica**.")

# Exibe o DataFrame de resultados, destacando a coluna de Pontuação Final
st.dataframe(
    df_resultado[['Analitico', 'Criatividade', 'Organizacao', 'Popularidade', 'Pontuacao_Final']].style.background_gradient(
        cmap='viridis', subset=['Pontuacao_Final']
    ).format(
        {'Popularidade': '{:.0f}', 'Pontuacao_Final': '{:.2f}'}
    ),
    use_container_width=True
)

st.markdown("---")
st.caption("Desenvolvido com Python, Streamlit e um algoritmo de afinidade ponderada.")

