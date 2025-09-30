# -*- coding: utf-8 -*-
"""Interfaz gráfica para ingreso de datos de Nefelómetro con validación mejorada,
manejo de errores y mejor experiencia de usuario.
Updates: 

- Enero 2025: GM actualizó criterios con ruta fija para guardar planilla.
- Junio 2024: FQ - Mejoras en UI, validaciones y manejo de errores.
@author: fquarin
"""

import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
import os
import openpyxl
from datetime import datetime


# Ruta fija para el archivo Excel
filepath = "C://Nephelometer/Nephelometer_integrating_AURORA3000/Datos/Crudos/2025/MBI_NEPHBS_log_2025.xlsx"
#Estructura de carga de datos fijas, solo hay que cambiarle el año

#############################################
##############  FUNCIONES   #################
#############################################

# Para que campos numéricos solo admitan números (permitir vacío)
def validate_numeric_input(input_value):
    return input_value.isnumeric() or input_value == ""

# Para admitir números con parte decimal (punto o coma) y vacío
def validate_decimal_input(input_value):
    if input_value == "":
        return True
    # Permite: "123", "123.", "123.45", ",45", "0,45", etc.
    allowed_chars = set("0123456789.,")
    if not set(input_value).issubset(allowed_chars):
        return False
    # Solo un separador decimal como máximo
    if input_value.count('.') + input_value.count(',') > 1:
        return False
    # No más de un separador seguido de nada o dígitos
    return True

#Deshabilitar widgets
def disable_widgets():
    if srcsetpt_cero_var.get() == 1:
        srcsetpt_entry.config(state='disabled')
    else:
        srcsetpt_entry.config(state='normal')

######### VENTANA: OBSERVACIONES ############
def open_observ_window():
    global observ_window
    global observ_entry
    observ_window = tk.Toplevel(root)
    observ_window.title("Observaciones")
    observ_window.configure(bg="#e7f2f9")
    observ_window.geometry("560x320")
    observ_window.resizable(False, False)

    # Contenedor con estilos de la sección Save
    wrapper = ttk.Frame(observ_window, style='Save.TLabelframe', padding=14)
    wrapper.grid(row=0, column=0, sticky='nsew')
    observ_window.columnconfigure(0, weight=1)
    observ_window.rowconfigure(0, weight=1)

    title = ttk.Label(wrapper, text="Ingrese cualquier tipo de información relevante:", style='Save.TLabel')
    title.grid(row=0, column=0, sticky='w')

    # Área de texto (tk) integrada visualmente con la paleta Save
    observ_entry = tk.Text(wrapper, width=60, height=10, font=("Calibri", 12), bg='#e7f2f9', fg='#005ca6', relief='solid', bd=1)
    observ_entry.grid(row=1, column=0, sticky='nsew', pady=(8, 12))
    wrapper.columnconfigure(0, weight=1)
    wrapper.rowconfigure(1, weight=1)

    btns = ttk.Frame(wrapper, style='Save.TLabelframe')
    btns.grid(row=2, column=0, sticky='ew')
    btns.columnconfigure(0, weight=1)
    btns.columnconfigure(1, weight=1)

    btn_save = ttk.Button(btns, text="Guardar y salir", command=save_observ, style='Save.TButton')
    btn_save.grid(row=0, column=0, sticky='ew', padx=(0, 6))
    btn_close = ttk.Button(btns, text="Cerrar", command=observ_window.destroy, style='Save.TButton')
    btn_close.grid(row=0, column=1, sticky='ew', padx=(6, 0))

    observ_window.grab_set()
    
#Para guardar Observaciones
def save_observ(): 
    observacion = observ_entry.get("1.0", "end-1c")
    root.observaciones = observacion 
    observ_window.destroy()
    
#Cerrar ventana: Observaciones
def close_observ_window(observ_window):
    observ_window.destroy()

#####################################################
############ VENTANA GUARDADO EXITOSO ###############
def open_guardado_window():  
    return messagebox.showinfo("Guardado exitoso", "Datos guardados, con fecha:\n       " + datetime.today().strftime("%Y-%m-%d %H:%M"))

#############################################
############# GUARDADO DE DATOS #############
#############################################

def guardar_datos():
    # Normalizar y validar flujo (decimales con punto o coma)
    flujo_raw = flujo_entry.get().strip()
    flujo_value = None
    if flujo_raw != "":
        try:
            flujo_norm = flujo_raw.replace(',', '.')
            flujo_value = float(flujo_norm)
        except Exception:
            messagebox.showerror("Dato inválido", "El campo 'Flujo' debe ser un número válido (use punto o coma decimal).")
            return False

    datos = {
        "Hora": datetime.today().strftime('%Y-%m-%d %H:%M'),
        "OPERADOR": operador_entry.get(),
        # Escribimos None si vacío (celda en blanco) o el float si válido
        "Flujo": flujo_value if flujo_raw != "" else None,
        "Status Led1": statusLED1_entry.get(),
        "Status Led2": statusLED2_entry.get(),
        "Apariencia Filtro": apariencia_options_var.get(),
        "Checkbox Gral": general_checkbox_var.get(),
        "FTP_check": ftp_check_var.get(),
        "Source Set Point Zero?": srcsetpt_cero_var.get(),
        "Source Set Point": srcsetpt_entry.get(),
        "Dark Count": darkcount_entry.get(),
        "Shutter Count SC1": shtr_count_sc1_entry.get(),
        "Shutter Count SC2": shtr_count_sc2_entry.get(),
        "Shutter Count SC3": shtr_count_sc3_entry.get(),
        "Meas SC1": meas_sc1_entry.get(),
        "Meas SC2": meas_sc2_entry.get(),
        "Meas SC3": meas_sc3_entry.get(),
        "BS Meas BSC1": bs_meas_bsc1_entry.get(),
        "BS Meas BSC2": bs_meas_bsc2_entry.get(),
        "BS Meas BSC3": bs_meas_bsc3_entry.get(),
        "Meas Ratio SC1": meas_ratio_sc1_entry.get(),
        "Meas Ratio SC2": meas_ratio_sc2_entry.get(),
        "Meas Ratio SC3": meas_ratio_sc3_entry.get(),
        "BS Meas Ratio BSC1": bs_meas_ratio_bsc1_entry.get(),
        "BS Meas Ratio BSC2": bs_meas_ratio_bsc2_entry.get(),
        "BS Meas Ratio BSC3": bs_meas_ratio_bsc3_entry.get(),
        "Major State Options": major_state_options_var.get(),
        "Minor State Options": minor_state_options_var.get(),
        "LightSource": radioValue_lightsource.get(),
        "Environment Status": radioValue_envirostatus.get(),
        "Shutter": radioValue_shutter.get(),
        "PMT": radioValue_pmt.get(),
        "RH": radioValue_rh.get(),
        "ST Sensor": radioValue_st_sensor.get(),
        "Et Sensor": radioValue_et_sensor.get(),
        "BP Sensor": radioValue_bp_sensor.get(),
        "Observaciones": getattr(root, "observaciones", "")
    }

    print(datos)

    try:
        # Asegurar directorio destino
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        # Crear el archivo si no existe y agregar encabezados
        if not os.path.exists(filepath):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            heading = list(datos.keys())
            sheet.append(heading)
            workbook.save(filepath)

        # Abrir, agregar fila y guardar
        workbook = openpyxl.load_workbook(filepath)
        sheet = workbook.active
        sheet.append(list(datos.values()))
        workbook.save(filepath)
        return True
    except Exception as e:
        messagebox.showerror("Error al guardar", f"No se pudieron guardar los datos. Detalle: {e}")
        return False

def handle_guardar_click():
    exito = guardar_datos()
    if exito:
        open_guardado_window()
    
#############################################

def destroy_all_windows():
    for widget in root.winfo_children():
        widget.destroy()
    root.destroy()

#############################################
############ VENTANA PRINCIPAL ##############

###### Ventana Principal (root) ######
root = tk.Tk()
root.title("Nephelometer") 
root.geometry("")

# Activar tema clam para mejor soporte de colores en ttk
style = ttk.Style()
style.theme_use('clam')

# Colores personalizados por sección
style.configure('Info.TLabelframe', background='#e6f2ff', foreground='#003366', font=('Calibri', 14, 'bold'))
style.configure('Info.TLabelframe.Label', background='#e6f2ff', foreground='#003366', font=('Calibri', 14, 'bold'))
style.configure('Info.TLabel', background='#e6f2ff', foreground='#003366', font=('Calibri', 12))

style.configure('Checklist.TLabelframe', background='#f9f2e7', foreground='#a65c00', font=('Calibri', 14, 'bold'))
style.configure('Checklist.TLabelframe.Label', background='#f9f2e7', foreground='#a65c00', font=('Calibri', 14, 'bold'))
style.configure('Checklist.TLabel', background='#f9f2e7', foreground='#a65c00', font=('Calibri', 12))

style.configure('SysCounts.TLabelframe', background='#e7f9f2', foreground='#008066', font=('Calibri', 14, 'bold'))
style.configure('SysCounts.TLabelframe.Label', background='#e7f9f2', foreground='#008066', font=('Calibri', 14, 'bold'))
style.configure('SysCounts.TLabel', background='#e7f9f2', foreground='#008066', font=('Calibri', 12))

style.configure('SysStatus.TLabelframe', background='#f2e7f9', foreground='#660080', font=('Calibri', 14, 'bold'))
style.configure('SysStatus.TLabelframe.Label', background='#f2e7f9', foreground='#660080', font=('Calibri', 14, 'bold'))
style.configure('SysStatus.TLabel', background='#f2e7f9', foreground='#660080', font=('Calibri', 12))

style.configure('Save.TLabelframe', background='#e7f2f9', foreground='#005ca6', font=('Calibri', 14, 'bold'))
style.configure('Save.TLabelframe.Label', background='#e7f2f9', foreground='#005ca6', font=('Calibri', 14, 'bold'))
style.configure('Save.TLabel', background='#e7f2f9', foreground='#005ca6', font=('Calibri', 12))

# Estilos para widgets de cada sección
style.configure('Info.TEntry', fieldbackground='#e6f2ff', background="#16375a")
style.configure('Info.TMenubutton', background='#e6f2ff')
style.configure('Checklist.TEntry', fieldbackground='#f9f2e7', background='#f9f2e7')
style.configure('Checklist.TCheckbutton', background='#f9f2e7')
style.configure('Checklist.TMenubutton', background='#f9f2e7')
style.configure('SysCounts.TEntry', fieldbackground='#e7f9f2', background='#e7f9f2')
style.configure('SysCounts.TCheckbutton', background='#e7f9f2',foreground='#008066',font=('Calibri', 12))
style.configure('SysCounts.TMenubutton', background='#e7f9f2')
style.configure('SysStatus.TEntry', fieldbackground='#f2e7f9', background='#f2e7f9')
style.configure('SysStatus.TMenubutton', background='#f2e7f9')
style.configure('Save.TEntry', fieldbackground='#e7f2f9', background='#e7f2f9')
style.configure('Save.TMenubutton', background='#e7f2f9')
style.configure('SysStatus.TRadiobutton', background='#f2e7f9')

# Configuración de separadores
style.configure('Checklist.TSeparator', background='#a65c00')      # Checklist General (marrón)
style.configure('SysStatus.TSeparator', background='#660080')      # Sys Status (violeta)
style.configure('Info.TSeparator', background='#003366')
style.configure('Checklist.TSeparator', background='#a65c00')
style.configure('SysCounts.TSeparator', background='#008066')
style.configure('SysStatus.TSeparator', background='#660080')
style.configure('Save.TSeparator', background='#005ca6')

style.configure(
    'Save.TButton',
    font=('Calibri', 13, 'bold'),
    background='#e7f2f9',
    foreground='#005ca6',
    borderwidth=2,
    focusthickness=3,
    focuscolor='#005ca6'
)

style.map('Save.TButton',
    background=[('active', '#cce6ff')],
    foreground=[('active', '#003366')]
)

root.configure(bg='#e6f2ff')

frame = ttk.Frame(root)
frame.pack(fill="both", expand=True)
frame.columnconfigure(0, weight=1)

# --- Separador antes de Información ---
sep_info = ttk.Separator(frame, orient='horizontal')
sep_info.grid(row=0, column=0, sticky='EW')

##### INFO FRAME -1- #####
info_frame_1 = ttk.LabelFrame(frame, text = "Información ➀",labelanchor="n", style='Info.TLabelframe',borderwidth=0)
info_frame_1.columnconfigure(0, weight=1)
info_frame_1.columnconfigure(1, weight=1)
info_frame_1.columnconfigure(2, weight=1)
info_frame_1.columnconfigure(3, weight=1)
info_frame_1.grid(row=1, column=0,sticky='WE')

#Operador
operador_label = ttk.Label(info_frame_1, text="Operador", style='Info.TLabel')
operador_label.grid(row=1, column=0, sticky='EW')

operador_entry = ttk.Entry(info_frame_1,style='Info.TEntry')
operador_entry.grid(row=1, column=1, sticky='EW')

    #Flujo. Solo se puede ingresar numeros
flujo_label = ttk.Label(info_frame_1, text="Flujo actual", style='Info.TLabel')
flujo_label.grid(row=2, column=0,sticky='EW')

# Validación decimal para flujo (permite punto o coma)
vcmd_decimal = (root.register(validate_decimal_input), '%P')
flujo_entry = ttk.Entry(info_frame_1, validate="key", validatecommand=vcmd_decimal,style='Info.TEntry')
flujo_entry.grid(row=2, column=1, sticky='EW')

    #Status LED1
statusLED1_label = ttk.Label(info_frame_1, text="Status LED1", style='Info.TLabel')
statusLED1_label.grid(row = 3, column = 0, sticky='EW')

statusLED1_entry = ttk.Entry(info_frame_1,style='Info.TEntry')
statusLED1_entry.grid(row=3, column=1, sticky='EW')

    #Status LED2
statusLED2_label = ttk.Label(info_frame_1, text="Status LED2", style='Info.TLabel')
statusLED2_label.grid(row = 3, column = 2, sticky='EW')

statusLED2_entry = ttk.Entry(info_frame_1,style='Info.TEntry')
statusLED2_entry.grid(row=3, column=3, sticky='EW')


    #Apariencia del filtro. Con desplegable
apariencia_filtro_label = ttk.Label(info_frame_1, text="Apariencia filtro", style='Info.TLabel')
apariencia_filtro_label.grid(row=4, column=0, columnspan=1, sticky='EW')

apariencia_options_var = tk.StringVar()
apariencia_options = ["","Normal","Marron"]
# Inicializar valor por defecto
apariencia_options_var.set(apariencia_options[0])
desplegable_apariencia = ttk.OptionMenu(info_frame_1, apariencia_options_var, *apariencia_options, style='Info.TMenubutton')
desplegable_apariencia.grid(row=4, column=1, columnspan=1, sticky='EW')

# --- Separador antes de Checklist General ---
sep_checklist = ttk.Separator(frame, orient='horizontal', style='Checklist.TSeparator')
sep_checklist.grid(row=2, column=0, sticky='EW')

##### CHECKLIST GRAL FRAME -2- #####
checklistgral_frame_2 = ttk.LabelFrame(frame, text = "Checklist General ➁",labelanchor="n", style='Checklist.TLabelframe',borderwidth=0)
checklistgral_frame_2.columnconfigure(0, weight=1)
checklistgral_frame_2.columnconfigure(2, weight=1)

checklistgral_frame_2.grid(row=3, column=0,sticky='WE')

general_checkbox_var = tk.BooleanVar()
   # Frame izquierdo
checklist_left = ttk.Frame(checklistgral_frame_2, style='Checklist.TLabelframe',borderwidth=0)
checklist_left.columnconfigure(0, weight=1)
checklist_left.grid(row=0, column=0, sticky='NS')

hora_label = ttk.Label(checklist_left, text="• Chequeo hora actual + instrumento", style='Checklist.TLabel')
hora_label.grid(row=0, column=0, sticky='W')
presion_label = ttk.Label(checklist_left, text="• Presion similar a la estacion", style='Checklist.TLabel')
presion_label.grid(row=1, column=0, sticky='W')
mangueras_label = ttk.Label(checklist_left, text="• Inspeccion caños y mangueras", style='Checklist.TLabel')
mangueras_label.grid(row=2, column=0, sticky='W')
aguainterna_label = ttk.Label(checklist_left, text="• Inspeccion trampa de agua interna  ", style='Checklist.TLabel')
aguainterna_label.grid(row=3, column=0, sticky='W')
aguaexterna_label = ttk.Label(checklist_left, text="• Inspeccion trampa de agua externa ", style='Checklist.TLabel')
aguaexterna_label.grid(row=4, column=0, sticky='W')
general_checkbox = ttk.Checkbutton(checklist_left, variable=general_checkbox_var, width=0, style='Checklist.TCheckbutton')
general_checkbox.grid(row=2, column=1, padx=30)

# Separador vertical
separador_ftp = ttk.Separator(checklistgral_frame_2, orient='vertical', style='Checklist.TSeparator')
separador_ftp.grid(row=0, column=1, sticky='NS', padx=10)

# Frame derecho
checklist_right = ttk.Frame(checklistgral_frame_2, style='Checklist.TLabelframe', borderwidth=0,relief='flat')
checklist_right.columnconfigure(0, weight=1)
checklist_right.rowconfigure(0, weight=1)
checklist_right.grid(row=0, column=2, sticky='NS')

# Frame interno para centrar verticalmente
ftp_block = ttk.Frame(checklist_right, style='Checklist.TLabelframe', borderwidth=0, relief='flat')
ftp_block.grid(row=0, column=0, sticky='NS')

ftpnota_label = ttk.Label(ftp_block, text="Datos semanales cargados al FTP?", style='Checklist.TLabel')
ftpnota_label.pack(pady=(20, 5))  # Espaciado arriba y abajo

ftp_check_var = tk.BooleanVar()
ftp_check = ttk.Checkbutton(ftp_block, variable=ftp_check_var, width=0, style='Checklist.TCheckbutton')
ftp_check.pack(pady=(0, 20))  # Espaciado abajo

# --- Separador antes de Chequeo Sys Counts por variable ---
sep_syscounts = ttk.Separator(frame, orient='horizontal', style='SysCounts.TSeparator')
sep_syscounts.grid(row=4, column=0, sticky='EW')

##### CHEQUEO SYS COUNTS POR VARIABLE FRAME -3- #####

check_sys_counts_frame_3 = ttk.LabelFrame(frame, text = "Chequeo Sys Counts por variable ➂",labelanchor="n", style='SysCounts.TLabelframe',borderwidth=0)
check_sys_counts_frame_3.grid(row=5, column=0,sticky='WE')

for col in range(7):  # Ajusta el rango según la cantidad de columnas que usas
    check_sys_counts_frame_3.columnconfigure(col, weight=1)

#Src set pt: #Si 0 esta tildado deshabilito entrybox

srcsetpt_label = ttk.Label(check_sys_counts_frame_3, text="➥ Src set pt:", style='SysCounts.TLabel')
srcsetpt_label.grid(row=0, column=0, sticky='W')

srcsetpt_cero_var = tk.BooleanVar()
srcsetpt_cero_check = ttk.Checkbutton(
    check_sys_counts_frame_3,
    text="0?",
    variable=srcsetpt_cero_var,
    command=disable_widgets,
    style='SysCounts.TCheckbutton'
)
srcsetpt_cero_check.grid(row=0, column=1)

srcsetpt_entry = ttk.Entry(check_sys_counts_frame_3)
srcsetpt_entry.grid(row=0, column=2)
# Sincronizar estado inicial del entry con el checkbox
disable_widgets()

#Dark Count
darkcount_label = ttk.Label(check_sys_counts_frame_3, text="• Dark count:", style='SysCounts.TLabel')
darkcount_label.grid(row=0, column=5, sticky='W')  # Si quieres también alinear este label

darkcount_entry = ttk.Entry(check_sys_counts_frame_3)
darkcount_entry.grid(row=0, column=6)

#SHTR COUNT
shtr_label = ttk.Label(check_sys_counts_frame_3, text="➥ Shtr count:", style='SysCounts.TLabel')
shtr_label.grid(row=2, column=0, sticky='W')

#shtr count-sc1
shtr_count_sc1_label = ttk.Label(check_sys_counts_frame_3,text="• sc1",style='SysCounts.TLabel')
shtr_count_sc1_label.grid(row=2, column=1)

shtr_count_sc1_entry = ttk.Entry(check_sys_counts_frame_3)
shtr_count_sc1_entry.grid(row=2, column=2)

#shtr count-sc2
shtr_count_sc2_label = ttk.Label(check_sys_counts_frame_3,text="• sc2",style='SysCounts.TLabel')
shtr_count_sc2_label.grid(row=2, column=3)

shtr_count_sc2_entry = ttk.Entry(check_sys_counts_frame_3)
shtr_count_sc2_entry.grid(row=2, column=4)

#shtr count-sc3
shtr_count_sc3_label = ttk.Label(check_sys_counts_frame_3,text="• sc3",style='SysCounts.TLabel')
shtr_count_sc3_label.grid(row=2, column=5)

shtr_count_sc3_entry = ttk.Entry(check_sys_counts_frame_3)
shtr_count_sc3_entry.grid(row=2, column=6)


#MEAS COUNT
meas_label = ttk.Label(check_sys_counts_frame_3, text="➥ Meas count:", style='SysCounts.TLabel')
meas_label.grid(row=4, column=0, sticky='W')

#meas count-sc1
meas_sc1_label = ttk.Label(check_sys_counts_frame_3,text="• sc1",style='SysCounts.TLabel')
meas_sc1_label.grid(row=4, column=1)
 
meas_sc1_entry = ttk.Entry(check_sys_counts_frame_3)
meas_sc1_entry.grid(row=4, column=2)

#meas count-sc2
meas_sc2_label = ttk.Label(check_sys_counts_frame_3,text="• sc2",style='SysCounts.TLabel')
meas_sc2_label.grid(row=4, column=3)

meas_sc2_entry = ttk.Entry(check_sys_counts_frame_3)
meas_sc2_entry.grid(row=4, column=4)

#meas count-sc3
meas_sc3_label = ttk.Label(check_sys_counts_frame_3,text="• sc3",style='SysCounts.TLabel')
meas_sc3_label.grid(row=4, column=5)

meas_sc3_entry = ttk.Entry(check_sys_counts_frame_3)
meas_sc3_entry.grid(row=4, column=6)

#BS MEAS COUNT
bs_meas_label = ttk.Label(check_sys_counts_frame_3, text="➥ Bs meas count:", style='SysCounts.TLabel')
bs_meas_label.grid(row=5, column=0, sticky='W')

#bs meas count-bsc1
bs_meas_bsc1_label = ttk.Label(check_sys_counts_frame_3,text="• bsc1",style='SysCounts.TLabel')
bs_meas_bsc1_label.grid(row=5, column=1)

bs_meas_bsc1_entry = ttk.Entry(check_sys_counts_frame_3)
bs_meas_bsc1_entry.grid(row=5, column=2)

#bs meas count-bsc2
bs_meas_bsc2_label = ttk.Label(check_sys_counts_frame_3,text="• bsc2",style='SysCounts.TLabel')
bs_meas_bsc2_label.grid(row=5, column=3)

bs_meas_bsc2_entry = ttk.Entry(check_sys_counts_frame_3)
bs_meas_bsc2_entry.grid(row=5, column=4)

#bs meas count-bsc3
bs_meas_bsc3_label = ttk.Label(check_sys_counts_frame_3,text="• bsc3",style='SysCounts.TLabel')
bs_meas_bsc3_label.grid(row=5, column=5)

bs_meas_bsc3_entry = ttk.Entry(check_sys_counts_frame_3)
bs_meas_bsc3_entry.grid(row=5, column=6)

#MEAS RATIO
meas_ratio_label = ttk.Label(check_sys_counts_frame_3, text="➥ Meas ratio:", style='SysCounts.TLabel')
meas_ratio_label.grid(row=6, column=0, sticky='W')

#meas ratio-sc1
meas_ratio_sc1_label = ttk.Label(check_sys_counts_frame_3,text="• sc1",style='SysCounts.TLabel')
meas_ratio_sc1_label.grid(row=6, column=1)

meas_ratio_sc1_entry = ttk.Entry(check_sys_counts_frame_3)
meas_ratio_sc1_entry.grid(row=6, column=2)

#meas ratio-sc2
meas_ratio_sc2_label = ttk.Label(check_sys_counts_frame_3,text="• sc2",style='SysCounts.TLabel')
meas_ratio_sc2_label.grid(row=6, column=3)

meas_ratio_sc2_entry = ttk.Entry(check_sys_counts_frame_3)
meas_ratio_sc2_entry.grid(row=6, column=4)

#meas ratio-sc3
meas_ratio_sc3_label = ttk.Label(check_sys_counts_frame_3,text="• sc3",style='SysCounts.TLabel')
meas_ratio_sc3_label.grid(row=6, column=5)

meas_ratio_sc3_entry = ttk.Entry(check_sys_counts_frame_3)
meas_ratio_sc3_entry.grid(row=6, column=6)

#BS MEAS RATIO
bs_meas_ratio_label = ttk.Label(check_sys_counts_frame_3, text="➥ Bs meas ratio:", style='SysCounts.TLabel')
bs_meas_ratio_label.grid(row=7, column=0, sticky='W')

#bs meas ratio-sc1
bs_meas_ratio_bsc1_label = ttk.Label(check_sys_counts_frame_3,text="• sc1",style='SysCounts.TLabel')
bs_meas_ratio_bsc1_label.grid(row=7, column=1)

bs_meas_ratio_bsc1_entry = ttk.Entry(check_sys_counts_frame_3)
bs_meas_ratio_bsc1_entry.grid(row=7, column=2)

#bs meas ratio-sc2
bs_meas_ratio_bsc2_label = ttk.Label(check_sys_counts_frame_3,text="• sc2",style='SysCounts.TLabel')
bs_meas_ratio_bsc2_label.grid(row=7, column=3)

bs_meas_ratio_bsc2_entry = ttk.Entry(check_sys_counts_frame_3)
bs_meas_ratio_bsc2_entry.grid(row=7, column=4)

#bs meas ratio-sc3
bs_meas_ratio_bsc3_label = ttk.Label(check_sys_counts_frame_3,text="• sc3",style='SysCounts.TLabel')
bs_meas_ratio_bsc3_label.grid(row=7, column=5)

bs_meas_ratio_bsc3_entry = ttk.Entry(check_sys_counts_frame_3)
bs_meas_ratio_bsc3_entry.grid(row=7, column=6)

# --- Separador antes de Chequeo Sys Status ---
sep_sysstatus = ttk.Separator(frame, orient='horizontal', style='SysStatus.TSeparator')
sep_sysstatus.grid(row=6, column=0, sticky='EW')

##### CHEQUEO SYS STATUS FRAME -4- #####

check_sys_status_frame_4 = ttk.LabelFrame(frame, text = "Chequeo Sys Status ➃", labelanchor="n", style='SysStatus.TLabelframe', borderwidth=0)
check_sys_status_frame_4.grid(row=7, column=0, sticky='NSEW')
check_sys_status_frame_4.columnconfigure(0, weight=1)
check_sys_status_frame_4.columnconfigure(2, weight=1)
check_sys_status_frame_4.rowconfigure(0, weight=1)

# Frame izquierdo (centrado)
sysstatus_left = ttk.Frame(check_sys_status_frame_4, style='SysStatus.TLabelframe', borderwidth=0, relief='flat')
sysstatus_left.grid(row=0, column=0, sticky='NSEW')
sysstatus_left.columnconfigure(0, weight=1)
sysstatus_left.rowconfigure(0, weight=1)

sysstatus_left_inner = ttk.Frame(sysstatus_left, style='SysStatus.TLabelframe', borderwidth=0, relief='flat')
sysstatus_left_inner.grid(row=0, column=0, sticky='NSEW')
for i in range(5):  # Ajusta según la cantidad de filas de widgets
    sysstatus_left_inner.rowconfigure(i, weight=1)
sysstatus_left_inner.columnconfigure(0, weight=1)
sysstatus_left_inner.columnconfigure(1, weight=1)
sysstatus_left_inner.columnconfigure(2, weight=1)

# Frame derecho (centrado)
sysstatus_right = ttk.Frame(check_sys_status_frame_4, style='SysStatus.TLabelframe', borderwidth=0, relief='flat')
sysstatus_right.grid(row=0, column=2, sticky='NSEW')
sysstatus_right.columnconfigure(0, weight=1)
sysstatus_right.rowconfigure(0, weight=1)

sysstatus_right_inner = ttk.Frame(sysstatus_right, style='SysStatus.TLabelframe', borderwidth=0, relief='flat')
sysstatus_right_inner.grid(row=0, column=0, sticky='NSEW')
for i in range(5):  # Ajusta según la cantidad de filas de widgets
    sysstatus_right_inner.rowconfigure(i, weight=1)
sysstatus_right_inner.columnconfigure(0, weight=1)
sysstatus_right_inner.columnconfigure(1, weight=1)
sysstatus_right_inner.columnconfigure(2, weight=1)

# Separador vertical
separador = ttk.Separator(check_sys_status_frame_4, orient='vertical', style='SysStatus.TSeparator')
separador.grid(row=0, column=1, sticky='NS', padx=10)

# --- Widgets lado izquierdo ---
major_state_label = ttk.Label(sysstatus_left_inner, text="• Major State", style='SysStatus.TLabel')
major_state_label.grid(row=0, column=0, sticky='EW')
major_state_options_var = tk.StringVar()
major_state_options = ["","Normal","Syscal", "SpnCal", "ZroCal","ZroChk","SpnChk","LeaChk","ZroAdj"]
major_state_options_var.set(major_state_options[0])
major_state_dropdown = ttk.OptionMenu(sysstatus_left_inner, major_state_options_var, *major_state_options, style='SysStatus.TMenubutton')
major_state_dropdown.grid(row=0, column=1, sticky='EW')

minor_state_label = ttk.Label(sysstatus_left_inner, text="• Minor State", style='SysStatus.TLabel')
minor_state_label.grid(row=1, column=0, sticky='EW')
minor_state_options_var = tk.StringVar()
minor_state_options = ["","Normal", "ShtrDn", "ShtrMs", "ShtrUp"]
minor_state_options_var.set(minor_state_options[0])
minor_state_dropdown = ttk.OptionMenu(sysstatus_left_inner, minor_state_options_var, *minor_state_options, style='SysStatus.TMenubutton')
minor_state_dropdown.grid(row=1, column=1, sticky='EW')

lightsource_label = ttk.Label(sysstatus_left_inner, text="• Light Source:", style='SysStatus.TLabel')
lightsource_label.grid(row=2, column=0, sticky='EW')
radioValue_lightsource = tk.StringVar(value="")
radioOne_lightsource = ttk.Radiobutton(sysstatus_left_inner, text='Pass', variable=radioValue_lightsource, value="Pass", style='SysStatus.TRadiobutton')
radioTwo_lightsource = ttk.Radiobutton(sysstatus_left_inner, text='Fail', variable=radioValue_lightsource, value="Fail", style='SysStatus.TRadiobutton')
radioOne_lightsource.grid(row=2, column=1, sticky='EW')
radioTwo_lightsource.grid(row=2, column=2, sticky='EW')

envirostatus_label = ttk.Label(sysstatus_left_inner, text="• Environment Status:", style='SysStatus.TLabel')
envirostatus_label.grid(row=3, column=0, sticky='EW')
radioValue_envirostatus = tk.StringVar()
radioOne_envirostatus = ttk.Radiobutton(sysstatus_left_inner, text='Pass', variable=radioValue_envirostatus, value="Pass", style='SysStatus.TRadiobutton')
radioTwo_envirostatus = ttk.Radiobutton(sysstatus_left_inner, text='Fail', variable=radioValue_envirostatus, value="Fail", style='SysStatus.TRadiobutton')
radioOne_envirostatus.grid(row=3, column=1, sticky='EW')
radioTwo_envirostatus.grid(row=3, column=2, sticky='EW')

shutter_label = ttk.Label(sysstatus_left_inner, text="• Shutter:", style='SysStatus.TLabel')
shutter_label.grid(row=4, column=0, sticky='EW')
radioValue_shutter = tk.StringVar()
radioOne_shutter = ttk.Radiobutton(sysstatus_left_inner, text='Pass', variable=radioValue_shutter, value="Pass", style='SysStatus.TRadiobutton')
radioTwo_shutter = ttk.Radiobutton(sysstatus_left_inner, text='Fail', variable=radioValue_shutter, value="Fail", style='SysStatus.TRadiobutton')
radioOne_shutter.grid(row=4, column=1, sticky='EW')
radioTwo_shutter.grid(row=4, column=2, sticky='EW')

# --- Widgets lado derecho ---
pmt_label = ttk.Label(sysstatus_right_inner, text="• PMT:", style='SysStatus.TLabel')
pmt_label.grid(row=0, column=0, padx=10, sticky='EW')
radioValue_pmt = tk.StringVar()
radioOne_pmt = ttk.Radiobutton(sysstatus_right_inner, text='Pass', variable=radioValue_pmt, value="Pass", style='SysStatus.TRadiobutton')
radioTwo_pmt = ttk.Radiobutton(sysstatus_right_inner, text='Fail', variable=radioValue_pmt, value="Fail", style='SysStatus.TRadiobutton')
radioOne_pmt.grid(row=0, column=1, padx=10, sticky='EW')
radioTwo_pmt.grid(row=0, column=2, padx=10, sticky='EW')

rh_label = ttk.Label(sysstatus_right_inner, text="• RH:", style='SysStatus.TLabel')
rh_label.grid(row=1, column=0, padx=10, sticky='EW')
radioValue_rh = tk.StringVar()
radioOne_rh = ttk.Radiobutton(sysstatus_right_inner, text='Pass', variable=radioValue_rh, value="Pass", style='SysStatus.TRadiobutton')
radioTwo_rh = ttk.Radiobutton(sysstatus_right_inner, text='Fail', variable=radioValue_rh, value="Fail", style='SysStatus.TRadiobutton')
radioOne_rh.grid(row=1, column=1, padx=10, sticky='EW')
radioTwo_rh.grid(row=1, column=2, padx=10, sticky='EW')

st_sensor_label = ttk.Label(sysstatus_right_inner, text="• ST sensor:", style='SysStatus.TLabel')
st_sensor_label.grid(row=2, column=0, padx=10, sticky='EW')
radioValue_st_sensor = tk.StringVar()
radioOne_st_sensor = ttk.Radiobutton(sysstatus_right_inner, text='Pass', variable=radioValue_st_sensor, value="Pass", style='SysStatus.TRadiobutton')
radioTwo_st_sensor = ttk.Radiobutton(sysstatus_right_inner, text='Fail', variable=radioValue_st_sensor, value="Fail", style='SysStatus.TRadiobutton')
radioOne_st_sensor.grid(row=2, column=1, padx=10, sticky='EW')
radioTwo_st_sensor.grid(row=2, column=2, padx=10, sticky='EW')

et_sensor_label = ttk.Label(sysstatus_right_inner, text="• ET sensor:", style='SysStatus.TLabel')
et_sensor_label.grid(row=3, column=0, padx=10, sticky='EW')
radioValue_et_sensor = tk.StringVar()
radioOne_et_sensor = ttk.Radiobutton(sysstatus_right_inner, text='Pass', variable=radioValue_et_sensor, value="Pass", style='SysStatus.TRadiobutton')
radioTwo_et_sensor = ttk.Radiobutton(sysstatus_right_inner, text='Fail', variable=radioValue_et_sensor, value="Fail", style='SysStatus.TRadiobutton')
radioOne_et_sensor.grid(row=3, column=1, padx=10, sticky='EW')
radioTwo_et_sensor.grid(row=3, column=2, padx=10, sticky='EW')

bp_sensor_label = ttk.Label(sysstatus_right_inner, text="• BP sensor:", style='SysStatus.TLabel')
bp_sensor_label.grid(row=4, column=0, padx=10, sticky='EW')
radioValue_bp_sensor = tk.StringVar()
radioOne_bp_sensor = ttk.Radiobutton(sysstatus_right_inner, text='Pass', variable=radioValue_bp_sensor, value="Pass", style='SysStatus.TRadiobutton')
radioTwo_bp_sensor = ttk.Radiobutton(sysstatus_right_inner, text='Fail', variable=radioValue_bp_sensor, value="Fail", style='SysStatus.TRadiobutton')
radioOne_bp_sensor.grid(row=4, column=1, padx=10, sticky='EW')
radioTwo_bp_sensor.grid(row=4, column=2, padx=10, sticky='EW')

# --- Separador antes de Guardar datos ---
sep_guardar = ttk.Separator(frame, orient='horizontal', style='Save.TSeparator')
sep_guardar.grid(row=8, column=0, sticky='EW')

##### OBSERV Y GUARDADO FRAME -5- #####

observ_guardar_frame_5 = ttk.LabelFrame(frame, text = "Salvar datos ➄",labelanchor="n", style='Save.TLabelframe',borderwidth=0)
observ_guardar_frame_5.grid(row=9, column=0,sticky='WE')

observ_button = ttk.Button(
    observ_guardar_frame_5,
    text="Agregar observaciones 📝",
    command=open_observ_window,
    style='Save.TButton'
)
observ_button.grid(row=0, column=0, padx=10, pady=10, ipadx=20)

guardar_button = ttk.Button(
    observ_guardar_frame_5,
    text="Guardar datos ✅",
    command=handle_guardar_click,
    style='Save.TButton'
)
guardar_button.grid(row=0, column=1, padx=80, pady=10, ipadx=20)

salir_button = ttk.Button(
    observ_guardar_frame_5,
    text="Salir 🚪",
    command=destroy_all_windows,
    style='Save.TButton'
)
salir_button.grid(row=0, column=2, padx=10, pady=10, ipadx=20)

root.mainloop()
