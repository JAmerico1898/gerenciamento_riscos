import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import base64

# Configuração da página
st.set_page_config(
    page_title="Risco de Liquidez Bancário - O Caso Northern Rock",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Funções auxiliares
def add_logo_and_styling():
    # Estilos CSS personalizados
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem !important;
        font-weight: 600;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.8rem;
    }
    .sub-header {
        font-size: 1.5rem !important;
        font-weight: 500;
        color: #2563EB;
        margin-bottom: 1rem;
    }
    .risk-high {
        color: #DC2626;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .risk-medium {
        color: #F59E0B;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .risk-low {
        color: #10B981;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .reference-box {
        background-color: #F3F4F6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #2563EB;
    }
    .info-box {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #3B82F6;
    }
    .warning-box {
        background-color: #FEF3C7;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #F59E0B;
    }
    </style>
    """, unsafe_allow_html=True)

def create_northern_rock_data():
    # Dados históricos do Northern Rock
    dates = ["Jun-98", "Dec-98", "Jun-99", "Dec-99", "Jun-00", "Dec-00", "Jun-01", 
             "Dec-01", "Jun-02", "Dec-02", "Jun-03", "Dec-03", "Jun-04", "Dec-04", 
             "Jun-05", "Dec-05", "Jun-06", "Dec-06", "Jun-07"]
    
    # Composição de passivos em bilhões de libras
    retail_deposits = [8.0, 9.0, 10.0, 11.0, 12.0, 12.5, 13.0, 13.5, 14.0, 15.0, 16.0, 17.0, 18.0, 20.0, 22.0, 22.5, 23.0, 24.0, 24.4]
    securitized_notes = [0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 15.0, 18.0, 22.0, 26.0, 30.0, 35.0, 40.0, 45.7]
    other_liabilities = [8.0, 10.0, 12.0, 14.0, 16.0, 16.5, 17.0, 18.5, 21.0, 23.0, 25.0, 26.0, 30.0, 32.0, 35.0, 37.5, 40.0, 42.0, 42.0]
    equity = [2.0, 2.0, 2.0, 2.2, 2.5, 2.7, 2.8, 3.0, 3.2, 3.5, 3.7, 3.8, 4.0, 4.2, 4.5, 4.7, 4.8, 5.0, 5.3]
    
    total_assets = [sum(x) for x in zip(retail_deposits, securitized_notes, other_liabilities, equity)]
    
    # Para os cálculos de risco
    leverage = [round(total_assets[i] / equity[i], 1) for i in range(len(dates))]
    retail_deposit_ratio = [round(retail_deposits[i] / total_assets[i] * 100, 1) for i in range(len(dates))]
    securitized_ratio = [round(securitized_notes[i] / total_assets[i] * 100, 1) for i in range(len(dates))]
    
    df = pd.DataFrame({
        'Data': dates,
        'Depósitos de Varejo': retail_deposits,
        'Notas Securitizadas': securitized_notes,
        'Outros Passivos': other_liabilities,
        'Patrimônio': equity,
        'Total de Ativos': total_assets,
        'Alavancagem': leverage,
        'Proporção de Depósitos (%)': retail_deposit_ratio,
        'Proporção de Securitização (%)': securitized_ratio
    })
    
    return df

def calculate_lcr(hqla, saidas_30dias):
    """Calcula o Liquidity Coverage Ratio"""
    if saidas_30dias == 0:
        return float('inf')
    return (hqla / saidas_30dias) * 100

def calculate_nsfr(funding_estavel, ativos_longo_prazo):
    """Calcula o Net Stable Funding Ratio"""
    if ativos_longo_prazo == 0:
        return float('inf')
    return (funding_estavel / ativos_longo_prazo) * 100

def calculate_liquidity_risk(ativos_liquidos_pct, wholesale_funding_pct):
    """Calcula o risco de liquidez com base na composição de ativos e fontes de financiamento"""
    # Quanto menor a proporção de ativos líquidos e maior a dependência de wholesale funding, maior o risco
    risk_score = (100 - ativos_liquidos_pct) * (wholesale_funding_pct / 100)
    
    # Normalizar para uma escala de 0-100
    risk_score = min(100, max(0, risk_score))
    
    return risk_score

def plot_balance_sheet(ativos_liquidos_pct, wholesale_funding_pct):
    """Cria um gráfico do balanço patrimonial do banco simulado"""
    # Calcular valores baseados nas porcentagens
    ativos_liquidos = ativos_liquidos_pct
    ativos_iliquidos = 100 - ativos_liquidos_pct
    
    depositos_varejo = 100 - wholesale_funding_pct
    funding_wholesale = wholesale_funding_pct
    
    # Criar figura para o balanço
    fig = go.Figure()
    
    # Adicionar barras para ativos
    fig.add_trace(go.Bar(
        y=['Ativos'],
        x=[ativos_liquidos],
        name='Ativos Líquidos',
        orientation='h',
        marker=dict(color='rgba(16, 185, 129, 0.8)'),
        text=f"{ativos_liquidos}%",
        textposition='inside',
        hoverinfo='text',
        hovertext=f'Ativos Líquidos: {ativos_liquidos}%'
    ))
    
    fig.add_trace(go.Bar(
        y=['Ativos'],
        x=[ativos_iliquidos],
        name='Financiamentos Imobiliários (Ilíquidos)',
        orientation='h',
        marker=dict(color='rgba(245, 158, 11, 0.8)'),
        text=f"{ativos_iliquidos}%",
        textposition='inside',
        hoverinfo='text',
        hovertext=f'Ativos Ilíquidos: {ativos_iliquidos}%'
    ))
    
    # Adicionar barras para passivos
    fig.add_trace(go.Bar(
        y=['Passivos'],
        x=[depositos_varejo],
        name='Depósitos de Varejo',
        orientation='h',
        marker=dict(color='rgba(37, 99, 235, 0.8)'),
        text=f"{depositos_varejo}%",
        textposition='inside',
        hoverinfo='text',
        hovertext=f'Depósitos de Varejo: {depositos_varejo}%'
    ))
    
    fig.add_trace(go.Bar(
        y=['Passivos'],
        x=[funding_wholesale],
        name='Funding Wholesale/Securitizado',
        orientation='h',
        marker=dict(color='rgba(220, 38, 38, 0.8)'),
        text=f"{funding_wholesale}%",
        textposition='inside',
        hoverinfo='text',
        hovertext=f'Funding Wholesale: {funding_wholesale}%'
    ))
    
    # Atualizar layout
    fig.update_layout(
        barmode='stack',
        title='Composição Simulada do Balanço Patrimonial',
        height=250,
        margin=dict(l=50, r=50, t=80, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        xaxis=dict(
            title='Porcentagem (%)',
            range=[0, 100]
        )
    )
    
    return fig

def simulate_crisis(ativos_liquidos_pct, wholesale_funding_pct, stress_level):
    """Simula uma crise de liquidez e seu impacto no banco"""
    # Parâmetros de simulação
    dias_simulacao = 30
    impacto_varejo = min(50, stress_level * 5)  # Impacto limitado nos depósitos de varejo
    impacto_wholesale = min(90, stress_level * 9)  # Impacto maior no funding wholesale
    
    # Calcular valores iniciais
    depositos_varejo_inicial = 100 - wholesale_funding_pct
    funding_wholesale_inicial = wholesale_funding_pct
    ativos_liquidos_inicial = ativos_liquidos_pct
    ativos_iliquidos_inicial = 100 - ativos_liquidos_pct
    
    # Arrays para armazenar resultados da simulação
    dias = list(range(dias_simulacao + 1))
    depositos_varejo_arr = [depositos_varejo_inicial]
    funding_wholesale_arr = [funding_wholesale_inicial]
    ativos_liquidos_arr = [ativos_liquidos_inicial]
    ativos_iliquidos_arr = [ativos_iliquidos_inicial]
    saldo_liquido_arr = [0]
    
    # Simular dia a dia
    for dia in range(1, dias_simulacao + 1):
        # Probabilidade crescente de corrida bancária
        prob_corrida = min(1.0, dia / dias_simulacao * (stress_level / 10))
        
        # Cálculo de saídas
        saida_varejo = depositos_varejo_arr[dia-1] * (impacto_varejo/100) * prob_corrida / dias_simulacao
        saida_wholesale = funding_wholesale_arr[dia-1] * (impacto_wholesale/100) * prob_corrida / (dias_simulacao/2)
        
        # Novos valores
        novo_deposito_varejo = max(0, depositos_varejo_arr[dia-1] - saida_varejo)
        novo_funding_wholesale = max(0, funding_wholesale_arr[dia-1] - saida_wholesale)
        
        # Uso de ativos líquidos para cobrir saídas
        saida_total = saida_varejo + saida_wholesale
        novo_ativos_liquidos = max(0, ativos_liquidos_arr[dia-1] - saida_total)
        
        # Se não houver ativos líquidos suficientes, o banco falha
        saldo_liquido = novo_ativos_liquidos - (ativos_liquidos_arr[dia-1] - saida_total)
        
        # Adicionar aos arrays
        depositos_varejo_arr.append(novo_deposito_varejo)
        funding_wholesale_arr.append(novo_funding_wholesale)
        ativos_liquidos_arr.append(novo_ativos_liquidos)
        ativos_iliquidos_arr.append(ativos_iliquidos_inicial)  # não muda no curto prazo
        saldo_liquido_arr.append(saldo_liquido)
    
    # Detecção de falha de liquidez
    failed_day = None
    for i, saldo in enumerate(ativos_liquidos_arr):
        if saldo <= 0 and i > 0:
            failed_day = i
            break
    
    # Criar dataframe com os resultados
    results_df = pd.DataFrame({
        'Dia': dias,
        'Depósitos de Varejo': depositos_varejo_arr,
        'Funding Wholesale': funding_wholesale_arr,
        'Ativos Líquidos': ativos_liquidos_arr,
        'Ativos Ilíquidos': ativos_iliquidos_arr,
        'Saldo Líquido': saldo_liquido_arr
    })
    
    # Gráfico dos resultados
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=results_df['Dia'],
        y=results_df['Depósitos de Varejo'],
        mode='lines',
        name='Depósitos de Varejo',
        line=dict(color='rgb(37, 99, 235)', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=results_df['Dia'],
        y=results_df['Funding Wholesale'],
        mode='lines',
        name='Funding Wholesale',
        line=dict(color='rgb(220, 38, 38)', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=results_df['Dia'],
        y=results_df['Ativos Líquidos'],
        mode='lines',
        name='Ativos Líquidos',
        line=dict(color='rgb(16, 185, 129)', width=2)
    ))
    
    # Adicionar linha vertical no dia da falha, se houver
    if failed_day is not None:
        fig.add_shape(
            type="line",
            x0=failed_day,
            y0=0,
            x1=failed_day,
            y1=100,
            line=dict(
                color="Black",
                width=3,
                dash="dash",
            )
        )
        fig.add_annotation(
            x=failed_day,
            y=50,
            text=f"Falha no dia {failed_day}",
            showarrow=True,
            arrowhead=1,
            ax=50,
            ay=0
        )
    
    fig.update_layout(
        title='Simulação de Crise de Liquidez',
        xaxis_title='Dias',
        yaxis_title='Porcentagem (%)',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig, failed_day, results_df

def apply_stress_test(lcr_value, nsfr_value, ativos_liquidos_pct, wholesale_funding_pct):
    """Aplica testes de estresse para avaliar a resistência do banco"""
    # Cenários de estresse
    scenarios = {
        "Corrida Bancária Moderada": {
            "retail_outflow": 15,  # 15% dos depósitos de varejo saem
            "wholesale_outflow": 35,  # 35% do funding wholesale sai
            "market_liquidity": 0.8  # Liquidez de mercado reduzida em 20%
        },
        "Crise de Funding": {
            "retail_outflow": 5,
            "wholesale_outflow": 70,
            "market_liquidity": 0.6
        },
        "Choque Sistêmico": {
            "retail_outflow": 25,
            "wholesale_outflow": 80,
            "market_liquidity": 0.4
        }
    }
    
    results = {}
    
    for scenario_name, params in scenarios.items():
        # Calcular novos valores após o estresse
        new_retail = (100 - wholesale_funding_pct) * (1 - params["retail_outflow"]/100)
        new_wholesale = wholesale_funding_pct * (1 - params["wholesale_outflow"]/100)
        new_liquid_assets = ativos_liquidos_pct * params["market_liquidity"]
        
        # Calcular novos indicadores
        new_lcr = calculate_lcr(new_liquid_assets, (new_retail + new_wholesale) * 0.3)
        new_nsfr = calculate_nsfr(new_retail + (new_wholesale * 0.5), (100 - ativos_liquidos_pct))
        
        # Verificar sobrevivência
        survived = new_lcr >= 70 and new_liquid_assets > 0
        
        results[scenario_name] = {
            "survived": survived,
            "new_lcr": new_lcr,
            "new_nsfr": new_nsfr,
            "liquid_assets_remaining": new_liquid_assets
        }
    
    return results

# Aplicativo principal
def main():
    add_logo_and_styling()
    
    # Cabeçalho principal
    st.markdown("<h1 class='main-header'>Risco de Liquidez Bancário</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='sub-header'>O Caso Northern Rock e Lições para a Gestão de Risco de Liquidez</h2>", unsafe_allow_html=True)
    
    # Barra lateral com navegação
    st.sidebar.image("https://raw.githubusercontent.com/JAmerico1898/gereneciamento_riscos/e0978ccb2502a2b6a3f03dbe6f2ebe6773812b7a/nothern_rock_logo.png", width=200)
    st.sidebar.markdown("## Navegação")
    menu = st.sidebar.selectbox(
        "Escolha um módulo:",
        ["Introdução ao Risco de Liquidez", 
         "O Caso Northern Rock", 
         "Simulador de Balanço e Risco",
         "Técnicas de Gestão de Risco",
         "Stress Testing de Liquidez",
         "Sobre o Aplicativo"]
    )
    
    # Dados históricos do Northern Rock
    df_northern_rock = create_northern_rock_data()
    
    # Conteúdo baseado na opção selecionada
    if menu == "Introdução ao Risco de Liquidez":
        st.markdown("## 📚 Conceito e Importância")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown("""
            ### O que é Risco de Liquidez?
            
            O risco de liquidez refere-se à incapacidade de uma instituição financeira honrar suas obrigações de curto prazo sem incorrer em perdas inaceitáveis. Ele ocorre quando um banco não consegue obter recursos suficientes para atender suas necessidades imediatas de caixa, seja por não conseguir vender ativos rapidamente a preços razoáveis (risco de liquidez de mercado) ou por não conseguir obter financiamento adequado (risco de liquidez de financiamento).
            
            ### Por que é crítico para bancos?
            
            Os bancos são particularmente vulneráveis ao risco de liquidez devido à natureza de seu modelo de negócios: eles captam recursos de curto prazo (como depósitos à vista) e os aplicam em ativos de longo prazo (como empréstimos imobiliários). Este **descasamento de prazos** é uma característica fundamental da intermediação financeira, mas também cria vulnerabilidades.
            """)
            
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.markdown("""
            **Fontes típicas de risco de liquidez:**
            - **Corridas bancárias**: Quando muitos depositantes retiram seus fundos simultaneamente
            - **Perda de acesso ao mercado de funding**: Quando fontes de financiamento (depositantes) secam
            - **Deterioração da confiança no banco**: Pode levar a dificuldades de refinanciamento
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.image("https://raw.githubusercontent.com/JAmerico1898/gereneciamento_riscos/9f1b012f661712ed63bb2896ddd375fb8fa6c2e0/liquidity_mismatch.jpg", 
                     caption="Modelo básico de transformação de maturidade em bancos", 
                     width=350)
    
        st.markdown("### Manifestações do Risco de Liquidez")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='reference-box'>", unsafe_allow_html=True)
            st.markdown("""
            #### Liquidez de Financiamento (Passivos)
            
            Refere-se à capacidade do banco de obter recursos para financiar seus ativos e atender suas obrigações.
            
            **Indicadores:**
            - Concentração de fontes de funding
            - Proporção de financiamento de curto prazo
            - Custo de funding em comparação ao mercado
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div class='reference-box'>", unsafe_allow_html=True)
            st.markdown("""
            #### Liquidez de Mercado (Ativos)
            
            Refere-se à capacidade do banco de vender ativos rapidamente sem causar mudanças significativas em seus preços.
            
            **Indicadores:**
            - Bid-ask spread dos ativos
            - Volume de negociação
            - Tempo necessário para liquidar posições
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("### Consequências de uma Crise de Liquidez")
        
        st.markdown("""
        Se não gerenciado adequadamente, o risco de liquidez pode levar a:
        
        1. **Venda forçada de ativos** a preços descontados
        2. **Aumento nos custos de financiamento**
        3. **Intervenção regulatória**
        4. **Falência do banco**
        5. **Contágio para outras instituições financeiras**
        
        > *"A liquidez pode desaparecer rapidamente, e a iliquidez pode durar por um período prolongado. Como suas fontes são inerentemente imprevisíveis, o risco de liquidez deve ser considerado um dos riscos mais críticos em um ambiente bancário."*
        > — Comitê de Basileia de Supervisão Bancária
        """)
    
    elif menu == "O Caso Northern Rock":
        st.markdown("## 🏦 O Caso Northern Rock: Anatomia de uma Quebra Bancária")
        
        tab1, tab2, tab3 = st.tabs(["Contexto Histórico", "Modelo de Negócios", "A Crise"])
        
        with tab1:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("""
                ### Origens e Crescimento
                
                O Northern Rock foi fundado em 1965, resultado da fusão entre a Northern Counties Permanent Building Society (estabelecida em 1850) e a Rock Building Society (estabelecida em 1865). Inicialmente operava como uma sociedade de crédito imobiliário (*building society*) mutuamente detida por seus membros, com foco na região nordeste da Inglaterra.
                
                Em 1997, o banco passou por um processo de "desmutualização" e se tornou uma companhia de capital aberto listada na Bolsa de Valores de Londres. Esta transição marcou o início de um período de crescimento agressivo.
                """)
            
            with col2:
                st.image("https://raw.githubusercontent.com/JAmerico1898/gereneciamento_riscos/e0978ccb2502a2b6a3f03dbe6f2ebe6773812b7a/northern-rock-headquarters.jpg",
                        caption="Sede do Northern Rock em Newcastle", 
                        width=300)            
            st.markdown("""
            ### Expansão Acelerada
            
            Entre 1998 e 2007, o Northern Rock experimentou um crescimento extraordinário:
            
            - Os ativos totais aumentaram de 17,4 bilhões para 113,5 bilhões de libras
            - Uma taxa de crescimento anual equivalente a 23,2%
            - Tornou-se o quinto maior banco hipotecário do Reino Unido
            """)
            
            # Gráfico de crescimento do Northern Rock
            st.markdown("#### Crescimento dos Ativos e Passivos (1998-2007)")
            
            fig = px.area(
                df_northern_rock,
                x='Data',
                y=['Depósitos de Varejo', 'Notas Securitizadas', 'Outros Passivos', 'Patrimônio'],
                title='Composição dos Passivos do Northern Rock, 1998-2007',
                labels={'value': 'Bilhões de Libras', 'variable': 'Tipo de Passivo'},
                color_discrete_map={
                    'Depósitos de Varejo': 'rgba(37, 99, 235, 0.8)',
                    'Notas Securitizadas': 'rgba(220, 38, 38, 0.8)',
                    'Outros Passivos': 'rgba(245, 158, 11, 0.8)',
                    'Patrimônio': 'rgba(16, 185, 129, 0.8)'
                }
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.markdown("""
            ### Modelo de Negócios do Northern Rock
            
            O Northern Rock desenvolveu um modelo de negócios altamente dependente de financiamento no mercado de capitais, diferente do modelo bancário tradicional que se baseia principalmente em depósitos de varejo.
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                st.markdown("""
                #### Ativo
                
                - **Empréstimos hipotecários de alta qualidade**: Foco em empréstimos prime para o mercado residencial do Reino Unido
                - **Baixa diversificação**: Concentração excessiva em um único tipo de ativo
                - **Originar para distribuir**: Originação de hipotecas para securitização
                """)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='warning-box'>", unsafe_allow_html=True)
                st.markdown("""
                #### Passivo
                
                - **Dependência de funding de atacado**: Apenas 23% dos passivos eram depósitos de varejo em 2007
                - **Securitização**: Extensa utilização de veículos de securitização (Granite)
                - **Descasamento de prazos**: Financiamento de curto prazo para ativos de longo prazo
                """)
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("#### Mecanismo de Securitização")
            st.image("https://raw.githubusercontent.com/JAmerico1898/gereneciamento_riscos/9f1b012f661712ed63bb2896ddd375fb8fa6c2e0/securitization_structure.png", 
                      caption="Estrutura típica de securitização", 
                      width=700)

           
            st.markdown("""
            ### Evolução da Estrutura de Funding
            
            Um aspecto crítico do modelo de negócios do Northern Rock foi a drástica mudança na sua estrutura de financiamento. Em junho de 1998, 60% dos passivos eram depósitos de varejo. Em junho de 2007, este percentual havia caído para apenas 23%.
            """)
            
            # Gráfico da evolução das fontes de financiamento
            fig = px.line(
                df_northern_rock,
                x='Data',
                y=['Proporção de Depósitos (%)', 'Proporção de Securitização (%)'],
                title='Evolução da Estrutura de Funding do Northern Rock',
                labels={'value': 'Porcentagem (%)', 'variable': 'Fonte de Funding'},
                color_discrete_map={
                    'Proporção de Depósitos (%)': 'rgba(37, 99, 235, 0.8)',
                    'Proporção de Securitização (%)': 'rgba(220, 38, 38, 0.8)'
                }
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            st.markdown("""
            ### Cronologia da Crise
            """)
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.image("https://raw.githubusercontent.com/JAmerico1898/gereneciamento_riscos/e0978ccb2502a2b6a3f03dbe6f2ebe6773812b7a/images.jpg",
                         caption="Clientes fazendo fila durante a corrida bancária", 
                         width=250)

            with col2:
                st.markdown("""
                #### Eventos Principais
                
                - **9 de agosto de 2007**: BNP Paribas congela fundos de investimento com exposição a hipotecas subprime dos EUA, desencadeando uma crise de liquidez no mercado interbancário
                
                - **13-14 de agosto de 2007**: Northern Rock alerta os reguladores do Reino Unido sobre suas dificuldades de financiamento
                
                - **14 de agosto - 13 de setembro**: Tentativas frustradas de encontrar um comprador para o banco
                
                - **13 de setembro**: BBC anuncia que o Northern Rock buscou apoio de emergência do Banco da Inglaterra
                
                - **14 de setembro**: Banco da Inglaterra anuncia oficialmente suporte de liquidez de emergência
                
                - **14-17 de setembro**: Corrida bancária - clientes retiram £2 bilhões (cerca de 8% dos depósitos de varejo)
                
                - **17 de setembro**: Governo anuncia garantia para todos os depósitos existentes do Northern Rock
                
                - **22 de fevereiro de 2008**: Banco é nacionalizado pelo governo britânico
                """)
            
            st.markdown("#### Composição dos Passivos Antes e Depois da Corrida")
            
            # Dados da composição de passivos antes e depois da corrida
            data = {
                'Categoria': ['Notas Securitizadas', 'Covered Bonds', 'Depósitos de Varejo', 'Funding Wholesale', 'Empréstimo do Banco da Inglaterra'],
                'Junho 2007 (£m)': [45698, 8105, 24350, 26710, 0],
                'Dezembro 2007 (£m)': [43070, 8938, 10469, 11472, 28473]
            }
            
            df_corrida = pd.DataFrame(data)
            
            # Gráfico de barras lado a lado
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=df_corrida['Categoria'],
                y=df_corrida['Junho 2007 (£m)'],
                name='Junho 2007',
                marker_color='rgba(55, 83, 109, 0.7)'
            ))
            
            fig.add_trace(go.Bar(
                x=df_corrida['Categoria'],
                y=df_corrida['Dezembro 2007 (£m)'],
                name='Dezembro 2007',
                marker_color='rgba(26, 118, 255, 0.7)'
            ))
            
            fig.update_layout(
                title='Composição dos Passivos do Northern Rock Antes e Depois da Corrida (milhões £)',
                xaxis_tickfont_size=14,
                yaxis=dict(
                    title='Valor (milhões £)',
                    titlefont_size=16,
                    tickfont_size=14,
                ),
                legend=dict(
                    x=0,
                    y=1.0,
                    bgcolor='rgba(255, 255, 255, 0)',
                    bordercolor='rgba(255, 255, 255, 0)'
                ),
                barmode='group',
                bargap=0.15,
                bargroupgap=0.1,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            ### Lições da Quebra do Northern Rock
            
            A falência do Northern Rock destaca várias vulnerabilidades críticas no modelo de negócios bancário:
            
            1. **Dependência excessiva de financiamento de atacado**: A confiança em funding de curto prazo nos mercados de capitais tornou o banco vulnerável a mudanças nas condições de liquidez do mercado
            
            2. **Descasamento de prazos extremo**: Ativos de longo prazo (hipotecas) financiados com passivos de curto prazo
            
            3. **Crescimento muito rápido**: Taxa de crescimento anual de 23% era insustentável e aumentou a vulnerabilidade
            
            4. **Falta de diversificação**: Concentração excessiva tanto nos ativos (hipotecas) quanto nas fontes de financiamento
            
            5. **Supervisão regulatória inadequada**: Falha dos reguladores em identificar os riscos acumulados no modelo de negócios
            """)
            
    elif menu == "Simulador de Balanço e Risco":
        st.markdown("## 📊 Simulador de Balanço e Risco de Liquidez")
        
        st.markdown("""
        Este simulador permite você experimentar diferentes configurações de balanço patrimonial de um banco hipotético 
        e visualizar o impacto dessas escolhas no risco de liquidez. Use os controles abaixo para ajustar as proporções.
        """)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### Composição dos Ativos")
            ativos_liquidos_pct = st.slider("Ativos Líquidos (%)", 0, 100, 30, 
                                         help="Ativos de alta qualidade que podem ser convertidos rapidamente em caixa")
            ativos_iliquidos_pct = 100 - ativos_liquidos_pct
            st.markdown(f"Financiamentos Imobiliários (Ilíquidos): **{ativos_iliquidos_pct}%**")
        
        with col2:
            st.markdown("### Fontes de Financiamento")
            wholesale_funding_pct = st.slider("Funding Wholesale/Securitizado (%)", 0, 100, 70,
                                          help="Inclui empréstimos interbancários, notas securitizadas e outros financiamentos de mercado")
            depositos_varejo_pct = 100 - wholesale_funding_pct
            st.markdown(f"Depósitos de Varejo: **{depositos_varejo_pct}%**")
        
        # Visualização do balanço
        st.markdown("### Balanço Patrimonial Simulado")
        fig_balance = plot_balance_sheet(ativos_liquidos_pct, wholesale_funding_pct)
        st.plotly_chart(fig_balance, use_container_width=True)
        
        # Cálculo de indicadores de risco
        st.markdown("### Indicadores de Risco de Liquidez")
        
        # Calcular LCR e NSFR simulados
        lcr_value = calculate_lcr(ativos_liquidos_pct, wholesale_funding_pct * 0.3)
        nsfr_value = calculate_nsfr(depositos_varejo_pct + (wholesale_funding_pct * 0.5), ativos_iliquidos_pct)
        
        # Calcular score de risco geral
        risk_score = calculate_liquidity_risk(ativos_liquidos_pct, wholesale_funding_pct)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="Liquidity Coverage Ratio (LCR)",
                value=f"{lcr_value:.1f}%",
                delta=f"{lcr_value - 100:.1f}%" if lcr_value != 100 else "0%",
                delta_color="normal" if lcr_value >= 100 else "inverse"
            )
            st.markdown("Requerimento regulatório: >= 100%")
        
        with col2:
            st.metric(
                label="Net Stable Funding Ratio (NSFR)",
                value=f"{nsfr_value:.1f}%",
                delta=f"{nsfr_value - 100:.1f}%" if nsfr_value != 100 else "0%",
                delta_color="normal" if nsfr_value >= 100 else "inverse"
            )
            st.markdown("Requerimento regulatório: >= 100%")
        
        with col3:
            # Determinar nível de risco e formato de exibição
            if risk_score < 30:
                risk_level = "BAIXO"
                risk_class = "risk-low"
            elif risk_score < 60:
                risk_level = "MÉDIO"
                risk_class = "risk-medium"
            else:
                risk_level = "ALTO"
                risk_class = "risk-high"
            
            st.metric(
                label="Score de Risco de Liquidez",
                value=f"{risk_score:.1f}/100",
                delta=None
            )
            st.markdown(f"Nível de Risco: <span class='{risk_class}'>{risk_level}</span>", unsafe_allow_html=True)
        
        # Comparação com o Northern Rock
        st.markdown("### Comparação com o Northern Rock")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            **Composição do Northern Rock em Junho 2007:**
            - Ativos Líquidos: aproximadamente 15%
            - Funding Wholesale/Securitizado: aproximadamente 77%
            - Alavancagem (Ativos/Patrimônio): 58.2x
            """)
        
        with col2:
            if risk_score > 50:
                st.warning("⚠️ O seu modelo de balanço apresenta características de vulnerabilidade similares ao Northern Rock", icon="⚠️")
            else:
                st.success("✅ O seu modelo de balanço é mais resiliente que o do Northern Rock", icon="✅")
        
        # Análise de vulnerabilidade
        st.markdown("### Análise de Vulnerabilidade")
        
        if wholesale_funding_pct > 60:
            st.markdown("<div class='warning-box'>", unsafe_allow_html=True)
            st.markdown(f"""
            **Alta dependência de funding wholesale ({wholesale_funding_pct}%)**
            
            Uma dependência excessiva de financiamento de atacado/securitizado torna o banco vulnerável a 
            interrupções no mercado de capitais, como ocorreu no caso do Northern Rock. A falta de acesso 
            a este mercado pode rapidamente transformar-se em uma crise de liquidez.
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        
        if ativos_liquidos_pct < 20:
            st.markdown("<div class='warning-box'>", unsafe_allow_html=True)
            st.markdown(f"""
            **Baixo nível de ativos líquidos ({ativos_liquidos_pct}%)**
            
            Um colchão de liquidez insuficiente limita a capacidade do banco de resistir a 
            saídas inesperadas de caixa sem recorrer à venda de ativos ilíquidos com desconto 
            ou a fontes de financiamento de emergência.
            """)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Simulação de estresse
        st.markdown("### Simulação de Estresse de Liquidez")
        
        stress_level = st.slider("Nível de Estresse do Mercado", 1, 10, 5,
                               help="1 = condições normais, 10 = crise severa")
        
        if st.button("Executar Simulação"):
            fig_sim, failed_day, sim_results = simulate_crisis(ativos_liquidos_pct, wholesale_funding_pct, stress_level)
            st.plotly_chart(fig_sim, use_container_width=True)
            
            if failed_day:
                st.error(f"O banco falhou no dia {failed_day} da simulação devido à falta de liquidez.")
                st.markdown(f"""
                **Análise da Falha:**
                - Os ativos líquidos foram esgotados devido à saída rápida de funding
                - A alta proporção de financiamento wholesale acelerou a crise
                - O banco não conseguiu vender ativos ilíquidos a tempo de cobrir as saídas
                """)
            else:
                st.success("O banco conseguiu sobreviver ao período de estresse simulado.")
                final_liquidity = sim_results.iloc[-1]['Ativos Líquidos']
                st.markdown(f"""
                **Análise da Resistência:**
                - Ativos líquidos remanescentes: {final_liquidity:.2f}%
                - O colchão de liquidez foi suficiente para absorver as saídas
                - A proporção adequada entre ativos líquidos e funding wholesale contribuiu para a resiliência
                """)
    
    elif menu == "Técnicas de Gestão de Risco":
        st.markdown("## 🛡️ Técnicas de Gestão do Risco de Liquidez")
        
        st.markdown("""
        A gestão eficaz do risco de liquidez envolve várias estratégias e ferramentas complementares. 
        As técnicas a seguir são essenciais para mitigar vulnerabilidades como as observadas no caso Northern Rock.
        """)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Gap de Liquidez", 
            "Colchão de Liquidez", 
            "Diversificação", 
            "Testes de Estresse", 
            "Planos de Contingência"
        ])
        
        with tab1:
            st.markdown("### 📈 Gap de Liquidez (Liquidity Gap Analysis)")
            
            st.markdown("""
            A análise de gap de liquidez avalia o descompasso entre ativos líquidos e passivos exigíveis em diferentes horizontes de tempo.
            
            #### Objetivo:
            Identificar desequilíbrios potenciais entre entradas e saídas de caixa em diferentes períodos, permitindo um gerenciamento proativo do fluxo de caixa.
            """)
            
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.markdown("""
            #### Implementação Prática:
            1. Categorizar ativos e passivos por prazos de vencimento
            2. Calcular o gap líquido (ativos - passivos) para cada período
            3. Identificar períodos com gaps negativos significativos
            4. Desenvolver estratégias para cobrir esses déficits potenciais
            """)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Exemplo de gráfico de gap de liquidez
            st.markdown("#### Exemplo de Análise de Gap de Liquidez")
            
            # Dados de exemplo para o gráfico
            faixas = ["0-7 dias", "8-30 dias", "31-90 dias", "91-180 dias", "181-360 dias", "Acima de 1 ano"]
            ativos_exemplo = [15, 10, 20, 25, 30, 100]
            passivos_exemplo = [20, 15, 15, 20, 25, 80]
            gap_exemplo = [a - p for a, p in zip(ativos_exemplo, passivos_exemplo)]
            
            # Criar dataframe
            df_gap = pd.DataFrame({
                'Faixa': faixas,
                'Ativos': ativos_exemplo,
                'Passivos': passivos_exemplo,
                'Gap': gap_exemplo
            })
            
            # Gráfico de barras para ativos e passivos
            fig1 = go.Figure()
            
            fig1.add_trace(go.Bar(
                x=df_gap['Faixa'],
                y=df_gap['Ativos'],
                name='Ativos',
                marker_color='rgba(16, 185, 129, 0.8)'
            ))
            
            fig1.add_trace(go.Bar(
                x=df_gap['Faixa'],
                y=df_gap['Passivos'],
                name='Passivos',
                marker_color='rgba(220, 38, 38, 0.8)'
            ))
            
            fig1.update_layout(
                title='Ativos e Passivos por Faixa de Vencimento',
                xaxis_title='Faixa de Vencimento',
                yaxis_title='Valor (milhões)',
                barmode='group',
                height=400
            )
            
            # Gráfico de linha para o gap
            fig2 = go.Figure()
            
            fig2.add_trace(go.Bar(
                x=df_gap['Faixa'],
                y=df_gap['Gap'],
                name='Gap de Liquidez',
                marker_color=['rgba(220, 38, 38, 0.8)' if x < 0 else 'rgba(16, 185, 129, 0.8)' for x in df_gap['Gap']]
            ))
            
            fig2.add_trace(go.Scatter(
                x=df_gap['Faixa'],
                y=[0] * len(df_gap),
                mode='lines',
                line=dict(color='black', width=1, dash='dash'),
                showlegend=False
            ))
            
            fig2.update_layout(
                title='Gap de Liquidez por Faixa de Vencimento',
                xaxis_title='Faixa de Vencimento',
                yaxis_title='Gap (milhões)',
                height=300
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown("""
            #### Interpretação:
            - **Gap positivo**: Indica excesso de liquidez no período
            - **Gap negativo**: Indica déficit potencial de liquidez que precisará ser gerenciado
            
            #### Northern Rock - O que deu errado:
            O Northern Rock apresentava grandes gaps negativos nos prazos mais curtos, devido ao seu forte descasamento de prazos. O banco não mantinha ativos líquidos suficientes para cobrir a potencial não renovação de seus financiamentos de curto prazo.
            """)
        
        with tab2:
            st.markdown("### 💧 Colchão de Liquidez (Liquidity Buffer)")
            
            st.markdown("""
            Um colchão de liquidez consiste na manutenção de ativos líquidos de alta qualidade (HQLA) que podem ser 
            convertidos rapidamente em caixa com perda mínima de valor.
            
            #### Objetivo:
            Garantir que a instituição tenha recursos líquidos suficientes para resistir a um período de estresse de liquidez.
            """)
            
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.markdown("""
            #### Componentes típicos do colchão de liquidez:
            1. **Caixa e reservas no banco central**
            2. **Títulos soberanos de alta qualidade**
            3. **Títulos corporativos de grau de investimento**
            4. **Linhas de crédito comprometidas**
            """)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Simulador de colchão de liquidez
            st.markdown("#### Simulador de Colchão de Liquidez")
            
            col1, col2 = st.columns(2)
            
            with col1:
                hqla = st.number_input("Ativos líquidos de alta qualidade (HQLA) (milhões)", min_value=0, max_value=1000, value=500)
                st.markdown("""
                Exemplos de HQLA:
                - Caixa
                - Reservas no banco central
                - Títulos soberanos AAA-AA
                - Outros ativos líquidos de alta qualidade
                """)
            
            with col2:
                saidas_esperadas = st.number_input("Saídas de caixa esperadas em 30 dias (milhões)", min_value=1, max_value=1000, value=400)
                st.markdown("""
                Componentes das saídas:
                - Saques de depósitos
                - Vencimento de dívidas
                - Chamadas de margem
                - Saques de linhas de crédito
                """)
            
            # Calcular LCR
            lcr = calculate_lcr(hqla, saidas_esperadas)
            
            # Calcular dias de cobertura
            dias_cobertura = hqla / (saidas_esperadas / 30)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if lcr >= 100:
                    st.success(f"Liquidity Coverage Ratio (LCR): {lcr:.1f}%")
                else:
                    st.error(f"Liquidity Coverage Ratio (LCR): {lcr:.1f}%")
                
                st.markdown("Requerimento Basileia III: LCR >= 100%")
            
            with col2:
                if dias_cobertura >= 30:
                    st.success(f"Dias de cobertura de liquidez: {dias_cobertura:.1f} dias")
                else:
                    st.error(f"Dias de cobertura de liquidez: {dias_cobertura:.1f} dias")
                
                st.markdown("Melhor prática: Mínimo de 30 dias de cobertura")
            
            st.markdown("""
            #### Importância do LCR:
            O Liquidity Coverage Ratio (LCR) foi introduzido pelo Comitê de Basileia após a crise financeira de 2008, 
            em parte como resposta a falhas como as do Northern Rock. Ele exige que os bancos mantenham um estoque 
            adequado de ativos líquidos de alta qualidade para sobreviver a um cenário de estresse de 30 dias.
            
            #### Northern Rock - O que deu errado:
            O Northern Rock mantinha um colchão de liquidez claramente insuficiente para seu modelo de negócios. 
            O banco não possuía HQLA suficientes para cobrir a potencial não renovação de seu funding de curto prazo.
            """)
        
        with tab3:
            st.markdown("### 🔄 Diversificação de Fontes de Financiamento")
            
            st.markdown("""
            A diversificação das fontes de financiamento visa reduzir a dependência de uma única fonte de funding, 
            minimizando o risco de uma interrupção severa no caso de problemas em um segmento específico do mercado.
            
            #### Objetivo:
            Criar um mix equilibrado de fontes de funding com diferentes características de estabilidade, custo e maturidade.
            """)
            
            # Gráfico de diversificação
            st.markdown("#### Ilustração de Diversificação de Funding")
            
            # Dados para o gráfico
            funding_tipos = [
                "Depósitos de Varejo", 
                "Depósitos Corporativos", 
                "Empréstimos Interbancários",
                "Emissões de Dívida", 
                "Securitização", 
                "Covered Bonds"
            ]
            
            # Banco diversificado vs Northern Rock
            diversificado = [35, 20, 15, 15, 10, 5]
            northern_rock = [23, 5, 15, 2, 45, 10]
            
            # Criar dataframe
            df_div = pd.DataFrame({
                'Fonte de Funding': funding_tipos,
                'Banco Diversificado (%)': diversificado,
                'Northern Rock (%)': northern_rock
            })
            
            # Gráfico de radar
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=diversificado,
                theta=funding_tipos,
                fill='toself',
                name='Banco Diversificado',
                line_color='rgba(16, 185, 129, 0.8)'
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=northern_rock,
                theta=funding_tipos,
                fill='toself',
                name='Northern Rock',
                line_color='rgba(220, 38, 38, 0.8)'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 50]
                    )
                ),
                title="Comparação da Diversificação de Funding",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                st.markdown("""
                #### Estratégias de Diversificação:
                
                1. **Diversificar tipos de instrumentos**
                   - Depósitos (varejo, corporativos)
                   - Dívida de curto e longo prazo
                   - Securitização (com limites prudentes)
                   - Covered bonds
                
                2. **Diversificar prazos de vencimento**
                   - Escalonar vencimentos
                   - Evitar concentração de vencimentos
                
                3. **Diversificar base de investidores**
                   - Diferentes segmentos de mercado
                   - Diferentes regiões geográficas
                """)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='warning-box'>", unsafe_allow_html=True)
                st.markdown("""
                #### Northern Rock - O que deu errado:
                
                Northern Rock apresentava diversas falhas na diversificação:
                
                1. **Concentração excessiva em securitização**
                   - 45% do funding vinha de notas securitizadas
                   - Apenas 23% de depósitos de varejo
                
                2. **Dependência do mercado atacadista**
                   - Mais de 75% do funding vinha de fontes não-varejo
                   - Vulnerabilidade a choques de liquidez no mercado
                
                3. **Modelo de crescimento insustentável**
                   - Crescimento de ativos muito mais rápido que a base de depósitos
                   - Aumento da dependência de mercados de capitais
                """)
                st.markdown("</div>", unsafe_allow_html=True)
        
        with tab4:
            st.markdown("### 🧪 Stress Testing de Liquidez")
            
            st.markdown("""
            Os testes de estresse de liquidez simulam cenários adversos para avaliar a capacidade do banco de 
            resistir a choques de liquidez e identificar vulnerabilidades em sua estrutura de funding.
            
            #### Objetivo:
            Avaliar a resiliência do banco sob diferentes cenários de estresse e garantir que tenha planos 
            de contingência adequados para cada situação.
            """)
            
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.markdown("""
            #### Tipos de Cenários de Estresse:
            
            1. **Específicos da instituição**
               - Downgrade de rating
               - Rumores sobre solvência
               - Perda de acesso a mercados específicos
            
            2. **Relacionados ao mercado**
               - Crise de liquidez sistêmica
               - Fechamento de mercados de capitais
               - Aumento de volatilidade e custos de funding
            
            3. **Combinados**
               - Cenários que combinam choque individual e de mercado
               - Geralmente os mais severos e realistas
            """)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Simulador de stress test
            st.markdown("#### Simulador de Stress Test")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Parâmetros do Banco")
                ativos_liquidos_stress = st.slider("Ativos Líquidos de Alta Qualidade (%)", 0, 100, 25)
                wholesale_funding_stress = st.slider("Proporção de Funding Wholesale (%)", 0, 100, 60)
            
            with col2:
                lcr_stress = calculate_lcr(ativos_liquidos_stress, wholesale_funding_stress * 0.3)
                nsfr_stress = calculate_nsfr((100 - wholesale_funding_stress) + (wholesale_funding_stress * 0.5), (100 - ativos_liquidos_stress))
                
                st.metric("Liquidity Coverage Ratio (LCR)", f"{lcr_stress:.1f}%")
                st.metric("Net Stable Funding Ratio (NSFR)", f"{nsfr_stress:.1f}%")
            
            if st.button("Executar Testes de Estresse"):
                stress_results = apply_stress_test(lcr_stress, nsfr_stress, ativos_liquidos_stress, wholesale_funding_stress)
                
                # Exibir resultados
                st.markdown("##### Resultados dos Testes de Estresse")
                
                for scenario, results in stress_results.items():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{scenario}**")
                    
                    with col2:
                        if results["survived"]:
                            st.markdown("✅ **APROVADO**")
                        else:
                            st.markdown("❌ **REPROVADO**")
                    
                    with col3:
                        st.markdown(f"LCR: {results['new_lcr']:.1f}%")
                    
                    # Detalhes do cenário
                    st.markdown(f"""
                    - Ativos líquidos restantes: {results['liquid_assets_remaining']:.1f}%
                    - NSFR após estresse: {results['new_nsfr']:.1f}%
                    """)
                    st.markdown("---")
                
                # Recomendações baseadas nos resultados
                failed_scenarios = sum(1 for r in stress_results.values() if not r["survived"])
                
                if failed_scenarios == 0:
                    st.success("O banco apresenta boa resiliência em todos os cenários de estresse.")
                elif failed_scenarios == 1:
                    st.warning("O banco apresenta vulnerabilidade em um cenário de estresse. Considere reforçar seu colchão de liquidez.")
                else:
                    st.error(f"O banco apresenta vulnerabilidades em {failed_scenarios} cenários de estresse. É necessário reformular sua estrutura de funding e aumentar significativamente seu colchão de liquidez.")
            
            st.markdown("""
            #### Implementação e Regulação:
            
            Os testes de estresse de liquidez tornaram-se obrigatórios sob Basileia III, como resposta direta à crise financeira de 2007-2008. 
            Os reguladores agora exigem que os bancos realizem testes de estresse regulares e mantenham planos de contingência para diferentes cenários.
            
            #### Northern Rock - O que deu errado:
            
            O Northern Rock não realizava testes de estresse abrangentes que cobrissem cenários extremos, como o fechamento completo 
            do mercado de securitização. O banco não estava preparado para um evento que de fato ocorreu - a paralisia do mercado 
            interbancário e de securitização que começou em agosto de 2007.
            """)
        
        with tab5:
            st.markdown("### 📝 Política de Contingência de Liquidez")
            
            st.markdown("""
            Um plano de contingência de liquidez estabelece antecipadamente as ações que serão tomadas em caso de crise, 
            permitindo uma resposta rápida e coordenada quando o tempo é essencial.
            
            #### Objetivo:
            Estabelecer um roteiro claro de ações para responder a uma crise de liquidez, minimizando o impacto e 
            evitando decisões precipitadas em momentos de estresse.
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                st.markdown("""
                #### Componentes essenciais de um plano de contingência:
                
                1. **Indicadores de alerta precoce**
                   - Gatilhos para ativar o plano
                   - Indicadores de mercado
                   - Métricas internas
                
                2. **Estrutura clara de governança**
                   - Comitê de crise
                   - Papéis e responsabilidades
                   - Processos de escalação
                
                3. **Opções de funding de emergência**
                   - Linhas de crédito comprometidas
                   - Ativos para venda/colateral
                   - Acesso a facilidades do banco central
                
                4. **Estratégias de comunicação**
                   - Comunicação com reguladores
                   - Comunicação com investidores
                   - Comunicação com o público
                """)
                st.markdown("</div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown("<div class='reference-box'>", unsafe_allow_html=True)
                st.markdown("""
                #### Níveis típicos de um plano de contingência:
                
                **Nível 1: Alerta Inicial**
                - Sinais de tensão no mercado
                - Monitoramento intensificado
                - Preparação de opções de funding
                
                **Nível 2: Tensão Elevada**
                - Deterioração significativa nas condições de funding
                - Ativação do comitê de crise
                - Implementação de medidas preventivas
                
                **Nível 3: Crise Severa**
                - Acesso ao mercado seriamente comprometido
                - Implementação completa do plano de emergência
                - Consideração de medidas extraordinárias
                
                **Nível 4: Sobrevivência**
                - Ações drásticas para preservar liquidez
                - Ativação de suporte do banco central
                - Foco em operações essenciais
                """)
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Fluxograma simples de contingência
            st.markdown("#### Fluxograma Simplificado de Contingência de Liquidez")
            
            # Dados para o fluxograma (usando um gráfico simples)
            nodes = [
                dict(name="Monitoramento", x=0, y=0.5),
                dict(name="Detecção\nde Alerta", x=1, y=0.5),
                dict(name="Avaliação\nda Situação", x=2, y=0.5),
                dict(name="Ativação do\nComitê de Crise", x=3, y=0.5),
                dict(name="Implementação\nde Medidas", x=4, y=0.5),
                dict(name="Resolução\nou Crise", x=5, y=0.5)
            ]
            
            edges = [
                dict(source=0, target=1),
                dict(source=1, target=2),
                dict(source=2, target=3),
                dict(source=3, target=4),
                dict(source=4, target=5),
                dict(source=5, target=0, line=dict(dash="dash"))
            ]
            
            # Criar o gráfico
            fig = go.Figure()
            
            # Adicionar nós
            for node in nodes:
                fig.add_trace(go.Scatter(
                    x=[node["x"]], 
                    y=[node["y"]],
                    mode="markers+text",
                    marker=dict(size=30, color="rgba(37, 99, 235, 0.8)"),
                    text=node["name"],
                    textposition="top center",
                    hoverinfo="text",
                    name=""
                ))
            
            # Adicionar arestas
            for edge in edges:
                source = nodes[edge["source"]]
                target = nodes[edge["target"]]
                
                line_props = edge.get("line", dict())
                default_line = dict(width=2, color="rgba(0, 0, 0, 0.5)")
                line = {**default_line, **line_props}
                
                fig.add_trace(go.Scatter(
                    x=[source["x"], target["x"]],
                    y=[source["y"], target["y"]],
                    mode="lines",
                    line=line,
                    hoverinfo="none",
                    showlegend=False
                ))
            
            fig.update_layout(
                title="Processo de Contingência de Liquidez",
                showlegend=False,
                xaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False
                ),
                height=250,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            
            st.markdown("""
            #### Testes e atualizações regulares:
            
            O plano de contingência de liquidez deve ser testado regularmente através de exercícios de simulação 
            e atualizado para refletir mudanças no ambiente de mercado e na estrutura do banco.
            
            #### Northern Rock - O que deu errado:
            
            O Northern Rock não possuía um plano de contingência adequado para lidar com o fechamento do mercado 
            de securitização. Quando a crise eclodiu, o banco não tinha opções viáveis além de buscar o apoio 
            emergencial do Banco da Inglaterra, o que acabou precipitando a corrida bancária.
            """)
    
    elif menu == "Stress Testing de Liquidez":
        st.markdown("## 🧪 Simulador de Stress Testing de Liquidez")
        
        st.markdown("""
        Este módulo permite simular diferentes cenários de estresse e avaliar o impacto no perfil de liquidez de um banco. 
        Configure os parâmetros do banco e escolha os cenários de estresse para avaliar sua resiliência.
        """)
        
        # Configuração do banco
        st.markdown("### Configuração do Banco")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ativos_liquidos_pct = st.slider("Ativos Líquidos (%)", 0, 100, 20)
            hqla = st.slider("Dos quais são HQLA (£ milhões)", 0, 10000, 3000)
        
        with col2:
            depositos_varejo = st.slider("Depósitos de Varejo (£ milhões)", 0, 50000, 15000)
            depositos_corporate = st.slider("Depósitos Corporativos (£ milhões)", 0, 30000, 5000)
        
        with col3:
            funding_curto = st.slider("Funding de Curto Prazo (£ milhões)", 0, 50000, 25000)
            funding_longo = st.slider("Funding de Longo Prazo (£ milhões)", 0, 50000, 15000)
        
        # Total de ativos e passivos
        total_passivos = depositos_varejo + depositos_corporate + funding_curto + funding_longo
        total_ativos = total_passivos  # Assumindo balanço equilibrado
        ativos_liquidos = total_ativos * (ativos_liquidos_pct / 100)
        ativos_iliquidos = total_ativos - ativos_liquidos
        
        # Cálculo de métricas-chave
        lcr_pre = (hqla / (funding_curto * 0.5 + depositos_varejo * 0.1 + depositos_corporate * 0.2)) * 100
        nsfr_pre = ((depositos_varejo * 0.9 + depositos_corporate * 0.5 + funding_longo * 0.8) / (ativos_iliquidos * 0.85 + ativos_liquidos * 0.15)) * 100
        
        # Exibir resumo do banco
        st.markdown("### Resumo do Perfil de Liquidez")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Ativos", f"£{total_ativos/1000:.1f} bilhões")
            st.metric("Ativos Líquidos", f"£{ativos_liquidos/1000:.1f} bilhões")
            st.metric("% de Ativos Líquidos", f"{ativos_liquidos_pct:.1f}%")
        
        with col2:
            st.metric("Depósitos Totais", f"£{(depositos_varejo + depositos_corporate)/1000:.1f} bilhões")
            st.metric("% de Funding de Varejo", f"{depositos_varejo/total_passivos*100:.1f}%")
            st.metric("% de Funding de Curto Prazo", f"{funding_curto/total_passivos*100:.1f}%")
        
        with col3:
            st.metric("Liquidity Coverage Ratio", f"{lcr_pre:.1f}%")
            st.metric("Net Stable Funding Ratio", f"{nsfr_pre:.1f}%")
            
            # Avaliar vulnerabilidade
            if funding_curto/total_passivos > 0.4 and ativos_liquidos_pct < 25:
                st.markdown("<span class='risk-high'>ALTA VULNERABILIDADE</span>", unsafe_allow_html=True)
            elif funding_curto/total_passivos > 0.3 or ativos_liquidos_pct < 20:
                st.markdown("<span class='risk-medium'>MÉDIA VULNERABILIDADE</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span class='risk-low'>BAIXA VULNERABILIDADE</span>", unsafe_allow_html=True)
        
        # Definição de cenários de estresse
        st.markdown("### Escolha de Cenários de Estresse")
        
        cenarios = {
            "Crise de Liquidez Moderada": {
                "descricao": "Tensão nos mercados de funding de curto prazo com algum impacto nos depósitos",
                "saida_varejo": 10,  # % de saída
                "saida_corporate": 20,
                "renovacao_curto": 50,  # % de não renovação
                "impacto_hqla": 5,  # % de haircut
                "duracao": 30  # dias
            },
            "Corrida Bancária": {
                "descricao": "Saída intensa de depósitos de varejo e corporativos com perda de confiança na instituição",
                "saida_varejo": 30,
                "saida_corporate": 40,
                "renovacao_curto": 80,
                "impacto_hqla": 10,
                "duracao": 14
            },
            "Crise Sistêmica": {
                "descricao": "Fechamento dos mercados de funding, corrida bancária e desvalorização de ativos",
                "saida_varejo": 20,
                "saida_corporate": 50,
                "renovacao_curto": 90,
                "impacto_hqla": 15,
                "duracao": 60
            },
            "Cenário Northern Rock (2007)": {
                "descricao": "Fechamento do mercado de securitização, seguido de corrida bancária",
                "saida_varejo": 25,
                "saida_corporate": 35,
                "renovacao_curto": 95,
                "impacto_hqla": 5,
                "duracao": 30
            }
        }
        
        selected_cenarios = st.multiselect(
            "Selecione os cenários de estresse a simular:",
            list(cenarios.keys()),
            default=["Crise de Liquidez Moderada", "Cenário Northern Rock (2007)"]
        )
        
        if st.button("Executar Simulação de Estresse"):
            if not selected_cenarios:
                st.warning("Por favor, selecione pelo menos um cenário de estresse.")
            else:
                # Resultados da simulação
                st.markdown("### Resultados da Simulação")
                
                for cenario_nome in selected_cenarios:
                    cenario = cenarios[cenario_nome]
                    
                    st.markdown(f"#### {cenario_nome}")
                    st.markdown(f"*{cenario['descricao']}*")
                    
                    # Calcular impactos
                    saida_dep_varejo = depositos_varejo * (cenario["saida_varejo"] / 100)
                    saida_dep_corp = depositos_corporate * (cenario["saida_corporate"] / 100)
                    nao_renovacao_curto = funding_curto * (cenario["renovacao_curto"] / 100)
                    
                    total_saidas = saida_dep_varejo + saida_dep_corp + nao_renovacao_curto
                    hqla_ajustado = hqla * (1 - cenario["impacto_hqla"] / 100)
                    
                    # Verificar sobrevivência
                    sobrevive = hqla_ajustado >= total_saidas
                    dias_sobrevivencia = min(cenario["duracao"], (hqla_ajustado / total_saidas) * cenario["duracao"])
                    
                    # Métricas pós-estresse
                    lcr_pos = ((hqla_ajustado - total_saidas) / ((funding_curto - nao_renovacao_curto) * 0.5 + 
                                                              (depositos_varejo - saida_dep_varejo) * 0.1 + 
                                                              (depositos_corporate - saida_dep_corp) * 0.2)) * 100 if not sobrevive else 0
                    
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"""
                        - Saída de depósitos de varejo: £{saida_dep_varejo/1000:.2f} bilhões ({cenario["saida_varejo"]}%)
                        - Saída de depósitos corporativos: £{saida_dep_corp/1000:.2f} bilhões ({cenario["saida_corporate"]}%)
                        - Não renovação de funding de curto prazo: £{nao_renovacao_curto/1000:.2f} bilhões ({cenario["renovacao_curto"]}%)
                        - **Total de saídas de caixa: £{total_saidas/1000:.2f} bilhões**
                        - HQLA disponível (após haircuts): £{hqla_ajustado/1000:.2f} bilhões
                        """)
                    
                    with col2:
                        if sobrevive:
                            st.markdown(f"### ✅ SOBREVIVE")
                        else:
                            st.markdown(f"### ❌ FALHA")
                            st.markdown(f"**Dias até falha: {dias_sobrevivencia:.1f}**")
                    
                    # Gráfico de evolução da liquidez durante o estresse
                    dias = list(range(cenario["duracao"] + 1))
                    liquidez_diaria = []
                    
                    liquidez_atual = hqla_ajustado
                    saida_diaria = total_saidas / cenario["duracao"]
                    
                    for _ in dias:
                        liquidez_diaria.append(max(0, liquidez_atual))
                        liquidez_atual -= saida_diaria
                    
                    # Criar dataframe
                    df_evolucao = pd.DataFrame({
                        'Dia': dias,
                        'Liquidez Disponível': liquidez_diaria
                    })
                    
                    # Gráfico
                    fig = px.line(
                        df_evolucao,
                        x='Dia',
                        y='Liquidez Disponível',
                        title=f'Evolução da Liquidez - {cenario_nome}',
                        labels={'Liquidez Disponível': 'Milhões £'}
                    )
                    
                    # Adicionar linha de falha se aplicável
                    if not sobrevive:
                        fig.add_shape(
                            type="line",
                            x0=dias_sobrevivencia,
                            y0=0,
                            x1=dias_sobrevivencia,
                            y1=hqla_ajustado,
                            line=dict(
                                color="Red",
                                width=3,
                                dash="dash",
                            )
                        )
                        
                        fig.add_annotation(
                            x=dias_sobrevivencia,
                            y=hqla_ajustado / 2,
                            text=f"Falha no dia {dias_sobrevivencia:.1f}",
                            showarrow=True,
                            arrowhead=1,
                        )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
                
                # Recomendações baseadas nos resultados
                st.markdown("### Recomendações")
                
                failed_scenarios = sum(1 for sc in selected_cenarios if not cenarios[sc]["saida_varejo"] * depositos_varejo / 100 + 
                                       cenarios[sc]["saida_corporate"] * depositos_corporate / 100 + 
                                       cenarios[sc]["renovacao_curto"] * funding_curto / 100 <= 
                                       hqla * (1 - cenarios[sc]["impacto_hqla"] / 100))
                
                if failed_scenarios == 0:
                    st.success("""
                    ✅ O banco demonstra boa resiliência em todos os cenários testados. Recomendações:
                    
                    1. Manter o atual colchão de liquidez e mix de funding
                    2. Continuar monitorando os mercados para sinais de alerta precoce
                    3. Realizar testes de estresse com cenários ainda mais severos para identificar limites
                    """)
                elif failed_scenarios < len(selected_cenarios):
                    st.warning(f"""
                    ⚠️ O banco falha em {failed_scenarios} dos {len(selected_cenarios)} cenários testados. Recomendações:
                    
                    1. Aumentar o colchão de HQLA em pelo menos 20%
                    2. Reduzir gradualmente a dependência de funding de curto prazo
                    3. Diversificar as fontes de funding para reduzir concentrações
                    4. Revisar e fortalecer o plano de contingência de liquidez
                    """)
                else:
                    st.error(f"""
                    ❌ O banco falha em todos os {len(selected_cenarios)} cenários testados. Recomendações urgentes:
                    
                    1. Reestruturar imediatamente o perfil de liquidez:
                       - Aumentar HQLA em pelo menos 50%
                       - Reduzir significativamente a dependência de funding de curto prazo
                       - Aumentar a captação de depósitos estáveis de varejo
                    
                    2. Desenvolver plano de contingência robusto com acesso a linhas de crédito comprometidas
                    
                    3. Considerar redução do ritmo de crescimento para alinhar com fontes de funding sustentáveis
                    
                    4. Implementar monitoramento diário de indicadores de liquidez com alertas precoces
                    """)
    
    elif menu == "Sobre o Aplicativo":
        st.markdown("## ℹ️ Sobre este Aplicativo")
        
        st.markdown("""
        ### Objetivo Pedagógico
        
        Este aplicativo foi desenvolvido com finalidade educacional, para ilustrar os conceitos de risco de liquidez
        bancária utilizando o caso histórico do Northern Rock como exemplo. O objetivo é proporcionar uma compreensão
        prática dos mecanismos que levam a crises de liquidez e das estratégias para mitigá-las.
        
        ### Funcionalidades
        
        - **Contextualização histórica** do caso Northern Rock
        - **Simulador de balanço e risco** que permite experimentar diferentes configurações
        - **Simulador de stress testing** para avaliar a resistência a cenários adversos
        - **Explicações detalhadas** sobre técnicas de gestão de risco de liquidez
        
        ### Referências
        
        Este aplicativo é baseado em fontes acadêmicas e regulatórias, incluindo:
        
        - Shin, H. S. (2009). Reflections on Northern Rock: The Bank Run that Heralded the Global Financial Crisis. Journal of Economic Perspectives, 23(1), 101-119.
        - Basel Committee on Banking Supervision. (2013). Basel III: The Liquidity Coverage Ratio and liquidity risk monitoring tools.
        - Basel Committee on Banking Supervision. (2014). Basel III: The Net Stable Funding Ratio.
        - Bank of England. (2007-2008). Financial Stability Reports.
        
        ### Limitações
        
        Este simulador é uma simplificação da realidade bancária e não deve ser utilizado para decisões reais de gestão
        de risco. Os modelos apresentados são ilustrativos e objetivam o entendimento conceitual, não a precisão absoluta.
        """)
        
        st.markdown("<div class='reference-box'>", unsafe_allow_html=True)
        st.markdown("""
        ### Lições da Crise Financeira Global
        
        A quebra do Northern Rock foi apenas o primeiro episódio de uma crise financeira global muito mais ampla.
        Entre as principais lições aprendidas estão:
        
        1. A importância de uma regulação bancária que considere o risco de liquidez, não apenas o risco de crédito
        
        2. A necessidade de limites para descasamentos excessivos de prazos entre ativos e passivos
        
        3. Os perigos de modelos de crescimento acelerado baseados em funding de mercado
        
        4. A facilidade com que crises de confiança podem se espalhar no sistema financeiro
        
        5. O papel crucial de colchões de liquidez adequados e planos de contingência robustos
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
# Executar o aplicativo
if __name__ == "__main__":
    main()
    
# Footer
st.divider()
st.markdown("<p style='text-align: center; color: #777; font-size: 0.8em;'>© 2025 Estudos de Caso sobre Gestão de Risco de Liquidez | Desenvolvido com finalidade pedagógica</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #777; font-size: 0.8em;'>Prof. José Américo – Coppead</p>", unsafe_allow_html=True)