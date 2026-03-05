#!/usr/bin/env python
""" 
Python script to download selected files from rda.ucar.edu.
After you save the file, don't forget to make it executable
i.e. - "chmod 755 <name_of_script>"
"""
import sys, os
from urllib.request import build_opener

opener = build_opener()

filelist = [
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796946/796946.tmp-pres-an-ll125.jra3q.anl_p125.0_0_0.tmp-pres-an-ll125.2002080100_2002083118.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796946/796946.tmp-pres-an-ll125.jra3q.anl_p125.0_0_0.tmp-pres-an-ll125.2002090100_2002093018.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796946/796946.tmp-pres-an-ll125.jra3q.anl_p125.0_0_0.tmp-pres-an-ll125.2002100100_2002103118.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796946/796946.tmp-pres-an-ll125.jra3q.anl_p125.0_0_0.tmp-pres-an-ll125.2002110100_2002113018.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796946/796946.ugrd-pres-an-ll125.jra3q.anl_p125.0_2_2.ugrd-pres-an-ll125.2002080100_2002083118.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796946/796946.ugrd-pres-an-ll125.jra3q.anl_p125.0_2_2.ugrd-pres-an-ll125.2002090100_2002093018.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796946/796946.ugrd-pres-an-ll125.jra3q.anl_p125.0_2_2.ugrd-pres-an-ll125.2002100100_2002103118.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796946/796946.ugrd-pres-an-ll125.jra3q.anl_p125.0_2_2.ugrd-pres-an-ll125.2002110100_2002113018.nc'
]

for file in filelist:
    ofile = os.path.basename(file)
    sys.stdout.write("downloading " + ofile + " ... ")
    sys.stdout.flush()
    infile = opener.open(file)
    outfile = open(ofile, "wb")
    outfile.write(infile.read())
    outfile.close()
    sys.stdout.write("done\n")
