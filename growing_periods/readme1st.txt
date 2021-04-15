Global AEZ CDrom Image files
============================

The downloadable zip files *.zip comprise all the plates from the
Global AEZ Cdrom in a 1 or 2 byte binary image format.
The images can be imported into any GIS software 
(e.g. Arc/Info,Idrisi,Erdas,etc.).

For each image a header file *.hdr, a world file *.blw and a
*.doc file is given. The former two are required to import the
*.bil images into Arc/Info via the "imagegrid" command. 
The *.doc file is required to import into IDRISI, then the 
*.bil files should be renamed to *.img.
Some of the *.doc files are also required by Arc/Info users
to identify the legend of an image.

Furthermore, for each plate tow *.bmp files are available, 
one for the image (plate*.bmp) and one for the legend (lgd*.bmp).
They can be viewed in any graphics software (e.g. Microsoft Paint,
CorelDraw, etc. on the PC or XV,ghostview....under Unix). 

All images:
*) cover the whole globe
*) are in geographic projection, i.e. in longitude, latitude
*) the corner point of the lower left corner is at:
   -180 x-coord and -90 y-coord.
*) use the INTEL byte order
*) store integers

There are four different image sizes:

1) 
cell size: 0.5 degree
360 rows, 720 columns
1 byte integer
*.bil file = 259200 bytes

2)
cell size: 0.5 degree
360 rows, 720 columns
2 byte integer
*.bil file = 518400 bytes

3)
cell size: 5 minutes
2160 rows, 4320 columns
1 byte integer
*.bil file = 9331200 bytes

4)
cell size: 5 minutes
2160 rows, 4320 columns
2 byte integer
Size of *.bil file is 18662400 bytes


Remarks for Yields
==================
Whenever yields are shown in a plate, the values are given in
the image area 1/10ths of kg/ha. The legends consider this
already. Thus a value 500 in the image means 5000 kg/ha.

Remarks for Arc/Info users:
==========================
Negative values in the images (such as -9999 for nodata) are 
imported into Arc/Info as positve values by adding 65536.
For example in plate01, the value 55537 should be changed to 
-9999 for nodata (55537 - 65536 = -9999). The "setnull" command
may be used to introduce nodata.
In plate58a and plate58b also negative values occur beside the
nodata value. The commands to import e.g. plate58a are listed below:

Grid: arc imagegrid plate58a.bil tmp_plate58a
Grid: pl58a = con (tmp_plate58a > 10000, tmp_plate58a - 65536, tmp_plate58a)
Grid: kill tmp_plate58a
 



