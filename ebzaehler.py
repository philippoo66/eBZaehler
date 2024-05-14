'''
   Copyright 2024 philippoo66
   
   Licensed under the GNU GENERAL PUBLIC LICENSE, Version 3 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.gnu.org/licenses/gpl-3.0.html

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

import serial
import time
import datetime
import sys
import os
import importlib
import threading

import settings_ini

logbuffer = []
recent_file = ""


def write_log():
    global logbuffer
    global recent_file
    with open(os.path.join(settings_ini.csv_path, recent_file), 'a') as file:
        for itm in logbuffer:
            file.write(itm + '\n')
        file.flush()  # Datei sofort aktualisieren
    logbuffer = []
    recent_file = get_filename()


def get_filename():
    now = datetime.datetime.now()
    return f"{now.year:04d}_{now.month:02d}_{now.day:02d}.csv"


def get_value(dp:str, data:str):
    value = None 
    #start_index = data.find("1-0:16.7.0*255(")
    fstr = dp + "*255("
    # Finde den Index des Anfangs des Werts
    start_index = data.find(fstr)
    if start_index != -1:
        start_index += len(fstr)
        # Finde den Index des Endes des Werts
        end_index = data.find("*", start_index)
        if end_index != -1:
            value = data[start_index:end_index]
            #print("Wert zu " + dp, value)
        else:
            value = "end not found" 
            #print(value, dp)
    else:
        value = "start not found" 
        #print(value, dp)
    return value


# Hauptfunktion
def main():
    global logbuffer
    global recent_file

    mod_mqtt = None
    ser = None
    eot_time = 0.1  # sec

    # init some things
    recent_file = get_filename()
    lasthour = datetime.datetime.now().hour

    try:
        if(len(sys.argv) > 1):
            port = sys.argv[1]
        else:
            port = settings_ini.serial_port

        # Serielle Port-Einstellungen, öffnet auch den Port
        #ser = serial.Serial(port, 9600, 7, "E", timeout=0)
        ser = serial.Serial(port=port,
                    baudrate=9600,
                    parity=serial.PARITY_EVEN,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.SEVENBITS,
                    #exclusive=True,
                    timeout=0)
        
        if(settings_ini.mqtt is not None):
            # avoid paho.mqtt required if not used
            mod_mqtt = importlib.import_module("mqtt_util")
            mod_mqtt.connect_mqtt()
            # MQTT publishing may take some longer so we use a queue
            mqtt_thread = threading.Thread(target=mod_mqtt.publish_loop)
            mqtt_thread.daemon = True  # Setze den Thread als Hintergrundthread - wichtig für Ctrl-C
            mqtt_thread.start()


        data_buffer = b''
        last_receive_time = time.time()

        while True:
            # Zeichen vom Serial Port lesen
            incoming_data = ser.read_all()

            if incoming_data:
                # Daten zum Datenpuffer hinzufügen
                data_buffer += incoming_data
                last_receive_time = time.time()
                #print(data_buffer) #.hex())
            elif ((time.time() - last_receive_time) > eot_time) and data_buffer:
                # Wenn 0,x Sekunde vergangen ist und der Datenpuffer nicht leer ist,
                # Bytes in String umwandeln
                data_str = data_buffer.decode("utf-8")
                data_buffer = b''
                #data_str = data_str.replace('\r\n', ';')
                p_sum = get_value("16.7.0", data_str)
                p_L1 = get_value("36.7.0", data_str)
                p_L2 = get_value("56.7.0", data_str)
                p_L3 = get_value("76.7.0", data_str)
                now = datetime.datetime.now()
                dt = "{0:02d}:{1:02d}:{2:02d}".format(now.hour, now.minute, now.second)
                log_str = f"{dt};{p_L1};{p_L2};{p_L3};{p_sum}"

                print(log_str)

                if(settings_ini.mqtt is not None):
                    mod_mqtt.add2queue("Sum", float(p_sum))
                    mod_mqtt.add2queue("L1", float(p_L1))
                    mod_mqtt.add2queue("L2", float(p_L2))
                    mod_mqtt.add2queue("L3", float(p_L3))

                if(settings_ini.write_csv):
                    currhour = now.hour
                    newday = (currhour < lasthour)
                    lasthour = currhour

                    if(newday or (len(logbuffer) >= settings_ini.buffer_to_write)):  # 30 min
                        write_log()
                    logbuffer.append(log_str)

            time.sleep(0.01)

    except Exception as e:
        print(e)
    finally:
        write_log()
        # Serial Port schliessen
        if (ser is not None):
            if ser.is_open:
                ser.close()
        if(mod_mqtt is not None):
            mod_mqtt.exit_mqtt()


if __name__ == "__main__":
    main()
