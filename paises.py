import streamlit as st
import re  # Biblioteca padrão do Python para Expressões Regulares (busca e substituição de texto)
import pandas as pd

# --- LISTA DE TERMOS JURÍDICOS (O "Coração" do Projeto) ---
# Você pode expandir ou mudar essa lista à vontade!
TERMOS_CHAVE = [
    "Petição Inicial",
    "Contrato Social",
    "Acórdão",
    "Jurisprudência",
    "Requerido",
    "Requerente",
    "Exceção",
    "Recurso",
    "Sentença",
    "Agravo",
    "Código Civil",
    "Código de Processo Civil",
    "Tribunal de Justiça"
]

# --- FUNÇÃO DE PROCESSAMENTO DE TEXTO ---
def destacar_termos(texto, termos):
    """Percorre o texto e formata os termos chave com HTML para destaque."""
    
    # 1. Cria um dicionário para contar a frequência dos termos
    contagem = {}
    
    # 2. Prepara o estilo de destaque (HTML/Markdown com cor vermelha)
    # Usamos re.escape para garantir que termos com caracteres especiais funcionem (ex: "Art. 5º")
    for termo in termos:
        # A expressão regular ignora maiúsculas/minúsculas (re.IGNORECASE)
        # e usa boundary \b para pegar a palavra inteira (evita que "Réu" destaque em "Reunião")
        
        # Cria a tag de destaque: **<span style="color:red;">TERMO</span>**
        estilo_destaque = f'**<span style="color:red;">{termo.upper()}</span>**'
        
        # Expressão regular para encontrar o termo
        pattern = r'\b' + re.escape(termo) + r'\b'
        
        # Encontra todas as ocorrências para a contagem
        ocorrencias = re.findall(pattern, texto, re.IGNORECASE)
        contagem[termo] = len(ocorrencias)
        
        # Substitui todas as ocorrências no texto pela versão formatada em vermelho
        texto = re.sub(pattern, estilo_destaque, texto, flags=re.IGNORECASE)
        
    return texto, contagem


# --- INTERFACE STREAMLIT ---

st.set_page_config(
    page_title="Detector de Termos Jurídicos Chave",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Detector de Termos Jurídicos Chave")
st.markdown("### Ferramenta de Análise Rápida de Documentos (LegalTech)")
st.caption("Cole um texto jurídico (petição, trecho de lei) para destacar instantaneamente os termos mais relevantes para a sua área.")

# 1. Área de texto para o usuário colar o documento
texto_entrada = st.text_area(
    "Cole seu texto jurídico aqui:",
    height=400,
    placeholder="Ex: 'O réu apresentou Petição Inicial com Recurso contra a Sentença do Tribunal de Justiça, alegando violação do Código Civil...'"
)

# 2. Botão para iniciar a análise
if st.button("Analisar Documento e Destacar Termos", type="primary"):
    
    if not texto_entrada:
        st.warning("Por favor, cole algum texto para iniciar a análise.")
    else:
        # Chama a função de destaque
        texto_destacado, contagem_termos = destacar_termos(texto_entrada, TERMOS_CHAVE)
        
        # --- COLUNA LATERAL (Contador, o que parece inteligente) ---
        with st.sidebar:
            st.header("📊 Frequência de Termos")
            
            # Converte a contagem para um DataFrame e filtra apenas os termos que apareceram
            df_contagem = pd.DataFrame(list(contagem_termos.items()), columns=['Termo', 'Ocorrências'])
            df_contagem = df_contagem[df_contagem['Ocorrências'] > 0]
            
            if not df_contagem.empty:
                # Exibe a tabela de forma simples e compacta
                st.dataframe(df_contagem, hide_index=True, use_container_width=True)
            else:
                st.info("Nenhum termo chave foi detectado no texto.")

        # --- COLUNA PRINCIPAL (O Efeito Visual Impactante) ---
        st.subheader("Documento com Destaques:")
        
        # st.markdown com a flag unsafe_allow_html é OBRIGATÓRIO 
        # para que o Streamlit exiba as cores e formatações HTML injetadas.
        st.markdown(texto_destacado, unsafe_allow_html=True)

st.markdown("---")
st.caption("Desenvolvido com Python e Streamlit.")
