import json
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
from fpdf import FPDF

st.set_page_config(page_title="Nicalapia - Control y Trazabilidad", page_icon="🐟", layout="wide")

# ==========================================
# 🔐 SISTEMA DE LOGIN
# ==========================================
def check_password():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🐟 Nicalapia - Acceso Restringido")
        with st.form("login_form"):
            usuario = st.text_input("Usuario")
            contrasena = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Entrar"):
                if usuario == "admin" and contrasena == "nicalapia123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")
        st.stop()

check_password()

# ==========================================
# ☁️ CONEXIÓN A GOOGLE SHEETS Y DRIVE
# ==========================================
@st.cache_resource
def init_connection():
    creds_dict = dict(st.secrets["gcp_service_account"])
    # Añadidos alcances para Sheets y Drive corporativo
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return creds

def guardar_en_sheets(nombre_hoja, datos):
    try:
        creds = init_connection()
        client = gspread.authorize(creds)
        sheet = client.open_by_key(st.secrets["sheet_id"]).worksheet(nombre_hoja)
        if isinstance(datos, list) and len(datos) > 0:
            df = pd.DataFrame(datos).fillna("") 
            sheet.append_rows(df.values.tolist())
            return True
    except Exception as e:
        st.error(f"🚨 Error en Google Sheets: {e}")
        return False
    return False

def subir_pdf_a_drive(nombre_archivo, pdf_bytes):
    try:
        creds = init_connection()
        service = build('drive', 'v3', credentials=creds)
        folder_id = st.secrets.get("drive_folder_id", "") # Opcional: ID de carpeta compartida en secrets
        
        file_metadata = {'name': nombre_archivo, 'mimeType': 'application/pdf'}
        if folder_id:
            file_metadata['parents'] = [folder_id]
            
        media = MediaIoBaseUpload(io.BytesIO(pdf_bytes), mimetype='application/pdf', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file.get('id')
    except Exception as e:
        st.error(f"🚨 Error al subir a Google Drive: {e}")
        return None

def obtener_historial(nombre_hoja):
    try:
        creds = init_connection()
        client = gspread.authorize(creds)
        sheet = client.open_by_key(st.secrets["sheet_id"]).worksheet(nombre_hoja)
        datos = sheet.get_all_records()
        return pd.DataFrame(datos)
    except Exception as e:
        st.error(f"No se pudo conectar al historial: {e}")
        return pd.DataFrame()

# ==========================================
# 📄 GENERADOR DE PDF NATIVO
# ==========================================
def generar_pdf_reporte(titulo, encabezado, df_datos):
    pdf = FPDF(orientation="L", unit="mm", format="letter")
    pdf.add_page()
    pdf.set_font("helvetica", "B", 14)
    pdf.cell(0, 10, f"Nicalapia S.A. - {titulo}", ln=True, align="C")
    pdf.ln(4)
    
    # Renderizar Encabezados
    pdf.set_font("helvetica", "B", 9)
    for k, v in encabezado.items():
        pdf.cell(60, 5, f"{k}: {v}", ln=False)
    pdf.ln(8)
    
    # Tabla de Contenidos
    pdf.set_font("helvetica", "B", 8)
    columnas = list(df_datos.columns)
    col_width = 260 / max(len(columnas), 1)
    
    for col in columnas:
        pdf.cell(col_width, 6, str(col)[:12], border=1, align="C")
    pdf.ln()
    
    pdf.set_font("helvetica", "", 8)
    for _, row in df_datos.iterrows():
        for col in columnas:
            pdf.cell(col_width, 5, str(row[col])[:12], border=1, align="C")
        pdf.ln()
        
    return pdf.output()

# ==========================================
# LISTAS PREDETERMINADAS
# ==========================================
PROVEEDORES_LISTA = ["Chester Espinoza", "Alba Osava", "Omar Mercado", "Darvin Lopez","Rafael Baltodano", "➕ Escribir manualmente..."]
ZONAS_LISTA = ["Masachapa", "Casares", "San Juan del Sur", "Las peñitas", "Acopio Blufields", "➕ Escribir manualmente..."]
PERSONAL_LISTA = ["Wilbert Solis", "Maikelyn Zelaya", "Donald Fonseca", "Alice Mendoza", "Yilbert Solis","➕ Escribir manualmente..."]
ESPECIES_LISTA = ["Mancha 1-2", "Mancha 2-4", "Mancha 4-6", "Cola Amarilla 2-4", "Cola Amarilla 4-6", "Dientón 1-3", "Dientón 3-5", "Guacamayo 1-3", "➕ Escribir manualmente..."]
PRODUCTOS_TRAZABILIDAD_LISTA = ["Filete de Dorado sin Piel", "Filete de Robalo Sin piel", "Minuta de yellow Tail", "Minuta de Silk", "Minuta de Rucco", "Lonjas de Atun", "➕ Escribir manualmente..."]

# Inicialización de Estados
if 'filas_actuales' not in st.session_state: st.session_state.filas_actuales = []
if 'filas_trazabilidad' not in st.session_state: st.session_state.filas_trazabilidad = []
if 'historial_ver' not in st.session_state: st.session_state.historial_ver = None

LOGO_NICALAPIA_SVG = """
<svg width="85" height="62" viewBox="15 15 90 90" xmlns="http://www.w3.org/2000/svg" style="display: block; margin: 0 auto;">
    <path d="M 20 62 A 40 40 0 1 1 100 62" fill="none" stroke="#124491" stroke-width="3.5" stroke-linecap="round"/>
    <circle cx="74" cy="40" r="4.5" fill="#124491"/>
    <path d="M 22 61 L 45 32 L 61 56" fill="none" stroke="#124491" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 53 51 L 68 41 L 98 61" fill="none" stroke="#124491" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M 23 67 Q 27 64 31 67 T 39 67 T 47 67 T 55 67 T 63 67 T 71 67 T 79 67 T 87 67 T 97 67" fill="none" stroke="#124491" stroke-width="2.8" stroke-linecap="round"/>
    <path d="M 25 73 Q 29 70 33 73 T 41 73 T 49 73 T 57 73 T 65 73 T 73 73 T 81 73 T 89 73 T 95 73" fill="none" stroke="#124491" stroke-width="2.8" stroke-linecap="round"/>
    <path d="M 29 79 Q 33 76 37 79 T 45 79 T 53 79 T 61 79 T 69 79 T 77 79 T 85 79 T 91 79" fill="none" stroke="#124491" stroke-width="2.8" stroke-linecap="round"/>
    <path d="M 37 85 Q 41 82 45 85 T 53 85 T 61 85 T 69 85 T 77 85 T 83 85" fill="none" stroke="#124491" stroke-width="2.8" stroke-linecap="round"/>
    <text x="60" y="104" font-family="'Brush Script MT', 'Comic Sans MS', cursive, sans-serif" font-size="20" font-weight="bold" fill="#124491" text-anchor="middle" font-style="italic">Nicalapia</text>
</svg>
"""

with st.sidebar:
    st.title("Nicalapia S.A.")
    modulo = st.radio("SELECCIONE EL MÓDULO:", ["📊 Recepción de Materia Prima", "🔍 Seguimiento de Trazabilidad"])
    st.write("---")

# ==============================================================================
# MÓDULO 1: RECEPCIÓN DE MATERIA PRIMA (FT-HACCP-005)
# ==============================================================================
if modulo == "📊 Recepción de Materia Prima":
    st.title("🐟 Clasificación y Recepción de Materia Prima")
    
    # Botón global para crear una nueva recepción limpia
    if st.button("🆕 Crear Nueva Recepción (Limpiar Todo)", type="primary"):
        st.session_state.filas_actuales = []
        st.session_state.historial_ver = None
        st.rerun()

    tab_datos, tab_registro, tab_impresion, tab_historial = st.tabs(["📋 Encabezado", "⚖️ Pesajes", "🖨️ Vista de Impresión", "🗂️ Historial de Registros"])

    with tab_datos:
        col1, col2, col3 = st.columns(3)
        with col1:
            prov_sel = st.selectbox("Proveedor:", PROVEEDORES_LISTA, key="prov")
            proveedor = st.text_input("Escriba Proveedor Manual:", value="Darvin Lopez") if prov_sel == "➕ Escribir manualmente..." else prov_sel
            zona_sel = st.selectbox("Zona de Pesca:", ZONAS_LISTA, key="zona")
            zona = st.text_input("Escriba Zona Manual:", value="Las Poritas") if zona_sel == "➕ Escribir manualmente..." else zona_sel
            granja = st.text_input("Nombre de la Granja:", value="")
        with col2:
            rec_sel = st.selectbox("Recibidor / Pesador:", PERSONAL_LISTA, index=2, key="rec")
            recibidor = st.text_input("Escriba Recibidor Manual:", value="D. Fonseca / M. Morales") if rec_sel == "➕ Escribir manualmente..." else rec_sel
            elab_sel = st.selectbox("Elaborado Por:", PERSONAL_LISTA, index=3, key="elab")
            elaborado = st.text_input("Escriba Elaborador Manual:", value="Alice Mendoza") if elab_sel == "➕ Escribir manualmente..." else elab_sel
            carta = st.selectbox("Carta de Garantía:", ["SI", "NO"])
        with col3:
            histaminico = st.selectbox("Producto Histamínico:", ["NO", "SI", "N/A"])
            hora_inicio = st.text_input("Hora Inicio:", value="08:00 AM")
            hora_fin = st.text_input("Hora Final:", value="12:00 PM")

    with tab_registro:
        with st.form("registro_especie", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
            with c1:
                esp_sel = st.selectbox("Especie / Talla:", ESPECIES_LISTA)
                especie = st.text_input("Escriba Especie Manual:") if esp_sel == "➕ Escribir manualmente..." else esp_sel
                lote = st.text_input("Lote:")
            with c2:
                termo = st.text_input("Nº Termos:")
                temp = st.number_input("Temperatura (ºC):", value=1.1, step=0.1)
            with c3:
                olor = st.selectbox("Olor:", ["E", "B", "MB", "N/A"])
                color = st.selectbox("Color:", ["E", "B", "MB", "N/A"])
            with c4:
                textura = st.selectbox("Textura:", ["E", "B", "MB", "N/A"])
                sabor = st.selectbox("Sabor:", ["N/A", "C", "NC", "MP"])
            
            st.markdown("**Pesos (Lbs)**")
            pw = st.columns(8)
            pesos = [pw[i].number_input(f"P{i+1}", min_value=0.0, value=0.0) for i in range(8)]
            
            if st.form_submit_button("➕ AGREGAR FILA"):
                if especie:
                    nueva_fila = {"Especie/Talla": especie, "Lote": lote, "Olor": olor, "Color": color, "Textura": textura, "Sabor": sabor, "Nº Termos": termo, "ºC": temp}
                    for idx, p in enumerate(pesos, 1): nueva_fila[f"Peso {idx}"] = p if p > 0 else ""
                    st.session_state.filas_actuales.append(nueva_fila)
                    st.rerun()

        if st.session_state.filas_actuales:
            st.markdown("### ✏️ Tabla de Pesajes (Puedes editar celdas o corregir pesos directamente aquí abajo):")
            df_editable = pd.DataFrame(st.session_state.filas_actuales).fillna("")
            
            # El data_editor permite guardar cualquier cambio que realice el usuario en vivo
            df_corregido = st.data_editor(df_editable, use_container_width=True, num_rows="dynamic", key="editor_recep")
            st.session_state.filas_actuales = df_corregido.to_dict('records')
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("💾 Guardar, Procesar y Subir a Drive", use_container_width=True, type="primary"):
                    # Compilar registros estructurados con metadata completa para el historial
                    bloque_completo = []
                    for f in st.session_state.filas_actuales:
                        meta_fila = {
                            "Fecha_Registro": datetime.now().strftime("%d/%m/%Y"),
                            "Proveedor": proveedor, "Zona": zona, "Granja": granja,
                            "Recibidor": recibidor, "Elaborado": elaborado, "Carta": carta,
                            "Histaminico": histaminico, "Hora_Inicio": hora_inicio, "Hora_Fin": hora_fin
                        }
                        meta_fila.update(f)
                        bloque_completo.append(meta_fila)
                    
                    st.info("Subiendo copia de respaldo a Google Sheets...")
                    if guardar_en_sheets("Recepcion", bloque_completo):
                        # Generación automática de PDF y subida a Drive
                        encab_pdf = {"Proveedor": proveedor, "Fecha": datetime.now().strftime("%d/%m/%y"), "Granja": granja}
                        pdf_data = generar_pdf_reporte("Clasificación y Recepción", encab_pdf, df_corregido)
                        
                        id_drive = subir_pdf_a_drive(f"Recepcion_{proveedor}_{lote}.pdf", pdf_data)
                        if id_drive:
                            st.success(f"✨ ¡Procesado con éxito! Guardado en Sheets y PDF subido a Drive (ID: {id_drive})")
                        else:
                            st.warning("⚠️ Guardado en Sheets pero falló la subida automática a Drive.")
                    else:
                        st.error("No se pudo conectar con la base de datos de la nube.")
            
            with col_btn2:
                if st.button("🗑️ Vaciar Tabla Temporal", use_container_width=True):
                    st.session_state.filas_actuales = []
                    st.rerun()

    with tab_historial:
        st.markdown("### 🗂️ Buscador de Recepciones Anteriores")
        if st.button("🔄 Cargar / Actualizar Historial Completo de la Nube"):
            st.session_state.df_historial_recep = obtener_historial("Recepcion")
            
        if 'df_historial_recep' in st.session_state and not st.session_state.df_historial_recep.empty:
            df_h = st.session_state.df_historial_recep
            lotes_disponibles = df_h["Lote"].unique()
            lote_sel = st.selectbox("Seleccione el Lote Histórico que desea revisar o imprimir:", lotes_disponibles)
            
            if lote_sel:
                filtrado = df_h[df_h["Lote"] == lote_sel]
                st.dataframe(filtrado, use_container_width=True)
                if st.button("📖 Cargar este registro en la Vista de Impresión"):
                    # Extraer filas formateadas para la tabla de visualización
                    columnas_tabla = ["Especie/Talla", "Lote", "Olor", "Color", "Textura", "Sabor", "Nº Termos", "ºC", "Peso 1", "Peso 2", "Peso 3", "Peso 4", "Peso 5", "Peso 6", "Peso 7", "Peso 8"]
                    st.session_state.filas_actuales = filtrado[columnas_tabla].to_dict('records')
                    st.success("¡Cargado! Dirígete a la pestaña 'Vista de Impresión' para ver el formato oficial.")
        else:
            st.write("Presiona el botón superior para descargar los datos de Google Sheets.")

    with tab_impresion:
        gran_total_libras = 0.0
        html_rows = ""
        filas_imprimir = st.session_state.filas_actuales.copy()
        
        while len(filas_imprimir) < 14: filas_imprimir.append({})

        for f in filas_imprimir:
            suma_fila = 0.0
            if f:
                for i in range(1, 9):
                    val = f.get(f"Peso {i}", "")
                    if val != "": suma_fila += float(val)
                gran_total_libras += suma_fila
            txt_suma_fila = f"{suma_fila:,.1f}" if f and suma_fila > 0 else ""
            html_rows += f"""
            <tr style="height: 24px;">
                <td style="border: 1px solid #000; text-align: left; padding-left: 5px; font-weight: bold;">{f.get('Especie/Talla', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Lote', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Olor', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Color', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Textura', '')} </td>
                <td style="border: 1px solid #000;">{f.get('Sabor', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Nº Termos', '')}</td>
                <td style="border: 1px solid #000; font-weight: bold;">{f.get('ºC', '')}</td>
                {"".join([f'<td style="border: 1px solid #000;">{f.get(f"Peso {i}", "")}</td>' for i in range(1,9)])}
                <td style="border: 1px solid #000; font-weight: bold; background-color: #f9f9f9;">{txt_suma_fila}</td>
            </tr>
            """
        fecha_hoy = datetime.now().strftime("%d/%m/%y")
        carta_si = "[X] SI" if carta == "SI" else "[ &nbsp;] SI"
        carta_no = "[X] NO" if carta == "NO" else "[ &nbsp;] NO"
        hist_si  = "[X] SI" if histaminico == "SI" else "[ &nbsp;] SI"
        hist_no  = "[X] NO" if histaminico == "NO" else "[ &nbsp;] NO"
        hist_na  = "[X] N/A" if histaminico == "N/A" else "[ &nbsp;] N/A"

        documento_imprimible = f"""
        <html><head><style>
            @media print {{ 
                button {{ display: none !important; }} 
                body {{ background-color: white; color: black; padding: 0; margin: 0; }} 
                @page {{ size: letter landscape; margin: 0.15in; }}
            }}
            body {{ font-family: 'Arial', sans-serif; background-color: #fafafa; margin: 0; padding: 2px; }}
            #hoja-oficial {{ background: white; width: 11.1in; height: auto; min-height: 7.2in; margin: 0 auto; box-sizing: border-box; padding: 6px; display: flex; flex-direction: column; justify-content: flex-start; color: black; border: 1px solid #000; }}
            .header-table {{ margin-bottom: 8px; width: 100%; border-collapse: collapse; }}
            .grid-container {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5px; border: 1px solid #000; padding: 5px; font-size: 8.5pt; margin-bottom: 8px; line-height: 1.5; }}
            table {{ table-layout: fixed; width: 100%; border-collapse: collapse; text-align: center; font-size: 8.5pt; }}
            th, td {{ border: 1px solid #000; overflow: hidden; }}
            .footer-section {{ font-size: 7.2pt; line-height: 1.3; text-align: justify; margin-top: 5px; }}
            .obs-lines {{ margin-top: 3px; font-size: 8.5pt; line-height: 1.4; text-align: justify; width: 100%; word-break: break-all; }}
            .custom-recepcion-footer {{ font-size: 7.2pt; line-height: 1.4; font-weight: normal; margin-top: 4px; text-align: justify; }}
        </style></head><body>
            <div style="text-align: center; margin-bottom: 4px;"><button onclick="window.print();" style="background-color: #124491; color: white; border: none; padding: 6px 16px; font-weight: bold; cursor: pointer; font-size:11pt;">🖨️ IMPRIMIR / GUARDAR PDF</button></div>
            <div id="hoja-oficial">
                <div>
                    <table class="header-table">
                        <tr>
                            <td style="width: 14%; padding: 1px;">{LOGO_NICALAPIA_SVG}</td>
                            <td style="width: 64%; vertical-align: middle;">
                                <span style="font-size: 13.5pt; font-weight: bold;">Nicaraguan Tilapia (Nicalapia S.A)</span><br>
                                <span style="font-size: 11.5pt; font-weight: bold;">FORMATO: CLASIFICACION Y RECEPCION DE MATERIA PRIMA</span>
                            </td>
                            <td style="width: 22%; font-size: 8.5pt; font-weight: bold; text-align: left; padding-left: 8px; line-height: 1.3; border-left: 2px solid #000;">CODIGO: FT-HACCP-005<br>FECHA ULTIMA VERSION:<br>Mayo 2026<br>Versión: 1</td>
                        </tr>
                    </table>
                    <div class="grid-container">
                        <div><b>FECHA/HORA DE RECEPCIÓN:</b> {fecha_hoy}<br><b>NOMBRE DE LA GRANJA:</b> {granja}<br><b>PROVEEDOR:</b> {proveedor}</div>
                        <div><b>ZONA DE PESCA:</b> {zona}<br><b>CARTA DE GARANTÍA:</b> {carta_si} &nbsp;&nbsp; {carta_no}<br><b>PRODUCTO HISTAMÍNICO:</b> {hist_si} &nbsp;&nbsp; {hist_no} &nbsp;&nbsp; {hist_na}</div>
                        <div><b>HORA INICIO:</b> {hora_inicio}<br><b>HORA FINAL:</b> {hora_fin}<br><b>RECIBIDOR/PESADOR:</b> {recibidor}<br>
                    </div>
                    <table>
                        <colgroup>
                            <col style="width: 15%;"><col style="width: 10%;"><col style="width: 4%;"><col style="width: 4%;"><col style="width: 4%;"><col style="width: 4%;"><col style="width: 5%;"><col style="width: 4%;">
                            {"".join(['<col style="width: 5%;">' for i in range(1,9)])}<col style="width: 10%;">
                        </colgroup>
                        <thead>
                            <tr style="background-color: #f2f2f2; height: 18px;">
                                <th rowspan="2">ESPECIE/TALLA</th><th rowspan="2">LOTE</th><th colspan="4">EVALUACION SENSORIAL</th><th rowspan="2">No<br>TERMOS</th><th rowspan="2">ºC</th><th colspan="8">PESO</th><th rowspan="2">TOTAL</th>
                            </tr>
                            <tr style="background-color: #f2f2f2; height: 18px;">
                                <th style="font-size: 7pt;">OLOR</th><th style="font-size: 7pt;">COLOR</th><th style="font-size: 7pt;">TEXRURA</th><th style="font-size: 7pt;">SABOR</th>
                                {"".join([f'<th style="font-size: 8pt;">{i}</th>' for i in range(1,9)])}
                            </tr>
                        </thead>
                        <tbody>
                            {html_rows}
                            <tr style="height: 22px; background-color: #f2f2f2; font-weight: bold;"><td colspan="16" style="text-align: right; padding-right: 15px;">TOTAL:</td><td style="font-size: 9.5pt;">{gran_total_libras:,.1f}</td></tr>
                        </tbody>
                    </table>
                </div>
                <div class="footer-section">
                    <b>Evaluación Sensorial:</b> B: Bueno, MB: Muy Bueno; E: Excelente; N/A: No Aplica; AC: Acción Correctiva; <b>SABOR:</b> C: caracteristico, NC: No Conforme, MP: materia prima.<br>
                    
                    <div class="obs-lines">
                        <b>Observaciones:</b> <br>___________________________________________________________________________________________________________________________________________________________________</b>
                       <br>___________________________________________________________________________________________________________________________________________________________________________________________________________</b>

                    </div>
                    
                    <table style="border: none; margin-top: 15px; text-align: center; font-size: 8pt; width: 100%;">
                        <tr style="background: none;">
                            <td style="border: none; padding-top: 2px;">___________________________<br><b>ENTREGADO POR:</b></td>
                            <td style="border: none; padding-top: 2px;">___________________________<br><b>SUPERVISADO POR:</b></td>
                            <td style="border: none; padding-top: 2px;">___________________________<br><b>VERIFICADO POR:</b></td>

                        </tr>
                    </table>
                    
                    <hr style="border: 0; border-top: 1px solid #000; margin-top: 14px; margin-bottom: 6px;">
                    
                    <div class="custom-recepcion-footer">
                        <b>Límite crítico:</b> Temperatura del producto &le; 4°C;<br>
                        <b>Frecuencia del monitoreo:</b> En cada recepción de materia prima, por cada 2 cajillas pesadas se verifica la temperatura, Cada vez que se recibe MP se hace el evaluación sensorial a cada unidad recibida, sino cumple con el con los parámetros sensoriales el producto se rechaza.<br>
                        <b>Modificado el 16/12/2024//Modificado 19/03/2026//Modificado 14/05/2026</b>
                        <div style="text-align: center; font-size: 6.8pt; font-weight: bold; margin-top: 4px;">
                            Este Documento es propiedad de Nicaraguan Tilapia (Nicalapia S.A). Queda prohibida su reproducción total o parcial sin la autorización expresa de las autoridades superiores.
                        </div>
                    </div>
                </div>
            </div></body></html>
        """
        components.html(documento_imprimible, height=750, scrolling=True)


# ==============================================================================
# MÓDULO 2: SEGUIMIENTO DE TRAZABILIDAD (FT-PROD-03)
# ==============================================================================
else:
    st.title("🔍 Control de Trazabilidad de Producto en Proceso")
    
    if st.button("🆕 Crear Nueva Trazabilidad (Limpiar Todo)", type="primary"):
        st.session_state.filas_trazabilidad = []
        st.rerun()

    tab_traz_datos, tab_traz_registro, tab_traz_impresion, tab_traz_historial = st.tabs(["📋 Encabezado", "📐 Procesos", "🖨️ Vista de Impresión", "🗂️ Historial"])
    
    with tab_traz_datos:
        c1, c2, c3 = st.columns(3)
        with c1: traz_fecha = st.date_input("Fecha de Control:", value=datetime.now())
        with c2:
            traz_hora_inicio = st.text_input("Hora Inicio Proceso:", value="07:00 AM")
            traz_hora_fin = st.text_input("Hora Final Proceso:", value="05:00 PM")
        with c3: traz_elaborado = st.text_input("Elaborado Por:", value="Alice Mendoza")

    with tab_traz_registro:
        with st.form("form_trazabilidad", clear_on_submit=True):
            r1, r2, r3 = st.columns(3)
            with r1:
                f_almacenamiento = st.date_input("Fecha de Almacenamiento:")
                n_termo = st.text_input("No. de Termo:")
                prod_sel = st.selectbox("Producto Base:", PRODUCTOS_TRAZABILIDAD_LISTA)
                desc_producto = st.text_input("Escriba Producto Manual:") if prod_sel == "➕ Escribir manualmente..." else prod_sel
            with r2:
                lote_traz = st.text_input("Lote:")
                tipo_proceso = st.text_input("Fecha y Tipo de Proceso:")
                n_termo_destino = st.text_input("N° de Termo Destino:")
            with r3:
                p_inicial = st.number_input("Peso Inicial (Lbs):", min_value=0.0)
                p_final = st.number_input("Peso Final (Lbs):", min_value=0.0)
                proceso_destino = st.text_input("Fecha y Proceso Destino:")
                
            if st.form_submit_button("➕ REGISTRAR FILA"):
                rend_real = (p_final / p_inicial * 100) if p_inicial > 0 else 0.0
                nueva_fila_traz = {
                    "Fecha Almacenamiento": f_almacenamiento.strftime("%d/%m/%Y"), "No. Termo": n_termo, 
                    "Descripcion": desc_producto, "Lote": lote_traz, "Proceso Aplicado": tipo_proceso, 
                    "Peso Inicial": p_inicial, "Peso Final": p_final, "Termo Destino": n_termo_destino, 
                    "Rendimiento Real": f"{rend_real:.1f}%", "Proceso Destino": proceso_destino
                }
                st.session_state.filas_trazabilidad.append(nueva_fila_traz)
                st.rerun()

        if st.session_state.filas_trazabilidad:
            st.markdown("### ✏️ Tabla de Trazabilidad (Editable en vivo):")
            df_traz_edit = pd.DataFrame(st.session_state.filas_trazabilidad)
            
            df_traz_corregido = st.data_editor(df_traz_edit, use_container_width=True, num_rows="dynamic", key="editor_traz")
            st.session_state.filas_trazabilidad = df_traz_corregido.to_dict('records')
            
            col_btn3, col_btn4 = st.columns(2)
            with col_btn3:
                if st.button("💾 Guardar y Subir Trazabilidad a Drive", use_container_width=True):
                    bloque_traz_completo = []
                    for f in st.session_state.filas_trazabilidad:
                        meta = {
                            "Fecha_Control": traz_fecha.strftime("%d/%m/%Y"),
                            "Hora_Inicio": traz_hora_inicio, "Hora_Fin": traz_hora_fin,
                            "Elaborado_Por": traz_elaborado
                        }
                        meta.update(f)
                        bloque_traz_completo.append(meta)
                        
                    if guardar_en_sheets("Trazabilidad", bloque_traz_completo):
                        encab_traz_pdf = {"Encargado": traz_elaborado, "Fecha": traz_fecha.strftime("%d/%m/%Y")}
                        pdf_bytes = generar_pdf_reporte("Control de Trazabilidad", encab_traz_pdf, df_traz_corregido)
                        id_d = subir_pdf_a_drive(f"Trazabilidad_{traz_fecha.strftime('%d%m%Y')}.pdf", pdf_bytes)
                        st.success(f"✨ ¡Trazabilidad Respaldada! PDF en Drive exitoso (ID: {id_d})")
            with col_btn4:
                if st.button("🗑️ Vaciar Tabla Trazabilidad", use_container_width=True):
                    st.session_state.filas_trazabilidad = []
                    st.rerun()

    with tab_traz_historial:
        st.markdown("### 🗂️ Buscador de Trazabilidades Anteriores")
        if st.button("🔄 Descargar Historial de Trazabilidad"):
            st.session_state.df_historial_traz = obtener_historial("Trazabilidad")
            
        if 'df_historial_traz' in st.session_state and not st.session_state.df_historial_traz.empty:
            df_th = st.session_state.df_historial_traz
            lotes_traz_disp = df_th["Lote"].unique()
            lote_t_sel = st.selectbox("Seleccione el Lote de Trazabilidad:", lotes_traz_disp)
            
            if lote_t_sel:
                filtrado_t = df_th[df_th["Lote"] == lote_t_sel]
                st.dataframe(filtrado_t, use_container_width=True)
                if st.button("📖 Cargar en Vista de Impresión Trazabilidad"):
                    col_tabla_traz = ["Fecha Almacenamiento", "No. Termo", "Descripcion", "Lote", "Proceso Aplicado", "Peso Inicial", "Peso Final", "Termo Destino", "Rendimiento Real", "Proceso Destino"]
                    st.session_state.filas_trazabilidad = filtrado_t[col_tabla_traz].to_dict('records')
                    st.success("¡Cargado con éxito en el formato imprimible!")
        else:
            st.write("Presiona el botón para consultar los registros históricos de procesos.")

    with tab_traz_impresion:
        traz_rows_html = ""
        filas_traz_imp = st.session_state.filas_trazabilidad.copy()
        
        while len(filas_traz_imp) < 18: filas_traz_imp.append({})
        
        for ft in filas_traz_imp:
            traz_rows_html += f"""
            <tr style="height: 22px;">
                <td style="border: 1px solid #000; font-size: 8.5pt;">{ft.get('Fecha Almacenamiento', '')}</td>
                <td style="border: 1px solid #000;">{ft.get('No. Termo', '')}</td>
                <td style="border: 1px solid #000; text-align: left; padding-left: 4px;">{ft.get('Descripcion', '')}</td>
                <td style="border: 1px solid #000;">{ft.get('Lote', '')}</td>
                <td style="border: 1px solid #000; font-size: 8pt;">{ft.get('Proceso Aplicado', '')}</td>
                <td style="border: 1px solid #000; font-weight: bold;">{f"{ft.get('Peso Inicial'):,.1f}" if ft.get('Peso Inicial') else ''}</td>
                <td style="border: 1px solid #000; font-weight: bold;">{f"{ft.get('Peso Final'):,.1f}" if ft.get('Peso Final') else ''}</td>
                <td style="border: 1px solid #000;">{ft.get('Termo Destino', '')}</td>
                <td style="border: 1px solid #000; font-weight: bold;">{ft.get('Rendimiento Real', '')}</td>
                <td style="border: 1px solid #000; font-size: 8pt;">{ft.get('Proceso Destino', '')}</td>
            </tr>
            """
            
        documento_traz_html = f"""
        <html><head><style>
            @media print {{ 
                button {{ display: none !important; }} 
                body {{ background-color: white; color: black; padding: 0; margin: 0; }} 
                @page {{ size: letter landscape; margin: 0.15in; }}
            }}
            body {{ font-family: 'Arial', sans-serif; background-color: #fafafa; margin: 0; padding: 2px; }}
            #hoja-trazabilidad {{ background: white; width: 11.1in; height: auto; min-height: 5.5in; margin: 0 auto; box-sizing: border-box; padding: 6px; display: flex; flex-direction: column; justify-content: flex-start; color: black; border: 1px solid #000; }}
            .header-table {{ margin-bottom: 8px; width: 100%; border-collapse: collapse; }}
            .grid-traz {{ display: grid; grid-template-columns: 1.2fr 1fr 1fr 1.8fr; border: 1px solid #000; padding: 5px; font-size: 9pt; margin-bottom: 8px; line-height: 1.4; }}
            table {{ table-layout: fixed; width: 100%; border-collapse: collapse; text-align: center; font-size: 8.5pt; }}
            th, td {{ border: 1px solid #000; overflow: hidden; }}
            .obs-title {{ font-size: 8.5pt; font-weight: bold; margin-top: 4px; line-height: 1.4; text-align: justify; width: 100%; word-break: break-all; }}
            .custom-traz-footer {{ font-size: 7.2pt; line-height: 1.4; font-weight: normal; margin-top: 10px; text-align: justify; }}
        </style></head><body>
            <div style="text-align: center; margin-bottom: 4px;"><button onclick="window.print();" style="background-color: #124491; color: white; border: none; padding: 6px 16px; font-weight: bold; cursor: pointer; font-size:11pt;">🖨️ IMPRIMIR / GUARDAR PDF TRAZABILIDAD</button></div>
            <div id="hoja-trazabilidad">
                <div>
                    <table class="header-table">
                        <tr>
                            <td style="width: 14%; padding: 1px;">{LOGO_NICALAPIA_SVG}</td>
                            <td style="width: 64%; vertical-align: middle;">
                                <span style="font-size: 13.5pt; font-weight: bold;">Nicaraguan Tilapia (Nicalapia S.A)</span><br>
                                <span style="font-size: 11pt; font-weight: bold; letter-spacing: 0.2px;">FORMATO DE CONTROL DE TRAZABILIDAD DE PRODUCTO EN PROCESO</span>
                            </td>
                            <td style="width: 22%; font-size: 8.5pt; font-weight: bold; text-align: left; padding-left: 8px; line-height: 1.3; border-left: 2px solid #000;">CODIGO: FT-PROD-03<br>FECHA ULTIMA VERSION:<br>Julio 2026<br>Versión: 1</td>
                        </tr>
                    </table>
                    <div class="grid-traz">
                        <div><b>FECHA:</b> {traz_fecha.strftime('%d/%m/%Y')}</div>
                        <div><b>Hora Inicio:</b> {st.session_state.traz_hora_inicio}</div>
                        <div><b>Hora Final:</b> {st.session_state.traz_hora_fin}</div>
                        <div><b>ELABORADO POR:</b> {st.session_state.traz_elaborado}</div>
                    </div>
                    <table>
                        <colgroup>
                            <col style="width: 11%;"><col style="width: 8%;"><col style="width: 21%;"><col style="width: 9%;"><col style="width: 14%;"><col style="width: 8%;"><col style="width: 8%;"><col style="width: 8%;"><col style="width: 10%;"><col style="width: 13%;">
                        </colgroup>
                        <thead>
                            <tr style="background-color: #f2f2f2; height: 28px; font-size: 8.5pt;">
                                <th>FECHA DE<br>Almacenamiento</th><th>No. DE<br>TERMO</th><th>DESCRIPCION DEL PRODUCTO</th><th>LOTE</th><th>FECHA Y TIPO DE<br>PROCESO APLICADO</th><th>PESO INICIAL</th><th>PESO FINAL</th><th>N° DE TERMO<br>DESTINO</th><th>RENDIMIENTO<br>AUTOMÁTICO</th><th>FECHA Y PROCESO<br>DESTINO</th>
                            </tr>
                        </thead>
                        <tbody>{traz_rows_html}</tbody>
                    </table>
                </div>
                
                <div class="obs-title">
                    <b>OBSERVACIONES:</b> <b>________________________________________________________________________________________________________________________________________________________</b>
                    <b>___________________________________________________________________________________________________________________________________________________________________________________________________________________</b>

                    
                    <table style="border: none; margin-top: 15px; margin-bottom: 5px; width: 100%;">
                        <tr style="background: none;">
                            <td style="border: none; text-align: left; font-size: 9pt; padding: 0;"><b>Supervisado por:</b> ___________________________</td>
                            <td style="border: none; text-align: right; font-size: 9pt; padding: 0;"><b>Verificado por:</b> ___________________________</td>

                        </tr>
                    </table>
                    
                    <hr style="border: 0; border-top: 1px solid #000; margin-top: 15px; margin-bottom: 10px;">
                    
                    <div class="custom-traz-footer">
                        <b>Frecuencia del monitoreo:</b> Cada vez que se procesen productos en las Áreas de Almacenamiento Materia Prima, Procesos Varios, Fileteo, Empaque Al Vacío, Empaque Congelado.&nbsp;&nbsp;&nbsp;&nbsp;<b>Temperatura:</b> inferior a &le; -4.0°C.<br>
                        <span style="font-weight: bold;">Elaborado el 09/08/2024</span>
                        <div style="text-align: center; font-weight: bold; margin-top: 4px;">
                            Este Documento es propiedad de Nicaraguan Tilapia (Nicalapia S.A). Queda prohibida su reproducción total o parcial sin la autorización expresa de las autoridades superiores.
                        </div>
                    </div>
                </div>
            </div></body></html>
        """
        components.html(documento_traz_html, height=750, scrolling=True)