import streamlit as st
import pandas as pd
import json
from utils import Transformer

def validar_dados(dict_respostas):
    if dict_respostas['years_working'] != 0 and dict_respostas['years_unemployed'] != 0:
        st.warning('Dados de emprego/desemprego incompatíveis.')
        return False
    return True

def analisar_credito(dict_respostas):
    """Simulação de análise de crédito com lógica simples de if/else."""
    if dict_respostas['annual_income'] > 20000 and dict_respostas['age'] > 25:
        return True  # Crédito viável
    else:
        return False  # Crédito não recomendado

def exibir_resultados(previsao):
    """Exibe os resultados da análise de crédito."""
    if previsao:
        st.image("img/approved.gif")
        st.success("Seu crédito é viável!")
    else:
        st.image("img/denied.gif")
        st.error("Seu crédito não é recomendado.")

def estilo_local(nome_do_arquivo):
    """Carrega o estilo do CSS para a aplicação."""
    with open(nome_do_arquivo) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    """Função principal da aplicação Streamlit."""
    estilo_local("style.css")

    st.image("img/kima_kudi_logo_white.png")
    st.markdown("<h1 style='text-align: center; color: black;'>🧠 Kima Kudi - Análise Inteligente de Crédito 🧠</h1>", unsafe_allow_html=True)

    st.markdown("Bem-vindo ao **Kima Kudi**, seu assistente inteligente para a concepção de crédito bancário. Preencha as informações abaixo e clique em **Analisar Crédito** para verificar se seu crédito é <span style='color: green'>viável</span> ou <span style='color: red'>não recomendado</span>.", unsafe_allow_html=True)

    st.caption("**Aviso:** Kima Kudi é um sistema fictício para fins educacionais. A análise é feita com uma lógica simples de if/else. Mais detalhes podem ser encontrados [aqui no repositório do projeto](https://github.com/diascarolina/credit-scoring-streamlit).")

    expander_1 = st.expander("👤 Informações Pessoais")
    expander_2 = st.expander("💼 Informações Profissionais")
    expander_3 = st.expander("👥 Informações Familiares")

    dict_respostas = {}
    lista_de_categorias = ['Ensino Fundamental', 'Ensino Médio', 'Superior Incompleto', 'Superior Completo', 'Pós-Graduação', 'Mestrado', 'Doutorado', 'Não Informado', 'Outro', 'Desempregado', 'Aposentado', 'Trabalhador Autônomo', 'Empregado', 'Servidor Público', 'Outros', 'Casado', 'Solteiro', 'Separado', 'Divorciado', 'Viúvo', 'União Estável']

    with expander_1:
        col1_form, col2_form = st.columns(2)

        dict_respostas['name'] = col1_form.text_input('Nome Completo')
        dict_respostas['age'] = col1_form.slider('Qual sua idade?', help='O controle deslizante pode ser movido usando as teclas de seta.', min_value=0, max_value=100, step=1)
        dict_respostas['education_type'] = col1_form.selectbox('Qual seu nível de escolaridade?', lista_de_categorias)
        dict_respostas['marital_status'] = col1_form.selectbox('Qual seu estado civil?', lista_de_categorias)
        dict_respostas['own_car'] = 1 if col2_form.selectbox('Você possui um carro?', ['Sim', 'Não']) == 'Sim' else 0
        dict_respostas['own_phone'] = 1 if col2_form.selectbox('Você possui um telefone? (não celular)', ['Sim', 'Não']) == 'Sim' else 0
        dict_respostas['own_email'] = 1 if col2_form.selectbox('Você possui um endereço de e-mail?', ['Sim', 'Não']) == 'Sim' else 0

    with expander_2:
        col3_form, col4_form = st.columns(2)

        dict_respostas['occupation_type'] = col3_form.selectbox('Qual o tipo de seu trabalho?', lista_de_categorias)
        dict_respostas['income_type'] = col3_form.selectbox('Qual o tipo de sua renda?', lista_de_categorias)
        dict_respostas['own_workphone'] = 1 if col3_form.selectbox('Você possui um telefone comercial?', ['Sim', 'Não']) == 'Sim' else 0
        dict_respostas['annual_income'] = col3_form.slider('Qual seu salário mensal?', help='O controle deslizante pode ser movido usando as teclas de seta.', min_value=0, max_value=35000, step=500) * 12
        dict_respostas['years_working'] = col4_form.slider('Há quantos anos você trabalha (em anos)?', help='O controle deslizante pode ser movido usando as teclas de seta.', min_value=0, max_value=50, step=1)
        dict_respostas['years_unemployed'] = col4_form.slider('Há quantos anos você está desempregado (em anos)?', help='O controle deslizante pode ser movido usando as teclas de seta.', min_value=0, max_value=50, step=1)

    with expander_3:
        col4_form, col5_form = st.columns(2)

        dict_respostas['housing_type'] = col4_form.selectbox('Qual o tipo de sua moradia?', lista_de_categorias)
        dict_respostas['own_property'] = 1 if col4_form.selectbox('Você possui um imóvel?', ['Sim', 'Não']) == 'Sim' else 0
        dict_respostas['family_size'] = col5_form.slider('Qual o tamanho de sua família?', help='O controle deslizante pode ser movido usando as teclas de seta.', min_value=1, max_value=20, step=1)
        dict_respostas['children_count'] = col5_form.slider('Quantos filhos você tem?', help='O controle deslizante pode ser movido usando as teclas de seta.', min_value=0, max_value=20, step=1)

    if st.button('Analisar Crédito'):
        if validar_dados(dict_respostas):
            previsao = analisar_credito(dict_respostas)
            exibir_resultados(previsao)

            # Salvar dados em um arquivo JSON
            with open("credit_requests.json", "a") as file:
                json.dump(dict_respostas, file, indent=4)
                file.write(",\n")  # Adiciona uma vírgula após cada entrada

if __name__ == "__main__":
    main()