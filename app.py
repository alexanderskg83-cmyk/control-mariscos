import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Nicalapia - Recepción e Impresión", page_icon="🐟", layout="wide")

# LISTAS PREDETERMINADAS
PROVEEDORES_LISTA = ["Chester Espinoza", "Distribuidora del Mar", "Cooperativa Masachapa", "➕ Escribir manualmente..."]
ZONAS_LISTA = ["Masachapa", "Casares", "San Juan del Sur", "Granja interna", "➕ Escribir manualmente..."]
PERSONAL_LISTA = ["W. Solis / E. Palacios", "Maikelyn Zelaya", "Carlos Mendoza", "Juan Pérez", "➕ Escribir manualmente..."]
ESPECIES_LISTA = ["Macuá 1-2", "Macuá 2-4", "Macuá 4-6", "C/Amarilla 2-4", "C/Amarilla 4-6", "Dientón 1-3", "Dientón 3-5", "➕ Escribir manualmente..."]

if 'filas' not in st.session_state:
    st.session_state.filas = []
if 'hora_inicio' not in st.session_state:
    st.session_state.hora_inicio = ""
if 'hora_fin' not in st.session_state:
    st.session_state.hora_fin = ""

st.title("🐟 Formato de Clasificación y Recepción de Materia Prima")
st.caption("Nicaraguan Tilapia (Nicalapia S.A.) | Con Módulo de Impresión Idéntico al Físico")

tab_datos, tab_registro = st.tabs(["📋 1. Encabezado y Tiempos", "⚖️ 2. Tabla de Pesajes e Impresión"])

# ==========================================
# PESTAÑA 1: ENCABEZADO
# ==========================================
with tab_datos:
    st.subheader("Datos de Recepción")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        prov_sel = st.selectbox("Proveedor:", PROVEEDORES_LISTA)
        proveedor = st.text_input("Escriba el nuevo Proveedor:", value="Chester Espinoza") if prov_sel == "➕ Escribir manualmente..." else prov_sel
        
        zona_sel = st.selectbox("Zona de Pesca:", ZONAS_LISTA)
        zona = st.text_input("Escriba la nueva Zona:", value="Masachapa") if zona_sel == "➕ Escribir manualmente..." else zona_sel
        
        granja = st.text_input("Nombre de la Granja:", value="N/A")
        
    with col2:
        rec_sel = st.selectbox("Recibidor / Pesador:", PERSONAL_LISTA, index=0)
        recibidor = st.text_input("Escriba el nuevo Recibidor:", value="W. Solis / E. Palacios") if rec_sel == "➕ Escribir manualmente..." else rec_sel
        
        elab_sel = st.selectbox("Elaborado Por:", PERSONAL_LISTA, index=1)
        elaborado = st.text_input("Escriba quién elabora:", value="Maikelyn Zelaya") if elab_sel == "➕ Escribir manualmente..." else elab_sel
        
        carta = st.selectbox("Carta de Garantía:", ["SI", "NO"])
        
    with col3:
        histaminico = st.selectbox("Producto Histamínico:", ["NO", "SI"])
        
        st.write("---")
        st.markdown("**Control de Reloj de Planta**")
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            if st.button("🕒 Capturar Inicio"):
                st.session_state.hora_inicio = datetime.now().strftime("%I:%M %p")
            st.text_input("Hora Inicio:", value=st.session_state.hora_inicio, disabled=True)
        with col_t2:
            if st.button("🏁 Capturar Fin"):
                st.session_state.hora_fin = datetime.now().strftime("%I:%M %p")
            st.text_input("Hora Final:", value=st.session_state.hora_fin, disabled=True)

# ==========================================
# PESTAÑA 2: REGISTRO DE PESAJES E IMPRESIÓN
# ==========================================
with tab_registro:
    st.subheader("Ingreso de Pesos e Inspección Sensorial")
    
    lote_sugerido = st.session_state.filas[-1]['Lote'] if st.session_state.filas else "NL14-77-25-26-01"
    termo_sugerido = st.session_state.filas[-1]['Nº Termos'] if st.session_state.filas else "143"
    
    with st.form("registro_especie", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1:
            esp_sel = st.selectbox("Especie / Talla:", ESPECIES_LISTA)
            especie = st.text_input("Escriba la nueva Especie/Talla:") if esp_sel == "➕ Escribir manualmente..." else esp_sel
            
            lote = st.text_input("Lote:", value=lote_sugerido)
        with c2:
            termo = st.text_input("Nº Termos:", value=termo_sugerido)
            temp = st.number_input("Temperatura (ºC):", min_value=-5.0, max_value=30.0, value=1.0, step=0.1)
        with c3:
            st.markdown("**Inspección Sensorial**")
            olor = st.selectbox("Olor:", ["E", "B", "MB", "N/A"])
            color = st.selectbox("Color:", ["E", "B", "MB", "N/A"])
        with c4:
            st.markdown("** **")
            textura = st.selectbox("Textura:", ["E", "B", "MB", "N/A"])
            sabor = st.selectbox("Sabor:", ["N/A", "E", "B", "MB"])
            
        st.markdown("**Campos para Digitar Pesos Manuales (Lbs)**")
        pw1, pw2, pw3, pw4, pw5, pw6, pw7, pw8 = st.columns(8)
        p1 = pw1.number_input("Peso 1", min_value=0.0, value=0.0, step=0.1)
        p2 = pw2.number_input("Peso 2", min_value=0.0, value=0.0, step=0.1)
        p3 = pw3.number_input("Peso 3", min_value=0.0, value=0.0, step=0.1)
        p4 = pw4.number_input("Peso 4", min_value=0.0, value=0.0, step=0.1)
        p5 = pw5.number_input("Peso 5", min_value=0.0, value=0.0, step=0.1)
        p6 = pw6.number_input("Peso 6", min_value=0.0, value=0.0, step=0.1)
        p7 = pw7.number_input("Peso 7", min_value=0.0, value=0.0, step=0.1)
        p8 = pw8.number_input("Peso 8", min_value=0.0, value=0.0, step=0.1)
        
        enviar = st.form_submit_button("➕ AGREGAR FILA AL FORMATO")
        
        if enviar and especie:
            pesos_lista = [p for p in [p1, p2, p3, p4, p5, p6, p7, p8]]
            nueva_fila = {
                "Especie/Talla": especie, "Lote": lote, "Olor": olor, "Color": color,
                "Textura": textura, "Sabor": sabor, "Nº Termos": termo, "ºC": temp
            }
            for idx, p in enumerate(pesos_lista, 1):
                nueva_fila[f"Peso {idx}"] = p if p > 0 else ""
                
            st.session_state.filas.append(nueva_fila)
            st.rerun()

    # SECCIÓN DE IMPRESIÓN Y VISTA PREVIA
    if st.session_state.filas:
        st.markdown("---")
        st.markdown("### 📋 Formato Listo para Impresión")
        
        # Generar las filas vacías necesarias para completar las 10 filas del papel original
        filas_actuales = st.session_state.filas.copy()
        while len(filas_actuales) < 10:
            filas_actuales.append({
                "Especie/Talla": "", "Lote": "", "Olor": "", "Color": "",
                "Textura": "", "Sabor": "", "Nº Termos": "", "ºC": "",
                "Peso 1": "", "Peso 2": "", "Peso 3": "", "Peso 4": "", "Peso 5": "", "Peso 6": "", "Peso 7": "", "Peso 8": ""
            })

        # Construcción del HTML idéntico a la foto para mandar a imprimir
        html_rows = ""
        for f in filas_actuales:
            html_rows += f"""
            <tr style="height: 24px;">
                <td style="border: 1px solid #000; text-align: left; padding-left: 5px;">{f['Especie/Talla']}</td>
                <td style="border: 1px solid #000;">{f['Lote']}</td>
                <td style="border: 1px solid #000;">{f['Olor']}</td>
                <td style="border: 1px solid #000;">{f['Color']}</td>
                <td style="border: 1px solid #000;">{f['Textura']}</td>
                <td style="border: 1px solid #000;">{f['Sabor']}</td>
                <td style="border: 1px solid #000;">{f['Nº Termos']}</td>
                <td style="border: 1px solid #000;">{f['ºC']}</td>
                <td style="border: 1px solid #000;">{f['Peso 1']}</td>
                <td style="border: 1px solid #000;">{f['Peso 2']}</td>
                <td style="border: 1px solid #000;">{f['Peso 3']}</td>
                <td style="border: 1px solid #000;">{f['Peso 4']}</td>
                <td style="border: 1px solid #000;">{f['Peso 5']}</td>
                <td style="border: 1px solid #000;">{f['Peso 6']}</td>
                <td style="border: 1px solid #000;">{f['Peso 7']}</td>
                <td style="border: 1px solid #000;">{f['Peso 8']}</td>
            </tr>
            """

        fecha_hoy = datetime.now().strftime("%d/%m/%y")
        
        documento_imprimible = f"""
        <div style="font-family: Arial, sans-serif; padding: 10px; background-color: white; color: black; font-size: 9pt; width: 100%;">
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 10px;">
                <tr>
                    <td style="border: 1.5px solid #000; width: 20%; text-align: center; font-weight: bold; font-size: 13pt; padding: 5px;">
                        Nicalapia<br><span style="font-size: 8pt; font-weight: normal;">Nicaraguan Tilapia</span>
                    </td>
                    <td style="border: 1.5px solid #000; width: 65%; text-align: center; padding: 5px;">
                        <span style="font-size: 11pt; font-weight: bold;">Nicaraguan Tilapia (Nicalapia S.A)</span><br>
                        <span style="font-size: 12pt; font-weight: bold; letter-spacing: 0.5px;">FORMATO:<br>CLASIFICACION Y RECEPCION DE MATERIA PRIMA</span>
                    </td>
                    <td style="border: 1.5px solid #000; width: 15%; font-size: 7.5pt; font-weight: bold; padding: 5px; line-height: 1.3;">
                        CODIGO: FT-QA-01<br>FECHA ULT. REV:<br>Mayo 2026<br>Versión: 1
                    </td>
                </tr>
            </table>
            
            <div style="line-height: 1.8; margin-bottom: 12px; font-size: 9pt;">
                <span style="font-weight: bold;">FECHA/HORA DE RECEPCION:</span> <span style="border-bottom: 1px solid #000; padding: 0 10px;">{fecha_hoy}</span>
                <span style="font-weight: bold; margin-left: 15px;">PROVEEDOR:</span> <span style="border-bottom: 1px solid #000; padding: 0 15px;">{proveedor}</span>
                <span style="font-weight: bold; margin-left: 15px;">ZONA DE PESCA:</span> <span style="border-bottom: 1px solid #000; padding: 0 15px;">{zona}</span>
                <span style="font-weight: bold; margin-left: 15px;">CARTA DE GARANTIA:</span> <span style="border-bottom: 1px solid #000; padding: 0 10px;">{carta}</span><br>
                <span style="font-weight: bold;">NOMBRE DE LA GRANJA:</span> <span style="border-bottom: 1px solid #000; padding: 0 15px;">{granja}</span>
                <span style="font-weight: bold; margin-left: 15px;">RECIBIDOR/PESADOR:</span> <span style="border-bottom: 1px solid #000; padding: 0 20px;">{recibidor}</span>
                <span style="font-weight: bold; margin-left: 15px;">PRODUCTO HISTAMINICO:</span> <span style="font-weight: bold;">SI / </span><span style="border-bottom: 1px solid #000; padding: 0 10px;">{histaminico}</span><br>
                <span style="font-weight: bold;">HORA INICIO:</span> <span style="border-bottom: 1px solid #000; padding: 0 15px;">{st.session_state.hora_inicio}</span>
                <span style="font-weight: bold; margin-left: 30px;">HORA FINAL:</span> <span style="border-bottom: 1px solid #000; padding: 0 15px;">{st.session_state.hora_fin}</span>
                <span style="font-weight: bold; margin-left: 30px;">ELABORADO POR:</span> <span style="border-bottom: 1px solid #000; padding: 0 30px;">{elaborado}</span>
            </div>

            <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 8pt;">
                <thead>
                    <tr style="background-color: #f2f2f2;">
                        <th rowspan="2" style="border: 1px solid #000; width: 14%; font-weight: bold;">ESPECIE/TALLA</th>
                        <th rowspan="2" style="border: 1px solid #000; width: 12%; font-weight: bold;">LOTE</th>
                        <th colspan="4" style="border: 1px solid #000; width: 16%; font-weight: bold;">EVALUACION SENSORIAL<br>(B; MB; E; N/A)</th>
                        <th rowspan="2" style="border: 1px solid #000; width: 6%; font-weight: bold;">Nº TERMOS</th>
                        <th rowspan="2" style="border: 1px solid #000; width: 4%; font-weight: bold;">ºC</th>
                        <th colspan="8" style="border: 1px solid #000; width: 48%; font-weight: bold;">PESOS (Lbs)</th>
                    </tr>
                    <tr style="background-color: #f2f2f2; font-size: 7.5pt;">
                        <th style="border: 1px solid #000;">OLOR</th>
                        <th style="border: 1px solid #000;">COLOR</th>
                        <th style="border: 1px solid #000;">TEXRURA</th>
                        <th style="border: 1px solid #000;">SABOR</th>
                        <th style="border: 1px solid #000; width: 6%;">1</th>
                        <th style="border: 1px solid #000; width: 6%;">2</th>
                        <th style="border: 1px solid #000; width: 6%;">3</th>
                        <th style="border: 1px solid #000; width: 6%;">4</th>
                        <th style="border: 1px solid #000; width: 6%;">5</th>
                        <th style="border: 1px solid #000; width: 6%;">6</th>
                        <th style="border: 1px solid #000; width: 6%;">7</th>
                        <th style="border: 1px solid #000; width: 6%;">8</th>
                    </tr>
                </thead>
                <tbody>
                    {html_rows}
                </tbody>
            </table>
            <div style="margin-top: 8px; font-size: 7.5pt; font-style: italic;">
                Nota: Formato oficial regulado por el departamento de Aseguramiento de la Calidad (QA).
            </div>
        </div>
        """
        
        # Mostrar el formato físico exacto embebido en la aplicación para revisión visual
        st.markdown("#### 👁️ Vista Previa del Papel Oficial")
        components.html(documento_imprimible, height=450, scrolling=True)
        
        # Botón nativo del navegador para Guardar como PDF / Imprimir de inmediato
        st.warning("💡 Para imprimir de forma idéntica o guardar en PDF: Haga clic derecho sobre la vista previa superior -> Seleccione 'Imprimir' -> Ajuste la orientación a 'Horizontal'.")
        
        if st.button("🗑️ Borrar todo y abrir nueva recepción"):
            st.session_state.filas = []
            st.rerun()        
