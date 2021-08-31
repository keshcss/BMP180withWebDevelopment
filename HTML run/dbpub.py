#import sqlite3
import bmp_subscribe

###TO REMEMBER FOR DATABASE####
'''
    #Create Connection and Cursor
    conn = sqlite3.connect('base.db')
    c = conn.cursor()

    ###execute action#######
    
    #Commit and Close
    print("Welcome Soldier.")
    conn.commit()
    conn.close()
'''
while True:
    print(bmp_subscribe.temp_add())
