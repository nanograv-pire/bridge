# TOA_Filtering.py
# A script that takes in a .tim file, start time and end time, and an output directory
# as a result, it creates a new file with TOAs in the time range, stored in output directory
# sample input:
# python TOA_Filtering.py /Users/fkeri/Desktop/B1855+09_NANOGrav_9yv0.tim 51000 56000 /Users/fkeri/Desktop/
# we can see that it takes in 4 line arguments: [INPUT FILE], [TIME START], [TIME END], [OUTPUT DIRECTORY]
# [TIME START] and [TIME END] formats: MJD or YYYY/MM/DD
# the output file will have the same name as the input file, with "TOArange_" as a prefix: "TOArange_B1855+09_NANOGrav_9yv0.tim"
# it is possible to name the output file differently by putting the file name in [OUTPUT DIRECTORY]: /Users/fkeri/Desktop/filename.tim

import sys
import math
import datetime
import jdcal
import glob
import os.path

def date2mjd(year, month, day):
    """
    function that converts date in YYYY/MM/DD to MJD
    """
    jd = sum(jdcal.gcal2jd(year, month, day))
    mjd = jd -2400000.5
    return mjd

def isFloat( X ):
	try:
		float( X )
		return True
	except ValueError:
		return False

def transform( X ):
	X = str( X )
	A = [ "", "", "", "", "" ]
	ch = 0
	cnt = 0
	for i in range( len( X ) ):
		ch = X[i]
		if not ( ord( ch ) > 44 and ord( ch ) < 58 ):
			return "not ok"
		if ch == "-" or ch == "/":
			cnt += 1
		else:
			A[ cnt ] += ch
	if cnt == 2:
		if int( A[1] ) > 12 or int( A[2] ) > 31:
			return "not ok"
		return date2mjd( int( A[0] ), int( A[1] ), int( A[2] ) )
	return float( X )

inFile = open( sys.argv[1], "r" )

save_path = sys.argv[4]
if save_path[-4] != '.':
    nameFile = os.path.join( save_path, "TOArange_"+sys.argv[1].split("/")[-1] )
else:
    nameFile = save_path
outFile = open( nameFile, "w" )

inFile.readline() #omit first line
ALLlines = inFile.readlines()

start = str( sys.argv[2] )
end = str( sys.argv[3] )
start = transform( start )
end = transform( end )

if ( start == "not ok" ) or ( end == "not ok" ):
	outFile.write( "Wrong format! Please enter the data again! (either MJD or YYYY/MM/DD format)" )
else:
	if ( start < 0 ) or ( end < 0 ):
		outFile.write( "Your starting and ending points cannot be less than zero! Please enter the data again! (either MJD or YYYY/MM/DD format)" )
	else:
		if ( start > end ):
			outFile.write( "Your starting point cannot be greater than your ending point! Please enter the data again! (either MJD or YYYY/MM/DD format)" )
		else:
			L = []
			for i in range( 0, len( ALLlines ) ):
			    L.append( ALLlines[i].split(' ') )
			#L.sort(key = lamda row: row[2] )

			for i in range( 0, len( ALLlines ) ):
				if ( len( L[i] ) > 2 ):
					if isFloat( L[i][2] ):
						TOA = float( L[i][2] )
						if(TOA >= start and TOA <= end ):
							X = ' '.join( L[i] )
							outFile.write( X )

inFile.close()
outFile.close()
