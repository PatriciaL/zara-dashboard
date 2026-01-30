# DASHBOARD ZARA ANALYTICS - VERSIÓN COMPLETA
# ==============================================
# Combina: Setup + Visualizaciones + Filtros
# Autor: Workshop Zara Analytics
# ==============================================

import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================================
# CONFIGURACIÓN DE LA PÁGINA
# ==============================================
st.set_page_config(
    page_title="Zara Analytics Dashboard",
    page_icon="🛍️",
    layout="wide"
)

# ==============================================
# FUNCIÓN PARA CARGAR DATOS
# ==============================================
@st.cache_data
def load_data():
    """Carga y limpia los datos del Excel"""
    df = pd.read_excel('EADIC_claude_test.xlsx', sheet_name='raw_zara')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['Revenue'] = df['price'] * df['Sales Volume']
    return df

# Cargar datos
df = load_data()

# ==============================================
# HEADER PRINCIPAL
# ==============================================
st.title("🛍️ Zara Analytics Dashboard")
st.markdown("**Dashboard Interactivo para Análisis de Productos Zara**")
st.markdown("---")

# ==============================================
# SIDEBAR - FILTROS
# ==============================================
st.sidebar.title("🎛️ Filtros y Configuración")
st.sidebar.markdown("---")

# Filtro: Sección
selected_section = st.sidebar.multiselect(
    "📊 Sección",
    options=df['section'].unique(),
    default=df['section'].unique(),
    help="Selecciona las secciones a mostrar"
)

# Filtro: Posición en Tienda
selected_position = st.sidebar.multiselect(
    "📍 Posición en Tienda",
    options=df['Product Position'].unique(),
    default=df['Product Position'].unique(),
    help="Filtra por posición del producto en tienda"
)

# Filtro: Promoción
selected_promotion = st.sidebar.multiselect(
    "🏷️ En Promoción",
    options=df['Promotion'].unique(),
    default=df['Promotion'].unique(),
    help="Filtra productos en promoción"
)

# Filtro: Estacional
selected_seasonal = st.sidebar.multiselect(
    "🌦️ Estacional",
    options=df['Seasonal'].unique(),
    default=df['Seasonal'].unique(),
    help="Filtra productos estacionales"
)

# Filtro: Rango de Precio
price_range = st.sidebar.slider(
    "💰 Rango de Precio (€)",
    min_value=float(df['price'].min()),
    max_value=float(df['price'].max()),
    value=(float(df['price'].min()), float(df['price'].max())),
    help="Ajusta el rango de precios"
)

st.sidebar.markdown("---")

# ==============================================
# APLICAR FILTROS
# ==============================================
df_filtered = df[
    (df['section'].isin(selected_section)) &
    (df['Product Position'].isin(selected_position)) &
    (df['Promotion'].isin(selected_promotion)) &
    (df['Seasonal'].isin(selected_seasonal)) &
    (df['price'] >= price_range[0]) &
    (df['price'] <= price_range[1])
]

# Información de filtros
st.sidebar.success(f"✅ **{len(df_filtered)}** productos seleccionados de **{len(df)}** totales")

# Botón de reset en sidebar
if st.sidebar.button("🔄 Resetear Todos los Filtros"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Usa los filtros para explorar diferentes segmentos de productos")

# ==============================================
# KPIs PRINCIPALES
# ==============================================
st.subheader("📊 Métricas Principales")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Productos",
        f"{len(df_filtered):,}",
        delta=f"{len(df_filtered) - len(df)} vs total"
    )

with col2:
    total_revenue = df_filtered['Revenue'].sum()
    st.metric(
        "Revenue Total",
        f"€{total_revenue:,.0f}",
        delta=f"{(total_revenue/df['Revenue'].sum()*100):.1f}% del total"
    )

with col3:
    avg_price = df_filtered['price'].mean()
    st.metric(
        "Precio Promedio",
        f"€{avg_price:.2f}",
        delta=f"€{avg_price - df['price'].mean():.2f}"
    )

with col4:
    total_sales = df_filtered['Sales Volume'].sum()
    st.metric(
        "Unidades Vendidas",
        f"{total_sales:,}",
        delta=f"{(total_sales/df['Sales Volume'].sum()*100):.1f}% del total"
    )

st.markdown("---")

# ==============================================
# SECCIÓN DE VISUALIZACIONES
# ==============================================
st.subheader("📈 Análisis Visual")

# Primera fila de gráficos
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Ventas por Posición en Tienda")
    sales_by_position = df_filtered.groupby('Product Position')['Sales Volume'].sum().reset_index()
    
    fig1 = px.bar(
        sales_by_position,
        x='Product Position',
        y='Sales Volume',
        color='Product Position',
        color_discrete_sequence=['#000000', '#666666', '#999999'],
        title="Distribución de Ventas por Posición"
    )
    fig1.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Posición",
        yaxis_title="Unidades Vendidas"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### Distribución por Sección")
    section_dist = df_filtered['section'].value_counts().reset_index()
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

# Segunda fila: Scatter plot completo
st.markdown("### Relación Precio vs Volumen de Ventas")
fig3 = px.scatter(
    df_filtered,
    x='price',
    y='Sales Volume',
    color='section',
    size='Revenue',
    hover_data=['name', 'Product Position'],
    title="Análisis Precio-Volumen (tamaño = revenue)",
    color_discrete_sequence=['#000000', '#666666']
)
fig3.update_layout(height=500)
st.plotly_chart(fig3, use_container_width=True)

# Tercera fila de gráficos
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Top 10 Productos por Revenue")
    top_products = df_filtered.nlargest(10, 'Revenue')[['name', 'Revenue']]
    
    fig4 = px.bar(
        top_products,
        x='Revenue',
        y='name',
        orientation='h',
        title="Los 10 Productos Más Rentables",
        color='Revenue',
        color_continuous_scale='Greys'
    )
    fig4.update_layout(
        height=400,
        yaxis={'categoryorder':'total ascending'}
    )
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.markdown("### Revenue por Sección y Posición")
    revenue_analysis = df_filtered.groupby(['section', 'Product Position'])['Revenue'].sum().reset_index()
    
    fig5 = px.bar(
        revenue_analysis,
        x='section',
        y='Revenue',
        color='Product Position',
        barmode='group',
        title="Revenue Agrupado por Categorías",
        color_discrete_sequence=['#000000', '#444444', '#888888']
    )
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ==============================================
# SECCIÓN DE DATOS DETALLADOS
# ==============================================
st.subheader("📋 Exploración de Datos")

# Tabs para organizar información
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Todos los Datos", 
    "🏆 Top 20 por Revenue", 
    "📈 Estadísticas Descriptivas",
    "💡 Insights"
])

with tab1:
    st.markdown("##### Tabla Completa de Productos Filtrados")
    st.dataframe(
        df_filtered,
        use_container_width=True,
        height=400
    )
    
    # Botón de descarga
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Datos Filtrados (CSV)",
        data=csv,
        file_name=f"zara_filtered_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )

with tab2:
    st.markdown("##### Top 20 Productos por Revenue")
    top_20 = df_filtered.nlargest(20, 'Revenue')[
        ['name', 'section', 'Product Position', 'price', 'Sales Volume', 'Revenue', 'Promotion']
    ]
    st.dataframe(
        top_20,
        use_container_width=True,
        height=400
    )

with tab3:
    st.markdown("##### Estadísticas Descriptivas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Variables Numéricas:**")
        st.dataframe(
            df_filtered[['price', 'Sales Volume', 'Revenue']].describe(),
            use_container_width=True
        )
    
    with col2:
        st.markdown("**Información General:**")
        st.write(f"- **Total de registros:** {len(df_filtered):,}")
        st.write(f"- **Productos únicos:** {df_filtered['name'].nunique():,}")
        st.write(f"- **Secciones:** {', '.join(df_filtered['section'].unique())}")
        st.write(f"- **Posiciones:** {', '.join(df_filtered['Product Position'].unique())}")
        st.write(f"- **Productos en promoción:** {len(df_filtered[df_filtered['Promotion'] == 'Yes']):,}")
        st.write(f"- **Productos estacionales:** {len(df_filtered[df_filtered['Seasonal'] == 'Yes']):,}")

with tab4:
    st.markdown("##### 💡 Insights Automáticos")
    
    # Producto más caro
    most_expensive = df_filtered.nlargest(1, 'price').iloc[0]
    st.info(f"🔝 **Producto más caro:** {most_expensive['name']} - €{most_expensive['price']:.2f}")
    
    # Producto más vendido
    best_seller = df_filtered.nlargest(1, 'Sales Volume').iloc[0]
    st.success(f"🏆 **Producto más vendido:** {best_seller['name']} - {best_seller['Sales Volume']:,} unidades")
    
    # Mayor revenue
    top_revenue = df_filtered.nlargest(1, 'Revenue').iloc[0]
    st.warning(f"💰 **Mayor revenue:** {top_revenue['name']} - €{top_revenue['Revenue']:,.0f}")
    
    # Análisis de precios
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Precio Mínimo", f"€{df_filtered['price'].min():.2f}")
    with col2:
        st.metric("Precio Mediano", f"€{df_filtered['price'].median():.2f}")
    with col3:
        st.metric("Precio Máximo", f"€{df_filtered['price'].max():.2f}")

# ==============================================
# FOOTER
# ==============================================
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📊 Zara Analytics Dashboard**")
    st.caption("Powered by Streamlit")

with col2:
    st.markdown(f"**🕐 Última actualización:** {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}")

with col3:
    if st.button("ℹ️ Acerca de"):
        st.info("""
        **Dashboard Interactivo de Análisis de Productos Zara**
        
        Funcionalidades:
        - ✅ Filtros dinámicos múltiples
        - ✅ KPIs en tiempo real
        - ✅ Visualizaciones interactivas
        - ✅ Análisis estadístico
        - ✅ Exportación de datos
        - ✅ Insights automáticos
        
        Versión: 1.0 | Workshop 2026
        """)
