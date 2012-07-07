OpenGossip
==========

Tools for metrics analysis and fault detection. It's currently experimental only. Have a look at the [wiki]
(https://github.com/adrien-mogenet/opengossip/wiki) for current work's output.


## Introduction
There are sevenral kind of metrics that you would want to track:
  * Metrics that should always be evolving and never be constant
  * Metrics that are highly related to each other
  * Metrics that should be perfectly predictable

Of course, putting this or that metric into this or that model depends on your platform and 
programs that are running on it. OpenGossip has been designed as a toolbox that you might customize to fit your
own needs.


## Current results

Here is the graphic representing a load average (based on 1 last minute) :
![load-average](https://dl.dropbox.com/u/720826/opengossip/load-avg-1min/original-serie.png)

And now, how to automatically detect spikes ? Using classification algorithms mentionned above (here a
[hierarchical clustering](http://en.wikipedia.org/wiki/Hierarchical_clustering) technic) OpenGossip is able to 
detect abrupt changes, strange behaviors or related events.
![anomalies](https://dl.dropbox.com/u/720826/opengossip/load-avg-1min/anomalies.png)