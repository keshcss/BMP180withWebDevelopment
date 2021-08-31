from datetime import datetime
import paho.mqtt.client as mqtt
import time
import sqlite3

gReadStr = "Devices"
gTemperatureStr = "Are"
gPressureStr = "Not"
gLightStr = "ON"

gLightInt = "Int"
gTempInt = "Int2"
gPressInt = "Int3"
#Define
def add_c1(list):

    #Create Connection and Cursor
    conn = sqlite3.connect('chart1str.db')
    c = conn.cursor()

    #Add Many Records Line
    c.executemany("INSERT INTO c1 VALUES (?,?,?)",list)
    
    #Commit and Close
    conn.commit()
    conn.close()
    
def add_data(list):
    
    #Create Connection and Cursor
    conn = sqlite3.connect('bmppub.db')
    c = conn.cursor()

    #Add Many Records Line
    c.executemany("INSERT INTO storage VALUES (?,?,?,?,?)",list)
    
    #Commit and Close
    conn.commit()
    conn.close()
    
def on_read_message(client, userdata, message):
    global gReadStr
    gReadStr = str(message.payload.decode("utf-8"))
    print(gReadStr)

def read_val():
    client.subscribe("Reading")
    client.on_message = on_read_message

def on_temperature_message(client, userdata, message):
    global gTemperatureStr
    gTemperatureStr = str(message.payload.decode("utf-8"))
    print(gTemperatureStr)
     
def temp_data():
    tempClient.subscribe("Temperature")
    tempClient.on_message = on_temperature_message

def on_pressure_message(client, userdata, message):
    global gPressureStr
    gPressureStr = str(message.payload.decode("utf-8"))
    print(gPressureStr)
    
def press_data():
    pressClient.subscribe("Pressure")
    pressClient.on_message = on_pressure_message

def on_light_message(client, userdata, message):
    global gLightStr
    gLightStr = str(message.payload.decode("utf-8"))
    print (gLightStr)

def light_data():
    lightClient.subscribe("LightInten")
    lightClient.on_message = on_light_message

def on_light_int(client, userdata, message):
    global gLightInt
    gLightInt = str(message.payload.decode("utf-8"))
    print (gLightInt)

def light_int():
    lightIntClient.subscribe("LightINT")
    lightIntClient.on_message = on_light_int

def on_temp_int(client, userdata, message):
    global gTempInt
    gTempInt = str(message.payload.decode("utf-8"))
    print (gTempInt)

def temp_int():
    tempIntClient.subscribe("TemperatureINT")
    tempIntClient.on_message = on_temp_int

def on_press_int(client, userdata, message):
    global gPressInt
    gPressInt = str(message.payload.decode("utf-8"))
    print (gPressInt)

def press_int():
    pressIntClient.subscribe("PressureINT")
    pressIntClient.on_message = on_press_int
    
def test():
    a = "Yes it works"
    return a

def on_msg(client, userdata, message):
    print(str(message.payload.decode("utf-8")))
    
def space():
    client.subscribe("newl")
    client.on_msg = on_msg

def show_all():

    #Create Connection and Cursor
    conn = sqlite3.connect('bmppub.db')
    c = conn.cursor()
    
    #execute from finding name(querry)
    c.execute("SELECT rowid, * FROM storage ")
    items = c.fetchall()
    for item in items :
        print(item)
        
    #Commit and Close
    print("Plants4Life!.")
    conn.commit()
    conn.close()


#MQTT Setup
mqttBroker = "192.168.1.151"
client = mqtt.Client("PC")
client.connect(mqttBroker)
tempClient = mqtt.Client("PC1")
tempClient.connect(mqttBroker)
pressClient = mqtt.Client("PC2")
pressClient.connect(mqttBroker)
lightClient = mqtt.Client("PC3")
lightClient.connect(mqttBroker)

lightIntClient = mqtt.Client("PC4")
lightIntClient.connect(mqttBroker)
tempIntClient = mqtt.Client("PC5")
tempIntClient.connect(mqttBroker)
pressIntClient = mqtt.Client("PC6")
pressIntClient.connect(mqttBroker)

action = str(input("Please Enter Action: "))
print("")
if (action == "show"):

    lightIntClient.loop_start()
    tempIntClient.loop_start()
    pressIntClient.loop_start()
    
    light_int()
    temp_int()
    press_int()
    for i in range(1,2):
        print("not: " + gTempInt)
        print("not:  " + gPressInt)
        print("not:  " + gLightInt)
        time.sleep(2.5)
    while True:
        print("into db2: " + gTempInt)
        print("into db3: " + gPressInt)
        print("into db4: " + gLightInt)
        print("")
        time.sleep(2.5)

        #movetoc1 = [(gTempInt,gPressInt,gLightInt)]
        #add_c1(movetoc1)
        #time.sleep(2.5)
        
elif (action == "run"):

    client.loop_start()
    tempClient.loop_start()
    pressClient.loop_start()
    lightClient.loop_start()
    
    read_val()
    temp_data()
    press_data()
    light_data()
    for i in range(1,2):
        print("not: " + gReadStr)
        print("not: " + gTemperatureStr)
        print("not:  " + gPressureStr)
        print("not:  " + gLightStr)
        time.sleep(2.5)
    while True:
        gTime = str(datetime.today())
        print("into db1: " + gReadStr)
        print("into db2: " + gTemperatureStr)
        print("into db3: " + gPressureStr)
        print("into db4: " + gLightStr)
        print("into db5: " + gTime)
        print("")
        
        movetostorage = [(gReadStr,gTemperatureStr,gPressureStr,gLightStr,gTime)]
        add_data(movetostorage)
        time.sleep(2.5)
    
elif (action == "testlight"):
    lightClient.loop_start()
    light_data()
    
elif (action == "manual"):
    
    read1 = str(input("Enter: "))
    temp1 = str(input("Enter: "))
    press1 = str(input("Enter: "))
    movetostorage = [(read1,temp1,press1)]
    add_data(movetostorage)
        
elif (action == "count"):
    n = 1
    while True:
        print(test() + " x" + str(n))
        n = n + 1
        time.sleep(2.5)

elif (action == "timestamp"):
    print(gTime)
    
elif (action == "run10") :
    client.loop_start()
    tempClient.loop_start()
    pressClient.loop_start()
    lightClient.loop_start()
    
    read_val()
    temp_data()
    press_data()
    light_data()
    for i in range(1,2):
        print("not: " + gReadStr)
        print("not: " + gTemperatureStr)
        print("not:  " + gPressureStr)
        print("not:  " + gLightStr)
        time.sleep(2.5)
    for i in range(1,11):
        gTime = str(datetime.today())
        print("into db1: " + gReadStr)
        print("into db2: " + gTemperatureStr)
        print("into db3: " + gPressureStr)
        print("into db4: " + gLightStr)
        print("into db5: " + gTime)
        
        movetostorage = [(gReadStr,gTemperatureStr,gPressureStr,gLightStr,gTime)]
        add_data(movetostorage)
        time.sleep(2.5)

    
    client.loop_stop()
    tempClient.loop_stop()
    pressClient.loop_stop()
    lightClient.loop_stop()

else:
    while True:
        client.loop_start()
        tempClient.loop_start()
        pressClient.loop_start()
        lightClient.loop_start()
        
        read_val()
        temp_data()
        press_data()
        light_data()
        
            
            
    
