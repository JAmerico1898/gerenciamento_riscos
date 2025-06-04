import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import base64
from io import BytesIO
from sklearn.metrics import confusion_matrix, roc_curve, auc, classification_report, log_loss, precision_score, recall_score, f1_score
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="Modelando o Risco de Crédito",
    page_icon="💰",
    layout="wide"
)

# Título e descrição da aplicação
st.title("Ferramenta Interativa de Modelagem do Risco de Crédito")
st.markdown("""
Esta ferramenta demonstra como funciona a modelagem de risco de crédito utilizando regressão logística.
Você pode selecionar variáveis, treinar um modelo e analisar potenciais tomadores de empréstimo.
""")

# Função para carregar dados
@st.cache_data
def load_data():
    # Em uma aplicação real, substitua estes pelos caminhos dos arquivos reais
    try:
        training_sample = pd.read_csv('training_sample.csv')
        testing_sample = pd.read_csv('testing_sample.csv')
        return training_sample, testing_sample
    except:
        # Dados de demonstração para quando os arquivos não estiverem disponíveis
        st.warning("Usando dados de demonstração. Em produção, conecte-se a conjuntos de dados reais.")
        # Criar dados sintéticos de treinamento
        np.random.seed(42)
        n_training = 250000
        n_testing = 20000
        
        # Características
        loan_amnt = np.random.uniform(1000, 35000, n_training)
        int_rate = np.random.uniform(5, 25, n_training)
        annual_inc = np.random.uniform(20000, 150000, n_training)
        dti = np.random.uniform(0, 40, n_training)  # relação dívida-renda
        delinq_2yrs = np.random.poisson(0.5, n_training)
        fico_range_low = np.random.normal(700, 50, n_training).astype(int)
        
        # Variáveis dummy de grau (codificação one-hot)
        grade_probs = [0.30, 0.25, 0.20, 0.15, 0.05, 0.03, 0.02]  # Distribuição de probabilidade
        grades = np.random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'], n_training, p=grade_probs)
        grade_A = (grades == 'A').astype(int)
        grade_B = (grades == 'B').astype(int)
        grade_C = (grades == 'C').astype(int)
        grade_D = (grades == 'D').astype(int)
        grade_E = (grades == 'E').astype(int)
        grade_F = (grades == 'F').astype(int)
        grade_G = (grades == 'G').astype(int)
        
        # Gerar loan_status (variável alvo) com relação realista com as características
        # FICO mais alto, valor do empréstimo menor, taxa de juros menor, renda maior = menor probabilidade de inadimplência
        logit = -5 + 0.00005 * loan_amnt + 0.1 * int_rate - 0.00001 * annual_inc + 0.05 * dti + \
                0.5 * delinq_2yrs - 0.01 * fico_range_low + 0 * grade_A + 0.2 * grade_B + \
                0.5 * grade_C + 0.8 * grade_D + 1.1 * grade_E + 1.4 * grade_F + 1.7 * grade_G
        
        prob_default = 1 / (1 + np.exp(-logit))
        loan_status = np.random.binomial(1, prob_default)
        
        # Garantir proporção de 80% bem-sucedidos, 20% inadimplentes reamostrando
        successful_indices = np.where(loan_status == 0)[0]
        default_indices = np.where(loan_status == 1)[0]
        
        target_successful_count = int(0.8 * n_training)
        target_default_count = n_training - target_successful_count
        
        if len(successful_indices) > target_successful_count:
            successful_indices = np.random.choice(successful_indices, target_successful_count, replace=False)
        else:
            # Precisa criar mais empréstimos bem-sucedidos
            additional_needed = target_successful_count - len(successful_indices)
            loan_status[np.random.choice(default_indices, additional_needed, replace=False)] = 0
            successful_indices = np.where(loan_status == 0)[0]
            default_indices = np.where(loan_status == 1)[0]
        
        if len(default_indices) > target_default_count:
            default_indices = np.random.choice(default_indices, target_default_count, replace=False)
        else:
            # Precisa criar mais inadimplentes
            additional_needed = target_default_count - len(default_indices)
            loan_status[np.random.choice(successful_indices, additional_needed, replace=False)] = 1
        
        # Criar DataFrame
        training_sample = pd.DataFrame({
            'id': range(1, n_training + 1),
            'loan_amnt': loan_amnt,
            'int_rate': int_rate,
            'annual_inc': annual_inc,
            'dti': dti,
            'delinq_2yrs': delinq_2yrs,
            'fico_range_low': fico_range_low,
            'grade_A': grade_A,
            'grade_B': grade_B,
            'grade_C': grade_C,
            'grade_D': grade_D,
            'grade_E': grade_E,
            'grade_F': grade_F,
            'grade_G': grade_G,
            'loan_status': loan_status
        })
        
        # Criar amostra de teste (estrutura similar mas sem loan_status)
        # Usar as mesmas distribuições mas amostras aleatórias diferentes
        loan_amnt_test = np.random.uniform(1000, 35000, n_testing)
        int_rate_test = np.random.uniform(5, 25, n_testing)
        annual_inc_test = np.random.uniform(20000, 150000, n_testing)
        dti_test = np.random.uniform(0, 40, n_testing)
        delinq_2yrs_test = np.random.poisson(0.5, n_testing)
        fico_range_low_test = np.random.normal(700, 50, n_testing).astype(int)
        
        grades_test = np.random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'], n_testing, p=grade_probs)
        grade_A_test = (grades_test == 'A').astype(int)
        grade_B_test = (grades_test == 'B').astype(int)
        grade_C_test = (grades_test == 'C').astype(int)
        grade_D_test = (grades_test == 'D').astype(int)
        grade_E_test = (grades_test == 'E').astype(int)
        grade_F_test = (grades_test == 'F').astype(int)
        grade_G_test = (grades_test == 'G').astype(int)
        
        testing_sample = pd.DataFrame({
            'id': range(1, n_testing + 1),
            'loan_amnt': loan_amnt_test,
            'int_rate': int_rate_test,
            'annual_inc': annual_inc_test,
            'dti': dti_test,
            'delinq_2yrs': delinq_2yrs_test,
            'fico_range_low': fico_range_low_test,
            'grade_A': grade_A_test,
            'grade_B': grade_B_test,
            'grade_C': grade_C_test,
            'grade_D': grade_D_test,
            'grade_E': grade_E_test,
            'grade_F': grade_F_test,
            'grade_G': grade_G_test
        })
        
        return training_sample, testing_sample

# Carregar dados
training_sample, testing_sample = load_data()

# Exibir visão geral dos dados
with st.expander("Visão Geral dos Dados"):
    st.subheader("Base de Treinamento")
    st.write(f"Dimensões: {training_sample.shape}")
    
    # Estilização do DataFrame usando Pandas
    def style_table(df):
        df = df.reset_index(drop=True)

        # Criar lista de nomes de colunas para as colunas 2 a 8
        columns_to_format = df.columns[2:8]

        return (
            df.style
            .set_table_styles(
                [{
                    'selector': 'thead th',
                    'props': [('font-weight', 'bold'),
                            ('border-style', 'solid'),
                            ('border-width', '0px 0px 2px 0px'),
                            ('border-color', 'black')]
                }, {
                    'selector': 'thead th:not(:first-child)',
                    'props': [('text-align', 'center')]  # Centralizar todos os cabeçalhos exceto o primeiro
                }, {
                    'selector': 'thead th:last-child',
                    'props': [('color', 'black')]  # Fazer o cabeçalho da última coluna preto
                }, {
                    'selector': 'td',
                    'props': [('border-style', 'solid'),
                            ('border-width', '0px 0px 1px 0px'),
                            ('border-color', 'black'),
                            ('text-align', 'center')]
                }, {
                    'selector': 'th',
                    'props': [('border-style', 'solid'),
                            ('border-width', '0px 0px 1px 0px'),
                            ('border-color', 'black'),
                            ('text-align', 'left')]
                }]
            )
            .set_properties(**{'padding': '2px', 'font-size': '15px'})
            .format({col: "{:.2f}" for col in columns_to_format})  # Formatar colunas para 2 casas decimais
        )

    # Exibindo no Streamlit
    def main():
        styled_html = style_table(training_sample.head()).to_html(index=False, escape=False)
        centered_html = f'''
        <div style="display: flex; justify-content: left;">
            {styled_html}
        '''  # Fechar corretamente a tag div
        st.markdown(centered_html, unsafe_allow_html=True)

    if __name__ == '__main__':
        main()
    
    
    st.subheader("Base de Validação")
    st.write(f"Dimensões: {testing_sample.shape}")

    # Estilização do DataFrame usando Pandas
    def style_table(df):
        df = df.reset_index(drop=True)

        # Criar lista de nomes de colunas para as colunas 2 a 8
        columns_to_format = df.columns[2:8]

        return (
            df.style
            .set_table_styles(
                [{
                    'selector': 'thead th',
                    'props': [('font-weight', 'bold'),
                            ('border-style', 'solid'),
                            ('border-width', '0px 0px 2px 0px'),
                            ('border-color', 'black')]
                }, {
                    'selector': 'thead th:not(:first-child)',
                    'props': [('text-align', 'center')]  # Centralizar todos os cabeçalhos exceto o primeiro
                }, {
                    'selector': 'thead th:last-child',
                    'props': [('color', 'black')]  # Fazer o cabeçalho da última coluna preto
                }, {
                    'selector': 'td',
                    'props': [('border-style', 'solid'),
                            ('border-width', '0px 0px 1px 0px'),
                            ('border-color', 'black'),
                            ('text-align', 'center')]
                }, {
                    'selector': 'th',
                    'props': [('border-style', 'solid'),
                            ('border-width', '0px 0px 1px 0px'),
                            ('border-color', 'black'),
                            ('text-align', 'left')]
                }]
            )
            .set_properties(**{'padding': '2px', 'font-size': '15px'})
            .format({col: "{:.2f}" for col in columns_to_format})  # Formatar colunas para 2 casas decimais
        )

    # Exibindo no Streamlit
    def main():
        styled_html = style_table(testing_sample.head()).to_html(index=False, escape=False)
        centered_html = f'''
        <div style="display: flex; justify-content: left;">
            {styled_html}
        '''  # Fechar corretamente a tag div
        st.markdown(centered_html, unsafe_allow_html=True)

    if __name__ == '__main__':
        main()

    
    # Exibir distribuição de classes
    st.subheader("Distribuição de Classes nos Dados de Treinamento")
    fig, ax = plt.subplots(figsize=(6, 4))
    class_counts = training_sample['loan_status'].value_counts()
    ax.bar(['Pago (0)', 'Inadimplente (1)'], class_counts.values)
    ax.set_ylabel('Contagem')
    ax.set_title('Distribuição do Status do Empréstimo')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for i, v in enumerate(class_counts.values):
        ax.text(i, v + 3000, f"{v} ({v/len(training_sample)*100:.1f}%)", ha='center')
    col1, col2, col3 = st.columns([1, 5, 1])
    with col2:
        st.pyplot(fig)        

# Seleção de características
st.header("1. Seleção de Variáveis")
st.write("Selecione as variáveis que deseja incluir em seu modelo de regressão logística:")

# Obter características disponíveis (excluindo id e variável alvo)
available_features = [col for col in training_sample.columns 
                     if col not in ['id', 'loan_status']]

# Agrupar características por categoria para melhor organização
numerical_features = ['loan_amnt', 'int_rate', 'annual_inc', 'dti', 'delinq_2yrs', 'fico_range_low']
categorical_features = [col for col in available_features if col.startswith('grade_')]

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Variáveis Numéricas")
        selected_numerical = []
        for feature in numerical_features:
            if st.checkbox(f"{feature}", value=True):
                selected_numerical.append(feature)
    
    with col2:
        st.subheader("Variáveis Categóricas")
        selected_categorical = []
        for feature in categorical_features:
            if st.checkbox(f"{feature}", value=True):
                selected_categorical.append(feature)

selected_features = selected_numerical + selected_categorical

if not selected_features:
    st.warning("Por favor, selecione ao menos uma variável para construir o modelo.")
else:
    st.success(f"Selecionadas {len(selected_features)} variáveis: {', '.join(selected_features)}")

# Treinamento do modelo
st.header("2. Treinamento do Modelo")

if st.button("Treinar Modelo de Regressão Logística", key=1, disabled=not selected_features):
    if not selected_features:
        st.error("Nenhuma variável selecionada. Por favor, selecione ao menos uma variável.")
    else:
        with st.spinner("Treinando o modelo..."):
            # Preparar dados
            X = training_sample[selected_features]
            y = training_sample['loan_status']
            
            # Divisão treino-teste
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=42, stratify=y
            )
            
            st.session_state.X_train = X_train
            st.session_state.X_test = X_test
            st.session_state.y_train = y_train
            st.session_state.y_test = y_test
            
            # Ajustar modelo de regressão logística
            model = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1)
            model.fit(X_train, y_train)
            st.session_state.model = model
            
            # Previsões
            y_pred_proba = model.predict_proba(X_test)[:, 1]
            y_pred = model.predict(X_test)
            st.session_state.y_pred = y_pred
            st.session_state.y_pred_proba = y_pred_proba
            
            # Usar diretamente LogisticRegression do sklearn
            # Isso evita o processo problemático de ajuste do statsmodels
            st.session_state.model_coef = model.coef_[0]
            st.session_state.model_intercept = model.intercept_[0]
            
            # Criar estatísticas de resumo personalizadas
            from sklearn.metrics import log_loss
            train_pred_proba = model.predict_proba(X_train)[:, 1]
            train_log_loss = log_loss(y_train, train_pred_proba)
            
            # Armazenar para exibição posterior
            st.session_state.custom_summary = {
                'features': selected_features,
                'coefficients': model.coef_[0],
                'intercept': model.intercept_[0],
                'train_log_loss': train_log_loss,
                'train_accuracy': model.score(X_train, y_train),
                'test_accuracy': model.score(X_test, y_test)
            }
            
            # Calcular equação para exibição
            coefficients = model.coef_[0]
            intercept = model.intercept_[0]
            st.session_state.coefficients = coefficients
            st.session_state.intercept = intercept
            st.session_state.selected_features = selected_features
            
            st.success("Modelo treinado com sucesso!")
            st.session_state.model_trained = True
            
            # Armazenar informações das características para uso posterior com amostra de teste
            st.session_state.original_features = selected_features

# Exibição de resultados - mostrar apenas se o modelo foi treinado
if 'model_trained' in st.session_state and st.session_state.model_trained:
    st.header("Resultados do Modelo")
    
    # Adicionar seletor de limiar no topo da seção de resultados
    st.subheader("1. Configuração do Limiar de Decisão")
    with st.container():
        st.markdown("""
        **Configure o limiar de decisão para aprovação/rejeição de empréstimos:**
        - Empréstimos com probabilidade prevista **abaixo** deste limiar serão **aprovados**
        - Empréstimos com probabilidade prevista **acima** deste limiar serão **rejeitados**
        """)
        
        # Slider do limiar
        decision_threshold = st.slider(
            "Limiar de Decisão (Probabilidade de Inadimplência)",
            min_value=0.1,
            max_value=0.9,
            value=0.5,
            step=0.01,
            help="Ajuste este limiar com base em seu apetite ao risco. Valores menores aprovam mais empréstimos mas aumentam o risco de inadimplência."
        )
        
        # Armazenar limiar no session state
        st.session_state.decision_threshold = decision_threshold
        
        # Mostrar impacto da mudança de limiar
        col1, col2, col3 = st.columns(3)
        
        with col1:
            approved_at_threshold = (st.session_state.y_pred_proba < decision_threshold).sum()
            st.metric(
                "Empréstimos que seriam Aprovados", 
                f"{approved_at_threshold} ({approved_at_threshold/len(st.session_state.y_pred_proba)*100:.1f}%)",
                help="Número de empréstimos do conjunto de teste que seriam aprovados neste limiar"
            )
        
        with col2:
            rejected_at_threshold = (st.session_state.y_pred_proba >= decision_threshold).sum()
            st.metric(
                "Empréstimos que seriam Rejeitados", 
                f"{rejected_at_threshold} ({rejected_at_threshold/len(st.session_state.y_pred_proba)*100:.1f}%)",
                help="Número de empréstimos do conjunto de teste que seriam rejeitados neste limiar"
            )
            
        with col3:
            # Calcular precisão e recall neste limiar
            y_pred_at_threshold = (st.session_state.y_pred_proba >= decision_threshold).astype(int)
            if y_pred_at_threshold.sum() > 0:
                precision_at_threshold = precision_score(st.session_state.y_test, y_pred_at_threshold)
                st.metric(
                    "Precisão neste Limiar", 
                    f"{precision_at_threshold:.3f}",
                    help="Dos empréstimos previstos como inadimplentes, qual porcentagem realmente ficou inadimplente"
                )
            else:
                st.metric("Precisão neste Limiar", "N/A", help="Nenhum empréstimo previsto como inadimplente neste limiar")

    
    # 1. Curva de Regressão Logística
    st.subheader("2. Regressão Logística - Curva-S")
    with st.container():
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Ordenar probabilidades e valores reais para plotagem
        sorted_indices = np.argsort(st.session_state.y_pred_proba)
        sorted_probs = st.session_state.y_pred_proba[sorted_indices]
        sorted_actuals = st.session_state.y_test.values[sorted_indices]
        
        # Plotar a curva logística
        ax.plot(range(len(sorted_probs)), sorted_probs, 'b-', linewidth=2)
        
        # Adicionar observações reais como pontos (com jitter para visibilidade)
        y_jittered = sorted_actuals + np.random.normal(0, 0.02, len(sorted_actuals))
        ax.scatter(range(len(sorted_probs)), y_jittered, c='r', alpha=0.1, s=1)
        
        ax.set_xlabel('Observações (ordenadas pela probabilidade prevista)')
        ax.set_ylabel('Probabilidade de Inadimplência')
        ax.set_title('Regressão Logística - Curva-S')
        ax.grid(True, alpha=0.3)
        
        # Adicionar linha horizontal no limiar definido pelo usuário
        ax.axhline(y=decision_threshold, color='green', linestyle='--', alpha=0.7, linewidth=2)
        ax.text(len(sorted_probs)*0.02, decision_threshold + 0.02, f'Limiar de Decisão (p={decision_threshold:.2f})', color='green', fontweight='bold')

        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.pyplot(fig)        
        
        st.markdown(f"""
        **Interpretação:** A curva em S mostra como a probabilidade de inadimplência prevista pelo modelo varia entre todas as observações.
        - Linha azul: Probabilidades previstas (ordenadas da menor para a maior)
        - Pontos vermelhos: Resultados reais (0=pago, 1=inadimplente)
        - Linha verde: Limiar de decisão (definido pelo usuário: {decision_threshold:.2f})
        
        Com o limiar atual de {decision_threshold:.2f}:
        - Empréstimos com probabilidade < {decision_threshold:.2f} serão **aprovados**
        - Empréstimos com probabilidade ≥ {decision_threshold:.2f} serão **rejeitados**
        
        Em um bom modelo, é desejável que a maioria dos pontos esteja agrupada no canto inferior esquerdo 
        (pagamentos corretamente previstos) e no canto superior direito (inadimplências corretamente previstas).
        """)
    
    # 2. Curva ROC
    st.subheader("3. Curva ROC")
    with st.container():
        fpr, tpr, thresholds = roc_curve(st.session_state.y_test, st.session_state.y_pred_proba)
        roc_auc = auc(fpr, tpr)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(fpr, tpr, 'b-', linewidth=2, label=f'Curva ROC (AUC = {roc_auc:.3f})')
        ax.plot([0, 1], [0, 1], 'r--', linewidth=1, label='Classificador Aleatório')
        ax.set_xlabel('Taxa de Falsos Positivos (1 - Especificidade)')
        ax.set_ylabel('Taxa de Verdadeiros Positivos (Sensibilidade)')
        ax.set_title('Curva ROC (Receiver Operating Characteristic)')
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3)
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.pyplot(fig)        
        
        st.metric("Score AUC", f"{roc_auc:.3f}")
        st.markdown(f"""
        **Interpretação:** A curva ROC mostra o trade-off entre sensibilidade e especificidade.
        - AUC (Área Sob a Curva): {roc_auc:.3f} (quanto maior melhor, 1.0 é perfeito, 0.5 é aleatório)

        Quanto mais próxima a curva estiver do canto superior esquerdo, melhor é a capacidade do modelo de
        diferenciar entre pagamentos e inadimplências. Uma AUC de:

        * 0,9 a 1,0: Discriminação excelente
        * 0,8 a 0,9: Discriminação boa
        * 0,7 a 0,8: Discriminação razoável
        * 0,6 a 0,7: Discriminação fraca
        * 0,5 a 0,6: Discriminação falha
        """)
    
    # 3. Matriz de Confusão (atualizada para usar limiar do usuário)
    st.subheader("4. Matriz de Confusão")
    with st.container():
        # Recalcular previsões usando limiar definido pelo usuário
        y_pred_user_threshold = (st.session_state.y_pred_proba >= decision_threshold).astype(int)
        cm = confusion_matrix(st.session_state.y_test, y_pred_user_threshold)
        
        # Calcular métricas
        tn, fp, fn, tp = cm.ravel()
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                    xticklabels=['Previsto Pago', 'Previsto Inadimplente'],
                    yticklabels=['Realmente Pago', 'Realmente Inadimplente'])
        ax.set_xlabel('Rótulo Previsto')
        ax.set_ylabel('Rótulo Verdadeiro')
        ax.set_title(f'Matriz de Confusão (Limiar = {decision_threshold:.2f})')
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.pyplot(fig)        
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Métricas no Limiar {decision_threshold}:**
            - **Acurácia:** {accuracy:.3f}
            - **Precisão:** {precision:.3f}
            - **Recall (Sensibilidade):** {recall:.3f}
            - **Especificidade:** {specificity:.3f}
            - **F1 Score:** {f1:.3f}
            """)
            
        with col2:
            st.markdown("""
            **Definições:**
            - **Verdadeiros Negativos (TN):** Pagamentos corretamente previstos
            - **Falsos Positivos (FP):** Inadimplências incorretamente previstas
            - **Falsos Negativos (FN):** Pagamentos incorretamente previstos
            - **Verdadeiros Positivos (TP):** Inadimplências corretamente previstas
            - **Precisão:** Proporção de inadimplências previstas que eram inadimplências reais
            - **Recall:** Proporção de inadimplências reais que foram corretamente previstas
            """)

        # Explicação das métricas
        st.markdown(f"""
        ### 📊 Explicação das Métricas (Limiar = {decision_threshold:.2f}):
        - **Acurácia**: Proporção total de previsões corretas
        - **Precisão**: Dos casos previstos como inadimplentes, quantos realmente são?
        - **Recall (Sensibilidade)**: Dos casos realmente inadimplentes, quantos foram identificados?
        - **Especificidade**: Dos casos realmente bons, quantos foram identificados corretamente?
        
        **Impacto do Limiar:**
        - Limiar mais **baixo**: Aprova mais empréstimos, mas aumenta risco de inadimplência
        - Limiar mais **alto**: Rejeita mais empréstimos, mas reduz risco de inadimplência
        """)
    
    # 4. Resumo do Modelo (Versão personalizada já que statsmodels está causando problemas)
    st.subheader("5. Resumo das Estatísticas de Regressão")
    with st.container():
        if 'custom_summary' in st.session_state:
            summary = st.session_state.custom_summary
            
            # Criar DataFrame para exibição de coeficientes
            coef_df = pd.DataFrame({
                'Variável': summary['features'],
                'Coeficiente': summary['coefficients'],
                'Razão de Chances': np.exp(summary['coefficients'])
            })
            
            # Exibir informações do modelo
            st.markdown("### Informações do Modelo")
            st.markdown(f"""
            - **Número de observações:** {len(st.session_state.X_train)}
            - **Número de preditores:** {len(summary['features'])}
            - **Intercepto:** {summary['intercept']:.3f}
            - **Log Loss de Treinamento:** {summary['train_log_loss']:.3f}
            - **Acurácia de Treinamento:** {summary['train_accuracy']:.3f}
            - **Acurácia de Teste:** {summary['test_accuracy']:.3f}
            """)
            
            st.markdown("### Coeficientes")
            
            # Estilização do DataFrame usando Pandas
            def style_table(df):
                df = df.reset_index(drop=True)
                
                return df.style.set_table_styles(
                    [{
                        'selector': 'thead th',
                        'props': [('font-weight', 'bold'),
                                ('border-style', 'solid'),
                                ('border-width', '0px 0px 2px 0px'),
                                ('border-color', 'black'),]
                    }, {
                        'selector': 'thead th:not(:first-child)',
                        'props': [('text-align', 'center')]  # Centralizar todos os cabeçalhos exceto o primeiro
                    }, {
                        'selector': 'thead th:last-child',
                        'props': [('color', 'black')]  # Fazer o cabeçalho da última coluna preto
                    }, {
                        'selector': 'td',
                        'props': [('border-style', 'solid'),
                                ('border-width', '0px 0px 1px 0px'),
                                ('border-color', 'black'),
                                ('text-align', 'center')]
                    }, {
                        'selector': 'th',
                        'props': [('border-style', 'solid'),
                                ('border-width', '0px 0px 1px 0px'),
                                ('border-color', 'black'),
                                ('text-align', 'left'),]
                    }]
                ).set_properties(**{'padding': '2px',
                                    'font-size': '15px'})

            # Exibindo no Streamlit
            def main():
                styled_html = style_table(coef_df).to_html(index=False, escape=False)
                centered_html = f'''
                <div style="display: flex; justify-content: left;">
                    {styled_html}
                '''  # Fechar corretamente a tag div
                st.markdown(centered_html, unsafe_allow_html=True)

            if __name__ == '__main__':
                main()
            
            # Adicionar botão de download para resumo
            summary_text = f"""
            Resumo do Modelo de Regressão Logística para Risco de Crédito
            ============================================================
            
            Informações do Modelo:
            ----------------------
            Número de observações: {len(st.session_state.X_train)}
            Número de preditores: {len(summary['features'])}
            Intercepto: {summary['intercept']}
            Log Loss de Treinamento: {summary['train_log_loss']}
            Acurácia de Treinamento: {summary['train_accuracy']}
            Acurácia de Teste: {summary['test_accuracy']}
            
            Coeficientes:
            ------------
            """
            
            for feature, coef, odds in zip(summary['features'], summary['coefficients'], np.exp(summary['coefficients'])):
                summary_text += f"{feature}: {coef:.6f} (razão de chances: {odds:.6f})\n"
            
            st.download_button(
                label="Baixar Resumo como Texto",
                data=summary_text,
                file_name="resumo_regressao_logistica.txt",
                mime="text/plain"
            )
        else:
            st.error("Estatísticas de resumo do modelo não estão disponíveis. Por favor, treine o modelo primeiro.")
    
    # 5. Explicação das estatísticas
    st.subheader("6. Interpretação das Estatísticas")
    with st.container():
        st.markdown("""
        **Principais estatísticas e sua interpretação:**
        
        **Coeficiente (coef):** 
        - Indica a mudança no log-odds de inadimplência para um aumento de uma unidade no preditor.
        - Coeficiente positivo: À medida que o preditor aumenta, a probabilidade de inadimplência aumenta.
        - Coeficiente negativo: À medida que o preditor aumenta, a probabilidade de inadimplência diminui.
        
        **Razão de Chances:**
        - O coeficiente exponenciado (e^coef).
        - Representa como as chances de inadimplência se multiplicam quando o preditor aumenta em uma unidade.
        - Razão de Chances > 1: A variável aumenta o risco de inadimplência.
        - Razão de Chances < 1: A variável diminui o risco de inadimplência.
        
        **Log Loss:**
        - Mede quão bem as probabilidades previstas do modelo correspondem aos resultados reais.
        - Valores menores indicam melhor ajuste (menos incerteza).
        
        **Acurácia:**
        - Proporção de previsões corretas (tanto empréstimos pagos quanto inadimplentes).
        - Valores maiores indicam melhor desempenho preditivo geral.
        
        **Interpretando Efeitos das Variáveis:**
        - A magnitude dos coeficientes indica a força do efeito.
        - Variáveis categóricas (como grau) mostram o efeito relativo a uma categoria de referência.
        - Variáveis com coeficientes absolutos maiores têm efeitos mais fortes na probabilidade de inadimplência.
        """)
    
    # 6. Equação de Regressão Logística
    st.subheader("7. Equação de Regressão Logística")
    with st.container():
        # Formatar a equação com melhor espaçamento e alinhamento
        st.markdown("""
        A equação de regressão logística (forma log-odds):
        """)
        
        # Construir equação dinamicamente usando coeficientes reais do modelo
        intercept_term = f"{st.session_state.intercept:.4f}"
        
        # Criar versão em texto limpa
        text_equation = f"log(P(Inadimplência)/(1-P(Inadimplência))) = {intercept_term}"
        for feature, coef in zip(st.session_state.selected_features, st.session_state.coefficients):
            if coef >= 0:
                text_equation += f" + {coef:.4f} × {feature}"
            else:
                text_equation += f" {coef:.4f} × {feature}"
        
        st.code(text_equation, language=None)

        # Equação de probabilidade com melhor formatação
        st.markdown("""
        **Probabilidade de Inadimplência:**
        
        $\\large P(\\text{Inadimplência}) = \\frac{1}{1 + e^{-z}}$
        
        Onde $z$ é a equação log-odds acima.
        """)
        
        # Tabela de interpretação de coeficientes
        st.subheader("Interpretação dos Coeficientes")
        
        coef_df = pd.DataFrame({
            'Variável': st.session_state.selected_features,
            'Coeficiente': st.session_state.coefficients,
            'Razão de Chances': np.exp(st.session_state.coefficients)
        })
        
        # Adicionar interpretação
        def get_interpretation(feature, coef, odds_ratio):
            if coef > 0:
                return f"Um aumento de uma unidade em {feature} multiplica as chances de inadimplência por {odds_ratio:.3f} (aumenta em {(odds_ratio-1)*100:.1f}%)"
            else:
                return f"Um aumento de uma unidade em {feature} multiplica as chances de inadimplência por {odds_ratio:.3f} (diminui em {(1-odds_ratio)*100:.1f}%)"
        
        coef_df['Interpretação'] = [
            get_interpretation(feature, coef, odds_ratio) 
            for feature, coef, odds_ratio in zip(
                coef_df['Variável'], coef_df['Coeficiente'], coef_df['Razão de Chances']
            )
        ]
        
        # Estilização do DataFrame usando Pandas
        def style_table(df):
            df = df.reset_index(drop=True)
            
            return df.style.set_table_styles(
                [{
                    'selector': 'thead th',
                    'props': [('font-weight', 'bold'),
                            ('border-style', 'solid'),
                            ('border-width', '0px 0px 2px 0px'),
                            ('border-color', 'black'),]
                }, {
                    'selector': 'thead th:not(:first-child)',
                    'props': [('text-align', 'center')]  # Centralizar todos os cabeçalhos exceto o primeiro
                }, {
                    'selector': 'thead th:last-child',
                    'props': [('color', 'black')]  # Fazer o cabeçalho da última coluna preto
                }, {
                    'selector': 'td',
                    'props': [('border-style', 'solid'),
                            ('border-width', '0px 0px 1px 0px'),
                            ('border-color', 'black'),
                            ('text-align', 'center')]
                }, {
                    'selector': 'th',
                    'props': [('border-style', 'solid'),
                            ('border-width', '0px 0px 1px 0px'),
                            ('border-color', 'black'),
                            ('text-align', 'left'),]
                }]
            ).set_properties(**{'padding': '2px',
                                'font-size': '15px'})

        # Exibindo no Streamlit
        def main():
            styled_html = style_table(coef_df).to_html(index=False, escape=False)
            centered_html = f'''
            <div style="display: flex; justify-content: left;">
                {styled_html}
            '''  # Fechar corretamente a tag div
            st.markdown(centered_html, unsafe_allow_html=True)

        if __name__ == '__main__':
            main()                
        

# Previsão na Amostra de Teste
if 'model_trained' in st.session_state and st.session_state.model_trained:
    st.header("Analisar Potenciais Tomadores de Empréstimo")
    
    st.write("""
    Agora você pode analisar potenciais tomadores de empréstimo usando o modelo treinado.
    O modelo usará as mesmas variáveis que você selecionou para treinamento.
    """)
    
    # Verificar se as variáveis necessárias existem na amostra de teste
    missing_features = [f for f in st.session_state.original_features if f not in testing_sample.columns]
    
    if missing_features:
        st.error(f"A amostra de teste está faltando variáveis necessárias: {', '.join(missing_features)}")
    else:
        if st.button("Analisar Potenciais Tomadores de Empréstimo", key=2):
            with st.spinner("Analisando potenciais tomadores de empréstimo..."):
                # Preparar dados de teste usando as mesmas variáveis
                X_potential = testing_sample[st.session_state.original_features]
                
                # Fazer previsões
                potential_proba = st.session_state.model.predict_proba(X_potential)[:, 1]

                # Obter limiar do usuário
                user_threshold = st.session_state.get('decision_threshold')
                potential_pred = (potential_proba >= user_threshold).astype(int)  # Usar limiar do usuário
                
                # Adicionar previsões à amostra de teste
                results_df = testing_sample.copy()
                results_df['probabilidade_prevista'] = potential_proba
                results_df['status_previsto'] = potential_pred
                
                # Armazenar previsões para comparação posterior
                st.session_state.prediction_results = results_df
                
                # Exibir resultados
                st.subheader("Resultados das Previsões")
                
                # Estatísticas resumidas
                approved_count = (potential_pred == 0).sum()
                rejected_count = (potential_pred == 1).sum()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Empréstimos Aprovados", f"{approved_count} ({approved_count/len(potential_pred)*100:.1f}%)")
                with col2:
                    st.metric("Empréstimos Rejeitados", f"{rejected_count} ({rejected_count/len(potential_pred)*100:.1f}%)")
                
                # Distribuição de probabilidades previstas
                st.subheader("Distribuição das Probabilidades de Inadimplência")
                fig, ax = plt.subplots(figsize=(10, 6))
                
                sns.histplot(potential_proba, bins=50, kde=True, ax=ax)
                ax.axvline(x=decision_threshold, color='red', linestyle='--')
                ax.text(decision_threshold+0.02, ax.get_ylim()[1]*0.9, f'Limiar de Decisão ({decision_threshold:.2f})', color='red')
                ax.set_xlabel('Probabilidade Prevista de Inadimplência')
                ax.set_ylabel('Contagem')
                ax.set_title('Distribuição das Probabilidades Previstas de Inadimplência')
                
                col1, col2, col3 = st.columns([1, 6, 1])
                with col2:
                    st.pyplot(fig)        
                
                # Exibir tabela de resultados
                st.subheader("Resultados Detalhados")
                st.dataframe(results_df.sort_values('probabilidade_prevista', ascending=False))
                
                # Opção de download
                csv = results_df.to_csv(index=False)
                st.download_button(
                    label="Baixar Resultados como CSV",
                    data=csv,
                    file_name='previsoes_potenciais_tomadores.csv',
                    mime='text/csv',
                )
                
                # Análise por nível de risco
                st.subheader("Análise por Nível de Risco")
                
                # Criar níveis de risco
                bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
                labels = ['Risco Muito Baixo', 'Risco Baixo', 'Risco Moderado', 'Risco Alto', 'Risco Muito Alto']
                results_df['nivel_risco'] = pd.cut(results_df['probabilidade_prevista'], bins=bins, labels=labels)
                
                # Contar por nível
                tier_counts = results_df['nivel_risco'].value_counts().sort_index()
                
                # Exibir como gráfico de barras
                fig, ax = plt.subplots(figsize=(10, 6))
                tier_counts.plot(kind='bar', ax=ax, color=plt.cm.RdYlGn_r(np.linspace(0, 1, len(labels))))
                ax.set_xlabel('Nível de Risco')
                ax.set_ylabel('Número de Potenciais Tomadores de Empréstimo')
                ax.set_title('Distribuição de Potenciais Tomadores por Nível de Risco')
                
                for i, v in enumerate(tier_counts):
                    ax.text(i, v + 5, f"{v} ({v/len(results_df)*100:.1f}%)", ha='center')
                
                col1, col2, col3 = st.columns([1, 6, 1])
                with col2:
                    st.pyplot(fig)        

    # Comparar previsões com resultados reais
    st.header("Comparar Previsões com Resultados Reais")
    
    st.write("""
    Esta seção compara as previsões do modelo com os resultados reais dos empréstimos
    do arquivo testing_sample_true.csv.
    """)
    
    # Função para carregar os dados verdadeiros de teste
    @st.cache_data
    def load_true_testing_data():
        try:
            # Tentar carregar o arquivo real
            testing_sample_true = pd.read_csv('testing_sample_true.csv')
            return testing_sample_true
        except:
            # Criar dados sintéticos de verdade para demonstração
            st.warning("Usando dados sintéticos de verdade. Em produção, conecte-se ao testing_sample_true.csv real")
            if 'prediction_results' in st.session_state:
                # Usar IDs dos resultados de previsão
                ids = st.session_state.prediction_results['id'].values
                n = len(ids)
                
                # Gerar verdade sintética correlacionada com nossas previsões
                # mas não perfeitamente correspondente (taxa de concordância de 80%)
                if 'model' in st.session_state:
                    # Para demonstração: fazer verdade sintética parcialmente correlacionada com previsões do modelo
                    predicted_probs = st.session_state.prediction_results['probabilidade_prevista'].values
                    
                    # Adicionar algum ruído às probabilidades
                    noisy_probs = predicted_probs + np.random.normal(0, 0.15, n)
                    noisy_probs = np.clip(noisy_probs, 0, 1)
                    
                    # Converter para resultados binários
                    synthetic_outcomes = (noisy_probs > 0.5).astype(int)
                else:
                    # Se não há previsões do modelo disponíveis, gerar resultados aleatórios com distribuição realista
                    synthetic_outcomes = np.random.binomial(1, 0.2, n)  # Taxa de inadimplência de 20%
                
                return pd.DataFrame({
                    'id': ids,
                    'loan_status': synthetic_outcomes
                })
    
    # Carregar os resultados verdadeiros
    testing_sample_true = load_true_testing_data()
    
    if 'prediction_results' not in st.session_state:
        st.info("Por favor, execute 'Analisar Potenciais Tomadores de Empréstimo' primeiro para gerar previsões.")
    else:
        # Mesclar previsões com resultados verdadeiros
        comparison_df = st.session_state.prediction_results[['id', 'status_previsto', 'probabilidade_prevista']].merge(
            testing_sample_true[['id', 'loan_status']], 
            on='id',
            how='inner'
        )
        
        if len(comparison_df) == 0:
            st.error("Não foi possível corresponder nenhuma previsão com resultados verdadeiros. Verifique se os IDs correspondem entre os conjuntos de dados.")
        else:
            st.success(f"Correspondência bem-sucedida de {len(comparison_df)} empréstimos entre previsões e resultados reais.")
            
            # Calcular métricas
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
            
            accuracy = accuracy_score(comparison_df['loan_status'], comparison_df['status_previsto'])
            precision = precision_score(comparison_df['loan_status'], comparison_df['status_previsto'])
            recall = recall_score(comparison_df['loan_status'], comparison_df['status_previsto'])
            f1 = f1_score(comparison_df['loan_status'], comparison_df['status_previsto'])
            roc_auc = roc_auc_score(comparison_df['loan_status'], comparison_df['probabilidade_prevista'])
            
            # Exibir métricas
            st.subheader("Desempenho do Modelo nos Dados de Teste")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Acurácia", f"{accuracy:.4f}")
                st.metric("F1 Score", f"{f1:.4f}")
            with col2:
                st.metric("Precisão", f"{precision:.4f}")
                st.metric("ROC-AUC", f"{roc_auc:.4f}")
            with col3:
                st.metric("Recall", f"{recall:.4f}")
            
            # Adicionar explicação das métricas
            with st.expander("Entenda essas métricas"):
                st.markdown("""
                - **Acurácia**: Porcentagem de previsões corretas (tanto empréstimos pagos quanto inadimplentes)
                - **Precisão**: Porcentagem de inadimplências previstas que eram inadimplências reais (menos falsos positivos)
                - **Recall**: Porcentagem de inadimplências reais que foram corretamente previstas (menos falsos negativos)
                - **F1 Score**: Média harmônica de precisão e recall
                - **ROC-AUC**: Área sob a curva ROC, mede a capacidade do modelo de distinguir entre classes
                
                Na modelagem de risco de crédito, diferentes métricas podem ser priorizadas dependendo dos objetivos de negócio:
                - **Precisão** mais alta significa menos empréstimos bons são incorretamente rejeitados
                - **Recall** mais alto significa menos empréstimos ruins são incorretamente aprovados
                """)
            
            # Matriz de confusão
            st.subheader("Matriz de Confusão")
            cm = confusion_matrix(comparison_df['loan_status'], comparison_df['status_previsto'])
            
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                        xticklabels=['Previsto Pago', 'Previsto Inadimplente'],
                        yticklabels=['Realmente Pago', 'Realmente Inadimplente'])
            ax.set_xlabel('Rótulo Previsto')
            ax.set_ylabel('Rótulo Verdadeiro')
            ax.set_title('Matriz de Confusão nos Dados de Teste')
            col1, col2, col3 = st.columns([1, 6, 1])
            with col2:
                st.pyplot(fig)        
            
            # Análise de erros
            st.subheader("Análise de Erros")
            
            # Adicionar categorias de erro
            comparison_df['categoria_resultado'] = 'Desconhecido'
            comparison_df.loc[(comparison_df['status_previsto'] == 0) & (comparison_df['loan_status'] == 0), 'categoria_resultado'] = 'Verdadeiro Negativo (Pagamento Corretamente Previsto)'
            comparison_df.loc[(comparison_df['status_previsto'] == 1) & (comparison_df['loan_status'] == 1), 'categoria_resultado'] = 'Verdadeiro Positivo (Inadimplência Corretamente Prevista)'
            comparison_df.loc[(comparison_df['status_previsto'] == 1) & (comparison_df['loan_status'] == 0), 'categoria_resultado'] = 'Falso Positivo (Inadimplência Incorretamente Prevista)'
            comparison_df.loc[(comparison_df['status_previsto'] == 0) & (comparison_df['loan_status'] == 1), 'categoria_resultado'] = 'Falso Negativo (Pagamento Incorretamente Previsto)'
            
            # Contar por categoria
            result_counts = comparison_df['categoria_resultado'].value_counts()
            
            # Exibir como gráfico de pizza
            fig, ax = plt.subplots(figsize=(10, 8))
            colors = ['#4CAF50', '#2196F3', '#FFC107', '#F44336']
            result_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, colors=colors, textprops={'fontsize': 14})
            ax.set_ylabel('')
            ax.set_title('Distribuição dos Resultados de Previsão')
            col1, col2, col3 = st.columns([1, 6, 1])
            with col2:
                st.pyplot(fig)        
            
            # Curva ROC
            st.subheader("Curva ROC nos Dados de Teste")
            fpr, tpr, _ = roc_curve(comparison_df['loan_status'], comparison_df['probabilidade_prevista'])
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(fpr, tpr, 'b-', linewidth=2, label=f'Curva ROC (AUC = {roc_auc:.3f})')
            ax.plot([0, 1], [0, 1], 'r--', linewidth=1, label='Classificador Aleatório')
            ax.set_xlabel('Taxa de Falsos Positivos (1 - Especificidade)')
            ax.set_ylabel('Taxa de Verdadeiros Positivos (Sensibilidade)')
            ax.set_title('Curva ROC (Receiver Operating Characteristic) nos Dados de Teste')
            ax.legend(loc='lower right')
            ax.grid(True, alpha=0.3)
            col1, col2, col3 = st.columns([1, 6, 1])
            with col2:
                st.pyplot(fig)        
            
            # Análise detalhada de erros - mostrar os principais casos mal classificados
            st.subheader("Principais Casos Mal Classificados")
            
            # Falsos Positivos (erros Tipo I) - empréstimos bons rejeitados
            st.markdown("### Falsos Positivos (Empréstimos bons incorretamente previstos como inadimplentes)")
            fp_df = comparison_df[comparison_df['categoria_resultado'] == 'Falso Positivo (Inadimplência Incorretamente Prevista)'].sort_values('probabilidade_prevista', ascending=False)
            if len(fp_df) > 0:
                st.dataframe(fp_df.head(10))
            else:
                st.info("Nenhum falso positivo encontrado.")
                
            # Falsos Negativos (erros Tipo II) - empréstimos ruins aprovados
            st.markdown("### Falsos Negativos (Empréstimos ruins incorretamente previstos como pagamentos)")
            fn_df = comparison_df[comparison_df['categoria_resultado'] == 'Falso Negativo (Pagamento Incorretamente Previsto)'].sort_values('probabilidade_prevista')
            if len(fn_df) > 0:
                st.dataframe(fn_df.head(10))
            else:
                st.info("Nenhum falso negativo encontrado.")
            
            # Análise de impacto nos negócios
            st.subheader("Análise de Impacto nos Negócios")
            
            # Na modelagem de crédito, falsos negativos (aprovar empréstimos ruins) tipicamente custam mais que
            # falsos positivos (rejeitar empréstimos bons)
            fn_count = len(fn_df)
            fp_count = len(fp_df)
            
            # Estimar custos (para demonstração)
            avg_loan_amount = testing_sample['loan_amnt'].mean() if 'loan_amnt' in testing_sample.columns else 10000
            
            # Assumir taxa de perda em inadimplências de cerca de 70% do principal
            estimated_fn_loss = fn_count * avg_loan_amount * 0.7
            
            # Assumir custo de oportunidade em falsos positivos de cerca de 10% do lucro potencial
            estimated_fp_loss = fp_count * avg_loan_amount * 0.1
            
            st.markdown(f"""
            ### Impacto Financeiro Estimado
            
            Baseado em um modelo de custo simples:
            
            - **Falsos Negativos (Aprovar empréstimos ruins):**
              - Contagem: {fn_count}
              - Perda estimada: R${estimated_fn_loss:,.2f}
              
            - **Falsos Positivos (Rejeitar empréstimos bons):**
              - Contagem: {fp_count}
              - Custo de oportunidade estimado: R${estimated_fp_loss:,.2f}
              
            - **Impacto total estimado:** R${estimated_fn_loss + estimated_fp_loss:,.2f}
            
            Nota: Esta é uma estimativa simplificada para fins de demonstração. O impacto financeiro real
            exigiria análise mais complexa incorporando taxas de juros, taxas de recuperação, custos operacionais
            e custos de oportunidade.
            """)
            
            # Análise de limiar
            st.subheader("Análise do Limiar de Decisão")
            
            # Calcular métricas em diferentes limiares
            thresholds = np.linspace(0.1, 0.9, 9)
            threshold_results = []
            
            for threshold in thresholds:
                pred_at_threshold = (comparison_df['probabilidade_prevista'] >= threshold).astype(int)
                acc = accuracy_score(comparison_df['loan_status'], pred_at_threshold)
                prec = precision_score(comparison_df['loan_status'], pred_at_threshold)
                rec = recall_score(comparison_df['loan_status'], pred_at_threshold)
                f1_score_val = f1_score(comparison_df['loan_status'], pred_at_threshold)
                
                # Contar FP e FN neste limiar
                fp = ((pred_at_threshold == 1) & (comparison_df['loan_status'] == 0)).sum()
                fn = ((pred_at_threshold == 0) & (comparison_df['loan_status'] == 1)).sum()
                
                # Custos estimados
                fn_cost = fn * avg_loan_amount * 0.7
                fp_cost = fp * avg_loan_amount * 0.1
                total_cost = fn_cost + fp_cost
                
                threshold_results.append({
                    'Limiar': threshold,
                    'Acurácia': acc,
                    'Precisão': prec,
                    'Recall': rec,
                    'F1 Score': f1_score_val,
                    'Falsos Positivos': fp,
                    'Falsos Negativos': fn,
                    'Custo Estimado': total_cost
                })
            
            threshold_df = pd.DataFrame(threshold_results)
            
            # Plotar métricas vs limiar
            fig, ax1 = plt.subplots(figsize=(12, 6))
            
            # Plotar métricas
            ax1.set_xlabel('Limiar de Decisão')
            ax1.set_ylabel('Valor da Métrica')
            ax1.plot(threshold_df['Limiar'], threshold_df['Acurácia'], 'g-', label='Acurácia')
            ax1.plot(threshold_df['Limiar'], threshold_df['Precisão'], 'b-', label='Precisão')
            ax1.plot(threshold_df['Limiar'], threshold_df['Recall'], 'r-', label='Recall')
            ax1.plot(threshold_df['Limiar'], threshold_df['F1 Score'], 'y-', label='F1 Score')
            ax1.tick_params(axis='y')
            ax1.legend(loc='center left')
            ax1.grid(True, alpha=0.3)
            
            # Plotar custo estimado no eixo secundário
            ax2 = ax1.twinx()
            ax2.set_ylabel('Custo Estimado (R$)', color='purple')
            ax2.plot(threshold_df['Limiar'], threshold_df['Custo Estimado'], 'm--', label='Custo Est.')
            ax2.tick_params(axis='y', labelcolor='purple')
            
            fig.tight_layout()
            ax1.set_title('Impacto do Limiar de Probabilidade no Desempenho do Modelo e Custo')
            
            # Adicionar marcador do limiar ótimo
            optimal_idx = threshold_df['Custo Estimado'].idxmin()
            optimal_threshold = threshold_df.loc[optimal_idx, 'Limiar']
            ax1.axvline(x=optimal_threshold, color='black', linestyle='--', alpha=0.7)
            ax1.text(optimal_threshold+0.02, 0.5, f'Limiar ótimo: {optimal_threshold:.2f}', 
                    transform=ax1.get_xaxis_transform(), fontsize=10)
            
            col1, col2, col3 = st.columns([1, 6, 1])
            with col2:
                st.pyplot(fig)        
            
            st.markdown(f"""
            ### Limiar de Decisão Ótimo
            
            Baseado na análise de custo, o limiar de decisão ótimo é aproximadamente **{optimal_threshold:.2f}**
            (comparado ao limiar padrão de 0.5).
            
            Neste limiar:
            - Acurácia: {threshold_df.loc[optimal_idx, 'Acurácia']:.4f}
            - Precisão: {threshold_df.loc[optimal_idx, 'Precisão']:.4f}
            - Recall: {threshold_df.loc[optimal_idx, 'Recall']:.4f}
            - Custo estimado: R${threshold_df.loc[optimal_idx, 'Custo Estimado']:,.2f}
            
            **Recomendação de negócio:** Considere ajustar o limiar de decisão baseado nas prioridades
            específicas do negócio e apetite ao risco. Um limiar mais alto reduz inadimplências mas aprova menos empréstimos,
            enquanto um limiar mais baixo aprova mais empréstimos mas aumenta o risco de inadimplência.
            """)
            
            # Baixar resultados de comparação
            st.download_button(
                label="Baixar Resultados de Comparação",
                data=comparison_df.to_csv(index=False),
                file_name="comparacao_previsao_vs_real.csv",
                mime="text/csv"
            )


# Rodapé com dicas para novos usuários
st.markdown("---")
st.markdown("""
**Como usar esta ferramenta:**
1. Comece selecionando as variáveis nas caixas de seleção
2. Clique em "Treinar Modelo de Regressão Logística" para ver os resultados
3. Analise o desempenho e as estatísticas do modelo
4. Utilize o modelo para analisar potenciais tomadores de empréstimo
""")

# Rodapé
st.divider()
st.caption("© 2025 Ferramenta de Modelagem de Risco de Crédito | Desenvolvida com propósitos pedagógicos")
st.caption("Prof. José Américo – Coppead")