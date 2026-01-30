# NOTEBOOK 5: Deployment a Producción
# =====================================
# Duración: 25 minutos
# Objetivo: Desplegar el dashboard en Streamlit Cloud

"""
===========================================
PARTE 1: Preparar archivos para deployment
===========================================
"""

# 1.1: Verificar que tienes todos los archivos necesarios
"""
Estructura de archivos requerida:

zara-dashboard/
├── app.py                      # ✅ Tu aplicación principal
├── requirements.txt            # ✅ Dependencias
├── EADIC_claude_test.xlsx     # ✅ Datos
├── README.md                   # ✅ Documentación (opcional)
└── .gitignore                  # ✅ Git config
"""

# 1.2: Crear .gitignore
"""
Crea un archivo llamado .gitignore con este contenido:

__pycache__/
*.py[cod]
.streamlit/secrets.toml
.env
*.key
venv/
"""

# 1.3: Verificar requirements.txt
"""
Tu requirements.txt debe tener:

streamlit==1.31.0
pandas==2.2.0
plotly==5.18.0
openpyxl==3.1.2
anthropic==0.18.1
"""

"""
===========================================
PARTE 2: Subir a GitHub
===========================================
"""

# 2.1: Inicializar Git (si no lo has hecho)
"""
Abre terminal en la carpeta de tu proyecto y ejecuta:

git init
git add .
git commit -m "Initial commit - Zara Dashboard"
"""

# 2.2: Crear repositorio en GitHub
"""
1. Ve a https://github.com/new
2. Nombre del repo: zara-analytics-dashboard
3. Descripción: Dashboard interactivo para análisis de productos Zara
4. Public o Private (tu eliges)
5. NO marques "Initialize with README" (ya lo tienes)
6. Click en "Create repository"
"""

# 2.3: Conectar y subir
"""
Copia los comandos que GitHub te muestra y ejecútalos:

git remote add origin https://github.com/TU-USUARIO/zara-analytics-dashboard.git
git branch -M main
git push -u origin main
"""

"""
===========================================
PARTE 3: Desplegar en Streamlit Cloud
===========================================
"""

# 3.1: Ir a Streamlit Cloud
"""
1. Ve a https://share.streamlit.io/
2. Si no tienes cuenta, créala con tu cuenta de GitHub
3. Click en "New app"
"""

# 3.2: Configurar el deployment
"""
En el formulario que aparece:

Repository: TU-USUARIO/zara-analytics-dashboard
Branch: main
Main file path: app.py

Click en "Deploy!"
"""

# 3.3: Esperar deployment
"""
Streamlit Cloud hará automáticamente:
✅ Clonar tu repositorio
✅ Instalar dependencias de requirements.txt
✅ Ejecutar tu app.py
✅ Generar una URL pública

Tiempo estimado: 2-3 minutos
"""

"""
===========================================
PARTE 4: Configurar Secrets (OPCIONAL)
===========================================
"""

# 4.1: Añadir API Key de Claude (si la usas)
"""
1. En Streamlit Cloud, ve a tu app
2. Click en "⚙️ Settings" (esquina superior derecha)
3. Click en "Secrets"
4. Pega esto (reemplaza con tu key real):

ANTHROPIC_API_KEY = "sk-ant-api03-tu-key-aqui"

5. Click en "Save"
6. La app se reiniciará automáticamente
"""

"""
===========================================
PARTE 5: Verificar y Probar
===========================================
"""

# 5.1: Tu dashboard ya está vivo!
"""
URL será algo como:
https://tu-usuario-zara-analytics-dashboard-xxxxx.streamlit.app

✅ Accesible desde cualquier dispositivo
✅ Actualizaciones automáticas cuando hagas push a GitHub
✅ Hosting gratuito
✅ SSL/HTTPS incluido
"""

# 5.2: Probar funcionalidades
"""
Verifica que todo funciona:
✓ Los KPIs se muestran correctamente
✓ Los gráficos son interactivos
✓ Los filtros funcionan
✓ Los datos se cargan
✓ (Si aplica) El chat con Claude funciona
"""

"""
===========================================
PARTE 6: Actualizar el Dashboard
===========================================
"""

# 6.1: Hacer cambios locales
"""
1. Edita tu app.py localmente
2. Prueba con: streamlit run app.py
3. Cuando esté listo, haz commit y push:

git add .
git commit -m "Actualización: descripción del cambio"
git push
"""

# 6.2: Deployment automático
"""
✅ Streamlit Cloud detecta el push
✅ Actualiza automáticamente tu app
✅ Sin downtime
✅ Cambios visibles en 1-2 minutos
"""

"""
===========================================
PARTE 7: Troubleshooting Común
===========================================
"""

# Error 1: "ModuleNotFoundError"
"""
PROBLEMA: Falta una librería en requirements.txt
SOLUCIÓN: Añade la librería faltante a requirements.txt y haz push
"""

# Error 2: "File not found: EADIC_claude_test.xlsx"
"""
PROBLEMA: El archivo Excel no está en GitHub
SOLUCIÓN: Verifica que el archivo esté en el repo y haz push
"""

# Error 3: "API key not configured"
"""
PROBLEMA: Si usas Claude, falta la key en Secrets
SOLUCIÓN: Añade ANTHROPIC_API_KEY en Settings → Secrets
"""

# Error 4: "App is not loading"
"""
PROBLEMA: Error en el código
SOLUCIÓN: Revisa los logs en Streamlit Cloud (botón "Manage app" → "Logs")
"""

"""
===========================================
PARTE 8: Configuración Avanzada (Opcional)
===========================================
"""

# 8.1: Custom Domain (Premium)
"""
Si tienes cuenta Pro de Streamlit:
1. Ve a Settings → General
2. Añade tu dominio personalizado
3. Configura DNS según instrucciones
"""

# 8.2: Protección con contraseña
"""
Crea archivo .streamlit/secrets.toml localmente:

[passwords]
admin = "tu_contraseña"

Y en app.py:
def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["passwords"]["admin"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if not check_password():
    st.stop()
"""

"""
========================================
CHECKLIST FINAL DE DEPLOYMENT
========================================

ANTES DE DESPLEGAR:
□ Todos los archivos necesarios están en el repo
□ requirements.txt está completo y actualizado
□ .gitignore configurado (no subir secrets)
□ Código probado localmente
□ README.md con instrucciones (opcional)

DURANTE EL DEPLOYMENT:
□ Repositorio conectado correctamente
□ Branch y archivo principal correctos
□ Sin errores en los logs de Streamlit Cloud

DESPUÉS DEL DEPLOYMENT:
□ URL funciona correctamente
□ Todos los features funcionan
□ Rendimiento aceptable
□ Secrets configurados (si aplica)

MANTENIMIENTO:
□ Monitorear logs regularmente
□ Actualizar dependencias periódicamente
□ Hacer backups del código
□ Documentar cambios importantes
"""

"""
========================================
RECURSOS ADICIONALES
========================================

Documentación oficial:
- Streamlit Docs: https://docs.streamlit.io/
- Deployment: https://docs.streamlit.io/streamlit-community-cloud
- Secrets: https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management

Comunidad:
- Forum: https://discuss.streamlit.io/
- GitHub: https://github.com/streamlit/streamlit
- Twitter: @streamlit

Troubleshooting:
- Status: https://streamlit.statuspage.io/
- Known Issues: https://github.com/streamlit/streamlit/issues
"""

# ¡Felicidades! Tu dashboard ya está en producción 🎉
