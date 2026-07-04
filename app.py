import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Nicalapia - Control y Trazabilidad", page_icon="🐟", layout="wide")

# ==========================================
# LISTAS PREDETERMINADAS
# ==========================================
PROVEEDORES_LISTA = ["Chester Espinoza", "Distribuidora del Mar", "Cooperativa Masachapa", "Darvin Lopez", "➕ Escribir manualmente..."]
ZONAS_LISTA = ["Masachapa", "Casares", "San Juan del Sur", "Granja interna", "Las Poritas", "➕ Escribir manualmente..."]
PERSONAL_LISTA = ["W. Solis / E. Palacios", "Maikelyn Zelaya", "D. Fonseca / M. Morales", "Alice Mendoza", "➕ Escribir manualmente..."]
ESPECIES_LISTA = ["Macuá 1-2", "Macuá 2-4", "Macuá 4-6", "C/Amarilla 2-4", "C/Amarilla 4-6", "Dientón 1-3", "Dientón 3-5", "Guacamayo 1-3", "➕ Escribir manualmente..."]

# Lista de Sugerencias para Trazabilidad (Módulo 2)
PRODUCTOS_TRAZABILIDAD_LISTA = [
    "Filete de Tilapia Fresh 2-4 oz", 
    "Filete de Tilapia Fresh 4-6 oz", 
    "Macuá Entero Eviscerado", 
    "➕ Escribir manualmente..."
]

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

# --- BASE DE DATOS PARA TRAZABILIDAD ---
if 'filas_trazabilidad' not in st.session_state:
    st.session_state.filas_trazabilidad = []
if 'traz_hora_inicio' not in st.session_state:
    st.session_state.traz_hora_inicio = ""
if 'traz_hora_fin' not in st.session_state:
    st.session_state.traz_hora_fin = ""
if 'traz_elaborado' not in st.session_state:
    st.session_state.traz_elaborado = ""

# LOGO VECTORIAL REUTILIZABLE
LOGO_NICALAPIA_SVG = """
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

# ==========================================
# MENÚ PRINCIPAL LATERAL
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3062/3062234.png", width=60)
    st.title("Nicalapia S.A.")
    modulo = st.radio("SELECCIONE EL MÓDULO:", ["📊 Recepción de Materia Prima", "🔍 Seguimiento de Trazabilidad"])
    st.write("---")

# ==============================================================================
# MÓDULO 1: RECEPCIÓN DE MATERIA PRIMA
# ==============================================================================
if modulo == "📊 Recepción de Materia Prima":
    st.title("🐟 Gestión de Recepciones - Materia Prima")
    
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
            if hora_ini_input != st.session_state.hora_inicio: st.session_state.hora_inicio = hora_ini_input
            hora_fin_input = st.text_input("Hora Final (ej: 08:20 PM):", value=st.session_state.hora_fin)
            if hora_fin_input != st.session_state.hora_fin: st.session_state.hora_fin = hora_fin_input

    with tab_registro:
        st.subheader("Ingreso / Edición de Pesos")
        lote_sugerido = st.session_state.filas_actuales[-1]['Lote'] if st.session_state.filas_actuales else "11-14-772-22-26-03"
        termo_sugerido = st.session_state.filas_actuales[-1]['Nº Termos'] if st.session_state.filas_actuales else "059"
        
        with st.form("registro_especie", clear_on_submit=True):
            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
            with c1:
                esp_sel = st.selectbox("Especie / Talla:", ESPECIES_LISTA)
                especie_manual = st.text_input("Escriba Especie Manual (si aplica):")
                especie = especie_manual if esp_sel == "➕ Escribir manualmente..." else esp_sel
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
                    pesos_lista = [p1, p2, p3, p4, p5, p6, p7, p8]
                    nueva_fila = {
                        "Especie/Talla": especie, "Lote": lote, "Olor": olor, "Color": color,
                        "Textura": textura, "Sabor": sabor, "Nº Termos": termo, "ºC": temp
                    }
                    for idx, p in enumerate(pesos_lista, 1):
                        nueva_fila[f"Peso {idx}"] = p if p > 0 else ""
                    st.session_state.filas_actuales.append(nueva_fila)
                    st.rerun()

        if st.session_state.filas_actuales:
            st.markdown("### 📊 Registros de esta entrega")
            df_edit = pd.DataFrame(st.session_state.filas_actuales).fillna("")
            st.dataframe(df_edit, use_container_width=True)
            
            col_del, _ = st.columns([2, 6])
            with col_del:
                fila_eliminar = st.number_input("Número de fila a eliminar:", min_value=0, max_value=len(st.session_state.filas_actuales)-1, step=1)
                if st.button("🗑️ Eliminar Fila Seleccionada"):
                    st.session_state.filas_actuales.pop(int(fila_eliminar))
                    st.rerun()

    with tab_impresion:
        if st.session_state.filas_actuales:
            gran_total_libras = 0.0
            html_rows = ""
            filas_imprimir = st.session_state.filas_actuales.copy()
            while len(filas_imprimir) < 12: filas_imprimir.append({})

            for f in filas_imprimir:
                suma_fila = 0.0
                if f:
                    for i in range(1, 9):
                        val = f.get(f"Peso {i}", "")
                        if val != "": suma_fila += float(val)
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
                    {"".join([f'<td style="border: 1px solid #000;">{f.get(f"Peso {i}", "")}</td>' for i in range(1,9)])}
                    <td style="border: 1px solid #000; font-weight: bold; background-color: #f5f5f5;">{txt_suma_fila}</td>
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
                @media print {{ button {{ display: none !important; }} body {{ background-color: white; color: black; padding: 0; margin: 0; }} }}
                .grid-container {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; border: 1px solid #000; padding: 8px; font-size: 8.5pt; margin-bottom: 10px;}}
                .grid-cell {{ line-height: 1.6; }}
            </style></head><body>
                <div style="text-align: center; margin-bottom: 10px;"><button onclick="window.print();" style="background-color: #124491; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 4px; cursor: pointer;">🖨️ IMPRIMIR FORMATO OFICIAL FT-HACCP-005</button></div>
                <div id="hoja-oficial" style="font-family: 'Arial', sans-serif; padding: 5px; font-size: 8.5pt; color: black; background-color: white;">
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 8px;">
                        <tr>
                            <td style="border: 2px solid #000; width: 18%; text-align: center;">{LOGO_NICALAPIA_SVG}</td>
                            <td style="border: 2px solid #000; width: 64%; text-align: center; vertical-align: middle;">
                                <span style="font-size: 10.5pt; font-weight: bold;">Nicaraguan Tilapia (Nicalapia S.A)</span><br>
                                <span style="font-size: 11.5pt; font-weight: bold;">FORMATO: CLASIFICACION Y RECEPCION DE MATERIA PRIMA</span>
                            </td>
                            <td style="border: 2px solid #000; width: 18%; font-size: 8pt; font-weight: bold; padding: 6px; line-height: 1.4;">CODIGO: FT-HACCP-005<br>VERSION: Mayo 2026<br>Versión: 1</td>
                        </tr>
                    </table>
                    <div class="grid-container">
                        <div class="grid-cell"><b>FECHA/HORA:</b> {fecha_hoy}<br><b>GRANJA:</b> {granja}<br><b>PROVEEDOR:</b> {proveedor}</div>
                        <div class="grid-cell"><b>ZONA DE PESCA:</b> {zona}<br><b>CARTA GARANTIA:</b> {carta_si} &nbsp;&nbsp; {carta_no}<br><b>HISTAMINICO:</b> {hist_si} &nbsp;&nbsp; {hist_no} &nbsp;&nbsp; {hist_na}</div>
                        <div class="grid-cell"><b>HORA INICIO:</b> {st.session_state.hora_inicio}<br><b>HORA FINAL:</b> {st.session_state.hora_fin}<br><b>PESADOR:</b> {recibidor}<br><b>ELABORADO:</b> {elaborado}</div>
                    </div>
                    <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 8pt; border: 2px solid #000;">
                        <thead>
                            <tr style="background-color: #f2f2f2; height: 20px;">
                                <th rowspan="2" style="border: 1px solid #000; width: 15%;">ESPECIE/TALLA</th><th rowspan="2" style="border: 1px solid #000; width: 12%;">LOTE</th><th colspan="4" style="border: 1px solid #000;">EVALUACION SENSORIAL</th><th rowspan="2" style="border: 1px solid #000; width: 5%;">No<br>TERMOS</th><th rowspan="2" style="border: 1px solid #000; width: 4%;">ºC</th><th colspan="8" style="border: 1px solid #000;">PESO (Lbs)</th><th rowspan="2" style="border: 1px solid #000; width: 8%;">TOTAL</th>
                            </tr>
                            <tr style="background-color: #f2f2f2; height: 20px;">
                                <th style="border: 1px solid #000; font-size: 7pt;">OLOR</th><th style="border: 1px solid #000; font-size: 7pt;">COLOR</th><th style="border: 1px solid #000; font-size: 7pt;">TEXRURA</th><th style="border: 1px solid #000; font-size: 7pt;">SABOR</th>
                                {"".join([f'<th style="border: 1px solid #000; width: 4.5%;">{i}</th>' for i in range(1,9)])}
                            </tr>
                        </thead>
                        <tbody>{html_rows}
                            <tr style="height: 25px; background-color: #f2f2f2; font-weight: bold;"><td colspan="16" style="border: 1px solid #000; text-align: right; padding-right: 15px;">TOTAL:</td><td style="border: 1px solid #000; font-size: 9pt;">{gran_total_libras:,.1f}</td></tr>
                        </tbody>
                    </table>
                    <div style="margin-top: 8px; font-size: 7.2pt; line-height: 1.35; text-align: justify;">
                        <b>Evaluación Sensorial:</b> B: Bueno, MB: Muy Bueno; E: Excelente; N/A: No Aplica; AC: Acción Correctiva; <b>SABOR:</b> C: caracteristico, NC: No Conforme, MP: materia prima.<br><b>Observaciones:</b> ____________________________________________________________________________________________________________________<br>
                        <table style="width: 100%; border-collapse: collapse; margin-top: 10px; text-align: center; font-size: 7.5pt;"><tr><td style="padding-top: 20px;">___________________________<br><b>ENTREGADO POR:</b></td><td style="padding-top: 20px;">___________________________<br><b>SUPERVISADO POR:</b></td><td style="padding-top: 20px;">___________________________<br><b>VERIFICADO POR:</b></td></tr></table>
                    </div>
                </div></body></html>
            """
            components.html(documento_imprimible, height=900, scrolling=True)

# ==============================================================================
# MÓDULO 2: SEGUIMIENTO DE TRAZABILIDAD
# ==============================================================================
else:
    st.title("🔍 Sistema de Seguimiento de Trazabilidad")
    
    tab_traz_datos, tab_traz_registro, tab_traz_impresion = st.tabs(["📋 1. Encabezado de Turno", "📐 2. Registro de Procesos", "🖨️ 3. Reporte de Trazabilidad"])
    
    with tab_traz_datos:
        st.subheader("Datos de Control de Trazabilidad")
        c1, c2, c3 = st.columns(3)
        with c1:
            traz_fecha = st.date_input("Fecha de Control:", value=datetime.now())
        with c2:
            st.session_state.traz_hora_inicio = st.text_input("Hora Inicio Proceso:", value=st.session_state.traz_hora_inicio, placeholder="ej: 06:00 AM")
            st.session_state.traz_hora_fin = st.text_input("Hora Final Proceso:", value=st.session_state.traz_hora_fin, placeholder="ej: 03:30 PM")
        with c3:
            st.session_state.traz_elaborado = st.text_input("Elaborado Por:", value=st.session_state.traz_elaborado)

    with tab_traz_registro:
        st.subheader("Ingreso de Datos de Cadena y Rendimiento")
        
        with st.form("form_trazabilidad", clear_on_submit=True):
            r1, r2, r3 = st.columns(3)
            with r1:
                f_almacenamiento = st.date_input("Fecha de Almacenamiento:")
                n_termo = st.text_input("No. de Termo:")
                prod_sel = st.selectbox("Seleccione Producto Base:", PRODUCTOS_TRAZABILIDAD_LISTA)
                especie_manual = st.text_input("Escriba Producto Manual (Si seleccionó la opción manual arriba):")
                desc_producto = especie_manual if prod_sel == "➕ Escribir manualmente..." else prod_sel
                
            with r2:
                lote_traz = st.text_input("Lote:")
                tipo_proceso = st.text_input("Fecha y Tipo de Proceso Aplicado:", placeholder="ej: 04/07 - Eviscerado")
                n_termo_destino = st.text_input("N° de Termo Destino:")
            with r3:
                p_inicial = st.number_input("Peso Inicial (Lbs):", min_value=0.0, step=0.1)
                p_final = st.number_input("Peso Final (Lbs):", min_value=0.0, step=0.1)
                proceso_destino = st.text_input("Fecha y Proceso Destino:", placeholder="ej: 05/07 - Congelación")
                
            if st.form_submit_button("➕ REGISTRAR FILA DE TRAZABILIDAD"):
                # Cálculo automático del rendimiento
                rend_real = (p_final / p_inicial * 100) if p_inicial > 0 else 0.0
                
                nueva_fila_traz = {
                    "Fecha Almacenamiento": f_almacenamiento.strftime("%d/%m/%Y"),
                    "No. Termo": n_termo,
                    "Descripcion": desc_producto,
                    "Lote": lote_traz,
                    "Proceso Aplicado": tipo_proceso,
                    "Peso Inicial": p_inicial,
                    "Peso Final": p_final,
                    "Termo Destino": n_termo_destino,
                    "Rendimiento Real": f"{rend_real:.1f}%",
                    "Proceso Destino": proceso_destino
                }
                st.session_state.filas_trazabilidad.append(nueva_fila_traz)
                st.rerun()

        if st.session_state.filas_trazabilidad:
            st.markdown("### 📊 Historial de Trazabilidad en este Turno")
            df_traz = pd.DataFrame(st.session_state.filas_trazabilidad)
            st.dataframe(df_traz, use_container_width=True)
            
            if st.button("🗑️ Vaciar todos los registros de Trazabilidad"):
                st.session_state.filas_trazabilidad = []
                st.rerun()

    with tab_traz_impresion:
        if st.session_state.filas_trazabilidad:
            traz_rows_html = ""
            filas_traz_imp = st.session_state.filas_trazabilidad.copy()
            while len(filas_traz_imp) < 15: filas_traz_imp.append({}) 
            
            for ft in filas_traz_imp:
                traz_rows_html += f"""
                <tr style="height: 25px;">
                    <td style="border: 1px solid #000; font-size: 8pt;">{ft.get('Fecha Almacenamiento', '')}</td>
                    <td style="border: 1px solid #000;">{ft.get('No. Termo', '')}</td>
                    <td style="border: 1px solid #000; text-align: left; padding-left: 4px;">{ft.get('Descripcion', '')}</td>
                    <td style="border: 1px solid #000;">{ft.get('Lote', '')}</td>
                    <td style="border: 1px solid #000; font-size: 7.5pt;">{ft.get('Proceso Aplicado', '')}</td>
                    <td style="border: 1px solid #000; font-weight: bold;">{f"{ft.get('Peso Inicial', ''):,.1f}" if ft.get('Peso Inicial') else ''}</td>
                    <td style="border: 1px solid #000; font-weight: bold;">{f"{ft.get('Peso Final', ''):,.1f}" if ft.get('Peso Final') else ''}</td>
                    <td style="border: 1px solid #000;">{ft.get('Termo Destino', '')}</td>
                    <td style="border: 1px solid #000; color: black; font-weight: bold;" colspan="2">{ft.get('Rendimiento Real', '')}</td>
                    <td style="border: 1px solid #000; font-size: 7.5pt;">{ft.get('Proceso Destino', '')}</td>
                </tr>
                """
                
            documento_traz_html = f"""
            <html><head><style>
                @media print {{ button {{ display: none !important; }} body {{ background-color: white; color: black; padding: 0; margin: 0; }} }}
                .grid-traz {{ display: grid; grid-template-columns: 1.2fr 1fr 1fr 1.8fr; border: 1px solid #000; padding: 6px; font-size: 8.5pt; margin-bottom: 8px; }}
            </style></head><body>
                <div style="text-align: center; margin-bottom: 10px;"><button onclick="window.print();" style="background-color: #124491; color: white; border: none; padding: 10px 20px; font-weight: bold; border-radius: 4px; cursor: pointer;">🖨️ IMPRIMIR REPORTE DE TRAZABILIDAD OFICIAL</button></div>
                <div style="font-family: 'Arial', sans-serif; padding: 5px; color: black; background-color: white;">
                    <table style="width: 100%; border-collapse: collapse; margin-bottom: 8px;">
                        <tr>
                            <td style="border: 2px solid #000; width: 18%; text-align: center;">{LOGO_NICALAPIA_SVG}</td>
                            <td style="border: 2px solid #000; width: 64%; text-align: center; vertical-align: middle;">
                                <span style="font-size: 11pt; font-weight: bold;">Nicaraguan Tilapia (Nicalapia S.A)</span><br>
                                <span style="font-size: 11.5pt; font-weight: bold; letter-spacing: 0.3px;">FORMATO DE CONTROL DE TRAZABILIDAD DE PRODUCTO EN PROCESO</span>
                            </td>
                            <td style="border: 2px solid #000; width: 18%; font-size: 8pt; font-weight: bold; padding: 6px;">CODIGO: FT-PROD-03<br>FECHA ULTIMA VERSION:<br>Julio 2026<br>Versión: 1</td>
                        </tr>
                    </table>
                    <div class="grid-traz">
                        <div><b>FECHA:</b> {traz_fecha.strftime('%d/%m/%Y')}</div>
                        <div><b>Hora Inicio:</b> {st.session_state.traz_hora_inicio}</div>
                        <div><b>Hora Final:</b> {st.session_state.traz_hora_fin}</div>
                        <div><b>ELABORADO POR:</b> {st.session_state.traz_elaborado}</div>
                    </div>
                    <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 7.8pt; border: 2px solid #000;">
                        <thead>
                            <tr style="background-color: #ffffff; height: 35px;">
                                <th style="border: 1px solid #000; width: 9%;">FECHA DE<br>Almacenamiento</th>
                                <th style="border: 1px solid #000; width: 7%;">No. DE<br>TERMO</th>
                                <th style="border: 1px solid #000; width: 22%;">DESCRIPCION DEL PRODUCTO</th>
                                <th style="border: 1px solid #000; width: 9%;">LOTE</th>
                                <th style="border: 1px solid #000; width: 14%;">FECHA Y TIPO DE<br>PROCESO APLICADO</th>
                                <th style="border: 1px solid #000; width: 7%;">PESO INICIAL</th>
                                <th style="border: 1px solid #000; width: 7%;">PESO FINAL</th>
                                <th style="border: 1px solid #000; width: 7%;">N° DE TERMO<br>DESTINO</th>
                                <th style="border: 1px solid #000; width: 10%;" colspan="2">RENDIMIENTO AUTOMÁTICO</th>
                                <th style="border: 1px solid #000; width: 12%;">FECHA Y PROCESO<br>DESTINO</th>
                            </tr>
                        </thead>
                        <tbody>{traz_rows_html}</tbody>
                    </table>
                    
                    <div style="margin-top: 15px; font-size: 8.5pt; font-family: 'Arial', sans-serif;">
                        <b>OBSERVACIONES:</b>____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________<br><br><br>
                        
                        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 8.5pt;">
                            <tr>
                                <td style="width: 50%; border: none;"><b>Supervisado por:</b> ______________________</td>
                                <td style="width: 50%; border: none; text-align: right;"><b>Verificado por:</b> ________________________</td>
                            </tr>
                        </table>
                    </div>
                </div></body></html>
            """
            components.html(documento_traz_html, height=900, scrolling=True)
        else:
            st.warning("⚠️ Agregue registros en la pestaña de procesamiento para ver la hoja de trazabilidad oficial.")
