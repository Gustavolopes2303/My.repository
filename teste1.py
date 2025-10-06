import streamlit as st
st.write("Hello world")
st.title("Saudação")
nome = st.text_input("Digite seu nome")
if nome:
   st.write(nome.upper())
import random
import streamlit as st
import random
from datetime import datetime

# --- Dicionários de Dados (Complexidade de Dados) ---

# Citações categorizadas por "humor"
DADOS_CITACOES = {
    "SABIO": [
        "A simplicidade é o último grau de sofisticação.",
        "O que não te mata, te fortalece, a menos que mate.",
        "A vida é o que acontece enquanto você está ocupado fazendo outros planos.",
        "A verdadeira sabedoria está em reconhecer a própria ignorância."
    ],
    "IRRITADO": [
        "Por que você está me incomodando agora? Volte mais tarde.",
        "A pressa é inimiga da perfeição. E do meu bom humor.",
        "Se o seu problema tem solução, pare de se preocupar; se não tem, de que adianta?",
        "Tudo o que você pode imaginar é real. E provavelmente muito chato."
    ],
    "FILOSOFICO": [
        "Somos todos prisioneiros de nosso próprio modo de ver as coisas.",
        "O mundo que criamos é um produto do nosso pensamento.",
        "Existir é resistir.",
        "Não tentes ser bem-sucedido, tenta antes ser um valor."
    ]
}

# Autores categorizados por "humor"
AUTORES_IRÔNICOS = {
    "SABIO": [
        "Um Esquilo Meditando",
        "A Lua Cheia",
        "O Café que Finalmente Aqueceu"
    ],
    "IRRITADO": [
        "Um Desenvolvedor que Esqueceu de Commitar",
        "A Máquina de Café em Crise Existencial",
        "O Espírito da Segunda-feira às 8h"
    ],
    "FILOSOFICO": [
        "A Última Fatia de Pizza (ponderando seu destino)",
        "O Barulho da Chuva em Outra Dimensão",
        "Uma Meia Solitária na Lavanderia (buscando sentido)"
    ]
}

# --- Lógica de Humor Temporal (Complexidade Lógica) ---

def definir_humor_do_oraculo():
    """Define o humor do Oráculo baseado na hora e no dia."""
    agora = datetime.now()
    hora = agora.hour
    dia_da_semana = agora.weekday() # 0=Segunda, 6=Domingo

    humor = "FILOSOFICO" # Humor padrão

    if dia_da_semana < 5: # Dias úteis (Segunda a Sexta)
        if 6 <= hora < 10:
            humor = "SABIO" # Conselhos para começar o dia
        elif 10 <= hora < 16:
            humor = "IRRITADO" # Estresse do trabalho/rotina
        elif 16 <= hora < 20:
            humor = "FILOSOFICO" # Ponderando o fim do dia
    else: # Fim de semana (Sábado e Domingo)
        if 8 <= hora < 16:
            humor = "SABIO" # Calma do fim de semana
        else:
            humor = "FILOSOFICO" # Pensamentos noturnos

    return humor

# --- Estrutura e Layout Streamlit (Complexidade de Interface) ---

st.set_page_config(
    page_title="Oráculo Temporal de Conselhos ✨",
    page_icon="🔮",
    layout="wide" # Layout expandido
)

st.title("🔮 Oráculo Temporal de Conselhos")
st.markdown("Meu humor e conselho mudam conforme a hora do dia e o dia da semana... Seja cauteloso!")

# Container para organizar o input e o resultado
col1, col2 = st.columns([1, 2]) # Duas colunas: uma para o input, duas para o output

with col1:
    st.subheader("Quem Ousa Consultar?")
    nome = st.text_input("Digite seu nome, viajante:", max_chars=30)
    
    if st.button("Consultar o Oráculo!", use_container_width=True):
        if not nome:
            st.error("O Oráculo não fala com anônimos!")
        else:
            # Estado para acionar a exibição no col2
            st.session_state['consultado'] = True
            st.session_state['nome'] = nome
    
    # Exibe o humor atual do Oráculo em tempo real (DEBUG/Criatividade)
    humor_atual = definir_humor_do_oraculo()
    st.markdown(f"Status do Oráculo (agora): **{humor_atual}**")


# Lógica de exibição no Coluna 2
with col2:
    if 'consultado' in st.session_state and st.session_state['consultado']:
        nome_usuario = st.session_state['nome'].title()
        
        # 1. Determina o humor e as listas de citação/autor
        humor = definir_humor_do_oraculo()
        
        citacao_selecionada = random.choice(DADOS_CITACOES[humor])
        autor_selecionado = random.choice(AUTORES_IRÔNICOS[humor])
        
        # 2. Exibição Dinâmica (muda conforme o humor)
        if humor == "IRRITADO":
            st.error(f"**ALERTA! O Oráculo está de mau humor ({humor})!**")
            st.subheader(f"Resposta curta e grossa para **{nome_usuario}**:")
        elif humor == "SABIO":
            st.success(f"**O Oráculo está sereno ({humor}).**")
            st.subheader(f"Uma pepita de ouro para **{nome_usuario}**:")
        else: # FILOSOFICO
            st.warning(f"**O Oráculo está reflexivo ({humor}).**")
            st.subheader(f"Pondere sobre isso, **{nome_usuario}**:")

        st.markdown("---") 
        
        # 3. Exibe a citação
        st.markdown(f'<h1 style="text-align: center; color: #2E86C1;">"{citacao_selecionada}"</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align: right; font-size: 1.2em; color: grey;">— <i>{autor_selecionado}</i></p>', unsafe_allow_html=True)

        st.snow() # Efeito visual sutil ou st.balloons()
        
        # Limpa o estado para permitir nova consulta
        st.session_state['consultado'] = False
