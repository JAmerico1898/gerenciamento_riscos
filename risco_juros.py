import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="Risco de Taxas de Juros - SVB",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2563EB;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .section {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #F8FAFC;
        margin-bottom: 1rem;
    }
    .highlight {
        background-color: #DBEAFE;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #3B82F6;
    }
    .warning {
        background-color: #FEF2F2;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #EF4444;
    }
    .info {
        background-color: #ECFDF5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #10B981;
    }
</style>
""", unsafe_allow_html=True)

# Função para criar a barra lateral
def create_sidebar():
    st.sidebar.markdown("## Navegação")
    page = st.sidebar.radio(
        "Selecione uma seção:",
        [
            "📝 Introdução",
            "🏦 SVB: O Caso de Estudo",
            "📊 Gap de Reprecificação",
            "⏱️ Duration & DV01/PVBP",
            "🔥 Stress Testing",
            "⚖️ Gestão Ativo-Passivo (ALM)",
            "📚 Referências"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Sobre")
    st.sidebar.info(
        "Este aplicativo foi desenvolvido com finalidade pedagógica para ilustrar "
        "o Risco de Taxas de Juros em instituições bancárias, utilizando o caso "
        "do Silicon Valley Bank (SVB) como exemplo prático."
    )
    
    return page

# Função para a página de introdução
def intro_page():
    st.markdown('<div class="main-header">Risco de Taxas de Juros em Instituições Bancárias</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(
            """
            <div class="section">
            <p>O Risco de Taxas de Juros é um risco fundamental para instituições financeiras, especialmente bancos. 
            Ele surge da possibilidade de variações nas taxas de juros afetarem negativamente o valor dos ativos e passivos, 
            e, consequentemente, o patrimônio da instituição.</p>
            
            <p>Este aplicativo explora as principais dimensões do Risco de Taxas de Juros utilizando o colapso do 
            Silicon Valley Bank (SVB) em 2023 como caso de estudo. A quebra do SVB representa um exemplo clássico 
            de como o descasamento entre ativos e passivos pode gerar vulnerabilidades significativas quando as 
            taxas de juros mudam abruptamente.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="sub-header">Por que o Risco de Taxas de Juros é importante?</div>
            <div class="section">
            <p>O Risco de Taxas de Juros é um dos principais riscos enfrentados por instituições financeiras por diversas razões:</p>
            <ul>
                <li><strong>Impacto Patrimonial:</strong> Variações nas taxas podem gerar perdas significativas no valor de mercado dos ativos, reduzindo o patrimônio do banco.</li>
                <li><strong>Efeito na Margem Financeira:</strong> Mudanças nas taxas afetam a margem financeira do banco, impactando diretamente sua rentabilidade.</li>
                <li><strong>Risco Sistêmico:</strong> Como visto no caso do SVB, o risco de taxas de juros mal gerenciado pode desencadear crises de confiança e contágio no sistema financeiro.</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="info">
            <h3>Conceitos Fundamentais</h3>
            <p><strong>Custo Amortizado:</strong> Método contábil onde o valor do ativo é registrado com base no custo de aquisição, acrescido ou reduzido da amortização acumulada.</p>
            <p><strong>Marcação a Mercado:</strong> Valorização dos ativos pelo seu valor atual de mercado, refletindo as variações das taxas de juros.</p>
            <p><strong>Duration:</strong> Medida da sensibilidade do preço de um título a variações nas taxas de juros.</p>
            <p><strong>Gap de Reprecificação:</strong> Diferença entre ativos e passivos sensíveis a taxas de juros em diferentes intervalos de tempo.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="sub-header">Técnicas de Gestão do Risco de Taxas de Juros</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div class="highlight">
            <h3>Gap de Reprecificação</h3>
            <p>Avalia a diferença entre ativos e passivos sensíveis à taxa de juros em diferentes intervalos de tempo.
            Permite estimar o impacto de variações de juros sobre o resultado financeiro.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="highlight">
            <h3>Stress Testing</h3>
            <p>Simulações de cenários extremos (ex: choque abrupto de +200 bps) para avaliar a resiliência da carteira
            em situações adversas de mercado.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="highlight">
            <h3>Análise de Sensibilidade</h3>
            <p><strong>Duration:</strong> Mede a sensibilidade do valor presente de um ativo ou passivo a alterações nas taxas de juros.</p>
            <p><strong>DV01/PVBP:</strong> Estima a variação no valor de mercado de uma posição para uma variação de 1 bp na curva de juros.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown(
            """
            <div class="highlight">
            <h3>Gestão Ativo-Passivo (ALM)</h3>
            <p>Gestão integrada de ativos e passivos visando equilíbrio entre rentabilidade e risco, 
            levando em conta vencimentos, durations e reprecificações.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown(
        """
        <div class="warning">
        <h3>O Caso Silicon Valley Bank (2023)</h3>
        <p>O colapso do Silicon Valley Bank em março de 2023 representa um exemplo dramático de materialização do Risco de Taxas de Juros.
        Durante o período de baixas taxas de juros, o banco investiu pesadamente em títulos de longo prazo, financiados com depósitos de curto prazo.
        Quando o Federal Reserve elevou rapidamente as taxas para combater a inflação, o valor de mercado desses títulos despencou, criando uma
        discrepância significativa entre o valor contábil (custo amortizado) e o valor de mercado dos ativos.</p>
        <p>A necessidade de vender esses ativos para atender a saques de depositantes forçou o banco a realizar perdas consideráveis,
        levando à sua insolvência.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Função para a página do caso SVB
def svb_case_page():
    st.markdown('<div class="main-header">Silicon Valley Bank: Anatomia de uma Quebra por Risco de Taxas de Juros</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="section">
        <p>O Silicon Valley Bank (SVB) era o 16º maior banco dos Estados Unidos, com foco principal em startups e empresas de tecnologia.
        Sua quebra em março de 2023 foi uma das maiores falências bancárias desde a crise financeira de 2008 e um exemplo clássico de
        materialização do risco de taxas de juros.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sub-header">Modelo de Negócios do SVB</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(
            """
            <div class="section">
            <h3>Características do Modelo de Negócios</h3>
            <ul>
                <li><strong>Base de clientes especializada:</strong> Foco em startups de tecnologia e venture capital.</li>
                <li><strong>Depósitos voláteis:</strong> Grande volume de depósitos corporativos acima do limite de garantia do FDIC.</li>
                <li><strong>Estratégia de investimento:</strong> Aplicação de depósitos em títulos de longo prazo (principalmente MBS e títulos do governo).</li>
                <li><strong>Baixa diversificação:</strong> Alta concentração em um setor econômico específico.</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        # Dados para o gráfico de composição de ativos do SVB
        labels = ['Títulos de longo prazo', 'Empréstimos', 'Caixa e equivalentes', 'Outros ativos']
        values = [55, 31, 8, 6]  # Percentuais aproximados baseados no caso
        
        fig = px.pie(
            names=labels, 
            values=values, 
            title="Composição de Ativos do SVB (Dez/2022)",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<div class="sub-header">A Armadilha do Risco de Taxas de Juros</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Dados para o gráfico de taxas de juros
        years = [2020, 2021, 2022, 2023]
        rates = [0.25, 0.25, 4.5, 5.5]
        
        fig = px.line(
            x=years, 
            y=rates, 
            markers=True,
            title="Taxa Básica de Juros dos EUA (Fed Funds Rate)",
            labels={"x": "Ano", "y": "Taxa (%)"},
            color_discrete_sequence=['#1E40AF']
        )
        fig.add_shape(
            type="rect",
            x0=2022, y0=4.0,
            x1=2023, y1=5.5,
            line=dict(color="rgba(255, 0, 0, 0.5)"),
            fillcolor="rgba(255, 0, 0, 0.2)",
            layer="below"
        )
        fig.add_annotation(
            x=2022.5, y=4.75,
            text="Período Crítico",
            showarrow=False,
            font=dict(color="red")
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(
            """
            <div class="warning">
            <h3>A Sequência de Eventos</h3>
            <ol>
                <li><strong>2020-2021:</strong> Período de juros próximos de zero e grande liquidez no mercado.</li>
                <li><strong>2021-2022:</strong> SVB recebe grande volume de depósitos e investe em títulos de longo prazo.</li>
                <li><strong>2022-2023:</strong> Federal Reserve aumenta rapidamente as taxas para combater a inflação.</li>
                <li><strong>Março/2023:</strong> O valor de mercado dos títulos cai drasticamente.</li>
                <li><strong>8-9/Mar/2023:</strong> SVB anuncia perdas de $1,8 bilhão na venda de títulos para honrar saques em depósitos e tenta levantar capital.</li>
                <li><strong>10/Mar/2023:</strong> Corrida bancária e intervenção regulatória levam ao colapso do banco.</li>
            </ol>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown('<div class="sub-header">Números que Contam a História</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="highlight" style="text-align: center;">
            <h2>$117B</h2>
            <p>Volume de títulos de longo prazo no balanço do SVB (55% dos ativos)</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="highlight" style="text-align: center;">
            <h2>5,7 anos</h2>
            <p>Duration média dos títulos do SVB</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div class="highlight" style="text-align: center;">
            <h2>$15,2B</h2>
            <p>Perdas não realizadas (95% do patrimônio)</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown(
        """
        <div class="section">
        <p>O caso do SVB ilustra perfeitamente o conceito de "Gap de Duration". O banco tinha ativos de longo prazo (duration de aproximadamente 5,7 anos) 
        financiados principalmente por depósitos de curto prazo (duration próxima de zero). Este descasamento criou uma exposição de 3 a 4 anos em termos de duration gap.</p>
        
        <p>Segundo Lucas e Golding (2023), com este gap de duration, um aumento de 1 ponto percentual nas taxas de juros causaria uma perda de valor de mercado 
        de aproximadamente $6-8 bilhões (cerca de metade do patrimônio do banco). Um aumento de 2 pontos percentuais, como ocorreu, levaria o banco à beira da insolvência.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sub-header">Lições do Caso SVB</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="info">
        <ul>
            <li><strong>Importância da transparência:</strong> O artigo de Lucas e Golding propõe que bancos divulguem regularmente seu gap de duration, 
            similar ao que as GSEs (Fannie Mae e Freddie Mac) passaram a fazer após crises anteriores.</li>
            <li><strong>Falhas regulatórias:</strong> Apesar da alta regulação bancária, existem poucas regras específicas para mensurar e controlar 
            o risco de taxas de juros.</li>
            <li><strong>Efeitos da contabilidade:</strong> O método de "Hold to Maturity" permitiu que o SVB não reconhecesse as perdas de mercado em seu balanço, 
            mascarando os riscos até que fosse necessário vender os títulos.</li>
            <li><strong>Concentração de riscos:</strong> A combinação de risco de taxa de juros com concentração setorial e depósitos não segurados 
            amplificou a vulnerabilidade do banco.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# Função para a página de Gap de Reprecificação
def repricing_gap_page():
    st.markdown('<div class="main-header">Gap de Reprecificação (Repricing Gap Analysis)</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="section">
        <p>O Gap de Reprecificação é uma técnica fundamental para a gestão do risco de taxas de juros. Ela avalia a diferença entre
        ativos e passivos sensíveis à taxa de juros em diferentes intervalos de tempo, permitindo estimar o impacto de variações 
        nas taxas sobre o resultado financeiro da instituição.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sub-header">Conceito e Aplicação</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(
            """
            <div class="section">
            <h3>Como Funciona o Gap de Reprecificação</h3>
            <p>O método consiste em classificar ativos e passivos em faixas temporais de acordo com seus prazos de reprecificação.
            Para cada faixa, calcula-se a diferença entre o volume de ativos e passivos sensíveis a juros:</p>
            
            <p style="text-align: center;"><strong>Gap = Ativos Sensíveis a Juros - Passivos Sensíveis a Juros</strong></p>
            
            <p>O impacto de uma variação nas taxas de juros na margem financeira pode ser estimado através da fórmula:</p>
            
            <p style="text-align: center;"><strong>Δ Margem Financeira = Gap × Δ Taxa de Juros</strong></p>
            
            <p>Principais características:</p>
            <ul>
                <li><strong>Gap Positivo:</strong> Mais ativos que passivos sendo reprecificados no período. 
                Um aumento nas taxas beneficia a margem financeira.</li>
                <li><strong>Gap Negativo:</strong> Mais passivos que ativos sendo reprecificados no período. 
                Um aumento nas taxas prejudica a margem financeira.</li>
                <li><strong>Gap Nulo:</strong> Volumes iguais de ativos e passivos sendo reprecificados. 
                A margem financeira é imune a variações de taxas.</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="info">
            <h3>Exemplo Simplificado</h3>
            
            <p>Considere um banco com os seguintes valores em cada faixa temporal:</p>
            
            <p><strong>0-3 meses:</strong></p>
            <ul>
                <li>Ativos: R$ 200 milhões</li>
                <li>Passivos: R$ 300 milhões</li>
                <li>Gap: -R$ 100 milhões</li>
            </ul>
            
            <p><strong>3-6 meses:</strong></p>
            <ul>
                <li>Ativos: R$ 150 milhões</li>
                <li>Passivos: R$ 100 milhões</li>
                <li>Gap: +R$ 50 milhões</li>
            </ul>
            
            <p>Se as taxas subirem 1%, o impacto na margem financeira seria:</p>
            <ul>
                <li>0-3 meses: -R$ 1 milhão</li>
                <li>3-6 meses: +R$ 0,5 milhão</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown('<div class="sub-header">Simulação: Gap de Reprecificação</div>', unsafe_allow_html=True)
    
    # Criando a simulação interativa
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<h3>Insira os valores dos ativos e passivos em cada faixa temporal:</h3>", unsafe_allow_html=True)
        
        # Inputs para ativos
        st.markdown("<p><strong>Ativos:</strong></p>", unsafe_allow_html=True)
        ativos_0_3 = st.number_input("Ativos 0-3 meses (milhões R$)", min_value=0.0, value=200.0, step=10.0)
        ativos_3_6 = st.number_input("Ativos 3-6 meses (milhões R$)", min_value=0.0, value=150.0, step=10.0)
        ativos_6_12 = st.number_input("Ativos 6-12 meses (milhões R$)", min_value=0.0, value=100.0, step=10.0)
        ativos_12_24 = st.number_input("Ativos 1-2 anos (milhões R$)", min_value=0.0, value=300.0, step=10.0)
        
        # Inputs para passivos
        st.markdown("<p><strong>Passivos:</strong></p>", unsafe_allow_html=True)
        passivos_0_3 = st.number_input("Passivos 0-3 meses (milhões R$)", min_value=0.0, value=300.0, step=10.0)
        passivos_3_6 = st.number_input("Passivos 3-6 meses (milhões R$)", min_value=0.0, value=100.0, step=10.0)
        passivos_6_12 = st.number_input("Passivos 6-12 meses (milhões R$)", min_value=0.0, value=200.0, step=10.0)
        passivos_12_24 = st.number_input("Passivos 1-2 anos (milhões R$)", min_value=0.0, value=150.0, step=10.0)
        
        # Input para variação da taxa de juros
        delta_juros = st.slider("Variação na Taxa de Juros (%)", min_value=-5.0, max_value=5.0, value=1.0, step=0.25)
    
    with col2:
        # Calculando os gaps
        gaps = {
            "0-3 meses": ativos_0_3 - passivos_0_3,
            "3-6 meses": ativos_3_6 - passivos_3_6,
            "6-12 meses": ativos_6_12 - passivos_6_12,
            "1-2 anos": ativos_12_24 - passivos_12_24
        }
        
        # Calculando impactos na margem financeira
        impactos = {k: v * delta_juros / 100 for k, v in gaps.items()}
        
        # Preparando dados para o DataFrame
        data = {
            "Faixa": list(gaps.keys()),
            "Ativos (M R$)": [ativos_0_3, ativos_3_6, ativos_6_12, ativos_12_24],
            "Passivos (M R$)": [passivos_0_3, passivos_3_6, passivos_6_12, passivos_12_24],
            "Gap (M R$)": list(gaps.values()),
            f"Impacto de {delta_juros}% (M R$)": list(impactos.values())
        }
        
        df = pd.DataFrame(data)
        
        # Adicionando linha de totais
        totals = pd.DataFrame({
            "Faixa": ["Total"],
            "Ativos (M R$)": [sum(data["Ativos (M R$)"])],
            "Passivos (M R$)": [sum(data["Passivos (M R$)"])],
            "Gap (M R$)": [sum(data["Gap (M R$)"])],
            f"Impacto de {delta_juros}% (M R$)": [sum(data[f"Impacto de {delta_juros}% (M R$)"])]
        })
        
        df = pd.concat([df, totals], ignore_index=True)
        
        # Exibindo a tabela
        st.markdown("<h3>Análise de Gap de Reprecificação:</h3>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, height=250)  # Define uma altura fixa de 250 pixels
        
        # Criando o gráfico de barras
        fig = go.Figure()
        
        # Adicionando barras para ativos
        fig.add_trace(go.Bar(
            x=data["Faixa"],
            y=data["Ativos (M R$)"],
            name="Ativos",
            marker_color="#3B82F6"
        ))
        
        # Adicionando barras para passivos
        fig.add_trace(go.Bar(
            x=data["Faixa"],
            y=data["Passivos (M R$)"],
            name="Passivos",
            marker_color="#EF4444"
        ))
        
        # Adicionando linha para o gap
        fig.add_trace(go.Scatter(
            x=data["Faixa"],
            y=data["Gap (M R$)"],
            name="Gap",
            mode="lines+markers",
            line=dict(color="#10B981", width=3),
            marker=dict(size=10)
        ))
        
        # Configurando o layout
        fig.update_layout(
            title="Ativos, Passivos e Gap por Faixa Temporal",
            xaxis_title="Faixa Temporal",
            yaxis_title="Valor (milhões R$)",
            barmode="group",
            template="plotly_white"
        )
        
        # Exibindo o gráfico
        st.plotly_chart(fig, use_container_width=True)
        
        # Criando gráfico de impacto
        fig_impacto = go.Figure()
        
        # Cores baseadas no valor do impacto (positivo/negativo)
        colors = ["#EF4444" if imp < 0 else "#10B981" for imp in data[f"Impacto de {delta_juros}% (M R$)"]]
        
        fig_impacto.add_trace(go.Bar(
            x=data["Faixa"],
            y=data[f"Impacto de {delta_juros}% (M R$)"],
            name=f"Impacto de {delta_juros}%",
            marker_color=colors
        ))
        
        # Configurando o layout
        fig_impacto.update_layout(
            title=f"Impacto na Margem Financeira de uma variação de {delta_juros}% nas taxas",
            xaxis_title="Faixa Temporal",
            yaxis_title="Impacto na Margem (milhões R$)",
            template="plotly_white"
        )
        
        # Adicionando linha de zero
        fig_impacto.add_shape(
            type="line",
            x0=-0.5,
            y0=0,
            x1=3.5,
            y1=0,
            line=dict(color="black", width=1, dash="dot")
        )
        
        # Exibindo o gráfico
        st.plotly_chart(fig_impacto, use_container_width=True)
    
    # Análise dos resultados
    st.markdown('<div class="sub-header">Análise e Interpretação</div>', unsafe_allow_html=True)
    
    total_gap = sum(gaps.values())
    total_impacto = sum(impactos.values())
    
    if total_gap > 0:
        gap_type = "positivo"
        if delta_juros > 0:
            effect = "beneficiado"
        else:
            effect = "prejudicado"
    elif total_gap < 0:
        gap_type = "negativo"
        if delta_juros > 0:
            effect = "prejudicado"
        else:
            effect = "beneficiado"
    else:
        gap_type = "neutro"
        effect = "neutro"
    
    if abs(total_impacto) < 1:
        impact_level = "baixo"
    elif abs(total_impacto) < 10:
        impact_level = "moderado"
    else:
            impact_level = "significativo"
    
    st.markdown(
        f"""
        <div class="section">
        <p>De acordo com a análise realizada, o banco apresenta um <strong>gap {gap_type}</strong> no total das faixas temporais, 
        totalizando <strong>R$ {total_gap:.2f} milhões</strong>.</p>
        
        <p>Com uma variação de <strong>{delta_juros:.2f}%</strong> nas taxas de juros, o impacto esperado na margem financeira 
        seria de <strong>R$ {total_impacto:.2f} milhões</strong>, o que representa um impacto <strong>{impact_level}</strong>.</p>
        
        <p>Isso significa que, neste cenário, o banco seria <strong>{effect}</strong> por esta variação nas taxas de juros.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="info">
        <h3>Aplicação ao Caso SVB</h3>
        <p>No caso do Silicon Valley Bank, a instituição tinha um gap de reprecificação fortemente negativo nas faixas de curto prazo
        e positivo nas faixas de longo prazo, devido à grande concentração de títulos de longo prazo (55% dos ativos) financiados por
        depósitos de curto prazo.</p>
        
        <p>Quando as taxas de juros subiram rapidamente em 2022-2023, o banco foi severamente impactado tanto em termos de valor 
        de mercado de seus ativos quanto em sua margem financeira, contribuindo para sua insolvência.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="warning">
        <h3>Limitações da Análise de Gap de Reprecificação</h3>
        <ul>
            <li><strong>Foco na margem:</strong> Esta análise foca no impacto na margem financeira, não no valor econômico do patrimônio.</li>
            <li><strong>Linearidade:</strong> Assume uma relação linear entre variações de taxas e margens, o que nem sempre é verdade.</li>
            <li><strong>Opções embutidas:</strong> Não considera adequadamente opções embutidas, como pré-pagamentos em hipotecas.</li>
            <li><strong>Compensação entre prazos:</strong> Um gap positivo em uma faixa pode compensar um gap negativo em outra, 
            mas os impactos não são necessariamente simultâneos.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# Função para a página de Duration & DV01/PVBP
def duration_page():
    st.markdown('<div class="main-header">Análise de Sensibilidade: Duration e DV01/PVBP</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="section">
        <p>A Análise de Sensibilidade é um conjunto de técnicas que permitem mensurar o impacto de variações nas taxas de juros
        sobre o valor de mercado de ativos, passivos e, consequentemente, o patrimônio da instituição financeira.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    tab1, tab2 = st.tabs(["Duration", "DV01/PVBP"])
    
    with tab1:
        st.markdown('<div class="sub-header">Duration: Conceito e Aplicação</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown(
                """
                <div class="section">
                <h3>O que é Duration?</h3>
                <p>A Duration é uma medida da sensibilidade do valor de mercado de um título ou carteira a variações nas taxas de juros.
                Ela representa o tempo médio ponderado até o recebimento dos fluxos de caixa de um título, considerando tanto os pagamentos
                de juros quanto o principal.</p>
                
                <p>Existem diferentes tipos de duration:</p>
                <ul>
                    <li><strong>Duration de Macaulay:</strong> Média ponderada dos tempos até cada fluxo de caixa, ponderados pelo valor presente dos fluxos.</li>
                    <li><strong>Duration Modificada:</strong> Ajuste da Duration de Macaulay para refletir diretamente a sensibilidade do preço. É calculada dividindo
                    a Duration de Macaulay por (1 + taxa de juros).</li>
                    <li><strong>Duration Efetiva:</strong> Considera opções embutidas nos títulos, como pré-pagamentos em hipotecas.</li>
                </ul>
                
                <p>A fórmula simplificada para calcular a variação no valor de um título com base na duration é:</p>
                
                <p style="text-align: center;"><strong>ΔP/P ≈ -Duration × Δr</strong></p>
                
                <p>Onde:</p>
                <ul>
                    <li>ΔP/P é a variação percentual no preço do título</li>
                    <li>Duration é a duration modificada do título</li>
                    <li>Δr é a variação na taxa de juros (em termos decimais)</li>
                </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                """
                <div class="info">
                <h3>Interpretação da Duration</h3>
                
                <p><strong>Duration = 3 anos</strong> significa que:</p>
                <ul>
                    <li>Um aumento de 1% na taxa de juros causará uma queda aproximada de 3% no valor do título.</li>
                    <li>Uma redução de 1% na taxa de juros causará um aumento aproximado de 3% no valor do título.</li>
                </ul>
                
                <p><strong>Características importantes:</strong></p>
                <ul>
                    <li>Quanto maior o prazo do título, maior sua duration (geralmente).</li>
                    <li>Quanto menor a taxa de cupom, maior a duration.</li>
                    <li>A duration diminui quando a taxa de mercado aumenta.</li>
                    <li>Títulos zero-cupom têm duration igual ao seu prazo de vencimento.</li>
                </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('<div class="sub-header">Calculadora de Duration</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Inputs para o cálculo da duration
            st.markdown("<h3>Parâmetros do Título</h3>", unsafe_allow_html=True)
            
            valor_nominal = st.number_input("Valor Nominal (R$)", min_value=100.0, value=1000.0, step=100.0)
            taxa_cupom = st.number_input("Taxa de Cupom Anual (%)", min_value=0.0, max_value=20.0, value=5.0, step=0.5)
            frequencia_pagamentos = st.selectbox("Frequência de Pagamentos", ["Anual", "Semestral", "Trimestral"], index=0)
            
            if frequencia_pagamentos == "Anual":
                freq = 1
            elif frequencia_pagamentos == "Semestral":
                freq = 2
            else:
                freq = 4
            
            prazo_anos = st.number_input("Prazo (anos)", min_value=1, max_value=30, value=5, step=1)
            taxa_mercado = st.number_input("Taxa de Mercado Anual (%)", min_value=0.1, max_value=20.0, value=6.0, step=0.1)
            
            # Botão para calcular
            calcular = st.button("Calcular Duration")
        
        with col2:
            if calcular:
                # Calculando o cupom periódico
                cupom_periodico = taxa_cupom / 100 / freq
                
                # Calculando a taxa de desconto periódica
                taxa_periodica = taxa_mercado / 100 / freq
                
                # Número total de períodos
                n_periodos = prazo_anos * freq
                
                # Calculando os fluxos de caixa e seus valores presentes
                periodos = np.arange(1, n_periodos + 1)
                fluxos = np.ones(n_periodos) * valor_nominal * cupom_periodico
                fluxos[-1] += valor_nominal  # Adiciona o principal no último período
                
                # Fatores de desconto
                fatores_desconto = 1 / (1 + taxa_periodica) ** periodos
                
                # Valores presentes dos fluxos
                vp_fluxos = fluxos * fatores_desconto
                
                # Preço do título
                preco = np.sum(vp_fluxos)
                
                # Calculando a duration de Macaulay
                macaulay_duration = np.sum(periodos * vp_fluxos) / preco
                
                # Convertendo para anos
                macaulay_duration_anos = macaulay_duration / freq
                
                # Calculando a duration modificada
                modified_duration = macaulay_duration / (1 + taxa_periodica)
                modified_duration_anos = modified_duration / freq
                
                # Exibindo os resultados
                st.markdown(
                    f"""
                    <div class="section">
                    <h3>Resultados</h3>
                    <p><strong>Preço do Título:</strong> R$ {preco:.2f}</p>
                    <p><strong>Duration de Macaulay:</strong> {macaulay_duration_anos:.2f} anos</p>
                    <p><strong>Duration Modificada:</strong> {modified_duration_anos:.2f} anos</p>
                    
                    <h4>Sensibilidade do Preço</h4>
                    <ul>
                        <li>Se as taxas aumentarem 1%, o valor do título cairá aproximadamente {modified_duration_anos:.2f}%, para R$ {preco * (1 - modified_duration_anos/100):.2f}</li>
                        <li>Se as taxas caírem 1%, o valor do título aumentará aproximadamente {modified_duration_anos:.2f}%, para R$ {preco * (1 + modified_duration_anos/100):.2f}</li>
                    </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Criando gráfico com a sensibilidade do preço a mudanças na taxa
                deltas = np.linspace(-2, 2, 9)  # Variações de -2% a +2% em 0.5%
                precos = [preco * (1 + (-modified_duration_anos * delta / 100)) for delta in deltas]
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=deltas,
                    y=precos,
                    mode='lines+markers',
                    name='Preço Estimado',
                    line=dict(color='#3B82F6', width=3),
                    marker=dict(size=8)
                ))
                
                fig.update_layout(
                    title='Sensibilidade do Preço a Variações na Taxa de Juros',
                    xaxis_title='Variação na Taxa de Juros (%)',
                    yaxis_title='Preço do Título (R$)',
                    template='plotly_white'
                )
                
                # Adicionando linha vertical na posição atual
                fig.add_shape(
                    type="line",
                    x0=0, y0=0,
                    x1=0, y1=preco,
                    line=dict(color="red", width=2, dash="dot")
                )
                
                # Adicionando ponto para marcar o preço atual
                fig.add_trace(go.Scatter(
                    x=[0],
                    y=[preco],
                    mode='markers',
                    marker=dict(size=12, color='red'),
                    name='Preço Atual'
                ))
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Preencha os parâmetros do título e clique em 'Calcular Duration' para ver os resultados.")
        
        st.markdown(
            """
            <div class="warning">
            <h3>A Duration no Caso SVB</h3>
            <p>O SVB mantinha uma carteira substancial de títulos de longo prazo, com duration média de 5,7 anos. Com esta duration,
            um aumento de 1% nas taxas de juros causaria uma queda aproximada de 5,7% no valor de mercado desses títulos.</p>
            
            <p>O banco tinha aproximadamente $117 bilhões em títulos de longo prazo, o que significa que um aumento de 2% nas taxas
            (como ocorreu de 2022 a 2023) teria um impacto estimado de 11,4%, ou cerca de $13,3 bilhões de perda de valor de mercado.
            Com um patrimônio de apenas $16 bilhões, estas perdas foram suficientes para comprometer seriamente a solvência do banco.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with tab2:
        st.markdown('<div class="sub-header">DV01/PVBP: Conceito e Aplicação</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.markdown(
                """
                <div class="section">
                <h3>O que são DV01 e PVBP?</h3>
                <p>DV01 (Dollar Value of 01) e PVBP (Price Value of a Basis Point) são medidas que indicam a mudança absoluta 
                no valor de um título ou carteira para uma variação de 1 ponto base (0,01%) na taxa de juros.</p>
                
                <p>Enquanto a Duration expressa a sensibilidade em termos percentuais, o DV01/PVBP a expressa em termos monetários,
                o que pode ser mais útil para gestores de risco e traders.</p>
                
                <p>A relação entre Duration Modificada e DV01 é dada por:</p>
                
                <p style="text-align: center;"><strong>DV01 = Duration Modificada × Valor do Título × 0,0001</strong></p>
                
                <p>O DV01/PVBP é particularmente útil para:</p>
                <ul>
                    <li>Quantificar o risco de mercado em termos monetários</li>
                    <li>Comparar a sensibilidade de diferentes títulos ou carteiras</li>
                    <li>Estabelecer limites de risco</li>
                    <li>Dimensionar operações de hedge</li>
                </ul>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                """
                <div class="info">
                <h3>Exemplo Prático</h3>
                
                <p>Considere um título com:</p>
                <ul>
                    <li>Valor de mercado: R$ 10 milhões</li>
                    <li>Duration modificada: 4 anos</li>
                </ul>
                
                <p>O DV01 deste título seria:</p>
                <p>DV01 = 4 × R$ 10 milhões × 0,0001 = R$ 4.000</p>
                
                <p>Isso significa que para cada ponto base (0,01%) de aumento na taxa de juros, o valor do título 
                cairá em R$ 4.000. Para um aumento de 50 pontos base (0,5%), a perda seria de aproximadamente R$ 200.000.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('<div class="sub-header">Calculadora de DV01/PVBP</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Inputs para o cálculo de DV01/PVBP
            st.markdown("<h3>Parâmetros</h3>", unsafe_allow_html=True)
            
            valor_carteira = st.number_input("Valor da Carteira (milhões R$)", min_value=1.0, value=100.0, step=1.0)
            dur_modificada = st.number_input("Duration Modificada (anos)", min_value=0.1, max_value=20.0, value=4.0, step=0.1)
            pontos_base = st.slider("Variação em Pontos Base", min_value=1, max_value=300, value=100, step=1)
            
            # Botão para calcular
            calcular_dv01 = st.button("Calcular DV01/PVBP")
        
        with col2:
            if calcular_dv01:
                # Calculando o DV01
                dv01 = dur_modificada * valor_carteira * 1000000 * 0.0001
                
                # Calculando o impacto para a variação em pontos base
                impacto = dv01 * pontos_base
                impacto_percentual = dur_modificada * pontos_base * 0.0001 * 100
                
                # Exibindo os resultados
                st.markdown(
                    f"""
                    <div class="section">
                    <h3>Resultados</h3>
                    <p><strong>DV01/PVBP:</strong> R$ {dv01:,.2f}</p>
                    <p>Para uma variação de {pontos_base} pontos base ({pontos_base/100:.2f}%):</p>
                    <p><strong>Impacto no Valor:</strong> R$ {impacto:,.2f}</p>
                    <p><strong>Impacto Percentual:</strong> {impacto_percentual:.2f}%</p>
                    
                    <h4>Interpretação</h4>
                    <p>Para cada ponto base (0,01%) de variação na taxa de juros, o valor da carteira varia em R$ {dv01:,.2f}.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Criando um gráfico para mostrar o impacto de diferentes variações de taxa
                pb_range = np.arange(-200, 201, 20)
                impactos = [dv01 * pb for pb in pb_range]
                
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=pb_range,
                    y=impactos,
                    marker_color=['#EF4444' if imp < 0 else '#10B981' for imp in impactos]
                ))
                
                fig.update_layout(
                    title='Impacto no Valor da Carteira para Diferentes Variações de Taxa',
                    xaxis_title='Variação em Pontos Base',
                    yaxis_title='Impacto no Valor (R$)',
                    template='plotly_white'
                )
                
                # Adicionando linha horizontal no zero
                fig.add_shape(
                    type="line",
                    x0=min(pb_range), y0=0,
                    x1=max(pb_range), y1=0,
                    line=dict(color="black", width=1, dash="dot")
                )
                
                # Marcando a variação selecionada
                fig.add_trace(go.Scatter(
                    x=[pontos_base],
                    y=[dv01 * pontos_base],
                    mode='markers',
                    marker=dict(size=12, color='blue'),
                    name=f'Variação de {pontos_base} pb'
                ))
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Preencha os parâmetros e clique em 'Calcular DV01/PVBP' para ver os resultados.")
        
        st.markdown(
            """
            <div class="warning">
            <h3>DV01/PVBP no Caso SVB</h3>
            <p>Com ativos de aproximadamente $117 bilhões em títulos de longo prazo e uma duration modificada de cerca de 5,7 anos,
            o DV01 do SVB pode ser estimado em:</p>
            
            <p>DV01 = 5,7 × $117 bilhões × 0,0001 ≈ $66,7 milhões</p>
            
            <p>Isso significa que para cada ponto base de aumento nas taxas de juros, o banco perderia cerca de $66,7 milhões no valor
            de mercado de sua carteira. Com um aumento de 200 pontos base (2%) como ocorreu, as perdas potenciais chegariam a aproximadamente
            $13,3 bilhões, ou cerca de 83% do patrimônio do banco ($16 bilhões).</p>
            
            <p>Esta análise ajuda a entender por que o aumento nas taxas de juros teve um impacto tão devastador na solvência do SVB.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Função para a página de Stress Testing
def stress_testing_page():
    st.markdown('<div class="main-header">Stress Testing para Risco de Taxas de Juros</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="section">
        <p>Stress Testing é uma técnica de gestão de risco que avalia a capacidade de uma instituição financeira de resistir a 
        cenários extremos, porém plausíveis. No contexto do risco de taxas de juros, o stress testing simula o impacto de 
        variações abruptas e significativas nas taxas sobre o valor dos ativos, passivos e o patrimônio do banco.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sub-header">Conceito e Importância</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(
            """
            <div class="section">
            <h3>Objetivos do Stress Testing</h3>
            <ul>
                <li><strong>Identificar vulnerabilidades:</strong> Detectar pontos fracos na estrutura de ativos e passivos.</li>
                <li><strong>Quantificar impactos potenciais:</strong> Mensurar as perdas em cenários de estresse.</li>
                <li><strong>Avaliar a resiliência:</strong> Verificar se o capital é suficiente para absorver perdas extremas.</li>
                <li><strong>Planejar contingências:</strong> Desenvolver planos de ação para cenários adversos.</li>
                <li><strong>Atender requisitos regulatórios:</strong> Cumprir exigências de supervisores bancários.</li>
            </ul>
            
            <h3>Tipos de Cenários de Estresse</h3>
            <ul>
                <li><strong>Choques paralelos:</strong> Deslocamento paralelo de toda a curva de juros (e.g., +200bps em todos os vértices).</li>
                <li><strong>Choques não-paralelos:</strong> Alterações específicas em diferentes partes da curva (e.g., aumento em taxas curtas e queda em taxas longas).</li>
                <li><strong>Cenários históricos:</strong> Replicação de eventos passados significativos (e.g., crise de 2008).</li>
                <li><strong>Cenários hipotéticos:</strong> Baseados em situações plausíveis, mas ainda não observadas.</li>
                <li><strong>Cenários reversos:</strong> Identificação de movimentos de taxas que causariam dano específico.</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="info">
            <h3>Frequência e Regulação</h3>
            <p>Reguladores como o Banco Central do Brasil, Federal Reserve (EUA) e Banco Central Europeu exigem que bancos realizem 
            testes de estresse periodicamente. Os resultados destes testes podem influenciar:</p>
            <ul>
                <li>Requisitos de capital</li>
                <li>Limites de exposição a riscos</li>
                <li>Políticas de dividendos</li>
                <li>Aprovação de fusões e aquisições</li>
            </ul>
            
            <h3>Caso SVB: Falha no Stress Testing?</h3>
            <p>Uma das questões levantadas após o colapso do SVB foi se os reguladores falharam em realizar testes de estresse 
            adequados. Alguns especialistas argumentam que os testes focavam principalmente no risco de crédito, e não 
            capturavam adequadamente cenários de aumento rápido nas taxas de juros após um longo período de taxas baixas.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown('<div class="sub-header">Simulador de Stress Testing</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<h3>Parâmetros da Simulação</h3>", unsafe_allow_html=True)
        
        # Inputs para a simulação
        st.markdown("<p><strong>Composição da Carteira:</strong></p>", unsafe_allow_html=True)
        
        valor_total = st.number_input("Valor Total da Carteira (milhões R$)", min_value=100.0, value=1000.0, step=100.0)
        
        st.markdown("<p>Distribuição por Classe de Ativo:</p>", unsafe_allow_html=True)
        
        pct_titulos_curtos = st.slider("Títulos de Curto Prazo (%)", min_value=0, max_value=100, value=20, step=5)
        pct_titulos_medios = st.slider("Títulos de Médio Prazo (%)", min_value=0, max_value=100, value=30, step=5)
        pct_titulos_longos = st.slider("Títulos de Longo Prazo (%)", min_value=0, max_value=100, value=50, step=5)
        
        # Verificando se a soma é 100%
        soma_pct = pct_titulos_curtos + pct_titulos_medios + pct_titulos_longos
        
        if soma_pct != 100:
            st.warning(f"A soma dos percentuais deve ser 100%. Atualmente: {soma_pct}%")
        
        # Duration para cada classe
        dur_titulos_curtos = st.number_input("Duration - Títulos Curtos (anos)", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
        dur_titulos_medios = st.number_input("Duration - Títulos Médios (anos)", min_value=2.0, max_value=5.0, value=3.5, step=0.1)
        dur_titulos_longos = st.number_input("Duration - Títulos Longos (anos)", min_value=4.0, max_value=20.0, value=7.0, step=0.1)
        
        # Parâmetros do stress test
        st.markdown("<p><strong>Cenários de Estresse:</strong></p>", unsafe_allow_html=True)
        
        cenario = st.selectbox(
            "Selecione um cenário pré-definido",
            [
                "Choque Paralelo: +200 bps",
                "Choque Paralelo: +300 bps",
                "Choque Paralelo: +400 bps",
                "Choque Descasado: Curto +300 bps, Médio +200 bps, Longo +100 bps",
                "Choque Descasado: Curto +100 bps, Médio +200 bps, Longo +300 bps",
                "Cenário Personalizado"
            ]
        )
        
        # Definindo os choques com base no cenário selecionado
        if cenario == "Choque Paralelo: +200 bps":
            choque_curto = choque_medio = choque_longo = 200
        elif cenario == "Choque Paralelo: +300 bps":
            choque_curto = choque_medio = choque_longo = 300
        elif cenario == "Choque Paralelo: +400 bps":
            choque_curto = choque_medio = choque_longo = 400
        elif cenario == "Choque Descasado: Curto +300 bps, Médio +200 bps, Longo +100 bps":
            choque_curto, choque_medio, choque_longo = 300, 200, 100
        elif cenario == "Choque Descasado: Curto +100 bps, Médio +200 bps, Longo +300 bps":
            choque_curto, choque_medio, choque_longo = 100, 200, 300
        else:  # Cenário Personalizado
            choque_curto = st.number_input("Choque - Taxas Curtas (bps)", min_value=0, max_value=500, value=200, step=10)
            choque_medio = st.number_input("Choque - Taxas Médias (bps)", min_value=0, max_value=500, value=200, step=10)
            choque_longo = st.number_input("Choque - Taxas Longas (bps)", min_value=0, max_value=500, value=200, step=10)
        
        # Capital próprio
        capital = st.number_input("Capital Próprio (milhões R$)", min_value=10.0, max_value=valor_total, value=100.0, step=10.0)
        
        # Botão para executar o stress test
        executar = st.button("Executar Stress Test")
    
    with col2:
        if executar:
            if soma_pct != 100:
                st.error("Não é possível executar a simulação. A soma dos percentuais da carteira deve ser 100%.")
            else:
                # Calculando os valores por classe de ativo
                valor_curto = valor_total * pct_titulos_curtos / 100
                valor_medio = valor_total * pct_titulos_medios / 100
                valor_longo = valor_total * pct_titulos_longos / 100
                
                # Calculando as perdas em cada classe (em %)
                perda_pct_curto = dur_titulos_curtos * choque_curto / 10000  # bps para decimal e duration modificada
                perda_pct_medio = dur_titulos_medios * choque_medio / 10000
                perda_pct_longo = dur_titulos_longos * choque_longo / 10000
                
                # Calculando as perdas em cada classe (em valor)
                perda_valor_curto = valor_curto * perda_pct_curto
                perda_valor_medio = valor_medio * perda_pct_medio
                perda_valor_longo = valor_longo * perda_pct_longo
                
                # Calculando a perda total
                perda_total = perda_valor_curto + perda_valor_medio + perda_valor_longo
                
                # Calculando o impacto no capital
                capital_restante = capital - perda_total
                impacto_pct_capital = perda_total / capital * 100
                
                # Preparando dados para o DataFrame
                classes = ["Títulos Curtos", "Títulos Médios", "Títulos Longos", "Total"]
                valores = [valor_curto, valor_medio, valor_longo, valor_total]
                durations = [dur_titulos_curtos, dur_titulos_medios, dur_titulos_longos, "-"]
                choques = [choque_curto, choque_medio, choque_longo, "-"]
                perdas_pct = [round(perda_pct_curto * 100, 2),
                            round(perda_pct_medio * 100, 2),
                            round(perda_pct_longo * 100, 2),
                            "-"]
                perdas_valor = [perda_valor_curto, perda_valor_medio, perda_valor_longo, perda_total]
                
                if "df" not in st.session_state:
                    # Calcular os dados só uma vez
                    st.session_state.classes = classes
                    st.session_state.valores = valores
                    st.session_state.durations = durations
                    st.session_state.choques = choques
                    st.session_state.perdas_pct = [
                        round(p, 2) if isinstance(p, (int, float)) else p for p in perdas_pct
                    ]
                    st.session_state.perdas_valor = perdas_valor

                    # Criando e armazenando o DataFrame
                    st.session_state.df = pd.DataFrame({
                        "Classe": st.session_state.classes,
                        "Valor (M R$)": st.session_state.valores,
                        "Duration (anos)": st.session_state.durations,
                        "Choque (bps)": st.session_state.choques,
                        "Perda (%)": st.session_state.perdas_pct,
                        "Perda (M R$)": st.session_state.perdas_valor
                    })

                # Exibindo resultados
                st.markdown("<h3>Resultados do Stress Test</h3>", unsafe_allow_html=True)
                st.dataframe(st.session_state.df, use_container_width=True)
                
                # Status da solvência
                if capital_restante <= 0:
                    status = "INSOLVÊNCIA"
                    cor = "#EF4444"
                elif impacto_pct_capital >= 50:
                    status = "ALTO RISCO"
                    cor = "#F59E0B"
                elif impacto_pct_capital >= 25:
                    status = "RISCO MODERADO"
                    cor = "#3B82F6"
                else:
                    status = "ADEQUADO"
                    cor = "#10B981"
                
                # Exibindo o impacto no capital
                st.markdown(
                    f"""
                    <div style="background-color: #F8FAFC; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
                    <p><strong>Capital Inicial:</strong> R$ {capital:.2f} milhões</p>
                    <p><strong>Perda Total:</strong> R$ {perda_total:.2f} milhões ({impacto_pct_capital:.2f}% do capital)</p>
                    <p><strong>Capital Remanescente:</strong> R$ {capital_restante:.2f} milhões</p>
                    <h3 style="color: {cor}; text-align: center; margin-top: 1rem;">Status: {status}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Gráfico de barras com as perdas por classe
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=classes[:3],
                    y=perdas_valor[:3],
                    name="Perda por Classe",
                    marker_color="#EF4444"
                ))
                
                fig.update_layout(
                    title="Perdas por Classe de Ativo",
                    xaxis_title="Classe de Ativo",
                    yaxis_title="Perda (milhões R$)",
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Gráfico de capital antes e depois
                fig_capital = go.Figure()
                
                fig_capital.add_trace(go.Bar(
                    x=["Antes do Choque", "Depois do Choque"],
                    y=[capital, max(0, capital_restante)],
                    marker_color=["#3B82F6", "#10B981" if capital_restante > 0 else "#EF4444"]
                ))
                
                fig_capital.update_layout(
                    title="Impacto no Capital",
                    xaxis_title="",
                    yaxis_title="Capital (milhões R$)",
                    template="plotly_white"
                )
                
                # Adicionando linha para o capital mínimo (hipotético, 50% do capital inicial)
                capital_minimo = capital * 0.5
                
                fig_capital.add_shape(
                    type="line",
                    x0=-0.5, y0=capital_minimo,
                    x1=1.5, y1=capital_minimo,
                    line=dict(color="#F59E0B", width=2, dash="dash"),
                )
                
                fig_capital.add_annotation(
                    x=0.5, y=capital_minimo,
                    text="Capital Mínimo Regulatório (ilustrativo)",
                    showarrow=False,
                    yshift=10,
                    font=dict(color="#F59E0B")
                )
                
                st.plotly_chart(fig_capital, use_container_width=True)
                
                # Análise complementar
                st.markdown(
                    """
                    <div class="highlight">
                    <h3>Análise do Resultado</h3>
                    """,
                    unsafe_allow_html=True
                )
                
                if capital_restante <= 0:
                    st.markdown(
                        """
                        <p>O cenário de estresse testado resultaria em <strong>insolvência</strong> da instituição.
                        As perdas provocadas pelo choque de taxas excederiam o capital disponível, exigindo intervenção 
                        regulatória ou injeção de capital.</p>
                        """,
                        unsafe_allow_html=True
                    )
                elif impacto_pct_capital >= 50:
                    st.markdown(
                        """
                        <p>O cenário de estresse testado resultaria em <strong>alto risco</strong> para a instituição.
                        Embora o banco permaneça tecnicamente solvente, o capital remanescente seria insuficiente para 
                        atender requisitos regulatórios mínimos, exigindo ações corretivas imediatas.</p>
                        """,
                        unsafe_allow_html=True
                    )
                elif impacto_pct_capital >= 25:
                    st.markdown(
                        """
                        <p>O cenário de estresse testado resultaria em <strong>risco moderado</strong> para a instituição.
                        O banco manteria capital suficiente para permanecer solvente, mas seria prudente revisar a estrutura
                        de ativos e passivos para reduzir a exposição ao risco de taxas de juros.</p>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <p>O cenário de estresse testado resultaria em uma situação <strong>adequada</strong> de capital.
                        A instituição demonstra resiliência suficiente para absorver choques significativos nas taxas de juros
                        sem comprometer sua solvência ou estabilidade.</p>
                        """,
                        unsafe_allow_html=True
                    )
                
                # Classe com maior contribuição para a perda
                maior_perda_idx = perdas_valor[:3].index(max(perdas_valor[:3]))
                maior_perda_classe = classes[maior_perda_idx]
                
                st.markdown(
                    f"""
                    <p>A classe de ativos que mais contribuiu para a perda total foi <strong>{maior_perda_classe}</strong>,
                    respondendo por {perdas_valor[maior_perda_idx]/perda_total*100:.2f}% da perda total. Isso reflete a combinação
                    de valor exposto e sensibilidade (duration) desta classe às variações de taxa de juros.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
        else:
            st.info("Configure os parâmetros e clique em 'Executar Stress Test' para ver os resultados da simulação.")
    
    st.markdown(
        """
        <div class="warning">
        <h3>O Stress Testing no Caso SVB</h3>
        <p>Simulações de stress test realizadas após a quebra do SVB demonstraram que o banco estava extremamente vulnerável
        a aumentos nas taxas de juros, devido à combinação de:</p>
        <ul>
            <li>Alta concentração em títulos de longo prazo (55% dos ativos)</li>
            <li>Duration elevada destes títulos (5,7 anos em média)</li>
            <li>Baixo nível de capital em relação ao risco assumido</li>
            <li>Dependência de depósitos voláteis, não segurados e concentrados no setor de tecnologia</li>
        </ul>
        
        <p>Um stress test com aumento de 200-300 bps, similar ao que efetivamente ocorreu, teria indicado potencial
        insolvência do banco, sinalizando a necessidade de ações preventivas como:</p>
        <ul>
            <li>Hedge da exposição à taxa de juros com derivativos</li>
            <li>Diversificação das fontes de financiamento</li>
            <li>Aumento do capital próprio</li>
            <li>Redução da duration média da carteira</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )        
        




# Função para a página de Gestão Ativo-Passivo (ALM)
def alm_page():
    st.markdown('<div class="main-header">Gestão Ativo-Passivo (ALM - Asset and Liability Management)</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="section">
        <p>A Gestão Ativo-Passivo (ALM) é uma abordagem estratégica e integrada para gerenciar os riscos decorrentes de descasamentos
        entre ativos e passivos de uma instituição financeira. No contexto do risco de taxas de juros, o ALM busca equilibrar 
        rentabilidade e risco, gerenciando conjuntamente os vencimentos, durations e reprecificações de ativos e passivos.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sub-header">Conceito e Componentes</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown(
            """
            <div class="section">
            <h3>Principais Componentes do ALM</h3>
            <ul>
                <li><strong>Gerenciamento de Liquidez:</strong> Assegurar recursos suficientes para honrar obrigações à medida que vencem.</li>
                <li><strong>Gerenciamento do Risco de Taxa de Juros:</strong> Controlar o impacto de mudanças nas taxas sobre o valor econômico e a margem financeira.</li>
                <li><strong>Estratégia de Financiamento:</strong> Diversificar fontes e prazos de captação para reduzir vulnerabilidades.</li>
                <li><strong>Precificação de Transferência:</strong> Mecanismos internos para alocar custos e benefícios das decisões de ALM.</li>
                <li><strong>Planejamento de Capital:</strong> Assegurar capital suficiente para absorver perdas em cenários adversos.</li>
            </ul>
            
            <h3>Estratégias para Gestão do Risco de Taxa de Juros</h3>
            <ul>
                <li><strong>Imunização de Carteira:</strong> Estruturar ativos e passivos para que seus valores respondam de forma semelhante a variações nas taxas.</li>
                <li><strong>Casamento de Duration:</strong> Buscar equilibrar a duration média de ativos e passivos.</li>
                <li><strong>Hedges com Derivativos:</strong> Utilizar swaps, futuros e opções para proteger posições contra movimentos adversos nas taxas.</li>
                <li><strong>Diversificação Temporal:</strong> Distribuir vencimentos e reprecificações ao longo do tempo para evitar concentrações.</li>
                <li><strong>Limitação de Exposições:</strong> Estabelecer limites para gaps de reprecificação e duration.</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="info">
            <h3>Governança e Organização</h3>
            <p>As atividades de ALM são tipicamente supervisionadas por um comitê específico (ALCO - Asset and Liability Committee),
            composto por representantes das áreas de:</p>
            <ul>
                <li>Tesouraria</li>
                <li>Gestão de Riscos</li>
                <li>Planejamento Financeiro</li>
                <li>Áreas de Negócio</li>
            </ul>
            
            <p>O ALCO se reúne periodicamente para:</p>
            <ul>
                <li>Revisar métricas de risco</li>
                <li>Analisar tendências do mercado</li>
                <li>Definir estratégias de hedge</li>
                <li>Aprovar limites de exposição</li>
                <li>Deliberar sobre ajustes na estrutura de ativos e passivos</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.markdown('<div class="sub-header">Simulador de ALM</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("<h3>Parâmetros da Simulação</h3>", unsafe_allow_html=True)
        
        # Inputs para a simulação
        st.markdown("<p><strong>Estrutura Atual:</strong></p>", unsafe_allow_html=True)
        
        ativos_valor = st.number_input("Valor Total dos Ativos (milhões R$)", min_value=100.0, value=1000.0, step=100.0)
        ativos_duration = st.slider("Duration Média dos Ativos (anos)", min_value=0.1, max_value=10.0, value=5.0, step=0.1)
        
        passivos_valor = st.number_input("Valor Total dos Passivos (milhões R$)", min_value=100.0, value=900.0, step=100.0)
        passivos_duration = st.slider("Duration Média dos Passivos (anos)", min_value=0.1, max_value=10.0, value=2.0, step=0.1)
        
        # Inputs para estratégia de ALM
        st.markdown("<p><strong>Estratégia de ALM:</strong></p>", unsafe_allow_html=True)
        
        estrategia = st.selectbox(
            "Selecione uma estratégia",
            [
                "Manter estrutura atual",
                "Reduzir duration dos ativos",
                "Aumentar duration dos passivos",
                "Hedge com derivativos",
                "Combinação de estratégias"
            ]
        )
        
        # Parâmetros específicos da estratégia selecionada
        if estrategia == "Manter estrutura atual":
            ativos_duration_nova = ativos_duration
            passivos_duration_nova = passivos_duration
            hedge_valor = 0.0
            hedge_duration = 0.0
        elif estrategia == "Reduzir duration dos ativos":
            ativos_duration_nova = st.slider("Nova Duration Média dos Ativos (anos)", min_value=0.1, max_value=ativos_duration, value=max(1.0, ativos_duration-2), step=0.1)
            passivos_duration_nova = passivos_duration
            hedge_valor = 0.0
            hedge_duration = 0.0
        elif estrategia == "Aumentar duration dos passivos":
            ativos_duration_nova = ativos_duration
            passivos_duration_nova = st.slider("Nova Duration Média dos Passivos (anos)", min_value=passivos_duration, max_value=10.0, value=min(5.0, passivos_duration+2), step=0.1)
            hedge_valor = 0.0
            hedge_duration = 0.0
        elif estrategia == "Hedge com derivativos":
            ativos_duration_nova = ativos_duration
            passivos_duration_nova = passivos_duration
            hedge_valor = st.slider("Valor Nocional do Hedge (% dos Ativos)", min_value=0.0, max_value=100.0, value=50.0, step=5.0)
            hedge_duration = st.slider("Duration Efetiva do Hedge (anos)", min_value=-10.0, max_value=10.0, value=-5.0, step=0.5)
            hedge_valor = ativos_valor * hedge_valor / 100  # Convertendo para valor absoluto
        else:  # Combinação de estratégias
            ativos_duration_nova = st.slider("Nova Duration Média dos Ativos (anos)", min_value=0.1, max_value=ativos_duration, value=max(1.0, ativos_duration-1), step=0.1)
            passivos_duration_nova = st.slider("Nova Duration Média dos Passivos (anos)", min_value=passivos_duration, max_value=10.0, value=min(4.0, passivos_duration+1), step=0.1)
            hedge_valor = st.slider("Valor Nocional do Hedge (% dos Ativos)", min_value=0.0, max_value=100.0, value=25.0, step=5.0)
            hedge_duration = st.slider("Duration Efetiva do Hedge (anos)", min_value=-10.0, max_value=10.0, value=-3.0, step=0.5)
            hedge_valor = ativos_valor * hedge_valor / 100  # Convertendo para valor absoluto
        
        # Cenário de variação de taxa
        taxa_variacao = st.slider("Variação na Taxa de Juros (bps)", min_value=-300, max_value=300, value=100, step=10)
        
        # Botão para executar a simulação
        executar = st.button("Executar Simulação")
    
    with col2:
        if executar:
            # Calculando o patrimônio
            patrimonio = ativos_valor - passivos_valor
            
            # Calculando o gap de duration antes e depois da estratégia
            gap_duration_antes = ativos_duration - (passivos_valor / ativos_valor) * passivos_duration
            
            # Calculando o efeito do hedge (se houver)
            if hedge_valor > 0:
                # Ajustando a duration efetiva dos ativos considerando o hedge
                ativos_duration_ajustada = (ativos_valor * ativos_duration_nova + hedge_valor * hedge_duration) / ativos_valor
            else:
                ativos_duration_ajustada = ativos_duration_nova
            
            # Calculando o novo gap de duration
            gap_duration_depois = ativos_duration_ajustada - (passivos_valor / ativos_valor) * passivos_duration_nova
            
            # Calculando a sensibilidade do valor econômico antes e depois
            sensibilidade_antes = gap_duration_antes * ativos_valor * (taxa_variacao / 10000)  # bps para decimal
            sensibilidade_depois = gap_duration_depois * ativos_valor * (taxa_variacao / 10000)
            
            # Calculando o impacto no patrimônio antes e depois
            impacto_patrimonio_antes = sensibilidade_antes
            novo_patrimonio_antes = patrimonio - impacto_patrimonio_antes
            
            impacto_patrimonio_depois = sensibilidade_depois
            novo_patrimonio_depois = patrimonio - impacto_patrimonio_depois
            
            # Calculando a eficácia da estratégia
            reducao_impacto = impacto_patrimonio_antes - impacto_patrimonio_depois
            reducao_impacto_pct = (reducao_impacto / abs(impacto_patrimonio_antes)) * 100 if impacto_patrimonio_antes != 0 else 0
            
            # Exibindo resultados
            st.markdown("<h3>Análise da Estratégia de ALM</h3>", unsafe_allow_html=True)
            
            # Estrutura antes e depois
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(
                    """
                    <div style="background-color: #F8FAFC; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                    <h4>Estrutura Atual</h4>
                    <p><strong>Duration Ativos:</strong> {:.2f} anos</p>
                    <p><strong>Duration Passivos:</strong> {:.2f} anos</p>
                    <p><strong>Gap de Duration:</strong> {:.2f} anos</p>
                    </div>
                    """.format(ativos_duration, passivos_duration, gap_duration_antes),
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    """
                    <div style="background-color: #F8FAFC; padding: 1rem; border-radius: 0.5rem; text-align: center;">
                    <h4>Estrutura Após Estratégia</h4>
                    <p><strong>Duration Ativos:</strong> {:.2f} anos</p>
                    <p><strong>Duration Passivos:</strong> {:.2f} anos</p>
                    <p><strong>Gap de Duration:</strong> {:.2f} anos</p>
                    </div>
                    """.format(ativos_duration_ajustada, passivos_duration_nova, gap_duration_depois),
                    unsafe_allow_html=True
                )
            
            # Impacto no patrimônio
            st.markdown("<h4>Impacto no Patrimônio para Variação de {} bps</h4>".format(taxa_variacao), unsafe_allow_html=True)
            
            # Criando o DataFrame para comparação
            df = pd.DataFrame({
                "Cenário": ["Antes da Estratégia", "Após Estratégia"],
                "Gap Duration (anos)": [gap_duration_antes, gap_duration_depois],
                "Sensibilidade (M R$)": [sensibilidade_antes, sensibilidade_depois],
                "Impacto no Patrimônio (M R$)": [impacto_patrimonio_antes, impacto_patrimonio_depois],
                "Patrimônio Final (M R$)": [novo_patrimonio_antes, novo_patrimonio_depois]
            })
            
            st.dataframe(df, use_container_width=True)
            
            # Gráfico de comparação
            fig = go.Figure()
            
            # Adicionando barras para os patrimônios
            fig.add_trace(go.Bar(
                x=["Patrimônio Inicial", "Patrimônio Final (Sem Estratégia)", "Patrimônio Final (Com Estratégia)"],
                y=[patrimonio, novo_patrimonio_antes, novo_patrimonio_depois],
                marker_color=["#3B82F6", "#EF4444" if novo_patrimonio_antes < 0 else "#F59E0B", "#10B981" if novo_patrimonio_depois > novo_patrimonio_antes else "#F59E0B"]
            ))
            
            fig.update_layout(
                title=f"Comparação do Patrimônio com Variação de {taxa_variacao} bps nas Taxas",
                xaxis_title="",
                yaxis_title="Patrimônio (milhões R$)",
                template="plotly_white"
            )
            
            # Adicionando linha horizontal no zero
            fig.add_shape(
                type="line",
                x0=-0.5, y0=0,
                x1=2.5, y1=0,
                line=dict(color="black", width=1, dash="dot")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Análise dos resultados
            if novo_patrimonio_depois <= 0 and novo_patrimonio_antes <= 0:
                resultado = "A estratégia não foi suficiente para prevenir a insolvência da instituição no cenário testado."
                cor = "#EF4444"
            elif novo_patrimonio_depois > 0 and novo_patrimonio_antes <= 0:
                resultado = "A estratégia foi altamente eficaz, prevenindo a insolvência da instituição no cenário testado."
                cor = "#10B981"
            elif reducao_impacto_pct >= 50:
                resultado = "A estratégia foi muito eficaz, reduzindo significativamente o impacto no patrimônio."
                cor = "#10B981"
            elif reducao_impacto_pct >= 20:
                resultado = "A estratégia foi moderadamente eficaz, reduzindo o impacto no patrimônio."
                cor = "#3B82F6"
            elif reducao_impacto_pct > 0:
                resultado = "A estratégia teve eficácia limitada, com redução pequena do impacto no patrimônio."
                cor = "#F59E0B"
            else:
                resultado = "A estratégia não foi eficaz, aumentando a exposição ao risco de taxa de juros."
                cor = "#EF4444"
            
            st.markdown(
                f"""
                <div style="background-color: {cor}; color: white; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem;">
                <h3>Conclusão da Análise</h3>
                <p>{resultado}</p>
                <p>A estratégia implementada resultou em uma redução de {reducao_impacto:.2f} milhões de R$ no impacto ao patrimônio
                ({reducao_impacto_pct:.2f}% de redução) para o cenário de variação de {taxa_variacao} bps nas taxas de juros.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Recomendações
            st.markdown("<h3>Recomendações Adicionais</h3>", unsafe_allow_html=True)
            
            if gap_duration_depois > 1:
                st.markdown(
                    """
                    <div class="info">
                    <p>O gap de duration permanece significativo. Considere medidas adicionais como:</p>
                    <ul>
                        <li>Ampliar o volume de hedge com derivativos</li>
                        <li>Reduzir ainda mais a duration dos ativos, com troca de títulos longos por curtos</li>
                        <li>Emitir dívida de longo prazo para aumentar a duration dos passivos</li>
                        <li>Manter maior nível de capital para absorver potenciais perdas</li>
                    </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif gap_duration_depois < -1:
                st.markdown(
                    """
                    <div class="info">
                    <p>O gap de duration está negativo e significativo. Isso significa que agora a instituição está exposta
                    a quedas nas taxas de juros. Considere medidas de equilíbrio como:</p>
                    <ul>
                        <li>Reduzir o volume de hedge</li>
                        <li>Aumentar a duration dos ativos</li>
                        <li>Reduzir a duration dos passivos</li>
                    </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <div class="info">
                    <p>O gap de duration está próximo do ideal. Recomendações para manter esta estrutura:</p>
                    <ul>
                        <li>Monitorar continuamente o gap de duration</li>
                        <li>Ajustar o portfolio conforme as condições de mercado evoluem</li>
                        <li>Implementar limites operacionais para manter o gap dentro de intervalos desejados</li>
                        <li>Realizar simulações periódicas de stress test</li>
                    </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("Configure os parâmetros e clique em 'Executar Simulação' para ver os resultados da análise ALM.")
    
    st.markdown(
        """
        <div class="warning">
        <h3>ALM no Caso SVB</h3>
        <p>O Silicon Valley Bank falhou gravemente na gestão ativo-passivo, especialmente em relação ao risco de taxa de juros. 
        Algumas das principais falhas foram:</p>
        <ul>
            <li><strong>Gap de Duration Extremo:</strong> O banco mantinha um gap de duration estimado entre 3 e 4 anos, muito acima
            dos níveis considerados prudentes para instituições financeiras.</li>
            <li><strong>Ausência de Hedge:</strong> O SVB reduziu dramaticamente o uso de derivativos para hedge de taxa de juros.
            O valor nocional de derivativos caiu de $10,7 bilhões para apenas $550 milhões entre 2021 e 2022.</li>
            <li><strong>Dependência de Depósitos Voláteis:</strong> O banco financiava ativos de longo prazo com depósitos de curto prazo,
            muitos dos quais não segurados e concentrados em um único setor (tecnologia).</li>
            <li><strong>Capital Insuficiente:</strong> O nível de capital do banco era inadequado para o nível de risco assumido
            em sua estratégia de investimento.</li>
        </ul>
        
        <p>Medidas de ALM que poderiam ter prevenido a quebra:</p>
        <ul>
            <li>Manter um programa ativo de hedge com swaps e outros derivativos</li>
            <li>Diversificar a estrutura de financiamento, com maior proporção de dívida de longo prazo</li>
            <li>Limitar o volume de investimentos em títulos de longo prazo</li>
            <li>Implementar limites rígidos para o gap de duration</li>
            <li>Realizar stress tests frequentes para diversos cenários de taxas</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
            )        



    st.markdown(
                    """
                    <div class="info">
                    <p>O gap de duration está próximo do ideal. Recomendações para manter esta estrutura:</p>
                    <ul>
                        <li>Monitorar continuamente o gap de duration</li>
                        <li>Ajustar o portfolio conforme as condições de mercado evoluem</li>
                        <li>Implementar limites operacionais para manter o gap dentro de intervalos desejados</li>
                        <li>Realizar simulações periódicas de stress test</li>
                    </ul>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    
    st.markdown(
        """
        <div class="warning">
        <h3>ALM no Caso SVB</h3>
        <p>O Silicon Valley Bank falhou gravemente na gestão ativo-passivo, especialmente em relação ao risco de taxa de juros. 
        Algumas das principais falhas foram:</p>
        <ul>
            <li><strong>Gap de Duration Extremo:</strong> O banco mantinha um gap de duration estimado entre 3 e 4 anos, muito acima
            dos níveis considerados prudentes para instituições financeiras.</li>
            <li><strong>Ausência de Hedge:</strong> O SVB reduziu dramaticamente o uso de derivativos para hedge de taxa de juros.
            O valor nocional de derivativos caiu de $10,7 bilhões para apenas $550 milhões entre 2021 e 2022.</li>
            <li><strong>Dependência de Depósitos Voláteis:</strong> O banco financiava ativos de longo prazo com depósitos de curto prazo,
            muitos dos quais não segurados e concentrados em um único setor (tecnologia).</li>
            <li><strong>Capital Insuficiente:</strong> O nível de capital do banco era inadequado para o nível de risco assumido
            em sua estratégia de investimento.</li>
        </ul>
        
        <p>Medidas de ALM que poderiam ter prevenido a quebra:</p>
        <ul>
            <li>Manter um programa ativo de hedge com swaps e outros derivativos</li>
            <li>Diversificar a estrutura de financiamento, com maior proporção de dívida de longo prazo</li>
            <li>Limitar o volume de investimentos em títulos de longo prazo</li>
            <li>Implementar limites rígidos para o gap de duration</li>
            <li>Realizar stress tests frequentes para diversos cenários de taxas</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# Função para a página de referências
def references_page():
    st.markdown('<div class="main-header">Referências e Recursos Adicionais</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="section">
        <p>Esta seção apresenta as principais referências utilizadas para o desenvolvimento deste aplicativo, bem como
        recursos adicionais para aprofundamento no tema do Risco de Taxas de Juros.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sub-header">Artigos e Publicações</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="section">
        <ol>
            <li><strong>Lucas, D. J., & Golding, E. L. (2023).</strong> Duration Gap Disclosure: A Modest Proposal to Prevent Another SVB. MIT Golub Center for Finance and Policy.</li>
            <li><strong>Tuckman, B., & Serrat, A. (2011).</strong> Fixed Income Securities: Tools for Today's Markets (3rd ed.). Wiley.</li>
            <li><strong>Jaffe, D. (2003).</strong> The Interest Rate Risk of Fannie Mae and Freddie Mac. Journal of Financial Services Research.</li>
            <li><strong>Frame, S., & Wall, L. D. (2002).</strong> Fannie Mae's and Freddie Mac's Voluntary Initiatives: Lessons from Banking. Federal Reserve Bank of Atlanta Economic Review.</li>
            <li><strong>Basel Committee on Banking Supervision. (2016).</strong> Standards: Interest rate risk in the banking book. Bank for International Settlements.</li>
        </ol>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sub-header">Sites e Recursos Online</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="section">
        <ul>
            <li><a href="https://www.bis.org/bcbs/publ/d368.htm" target="_blank">Bank for International Settlements - Interest Rate Risk in the Banking Book</a></li>
            <li><a href="https://www.federalreserve.gov/supervisionreg/topics/interest_rate_risk.htm" target="_blank">Federal Reserve - Interest Rate Risk Management</a></li>
            <li><a href="https://www.fdic.gov/news/press-releases/2023/pr23018.html" target="_blank">FDIC - Silicon Valley Bank Failure Reports</a></li>
            <li><a href="https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2191.en.pdf" target="_blank">European Central Bank - The Pricing of Interest Rate Risk</a></li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="sub-header">Ferramentas e Calculadoras</div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="section">
        <ul>
            <li><a href="https://www.treasurers.org/hub/treasurer-magazine/technical/duration-and-interest-rate-risk" target="_blank">Association of Corporate Treasurers - Duration Calculator</a></li>
            <li><a href="https://financeformulas.net/Duration.html" target="_blank">Finance Formulas - Duration and Bond Pricing Calculators</a></li>
            <li><a href="https://www.fanniemae.com/about-us/investor-relations/monthly-summary" target="_blank">Fannie Mae - Monthly Summary Reports (incluindo Duration Gap)</a></li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="info">
        <h3>Leitura Recomendada sobre o Caso SVB</h3>
        <p>Para um entendimento mais aprofundado do caso do Silicon Valley Bank e suas implicações para a regulação do risco
        de taxas de juros, recomendamos fortemente a leitura do artigo "Duration Gap Disclosure: A Modest Proposal to Prevent Another SVB"
        de Deborah J. Lucas e Edward L. Golding (2023), que analisa em detalhe as causas da quebra e propõe medidas regulatórias
        para evitar casos semelhantes no futuro.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Função principal para executar o aplicativo
def main():
    # Criando a barra lateral para navegação
    page = create_sidebar()
    
    # Renderizando a página selecionada
    if page == "📝 Introdução":
        intro_page()
    elif page == "🏦 SVB: O Caso de Estudo":
        svb_case_page()
    elif page == "📊 Gap de Reprecificação":
        repricing_gap_page()
    elif page == "⏱️ Duration & DV01/PVBP":
        duration_page()
    elif page == "🔥 Stress Testing":
        stress_testing_page()
    elif page == "⚖️ Gestão Ativo-Passivo (ALM)":
        alm_page()
    elif page == "📚 Referências":
        references_page()

# Executando o aplicativo
if __name__ == "__main__":
    main()            
    
    
    





# Footer
st.divider()
st.markdown("<p style='text-align: center; color: #777; font-size: 0.8em;'>© 2025 Estudos de Caso sobre Gestão de Risco de Taxas de Juros | Desenvolvido com finalidade pedagógica</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #777; font-size: 0.8em;'>Prof. José Américo – Coppead</p>", unsafe_allow_html=True)