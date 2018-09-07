#!/bin/bash
# file destination usr/lib/cups/filter

echo -en "\033%-12345X"
echo -en "@PJL JOB\015\012"
echo -en "@PJL SET USERNAME = \"mwen\"\015\012"
echo -en "@PJL SET KMSECTIONKEY2 = \"090916\"\015\012"
echo -en "@PJL SET KMCOETYPE = 0\015\012"
echo -en "@PJL SET KMSECTIONNAME = \"\"\015\012"
echo -en "@PJL SET BOXNUM = 76\015\012"
echo -en "@PJL SET KMDRIVER = ON\015\012"
echo -en "@PJL SET BOXHOLD = STORE\015\012"
echo -en "@PJL SET BOXHOLDTYPE = PUBLIC\015\012"
echo -en "@PJL ENTER LANGUAGE = POSTSCRIPT\015\012"
echo -en "@PJL SET MEDIASOURCE = AUTO\015\012"
cat -
echo -en "\004\033%-12345X\015\012@PJL EOJ\015\012"
echo -en "\033%-12345X"
