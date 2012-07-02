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

# Quick sample generator. We are using Unix tools instead of raw /proc data
# for having a chance to work both on GNU/Linux and MacOSX.
# Some of commands below might require small change to work on your platform.

for i in `seq 1000`; do
  timestamp=`date +%s`
  load_avg_1min=`uptime | cut -d' ' -f 12`
  iostat_avg_1min=`iostat | tail -n 1 | cut -d' ' -f 17`
  vmstat_free=`vm_stat | grep "free" |  grep -o "[0-9]\+"`
  vmstat_faults=`vm_stat | grep "faults" |  grep -o "[0-9]\+"`
  echo "${timestamp} ${load_avg_1min}" >> "load-avg.sample"
  echo "${timestamp} ${iostat_avg_1min}" >> "iostat.sample"
  echo "${timestamp} ${vmstat_free}" >> "vmstat_free.sample"
  echo "${timestamp} ${vmstat_faults}" >> "vmstat_faults.sample"
  sleep 5
done
