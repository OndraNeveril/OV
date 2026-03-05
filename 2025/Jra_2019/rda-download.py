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
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796947/796947.tmp-pres-an-ll125.jra3q.anl_p125.0_0_0.tmp-pres-an-ll125.2019060100_2019063018.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796947/796947.tmp-pres-an-ll125.jra3q.anl_p125.0_0_0.tmp-pres-an-ll125.2019070100_2019073118.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796947/796947.tmp-pres-an-ll125.jra3q.anl_p125.0_0_0.tmp-pres-an-ll125.2019080100_2019083118.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796947/796947.tmp-pres-an-ll125.jra3q.anl_p125.0_0_0.tmp-pres-an-ll125.2019090100_2019093018.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796947/796947.ugrd-pres-an-ll125.jra3q.anl_p125.0_2_2.ugrd-pres-an-ll125.2019060100_2019063018.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796947/796947.ugrd-pres-an-ll125.jra3q.anl_p125.0_2_2.ugrd-pres-an-ll125.2019070100_2019073118.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796947/796947.ugrd-pres-an-ll125.jra3q.anl_p125.0_2_2.ugrd-pres-an-ll125.2019080100_2019083118.nc',
  'https://request.rda.ucar.edu/dsrqst/RAMATHEERTHAN796947/796947.ugrd-pres-an-ll125.jra3q.anl_p125.0_2_2.ugrd-pres-an-ll125.2019090100_2019093018.nc'
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
