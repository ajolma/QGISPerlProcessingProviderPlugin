# QGISPerlProcessingProviderPlugin
A QGIS plugin to add perl programs as processors in the processing toolbox

# How to describe the API of the perl program to the plugin

The program should be usable from the command line like this:

`perl -w program.pl arguments`

The program should be in directory `$HOME/.qgis3/processing/perlscripts`.

The arguments are described in the program in the order they are used
in the command line using specific comments:

```
# QP4: <key1>: <data1>
# QP4: <key2>: <data2>
...
```

Keys and respective data are:

key | data
----|-----
Name | Name of the processor (shown in the toolbox and dialog)
Group | Group in the toolbox
Input | <klass>,<name>,<description>
Output | <klass>,<name>,<description>

klass may be (these are supported by the processing toolbox, all are
not yet supported in this plugin):

Boolean, CRS, DataObject, Extent, Point, File, FixedTable,
MultipleInput, Number, Range, Raster, Selection, String, Expression,
Table, TableField, Vector

name is the name of the parameter. It should be a single word. It is
used when processors are linked together.

description is used on the dialog.
