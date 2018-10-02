import numpy as np
import struct
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
import cv2


filename = '/home/gebhardt/Desktop/Peregrine_Test/test12018-09-29_13-06-47.ascar'

# Type     Size (bytes)
# uint8_t  1
# uint16_t 2
# uint32_t 4
# uint64_t 8

def parse_range_bin(rv):
    
    return  int(rv[:14],2) + int(rv[14:], 2) / 2.**(len(rv[14:]))
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
# block type uint32_t value = 2
# block size uint32_t value = 16
# frame count uint32_t the total number of frames
# Sequence mode uint32_t Value = 0
# Timestamp uint64_t Value = Timestamp

sequence_info = struct.unpack("IIIIQ", fileContent[64:88])

print(sequence_info)

# Next there is 280 Bytes of configuration data that is engineering information used for development purposes

# so we have 368 bytes of header information to start the file the rest of the data is the actual frame data measured from the lidar

num_frames = sequence_info[2]

size_frame = len(fileContent[368:])//num_frames


#Each pixel is a 32-bit integer so

num_cols = camera_info[-3] #128
num_rows = camera_info[-2] #32

size_frame_data = num_cols * num_rows * 4

frame_header_size = size_frame - size_frame_data

size_header = 368

size_frame_header = 28

size_frame_footer = 8

#print("The frame header is")
#print(frame_header_size)

#print("The size of a frame is")
#print(size_frame)


#print(len(fileContent[368:388]))


#16420 bytes for each frame 
# Block type uint32_t value = 3
# Block size uint32_t value = 16412
# Frame number uint32_t
# Timestamp  uint64_t 
# Segment type 1 uint32_t value = 2
# Segment Size 1 uint32_t RI size = 16384 = col * row * 4 = 128 * 32 * 4
# Segment 1 uint8_t[Ri_size]


frame_count = 0 


#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('lidar-test.avi',fourcc, 20.0, (128,32))
frame_range = np.zeros((32,128,num_frames))

for zz in range(num_frames):
    frame_intensity = np.zeros((32,128))
    
    vid_frame_intensity = np.zeros((32,128,3))
    pixel_count = 0
    for ii in range(num_rows):
        for jj in reversed(range(num_cols)):

            pixel = struct.unpack(">BBBB", fileContent[(396 + (pixel_count*4) + (frame_count*16420)):(400 + (pixel_count*4)+(frame_count*16420))])
            pixel_byte1 = format(pixel[0],'08b')
            pixel_byte2 = format(pixel[1],'08b')
            pixel_byte3 = format(pixel[2],'08b')
            pixel_byte4 = format(pixel[3],'08b')

            pixel_binary = pixel_byte1 + pixel_byte2 + pixel_byte3 + pixel_byte4
            intensity_value = int(pixel_binary[20:],2)
            range_value = parse_range_bin(pixel_binary[:20])
            frame_range[ii,jj,zz] = range_value
            frame_intensity[ii,jj] = intensity_value
            vid_frame_intensity[ii,jj,:] = (intensity_value/4096)*255
            pixel_count += 1
    
    #out.write(vid_frame_intensity.astype(np.uint8))
    
    #cv2.imwrite('frame{}.jpg'.format(frame_count), (frame_intensity/4096)*255)
    frame_count += 1

#out.release()
#print(frame_range.shape)
#plt.imshow(frame1_intensity)
#plt.show()

#print(frame_range[:,:,0])

tdlist = []
#current_frame = frame_range[0]
#for zz  in range(num_frames):
current_frame = frame_range[:,:,238]
tdlist = []
for ii in range(num_rows):
    for jj in range(num_cols):
        val = current_frame[ii,jj]
        tdlist.append([ii, jj, val])

w, h = matplotlib.figure.figaspect(1/4.)

tdlist = np.asarray(tdlist)

fig = plt.figure(figsize = (w,h))



ax = fig.add_subplot(111, projection='3d')


mapping = tdlist[:,2]
high_threshval = 50
low_threshval = 20
mapping[mapping > high_threshval] = high_threshval
mapping[mapping < low_threshval] = low_threshval
zmax = np.max(mapping)
zmin = np.min(mapping)
ax.set_zlim(zmin,zmax)
p = ax.scatter(tdlist[:,1], tdlist[:,0], mapping, c = mapping)

fig.colorbar(p)

#fix azimuth 270

for ii in range(240,300,1):
    ax.view_init(elev=250., azim=ii)
    plt.savefig("azimuth%d.png" % ii)

for ii in reversed(range(270,300,1)):
    ax.view_init(elev=250., azim=ii)
    plt.savefig("azimuthr%d.png" % ii)


for jj in range(220,270,1): 
    ax.view_init(elev=jj, azim=270.)
    plt.savefig("elev%d.png" % jj)

#plt.show()



'''
pixel1 = fileContent[396:400]

#print(format(pixel1[0],'08b'))
#print(format(pixel1[1],'08b'))
#print(format(pixel1[2],'08b'))
#print(format(pixel1[3],'08b'))

pixel1_byte1 = format(pixel1[0],'08b')
pixel1_byte2 = format(pixel1[1],'08b')
pixel1_byte3 = format(pixel1[2],'08b')
pixel1_byte4 = format(pixel1[3],'08b')

pixel1_binary = pixel1_byte1 + pixel1_byte2 + pixel1_byte3 + pixel1_byte4
print(pixel1_binary)
range_values = pixel1_binary[:20]
print(int(pixel1_binary[20:],2))

pixel1_range = parse_range_bin(range_values)

print(pixel1_range)
'''


'''
print(range_values[:14])
print(parse_frac(range_values[14:]))

fractional = range_values[14:]

print(parse_frac(fractional))
'''

'''
print(len(pixel1))
print(pixel1)
print(sys.byteorder)
print(len(pixel1))
pixel1_binary = bin(int.from_bytes(pixel1, byteorder = 'little'))
print(len(pixel1_binary))
'''
#pixel1_binary_intensity = pixel1_binary[:12]
#pixel1_range = pixel1_binary[12:]
#print(pixel1_binary_intensity)

#print(pixel1_range)

#print(int(pixel1_range, 2))
