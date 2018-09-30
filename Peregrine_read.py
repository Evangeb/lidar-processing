import numpy as np
import struct

filename = '/home/evan/Desktop/Peregrine_Test/test12018-09-29_13-06-47.ascar'




#test22018-09-29_13-09-14.ascar

with open(filename, mode='rb') as file:
    fileContent = file.read()


# 12 bytes for format version
# block type uint32_t value = 0
# block size uint32_t value = 4
# Verseion   uint32_t value = 2
version = struct.unpack("III", fileContent[:12])

print(version)

# 52 bytes for camera info
# block type uint32_t value = 1
# block size uint32_t value = 44
# Camera name uint8_t[32] string that identifies camera type
# Columns uint32_t Width Resolution
# Rows uint32_t Height Resolution
# Max samples uint32_t Number of samples per pixel used for Raw data. 
#print(len(fileContent[12:64]))
#print("II" + "c" * 32 + "III")
camera_info = struct.unpack("II" + "B" * 32 + "III", fileContent[12:64])

print(camera_info)

#24 bytes for sequence info

sequence_info = struct.unpack("IIIIQ", fileContent[64:88])

print(sequence_info)
print(len(fileContent))
#280 configuration bytes
print(len(fileContent[368:388]))
frame0 = struct.unpack("I",fileContent[392:396])

print(frame0)
