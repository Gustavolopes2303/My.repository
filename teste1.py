import streamlit as st
st.write("Hello world")
st.title("Saudação")
nome = st.texto_input("Digite seu nome")
if nome:
   st.write(nome.upper())
 
