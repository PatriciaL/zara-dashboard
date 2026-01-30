# NOTEBOOK 2: Visualizaciones Avanzadas con Plotly
# ==================================================
# Duración: 30 minutos
# Objetivo: Crear gráficos interactivos profesionales

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Zara Analytics", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_excel('EADIC_claude_test.xlsx', sheet_name='raw_zara')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['Revenue'] = df['price'] * df['Sales Volume']
    return df

df = load_data()

st.title("📊 Visualizaciones Interactivas")

"""
===========================================
SECCIÓN 1: Gráfico de Barras - Ventas por Posición
===========================================
"""
st.subheader("Ventas por Posición en Tienda")

# Agrupar datos
sales_by_position = df.groupby('Product Position')['Sales Volume'].sum().reset_index()

# Crear gráfico
fig1 = px.bar(
    sales_by_position,
    x='Product Position',
    y='Sales Volume',
    color='Product Position',
    title="Distribución de Ventas por Posición",
    color_discrete_sequence=['#000000', '#666666', '#999999']  # Colores estilo Zara
)

# Personalización
fig1.update_layout(
    showlegend=False,
    height=400,
    xaxis_title="Posición",
    yaxis_title="Unidades Vendidas"
)

st.plotly_chart(fig1, use_container_width=True)

"""
===========================================
SECCIÓN 2: Pie Chart - Distribución por Sección
===========================================
"""
st.subheader("Distribución por Sección (MAN/WOMAN)")

section_dist = df['section'].value_counts().reset_index()
section_dist.columns = ['section', 'count']

fig2 = px.pie(
    section_dist,
    values='count',
    names='section',
    title="Productos por Sección",
    color_discrete_sequence=['#000000', '#666666']
)

fig2.update_traces(textposition='inside', textinfo='percent+label')

st.plotly_chart(fig2, use_container_width=True)

"""
===========================================
SECCIÓN 3: Scatter Plot - Precio vs Ventas
===========================================
"""
st.subheader("Relación Precio vs Volumen de Ventas")

fig3 = px.scatter(
    df,
    x='price',
    y='Sales Volume',
    color='section',
    size='Revenue',
    hover_data=['name', 'Product Position'],
    title="Análisis Precio-Volumen",
    color_discrete_sequence=['#000000', '#666666']
)

fig3.update_layout(height=500)

st.plotly_chart(fig3, use_container_width=True)

"""
===========================================
SECCIÓN 4: Gráfico de Líneas - Top Productos
===========================================
"""
st.subheader("Top 10 Productos por Revenue")

top_products = df.nlargest(10, 'Revenue')[['name', 'Revenue']]

fig4 = px.bar(
    top_products,
    x='Revenue',
    y='name',
    orientation='h',
    title="Top 10 Productos",
    color='Revenue',
    color_continuous_scale='Greys'
)

fig4.update_layout(height=400, yaxis={'categoryorder':'total ascending'})

st.plotly_chart(fig4, use_container_width=True)

"""
===========================================
SECCIÓN 5: Gráfico Agrupado - Revenue por Categoría
===========================================
"""
st.subheader("Revenue por Sección y Posición")

revenue_analysis = df.groupby(['section', 'Product Position'])['Revenue'].sum().reset_index()

fig5 = px.bar(
    revenue_analysis,
    x='section',
    y='Revenue',
    color='Product Position',
    barmode='group',
    title="Revenue Agrupado",
    color_discrete_sequence=['#000000', '#444444', '#888888']
)

st.plotly_chart(fig5, use_container_width=True)

"""
========================================
EJERCICIO PARA LOS ESTUDIANTES:
========================================

1. Crea un histograma de la distribución de precios
   HINT: usa px.histogram(df, x='price')

2. Añade un box plot comparando ventas entre secciones
   HINT: usa px.box(df, x='section', y='Sales Volume')

3. Personaliza los colores de AL MENOS un gráfico con tu paleta favorita

4. Añade tooltips personalizados a cualquier gráfico
   HINT: usa el parámetro hover_data=[]

5. BONUS: Crea un gráfico de sunburst para mostrar jerarquía
   HINT: px.sunburst(df, path=['section', 'Product Position'], values='Revenue')
"""

# Para ejecutar:
# streamlit run notebook2_visualizations.py
