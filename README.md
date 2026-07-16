# This script will be a wrapper to interface with packet tracer & write ExApps faster. 
# It is built on top of CPT test script "ptmp-negot-textenc.py", Source: https://github.com/bfranske/pt-python-examples by Ben Franske.


To turn an XML & Python script into a .pta to be used by packet tracer you need to have the following:
an XML file:   ptmp-test.xml
a python file: ptmp-negot-textenc.py

To encrypt call the "meta" executable in the command line from this directory. It cannot be called in the program files bin where it is actually located.

Command:
"C:\Program Files\Cisco Packet Tracer 9.0.0\bin\meta.exe" ptmp-test.pta ptmp-test.xml -i ptmp-negot-textenc.py

trace:
[meta] <encrypted-filename> <original-file> -i <integrity-file>

the integrity file is essentially the source of the app you want packet tracer to run
this can be an .exe, a .py file, whatever.

SOURCE: https://github.com/bfranske/pt-python-examples