# NOTEBOOK 1: Setup y Primeros Pasos con Streamlit
# ================================================
# Duración: 20 minutos
# Objetivo: Crear la estructura básica del dashboard

"""
PASO 1: Importar librerías necesarias
"""
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Zara Analytics Dashboard",
    page_icon="🛍️",
    layout="wide"
)

"""
PASO 2: Cargar los datos
"""
@st.cache_data  # Cache para no recargar el Excel cada vez
def load_data():
    df = pd.read_excel('EADIC_claude_test.xlsx', sheet_name='raw_zara')
    # Limpiar datos
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['Revenue'] = df['price'] * df['Sales Volume']
    return df

# Cargar datos
df = load_data()

"""
PASO 3: Header del dashboard
"""
st.title("🛍️ Zara Analytics Dashboard")
st.markdown("Dashboard interactivo para análisis de productos")

"""
PASO 4: Mostrar primeros KPIs
"""
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Productos", f"{len(df):,}")

with col2:
    total_revenue = df['Revenue'].sum()
    st.metric("Revenue Total", f"€{total_revenue:,.0f}")

with col3:
    avg_price = df['price'].mean()
    st.metric("Precio Promedio", f"€{avg_price:.2f}")

with col4:
    total_sales = df['Sales Volume'].sum()
    st.metric("Unidades Vendidas", f"{total_sales:,}")

"""
PASO 5: Mostrar datos en tabla
"""
st.subheader("Vista de Datos")
st.dataframe(df.head(10), use_container_width=True)

"""
PASO 6: Estadísticas básicas
"""
st.subheader("Estadísticas Descriptivas")
st.write(df[['price', 'Sales Volume', 'Revenue']].describe())

"""
========================================
EJERCICIO PARA LOS ESTUDIANTES:
========================================

1. Cambia el icono del dashboard a otro emoji
2. Añade un quinto KPI que muestre el producto más caro
3. Modifica el número de filas mostradas en la tabla a 20
4. Añade un gráfico de barras simple mostrando ventas por sección

HINT: Para el gráfico usa:
fig = px.bar(df.groupby('section')['Sales Volume'].sum().reset_index(), 
             x='section', y='Sales Volume')
st.plotly_chart(fig)
"""

# Para ejecutar:
# streamlit run notebook1_setup.py
