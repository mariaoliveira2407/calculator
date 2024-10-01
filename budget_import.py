import streamlit as st
import pandas as pd
import docx2txt
import PyPDF2
import os

# Parâmetros fixos de produtividade
palavras_por_hora = 900  # Palavras traduzidas por hora
palavras_por_pagina = 300  # Número médio de palavras por página

# Função para resetar os valores das entradas
def reset_inputs():
    st.session_state['valor_por_hora'] = 10.0
    st.session_state['numero_paginas'] = 0
    st.session_state['numero_horas'] = 0.0
    st.session_state['numero_palavras'] = 0
    st.session_state['uploaded_file'] = None
    st.session_state['reset'] = False

# Inicializar estado do aplicativo
if 'reset' not in st.session_state:
    reset_inputs()
    st.session_state['reset'] = True

# Função para converter o tempo decimal em horas e minutos
def format_time(hours):
    h = int(hours)
    m = int((hours - h) * 60)
    if h > 0:
        return f"{h}h {m}min"
    else:
        return f"{m}min"

# Título da Aplicação
st.title("Interactive Translation Budget Calculator")

# Entrada de valor por hora
valor_por_hora = st.number_input("Enter the hourly rate (USD):", 
                                 min_value=0.0, 
                                 step=1.0, 
                                 key='valor_por_hora')

valor_por_pagina = (valor_por_hora / palavras_por_hora) * palavras_por_pagina  # Calcula o valor por página com base na produtividade
valor_por_palavra = valor_por_hora / palavras_por_hora  # Valor por palavra baseado no valor por hora

st.write(f"Calculated cost per page: **USD {valor_por_pagina:.2f}**")
st.write(f"Calculated cost per word: **USD {valor_por_palavra:.4f}**")

# Seção para upload de arquivo e contagem de palavras
st.header("Upload File for Word Count")
st.markdown("<small>**(Note: 1 file at a time)**</small>", unsafe_allow_html=True)

# Tipos de arquivos permitidos
uploaded_file = st.file_uploader("Upload a file (txt, docx, pdf):", 
                                 type=["txt", "docx", "pdf"])

# Função para contar palavras em um arquivo de texto
def count_words_in_text(text):
    words = text.split()
    return len(words)

# Função para processar o arquivo e contar as palavras
def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # Lidar com arquivos de texto
        if uploaded_file.type == "text/plain":
            text = str(uploaded_file.read(), "utf-8")
            word_count = count_words_in_text(text)
            return word_count
        
        # Lidar com arquivos docx
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = docx2txt.process(uploaded_file)
            word_count = count_words_in_text(text)
            return word_count

        # Lidar com arquivos PDF
        elif uploaded_file.type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            word_count = count_words_in_text(text)
            return word_count

    return 0

# Processar o arquivo carregado e contar palavras
num_palavras = 0
if uploaded_file is not None:
    num_palavras = process_uploaded_file(uploaded_file)
    st.write(f"**Total Word Count: {num_palavras} words**")

# Entrada de número de palavras manualmente (opcional)
st.markdown("---")
st.subheader("Or optionally enter the number of words:")
numero_palavras_manual = st.number_input("Number of Words:", min_value=0, step=100, key='numero_palavras')

# Seção de entradas para cálculo do orçamento
st.header("Budget Calculation")

# Entrada de número de páginas e horas manualmente
numero_paginas = st.number_input("Enter the number of pages (optional):", 
                                 min_value=0, 
                                 step=1, 
                                 key='numero_paginas')

numero_horas = st.number_input("Enter the number of hours (optional):", 
                               min_value=0.0, 
                               step=0.5, 
                               key='numero_horas')

# Cálculo do orçamento e tempo estimado
orcamento_total = 0
tempo_estimado = 0

# Calcular com base no número de palavras do arquivo
if num_palavras > 0:
    orcamento_total += num_palavras * valor_por_palavra
    tempo_estimado += num_palavras / palavras_por_hora

# Calcular com base no número de palavras manualmente (se inserido)
if numero_palavras_manual > 0:
    orcamento_total += numero_palavras_manual * valor_por_palavra
    tempo_estimado += numero_palavras_manual / palavras_por_hora

# Calcular com base no número de páginas (se inserido manualmente)
if numero_paginas > 0:
    orcamento_total += numero_paginas * valor_por_pagina
    tempo_estimado += (numero_paginas * palavras_por_pagina) / palavras_por_hora

# Calcular com base no número de horas (se inserido manualmente)
if numero_horas > 0:
    orcamento_total += numero_horas * valor_por_hora
    tempo_estimado += numero_horas

# Converter o tempo estimado para horas e minutos
tempo_formatado = format_time(tempo_estimado)

# Botão de Reset
if st.button("Reset"):
    reset_inputs()
    st.experimental_rerun()

# Caixa de Resultado Destacada (tamanho reduzido)
st.markdown(
    f"""
    <div style="border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; background-color: #f9f9f9; text-align: center; max-width: 600px; margin: 0 auto;">
        <h3 style="color: #4CAF50;">Total Estimated Cost: USD {orcamento_total:.2f}</h3>
        <h4 style="color: #4CAF50;">Total Estimated Time: {tempo_formatado}</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# Observação sobre a aplicação
st.markdown("---")
st.markdown("**Note:** Upload a file to automatically calculate the word count. **Please ensure the file is not an image (e.g., scanned documents or certificates), as word count cannot be extracted from images.** You can also manually input the number of pages or hours for additional calculations.")

