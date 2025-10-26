import streamlit as st
import pandas as pd
from pypdf import PdfReader
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Metadados Forenses de Documentos",
    page_icon="🔍",
    layout="centered"
)

# --- FUNÇÃO DE EXTRAÇÃO DE METADADOS ---
def extrair_metadados_pdf(uploaded_file):
    """Extrai metadados essenciais de um PDF."""
    try:
        # Abrindo o arquivo PDF
        reader = PdfReader(uploaded_file)
        
        # Acessando o dicionário de metadados
        metadata = reader.metadata
        
        # Formatando as datas
        def formatar_data(data_obj):
            if data_obj:
                # O formato do pypdf é complexo, mas convertemos para um formato amigável.
                if isinstance(data_obj, datetime):
                    return data_obj.strftime("%d/%m/%Y %H:%M:%S")
                return str(data_obj).split('+')[0].replace('D:','')
            return "Não Encontrado"

        # Dicionário de resultados
        dados = {
            "Metadado": [
                "Autor/Criador", 
                "Software Produtor", 
                "Data de Criação Original", 
                "Data da Última Modificação",
                "Número de Páginas"
            ],
            "Valor Encontrado": [
                metadata.author or metadata.creator or "Desconhecido",
                metadata.producer or "Desconhecido",
                formatar_data(metadata.creation_date),
                formatar_data(metadata.modification_date),
                len(reader.pages)
            ]
        }
        
        df = pd.DataFrame(dados)
        return df, metadata.producer
    except Exception as e:
        st.error(f"Erro ao processar o arquivo. Certifique-se de que é um PDF válido. Erro: {e}")
        return None, None

# --- INTERFACE STREAMLIT ---

st.title("🔍 Metadados Forenses de Documentos")
st.markdown("## Scanner de Informações Ocultas (LegalTech)")
st.caption("Faça o upload de um arquivo PDF para analisar dados como autor original, software de criação e histórico de modificação. Uma ferramenta simples que gera *insights* valiosos em processos.")

uploaded_file = st.file_uploader(
    "Carregar Arquivo PDF (.pdf)", 
    type=["pdf"],
    accept_multiple_files=False 
)

if uploaded_file is not None:
    st.success("Arquivo carregado com sucesso!")
    
    # Processamento e Extração
    df_metadados, produtor = extrair_metadados_pdf(uploaded_file)
    
    if df_metadados is not None:
        
        # --- EXIBIÇÃO CRIATIVA E INTELIGENTE ---
        st.subheader("📋 Relatório de Análise Forense")
        
        # Destaque do Software Produtor (O que faz parecer inteligente)
        st.info(f"O Software Produtor do documento é: **{produtor or 'Não Registrado'}**")
        
        # Exibição dos Metadados em uma Tabela Elegante
        # Usa Markdown/HTML para centralizar e dar destaque visual
        st.dataframe(df_metadados.set_index('Metadado'), use_container_width=True)
        
        # --- ANÁLISE BÔNUS DE TIMELINE ---
        
        data_criacao_str = df_metadados.loc[df_metadados['Metadado'] == 'Data de Criação Original', 'Valor Encontrado'].iloc[0]
        data_modificacao_str = df_metadados.loc[df_metadados['Metadado'] == 'Data da Última Modificação', 'Valor Encontrado'].iloc[0]
        
        # Tenta calcular a diferença
        try:
            data_criacao = datetime.strptime(data_criacao_str.split(' ')[0], "%d/%m/%Y")
            data_modificacao = datetime.strptime(data_modificacao_str.split(' ')[0], "%d/%m/%Y")
            dias_entre = (data_modificacao - data_criacao).days
            
            st.markdown("---")
            st.subheader("⌛ Timeline do Documento")
            
            # Métrica que parece difícil de calcular
            st.metric(
                label="Tempo entre Criação e Última Modificação", 
                value=f"{dias_entre} dias",
                help="Indica o período em que o documento pode ter sido revisado ativamente."
            )
            
        except:
            st.warning("Não foi possível calcular o tempo de vida (datas ausentes ou incompletas).")
