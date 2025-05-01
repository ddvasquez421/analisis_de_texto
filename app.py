import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
from googletrans import Translator

# Configuración de la página
st.set_page_config(
    page_title="📖 Necronomicón Lingüístico",
    page_icon="🧠",
    layout="wide"
)

# Estilo Lovecraftiano
st.markdown("""
<style>
/* Importar fuente gótica desde Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=UnifrakturCook:wght@700&display=swap');

/* Fondo oscuro abismal */
body, .stApp {
    background-color: #0a0a0a !important;
    color: #cfcfcf;
    font-family: 'UnifrakturCook', cursive;
}

/* Títulos con resplandor brutal */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'UnifrakturCook', cursive;
    color: #ff4b4b !important;
    text-shadow: 
        0 0 5px #ff0000, 
        0 0 10px #ff2222, 
        0 0 20px #ff3333, 
        0 0 40px #ff3333;
    animation: glow 2s infinite alternate;
}

/* Texto general con leve resplandor */
.stMarkdown, .stText, p, div, span {
    font-family: 'UnifrakturCook', cursive;
    color: #d9d9d9 !important;
    text-shadow: 0 0 3px #aa0000;
}

/* Barras laterales y paneles */
.st-emotion-cache-1v0mbdj, .st-emotion-cache-1v0mbdj * {
    background-color: #121212 !important;
}

/* Animación brutal del resplandor */
@keyframes glow {
  from {
    text-shadow: 0 0 5px #ff0000, 0 0 10px #ff2222, 0 0 20px #ff3333;
  }
  to {
    text-shadow: 0 0 20px #ff4444, 0 0 30px #ff6666, 0 0 40px #ff6666;
  }
}
</style>
""", unsafe_allow_html=True)


# Título principal
st.title("📖 Necronomicón Lingüístico")
st.markdown("""
Adéntrate en el abismo del lenguaje. Este grimorio analiza textos oscuros y revela lo que yace en su interior:
- ☠️ Sentimientos ocultos
- 👁️ Subjetividad inquietante
- 📜 Palabras invocadas con mayor frecuencia
""")

# Barra lateral
st.sidebar.title("☠️ Modo de invocación")
modo = st.sidebar.selectbox(
    "Selecciona el método para desatar el texto:",
    ["Texto directo", "Archivo maldito (.txt)"]
)

# Función para contar palabras
def contar_palabras(texto):
    stop_words = set([...])  # OMITIDO por brevedad: pega tu lista completa aquí como ya la tienes
    palabras = re.findall(r'\b\w+\b', texto.lower())
    palabras_filtradas = [p for p in palabras if p not in stop_words and len(p) > 2]
    contador = {}
    for p in palabras_filtradas:
        contador[p] = contador.get(p, 0) + 1
    return dict(sorted(contador.items(), key=lambda x: x[1], reverse=True)), palabras_filtradas

translator = Translator()

def traducir_texto(texto):
    try:
        traduccion = translator.translate(texto, src='es', dest='en')
        return traduccion.text
    except Exception as e:
        st.error(f"👁️ Error en la traducción arcana: {e}")
        return texto

def procesar_texto(texto):
    texto_original = texto
    texto_ingles = traducir_texto(texto)
    blob = TextBlob(texto_ingles)
    sentimiento = blob.sentiment.polarity
    subjetividad = blob.sentiment.subjectivity
    frases_originales = [f.strip() for f in re.split(r'[.!?]+', texto_original) if f.strip()]
    frases_traducidas = [f.strip() for f in re.split(r'[.!?]+', texto_ingles) if f.strip()]
    frases_combinadas = []
    for i in range(min(len(frases_originales), len(frases_traducidas))):
        frases_combinadas.append({"original": frases_originales[i], "traducido": frases_traducidas[i]})
    contador_palabras, palabras = contar_palabras(texto_ingles)
    return {
        "sentimiento": sentimiento,
        "subjetividad": subjetividad,
        "frases": frases_combinadas,
        "contador_palabras": contador_palabras,
        "palabras": palabras,
        "texto_original": texto_original,
        "texto_traducido": texto_ingles
    }

def crear_visualizaciones(resultados):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔮 Ecos del Sentimiento")
        sentimiento_norm = (resultados["sentimiento"] + 1) / 2
        st.write("**Polaridad Espectral:**")
        st.progress(sentimiento_norm)
        if resultados["sentimiento"] > 0.05:
            st.success(f"✨ Positivo ({resultados['sentimiento']:.2f})")
        elif resultados["sentimiento"] < -0.05:
            st.error(f"🩸 Negativo ({resultados['sentimiento']:.2f})")
        else:
            st.info(f"🪞 Neutral ({resultados['sentimiento']:.2f})")
        st.write("**Subjetividad Eldritch:**")
        st.progress(resultados["subjetividad"])
        if resultados["subjetividad"] > 0.5:
            st.warning(f"👁️ Altamente Subjetivo ({resultados['subjetividad']:.2f})")
        else:
            st.info(f"📜 Objetividad Dominante ({resultados['subjetividad']:.2f})")
    
    with col2:
        st.subheader("📚 Palabras invocadas con mayor frecuencia")
        if resultados["contador_palabras"]:
            palabras_top = dict(list(resultados["contador_palabras"].items())[:10])
            st.bar_chart(palabras_top)

    st.subheader("🌘 Traducción de los ecos")
    with st.expander("🔍 Revelar la transcripción arcana"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Texto Original (Lengua Mortal):**")
            st.text(resultados["texto_original"])
        with col2:
            st.markdown("**Traducción (Lengua Prohibida):**")
            st.text(resultados["texto_traducido"])
    
    st.subheader("🔍 Análisis de fragmentos invocados")
    if resultados["frases"]:
        for i, frase in enumerate(resultados["frases"][:10], 1):
            f_o = frase["original"]
            f_t = frase["traducido"]
            try:
                blob_f = TextBlob(f_t)
                sent = blob_f.sentiment.polarity
                if sent > 0.05:
                    emoji = "😃"
                elif sent < -0.05:
                    emoji = "👹"
                else:
                    emoji = "😐"
                st.write(f"{i}. {emoji} *\"{f_o}\"*")
                st.write(f"   Traducción: *\"{f_t}\"* (Sentimiento: {sent:.2f})")
                st.write("---")
            except:
                st.write(f"{i}. *\"{f_o}\"*")
                st.write(f"   Traducción: *\"{f_t}\"*")
                st.write("---")

# Entrada principal
if modo == "Texto directo":
    st.subheader("✍️ Escribe un texto para analizar")
    texto = st.text_area("", height=200, placeholder="Invoca aquí tus pensamientos más oscuros...")
    if st.button("⚙️ Ejecutar el ritual"):
        if texto.strip():
            with st.spinner("🔄 Consultando al abismo..."):
                resultados = procesar_texto(texto)
                crear_visualizaciones(resultados)
        else:
            st.warning("👁️ Introduce un texto válido antes de invocar.")

elif modo == "Archivo maldito (.txt)":
    st.subheader("📂 Carga un texto prohibido")
    archivo = st.file_uploader("Arrastra aquí el pergamino...", type=["txt", "csv", "md"])
    if archivo:
        try:
            contenido = archivo.getvalue().decode("utf-8")
            with st.expander("📜 Ver fragmento del texto"):
                st.text(contenido[:1000] + ("..." if len(contenido) > 1000 else ""))
            if st.button("📖 Leer el grimorio"):
                with st.spinner("⏳ Descifrando los símbolos..."):
                    resultados = procesar_texto(contenido)
                    crear_visualizaciones(resultados)
        except Exception as e:
            st.error(f"💀 Error al procesar el archivo: {e}")

# Información adicional
with st.expander("📘 Notas del Culto"):
    st.markdown("""
    - **Polaridad**: Valor entre -1 y 1, donde -1 es maligno, 1 es benevolente, y 0 es neutral.
    - **Subjetividad**: Valor entre 0 y 1, donde 1 refleja emociones personales y 0 hechos objetivos.

    Esta herramienta ha sido alimentada con saberes antiguos:
    ```
    streamlit
    textblob
    pandas
    googletrans
    ```
    """)

# Pie de página
st.markdown("---")
st.markdown("*Desarrollado por una mente que miró demasiado tiempo al abismo...*")
