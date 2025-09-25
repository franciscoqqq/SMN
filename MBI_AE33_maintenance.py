# -*- coding: utf-8 -*-
"""
SEP25: Se quitan variables globales innecesarias. En su lugar, se usa un diccionario.
       Se mejora la validacion de entradas. FQ
AGO25: Mejoras en interfaz grafica. Agrego ttk. FQ
ENE25: Modifico ruta para dejarla fija p/ nuevo criterio. GM

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
filepath = "C://Aethalometer/AE33/Datos/Crudos/2025/MBI_AE33_log_2025.xlsx"
#Estructura de carga de datos fijas, solo hay que cambiarle el año

#############################################
##############  FUNCIONES   #################
#############################################

# Para que Status solo admita numeros
def validate_numeric_input(input):
    return input.isnumeric()

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

#############################################
############# GUARDADO DE DATOS #############
#############################################

def guardar_datos():
    global observaciones
    
    form_data = {
        "Hora": datetime.today().strftime('%Y-%m-%d %H:%M'),
        "Operador": operador_entry.get(),
        "Status": status_entry.get(),
        "Valve_Status_Cero": cerocheck_var.get(),
        "Valve_Status_options": cero_options_var.get(),
        "Apariencia_filtro": apariencia_options_var.get(),
        "Flujo_5lpm": flowcheck_var.get(),
        "Flujo_otro_valor": flow_entry.get(),
        "Cinta_reemplazada": reemplazocinta_var.get(),
        "Checkbox_gral": general_checkbox_var.get(),
        "FTP_check": ftp_check_var.get(),
        "Verif_Flujo_No_Necesario": verifflujononece_checkbox_var.get(),
        "Verif_Flujo_Aceptable": verifflujoacept_checkbox_var.get(),
        "Verif_Fugas": radioValue_veriffugas_var.get(),
        "Limpieza_Optica": limpiezaoptica_checkbox_var.get(),
        "Prueba_Aire_Limpio": radioValue_Airelimpio.get(),
        "Prueba_estabilidad": radioValue_Estabilidad.get(),
        "Observaciones": observaciones
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
    observ_window.configure(bg="#32506b")
    center_window(observ_window, 700, 300)

    lf = tk.LabelFrame(observ_window, text="Ingrese cualquier tipo de información relevante:", bg="#e6eef5", font=("Segoe UI", 12, "bold"))
    lf.pack(fill="both", expand=True, padx=15, pady=15,anchor="nw")

    observ_entry = tk.Text(lf, width=40, height=8, font=("Segoe UI", 12))
    observ_entry.pack(padx=10, pady=10, fill="both", expand=True)

    observ_button1 = ttk.Button(observ_window, text="Guardar y salir", command=save_observ)
    observ_button1.pack(pady=(0, 15))

    observ_window.grab_set()  # Hace modal la ventana
   # Centrar la ventana
    observ_window.update_idletasks()
    w = 700
    h = 300
    ws = observ_window.winfo_screenwidth()
    hs = observ_window.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    observ_window.geometry(f"{w}x{h}+{x}+{y}")

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
##### VENTANA: CONTROL MENSUAL. FLUJO   #####
def open_window_mensual_verificarflujo():
    
    new_window = tk.Toplevel(root)
    new_window.title("Control Mensual")
    new_window.geometry("320x100")
    center_window(new_window, 320, 100)
    new_window.grab_set()  # Hace modal la ventana
    frame_new_window = tk.Frame(new_window)
    frame_new_window.pack()
    
    calibracionflujo_frame = tk.LabelFrame(frame_new_window, text = "Calibracion de Flujo")
    calibracionflujo_frame.grid(row=0,column=0)
   
    calibflujomensual_var = tk.IntVar()
    R1_calibflujomensual = tk.Radiobutton(calibracionflujo_frame,text="Aceptable",variable=calibflujomensual_var,value=1)
    R1_calibflujomensual.grid(row=0, column=0)
    R2_calibflujomensual = tk.Radiobutton(calibracionflujo_frame,text="No aceptable",variable=calibflujomensual_var,value=2,command=lambda: [close_new_window(new_window),open_contacto_window()])
    R2_calibflujomensual.grid(row=0, column=1)
 
    quit_button = tk.Button(calibracionflujo_frame, text="Salir", command=lambda: close_new_window(new_window))
    quit_button.grid(row=1,columnspan=2)

#Cerrar ventana: Control mensual, flujo
def close_new_window(new_window):
    new_window.destroy()
    
#############################################
############ VENTANA CONTACTO ###############
def open_contacto_window():  
    return messagebox.showwarning('CONTACTO!', 'Por favor, contactarse con:\n\nGiselle Marincovich: gmarincovich@smn.gob.ar \n\nFrancisco Quarin: fquarin@smn.gob.ar\n\nMuchas Gracias') 
    messagebox.showinfo("CONTACTO")

#############################################
############ VENTANA GUARDADO EXITOSO ###############
def open_guardado_window():  
    return messagebox.showinfo("Guardado exitoso", "Datos guardados, con fecha:\n       " + datetime.today().strftime("%Y-%m-%d %H:%M"))
    
#############################################
############ VENTANA PRINCIPAL ##############

###### Ventana Principal (root) ######
root = tk.Tk()
root.title("Aethalometro") 

# Cambia el icono de la ventana
root.iconbitmap(r"C:\Aethalometer/AE33/Scripts/icono.ico")
################################################################

# Obtiene el tamaño de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_window(root, 800, 840)
root.minsize(800, 840)

# Set a default font for all widgets
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=12, family="Segoe UI")

# Use ttk theme for modern look
style = ttk.Style()
style.theme_use('vista')  # Try 'clam', 'alt', 'default', or 'vista' on Windows

frame = tk.Frame(root, bg="#f0f4f7")
frame.pack()
#frame.pack(fill="both", expand=True, padx=20, pady=20,)

##### INFO FRAME -1- #####

info_frame_1 = tk.LabelFrame(frame, text="Información", bg="#e6eef5", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
info_frame_1.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

# Configura el peso de las columnas para centrar el contenido
info_frame_1.grid_columnconfigure(0, weight=1)
info_frame_1.grid_columnconfigure(1, weight=30)
info_frame_1.grid_columnconfigure(2, weight=30)
info_frame_1.grid_columnconfigure(3, weight=30)

#Operador
operador_label = tk.Label(info_frame_1, text="Operador", bg="#e6eef5",anchor="w", justify="left")
operador_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

operador_entry = ttk.Entry(info_frame_1, font=("Segoe UI", 12))
operador_entry.grid(row=0, column=1, padx=5, pady=5,sticky="ew")

# Status (numeric only)
status_label = ttk.Label(info_frame_1, text="Status", background="#e6eef5")
status_label.grid(row=2, column=0,sticky="ew")

status_entry = ttk.Entry(info_frame_1, validate="key")
status_entry['validatecommand'] = (status_entry.register(validate_numeric_input), '%P')
status_entry.grid(row=2, column=1,sticky="ew")

#Valve status. Si 0 esta tildado, deshabilito desplegable 
valve_status_label = ttk.Label(info_frame_1, text="Valve Status",background="#e6eef5")
valve_status_label.grid(row=3, column=0,sticky="ew")

style = ttk.Style()
style.theme_use('vista')  # o 'clam', según prefieras
style.configure("Custom.TCheckbutton",
                background="#e6eef5",   # color de fondo
                foreground="#000000",   # color del texto
                font=("Segoe UI", 12))

cerocheck_var = tk.BooleanVar()
cero_checkbox = ttk.Checkbutton(info_frame_1, text="00000 : Medición", variable=cerocheck_var, command=disable_widgets,style="Custom.TCheckbutton")
cero_checkbox.grid(row=3, column=1,sticky="ew")

# Desplegable
cero_options_var = tk.StringVar()
cero_options = ["01011 : Derivación", "01100 : Calentamiento/Aire limpio", "00010 : Calibración medidor de flujo"]
dropdown = ttk.Combobox(info_frame_1, textvariable=cero_options_var, values=cero_options, state="readonly",background="white")
dropdown.grid(row=3, column=2,sticky="ew")

#Apariencia del filtro. Con desplegable
apariencia_filtro_label = ttk.Label(info_frame_1, text="Apariencia Filtro",background="#e6eef5")
apariencia_filtro_label.grid(row=4, column=0, columnspan=1,sticky="ew")

apariencia_options_var = tk.StringVar()
apariencia_options = ["Normal","Con humedad","Marron"]
desplegable_apariencia = ttk.Combobox(info_frame_1, textvariable=apariencia_options_var, values=apariencia_options, state="readonly",background="white")
desplegable_apariencia.grid(row=4, column=1,sticky="ew")

# Flujo. Si 5 lpm esta tildado deshabilito entrybox
flow_label = ttk.Label(info_frame_1, text="Flujo",background="#e6eef5")
flow_label.grid(row=5, column=0,sticky="ew")

flowcheck_var = tk.BooleanVar()
flow_check = ttk.Checkbutton(info_frame_1, text="5 lpm", variable=flowcheck_var, command=disable_widgets,style="Custom.TCheckbutton")
flow_check.grid(row=5, column=1,sticky="ew")

flow_entry = ttk.Entry(info_frame_1)
flow_entry.grid(row=5, column=2,sticky="ew")

lpm_text_label = ttk.Label(info_frame_1, text="lpm",background="#e6eef5")
lpm_text_label.grid(row=5, column=3,sticky="ew")
# Reemplazo Cinta
reemplazocinta_var = tk.BooleanVar()
reemplazocinta_checkbox = ttk.Checkbutton(info_frame_1, text="Se reemplazó la cinta", variable=reemplazocinta_var, command=disable_widgets,style="Custom.TCheckbutton")
reemplazocinta_checkbox.grid(row=6, column=0,sticky="w", pady=5)

##### CHECKLIST GRAL FRAME -2- #####

checklistgral_frame_2 = tk.LabelFrame(frame, text = "Checklist General", bg="#d5e9cd", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
checklistgral_frame_2.grid(row=1, column=0,sticky='')

checklistgral_frame_2.grid_columnconfigure(0, weight=1)
checklistgral_frame_2.grid_columnconfigure(1, weight=0)
checklistgral_frame_2.grid_columnconfigure(2, weight=0)
checklistgral_frame_2.grid_columnconfigure(3, weight=0)

# Hora actual + hora instrumento
hora_label = tk.Label(checklistgral_frame_2, text="- Chequeo hora actual + instrumento",background="#d5e9cd")
hora_label.grid(row=0, column=0)

# Inspeccion caño y manguera
mangueras_label = tk.Label(checklistgral_frame_2, text="- Inspección caños y mangueras",background="#d5e9cd")
mangueras_label.grid(row=1, column=0)

# Trampa agua interna
aguainterna_label = tk.Label(checklistgral_frame_2, text="- Inspección trampa de agua interna  ",background="#d5e9cd")
aguainterna_label.grid(row=2, column=0)

# Trampa agua externa
aguaexterna_label = tk.Label(checklistgral_frame_2, text="- Inspección trampa de agua externa ",background="#d5e9cd")
aguaexterna_label.grid(row=3, column=0)

#Checkbox gral
general_checkbox_var = tk.BooleanVar()
style.configure("Checklist.TCheckbutton", background="#d5e9cd", font=("Segoe UI", 12))
general_checkbox = ttk.Checkbutton(checklistgral_frame_2, variable=general_checkbox_var, style="Checklist.TCheckbutton")
general_checkbox.grid(row=1, column=1, rowspan=2,padx=30)

#Separador FTP
separador_ftp = ttk.Separator(checklistgral_frame_2, orient='vertical',style='TSeparator')
separador_ftp.grid(row=0, column=2, rowspan=4, sticky='ns', padx=5)
#separador_ftp.place(relx=0.5, rely=0, relwidth=1, relheight=1)

# Frame para la sección FTP, con fondo verde claro
ftp_frame = tk.Frame(checklistgral_frame_2, bg="#d5e9cd")
ftp_frame.grid(row=0, column=3, rowspan=4, sticky="nw", padx=5, pady=5)

#Check FTP
ftpnota_label = tk.Label(ftp_frame, text="Datos semanales cargados al FTP?", bg="#d5e9cd",anchor="w")
ftpnota_label.pack(anchor='w',pady=(0,25))

ftp_check_var = tk.BooleanVar()
ftp_check = ttk.Checkbutton(ftp_frame, variable=ftp_check_var, style="Checklist.TCheckbutton")
ftp_check.pack(pady=(0,10))

##### CONTROL MENSUAL FRAME -3- #####
style.configure("Mensual.TCheckbutton", background="#f0f5d2", font=("Segoe UI", 12))

controlmensual_frame_3 = tk.LabelFrame(frame, text = "Control Mensual", bg="#f0f5d2", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
controlmensual_frame_3.grid(row=2, column=0,sticky='WE')

#Control Mensual. Verificacion de flujo. 
                    #if Nonecesario esta tildado, entro a toggle_buttons para deshabilitar botones.
verifflujo_label = tk.Label(controlmensual_frame_3, text="Verificación de flujo",background="#f0f5d2")
verifflujo_label.grid(row=0, column=0)

verifflujononece_checkbox_var = tk.BooleanVar()
verifflujononece_checkbox = ttk.Checkbutton(controlmensual_frame_3, text="No necesario", variable=verifflujononece_checkbox_var, command=lambda: toggle_buttons(verifflujononece_checkbox_var, verifflujoacept_checkbox, verifflujonoacept_button),style="Mensual.TCheckbutton")
verifflujononece_checkbox.grid(row=0, column=1, padx=30,pady=10)

verifflujoacept_checkbox_var = tk.BooleanVar()
verifflujoacept_checkbox = tk.Checkbutton(controlmensual_frame_3, variable = verifflujoacept_checkbox_var,text="Aceptable",background="#f0f5d2")
verifflujoacept_checkbox.grid(row=0, column=2,ipadx=30)

verifflujonoacept_button_var = tk.BooleanVar()
verifflujonoacept_button = tk.Button(controlmensual_frame_3, text="No aceptable", command=open_window_mensual_verificarflujo,bg="#dddddd")
verifflujonoacept_button.grid(row=0, column=3,ipadx=30,pady=10)

#Control Mensual. Verificacion de fugas

veriffugas_label = tk.Label(controlmensual_frame_3, text="Verificación de fugas",background="#f0f5d2")
veriffugas_label.grid(row=1, column=0)

radioValue_veriffugas_var = tk.IntVar()
radioOne_veriffugas = tk.Radiobutton(controlmensual_frame_3, text='No necesario',variable=radioValue_veriffugas_var, value=1,background="#f0f5d2") 
radioTwo_veriffugas = tk.Radiobutton(controlmensual_frame_3, text='Aceptable',variable=radioValue_veriffugas_var, value=2,background="#f0f5d2") 
radioThree_veriffugas = tk.Radiobutton(controlmensual_frame_3, text='No aceptable',variable=radioValue_veriffugas_var, value=3,command=open_contacto_window,background="#f0f5d2")

radioOne_veriffugas.grid(row=1, column=1)
radioTwo_veriffugas.grid(row=1, column=2)
radioThree_veriffugas.grid(row=1, column=3)

##### CONTROL SEMESTRAL FRAME -4- #####

controlsemestral_frame_4 = tk.LabelFrame(frame, text = "Control Semestral", bg="#f1bfdd", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
controlsemestral_frame_4.grid(row=3, column=0,sticky='WE')

#Control Semestral: Limpieza optica
limpiezaoptica_label = tk.Label(controlsemestral_frame_4, text="Limpieza Óptica",background="#f1bfdd")
limpiezaoptica_label.grid(row=0, column=0) 

style.configure("Optica.TCheckbutton",
                background="#f1bfdd",   # color de fondo
                foreground="#000000",   # color del texto
                font=("Segoe UI", 12))

limpiezaoptica_checkbox_var = tk.BooleanVar()
limpiezaoptica_checkbox = ttk.Checkbutton(controlsemestral_frame_4, variable=limpiezaoptica_checkbox_var,width=0.1,style="Optica.TCheckbutton")
limpiezaoptica_checkbox.grid(row=0, column=1)

#Control Semestral: Prueba aire limpio
                    #Radiobutton
pruebaairelimpio_label = tk.Label(controlsemestral_frame_4, text="Prueba Aire limpio",background="#f1bfdd")
pruebaairelimpio_label.grid(row=1, column=0)

radioValue_Airelimpio = tk.IntVar()

radioOne_Airelimpio = tk.Radiobutton(controlsemestral_frame_4, text='No necesario',variable=radioValue_Airelimpio, value=1,background="#f1bfdd") 
radioOne_Airelimpio.grid(row=1, column=1,ipadx=30)

radioTwo_Airelimpio = tk.Radiobutton(controlsemestral_frame_4, text='Aceptable',variable=radioValue_Airelimpio, value=2,background="#f1bfdd") 
radioTwo_Airelimpio.grid(row=1, column=2,ipadx=30)

radioThree_Airelimpio = tk.Radiobutton(controlsemestral_frame_4, text='No aceptable',variable=radioValue_Airelimpio, value=3,command=open_contacto_window,background="#f1bfdd")
radioThree_Airelimpio.grid(row=1, column=3,ipadx=30)

#Control Semestral: Prueba estabilidad
                    #Radiobutton
pruebaestabilidad_label = tk.Label(controlsemestral_frame_4, text="Prueba Estabilidad",background="#f1bfdd")
pruebaestabilidad_label.grid(row=2, column=0)

radioValue_Estabilidad = tk.IntVar()

radioOne_Estabilidad = tk.Radiobutton(controlsemestral_frame_4, text='No necesario',variable=radioValue_Estabilidad, value=1,background="#f1bfdd") 
radioOne_Estabilidad.grid(row=2, column=1)

radioTwo_Estabilidad = tk.Radiobutton(controlsemestral_frame_4, text='Aceptable',variable=radioValue_Estabilidad, value=2,background="#f1bfdd") 
radioTwo_Estabilidad.grid(row=2, column=2)

radioThree_Estabilidad = tk.Radiobutton(controlsemestral_frame_4, text='No aceptable',variable=radioValue_Estabilidad, value=3,command=open_contacto_window,background="#f1bfdd")
radioThree_Estabilidad.grid(row=2, column=3)

##### OBSERV Y GUARDADO FRAME -5- #####

observ_guardar_frame_5 = tk.LabelFrame(frame, text = "Salvar datos",background="#f7d6b4", font=("Segoe UI", 12, "bold"), padx=10, pady=10)
observ_guardar_frame_5.grid(row=4, column=0,sticky='WE')

style.configure(
    "Custom.TButton",
    background="#b67224",
    foreground="black",
    font=("Segoe UI", 12, "bold"),
    padding=6
)
style.map(
    "Custom.TButton",
    background=[("active", "#14837d")]
)

#Observaciones
observaciones = ""
observ_button = ttk.Button(observ_guardar_frame_5, text="Agregar observaciones", command=open_observ_window,style="Custom.TButton")
observ_button.grid(row=0, column=0, padx=10, pady=10,ipadx=20)

#GUARDAR
guardar_button = ttk.Button(observ_guardar_frame_5, text="Guardar datos",command=guardar_datos,style="Custom.TButton")
guardar_button.grid(row=0, column=1, padx=80, pady=10, ipadx=20)

#SALIR
salir_button = ttk.Button(observ_guardar_frame_5, text="Salir",command=destroy_all_windows,style="Custom.TButton")
salir_button.grid(row=0, column=2, padx=10, pady=10, ipadx=20)

root.mainloop()