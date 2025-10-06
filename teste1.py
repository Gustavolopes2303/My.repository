import streamlit as st
st.write("Hello world")
st.title("Saudação")
nome = st.text_input("Digite seu nome")
if nome:
   st.write(nome.upper())
import random

# Lista de citações clássicas ou inspiradoras
CITATIONS = [
    "A simplicidade é o último grau de sofisticação.",
    "O que não te mata, te fortalece.",
    "Eu sou mais esperto do que pareço e menos do que gostaria de ser.",
    "A vida é o que acontece enquanto você está ocupado fazendo outros planos.",
    "Tudo o que você pode imaginar é real.",
    "Seja a mudança que você deseja ver no mundo."
]

# Lista de 'autores' inesperados/engraçados
AUTORES_IRÔNICOS = [
    "Um Desenvolvedor que Esqueceu de Commitar",
    "A Máquina de Café em Crise Existencial",
    "Um Gato Entediado Olhando para o Vazio",
    "A Última Fatia de Pizza",
    "Um Pato Usando Meias",
    "O Espírito da Segunda-feira"
]

def gerar_citacao_ironica():
    """Seleciona e combina aleatoriamente uma citação e um autor irônico."""
    # 1. Escolhe uma citação aleatoriamente
    citacao_selecionada = random.choice(CITATIONS)

    # 2. Escolhe um autor aleatoriamente
    autor_selecionado = random.choice(AUTORES_IRÔNICOS)

    # 3. Formata e imprime a saída
    print("-" * 40)
    print(f'"{citacao_selecionada}"')
    print(f'— {autor_selecionado}')
    print("-" * 40)

# Chama a função principal
if __name__ == "__main__":
    gerar_citacao_ironica()
 
