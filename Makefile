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


clean:
	rm -f src/python/analyzer/*.{pyc,pyo}
	rm -f results/*.png
	rm -f features/*.dat

build:
	python src/python

build-gnuplot:
	sh src/gnuplot/generate-graphics.sh features results

test:
	python src/python/analyzer/tests/ringbuffer_test.py
	python src/python/analyzer/tests/numericringbuffer_test.py
	python src/python/analyzer/tests/superlist_test.py
