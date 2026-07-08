from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def crear_presentacion_llamativa():
    archivo = "Presentacion_Llamativa_Nicalapia_BRCGS.pdf"
    c = canvas.Canvas(archivo, pagesize=landscape(letter))
    ancho, alto = landscape(letter)

    def aplicar_plantilla(titulo_pagina):
        # Fondo gris claro premium
        c.setFillColor(colors.HexColor("#f4f7fa"))
        c.rect(0, 0, ancho, alto, fill=1, stroke=0)
        # Barra superior Azul Corporativo
        c.setFillColor(colors.HexColor("#124491"))
        c.rect(0, alto - 60, ancho, 60, fill=1, stroke=0)
        # Título de la diapositiva
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 22)
        c.drawString(30, alto - 40, titulo_pagina)

    # ==========================================
    # LÁMINA 1: PORTADA REVOLUCIONADA
    # ==========================================
    c.setFillColor(colors.HexColor("#124491"))
    c.rect(0, 0, ancho, alto, fill=1, stroke=0)
    # Detalle en Cian Eléctrico
    c.setFillColor(colors.HexColor("#00e5ff"))
    c.rect(0, 0, 35, alto, fill=1, stroke=0)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 34)
    c.drawString(70, alto - 150, "Transformación Digital y Trazabilidad")
    c.setFont("Helvetica", 20)
    c.setFillColor(colors.HexColor("#00e5ff"))
    c.drawString(70, alto - 190, "Ecosistema Tecnológico de Cara a la Certificación BRCGS")
    
    c.setFont("Helvetica-Oblique", 13)
    c.setFillColor(colors.lightgrey)
    c.drawString(70, alto - 260, "Propuesta de Innovación de Procesos para: Gerencia Ejecutiva de Nicalapia S.A.")
    c.showPage()

    # ==========================================
    # LÁMINA 2: VENTAJAS OPERATIVAS (MÉTRICAS)
    # ==========================================
    aplicar_plantilla("Ventajas Operativas e Impacto Inmediato")
    c.setFillColor(colors.black)
    
    # Subtítulos y viñetas
    c.setFont("Helvetica-Bold", 15)
    c.drawString(40, alto - 110, "⚡ Ahorro de Tiempo de Trabajo (Reducción >70%)")
    c.setFont("Helvetica", 13)
    c.drawString(60, alto - 135, "- Automatización total de fórmulas complejas de rendimiento y balances de peso.")
    c.drawString(60, alto - 155, "- Eliminación definitiva de errores humanos en el cálculo manual de planta.")
    
    c.setFont("Helvetica-Bold", 15)
    c.drawString(40, alto - 200, "📊 Centralización Absoluta de la Información")
    c.setFont("Helvetica", 13)
    c.drawString(60, alto - 225, "- Integración unificada de los formatos FT-HACCP-005 y FT-PROD-03 en una sola app.")
    c.drawString(60, alto - 245, "- Toda la data fluye directo a una base de datos central en la nube.")
    
    c.setFont("Helvetica-Bold", 15)
    c.drawString(40, alto - 290, "🟢 Cultura Digital Sostenible (Planta 'Paperless')")
    c.setFont("Helvetica", 13)
    c.drawString(60, alto - 315, "- Fin de hojas físicas expuestas a pérdidas, humedad, daños o tachaduras.")
    c.showPage()

    # ==========================================
    # LÁMINA 3: ENFOQUE EN CERTIFICACIÓN BRCGS
    # ==========================================
    aplicar_plantilla("Pilar de Seguridad de Cara a la Certificación BRCGS")
    c.setFillColor(colors.black)
    
    c.setFont("Helvetica", 13)
    c.drawString(40, alto - 110, "La norma global BRCGS exige máxima rigurosidad técnica. Esta herramienta blinda la planta:")
    
    # Cuadro destacado
    c.setFillColor(colors.HexColor("#eef3fa"))
    c.rect(40, alto - 240, ancho - 80, 100, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#124491"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(60, alto - 175, "⚡ Prueba de Fuego: Speed Test de Masa Resuelto en Segundos")
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(60, alto - 200, "Ante auditorías imprevistas de la norma BRCGS, la reconstrucción de trazabilidad hacia atrás")
    c.drawString(60, alto - 215, "y hacia adelante se genera al instante de forma automatizada, transparente y sin fallas.")

    c.setFont("Helvetica", 13)
    c.drawString(40, alto - 280, "• Asegura la inalterabilidad de los registros históricos de control de calidad.")
    c.drawString(40, alto - 300, "• Proporciona evidencia sólida de monitoreo continuo las 24 horas ante inspectores.")
    c.showPage()

    # ==========================================
    # LÁMINA 4: FRAGMENTOS DE LA APP Y MAQUETA UI
    # ==========================================
    aplicar_plantilla("Módulos del Sistema y Fragmentos de Lógica")
    c.setFillColor(colors.black)
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, alto - 110, "[⚙️ Lógica Integrada de la App]")
    c.setFont("Courier-Bold", 11)
    c.setFillColor(colors.HexColor("#2c3e50"))
    c.drawString(50, alto - 135, "def calcular_rendimiento(libras_recibidas, libras_filete):")
    c.drawString(50, alto - 150, "    if libras_recibidas == 0: return 0.0")
    c.drawString(50, alto - 165, "    return round((libras_filete / libras_recibidas) * 100, 2)")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, alto - 205, "[📦 Características de Arquitectura Actuales]")
    c.setFont("Helvetica", 12)
    c.drawString(50, alto - 230, "✔ Módulo de Recepción (FT-HACCP-005): Auto-relleno inteligente a 15 filas fijas.")
    c.drawString(50, alto - 245, "✔ Módulo de Trazabilidad (FT-PROD-03): Auto-relleno inteligente a 17 filas fijas.")
    c.drawString(50, alto - 260, "✔ Seguridad de Planta (Login): Sistema por roles para personal autorizado.")
    c.drawString(50, alto - 275, "✔ Persistencia Cloud: Conexión transparente y automática a Google Sheets.")

    # Simulación de recuadro de interfaz
    c.setDash(4, 2)
    c.rect(450, alto - 320, 280, 210, fill=0, stroke=1)
    c.setFont("Helvetica", 11)
    c.drawString(465, alto - 210, "[ Simulación Interfaz de Usuario UI ]")
    c.drawString(465, alto - 235, "• Menú de Navegación Lateral Activo")
    c.drawString(465, alto - 255, "• Entrada Digital de Lotes y Temperaturas")
    c.drawString(465, alto - 275, "• Botón de Vista de Impresión Oficial")
    c.setDash()
    c.showPage()

    # ==========================================
    # LÁMINA 5: PLAN DE EXPANSIÓN (HOJA DE RUTA)
    # ==========================================
    aplicar_plantilla("Plan de Expansión: Futuros Reportes y Secciones")
    c.setFillColor(colors.black)
    
    # Caja Fase 1
    c.setFillColor(colors.white)
    c.rect(40, alto - 320, 330, 210, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#124491"))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(55, alto - 140, "🔍 Nuevas Secciones de Control")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    c.drawString(55, alto - 170, "• Monitoreo Digital Integrado de PCC")
    c.drawString(55, alto - 185, "  (Puntos Críticos de Control).")
    c.drawString(55, alto - 205, "• Control automatizado de Higiene y")
    c.drawString(55, alto - 220, "  Sanitización de Planta pre-operativa.")
    c.drawString(55, alto - 240, "• Control de Despacho y Cadena de Frío.")

    # Caja Fase 2
    c.setFillColor(colors.white)
    c.rect(400, alto - 320, 340, 210, fill=1, stroke=1)
    c.setFillColor(colors.HexColor("#008080"))
    c.drawString(415, alto - 140, "📊 Reportes Avanzados Gerenciales")
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    c.drawString(415, alto - 170, "• Dashboard Gráfico Interactivo con")
    c.drawString(415, alto - 185, "  métricas semanales de rendimiento.")
    c.drawString(415, alto - 205, "• Análisis inteligente de mermas e")
    c.drawString(415, alto - 220, "  ingresos filtrado por proveedor.")
    c.drawString(415, alto - 240, "• Módulo simulador de auditorías BRCGS.")
    c.showPage()

    # ==========================================
    # LÁMINA 6: INFORME TÉCNICO-ECONÓMICO
    # ==========================================
    aplicar_plantilla("Informe Técnico-Económico e Inversión")
    c.setFillColor(colors.black)
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, alto - 110, "Estructura Técnica y Académica del Equipo:")
    c.setFont("Helvetica", 13)
    c.drawString(60, alto - 135, "• Alianza integrada por un grupo de estudiantes avanzados de Ingeniería en Software.")
    c.drawString(60, alto - 155, "• Supervisión y asesoría de Profesores de la Universidad Nacional de Ingeniería (UNI).")
    c.drawString(60, alto - 175, "• Colaborador interno de planta (Su persona) estructurando flujos en sus tiempos libres.")
    
    c.setFillColor(colors.HexColor("#124491"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, alto - 220, "Inversión Total de la Solución: $850.00 USD")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Oblique", 11)
    c.drawString(40, alto - 240, "* Monto sumamente bajo y accesible para la industria al dividirse de forma directa entre un equipo de 6 personas.")
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, alto - 285, "Términos Comerciales y Plazos:")
    c.setFont("Helvetica", 13)
    c.drawString(60, alto - 310, "• Plazo de entrega cerrado (Despliegue y pruebas): 2 meses y medio (10 semanas).")
    c.drawString(60, alto - 330, "• Plan de financiamiento: 45% de anticipo al inicio ($382.50) / 55% contra entrega final ($467.50).")
    
    c.showPage()
    c.save()
    print("¡Éxito! Tu PDF real ha sido generado.")

if __name__ == "__main__":
    crear_presentacion_llamativa()
    