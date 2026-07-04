import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Nicalapia - Control de Recepciones", page_icon="🐟", layout="wide")

# LISTAS PREDETERMINADAS
PROVEEDORES_LISTA = ["Chester Espinoza", "Distribuidora del Mar", "Cooperativa Masachapa", "Darvin Lopez", "➕ Escribir manualmente..."]
ZONAS_LISTA = ["Masachapa", "Casares", "San Juan del Sur", "Granja interna", "Las Poritas", "➕ Escribir manualmente..."]
PERSONAL_LISTA = ["W. Solis / E. Palacios", "Maikelyn Zelaya", "D. Fonseca / M. Morales", "Alice Mendoza", "➕ Escribir manualmente..."]
ESPECIES_LISTA = ["Macuá 1-2", "Macuá 2-4", "Macuá 4-6", "C/Amarilla 2-4", "C/Amarilla 4-6", "Dientón 1-3", "Dientón 3-5", "Guacamayo 1-3", "➕ Escribir manualmente..."]

# --- BASE DE DATOS EN MEMORIA ---
if 'historial_recepciones' not in st.session_state:
    st.session_state.historial_recepciones = {}
if 'id_actual' not in st.session_state:
    st.session_state.id_actual = "REC-" + datetime.now().strftime("%Y%m%d-%H%M%S")
if 'filas_actuales' not in st.session_state:
    st.session_state.filas_actuales = []
if 'hora_inicio' not in st.session_state:
    st.session_state.hora_inicio = ""
if 'hora_fin' not in st.session_state:
    st.session_state.hora_fin = ""

st.title("🐟 Sistema de Gestión de Recepciones - Nicalapia S.A.")

# ==========================================
# BARRA LATERAL: HISTORIAL Y ACCIONES
# ==========================================
with st.sidebar:
    st.header("📂 Historial de Turno")
    
    if st.button("➕ INICIAR NUEVA RECEPCIÓN", use_container_width=True, type="primary"):
        if st.session_state.filas_actuales:
            st.session_state.historial_recepciones[st.session_state.id_actual] = {
                "encabezado": {"inicio": st.session_state.hora_inicio, "fin": st.session_state.hora_fin},
                "filas": st.session_state.filas_actuales
            }
        st.session_state.id_actual = "REC-" + datetime.now().strftime("%Y%m%d-%H%M%S")
        st.session_state.filas_actuales = []
        st.session_state.hora_inicio = ""
        st.session_state.hora_fin = ""
        st.rerun()
        
    st.write("---")
    st.subheader("📝 Editar / Ver Anteriores")
    
    opciones_recepcion = list(st.session_state.historial_recepciones.keys())
    if st.session_state.id_actual not in opciones_recepcion:
        opciones_recepcion.insert(0, f"{st.session_state.id_actual} (En proceso...)")
        
    seleccion = st.selectbox("Seleccione Recepción para trabajar/editar:", opciones_recepcion)
    
    id_seleccionado = seleccion.split(" ")[0]
    if id_seleccionado != st.session_state.id_actual and id_seleccionado in st.session_state.historial_recepciones:
        if st.button("🔄 Cargar para Editar/Imprimir"):
            if st.session_state.filas_actuales:
                st.session_state.historial_recepciones[st.session_state.id_actual] = {
                    "encabezado": {"inicio": st.session_state.hora_inicio, "fin": st.session_state.hora_fin},
                    "filas": st.session_state.filas_actuales
                }
            datos_viejos = st.session_state.historial_recepciones[id_seleccionado]
            st.session_state.id_actual = id_seleccionado
            st.session_state.filas_actuales = datos_viejos["filas"]
            st.session_state.hora_inicio = datos_viejos["encabezado"]["inicio"]
            st.session_state.hora_fin = datos_viejos["encabezado"]["fin"]
            st.rerun()

st.info(f"Trabajando en la Recepción Código: **{st.session_state.id_actual}**")

tab_datos, tab_registro, tab_impresion = st.tabs(["📋 1. Encabezado y Tiempos", "⚖️ 2. Registro de Pesajes", "🖨️ 3. Reporte Imprimible Oficial"])

# ==========================================
# PESTAÑA 1: ENCABEZADO
# ==========================================
with tab_datos:
    st.subheader("Datos de Control")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        prov_sel = st.selectbox("Proveedor:", PROVEEDORES_LISTA, key="prov")
        proveedor = st.text_input("Escriba Proveedor Manual:", value="Darvin Lopez") if prov_sel == "➕ Escribir manualmente..." else prov_sel
        zona_sel = st.selectbox("Zona de Pesca:", ZONAS_LISTA, key="zona")
        zona = st.text_input("Escriba Zona Manual:", value="Las Poritas") if zona_sel == "➕ Escribir manualmente..." else zona_sel
        granja = st.text_input("Nombre de la Granja:", value="N/A")
        
    with col2:
        rec_sel = st.selectbox("Recibidor / Pesador:", PERSONAL_LISTA, index=2, key="rec")
        recibidor = st.text_input("Escriba Recibidor Manual:", value="D. Fonseca / M. Morales") if rec_sel == "➕ Escribir manualmente..." else rec_sel
        elab_sel = st.selectbox("Elaborado Por:", PERSONAL_LISTA, index=3, key="elab")
        elaborado = st.text_input("Escriba Elaborador Manual:", value="Alice Mendoza") if elab_sel == "➕ Escribir manualmente..." else elab_sel
        carta = st.selectbox("Carta de Garantía:", ["SI", "NO"])
        
    with col3:
        histaminico = st.selectbox("Producto Histamínico:", ["NO", "SI", "N/A"])
        st.write("---")
        st.markdown("**Control de Reloj de Planta (Ingreso Manual)**")
        
        hora_ini_input = st.text_input("Hora Inicio (ej: 05:00 PM):", value=st.session_state.hora_inicio)
        if hora_ini_input != st.session_state.hora_inicio:
            st.session_state.hora_inicio = hora_ini_input
            
        hora_fin_input = st.text_input("Hora Final (ej: 08:20 PM):", value=st.session_state.hora_fin)
        if hora_fin_input != st.session_state.hora_fin:
            st.session_state.hora_fin = hora_fin_input

# ==========================================
# PESTAÑA 2: REGISTRO DE PESAJES
# ==========================================
with tab_registro:
    st.subheader("Ingreso / Edición de Pesos")
    
    lote_sugerido = st.session_state.filas_actuales[-1]['Lote'] if st.session_state.filas_actuales else "11-14-772-22-26-03"
    termo_sugerido = st.session_state.filas_actuales[-1]['Nº Termos'] if st.session_state.filas_actuales else "059"
    
    with st.form("registro_especie", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        with c1:
            esp_sel = st.selectbox("Especie / Talla:", ESPECIES_LISTA)
            especie = st.text_input("Escriba Especie Manual:") if esp_sel == "➕ Escribir manualmente..." else esp_sel
            lote = st.text_input("Lote:", value=lote_sugerido)
        with c2:
            termo = st.text_input("Nº Termos:", value=termo_sugerido)
            temp = st.number_input("Temperatura (ºC):", min_value=-5.0, max_value=30.0, value=1.1, step=0.1)
        with c3:
            st.markdown("**Evaluación Sensorial**")
            olor = st.selectbox("Olor:", ["E", "B", "MB", "N/A"])
            color = st.selectbox("Color:", ["E", "B", "MB", "N/A"])
        with c4:
            st.markdown("** **")
            textura = st.selectbox("Textura:", ["E", "B", "MB", "N/A"])
            sabor = st.selectbox("Sabor:", ["N/A", "C", "NC", "MP"])
            
        st.markdown("**Pesos Manuales (Lbs)**")
        pw1, pw2, pw3, pw4, pw5, pw6, pw7, pw8 = st.columns(8)
        p1 = pw1.number_input("P1", min_value=0.0, value=0.0, step=0.1)
        p2 = pw2.number_input("P2", min_value=0.0, value=0.0, step=0.1)
        p3 = pw3.number_input("P3", min_value=0.0, value=0.0, step=0.1)
        p4 = pw4.number_input("P4", min_value=0.0, value=0.0, step=0.1)
        p5 = pw5.number_input("P5", min_value=0.0, value=0.0, step=0.1)
        p6 = pw6.number_input("P6", min_value=0.0, value=0.0, step=0.1)
        p7 = pw7.number_input("P7", min_value=0.0, value=0.0, step=0.1)
        p8 = pw8.number_input("P8", min_value=0.0, value=0.0, step=0.1)
        
        if st.form_submit_button("➕ AGREGAR / ACTUALIZAR FILA"):
            if especie:
                pesos_lista = [p for p in [p1, p2, p3, p4, p5, p6, p7, p8]]
                nueva_fila = {
                    "Especie/Talla": especie, "Lote": lote, "Olor": olor, "Color": color,
                    "Textura": textura, "Sabor": sabor, "Nº Termos": termo, "ºC": temp
                }
                for idx, p in enumerate(pesos_lista, 1):
                    nueva_fila[f"Peso {idx}"] = p if p > 0 else ""
                    
                st.session_state.filas_actuales.append(nueva_fila)
                st.session_state.historial_recepciones[st.session_state.id_actual] = {
                    "encabezado": {"inicio": st.session_state.hora_inicio, "fin": st.session_state.hora_fin},
                    "filas": st.session_state.filas_actuales
                }
                st.rerun()

    if st.session_state.filas_actuales:
        st.markdown("### 📊 Registros de esta entrega")
        df_edit = pd.DataFrame(st.session_state.filas_actuales).fillna("")
        st.dataframe(df_edit, use_container_width=True)
        
        col_del, _ = st.columns([2, 6])
        with col_del:
            fila_eliminar = st.number_input("Número de fila a eliminar:", min_value=0, max_value=len(st.session_state.filas_actuales)-1, step=1)
            if st.button("🗑️ Eliminar Fila Seleccionada", type="secondary"):
                st.session_state.filas_actuales.pop(int(fila_eliminar))
                st.session_state.historial_recepciones[st.session_state.id_actual]["filas"] = st.session_state.filas_actuales
                st.rerun()

# ==========================================
# PESTAÑA 3: IMPRESIÓN CON EVALUACIÓN DINÁMICA DE CASILLAS [X]
# ==========================================
with tab_impresion:
    if st.session_state.filas_actuales:
        gran_total_libras = 0.0
        html_rows = ""
        
        filas_imprimir = st.session_state.filas_actuales.copy()
        while len(filas_imprimir) < 12:
            filas_imprimir.append({})

        for f in filas_imprimir:
            suma_fila = 0.0
            if f:
                for i in range(1, 9):
                    val = f.get(f"Peso {i}", "")
                    if val != "":
                        suma_fila += float(val)
                gran_total_libras += suma_fila
            
            txt_suma_fila = f"{suma_fila:,.1f}" if f and suma_fila > 0 else ""

            html_rows += f"""
            <tr style="height: 25px;">
                <td style="border: 1px solid #000; text-align: left; padding-left: 5px; font-weight: bold;">{f.get('Especie/Talla', '')}</td>
                <td style="border: 1px solid #000; font-size: 7.5pt;">{f.get('Lote', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Olor', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Color', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Textura', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Sabor', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Nº Termos', '')}</td>
                <td style="border: 1px solid #000; font-weight: bold;">{f.get('ºC', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Peso 1', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Peso 2', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Peso 3', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Peso 4', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Peso 5', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Peso 6', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Peso 7', '')}</td>
                <td style="border: 1px solid #000;">{f.get('Peso 8', '')}</td>
                <td style="border: 1px solid #000; font-weight: bold; background-color: #f5f5f5;">{txt_suma_fila}</td>
            </tr>
            """

        fecha_hoy = datetime.now().strftime("%d/%m/%y")
        
        # --- LÓGICA DE DETECCIÓN DINÁMICA DE MARCADORES [X] ---
        # Carta de Garantía
        carta_si = "[X] SI" if carta == "SI" else "[ &nbsp;] SI"
        carta_no = "[X] NO" if carta == "NO" else "[ &nbsp;] NO"
        
        # Producto Histamínico
        hist_si  = "[X] SI" if histaminico == "SI" else "[ &nbsp;] SI"
        hist_no  = "[X] NO" if histaminico == "NO" else "[ &nbsp;] NO"
        hist_na  = "[X] N/A" if histaminico == "N/A" else "[ &nbsp;] N/A"

        # LOGO VECTORIAL DETALLADO CON NUEVO HEIGHT="90"
        logo_nicalapia_svg = """
        <svg width="105" height="90" viewBox="15 15 90 90" xmlns="http://www.w3.org/2000/svg" style="display: block; margin: 0 auto;">
            <path d="M 20 62 A 40 40 0 1 1 100 62" fill="none" stroke="#124491" stroke-width="3.5" stroke-linecap="round"/>
            <circle cx="74" cy="40" r="4.5" fill="#124491"/>
            <path d="M 22 61 L 45 32 L 61 56" fill="none" stroke="#124491" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M 53 51 L 68 41 L 98 61" fill="none" stroke="#124491" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M 23 67 Q 27 64 31 67 T 39 67 T 47 67 T 55 67 T 63 67 T 71 67 T 79 67 T 87 67 T 97 67" fill="none" stroke="#124491" stroke-width="2.8" stroke-linecap="round"/>
            <path d="M 25 73 Q 29 70 33 73 T 41 73 T 49 73 T 57 73 T 65 73 T 73 73 T 81 73 T 89 73 T 95 73" fill="none" stroke="#124491" stroke-width="2.8" stroke-linecap="round"/>
            <path d="M 29 79 Q 33 76 37 79 T 45 79 T 53 79 T 61 79 T 69 79 T 77 79 T 85 79 T 91 79" fill="none" stroke="#124491" stroke-width="2.8" stroke-linecap="round"/>
            <path d="M 37 85 Q 41 82 45 85 T 53 85 T 61 85 T 69 85 T 77 85 T 83 85" fill="none" stroke="#124491" stroke-width="2.8" stroke-linecap="round"/>
            <text x="60" y="104" font-family="'Brush Script MT', 'Comic Sans MS', cursive, sans-serif" font-size="22" font-weight="bold" fill="#124491" text-anchor="middle" font-style="italic">Nicalapia</text>
        </svg>
        """

        documento_imprimible = f"""
        <html>
        <head>
            <style>
                @media print {{
                    button {{ display: none !important; }}
                    body {{ background-color: white; color: black; padding: 0; margin: 0; -webkit-print-color-adjust: exact; }}
                }}
                .grid-container {{
                    display: grid;
                    grid-template-columns: 1fr 1fr 1fr;
                    gap: 10px;
                    border: 1px solid #000;
                    padding: 8px;
                    margin-bottom: 10px;
                    font-size: 8.5pt;
                }}
                .grid-cell {{ line-height: 1.6; }}
            </style>
        </head>
        <body>
            <div style="text-align: center; margin-bottom: 10px;">
                <button onclick="window.print();" style="background-color: #124491; color: white; border: none; padding: 10px 20px; font-size: 13px; font-weight: bold; border-radius: 4px; cursor: pointer;">
                    🖨️ IMPRIMIR FORMATO OFICIAL FT-HACCP-005
                </button>
            </div>
            
            <div id="hoja-oficial" style="font-family: 'Arial', sans-serif; padding: 5px; background-color: white; color: black; font-size: 8.5pt;">
                
                <!-- ENCABEZADO TRIPLE RECUADRO -->
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 8px;">
                    <tr>
                        <td style="border: 2px solid #000; width: 18%; text-align: center; padding: 4px; vertical-align: middle;">
                            {logo_nicalapia_svg}
                        </td>
                        <td style="border: 2px solid #000; width: 64%; text-align: center; padding: 4px; vertical-align: middle;">
                            <span style="font-size: 10.5pt; font-weight: bold;">Nicaraguan Tilapia (Nicalapia S.A)</span><br>
                            <span style="font-size: 11.5pt; font-weight: bold; letter-spacing: 0.3px;">FORMATO: CLASIFICACION Y RECEPCION DE MATERIA PRIMA</span>
                        </td>
                        <td style="border: 2px solid #000; width: 18%; font-size: 8pt; font-weight: bold; padding: 6px; line-height: 1.4; vertical-align: middle;">
                            CODIGO: FT-HACCP-005<br>
                            FECHA ULTIMA VERSION:<br>Mayo 2026<br>
                            Versión: 1
                        </td>
                    </tr>
                </table>
                
                <!-- RECUADRO DE DATOS DE ORIGEN Y TIEMPOS CON CASILLAS INTEGRADAS -->
                <div class="grid-container">
                    <div class="grid-cell">
                        <b>FECHA/HORA DE RECEPCION:</b> {fecha_hoy}<br>
                        <b>NOMBRE DE LA GRANJA:</b> {granja}<br>
                        <b>PROVEEDOR:</b> {proveedor}
                    </div>
                    <div class="grid-cell">
                        <b>ZONA DE PESCA:</b> {zona}<br>
                        <b>CARTA DE GARANTIA:</b> {carta_si} &nbsp;&nbsp; {carta_no}<br>
                        <b>PRODUCTO HISTAMINICO:</b> {hist_si} &nbsp;&nbsp; {hist_no} &nbsp;&nbsp; {hist_na}
                    </div>
                    <div class="grid-cell">
                        <b>HORA INICIO:</b> {st.session_state.hora_inicio}<br>
                        <b>HORA FINAL:</b> {st.session_state.hora_fin}<br>
                        <b>RECIBIDOR/PESADOR:</b> {recibidor}<br>
                        <b>ELABORADO POR:</b> {elaborado}
                    </div>
                </div>

                <!-- TABLA PRINCIPAL DE PESOS -->
                <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 8pt; border: 2px solid #000;">
                    <thead>
                        <tr style="background-color: #f2f2f2; height: 20px;">
                            <th rowspan="2" style="border: 1px solid #000; width: 15%;">ESPECIE/TALLA</th>
                            <th rowspan="2" style="border: 1px solid #000; width: 12%;">LOTE</th>
                            <th colspan="4" style="border: 1px solid #000;">EVALUACION SENSORIAL</th>
                            <th rowspan="2" style="border: 1px solid #000; width: 5%;">No<br>TERMOS</th>
                            <th rowspan="2" style="border: 1px solid #000; width: 4%;">ºC</th>
                            <th colspan="8" style="border: 1px solid #000;">PESO (Lbs)</th>
                            <th rowspan="2" style="border: 1px solid #000; width: 8%; background-color: #f2f2f2;">TOTAL</th>
                        </tr>
                        <tr style="background-color: #f2f2f2; height: 20px;">
                            <th style="border: 1px solid #000; font-size: 7pt;">OLOR</th>
                            <th style="border: 1px solid #000; font-size: 7pt;">COLOR</th>
                            <th style="border: 1px solid #000; font-size: 7pt;">TEXRURA</th>
                            <th style="border: 1px solid #000; font-size: 7pt;">SABOR</th>
                            <th style="border: 1px solid #000; width: 4.5%;">1</th>
                            <th style="border: 1px solid #000; width: 4.5%;">2</th>
                            <th style="border: 1px solid #000; width: 4.5%;">3</th>
                            <th style="border: 1px solid #000; width: 4.5%;">4</th>
                            <th style="border: 1px solid #000; width: 4.5%;">5</th>
                            <th style="border: 1px solid #000; width: 4.5%;">6</th>
                            <th style="border: 1px solid #000; width: 4.5%;">7</th>
                            <th style="border: 1px solid #000; width: 4.5%;">8</th>
                        </tr>
                    </thead>
                    <tbody>
                        {html_rows}
                        <tr style="height: 25px; background-color: #f2f2f2; font-weight: bold; border-top: 2px solid #000;">
                            <td colspan="16" style="border: 1px solid #000; text-align: right; padding-right: 15px;">TOTAL:</td>
                            <td style="border: 1px solid #000; font-size: 9pt; color: #000;">{gran_total_libras:,.1f}</td>
                        </tr>
                    </tbody>
                </table>

                <!-- SECCIÓN INFERIOR DE NOTAS Y CONTROLES -->
                <div style="margin-top: 8px; font-size: 7.75 pt; line-height: 1.16; text-align: justify;">
                    <b>Evaluación Sensorial:</b> B: Bueno, MB: Muy Bueno; E: Excelente; N/A: No Aplica; AC: Acción Correctiva; <b>SABOR:</b> C: caracteristico, NC: No Conforme, MP: materia prima.<br>
                    <b>Observaciones:</b> ________________________________________________________________________________________________________________________________________________________________________________________________________<br><br>
                    </b> __________________________________________________________________________________________________________________________________________________________________________________________<br><br>
                    </b> __________________________________________________________________________________________________________________________________________________________________________________________<br><br>
    
                    <!-- FIRMAS -->
                    <table style="width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 12px; text-align: center; font-size: 7.5pt;">
                        <tr>
                            <td style="width: 33%; border: none; padding-top: 25px;">___________________________<br><b>ENTREGADO POR:</b></td>
                            <td style="width: 34%; border: none; padding-top: 25px;">___________________________<br><b>SUPERVISADO POR:</b></td>
                            <td style="width: 33%; border: none; padding-top: 25px;">___________________________<br><b>VERIFICADO POR:</b></td>
                        </tr>
                    </table>

                    <b>Limite crítico:</b> Temperatura del producto &le; 4.0°C;<br>
                    <b>Frecuencia del monitoreo:</b> En cada recepción de materia prima, por cada 2 cajillas pesadas se verifica la temperatura. Cada vez que se recibe MP se hace la evaluación sensorial a cada unidad recibida, si no cumple con los parámetros sensoriales el producto se rechaza.<br>
                    <span style="font-size: 6.5pt; color: #555; display: block; margin-top: 4px;">Modificado el 16/12/2024 // Modificado 19/03/2026 // Modificado 14/05/2026</span>
                </div>

                <!-- PIE DE PÁGINA -->
                <div style="border-top: 1px solid #000; margin-top: 6px; padding-top: 4px; font-size: 6.5pt; text-align: center; font-style: italic;">
                    Este Documento es propiedad de Nicaraguan Tilapia (Nicalapia S.A). Queda prohibida su reproducción total o parcial sin la autorización expresa de las autoridades superiores.
                </div>

            </div>
        </body>
        </html>
        """
        components.html(documento_imprimible, height=760, scrolling=True)
    else:
        st.warning("⚠️ No hay pesos registrados en esta recepción para poder generar una hoja de impresión.")
