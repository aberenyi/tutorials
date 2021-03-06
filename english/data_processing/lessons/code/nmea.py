""" Simple NMEA processing to create a text file with coordinates
"""

import sys
import os
import re

def checksum(buf):
    """ check nmea checksum on line """
    cs = ord(buf[1])
    for ch in buf[2:-3]:
        cs ^= ord(ch)
    return cs

def nmea2deg(nmea):
    """ convert nmea angle (dddmm.ss) to degree """
    w = nmea.rstrip('0').split('.')
    return int(w[0][:-2]) + int(w[0][-2:]) / 60.0 + int(w[1]) / 3600.0
    
fin = 'nmea1.txt'
if len(sys.argv) > 1:
    fin = sys.argv[1]   # get input file from command line
fi = open(fin, 'r') # input file
fo = open(os.path.splitext(fin)[0] + '.out', 'w') # output file
for line in fi:
    line = line.strip()
    if hex(checksum(line))[2:].upper() != line[-2:]:
        print("Chechsum error: " + line)
        continue
    if re.match('\$..GGA', line):
        gga = line.split(',')
        if gga[6] == '1':  # use only fix
            lat = nmea2deg(gga[2])
            if gga[3].upper() == 'S':
                lat *= -1
            lon = nmea2deg(gga[4])
            if gga[5].upper() == 'W':
                lon = 360 - lon
            height = float(gga[9])
            fo.write('{:.6f},{:.6f},{:.2f}\n'.format(lat, lon, height))
fo.close()
fi.close()
