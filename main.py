import os

import PySimpleGUI as sg
import numpy as np

from classes import airfoils as af
from classes import  liveplots as lp
import serial.tools.list_ports_windows
import time
import threading
import datetime
import random

# COM Ports
port_dict = {}
port_list = []
data_acquisition_started = False
ms_offset = 0

def read_com_port():
    while arduino.is_open:
        global ms_offset
        global data_acquisition_started

        try:
            # window.write_event_value('Event', datetime.datetime.now().strftime("%H:%M:%S"))

            arduino.write(bytes("g",  'utf-8'))
            time.sleep(0.1)
            data = arduino.readline().decode('ascii')

            if data != '' and (data[0:2] == 'P1'):

                # make sure we are reading a full message
                if not data_acquisition_started:

                    ms_offset = time.time()*1000.0
                    data_acquisition_started = True

                raw_ports_array = data.split(",")
                pressures = []
                ms = time.time()*1000.0

                for i in range(len(raw_ports_array)):

                    pressures.append(raw_ports_array[i].split(":")[1])
                liveplot.add_point(ms-ms_offset, pressures)
                window["-ATM_PORT-"].update(pressures[0])
                window["-RAM_PORT-"].update(pressures[1])
                window["-P1_PRESS-"].update(pressures[2])
                window["-P2_PRESS-"].update(pressures[3])

                den = float(window["-AIR_DENSITY-"].get())
                v_inf = round(np.sqrt(2*100*(float(pressures[1]) - float(pressures[0]))/den),1)
                visc = float(window["-VISC_INPUT-"].get())
                c = float(window["-CHORD_INPUT-"].get())
                window["-AIR_SPEED-"].update(v_inf)
                window["-RE_NUM-"].update(round(den*v_inf*c/visc))

        except:
            print("No COM Ports Available :(")
            data_acquisition_started = False
        # time.sleep(0.25)
def find_com_ports():
    ports_available = serial.tools.list_ports_windows.comports()

    for port, desc, hwid in sorted(ports_available):
        port_dict[port] = (port, desc, hwid)
        port_list.append(port + " - " + desc)
        # print (port, desc, hwid)
        # print("{}: {} [{}]".format(port, desc, hwid))

find_com_ports()
sg.theme("Dark Blue")



# GUI Constants
title_card_size = 17

# Zones
first_column =  [

    [sg.Text("COM Selection", justification="left", font=('Arial Bold', title_card_size, "underline"))],
    [sg.DropDown(list(port_list), size=(55,4), enable_events=True, key='-COMLIST-')],


    [sg.Text("Model Info", justification="left", font=('Arial Bold', title_card_size, "underline"))],
    [sg.Text("Chord             ", justification="left", font=('Arial', 15)),
        sg.Input('75', enable_events=True, key='-CHORD_INPUT-',s=10, font=('Arial', 15), justification='right'),
        sg.Text("[mm]", justification="left", font=('Arial', 15))],
    [sg.Text("AoA                ", justification="left", font=('Arial', 15), tooltip="Angle of Attack in degrees"),
        sg.Input('5', enable_events=True, key='-AOA_INPUT-',s=10, font=('Arial', 15), justification='right'),
        sg.Text("[deg]", justification="left", font=('Arial', 15))],
    [sg.Text("Fluid Viscosity ", justification="left", font=('Arial', 15), tooltip="Units of Pascal Seconds"),
        sg.Input('1.81', enable_events=True, key='-VISC_INPUT-',s=10, font=('Arial', 15), justification='right'),
        sg.Text("[Pa*s]", justification="left", font=('Arial', 15))],
    [sg.Text("Air Density      ", justification="left", font=('Arial', 15), tooltip="Air Density in kilograms per meters cubed"),
        sg.Input('1.1', enable_events=True, key='-AIR_DENSITY-',s=10, font=('Arial', 15), justification='right'),
        sg.Text("[kg/m3]", justification="left", font=('Arial', 15))],


    [sg.Text("Load Airfoil", justification="left", font=('Arial Bold', title_card_size, "underline"))],
    [sg.Canvas(key='-AIRFOIL_PLOT-', size=(200,150))],
    [sg.Text("Choose Airfoil"),
        sg.InputText(key="-AIRFOIL_FILE-"), sg.FileBrowse(button_text="Browse", initial_folder=os.getcwd(), file_types=[("txt Files", "*.txt")], target="-AIRFOIL_FILE-"),
         sg.Button(button_text="Load Airfoil", key="-LOAD_AIRFOIL-")]
]



port_management = [
    [sg.Text("Port Management", justification="left", font=('Arial Bold', title_card_size, "underline"))],
    [sg.Checkbox(text="Atm. Port",key="-AP_CB-", font=('Arial', 14),enable_events=True,default=True ),
    sg.Input('     0.00', enable_events=False,s=10, font=('Arial', 14), justification='right',key="-ATM_PORT-"),
        sg.Text("kPa", font=('Arial', 14))],


    [sg.Checkbox(text="Ram Port",key="-RP_CB-", font=('Arial', 14),enable_events=True,default=True),
        sg.Input('     0.00', enable_events=False,s=10, font=('Arial', 14), justification='right',key="-RAM_PORT-"),
        sg.Text("kPa", font=('Arial', 14))],


    [sg.Checkbox(text="Port 1      ",key="-P1_CB-", font=('Arial', 14),enable_events=True,default=True),
        sg.Input('     0.00', enable_events=False,s=10, font=('Arial', 14), justification='right',key="-P1_PRESS-"),
        sg.Text("kPa", font=('Arial', 14))
     ],


    [sg.Checkbox(text="Port 2      ",key="-P2_CB-", font=('Arial', 14),enable_events=True,default=True),
        sg.Input('     0.00', enable_events=False,s=10, font=('Arial', 14), justification='right',key="-P2_PRESS-"),
         sg.Text("kPa", font=('Arial', 14))
     ],


    [sg.Checkbox(text="Port 3",key="-P3_CB-", font=('Arial', 14),enable_events=True,default=True), ],
    [sg.Checkbox(text="Port 4",key="-P4_CB-", font=('Arial', 14),enable_events=True,default=True), ],
    [sg.Checkbox(text="Port 5",key="-P5_CB-", font=('Arial', 14),enable_events=True,default=True), ],
    [sg.Checkbox(text="Port 6",key="-P6_CB-", font=('Arial', 14),enable_events=True,default=True), ],
    [sg.Checkbox(text="Port 7",key="-P7_CB-", font=('Arial', 14),enable_events=True,default=True), ],
    [sg.Checkbox(text="Port 8",key="-P8_CB-", font=('Arial', 14),enable_events=True,default=True), ],
    [sg.Checkbox(text="Port 9",key="-P9_CB-", font=('Arial', 14),enable_events=True,default=True), ],
    [sg.Checkbox(text="Port 10",key="-P10_CB-", font=('Arial', 14),enable_events=True,default=True),],
    [sg.Checkbox(text="Port 11",key="-P11_CB-", font=('Arial', 14),enable_events=True,default=True), ],
    [sg.Checkbox(text="Port 12",key="-P12_CB-", font=('Arial', 14),enable_events=True,default=True), ],
    [sg.Checkbox(text="Port 13",key="-P13_CB-", font=('Arial', 14),enable_events=True,default=True), ],
    [sg.Checkbox(text="Port 14",key="-P14_CB-", font=('Arial', 14),enable_events=True,default=True),],
    [sg.Checkbox(text="Port 15",key="-P15_CB-", font=('Arial', 14),enable_events=True,default=True), ],
    [sg.Checkbox(text="Port 16",key="-P16_CB-", font=('Arial', 14),enable_events=True,default=True), ],
]

live_plot = [
    [sg.Canvas(key='-LIVE_PLOT-', size=(800,400))],
    [sg.B(button_text="Record", key="-RECORD_DATA-", button_color='red')],
    [sg.Text("Results", justification="left", font=('Arial Bold', title_card_size, "underline"))],

    [sg.T(text="Air Speed               ", font=('Arial', 14)),
        sg.Input(0.0, key="-AIR_SPEED-", font=('Arial', 14), enable_events=False,
                  justification="right", size=(10, 1)),
        sg.Text("m/s", font=('Arial', 14))
     ],

    [sg.T(text="Reynold's Number ", font=('Arial', 14)),
        sg.Input(0.0, key="-RE_NUM-", font=('Arial', 14), enable_events=False,
                  justification="right", size=(10, 1)),
         sg.Text("-", font=('Arial', 14))
     ],


]


layouts = [
    [
        sg.Column(first_column),
        sg.VSeparator(),
        sg.Column(port_management),
        sg.Column(live_plot)
    ],
]


window = sg.Window('Aero Dashboard - SE Projects', layouts,
                   icon = r'media/selogo.ico',
                   resizable = True).finalize()
# window.Maximize()

# Draw Airfoil
airfoil = af.airfoils(window['-AIRFOIL_PLOT-'].TKCanvas)
airfoil.draw_figure()

# Live Data Plot
liveplot = lp.liveplots(100,window['-LIVE_PLOT-'].TKCanvas)

# Initialize the COMs port
arduino = serial.Serial(baudrate=460800, timeout=.5)
com_port_available = False

def main_loop():
    while True:

        event, values = window.read()

        # Window Close
        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        # # Run Always
        # find_com_ports()

        # Load new airfoil profile
        if (event == "-LOAD_AIRFOIL-") and (values["-AIRFOIL_FILE-"] != ""):
            airfoil.load_airfoil(values["-AIRFOIL_FILE-"], window['-CHORD_INPUT-'].get())
            airfoil.draw_figure()


        # Choosing a COM port
        if event == "-COMLIST-" :
            # print(values["-COMLIST-"])
            com_picked = values["-COMLIST-"][0:4]
            # print(com_picked)
            arduino.close()
            if com_picked != arduino.port:
                arduino.port = com_picked
                if not arduino.is_open:
                    try:
                        arduino.open()
                        threading.Thread(target=read_com_port).start()

                    except:
                        print("Could not connect to ", com_picked)

        # if arduino.port != "" :
        #     try:
        #         print(arduino.read(32))
        #     except:
        #         continue

        if event == 'Event':
            continue

    window.close()
    try:
        arduino.close()
    except:
        print("No COM port to close")





main_loop()

# main_loop_thread = threading.Thread(main_loop(), None)
# com_thread = threading.Thread(read_com_port(), None)
#
#
# main_loop_thread.start()
# com_thread.start()
# sg.popup('You Entered', values['-IN-'])
