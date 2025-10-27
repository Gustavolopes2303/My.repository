import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt # Adicionado para gráficos

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Calculadora de Rescisão Completa (Estimativa 2024/2025)",
    page_icon="👷",
    layout="centered"
)

# --- 2. FUNÇÕES DE CÁLCULO (Lógica Trabalhista e Tributária) ---

def calcular_meses_proporcionais(admissao, demissao):
    """Calcula os meses proporcionais (com a regra dos 15 dias)."""
    if demissao <= admissao:
        return 0
    diff = relativedelta(demissao, admissao)
    meses = diff.years * 12 + diff.months
    # Regra dos 15 dias para contagem do avo proporcional
    if demissao.day >= 15:
        meses += 1
    return meses

def calcular_aviso_previo(admissao, demissao, salario, motivo):
    """Calcula o aviso prévio proporcional (Lei 12.506/2011)."""
    if motivo != "sem justa causa":
        return 0.0, 0
    
    anos = relativedelta(demissao, admissao).years
    dias = 30 + anos * 3
    if dias > 90:
        dias = 90
        
    valor = (salario / 30) * dias
    return valor, dias

def calcular_fgts_multa(salario, meses_trabalhados):
    """Calcula o FGTS depositado e a Multa de 40% (simplificação)."""
    # Simplificação: FGTS total depositado = 8% * Salário * Meses
    fgts_depositado = salario * meses_trabalhados * 0.08
    multa_fgts = fgts_depositado * 0.40
    return fgts_depositado, multa_fgts

def calcular_inss_progressivo(base):
    """Tabela progressiva de INSS 2024 (Mantida para simulação)."""
    faixas = [
        (1412.00, 0.075),
        (2666.68, 0.09),
        (4000.03, 0.12),
        (7786.02, 0.14)
    ]
    imposto = 0.0
    base_anterior = 0.0
    
    for limite, aliquota in faixas:
        if base > limite:
            imposto += (limite - base_anterior) * aliquota
            base_anterior = limite
        else:
            imposto += (base - base_anterior) * aliquota
            break
            
    if base > 7786.02: # Teto do INSS em 2024
        imposto = 908.86 
        
    return max(imposto, 0.0)

def calcular_irrf(base, dependentes):
    """Cálculo simplificado de IRRF (Tabela Mensal 2024)."""
    # Dedução de dependente (R$ 189,59 em 2024)
    deducao_dependente = dependentes * 189.59
    base -= deducao_dependente

    # Tabela progressiva
    if base <= 2259.20:
        aliquota, parcela = 0.0, 0.0
    elif base <= 2826.65:
        aliquota, parcela = 0.075, 169.44
    elif base <= 3751.05:
        aliquota, parcela = 0.15, 381.44
    elif base <= 4664.68:
        aliquota, parcela = 0.225, 662.77
    else:
        aliquota, parcela = 0.275, 896.00
    
    imposto = base * aliquota - parcela
    
    return max(imposto, 0.0)

# --- 3. INTERFACE STREAMLIT ---

st.title("👷 Calculadora de Rescisão Completa")
st.markdown("### Simulação detalhada de todas as verbas (CLT, INSS e IRRF)")
st.caption("Ferramenta educacional de LegalTech para estimativas iniciais.")

st.markdown("---")

# 3.1. Entrada de Dados
salario_base = st.number_input(
    "1. Salário Mensal Bruto (R$):",
    min_value=0.01,
    value=2400.00,
    step=100.00,
    format="%.2f"
)

col_adm, col_dem = st.columns(2)
with col_adm:
    data_admissao = st.date_input("2. Data de Admissão (Início):", value=date(2022, 1, 1))
with col_dem:
    data_demissao = st.date_input("3. Data de Demissão (Fim):", value=date.today(), min_value=data_admissao)

col_mot, col_dias = st.columns(2)
with col_mot:
    motivo = st.selectbox("4. Motivo da Rescisão:", ["sem justa causa", "por justa causa"])
with col_dias:
    dias_trabalhados_no_mes = st.number_input("5. Dias trabalhados no mês da demissão (Saldo de Salário):", 
                                              min_value=0, max_value=31, value=data_demissao.day)

col_dep, col_ferias = st.columns(2)
with col_dep:
    dependentes = st.number_input("6. Número de dependentes (IR):", min_value=0, max_value=10, value=0)
with col_ferias:
    ferias_vencidas = st.radio("7. Períodos de férias vencidas:", ["0", "1", "2"])
qtd_ferias_vencidas = int(ferias_vencidas)

st.markdown("---")

# --- 4. CÁLCULO E EXIBIÇÃO ---

if st.button("Calcular Rescisão Completa", type="primary"):
    
    meses_prop = calcular_meses_proporcionais(data_admissao, data_demissao)
    
    if meses_prop <= 0:
        st.error("Verifique as datas. A demissão deve ser posterior à admissão.")
    else:
        # --- CÁLCULO DAS VERBAS DE PROVENTOS ---
        
        # 1. Saldo de Salário
        saldo_salario = (salario_base / 30) * dias_trabalhados_no_mes
        
        # 2. 13º Salário Proporcional
        valor_13_proporcional = (salario_base / 12) * meses_prop
        
        # 3. Férias Proporcionais + 1/3
        valor_ferias_prop_base = (salario_base / 12) * meses_prop
        valor_terco_prop = valor_ferias_prop_base / 3
        
        # 4. Férias Vencidas + 1/3
        valor_ferias_vencidas = qtd_ferias_vencidas * (salario_base + (salario_base / 3))
        
        # 5. Aviso Prévio Indenizado
        aviso_valor, aviso_dias = calcular_aviso_previo(data_admissao, data_demissao, salario_base, motivo)
        
        # --- CÁLCULO TRIBUTÁRIO E DESCONTOS ---
        
        # Base de INSS (Incide sobre Saldo de Salário e 13º. Simplificação: apenas Saldo)
        base_inss = saldo_salario 
        inss = calcular_inss_progressivo(base_inss)
        
        # Base de IRRF (Incide sobre Saldo de Salário - INSS. Férias e Aviso são ISENTOS)
        base_irrf_salario = saldo_salario - inss
        ir_salario = calcular_irrf(base_irrf_salario, dependentes)
        
        # IRRF Exclusivo (Simplificação: apenas 13º Salário)
        inss_13 = calcular_inss_progressivo(valor_13_proporcional)
        ir_13_exclusivo = calcular_irrf(valor_13_proporcional - inss_13, 0) # 13º não usa dependentes para base
        
        # --- CÁLCULO FGTS E MULTA ---
        
        # Simplificação dos meses trabalhados para FGTS
        meses_fgts = relativedelta(data_demissao, data_admissao).years * 12 + relativedelta(data_demissao, data_admissao).months
        fgts_depositado, multa_fgts = calcular_fgts_multa(salario_base, meses_fgts)
        
        # --- TOTAIS ---
        
        proventos = saldo_salario + valor_13_proporcional + valor_ferias_prop_base + valor_terco_prop + valor_ferias_vencidas + aviso_valor
        descontos = inss + ir_salario + ir_13_exclusivo
        total_liquido = proventos - descontos
        
        # FGTS e Multa são valores a sacar, não entram no Líquido da folha
        total_a_sacar_fgts = fgts_depositado + multa_fgts

        # --- EXIBIÇÃO DOS RESULTADOS ---
        
        st.subheader(f"🧾 Rescisão Estimada (Tempo de Serviço: {meses_prop} meses)")
        
        col_liq, col_sacar = st.columns(2)
        col_liq.success(f"### 💰 Líquido a Receber (Folha): R$ {total_liquido:,.2f}")
        col_sacar.info(f"### 🏦 FGTS + Multa (a Sacar): R$ {total_a_sacar_fgts:,.2f}")
        
        st.markdown("---")

        # Detalhamento
        st.markdown("#### Detalhamento dos Proventos e Descontos")
        
        col_det1, col_det2 = st.columns(2)
        
        with col_det1:
            st.metric("Saldo de Salário", f"R$ {saldo_salario:,.2f}")
            st.metric("13º Salário Proporcional", f"R$ {valor_13_proporcional:,.2f}")
            st.metric("Férias Proporcionais + 1/3", f"R$ {valor_ferias_prop_base + valor_terco_prop:,.2f}")
            st.metric("Férias Vencidas + 1/3", f"R$ {valor_ferias_vencidas:,.2f}")
            st.metric(f"Aviso Prévio ({aviso_dias} dias)", f"R$ {aviso_valor:,.2f}")
            
        with col_det2:
            st.markdown(f"**Proventos Brutos:** R$ {proventos:,.2f}")
            st.markdown("---")
            st.error(f"**Desconto INSS (Salário):** R$ {inss:,.2f}")
            st.error(f"**Desconto IRRF (Salário):** R$ {ir_salario:,.2f}")
            st.error(f"**Desconto IRRF (13º Exclusivo):** R$ {ir_13_exclusivo:,.2f}")
            st.markdown(f"**Descontos Totais:** - R$ {descontos:,.2f}")

        # Gráfico de Pizza (Proporção das Verbas de Recebimento)
        st.markdown("---")
        st.subheader("Visualização da Composição dos Proventos")

        categorias_pizza = {
            "Saldo Salário": saldo_salario,
            "13º Salário Prop.": valor_13_proporcional,
            "Férias Prop. + 1/3": valor_ferias_prop_base + valor_terco_prop,
            "Férias Vencidas + 1/3": valor_ferias_vencidas,
            "Aviso Prévio": aviso_valor,
        }
        
        labels_pizza = []
        sizes_pizza = []
        for cat, val in categorias_pizza.items():
            if val > 0:
                labels_pizza.append(cat)
                sizes_pizza.append(val)
        
        if sum(sizes_pizza) > 0:
            plt.figure(figsize=(7, 7))
            plt.pie(sizes_pizza, labels=labels_pizza, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
            plt.title("Composição dos Proventos Rescisórios", fontsize=14)
            st.pyplot(plt)
        
        st.markdown("---")
        st.info(f"""
        ⚠️ **Aviso Legal (Simulação):**
        * Cálculo baseado nas tabelas de INSS e IRRF de **2024**.
        * Não inclui faltas, horas extras, adicionais (insalubridade/periculosidade) ou outras deduções.
        * **Consulte um profissional** (contador ou advogado trabalhista) para valores oficiais.
        """)

st.caption("Projeto de LegalTech (Direito do Trabalho) com Python e Streamlit.")
