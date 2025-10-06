import streamlit as st
st.write("Hello world")
st.title("Saudação")
nome = st.text_input("Digite seu nome")
if nome: 
   st.write(nome.upper())
import streamlit as st
import random

# --- Configurações da Página ---
st.set_page_config(
    page_title="Sua Citação do Dia (com um Toque) ✨",
    page_icon="💬",
    layout="centered"
)

# --- Dados das Citações e Autores ---
CITATIONS = [
    "A simplicidade é o último grau de sofisticação.",
    "O que não te mata, te fortalece.",
    "Eu sou mais esperto do que pareço e menos do que gostaria de ser.",
    "A vida é o que acontece enquanto você está ocupado fazendo outros planos.",
    "Tudo o que você pode imaginar é real.",
    "Seja a mudança que você deseja ver no mundo.",
    "A imaginação é mais importante que o conhecimento.",
    "A lógica te levará de A a B. A imaginação te levará a qualquer lugar.",
    "O sucesso é ir de fracasso em fracasso sem perder o entusiasmo."
]

AUTORES_IRÔNICOS = [
    "Um Desenvolvedor que Esqueceu de Commitar",
    "A Máquina de Café em Crise Existencial",
    "Um Gato Entediado Olhando para o Vazio",
    "A Última Fatia de Pizza",
    "Um Pato Usando Meias",
    "O Espírito da Segunda-feira",
    "Sua Torradeira Filosófica",
    "O Barulho da Chuva",
    "Uma Meia Solitária na Lavanderia"
]

# --- Título e Descrição ---
st.title("✨ Sua Citação do Dia (com um Toque)")
st.markdown("Descubra uma citação inspiradora (ou hilária) personalizada para você!")

# --- Entrada do Usuário ---
nome = st.text_input("Olá! Digite seu nome aqui:", max_chars=30)

# --- Gerar Citação ---
if st.button("Gerar Minha Citação!"):
    if nome:
        # Seleciona uma citação e um autor aleatoriamente
        citacao_selecionada = random.choice(CITATIONS)
        autor_selecionado = random.choice(AUTORES_IRÔNICOS)

        st.markdown("---") # Linha divisória

        # Exibe a citação personalizada
        st.subheader(f"Para você, {nome.title()}:") # Nome capitalizado

        # Estiliza a citação
        st.info(f'**"{citacao_selecionada}"**')
        st.markdown(f'<p style="text-align: right; color: grey;">— <i>{autor_selecionado}</i></p>', unsafe_allow_html=True)

        st.balloons() # Efeito visual divertido

    else:
        st.warning("Por favor, digite seu nome para gerar a citação!")

# --- Rodapé Opcional ---
st.markdown("---")
st.markdown("Feito com ❤️ e Streamlit.")
