# NOTEBOOK 4: Integración con Claude AI (Opcional)
# ==================================================
# Duración: 20 minutos
# Objetivo: Añadir chat conversacional para análisis de datos

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Zara Analytics + AI", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_excel('EADIC_claude_test.xlsx', sheet_name='raw_zara')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['Revenue'] = df['price'] * df['Sales Volume']
    return df

df = load_data()

st.title("🤖 Chat con Claude AI")

"""
===========================================
NOTA IMPORTANTE: Esta funcionalidad requiere API key
===========================================
Para usar Claude AI necesitas:
1. Cuenta en https://console.anthropic.com/
2. Crear una API key
3. La key cuesta ~$0.01-0.05 por pregunta

Este notebook muestra CÓMO implementarlo, pero la funcionalidad
es OPCIONAL para el dashboard.
"""

st.info("💡 **Esta sección es OPCIONAL**. El dashboard funciona perfectamente sin IA.")

"""
===========================================
SECCIÓN 1: Input de API Key del Usuario
===========================================
"""
st.subheader("Configuración")

user_api_key = st.text_input(
    "🔑 API Key de Anthropic (opcional)",
    type="password",
    placeholder="sk-ant-api03-...",
    help="Tu API key se usa solo en esta sesión y no se guarda"
)

if not user_api_key:
    st.warning("⚠️ Sin API key configurada. Ingresa tu key arriba para activar el chat.")
    
    with st.expander("📖 ¿Cómo conseguir una API key?"):
        st.markdown("""
        1. Ve a https://console.anthropic.com/
        2. Crea una cuenta (gratis)
        3. Ve a Settings → API Keys
        4. Click en "Create Key"
        5. Copia la key (empieza con `sk-ant-...`)
        
        **Costo**: ~$0.01-0.05 por pregunta
        """)
    
    st.stop()  # Detiene la ejecución si no hay key

"""
===========================================
SECCIÓN 2: Función para Llamar a Claude
===========================================
"""
def call_claude_api(prompt, data_context, api_key):
    """
    Llama a la API de Claude con el contexto de los datos
    """
    try:
        import anthropic
        
        client = anthropic.Anthropic(api_key=api_key)
        
        system_prompt = f"""Eres un analista de datos experto trabajando con datos de productos de Zara.

DATOS DISPONIBLES:
{data_context}

Responde de forma clara, concisa y profesional. Usa números y datos específicos."""
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
            system=system_prompt
        )
        
        return message.content[0].text
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

"""
===========================================
SECCIÓN 3: Preparar Contexto de Datos
===========================================
"""
# Resumen de los datos para enviar a Claude
data_summary = f"""
Dataset de Productos Zara:
- Total productos: {len(df)}
- Secciones: {', '.join(df['section'].unique())}
- Posiciones: {', '.join(df['Product Position'].unique())}
- Rango de precios: €{df['price'].min():.2f} - €{df['price'].max():.2f}
- Precio promedio: €{df['price'].mean():.2f}
- Total ventas (unidades): {df['Sales Volume'].sum():,}
- Revenue total: €{df['Revenue'].sum():,.0f}

Top 5 productos por revenue:
{df.nlargest(5, 'Revenue')[['name', 'price', 'Sales Volume', 'Revenue']].to_string()}
"""

"""
===========================================
SECCIÓN 4: Interfaz de Chat
===========================================
"""
st.success("✅ **Chat con Claude activado**")

# Inicializar historial de chat en session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("Pregunta sobre los datos de Zara..."):
    # Añadir mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Obtener respuesta de Claude
    with st.chat_message("assistant"):
        with st.spinner("Claude está analizando..."):
            response = call_claude_api(prompt, data_summary, user_api_key)
            st.markdown(response)
    
    # Añadir respuesta al historial
    st.session_state.messages.append({"role": "assistant", "content": response})

# Botón para limpiar conversación
if st.button("🗑️ Limpiar Chat"):
    st.session_state.messages = []
    st.rerun()

"""
===========================================
SECCIÓN 5: Sugerencias de Preguntas
===========================================
"""
with st.expander("💡 Preguntas Sugeridas"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Análisis de Ventas:**
        - ¿Qué productos tienen mejor rendimiento?
        - ¿Cómo afectan las promociones a las ventas?
        - ¿Qué sección genera más revenue?
        """)
    
    with col2:
        st.markdown("""
        **Estrategia:**
        - ¿Qué productos deberíamos promocionar más?
        - Dame insights sobre la estrategia de precios
        - ¿Qué posición en tienda funciona mejor?
        """)

"""
===========================================
SECCIÓN 6: Info sobre Costos
===========================================
"""
with st.expander("💰 ¿Cuánto cuesta usar Claude?"):
    st.markdown("""
    **Costos aproximados:**
    - Una pregunta simple: ~$0.01-0.02
    - Una pregunta compleja: ~$0.03-0.05
    - 100 preguntas al mes: ~$1-5 USD
    
    **Tu API key se usa solo en esta sesión** y no se guarda en ningún servidor.
    
    [Más info sobre precios](https://www.anthropic.com/pricing)
    """)

"""
========================================
EJERCICIO PARA LOS ESTUDIANTES:
========================================

1. Modifica el system_prompt para que Claude responda en un estilo diferente
   (por ejemplo, más técnico o más casual)

2. Añade un botón que envíe automáticamente una pregunta predefinida
   HINT: Usa st.button() y simula un prompt

3. Implementa un contador que muestre cuántas preguntas se han hecho en la sesión
   HINT: Cuenta len(st.session_state.messages) / 2

4. BONUS: Añade la opción de exportar toda la conversación a un archivo txt
   HINT: Usa st.download_button() con el contenido del historial

5. SUPER BONUS: Implementa rate limiting para evitar muchas consultas seguidas
   HINT: Usa time.time() y st.session_state para rastrear timestamps
"""

# Para ejecutar:
# streamlit run notebook4_claude_ai.py

# IMPORTANTE: Necesitas instalar:
# pip install anthropic
