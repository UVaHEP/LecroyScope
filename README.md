# LecroyScope
Tools for working with our lecroy scope 

# Data file processing

LecroyBinProcessor2.py produces a root tree from scope data files

Enter up to 4 channels of data from the scope.  Nominal connections are
Chan 1: trigger, Chan 2: sipm1, Chan3, sipm2, chan4, MCP

Choosing zero suppression requires 

> usage: LecroyBinProcessor2.py [-h] [-n NMAX] [-z] [-o [OUTPUT]]
>                               [files [files ...]]
>
> Lecroy Data Processor
>
> positional arguments:
>   files                 Give file paths or a [filename].list to specify
>                         channel data files.
>
> optional arguments:
>   -h, --help            show this help message and exit
>   -n NMAX, --nmax NMAX  Maximum number of events to process
>   -z, --useZSP          use zero suppression to require signal
>   -o [OUTPUT], --output [OUTPUT]
                        Output root file

* plotting example

run: python testplotter.py

> Lecroy Data Test Plotter
>
> positional arguments:
>   files                 Give a filename or use default [lecroy.root]
>
> optional arguments:
>   -h, --help            show this help message and exit
>   -n EVENTNUMBER, --eventnumber EVENTNUMBER
>                         Event numebr to graph
