# Importing modules
import spidev # To communicate with SPI devices
from time import sleep  # To add delay
# Start SPI connection
spi = spidev.SpiDev() # Created an object
spi.open(0,0) 
# Read MCP3008 data
def analogInput(channel):
  spi.max_speed_hz = 1350000
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

while True:
  temp_output = analogInput(0) # Reading from CH0
  print(temp_output)
  sleep(1)