





#Initial Stage

import serial
from serial.tools import list_ports
import time

# Send "?" to initiate synchronize communication
SEND_SYNCRONIZE = b"?"

# Commands to synchronize LPC40xx
DEVICE_SYNCHRONIZE_RESPONSE=b"Synchronized\r\n"
HOST_RESPONSE=b"Synchronized\r\n"

DEVICE_ACKNOLEDGE_SYNC=b"Synchronized\rOK\r\n"
SEND_CRYSTAL_FREQUENCY=b"12000\r\n"

DEVICE_RESPONSE_TO_CRYSTAL_FREQ=b"12000\rOK\r\n"

# Data communication baud-rate
baudrate=38400

"""Set Up Serial"""
ser= serial.Serial()
ser.baudrate=baudrate
ser.port='/dev/ttyS3'
ser.rts=False
ser.dtr=False
ser.timeout=5

#Boolean used in loop to clear buffer
buffer_full=True

try:
        ser.open()

        # Condition to check port properly opened
        if ser.isOpen():
                print("Open")
        else:
                print("NO")

        # Condition is satisfied virtually press DTR & RTS
        if(ser.rts is False and ser.dtr is False):
                ser.dtr=True
                ser.rts=True

                # Flushing out the input buffer that has
                # data remaining
                while(buffer_full):
                        ser.flushInput()
                        buffer= ser.read(500)
                        print(buffer)
                        if buffer is b"":
                                buffer_full=False
                        else:
                                buffer_full=True

        # Conditioned satisfied that both DTR & RTS pressed
        # release DTR
        if(ser.rts and ser.dtr):
                ser.dtr=False
        else:   
                print("Need to toggle dtr")


        # Send "?" to LPC40xx to begin syncronization
        ser.write(SEND_SYNCRONIZE)
        serial_response=ser.read(50) # Read the data/response
        print(serial_response)       # display data retrieved from input buffer

        # Serial response checked
        if serial_response==DEVICE_SYNCHRONIZE_RESPONSE:
                ser.write(HOST_RESPONSE)
                serial_response=ser.read(50) # Read input buffer again
                                             # for serial response
        else:
                print("No response")
        
        print(serial_response)

        # Serial Response to acknoledge that Host acknoledge
        # WHY IS THE LPC40xx RESPONSE NOT JUST b"OK<CR><LF>",
        # INSTEAD IT IS b"SYNCRONIZED<CR>OK<CR><LF>
        if serial_response==DEVICE_ACKNOLEDGE_SYNC:
                ser.write(SEND_CRYSTAL_FREQUENCY)
                serial_response=ser.read(50)

        else:
                print("NACK Crystal")

        print(serial_response)

        # SAME THING HERE, LPC40XX RESPONDED WITH b"12000<CR>OK<CR><LF>,
        # INSTEAD OF b"OK<CR><LF>
        if serial_response==DEVICE_RESPONSE_TO_CRYSTAL_FREQ:
                print("Init. Complete")
        else:
                print("Failed Init.")
                
        # Closing Port
        ser.close()

except Exception as e:
        #Fix this to capture error messages
        print(e.message)
else:
    # Using Else with Try-Except will Close port
    # I believe it is used correctly here
    ser.close()


