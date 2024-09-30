import streamlit as st

# Parâmetros fixos de produtividade
palavras_por_hora = 900  # Palavras traduzidas por hora
palavras_por_pagina = 300  # Número médio de palavras por página

# Título da Aplicação
st.title("Interactive Translation Budget Calculator")

# Entrada de valores de custo
valor_por_hora = st.number_input("Enter the hourly rate (USD):", min_value=0.0, value=10.0, step=1.0)
valor_por_pagina = (valor_por_hora / palavras_por_hora) * palavras_por_pagina  # Calcula o valor por página com base na produtividade
valor_por_palavra = valor_por_hora / palavras_por_hora  # Valor por palavra baseado no valor por hora

st.write(f"Calculated cost per page: **USD {valor_por_pagina:.2f}**")
st.write(f"Calculated cost per word: **USD {valor_por_palavra:.4f}**")

# Seção de entradas para cálculo do orçamento
st.header("Budget Calculation")

# Entrada de número de páginas, palavras e horas
numero_paginas = st.number_input("Enter the number of pages:", min_value=0, value=0, step=1)
numero_palavras = st.number_input("Enter the number of words:", min_value=0, value=0, step=100)
numero_horas = st.number_input("Enter the number of hours:", min_value=0.0, value=0.0, step=0.5)

# Cálculo do orçamento e tempo estimado
orcamento_total = 0
tempo_estimado = 0

# Calcular com base no número de páginas
if numero_paginas > 0:
    orcamento_total += numero_paginas * valor_por_pagina
    tempo_estimado += (numero_paginas * palavras_por_pagina) / palavras_por_hora

# Calcular com base no número de palavras
if numero_palavras > 0:
    orcamento_total += numero_palavras * valor_por_palavra
    tempo_estimado += numero_palavras / palavras_por_hora

# Calcular com base no número de horas
if numero_horas > 0:
    orcamento_total += numero_horas * valor_por_hora
    tempo_estimado += numero_horas

# Exibição dos resultados de orçamento e tempo
st.write(f"**Total Estimated Cost: USD {orcamento_total:.2f}**")
st.write(f"**Total Estimated Time: {tempo_estimado:.2f} hours**")

# Observação sobre a aplicação
st.markdown("---")
st.markdown("**Note:** The calculations are based on the provided hourly rate and estimated productivity (words per hour and words per page). Adjust the inputs as needed.")
