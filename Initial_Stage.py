#Initiate setup using while-loop
import serial
from serial.tools import list_ports
import time

# Commands to synchronize LPC40xx
Set_Up_Instructions= {"Init_Com":b"?","Host_Response":b"Synchronized\r\n",
                      "Send_Crystal_Freq":b"12000\r\n"}

# Work on after
# # ISP_Return_Code={"0":"CMD_SUCCESS","1":"Invalid_COMMAND"}
# # LPC_Response= {"DEVICE_SYNC":b"Synchronized\r\n","DEVICE_ACK":b"Synchronized\rOK\r\n"",
                      # "DEVICE_RESPONSE_TO_CRYSTAL_FREQ":b"12000\r\n"}

# Device Responses
DEVICE_SYNCHRONIZE_RESPONSE=b"Synchronized\r\n"
DEVICE_ACKNOLEDGE_SYNC=b"Synchronized\rOK\r\n"
DEVICE_RESPONSE_TO_CRYSTAL_FREQ=b"12000\rOK\r\n"

init_complete=False
fail_initiate=False

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

# variable assigned ISP return code from LPC40XX
ISP_Return_Code=""

try:
        ser.open()

        # Condition to check port properly opened
        if ser.isOpen():
                print("Open")
        else:
                print("NO")

        # Condition is satisfied, virtually press DTR & RTS
        if(ser.rts is False and ser.dtr is False):
                ser.dtr=True
                ser.rts=True

                # Flushing out the input buffer that has
                # data remaining when LPC40XX was initially turned on
                while(buffer_full):
                        ser.flushInput()
                        buffer= ser.read(500)
                        if buffer is b"":
                                buffer_full=False
                        else:
                                buffer_full=True

        print(buffer)

        # Conditioned satisfied that both DTR & RTS pressed
        # release DTR
        if(ser.rts and ser.dtr):
                ser.dtr=False
        else:   
                print("Need to toggle dtr")

        # Here we begin to send set-up commands
        ser.write(Set_Up_Instructions["Init_Com"])
        device_response=ser.read(50)                                                    # Read the data/response
        print("Response:{}".format(device_response))                    # display data retrieved from input buffer

        while not init_complete and not fail_initiate:
                # Serial response checked
                if device_response==DEVICE_SYNCHRONIZE_RESPONSE:
                                ser.write(Set_Up_Instructions["Host_Response"])
                                device_response=ser.read(50)    # Read input buffer again
                                                                # for serial response
                                print("Response:{}".format(device_response))
                # LPC40XX Response to acknowledge that Host acknowledge
                elif device_response==DEVICE_ACKNOLEDGE_SYNC:
                                ser.write(Set_Up_Instructions["Send_Crystal_Freq"])
                                device_response=ser.read(50)
                                print("Response:{}".format(device_response))
                # LPC40XX RESPONSE to acknowledge the Crystal Frequency was set
                elif device_response==DEVICE_RESPONSE_TO_CRYSTAL_FREQ:
                                init_complete=True                              #After device ACK crystal Freq then initiation is done
                                print("Initiation Complete")
                else:
                                fail_initiate=True
                                print("Failed Set-Up")

        if init_complete:
                # Turn OFF Echo (Default: ON)
                ser.write(b"A 0\r\n")
                ISP_Return_Code=ser.read(50)
                print(ISP_Return_Code)

                # Fetch Part Identification Number
                ser.write(b"J\r\n")
                ser.flushInput()
                ISP_Return_Code=ser.read(50)
                print(ISP_Return_Code)
                                
                # Fetch Device Serial Number
                ser.write(b"N\r\n")
                ISP_Return_Code=ser.read(50)
                print(ISP_Return_Code)

        # Closing Port
        ser.close()
        print("close from try...")

except Exception as e:
        print(e)
else:
    # Using Else with Try-Except will Close port
    # I believe it is used correctly here
    ser.close()
    print("Closed..")
