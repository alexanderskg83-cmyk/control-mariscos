import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Nicalapia - Recepción", page_icon="🐟", layout="wide")

# Inicializar estados de memoria para evitar pérdidas de datos al cambiar de pestaña
if 'filas' not in st.session_state:
    st.session_state.filas = []
if 'hora_inicio' not in st.session_state:
    st.session_state.hora_inicio = ""
if 'hora_fin' not in st.session_state:
    st.session_state.hora_fin = ""

st.title("🐟 Formato: Clasificación y Recepción de Materia Prima")
st.caption("Nicaraguan Tilapia (Nicalapia S.A.) | Código: FT-QA-01")

tab_datos, tab_registro = st.tabs(["📋 1. Encabezado y Tiempos", "⚖️ 2. Tabla de Pesajes e Inspección"])

with tab_datos:
    st.subheader("Datos de Recepción")
    col1, col2, col3 = st.columns(3)
    with col1:
        proveedor = st.text_input("Proveedor:", value="Chester Espinoza")
        zona = st.text_input("Zona de Pesca:", value="Masachapa")
        granja = st.text_input("Nombre de la Granja:", value="N/A")
    with col2:
        recibidor = st.text_input("Recibidor / Pesador:", value="W. Solis / E. Palacios")
        elaborado = st.text_input("Elaborado Por:", value="Maikelyn Zelaya")
        carta = st.selectbox("Carta de Garantía:", ["SI", "NO"])
    with col3:
        histaminico = st.selectbox("Producto Histamínico:", ["NO", "SI"])
        
        st.write("---")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            if st.button("🕒 Capturar Inicio"):
                st.session_state.hora_inicio = datetime.now().strftime("%I:%M %p")
            st.text_input("Hora Inicio:", value=st.session_state.hora_inicio, disabled=True)
        with col_t2:
            if st.button("🏁 Capturar Fin"):
                st.session_state.hora_fin = datetime.now().strftime("%I:%M %p")
            st.text_input("Hora Final:", value=st.session_state.hora_fin, disabled=True)

with tab_registro:
    st.subheader("Optimización de Ingreso de Pesos y Calidad")
    
    # Valores sugeridos/heredados automáticos para agilizar
    lote_sugerido = st.session_state.filas[-1]['Lote'] if st.session_state.filas else "NL14-77-25-26-01"
    termo_sugerido = st.session_state.filas[-1]['Nº Termos'] if st.session_state.filas else "143"
    
    with st.form("registro_especie", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1:
            especie = st.text_input("Especie / Talla:", placeholder="Ej. Macuá 1-2")
            lote = st.text_input("Lote:", value=lote_sugerido)
        with c2:
            termo = st.text_input("Nº Termos:", value=termo_sugerido)
            temp = st.number_input("Temperatura (ºC):", min_value=-5.0, max_value=30.0, value=1.0, step=0.1)
        with c3:
            st.markdown("**Evaluación Sensorial (Auto)**")
            olor = st.selectbox("Olor:", ["E", "B", "MB", "N/A"])
            color = st.selectbox("Color:", ["E", "B", "MB", "N/A"])
        with c4:
            st.markdown("** **")
            textura = st.selectbox("Textura:", ["E", "B", "MB", "N/A"])
            sabor = st.selectbox("Sabor:", ["N/A", "E", "B", "MB"])
            
        st.markdown("**Digitación Manual de Pesos (Lbs)**")
        pw1, pw2, pw3, pw4, pw5, pw6, pw7, pw8 = st.columns(8)
        p1 = pw1.number_input("Peso 1", min_value=0.0, value=0.0, step=0.5)
        p2 = pw2.number_input("Peso 2", min_value=0.0, value=0.0, step=0.5)
        p3 = pw3.number_input("Peso 3", min_value=0.0, value=0.0, step=0.5)
        p4 = pw4.number_input("Peso 4", min_value=0.0, value=0.0, step=0.5)
        p5 = pw5.number_input("Peso 5", min_value=0.0, value=0.0, step=0.5)
        p6 = pw6.number_input("Peso 6", min_value=0.0, value=0.0, step=0.5)
        p7 = pw7.number_input("Peso 7", min_value=0.0, value=0.0, step=0.5)
        p8 = pw8.number_input("Peso 8", min_value=0.0, value=0.0, step=0.5)
        
        enviar = st.form_submit_button("➕ Agregar Fila al Formato")
        
        if enviar and especie:
            pesos_lista = [p for p in [p1, p2, p3, p4, p5, p6, p7, p8] if p > 0]
            nueva_fila = {
                "Especie/Talla": especie, "Lote": lote, "Olor": olor, "Color": color,
                "Textura": textura, "Sabor": sabor, "Nº Termos": termo, "ºC": temp
            }
            for idx, p in enumerate(pesos_lista, 1):
                nueva_fila[f"Peso {idx}"] = p
                
            st.session_state.filas.append(nueva_fila)
            st.rerun()

    if st.session_state.filas:
        st.markdown("### 📊 Vista del Formato Actual")
        df_mostrar = pd.DataFrame(st.session_state.filas).fillna("")
        st.dataframe(df_mostrar, use_container_width=True)
        
        # Generar CSV para descargar en Excel
        csv = df_mostrar.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Exportar a Excel (CSV)", data=csv, file_name="recepcion_nicalapia.csv", mime="text/csv")