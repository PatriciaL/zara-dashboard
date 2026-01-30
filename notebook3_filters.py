# NOTEBOOK 3: Filtros Dinámicos e Interactividad
# ================================================
# Duración: 25 minutos
# Objetivo: Añadir filtros que actualicen el dashboard en tiempo real

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Zara Analytics", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_excel('EADIC_claude_test.xlsx', sheet_name='raw_zara')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['Revenue'] = df['price'] * df['Sales Volume']
    return df

df = load_data()

st.title("🔍 Dashboard con Filtros Dinámicos")

"""
===========================================
SECCIÓN 1: Sidebar con Filtros
===========================================
"""
st.sidebar.title("🎛️ Filtros")
st.sidebar.markdown("---")

# Filtro 1: Sección
selected_section = st.sidebar.multiselect(
    "Sección",
    options=df['section'].unique(),
    default=df['section'].unique()
)

# Filtro 2: Posición en Tienda
selected_position = st.sidebar.multiselect(
    "Posición en Tienda",
    options=df['Product Position'].unique(),
    default=df['Product Position'].unique()
)

# Filtro 3: Promoción
selected_promotion = st.sidebar.multiselect(
    "En Promoción",
    options=df['Promotion'].unique(),
    default=df['Promotion'].unique()
)

# Filtro 4: Estacional
selected_seasonal = st.sidebar.multiselect(
    "Estacional",
    options=df['Seasonal'].unique(),
    default=df['Seasonal'].unique()
)

# Filtro 5: Rango de Precio
price_range = st.sidebar.slider(
    "Rango de Precio (€)",
    min_value=float(df['price'].min()),
    max_value=float(df['price'].max()),
    value=(float(df['price'].min()), float(df['price'].max()))
)

st.sidebar.markdown("---")

"""
===========================================
SECCIÓN 2: Aplicar Filtros al DataFrame
===========================================
"""
# Filtrar datos según las selecciones
df_filtered = df[
    (df['section'].isin(selected_section)) &
    (df['Product Position'].isin(selected_position)) &
    (df['Promotion'].isin(selected_promotion)) &
    (df['Seasonal'].isin(selected_seasonal)) &
    (df['price'] >= price_range[0]) &
    (df['price'] <= price_range[1])
]

# Mostrar info de filtros
st.sidebar.info(f"📊 {len(df_filtered)} productos seleccionados de {len(df)} totales")

"""
===========================================
SECCIÓN 3: KPIs Dinámicos
===========================================
"""
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Productos", f"{len(df_filtered):,}")

with col2:
    total_revenue = df_filtered['Revenue'].sum()
    st.metric("Revenue", f"€{total_revenue:,.0f}")

with col3:
    avg_price = df_filtered['price'].mean()
    st.metric("Precio Medio", f"€{avg_price:.2f}")

with col4:
    total_sales = df_filtered['Sales Volume'].sum()
    st.metric("Unidades", f"{total_sales:,}")

st.markdown("---")

"""
===========================================
SECCIÓN 4: Visualizaciones que se Actualizan
===========================================
"""
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ventas por Posición")
    sales_by_position = df_filtered.groupby('Product Position')['Sales Volume'].sum().reset_index()
    fig1 = px.bar(
        sales_by_position,
        x='Product Position',
        y='Sales Volume',
        color='Product Position',
        color_discrete_sequence=['#000000', '#666666', '#999999']
    )
    fig1.update_layout(showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Distribución por Sección")
    section_dist = df_filtered['section'].value_counts().reset_index()
    section_dist.columns = ['section', 'count']
    fig2 = px.pie(
        section_dist,
        values='count',
        names='section',
        color_discrete_sequence=['#000000', '#666666']
    )
    st.plotly_chart(fig2, use_container_width=True)

"""
===========================================
SECCIÓN 5: Tabs para Organizar Contenido
===========================================
"""
tab1, tab2, tab3 = st.tabs(["📊 Overview", "💰 Revenue", "🔝 Top Productos"])

with tab1:
    st.dataframe(df_filtered, use_container_width=True)

with tab2:
    revenue_by_section = df_filtered.groupby('section')['Revenue'].sum().reset_index()
    fig3 = px.bar(revenue_by_section, x='section', y='Revenue')
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    top10 = df_filtered.nlargest(10, 'Revenue')[['name', 'price', 'Sales Volume', 'Revenue']]
    st.dataframe(top10, use_container_width=True)

"""
===========================================
SECCIÓN 6: Botones y Acciones
===========================================
"""
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 Resetear Filtros"):
        st.rerun()  # Recarga la página

with col2:
    if st.button("📥 Descargar Datos Filtrados"):
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="Descargar CSV",
            data=csv,
            file_name="zara_filtered_data.csv",
            mime="text/csv"
        )

with col3:
    st.write(f"Última actualización: {pd.Timestamp.now().strftime('%H:%M:%S')}")

"""
========================================
EJERCICIO PARA LOS ESTUDIANTES:
========================================

1. Añade un filtro de búsqueda por nombre de producto
   HINT: usa st.sidebar.text_input() y df[df['name'].str.contains()]

2. Crea un filtro de tipo selectbox (uno solo) para Product Category
   HINT: usa st.sidebar.selectbox()

3. Añade un checkbox para mostrar/ocultar productos en promoción
   HINT: usa st.sidebar.checkbox()

4. Implementa un botón que muestre estadísticas avanzadas solo cuando se presiona
   HINT: usa if st.button(): st.write(df_filtered.describe())

5. BONUS: Añade un expander en el sidebar con información de ayuda
   HINT: usa st.sidebar.expander("Ayuda")
"""

# Para ejecutar:
# streamlit run notebook3_filters.py
