# -*- coding: utf-8 -*-
"""Interfaz gráfica para ingreso de datos de Aethalómetro con validación mejorada,
manejo de errores y mejor experiencia de usuario.

Updates:
 -OCT25: Se unifican campos para evitar columnas innecesarias en Excel. Modularizo codigo y bloques de UI. FQ
 -SEP25: Se quitan variables globales innecesarias. En su lugar, se usa un diccionario. Se mejora la validacion de entradas. FQ
 -AGO25: Mejoras en interfaz grafica. Agrego ttk. FQ
 -ENE25: Modifico ruta para dejarla fija p/ nuevo criterio. GM

@author: fquarin
"""
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from tkinter import font
import os
import openpyxl
from datetime import datetime

################################################################
#INGRESAR DIRECCION Y NOMBRE DE LA PLANILLA A CREAR/MODIFICAR
#filepath = "____________________________________________________"
filepath = "C://Aethalometer/AE33/Datos/Crudos/2026/MBI_AE33_log_2026.xlsx"
#Estructura de carga de datos fijas, solo hay que cambiarle el año

#############################################
##############  FUNCIONES   ################# 
#############################################

# Para que Status solo admita numeros
def validate_numeric_input(input):
    return input.isnumeric()

# Para admitir números con parte decimal (punto o coma) y vacío
def validate_decimal_input(input_value):
    if input_value == "":
        return True
    allowed_chars = set("0123456789.,")
    if not set(input_value).issubset(allowed_chars):
        return False
    if input_value.count('.') + input_value.count(',') > 1:
        return False
    return True

#Deshabilitar widgets
def disable_widgets():
####Si Valve Status "0 (cero)" esta checkeado --> Disable dropdown de valve status
    if cerocheck_var.get() == 1:
        dropdown.config(state='disabled')
    else:
        dropdown.config(state='normal')  
####Si 5lpm esta checkeado --> Disable flujo blankbox
    if flowcheck_var.get() == 1:
        flow_entry.config(state='disabled')
    else:
        flow_entry.config(state='normal')
              
#  Deshabilito opcion1 Y opcion2 si condicion cambia
def toggle_buttons(condicion, opcion1, opcion2):
    if condicion.get():
        opcion1.config(state=tk.DISABLED)
        opcion2.config(state=tk.DISABLED)
    else:
        opcion1.config(state=tk.NORMAL)
        opcion2.config(state=tk.NORMAL)
        
def destroy_all_windows():
    for widget in root.winfo_children():
        widget.destroy()
    root.destroy()

def copy_to_clipboard(text):
    try:
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
    except Exception:
        pass

# Mostrar pista según selección en Valve Status
    sel = cero_options_var.get()

#############################################
############# GUARDADO DE DATOS #############
#############################################

def guardar_datos():
    global observaciones
    
    # Determinar valor de flujo: 5 si está marcado 5lpm, sino el valor del entry
    flujo_value = 5 if flowcheck_var.get() else flow_entry.get()
    
    # Combinar Valve Status en un solo campo
    if cerocheck_var.get():
        valve_status = "00000 : Medición"
    else:
        valve_status = cero_options_var.get()
    
    form_data = {
        "Hora": datetime.today().strftime('%Y-%m-%d %H:%M'), #A
        "Operador": operador_entry.get(), #B
        "Status": status_entry.get(), #C
        "Valve_Status": valve_status, # D (columna única combinada)
        #"Valve_Status_Cero": cerocheck_var.get(), #D
        #"Valve_Status_options": cero_options_var.get(), #E
        "Apariencia_filtro": apariencia_options_var.get(), #F
        "Flujo": flujo_value, #G - Columna unificada
        "Cinta_reemplazada": reemplazocinta_var.get(), #H
        "Checkbox_gral": general_checkbox_var.get(), #I
        "FTP_check": ftp_check_var.get(), #J
        "Verif_Flujo_No_Necesario": verifflujononece_checkbox_var.get(), #K
        "Verif_Flujo_Aceptable": verifflujoacept_checkbox_var.get(), #L
        "Prueba_Fugas_en_entrada": radioValue_veriffugas_var.get(), #M
        "Limpieza_Optica": limpiezaoptica_checkbox_var.get(), #N
        "Prueba_fugas(sist.interno)": radioValue_pruebafugas.get(), #O
        "Prueba_estabilidad": radioValue_Estabilidad.get(), #P
        "Prueba_Aire_Limpio": radioValue_Airelimpio.get(), #Q
        "Observaciones": observaciones #R
    }
        
    if not form_data["Operador"]:
        messagebox.showwarning("Advertencia", "El campo Operador es obligatorio.")
        return

    try:
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.append(list(form_data.keys()))
            workbook.save(filepath)
        
        workbook = openpyxl.load_workbook(filepath)
        sheet = workbook.active
        sheet.append(list(form_data.values()))
        workbook.save(filepath)
        open_guardado_window()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

#############################################
############## VENTANAS EXTRA ###############
#############################################

######### VENTANA: OBSERVACIONES ############
def open_observ_window():
    global observ_window, observ_entry
    observ_window = tk.Toplevel(root)
    observ_window.title("Observaciones")
    observ_window.configure(bg="#e7f2f9")
    center_window(observ_window, 550, 520)

    # Marco contenedor con estilos de la sección Save
    wrapper = ttk.Frame(observ_window, style='Save.TLabelframe', padding=14)
    wrapper.grid(row=0, column=0, sticky='nsew')
    observ_window.columnconfigure(0, weight=1)
    observ_window.rowconfigure(0, weight=1)

    title = ttk.Label(wrapper, text="Recuerde registrar cualquier situación que pueda afectar las mediciones \n y que no hayan sido contempladas en la interfaz\n que suceda en este momento o que haya notado en la última semana: \n" "•Otro tipo mantenimiento en el instrumento o la estación\n•Cortes de energía\n•Condiciones meteorológicas inusuales\n•Presencia de humo o cenizas\n•Problemas de flujo\n•Ruidos extraños del instrumento\n•Cambios de filtro o trampas de agua.\n•Si no hay nada relevante, escribir ‘sin novedades’", style='Save.TLabel')
    title.grid(row=0, column=0, sticky='w')

    # Text no tiene variante ttk: ajusto colores para integrarlo visualmente
    observ_entry = tk.Text(wrapper, width=60, height=10, font=("Calibri", 12),
                           bg='#e7f2f9', fg='#005ca6', relief='solid', bd=1)
    observ_entry.grid(row=1, column=0, sticky='nsew', pady=(8, 12))
    wrapper.columnconfigure(0, weight=1)
    wrapper.rowconfigure(1, weight=1)

    buttons = ttk.Frame(wrapper, style='Save.TLabelframe')
    buttons.grid(row=2, column=0, sticky='ew')
    buttons.columnconfigure(0, weight=1)
    buttons.columnconfigure(1, weight=1)

    observ_button1 = ttk.Button(buttons, text="Guardar y salir", command=save_observ, style='Save.TButton')
    observ_button1.grid(row=0, column=0, sticky='ew', padx=(0, 6))
    observ_button2 = ttk.Button(buttons, text="Cerrar", command=observ_window.destroy, style='Save.TButton')
    observ_button2.grid(row=0, column=1, sticky='ew', padx=(6, 0))

    observ_window.grab_set()  # Hace modal la ventana

#Para centrar cualquier ventana
def center_window(window, width, height):
    window.update_idletasks()  # Asegura que los cálculos de tamaño sean precisos
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

#Para guardar Observaciones
def save_observ():
    global observaciones
    observaciones = observ_entry.get("1.0", "end-1c") 
    observ_window.destroy()
    
#Cerrar ventana: Observaciones
def close_observ_window(observ_window):
    observ_window.destroy()

#############################################
##### VENTANA: CONTROL BIMESTRAL. FLUJO   #####
def open_window_bimestral_verificarflujo():
    new_window = tk.Toplevel(root)
    new_window.title("Control Bimestral")
    new_window.configure(bg='#e7f9f2')
    center_window(new_window, 440, 150)
    new_window.resizable(True, True)
    new_window.minsize(380, 180)
    new_window.grab_set()

    wrapper = ttk.Frame(new_window, style='controlBimestral.TFrame', padding=12)
    wrapper.grid(row=0, column=0, sticky='nsew', padx=6, pady=6)
    new_window.columnconfigure(0, weight=1)
    new_window.rowconfigure(0, weight=1)

    # Título sin recuadro visible
    calib_title = ttk.Label(wrapper, text="Calibración de Flujo", style='controlBimestral.Title.TLabel')
    calib_title.grid(row=0, column=0, sticky='w', padx=8, pady=(6, 2))

    # Contenedor plano (sin bordes) en lugar de LabelFrame
    calibracionflujo_frame = ttk.Frame(wrapper, style='controlBimestral.TFrame')
    calibracionflujo_frame.grid(row=1, column=0, sticky='nsew', padx=8, pady=4)
    wrapper.columnconfigure(0, weight=1)
    wrapper.rowconfigure(1, weight=1)
    calibracionflujo_frame.columnconfigure(0, weight=1)
    calibracionflujo_frame.columnconfigure(1, weight=1)
    calibracionflujo_frame.rowconfigure(0, weight=1)

    calibflujobimestral_var = tk.IntVar()
    options_row = ttk.Frame(calibracionflujo_frame, style='controlBimestral.TFrame')
    options_row.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=(6, 6))
    calibracionflujo_frame.rowconfigure(0, weight=1)
    options_row.columnconfigure(0, weight=1)
    options_row.columnconfigure(1, weight=1)

    R1_calibflujobimestral = ttk.Radiobutton(options_row, text="Aceptable", variable=calibflujobimestral_var, value=1, style='controlBimestral.TRadiobutton')
    R1_calibflujobimestral.grid(row=0, column=0, padx=12, pady=4, sticky='e')

    R2_calibflujobimestral = ttk.Radiobutton(options_row, text="No aceptable", variable=calibflujobimestral_var, value=2, command=lambda: [close_new_window(new_window), open_contacto_window()], style='controlBimestral.TRadiobutton')
    R2_calibflujobimestral.grid(row=0, column=1, padx=12, pady=4, sticky='w')

    quit_button = ttk.Button(calibracionflujo_frame, text="Cerrar", command=lambda: close_new_window(new_window), style='controlBimestral.TButton')
    quit_button.grid(row=1, column=0, columnspan=2, pady=(4, 2), padx=8, sticky='ew')

#Cerrar ventana: Control bimestral, flujo
def close_new_window(new_window):
    new_window.destroy()
    
#############################################
############ VENTANA CONTACTO ###############
def open_contacto_window():  
    contacto = tk.Toplevel(root)
    contacto.title('Contacto')
    contacto.configure(bg='#e7f2f9')
    center_window(contacto, 280, 260)
    contacto.minsize(280, 220)
    contacto.grab_set()

    wrapper = ttk.Frame(contacto, style='Save.TFrame', padding=16)
    wrapper.grid(row=0, column=0, sticky='nsew')
    contacto.columnconfigure(0, weight=1)
    contacto.rowconfigure(0, weight=1)
    # Hacer que todas las filas internas puedan expandir
    for i in range(0, 5):
        wrapper.rowconfigure(i, weight=1)
    wrapper.columnconfigure(0, weight=1)

    title = ttk.Label(wrapper, text='Contacto', style='Save.Title.TLabel')
    title.grid(row=0, column=0, sticky='ew', pady=(0,8))

    lbl = ttk.Label(wrapper, text='Por favor, contactarse con:', style='Save.TLabel')
    lbl.grid(row=1, column=0, sticky='ew')

    mail_row_1 = ttk.Frame(wrapper, style='Save.TFrame')
    mail_row_1.grid(row=2, column=0, sticky='nsew', pady=(6,2))
    mail_row_1.columnconfigure(0, weight=1)
    mail_label_1 = ttk.Label(mail_row_1, text='Giselle Marincovich:', style='Save.TLabel')
    mail_label_1.grid(row=0, column=0, sticky='ew')
    mail_value_1 = ttk.Label(mail_row_1, text='gmarincovich@smn.gob.ar', style='Save.Email.TLabel')
    mail_value_1.grid(row=1, column=0, sticky='ew')

    mail_row_2 = ttk.Frame(wrapper, style='Save.TFrame')
    mail_row_2.grid(row=3, column=0, sticky='nsew', pady=(2,6))
    mail_row_2.columnconfigure(0, weight=1)
    mail_label_2 = ttk.Label(mail_row_2, text='Francisco Quarin:', style='Save.TLabel')
    mail_label_2.grid(row=0, column=0, sticky='ew')
    mail_value_2 = ttk.Label(mail_row_2, text='fquarin@smn.gob.ar', style='Save.Email.TLabel')
    mail_value_2.grid(row=1, column=0, sticky='ew')

    btns = ttk.Frame(wrapper, style='Save.TFrame')
    btns.grid(row=4, column=0, sticky='nsew', pady=(12, 0))
    btns.columnconfigure(0, weight=1)
    btns.rowconfigure(0, weight=1)

    cerrar_btn = ttk.Button(btns, text='Cerrar', command=contacto.destroy, style='Save.TButton')
    cerrar_btn.grid(row=0, column=0, sticky='nsew')
    return contacto

#############################################
############ VENTANA GUARDADO EXITOSO ###############
def open_guardado_window():  
    return messagebox.showinfo("Guardado exitoso", "Datos guardados, con fecha:\n       " + datetime.today().strftime("%Y-%m-%d %H:%M"))
    
#############################################
############ VENTANA PRINCIPAL ##############

###### Ventana Principal (root) ######
root = tk.Tk()
root.title("Aethalometro") 
root.geometry("")
# Cambia el icono de la ventana
root.iconbitmap(r"C:\Aethalometer/AE33/Scripts/icono.ico")
################################################################

# Estilos
style = ttk.Style()
style.theme_use('clam')

# Colores y estilos por sección
style.configure('Info.TLabelframe', background='#e6f2ff', foreground='#003366', font=('Calibri', 14, 'bold'))
style.configure('Info.TLabelframe.Label', background='#e6f2ff', foreground='#003366', font=('Calibri', 14, 'bold'))
style.configure('Info.TLabel', background='#e6f2ff', foreground='#003366', font=('Calibri', 12))

style.configure('Checklist.TLabelframe', background='#f9f2e7', foreground='#a65c00', font=('Calibri', 14, 'bold'))
style.configure('Checklist.TLabelframe.Label', background='#f9f2e7', foreground='#a65c00', font=('Calibri', 14, 'bold'))
style.configure('Checklist.TLabel', background='#f9f2e7', foreground='#a65c00', font=('Calibri', 12))

style.configure('controlBimestral.TLabelframe', background='#e7f9f2', foreground='#008066', font=('Calibri', 14, 'bold'))
style.configure('controlBimestral.TLabelframe.Label', background='#e7f9f2', foreground='#008066', font=('Calibri', 14, 'bold'))
style.configure('controlBimestral.TLabel', background='#e7f9f2', foreground='#008066', font=('Calibri', 12))

style.configure('controlSemestral.TLabelframe', background='#f2e7f9', foreground='#660080', font=('Calibri', 14, 'bold'))
style.configure('controlSemestral.TLabelframe.Label', background='#f2e7f9', foreground='#660080', font=('Calibri', 14, 'bold'))
style.configure('controlSemestral.TLabel', background='#f2e7f9', foreground='#660080', font=('Calibri', 12))

style.configure('Save.TLabelframe', background='#e7f2f9', foreground='#005ca6', font=('Calibri', 14, 'bold'))
style.configure('Save.TLabelframe.Label', background='#e7f2f9', foreground='#005ca6', font=('Calibri', 14, 'bold'))
style.configure('Save.TLabel', background='#e7f2f9', foreground='#005ca6', font=('Calibri', 12))

style.configure('Save.TButton', font=('Calibri', 13, 'bold'), background='#e7f2f9', foreground='#005ca6', borderwidth=2, focusthickness=3, focuscolor='#005ca6')
style.map('Save.TButton', background=[('active', '#cce6ff')], foreground=[('active', '#003366')])

style.configure('Checklist.TCheckbutton', background='#f9f2e7', foreground='#a65c00', font=('Calibri', 12))
style.configure('controlBimestral.TCheckbutton', background='#e7f9f2', foreground='#008066', font=('Calibri', 12))
style.configure('Info.TCheckbutton', background='#e6f2ff', foreground='#003366', font=('Calibri', 12))
style.configure('controlSemestral.TCheckbutton', background='#f2e7f9', foreground='#660080', font=('Calibri', 12))
style.configure('controlSemestral.TRadiobutton', background='#f2e7f9', foreground='#660080', font=('Calibri', 12))
style.configure('controlBimestral.TRadiobutton', background='#e7f9f2', foreground='#008066', font=('Calibri', 12))
style.configure('controlBimestral.TFrame', background='#e7f9f2')
style.configure('controlBimestral.Title.TLabel', background='#e7f9f2', foreground='#008066', font=('Calibri', 16, 'bold'))
style.configure('Save.Title.TLabel', background='#e7f2f9', foreground='#005ca6', font=('Calibri', 16, 'bold'))
style.configure('Save.Email.TLabel', background='#e7f2f9', foreground='#005ca6', font=('Consolas', 12))
style.configure('Save.TFrame', background='#e7f2f9')

# Combobox estilo para Info
style.configure('Info.TCombobox', fieldbackground='#e6f2ff', background='#e6f2ff')
style.map('Info.TCombobox', fieldbackground=[('readonly', '#e6f2ff')], background=[('readonly', '#e6f2ff')])

# Separadores
style.configure('Checklist.TSeparator', background='#a65c00')
style.configure('controlSemestral.TSeparator', background='#660080')
style.configure('Info.TSeparator', background='#003366')
style.configure('controlBimestral.TSeparator', background='#008066')
style.configure('Save.TSeparator', background='#005ca6')

root.configure(bg='#e6f2ff')

frame = ttk.Frame(root)
frame.pack(fill="both", expand=True)
frame.columnconfigure(0, weight=1)

##### INFO FRAME -1- #####

sep_info = ttk.Separator(frame, orient='horizontal', style='Info.TSeparator')
sep_info.grid(row=0, column=0, sticky='EW')

info_frame_1 = ttk.LabelFrame(frame, text="Información ➀", labelanchor='n', style='Info.TLabelframe')
info_frame_1.grid(row=1, column=0, sticky="we")

# Configura el peso de las columnas para centrar el contenido
info_frame_1.grid_columnconfigure(0, weight=1)
info_frame_1.grid_columnconfigure(1, weight=30)
info_frame_1.grid_columnconfigure(2, weight=30)
info_frame_1.grid_columnconfigure(3, weight=30)

#Operador
operador_label = ttk.Label(info_frame_1, text="Operador", style='Info.TLabel')
operador_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

operador_entry = ttk.Entry(info_frame_1)
operador_entry.grid(row=0, column=1, padx=5, pady=5,sticky="ew")

# Status (numeric only)
status_label = ttk.Label(info_frame_1, text="Status", style='Info.TLabel')
status_label.grid(row=2, column=0,sticky="ew")

status_entry = ttk.Entry(info_frame_1, validate="key")
status_entry['validatecommand'] = (status_entry.register(validate_numeric_input), '%P')
status_entry.grid(row=2, column=1,sticky="ew")

#Valve status. Si 0 esta tildado, deshabilito desplegable 
valve_status_label = ttk.Label(info_frame_1, text="Valve Status", style='Info.TLabel')
valve_status_label.grid(row=3, column=0,sticky="ew")

cerocheck_var = tk.BooleanVar()
cero_checkbox = ttk.Checkbutton(info_frame_1, text="00000 : Medición", variable=cerocheck_var, command=disable_widgets, style='Info.TCheckbutton')
cero_checkbox.grid(row=3, column=1,sticky="ew")

# Desplegable
cero_options_var = tk.StringVar()
cero_options = ["", "01011 : Derivación", "01100 : Calentamiento/Aire limpio", "00010 : Calibración medidor de flujo"]
dropdown = ttk.Combobox(info_frame_1, textvariable=cero_options_var, values=cero_options, state="readonly", width=38, style='Info.TCombobox')
dropdown.set(cero_options[0])
dropdown.grid(row=3, column=2,sticky="ew")
#dropdown.bind('<<ComboboxSelected>>', on_valve_status_change)

# Pista bajo el combobox
valve_hint_label = ttk.Label(info_frame_1, text="", style='Info.TLabel')
valve_hint_label.grid(row=4, column=0, columnspan=4, sticky='w', padx=5, pady=(2, 8))

#Apariencia del filtro. Con desplegable
apariencia_filtro_label = ttk.Label(info_frame_1, text="Apariencia Filtro", style='Info.TLabel')
apariencia_filtro_label.grid(row=4, column=0, columnspan=1,sticky="ew")

apariencia_options_var = tk.StringVar()
apariencia_options = ["", "Normal","Con humedad","Marron"]
desplegable_apariencia = ttk.Combobox(info_frame_1, textvariable=apariencia_options_var, values=apariencia_options, state="readonly", style='Info.TCombobox')
desplegable_apariencia.set(apariencia_options[0])
desplegable_apariencia.grid(row=4, column=1,sticky="ew")

# Flujo. Si 5 lpm esta tildado deshabilito entrybox
flow_label = ttk.Label(info_frame_1, text="Flujo externo", style='Info.TLabel')
flow_label.grid(row=5, column=0,sticky="ew")

flowcheck_var = tk.BooleanVar()
flow_check = ttk.Checkbutton(info_frame_1, text="5 lpm", variable=flowcheck_var, command=disable_widgets, style='Info.TCheckbutton')
flow_check.grid(row=5, column=1,sticky="ew")

vcmd_decimal = (root.register(validate_decimal_input), '%P')
flow_entry = ttk.Entry(info_frame_1, validate='key', validatecommand=vcmd_decimal)
flow_entry.grid(row=5, column=2,sticky="ew")

lpm_text_label = ttk.Label(info_frame_1, text="lpm", style='Info.TLabel')
lpm_text_label.grid(row=5, column=3,sticky="ew")
# Reemplazo Cinta
reemplazocinta_var = tk.BooleanVar()
reemplazocinta_checkbox = ttk.Checkbutton(info_frame_1, text="Se reemplazó la cinta", variable=reemplazocinta_var, command=disable_widgets, style='Info.TCheckbutton')
reemplazocinta_checkbox.grid(row=6, column=0,sticky="w", pady=5)

##### CHECKLIST GRAL FRAME -2- #####

sep_checklist = ttk.Separator(frame, orient='horizontal', style='Checklist.TSeparator')
sep_checklist.grid(row=2, column=0, sticky='EW')

checklistgral_frame_2 = ttk.LabelFrame(frame, text = "Checklist General ➁", labelanchor='n', style='Checklist.TLabelframe')
checklistgral_frame_2.grid(row=3, column=0,sticky='WE', padx=10, pady=8)
checklistgral_frame_2.columnconfigure(0, weight=1)
checklistgral_frame_2.columnconfigure(1, weight=1)
checklistgral_frame_2.columnconfigure(2, weight=0)
checklistgral_frame_2.columnconfigure(3, weight=1)

checklistgral_frame_2.grid_columnconfigure(0, weight=1)
checklistgral_frame_2.grid_columnconfigure(1, weight=0)
checklistgral_frame_2.grid_columnconfigure(2, weight=0)
checklistgral_frame_2.grid_columnconfigure(3, weight=0)

# Hora actual + hora instrumento
hora_label = ttk.Label(checklistgral_frame_2, text="• Chequeo hora actual + instrumento", style='Checklist.TLabel')
hora_label.grid(row=0, column=0)

# Inspeccion caño y manguera
mangueras_label = ttk.Label(checklistgral_frame_2, text="• Inspección caños y mangueras", style='Checklist.TLabel')
mangueras_label.grid(row=1, column=0)

# Trampa agua interna
aguainterna_label = ttk.Label(checklistgral_frame_2, text="• Inspección trampa de agua interna  ", style='Checklist.TLabel')
aguainterna_label.grid(row=2, column=0)

# Trampa agua externa
aguaexterna_label = ttk.Label(checklistgral_frame_2, text="• Inspección trampa de agua externa ", style='Checklist.TLabel')
aguaexterna_label.grid(row=3, column=0)

#Checkbox gral
general_checkbox_var = tk.BooleanVar()
general_checkbox = ttk.Checkbutton(checklistgral_frame_2, variable=general_checkbox_var, style='Checklist.TCheckbutton')
general_checkbox.grid(row=1, column=1, rowspan=2,padx=30)

#Separador FTP
separador_ftp = ttk.Separator(checklistgral_frame_2, orient='vertical', style='Checklist.TSeparator')
separador_ftp.grid(row=0, column=2, rowspan=4, sticky='ns', padx=5)
#separador_ftp.place(relx=0.5, rely=0, relwidth=1, relheight=1)

# Frame para la sección FTP, con fondo verde claro
ftp_frame = ttk.Frame(checklistgral_frame_2, style='Checklist.TLabelframe', relief='flat')
ftp_frame.grid(row=0, column=3, rowspan=4, sticky="nsew", padx=5, pady=5)
ftp_frame.columnconfigure(0, weight=1)
ftp_frame.rowconfigure(0, weight=1)
ftp_frame.rowconfigure(1, weight=1)

#Check FTP
ftpnota_label = ttk.Label(ftp_frame, text="Datos semanales cargados al FTP?", style='Checklist.TLabel', anchor='center', justify='center')
ftpnota_label.grid(row=0, column=0, sticky='ew', pady=(0,8))

ftp_check_var = tk.BooleanVar()
ftp_check = ttk.Checkbutton(ftp_frame, variable=ftp_check_var, style='Checklist.TCheckbutton')
ftp_check.grid(row=1, column=0, sticky='n', pady=(0,10))

##### CONTROL BIMESTRAL FRAME -3- #####
# (no usar estilos antiguos con colores fijos de fondo)

sep_controlBimestral = ttk.Separator(frame, orient='horizontal', style='controlBimestral.TSeparator')
sep_controlBimestral.grid(row=4, column=0, sticky='EW')

controlBimestral_frame_3 = ttk.LabelFrame(frame, text = "Control Bimestral ➂", labelanchor='n', style='controlBimestral.TLabelframe')
controlBimestral_frame_3.grid(row=5, column=0,sticky='WE', padx=10, pady=8)
controlBimestral_frame_3.columnconfigure(0, weight=1)
controlBimestral_frame_3.columnconfigure(1, weight=1)
controlBimestral_frame_3.columnconfigure(2, weight=1)
controlBimestral_frame_3.columnconfigure(3, weight=1)

#Control Bimestral. Verificacion de flujo. 
                    #if Nonecesario esta tildado, entro a toggle_buttons para deshabilitar botones.
verifflujo_label = ttk.Label(controlBimestral_frame_3, text="Verificación de flujo", style='controlBimestral.TLabel')
verifflujo_label.grid(row=0, column=0, pady=(4, 4))

verifflujononece_checkbox_var = tk.BooleanVar()
verifflujononece_checkbox = ttk.Checkbutton(controlBimestral_frame_3, text="No necesario", variable=verifflujononece_checkbox_var, command=lambda: toggle_buttons(verifflujononece_checkbox_var, verifflujoacept_checkbox, verifflujonoacept_button), style='controlBimestral.TCheckbutton')
verifflujononece_checkbox.grid(row=0, column=1, padx=20, pady=4)

verifflujoacept_checkbox_var = tk.BooleanVar()
verifflujoacept_checkbox = ttk.Checkbutton(controlBimestral_frame_3, variable=verifflujoacept_checkbox_var, text="Aceptable", style='controlBimestral.TCheckbutton')
verifflujoacept_checkbox.grid(row=0, column=2, padx=10, pady=4)

verifflujonoacept_button_var = tk.BooleanVar()
style.configure('controlBimestral.TButton', font=('Calibri', 12, 'bold'), background='#e7f9f2', foreground='#008066')
style.map('controlBimestral.TButton', background=[('active', '#c9efe3')], foreground=[('active', '#005945')])

verifflujonoacept_button = ttk.Button(controlBimestral_frame_3, text="No aceptable ⚠️", command=open_window_bimestral_verificarflujo, style='controlBimestral.TButton')
verifflujonoacept_button.grid(row=0, column=3, padx=10, pady=4, sticky='EW')

#Control Bimestral. Prueba de fugas en la entrada

veriffugas_label = ttk.Label(controlBimestral_frame_3, text="Prueba de fugas en la entrada", style='controlBimestral.TLabel')
veriffugas_label.grid(row=1, column=0, pady=(8, 4))

radioValue_veriffugas_var = tk.IntVar()
radioOne_veriffugas = ttk.Radiobutton(controlBimestral_frame_3, text='No necesario', variable=radioValue_veriffugas_var, value=1, style='controlBimestral.TRadiobutton') 
radioTwo_veriffugas = ttk.Radiobutton(controlBimestral_frame_3, text='Aceptable', variable=radioValue_veriffugas_var, value=2, style='controlBimestral.TRadiobutton') 
radioThree_veriffugas = ttk.Radiobutton(controlBimestral_frame_3, text='No aceptable', variable=radioValue_veriffugas_var, value=3, command=open_contacto_window, style='controlBimestral.TRadiobutton')

radioOne_veriffugas.grid(row=1, column=1, padx=10, pady=2)
radioTwo_veriffugas.grid(row=1, column=2, padx=10, pady=2)
radioThree_veriffugas.grid(row=1, column=3, padx=10, pady=2)

##### CONTROL SEMESTRAL FRAME -4- #####

sep_controlSemestral = ttk.Separator(frame, orient='horizontal', style='controlSemestral.TSeparator')
sep_controlSemestral.grid(row=6, column=0, sticky='EW')

controlsemestral_frame_4 = ttk.LabelFrame(frame, text = "Control Semestral ➃", labelanchor='n', style='controlSemestral.TLabelframe')
controlsemestral_frame_4.grid(row=7, column=0,sticky='WE', padx=10, pady=8)
controlsemestral_frame_4.columnconfigure(0, weight=1)
controlsemestral_frame_4.columnconfigure(1, weight=1)
controlsemestral_frame_4.columnconfigure(2, weight=1)
controlsemestral_frame_4.columnconfigure(3, weight=1)

#Control Semestral: Limpieza optica
limpiezaoptica_label = ttk.Label(controlsemestral_frame_4, text="Limpieza Óptica", style='controlSemestral.TLabel')
limpiezaoptica_label.grid(row=0, column=0, pady=(4, 4)) 

limpiezaoptica_checkbox_var = tk.BooleanVar()
limpiezaoptica_checkbox = ttk.Checkbutton(controlsemestral_frame_4, variable=limpiezaoptica_checkbox_var,width=0.1, style='controlSemestral.TCheckbutton')
limpiezaoptica_checkbox.grid(row=0, column=1, padx=10, pady=4)

#Control Semestral: Prueba de fugas
                    #Radiobutton
pruebafugas_label = ttk.Label(controlsemestral_frame_4, text="Prueba de fugas (sistema interno)", style='controlSemestral.TLabel')
pruebafugas_label.grid(row=1, column=0, pady=(8, 4))

radioValue_pruebafugas = tk.IntVar()

radioOne_pruebafugas = ttk.Radiobutton(controlsemestral_frame_4, text='No necesario', variable=radioValue_pruebafugas, value=1, style='controlSemestral.TRadiobutton') 
radioOne_pruebafugas.grid(row=1, column=1, padx=10, pady=2)

radioTwo_pruebafugas = ttk.Radiobutton(controlsemestral_frame_4, text='Aceptable', variable=radioValue_pruebafugas, value=2, style='controlSemestral.TRadiobutton') 
radioTwo_pruebafugas.grid(row=1, column=2, padx=10, pady=2)

radioThree_pruebafugas = ttk.Radiobutton(controlsemestral_frame_4, text='No aceptable', variable=radioValue_pruebafugas, value=3, command=open_contacto_window, style='controlSemestral.TRadiobutton')
radioThree_pruebafugas.grid(row=1, column=3, padx=10, pady=2)

#Control Semestral: Prueba estabilidad
                    #Radiobutton
pruebaestabilidad_label = ttk.Label(controlsemestral_frame_4, text="Prueba Estabilidad", style='controlSemestral.TLabel')
pruebaestabilidad_label.grid(row=2, column=0, pady=(8, 4))

radioValue_Estabilidad = tk.IntVar()

radioOne_Estabilidad = ttk.Radiobutton(controlsemestral_frame_4, text='No necesario', variable=radioValue_Estabilidad, value=1, style='controlSemestral.TRadiobutton') 
radioOne_Estabilidad.grid(row=2, column=1, padx=10, pady=2)

radioTwo_Estabilidad = ttk.Radiobutton(controlsemestral_frame_4, text='Aceptable', variable=radioValue_Estabilidad, value=2, style='controlSemestral.TRadiobutton') 
radioTwo_Estabilidad.grid(row=2, column=2, padx=10, pady=2)

radioThree_Estabilidad = ttk.Radiobutton(controlsemestral_frame_4, text='No aceptable', variable=radioValue_Estabilidad, value=3, command=open_contacto_window, style='controlSemestral.TRadiobutton')
radioThree_Estabilidad.grid(row=2, column=3, padx=10, pady=2)

#Control Semestral: Prueba aire limpio
                    #Radiobutton
pruebaairelimpio_label = ttk.Label(controlsemestral_frame_4, text="Prueba Aire limpio", style='controlSemestral.TLabel')
pruebaairelimpio_label.grid(row=3, column=0, pady=(8, 4))

radioValue_Airelimpio = tk.IntVar()

radioOne_Airelimpio = ttk.Radiobutton(controlsemestral_frame_4, text='No necesario', variable=radioValue_Airelimpio, value=1, style='controlSemestral.TRadiobutton') 
radioOne_Airelimpio.grid(row=3, column=1, padx=10, pady=2)

radioTwo_Airelimpio = ttk.Radiobutton(controlsemestral_frame_4, text='Aceptable', variable=radioValue_Airelimpio, value=2, style='controlSemestral.TRadiobutton') 
radioTwo_Airelimpio.grid(row=3, column=2, padx=10, pady=2)

radioThree_Airelimpio = ttk.Radiobutton(controlsemestral_frame_4, text='No aceptable', variable=radioValue_Airelimpio, value=3, command=open_contacto_window, style='controlSemestral.TRadiobutton')
radioThree_Airelimpio.grid(row=3, column=3, padx=10, pady=2)

##### OBSERV Y GUARDADO FRAME -5- #####

sep_save = ttk.Separator(frame, orient='horizontal', style='Save.TSeparator')
sep_save.grid(row=8, column=0, sticky='EW')

observ_guardar_frame_5 = ttk.LabelFrame(frame, text = "Salvar datos ➄", labelanchor='n', style='Save.TLabelframe')
observ_guardar_frame_5.grid(row=9, column=0,sticky='WE', padx=10, pady=8)
observ_guardar_frame_5.columnconfigure(0, weight=1)
observ_guardar_frame_5.columnconfigure(1, weight=1)
observ_guardar_frame_5.columnconfigure(2, weight=1)

#Observaciones
observaciones = ""
observ_button = ttk.Button(observ_guardar_frame_5, text="Agregar observaciones 📝", command=open_observ_window, style='Save.TButton')
observ_button.grid(row=0, column=0, padx=10, pady=10,ipadx=20, sticky='EW')

#GUARDAR
guardar_button = ttk.Button(observ_guardar_frame_5, text="Guardar datos ✅", command=guardar_datos, style='Save.TButton')
guardar_button.grid(row=0, column=1, padx=20, pady=10, ipadx=20, sticky='EW')

#SALIR
salir_button = ttk.Button(observ_guardar_frame_5, text="Salir 🚪", command=destroy_all_windows, style='Save.TButton')
salir_button.grid(row=0, column=2, padx=10, pady=10, ipadx=20, sticky='EW')

root.mainloop()