#!/bin/sh

# This file is part of OpenGossip.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser
# General Public License for more details.  You should have received a copy
# of the GNU Lesser General Public License along with this program.  If not,
# see <http://www.gnu.org/licenses/>.

if [ $# -ne 2 ]; then
  echo "Usage: `basename $0` DAT_FOLDER OUTPUT_FOLDER"
  exit 1
fi

DAT_FOLDER="$1"
PNG_FOLDER="$2"
GNUPLOT=`which gnuplot`

if [ "$GNUPLOT" == "" ]; then
  echo "Gnuplot not found. Check your \$PATH"
  exit 2
fi

if [ ! -d $DAT_FOLDER ]; then
  echo "Input folder ${DAT_FOLDER} does not exist"
  exit 2
fi

if [ ! -d $PNG_FOLDER ]; then
  echo "Output folder ${PNG_FOLDER} does not exist"
  exit 2
fi

# Some series stand in just one column, then we display the resulting curve
# showing evolution of values.
# If there are 2 columns, we currently consider that we are ploting (x,y)
# datapoints (even if `x` is a timestamp)

for file in $DAT_FOLDER/*.dat; do
    echo "Processing ${file}"
    spaces=`echo $(tail -n 1 $file) | grep -c ' '`
    filename=`basename ${file} .dat`
    if [[ $spaces -eq 0 ]]; then
	$GNUPLOT <<EOF
set term png size 800,480
set output "$PNG_FOLDER/${filename}.png"
set pointsize 0.1
plot "${file}" w linespoints linecolor rgb "#336699" title "${filename}"
EOF
    fi
    if [[ $spaces -eq 1 ]]; then
    $GNUPLOT <<EOF
set term png size 800,480
set output "$PNG_FOLDER/${filename}.png"
set pointsize 2
plot "${file}" using 2:1 title "${filename}"
EOF
    fi
done
