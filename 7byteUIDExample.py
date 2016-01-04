#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

def getcardUID(uid7):
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        #print "Card detected"
    
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        
        sak=[0]
        MIFAREReader.MFRC522_SelectTag(uid,sak)

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK and ((sak[0] & 0x04) == 0x00):
            #print "CLASSIC"
            #print "Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])
            uid7[0] = uid[0]
            uid7[1] = uid[1]
            uid7[2] = uid[2]
            uid7[3] = uid[3]
            return 1
        
        else:
            #print "ULTRA"
            uid7[0]= uid[1]
            uid7[1]= uid[2]
            uid7[2]= uid[3]
            (status,uid2) = MIFAREReader.MFRC522_Anticoll2()

            if status == MIFAREReader.MI_OK:
                #print "EXITO"
                uid7[3]= uid2[0]
                uid7[4]= uid2[1]
                uid7[5]= uid2[2]
                uid7[6]= uid2[3]

                #print ' '.join([hex(i) for i in uid7])
                return 1
                #sak[0]= 0
                #MIFAREReader.MFRC522_SelectTag2(uid2,sak)

    return 0

cardUID= [0,0,0,0,0,0,0]

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    if getcardUID(cardUID):
        h = "".join(["%02x" % i for i in cardUID])
        print h
    
                

