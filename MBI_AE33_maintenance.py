# -*- coding: utf-8 -*-
"""
Modifiqué la ruta para dejarla fija en base a nuestro nuevo criterio GM enero 2025

@author: fquarin
"""
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
import os
import openpyxl
from datetime import datetime

################################################################
#INGRESAR DIRECCION Y NOMBRE DE LA PLANILLA A CREAR/MODIFICAR
#filepath = "____________________________________________________"
filepath = "C://Aethalometer/AE33/Datos/Crudos/2025/MBI_AE33_log_2025.xlsx"
#Estructura de carga de datos fijas, solo hay que cambiarle el año
################################################################



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
    
    global OPERADOR, STATUS, VALVE_STATUS_CERO, VALVE_STATUS_OPTIONS, APARIENCIA_FILTRO
    global FLUJO_5, FLUJO_otrovalor, CINTA_REEMPLAZADA, CHECKBOX_GRAL
    global FTP_CHECK, VERIF_FLUJO_NONECESARIO, VERIF_FLUJO_OK, VERIF_FUGAS, LIMPIEZA_OPTICA
    global PRUEBA_AIRELIMPIO, PRUEBA_ESTABILIDAD, OBSERVACIONES,observaciones
    
    OPERADOR = operador_entry.get()
    STATUS = status_entry.get()
    VALVE_STATUS_CERO = cerocheck_var.get()
    VALVE_STATUS_OPTIONS = cero_options_var.get()
    APARIENCIA_FILTRO = apariencia_options_var.get()
    FLUJO_5 = flowcheck_var.get()
    FLUJO_otrovalor = flow_entry.get()
    CINTA_REEMPLAZADA = reemplazocinta_var.get()
    CHECKBOX_GRAL = general_checkbox_var.get()
    FTP_CHECK = ftp_check_var.get()
    
    VERIF_FLUJO_NONECESARIO = verifflujononece_checkbox_var.get()
    VERIF_FLUJO_OK = verifflujoacept_checkbox_var.get()
    VERIF_FUGAS = radioValue_veriffugas_var.get()
    
    LIMPIEZA_OPTICA = limpiezaoptica_checkbox_var.get()
    PRUEBA_AIRELIMPIO = radioValue_Airelimpio.get()
    PRUEBA_ESTABILIDAD = radioValue_Estabilidad.get()
    
    OBSERVACIONES = observaciones
   
    print(datetime.today().strftime('%Y-%m-%d %H:%M'))
    print(OPERADOR,STATUS,VALVE_STATUS_CERO,VALVE_STATUS_OPTIONS,APARIENCIA_FILTRO)
    print(FLUJO_5,FLUJO_otrovalor,CINTA_REEMPLAZADA,CHECKBOX_GRAL)
    print(FTP_CHECK,VERIF_FLUJO_NONECESARIO,VERIF_FLUJO_OK,VERIF_FUGAS)
    print(LIMPIEZA_OPTICA,PRUEBA_AIRELIMPIO,PRUEBA_ESTABILIDAD)
    print(OBSERVACIONES)
    
    if not os.path.exists(filepath):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        heading = ["Hora", "Operador", "Status", "Valve Status Zero", "Valve Status options", "Apariencia filtro",
                   "Flujo 5lpm?", "Flujo otro valor", "Cinta reemplazada?","Checkbox gral",
                   "FTP check", "Verif. Flujo No Necesario", "Verif. Flujo Aceptable", "Verif. Fugas",
                   "Limpieza Optica", "Prueba Aire Limpio", "Prueba estabilidad",
                   "Observaciones"]
        sheet.append(heading)
        workbook.save(filepath)
        
    workbook = openpyxl.load_workbook(filepath)
    sheet = workbook.active
    sheet.append([datetime.today().strftime('%Y-%m-%d %H:%M'),OPERADOR,STATUS,VALVE_STATUS_CERO,VALVE_STATUS_OPTIONS,APARIENCIA_FILTRO,
                  FLUJO_5,FLUJO_otrovalor,CINTA_REEMPLAZADA,CHECKBOX_GRAL,
                  FTP_CHECK,VERIF_FLUJO_NONECESARIO,VERIF_FLUJO_OK,VERIF_FUGAS,
                  LIMPIEZA_OPTICA,PRUEBA_AIRELIMPIO,PRUEBA_ESTABILIDAD,
                  OBSERVACIONES])
    workbook.save(filepath)
    
#############################################
############## VENTANAS EXTRA ###############
#############################################


######### VENTANA: OBSERVACIONES ############
def open_observ_window():
    global observ_window
    global observ_entry
    observ_window = tk.Toplevel(root)
    observ_window.title("Observaciones")
   
    observ_label = tk.Label(observ_window, text="Ingrese cualquier tipo\n\nde informacion relevante:")
    observ_label.grid(row=0, column=0, padx=10, pady=10)
    
    observ_entry = tk.Text(observ_window, width=20, height=10, font=("Helvetica", 16))
    observ_entry.grid(row=0, column=1, padx=10, pady=10)
    
    observ_button1 = ttk.Button(observ_window, text="Guardar y salir ",command=save_observ)
    observ_button1.grid(row=3,column=2)  
    
    observ_window.mainloop()
    
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
    new_window.geometry("320x70")
    
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

    new_window.mainloop()
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
root.geometry("")

frame = tk.Frame(root)
frame.pack()

##### INFO FRAME -1- #####

info_frame_1 = tk.LabelFrame(frame, text = "Información")
info_frame_1.grid(row=0, column=0)

#Operador
operador_label = tk.Label(info_frame_1,  text="Operador")
operador_label.grid(row=1, column=0)

operador_entry = tk.Entry(info_frame_1)
operador_entry.grid(row=1, column=1)

#Status. Solo se puede ingresar numeros
status_label = tk.Label(info_frame_1, text="Status")
status_label.grid(row=2, column=0)

status_entry = tk.Entry(info_frame_1, validate="key")
status_entry['validatecommand'] = (status_entry.register(validate_numeric_input), '%P')
status_entry.grid(row=2, column=1)

#Valve status. Si 0 esta tildado, deshabilito desplegable 
valve_status_label = tk.Label(info_frame_1, text="Valve Status")
valve_status_label.grid(row = 3, column = 0)

cerocheck_var = tk.BooleanVar()
cero_checkbox = tk.Checkbutton(info_frame_1, text="00000 : Medición", variable=cerocheck_var, command=disable_widgets)
cero_checkbox.grid(row=3, column=1)

     # Desplegable
cero_options_var = tk.StringVar()
cero_options = ["01011 : Derivación", "01100 : Calentamiento/Aire limpio", "00010 : Calibración medidor de flujo"]
dropdown = tk.OptionMenu(info_frame_1, cero_options_var, *cero_options)
dropdown.grid(row=3, column=2)

#Apariencia del filtro. Con desplegable
apariencia_filtro_label = tk.Label(info_frame_1, text="Apariencia Filtro")
apariencia_filtro_label.grid(row=4, column=0, columnspan=1)

apariencia_options_var = tk.StringVar()
apariencia_options = ["Normal","Con humedad","Marron"]
desplegable_apariencia = tk.OptionMenu(info_frame_1, apariencia_options_var, *apariencia_options)
desplegable_apariencia.grid(row=4, column=1)

# Flujo. Si 5 lpm esta tildado deshabilito entrybox
flow_label = tk.Label(info_frame_1, text="Flujo")
flow_label.grid(row=5, column=0)

flowcheck_var = tk.BooleanVar()
flow_check = tk.Checkbutton(info_frame_1, text="5 lpm",variable=flowcheck_var, command=disable_widgets)
flow_check.grid(row=5, column=1)

flow_entry = tk.Entry(info_frame_1)
flow_entry.grid(row=5, column=2)

lpm_text_label = tk.Label(info_frame_1, text = "lpm")
lpm_text_label.grid(row=5,column=3)

# Reemplazo Cinta
reemplazocinta_var = tk.BooleanVar()
reemplazocinta_checkbox = tk.Checkbutton(info_frame_1, text="Se reemplazó la cinta", variable=reemplazocinta_var, command=disable_widgets)
reemplazocinta_checkbox.grid(row=6, column=1)

##### CHECKLIST GRAL FRAME -2- #####

checklistgral_frame_2 = tk.LabelFrame(frame, text = "Checklist General")
checklistgral_frame_2.grid(row=1, column=0,sticky='')

# Hora actual + hora instrumento
hora_label = tk.Label(checklistgral_frame_2, text="- Chequeo hora actual + instrumento")
hora_label.grid(row=0, column=0)

# Inspeccion caño y manguera
mangueras_label = tk.Label(checklistgral_frame_2, text="- Inspeccion caños y mangueras")
mangueras_label.grid(row=1, column=0)

# Trampa agua interna
aguainterna_label = tk.Label(checklistgral_frame_2, text="- Inspeccion trampa de agua interna  ")
aguainterna_label.grid(row=2, column=0)

# Trampa agua externa
aguaexterna_label = tk.Label(checklistgral_frame_2, text="- Inspeccion trampa de agua externa ")
aguaexterna_label.grid(row=3, column=0)

#Checkbox gral
general_checkbox_var = tk.BooleanVar()
general_checkbox = tk.Checkbutton(checklistgral_frame_2,variable=general_checkbox_var, width=0)
general_checkbox.grid(row=1, column=1, rowspan=2,padx=30)

#Separador FTP
separador_ftp = ttk.Separator(checklistgral_frame_2, orient='vertical')
separador_ftp.place(relx=0.5, rely=0, relwidth=1, relheight=1)

#Check FTP
ftpnota_label = tk.Label(checklistgral_frame_2, text="Datos semanales cargados al FTP?")
ftpnota_label.grid(row=0, column=3, rowspan=3,padx=30)

ftp_check_var=tk.BooleanVar()
ftp_check=tk.Checkbutton(checklistgral_frame_2,variable=ftp_check_var)
ftp_check.grid(row=1, column=3, rowspan=3, padx = 30)

##### CONTROL MENSUAL FRAME -3- #####

controlmensual_frame_3 = tk.LabelFrame(frame, text = "Control Mensual")
controlmensual_frame_3.grid(row=2, column=0,sticky='WE')

#Control Mensual. Verificacion de flujo. 
                    #if Nonecesario esta tildado, entro a toggle_buttons para deshabilitar botones.
verifflujo_label = tk.Label(controlmensual_frame_3, text="Verificacion de flujo")
verifflujo_label.grid(row=0, column=0)

verifflujononece_checkbox_var = tk.BooleanVar()
verifflujononece_checkbox = tk.Checkbutton(controlmensual_frame_3, text="No necesario", variable=verifflujononece_checkbox_var, command=lambda: toggle_buttons(verifflujononece_checkbox_var, verifflujoacept_checkbox, verifflujonoacept_button))
verifflujononece_checkbox.grid(row=0, column=1, ipadx=30)

verifflujoacept_checkbox_var = tk.BooleanVar()
verifflujoacept_checkbox = tk.Checkbutton(controlmensual_frame_3, variable = verifflujoacept_checkbox_var,text="Aceptable")
verifflujoacept_checkbox.grid(row=0, column=2,ipadx=30)

verifflujonoacept_button_var = tk.BooleanVar()
verifflujonoacept_button = tk.Button(controlmensual_frame_3, text="No aceptable", command=open_window_mensual_verificarflujo)
verifflujonoacept_button.grid(row=0, column=3,ipadx=30,pady=10)

#Control Mensual. Verificacion de fugas

veriffugas_label = tk.Label(controlmensual_frame_3, text="Verificacion de fugas")
veriffugas_label.grid(row=1, column=0)

radioValue_veriffugas_var = tk.IntVar()
radioOne_veriffugas = tk.Radiobutton(controlmensual_frame_3, text='No necesario',variable=radioValue_veriffugas_var, value=1) 
radioTwo_veriffugas = tk.Radiobutton(controlmensual_frame_3, text='Aceptable',variable=radioValue_veriffugas_var, value=2) 
radioThree_veriffugas = tk.Radiobutton(controlmensual_frame_3, text='No aceptable',variable=radioValue_veriffugas_var, value=3,command=open_contacto_window)

radioOne_veriffugas.grid(row=1, column=1)
radioTwo_veriffugas.grid(row=1, column=2)
radioThree_veriffugas.grid(row=1, column=3)

##### CONTROL SEMESTRAL FRAME -4- #####

controlsemestral_frame_4 = tk.LabelFrame(frame, text = "Control Semestral")
controlsemestral_frame_4.grid(row=3, column=0,sticky='WE')

#Control Semestral: Limpieza optica
limpiezaoptica_label = tk.Label(controlsemestral_frame_4, text="Limpieza Optica")
limpiezaoptica_label.grid(row=0, column=0) 

limpiezaoptica_checkbox_var = tk.BooleanVar()
limpiezaoptica_checkbox = ttk.Checkbutton(controlsemestral_frame_4, variable=limpiezaoptica_checkbox_var,width=0)
limpiezaoptica_checkbox.grid(row=0, column=1)

#Control Semestral: Prueba aire limpio
                    #Radiobutton
pruebaairelimpio_label = tk.Label(controlsemestral_frame_4, text="Prueba Aire limpio")
pruebaairelimpio_label.grid(row=1, column=0)

radioValue_Airelimpio = tk.IntVar()

radioOne_Airelimpio = tk.Radiobutton(controlsemestral_frame_4, text='No necesario',variable=radioValue_Airelimpio, value=1) 
radioOne_Airelimpio.grid(row=1, column=1,ipadx=30)

radioTwo_Airelimpio = tk.Radiobutton(controlsemestral_frame_4, text='Aceptable',variable=radioValue_Airelimpio, value=2) 
radioTwo_Airelimpio.grid(row=1, column=2,ipadx=30)

radioThree_Airelimpio = tk.Radiobutton(controlsemestral_frame_4, text='No aceptable',variable=radioValue_Airelimpio, value=3,command=open_contacto_window)
radioThree_Airelimpio.grid(row=1, column=3,ipadx=30)

#Control Semestral: Prueba estabilidad
                    #Radiobutton
pruebaestabilidad_label = tk.Label(controlsemestral_frame_4, text="Prueba Estabilidad")
pruebaestabilidad_label.grid(row=2, column=0)

radioValue_Estabilidad = tk.IntVar()

radioOne_Estabilidad = tk.Radiobutton(controlsemestral_frame_4, text='No necesario',variable=radioValue_Estabilidad, value=1) 
radioOne_Estabilidad.grid(row=2, column=1)

radioTwo_Estabilidad = tk.Radiobutton(controlsemestral_frame_4, text='Aceptable',variable=radioValue_Estabilidad, value=2) 
radioTwo_Estabilidad.grid(row=2, column=2)

radioThree_Estabilidad = tk.Radiobutton(controlsemestral_frame_4, text='No aceptable',variable=radioValue_Estabilidad, value=3,command=open_contacto_window)
radioThree_Estabilidad.grid(row=2, column=3)

##### OBSERV Y GUARDADO FRAME -5- #####

observ_guardar_frame_5 = tk.LabelFrame(frame, text = "Salvar datos")
observ_guardar_frame_5.grid(row=4, column=0,sticky='WE')

#Observaciones
observ_button = tk.Button(observ_guardar_frame_5, text="Agregar observaciones", command=open_observ_window)
observ_button.grid(row=0, column=0, padx=10, pady=10,ipadx=20)

#GUARDAR
guardar_button = tk.Button(observ_guardar_frame_5, text="Guardar datos",command=lambda:[guardar_datos(),open_guardado_window()])
guardar_button.grid(row=0, column=1, padx=80, pady=10, ipadx=20)

#SALIR
salir_button = tk.Button(observ_guardar_frame_5, text="Salir",command=destroy_all_windows)
salir_button.grid(row=0, column=2, padx=10, pady=10, ipadx=20)

root.mainloop()
