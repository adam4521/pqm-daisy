import math
import time
import machine
import utime
import ustruct
import sys
from machine import Pin


# pin and SPI setup
led = machine.Pin(25, Pin.OUT)
boardled = machine.Pin(15, Pin.OUT)
cs_adc = machine.Pin(1, Pin.OUT)
#sck_adc = machine.Pin(2, Pin.OUT)
#sdo_adc = machine.Pin(0, Pin.IN)
#sdi_adc = machine.Pin(3, Pin.OUT)
reset_adc = machine.Pin(5, Pin.OUT)
dr_adc = machine.Pin(4, Pin.IN)


spi_adc = machine.SPI(0,
                  baudrate = 1000000,
                  polarity = 0,
                  phase = 0,
                  bits = 8,
                  firstbit = machine.SPI.MSB,
                  sck = machine.Pin(2),
                  mosi = machine.Pin(3),
                  miso = machine.Pin(0))

def write_text(spi, cs, text):
    message = bytearray()
    for c in text:
        message.append(ord(c))
    # send the message on the bus    
    cs.value(0)
    spi.write(message)
    cs.value(1)
    
def write_bytes(spi, cs, bs):
    # send the message on the bus    
    cs.value(0)
    spi.write(bs)
    cs.value(1)
        
def write_and_read_bytes(spi, cs, bs, n):
    cs.value(0)
    spi.write(bs)
    obs = spi.read(n)
    cs.value(1)
    return obs



# convert two's complement 24 bit binary to signed integer
def binary_to_signed_int(bs):
    if bs[0] & 1<<7 == True:    # negative number if most significant bit is set
        # flip all the bits and add 1 to answer
        for b in bs:
            b = ~b
        result = - (int.from_bytes(bs, 'big') + 1)
    else:
        result = int.from_bytes(bs, 'big')
    return result

def set_and_verify_adc_register(spi, cs, reg, bs):
    # The actual address byte leads with binary 01 and ends with the read/write bit (1 or 0).
    # The five bits in the middle are the 'register' address
    addr = 0x40 | (reg << 1)
    # for writing, make sure lowest bit is cleared
    write_bytes(spi, cs, bytes([(addr & 0b11111110)]) + bs)
    # for reading, make sure lowest bit is set
    obs = write_and_read_bytes(spi, cs, bytes([(addr | 0b00000001)]) + bs, len(bs))
    print("Verify: " + " ".join(hex(b) for b in obs))
    

def setup_adc(spi, cs):
    # Setup the MC3912 ADC
    # Set the gain configuration register 0x0b
    print("Setting gain register 0x0b to 0x00, 0x00, 0x00.")
    set_and_verify_adc_register(spi, cs, 0x0b, bytes([0x00,0x00,0x00]))
    time.sleep(1)
    
    # Set the status and communication register 0x0c
    print("Setting status and communication register 0x0c to 0x89, 0x00, 0x0f.")
    set_and_verify_adc_register(spi, cs, 0x0c, bytes([0x89,0x00,0x0f]))
    time.sleep(1)

    # Set the configuration register CONFIG0 at 0x0d
    print("Setting configuration register CONFIG0 at 0x0d to 0x5a, 0x38, 0x50.")
    set_and_verify_adc_register(spi, cs, 0x0d, bytes([0x5a,0x38,0x50]))
    time.sleep(1)

    # Set the configuration register CONFIG1 at 0x0e
    print("Setting configuration register CONFIG0 at 0x0e to 0x00, 0x00, 0x00.")
    set_and_verify_adc_register(spi, cs, 0x0e, bytes([0x00,0x00,0x00]))
    time.sleep(1)
    
def read_adc(spi, cs, ch):
    cs.value(0)
    if ch == 0:
        spi.write(bytes([0b01000001]))
    elif ch == 1:
        spi.write(bytes([0b01000011]))
    elif ch == 2:
        spi.write(bytes([0b01000101]))
    elif ch == 3:
        spi.write(bytes([0b01000111]))
    result = spi.read(3)
    cs.value(1)
    return result  # readings are in big-endian format

def read_adcs(spi, cs, dr):
        # sync to next sample by waiting until DR pin is low
        while dr.value() == 1:
            1   # (do nothing)
        # now read each ADC register
        ch = [0,0,0,0]
        raw = [0,0,0,0]
        signed_int = [0,0,0,0]
        for i in range(0,4):
            ch[i] = read_adc(spi, cs, i)
            raw[i] = int.from_bytes(ch[i], 'big')
            signed_int[i] = binary_to_signed_int(ch[i])
        return (raw, signed_int)
    

def main():
    # deselect the ADC
    cs_adc.value(1)

    # configure the ADC
    setup_adc(spi_adc, cs_adc)
    
    # Now repeatedly read from ADCs
    i = 0
    while True:
        r, s = read_adcs(spi_adc, cs_adc, dr_adc)
        # indicate and print every 1000 readings
        if i % 1000 == 0:
            boardled.toggle()
            print(f"Readings HEX:   {r[0]:06x}   {r[1]:06x}   {r[2]:06x}   {r[3]:06x}")
            print(f"Readings DEC: {s[0]:8d} {s[1]:8d} {s[2]:8d} {s[3]:8d}")
        i = i + 1
    

# run from here
if __name__ == '__main__':
    main()


