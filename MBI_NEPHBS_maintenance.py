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
filepath = "C://Nephelometer/Nephelometer_integrating_AURORA3000/Datos/Crudos/2025/MBI_NEPHBS_log_2025.xlsx"
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
###Si normal  esta checkeado --> Disable dropdown de major state
#     if major_state_check_var.get() == 1:
#         major_state_dropdown.config(state='disabled')
#     else:
#         major_state_dropdown.config(state='normal')  
# ###Si normal  esta checkeado --> Disable dropdown de minor state
#     if minor_state_check_var.get() == 1:
#         minor_state_dropdown.config(state='disabled')
#     else:
#         minor_state_dropdown.config(state='normal') 
####Si 0 srcsetpt esta checkeado --> Disable flujo blankbox
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

#####################################################
############ VENTANA GUARDADO EXITOSO ###############
def open_guardado_window():  
    return messagebox.showinfo("Guardado exitoso", "Datos guardados, con fecha:\n       " + datetime.today().strftime("%Y-%m-%d %H:%M"))

#############################################
############# GUARDADO DE DATOS #############
#############################################

def guardar_datos():
    
    global OPERADOR,FLUJO,STATUSLED1,STATUSLED2,APARIENCIA_FILTRO
    global CHECKBOX_GRAL,FTP_CHECK
    global SRCSETPT_CERO,SRCSETPT,DARKCOUNT,SHTR_COUNT_SC1,SHTR_COUNT_SC2,SHTR_COUNT_SC3
    global MEAS_SC1,MEAS_SC2,MEAS_SC3,BS_MEAS_BSC1,BS_MEAS_BSC2,BS_MEAS_BSC3
    global MEAS_RATIO_SC1,MEAS_RATIO_SC2,MEAS_RATIO_SC3,BS_MEAS_RATIO_BSC1,BS_MEAS_RATIO_BSC2,BS_MEAS_RATIO_BSC3
    global MAJOR_STATE_OPTIONS,MINOR_STATE_OPTIONS,LIGHTSOURCE,ENVIRONMENT_STATUS,SHUTTER,PMT,RH,ST_SENSOR,ET_SENSOR,BP_SENSOR
    global OBSERVACIONES, observaciones
    
    OPERADOR = operador_entry.get()
    FLUJO = flujo_entry.get() 
    STATUSLED1 = statusLED1_entry.get()
    STATUSLED2 = statusLED2_entry.get()
    APARIENCIA_FILTRO = apariencia_options_var.get()
    
    CHECKBOX_GRAL = general_checkbox_var.get()
    FTP_CHECK = ftp_check_var.get()
    
    SRCSETPT_CERO = srcsetpt_cero_var.get()
    SRCSETPT = srcsetpt_entry.get()
    DARKCOUNT = darkcount_entry.get()
    SHTR_COUNT_SC1 = shtr_count_sc1_entry.get()
    SHTR_COUNT_SC2 = shtr_count_sc2_entry.get()
    SHTR_COUNT_SC3 = shtr_count_sc3_entry.get()
    MEAS_SC1 = meas_sc1_entry.get()
    MEAS_SC2 = meas_sc2_entry.get()
    MEAS_SC3 = meas_sc3_entry.get()
    BS_MEAS_BSC1 = bs_meas_bsc1_entry.get()
    BS_MEAS_BSC2 = bs_meas_bsc2_entry.get()
    BS_MEAS_BSC3 = bs_meas_bsc3_entry.get()
    MEAS_RATIO_SC1 = meas_ratio_sc1_entry.get()
    MEAS_RATIO_SC2 = meas_ratio_sc2_entry.get()
    MEAS_RATIO_SC3 = meas_ratio_sc3_entry.get()
    BS_MEAS_RATIO_BSC1 = bs_meas_ratio_bsc1_entry.get()
    BS_MEAS_RATIO_BSC2 = bs_meas_ratio_bsc2_entry.get()
    BS_MEAS_RATIO_BSC3 = bs_meas_ratio_bsc3_entry.get()
        
    #MAJOR_STATE_NORMAL = major_state_check_var.get()
    MAJOR_STATE_OPTIONS = major_state_options_var.get()
    #MINOR_STATE_NORMAL = minor_state_check_var.get()
    MINOR_STATE_OPTIONS = minor_state_options_var.get()
    LIGHTSOURCE = radioValue_lightsource.get()
    ENVIRONMENT_STATUS = radioValue_envirostatus.get()
    SHUTTER = radioValue_shutter.get()
    PMT = radioValue_pmt.get()
    RH = radioValue_rh.get()
    ST_SENSOR = radioValue_st_sensor.get()
    ET_SENSOR = radioValue_et_sensor.get()
    BP_SENSOR = radioValue_bp_sensor.get()
    
    OBSERVACIONES = observaciones
   
    print(datetime.today().strftime('%Y-%m-%d %H:%M'))
    print(OPERADOR,FLUJO,STATUSLED1,STATUSLED2,APARIENCIA_FILTRO)
    print(CHECKBOX_GRAL,FTP_CHECK)
    print(SRCSETPT_CERO,SRCSETPT,DARKCOUNT,SHTR_COUNT_SC1,SHTR_COUNT_SC2,SHTR_COUNT_SC3)
    print(MEAS_SC1,MEAS_SC2,MEAS_SC3,BS_MEAS_BSC1,BS_MEAS_BSC2,BS_MEAS_BSC3)
    print(MEAS_RATIO_SC1,MEAS_RATIO_SC2,MEAS_RATIO_SC3,BS_MEAS_RATIO_BSC1,BS_MEAS_RATIO_BSC2,BS_MEAS_RATIO_BSC3)
    print(MAJOR_STATE_OPTIONS,MINOR_STATE_OPTIONS,LIGHTSOURCE,ENVIRONMENT_STATUS,SHUTTER,PMT,RH,ST_SENSOR,ET_SENSOR,BP_SENSOR)
    
    print(OBSERVACIONES)
    
    if not os.path.exists(filepath):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        heading = ["Hora", "Operador", "Flujo", "Status Led1", "Status Led2", "Apariencia Filtro", "Checkbox Gral",
                    "FTP check", "Source Set Point Zero?","Source Set Point", "Dark Count","Shutter Count SC1",
                    "Shutter Count SC2", "Shutter Count SC3",
                    "Meas SC1", "Meas SC2", "Meas SC3", "BS Meas BSC1",
                    "BS Meas BSC2", "BS Meas BSC3", "Meas Ratio SC1","Meas Ratio SC2", "Meas Ratio SC3",
                    "BS Meas Ratio BSC1", "BS Meas Ratio BSC2", "BS Meas Ratio BSC3",
                    "Major State Options", "Minor State Options", "LightSource",
                    "Environment Status", "Shutter", "PMT", "RH", "ST Sensor","Et Sensor",
                    "BP Sensor",
                    "Observaciones"]
        sheet.append(heading)
        workbook.save(filepath)
        
    workbook = openpyxl.load_workbook(filepath)
    sheet = workbook.active
    sheet.append([datetime.today().strftime('%Y-%m-%d %H:%M'),OPERADOR,FLUJO,STATUSLED1,STATUSLED2,APARIENCIA_FILTRO,
                  CHECKBOX_GRAL,FTP_CHECK,
                  SRCSETPT_CERO,SRCSETPT,DARKCOUNT,SHTR_COUNT_SC1,SHTR_COUNT_SC2,SHTR_COUNT_SC3,
                  MEAS_SC1,MEAS_SC2,MEAS_SC3,BS_MEAS_BSC1,BS_MEAS_BSC2,BS_MEAS_BSC3,
                  MEAS_RATIO_SC1,MEAS_RATIO_SC2,MEAS_RATIO_SC3,BS_MEAS_RATIO_BSC1,BS_MEAS_RATIO_BSC2,BS_MEAS_RATIO_BSC3,
                  MAJOR_STATE_OPTIONS,MINOR_STATE_OPTIONS,LIGHTSOURCE,ENVIRONMENT_STATUS,SHUTTER,PMT,RH,ST_SENSOR,ET_SENSOR,BP_SENSOR,
                  OBSERVACIONES])
    workbook.save(filepath)
    
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

frame = tk.Frame(root)
frame.pack()

##### INFO FRAME -1- #####
info_frame_1 = tk.LabelFrame(frame, text = "Información",labelanchor="n")
info_frame_1.grid(row=0, column=0)

    #Operador
operador_label = tk.Label(info_frame_1,  text="Operador")
operador_label.grid(row=1, column=0)

operador_entry = tk.Entry(info_frame_1)
operador_entry.grid(row=1, column=1)

    #Flujo. Solo se puede ingresar numeros
flujo_label = tk.Label(info_frame_1, text="Flujo actual")
flujo_label.grid(row=2, column=0)

flujo_entry = tk.Entry(info_frame_1, validate="key")
#flujo_entry['validatecommand'] = (flujo_entry.register(validate_numeric_input), '%P')
flujo_entry.grid(row=2, column=1)

    #Status LED1
statusLED1_label = tk.Label(info_frame_1, text="Status LED1")
statusLED1_label.grid(row = 3, column = 0)

statusLED1_entry = tk.Entry(info_frame_1)
statusLED1_entry.grid(row=3, column=1)

    #Status LED2
statusLED2_label = tk.Label(info_frame_1, text="Status LED2")
statusLED2_label.grid(row = 3, column = 2)

statusLED2_entry = tk.Entry(info_frame_1)
statusLED2_entry.grid(row=3, column=3)


    #Apariencia del filtro. Con desplegable
apariencia_filtro_label = tk.Label(info_frame_1, text="Apariencia filtro")
apariencia_filtro_label.grid(row=4, column=0, columnspan=1)

apariencia_options_var = tk.StringVar()
apariencia_options = ["Normal","Marron"]
desplegable_apariencia = tk.OptionMenu(info_frame_1, apariencia_options_var, *apariencia_options)
desplegable_apariencia.grid(row=4, column=1)

##### CHECKLIST GRAL FRAME -2- #####
checklistgral_frame_2 = tk.LabelFrame(frame, text = "Checklist General",labelanchor="n")
checklistgral_frame_2.grid(row=1, column=0)

    # Hora actual + hora instrumento
hora_label = tk.Label(checklistgral_frame_2, text="- Chequeo hora actual + instrumento")
hora_label.grid(row=0, column=0)

    # Presion similar a la estacion
presion_label = tk.Label(checklistgral_frame_2, text="- Presion similar a la estacion")
presion_label.grid(row=1, column=0)

    # Inspeccion caño y manguera
mangueras_label = tk.Label(checklistgral_frame_2, text="- Inspeccion caños y mangueras")
mangueras_label.grid(row=2, column=0)

    # Trampa agua interna
aguainterna_label = tk.Label(checklistgral_frame_2, text="- Inspeccion trampa de agua interna  ")
aguainterna_label.grid(row=3, column=0)

    # Trampa agua externa
aguaexterna_label = tk.Label(checklistgral_frame_2, text="- Inspeccion trampa de agua externa ")
aguaexterna_label.grid(row=4, column=0)

    #Checkbox gral
general_checkbox_var = tk.BooleanVar()
general_checkbox = tk.Checkbutton(checklistgral_frame_2,variable=general_checkbox_var, width=0)
general_checkbox.grid(row=2, column=1,padx=30)

#Separador FTP
separador_ftp = ttk.Separator(checklistgral_frame_2, orient='vertical')
separador_ftp.place(relx=0.5, rely=0, relwidth=1, relheight=1)

#Check FTP
ftpnota_label = tk.Label(checklistgral_frame_2, text="Datos semanales cargados al FTP?")
ftpnota_label.grid(row=0, column=3, rowspan=3,padx=30)

ftp_check_var=tk.BooleanVar()
ftp_check=tk.Checkbutton(checklistgral_frame_2,variable=ftp_check_var)
ftp_check.grid(row=1, column=3, rowspan=3, padx = 30)

##### CHEQUEO SYS COUNTS POR VARIABLE FRAME -3- #####

check_sys_counts_frame_3 = tk.LabelFrame(frame, text = "Chequeo Sys Counts por variable",labelanchor="n")
check_sys_counts_frame_3.grid(row=2, column=0,sticky='WE')

#Src set pt
    #Si 0 esta tildado deshabilito entrybox

srcsetpt_label = tk.Label(check_sys_counts_frame_3, text="Src set pt:")
srcsetpt_label.grid(row=0, column=0)

srcsetpt_cero_var = tk.BooleanVar()
srcsetpt_cero_check = tk.Checkbutton(check_sys_counts_frame_3, text="0?",variable=srcsetpt_cero_var, command=disable_widgets)
srcsetpt_cero_check.grid(row=0, column=1)

srcsetpt_entry = tk.Entry(check_sys_counts_frame_3)
srcsetpt_entry.grid(row=0, column=2)

#Dark Count
darkcount_label = tk.Label(check_sys_counts_frame_3, text="Dark count:")
darkcount_label.grid(row=0, column=5)

darkcount_entry = tk.Entry(check_sys_counts_frame_3)
darkcount_entry.grid(row=0, column=6)

#SHTR COUNT
shtr_label = tk.Label(check_sys_counts_frame_3, text="Shtr count:")
shtr_label.grid(row=2, column=0)

#shtr count-sc1
shtr_count_sc1_label = tk.Label(check_sys_counts_frame_3,text="sc1")
shtr_count_sc1_label.grid(row=2, column=1)

shtr_count_sc1_entry = tk.Entry(check_sys_counts_frame_3)
shtr_count_sc1_entry.grid(row=2, column=2)

#shtr count-sc2
shtr_count_sc2_label = tk.Label(check_sys_counts_frame_3,text="sc2")
shtr_count_sc2_label.grid(row=2, column=3)

shtr_count_sc2_entry = tk.Entry(check_sys_counts_frame_3)
shtr_count_sc2_entry.grid(row=2, column=4)

#shtr count-sc3
shtr_count_sc3_label = tk.Label(check_sys_counts_frame_3,text="sc3")
shtr_count_sc3_label.grid(row=2, column=5)

shtr_count_sc3_entry = tk.Entry(check_sys_counts_frame_3)
shtr_count_sc3_entry.grid(row=2, column=6)


#MEAS COUNT
meas_label = tk.Label(check_sys_counts_frame_3, text="Meas count:")
meas_label.grid(row=4, column=0)

#meas count-sc1
meas_sc1_label = tk.Label(check_sys_counts_frame_3,text="sc1")
meas_sc1_label.grid(row=4, column=1)

meas_sc1_entry = tk.Entry(check_sys_counts_frame_3)
meas_sc1_entry.grid(row=4, column=2)

#meas count-sc2
meas_sc2_label = tk.Label(check_sys_counts_frame_3,text="sc2")
meas_sc2_label.grid(row=4, column=3)

meas_sc2_entry = tk.Entry(check_sys_counts_frame_3)
meas_sc2_entry.grid(row=4, column=4)

#meas count-sc3
meas_sc3_label = tk.Label(check_sys_counts_frame_3,text="sc3")
meas_sc3_label.grid(row=4, column=5)

meas_sc3_entry = tk.Entry(check_sys_counts_frame_3)
meas_sc3_entry.grid(row=4, column=6)

#BS MEAS COUNT
bs_meas_label = tk.Label(check_sys_counts_frame_3, text="Bs meas count:")
bs_meas_label.grid(row=5, column=0)

#bs meas count-bsc1
bs_meas_bsc1_label = tk.Label(check_sys_counts_frame_3,text="bsc1")
bs_meas_bsc1_label.grid(row=5, column=1)

bs_meas_bsc1_entry = tk.Entry(check_sys_counts_frame_3)
bs_meas_bsc1_entry.grid(row=5, column=2)

#bs meas count-bsc2
bs_meas_bsc2_label = tk.Label(check_sys_counts_frame_3,text="bsc2")
bs_meas_bsc2_label.grid(row=5, column=3)

bs_meas_bsc2_entry = tk.Entry(check_sys_counts_frame_3)
bs_meas_bsc2_entry.grid(row=5, column=4)

#bs meas count-bsc3
bs_meas_bsc3_label = tk.Label(check_sys_counts_frame_3,text="bsc3")
bs_meas_bsc3_label.grid(row=5, column=5)

bs_meas_bsc3_entry = tk.Entry(check_sys_counts_frame_3)
bs_meas_bsc3_entry.grid(row=5, column=6)

#MEAS RATIO
meas_ratio_label = tk.Label(check_sys_counts_frame_3, text="Meas ratio:")
meas_ratio_label.grid(row=6, column=0)

#meas ratio-sc1
meas_ratio_sc1_label = tk.Label(check_sys_counts_frame_3,text="sc1")
meas_ratio_sc1_label.grid(row=6, column=1)

meas_ratio_sc1_entry = tk.Entry(check_sys_counts_frame_3)
meas_ratio_sc1_entry.grid(row=6, column=2)

#meas ratio-sc2
meas_ratio_sc2_label = tk.Label(check_sys_counts_frame_3,text="sc2")
meas_ratio_sc2_label.grid(row=6, column=3)

meas_ratio_sc2_entry = tk.Entry(check_sys_counts_frame_3)
meas_ratio_sc2_entry.grid(row=6, column=4)

#meas ratio-sc3
meas_ratio_sc3_label = tk.Label(check_sys_counts_frame_3,text="sc3")
meas_ratio_sc3_label.grid(row=6, column=5)

meas_ratio_sc3_entry = tk.Entry(check_sys_counts_frame_3)
meas_ratio_sc3_entry.grid(row=6, column=6)

#BS MEAS RATIO
bs_meas_ratio_label = tk.Label(check_sys_counts_frame_3, text="Bs meas ratio:")
bs_meas_ratio_label.grid(row=7, column=0)

#bs meas ratio-sc1
bs_meas_ratio_bsc1_label = tk.Label(check_sys_counts_frame_3,text="sc1")
bs_meas_ratio_bsc1_label.grid(row=7, column=1)

bs_meas_ratio_bsc1_entry = tk.Entry(check_sys_counts_frame_3)
bs_meas_ratio_bsc1_entry.grid(row=7, column=2)

#bs meas ratio-sc2
bs_meas_ratio_bsc2_label = tk.Label(check_sys_counts_frame_3,text="sc2")
bs_meas_ratio_bsc2_label.grid(row=7, column=3)

bs_meas_ratio_bsc2_entry = tk.Entry(check_sys_counts_frame_3)
bs_meas_ratio_bsc2_entry.grid(row=7, column=4)

#bs meas ratio-sc3
bs_meas_ratio_bsc3_label = tk.Label(check_sys_counts_frame_3,text="sc3")
bs_meas_ratio_bsc3_label.grid(row=7, column=5)

bs_meas_ratio_bsc3_entry = tk.Entry(check_sys_counts_frame_3)
bs_meas_ratio_bsc3_entry.grid(row=7, column=6)

##### CHEQUEO SYS STATUS FRAME -4- #####

check_sys_status_frame_4 = tk.LabelFrame(frame, text = "Chequeo Sys Status",labelanchor="n")
check_sys_status_frame_4.grid(row=3, column=0,sticky='WE')

#Major state. Si normal esta tildado, deshabilito desplegable 
major_state_label = tk.Label(check_sys_status_frame_4, text="Major State")
major_state_label.grid(row = 0, column = 0)

#major_state_check_var = tk.StringVar()
#major_state_checkbox = tk.Checkbutton(check_sys_status_frame_4, text="Normal", variable=major_state_check_var, command=disable_widgets)
#major_state_checkbox.grid(row=0, column=1)

     # Desplegable major state
major_state_options_var = tk.StringVar()
major_state_options = ["Normal","Syscal", "SpnCal", "ZroCal","ZroChk","SpnChk","LeaChk","ZroAdj"]
major_state_dropdown = tk.OptionMenu(check_sys_status_frame_4, major_state_options_var, *major_state_options)
major_state_dropdown.grid(row=0, column=1)

#Minor state. Si normal esta tildado, deshabilito desplegable 
minor_state_label = tk.Label(check_sys_status_frame_4, text="Minor State")
minor_state_label.grid(row = 1, column = 0)

#minor_state_check_var = tk.StringVar()
#minor_state_checkbox = tk.Checkbutton(check_sys_status_frame_4, text="Normal", variable=minor_state_check_var, command=disable_widgets)
#minor_state_checkbox.grid(row=1, column=1)

     # Desplegable minor state
minor_state_options_var = tk.StringVar()
minor_state_options = ["Normal", "ShtrDn", "ShtrMs", "ShtrUp"]
minor_state_dropdown = tk.OptionMenu(check_sys_status_frame_4, minor_state_options_var, *minor_state_options)
minor_state_dropdown.grid(row=1, column=1)

#Separador
separador = ttk.Separator(check_sys_status_frame_4, orient='vertical')
separador.place(relx=0.49, rely=0, relwidth=1, relheight=1,)

#Light Source
lightsource_label = tk.Label(check_sys_status_frame_4, text="Light Source:")
lightsource_label.grid(row = 2, column = 0)

radioValue_lightsource = tk.StringVar(value="")

radioOne_lightsource = tk.Radiobutton(check_sys_status_frame_4, text='Pass',variable=radioValue_lightsource, value="Pass") 
radioOne_lightsource.grid(row=2, column=1)
radioTwo_lightsource = tk.Radiobutton(check_sys_status_frame_4, text='Fail',variable=radioValue_lightsource, value="Fail") 
radioTwo_lightsource.grid(row=2, column=2)

#Environment Status
envirostatus_label = tk.Label(check_sys_status_frame_4, text="Environment Status:")
envirostatus_label.grid(row = 3,column=0)

radioValue_envirostatus = tk.StringVar()
radioOne_envirostatus = tk.Radiobutton(check_sys_status_frame_4, text='Pass',variable=radioValue_envirostatus, value="Pass") 
radioOne_envirostatus.grid(row=3, column=1)

radioTwo_envirostatus = tk.Radiobutton(check_sys_status_frame_4, text='Fail',variable=radioValue_envirostatus, value="Fail") 
radioTwo_envirostatus.grid(row=3, column=2)

#Shutter
shutter_label = tk.Label(check_sys_status_frame_4, text="Shutter:")
shutter_label.grid(row = 4, column = 0)

radioValue_shutter = tk.StringVar()
radioOne_shutter = tk.Radiobutton(check_sys_status_frame_4, text='Pass',variable=radioValue_shutter, value="Pass") 
radioOne_shutter.grid(row=4, column=1)

radioTwo_shutter = tk.Radiobutton(check_sys_status_frame_4, text='Fail',variable=radioValue_shutter, value="Fail") 
radioTwo_shutter.grid(row=4, column=2)

#PMT
pmt_label = tk.Label(check_sys_status_frame_4, text="PMT:")
pmt_label.grid(row = 0, column = 3,padx=60)

radioValue_pmt = tk.StringVar()
radioOne_pmt = tk.Radiobutton(check_sys_status_frame_4, text='Pass',variable=radioValue_pmt, value="Pass") 
radioOne_pmt.grid(row=0, column=4,padx=30)

radioTwo_pmt = tk.Radiobutton(check_sys_status_frame_4, text='Fail',variable=radioValue_pmt, value="Fail") 
radioTwo_pmt.grid(row=0, column=5,padx=0)

#RH
rh_label = tk.Label(check_sys_status_frame_4, text="RH:")
rh_label.grid(row = 1, column = 3,padx=60)

radioValue_rh = tk.StringVar()
radioOne_rh = tk.Radiobutton(check_sys_status_frame_4, text='Pass',variable=radioValue_rh, value="Pass") 
radioOne_rh.grid(row=1, column=4,padx=30)

radioTwo_rh = tk.Radiobutton(check_sys_status_frame_4, text='Fail',variable=radioValue_rh, value="Fail") 
radioTwo_rh.grid(row=1, column=5,padx=0)

#ST sensor
st_sensor_label = tk.Label(check_sys_status_frame_4, text="ST sensor:")
st_sensor_label.grid(row = 2, column = 3,padx=90)

radioValue_st_sensor = tk.StringVar()
radioOne_st_sensor = tk.Radiobutton(check_sys_status_frame_4, text='Pass',variable=radioValue_st_sensor, value="Pass") 
radioOne_st_sensor.grid(row=2, column=4,padx=15)

radioTwo_st_sensor = tk.Radiobutton(check_sys_status_frame_4, text='Fail',variable=radioValue_st_sensor, value="Fail") 
radioTwo_st_sensor.grid(row=2, column=5,padx=0)

#ET sensor
et_sensor_label = tk.Label(check_sys_status_frame_4, text="ET sensor:")
et_sensor_label.grid(row = 3, column = 3,padx=60)

radioValue_et_sensor = tk.StringVar()
radioOne_et_sensor = tk.Radiobutton(check_sys_status_frame_4, text='Pass',variable=radioValue_et_sensor, value="Pass") 
radioOne_et_sensor.grid(row=3, column=4,padx=25)

radioTwo_et_sensor = tk.Radiobutton(check_sys_status_frame_4, text='Fail',variable=radioValue_et_sensor, value="Fail") 
radioTwo_et_sensor.grid(row=3, column=5,padx=0)

#BP sensor
bp_sensor_label = tk.Label(check_sys_status_frame_4, text="BP sensor:")
bp_sensor_label.grid(row = 4, column = 3,padx=60)

radioValue_bp_sensor = tk.StringVar()
radioOne_bp_sensor = tk.Radiobutton(check_sys_status_frame_4, text='Pass',variable=radioValue_bp_sensor, value="Pass") 
radioOne_bp_sensor.grid(row=4, column=4,padx=30)

radioTwo_bp_sensor = tk.Radiobutton(check_sys_status_frame_4, text='Fail',variable=radioValue_bp_sensor, value="Fail") 
radioTwo_bp_sensor.grid(row=4, column=5,padx=0)

##### OBSERV Y GUARDADO FRAME -5- #####

observ_guardar_frame_5 = tk.LabelFrame(frame, text = "Salvar datos",labelanchor="n")
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
