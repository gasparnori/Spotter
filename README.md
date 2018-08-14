Spotter v2.0 : LED based real-time video tracking software (and hardware) system for behavioural experiments developed by Nora Gaspar

===============================

[Spotter version 2.0](https://github.com/gasparnori/spotterupdated) can track LEDs in real-time video stream--either from a webcam, or a video file--and simultaneously write encoded video to disk, while outputs the tracked variables as analog and digital signals. It is based on the [OpenCV](http://opencv.org/) library and interfaces with Arduino Mega


Spotter v1.0 developed by Ronny Eichler is available [here](https://github.com/wonkoderverstaendige)


For more detailed documentation, please refer to: [full documentation](docs/full_documentation_v1.1.pdf).

Requirements
------------

Tested on Windows 7

- Python 2.7 (Python 3.x is not supported)
- numpy 1.6+
- OpenCV 2.4+
- pyOpenGL
- pyQt4
- pySerial

- Arduino Mega

-recommended hardware: 4 digital to analog converters [MCP4921](http://ww1.microchip.com/downloads/en/devicedoc/21897b.pdf) , additional buffering and filtering circuitry

**Windows**

*Python installation:*

Download and install Python 2.7
Add python to the PATH variable by appending the lines below under MyComputer->Properties->Advanced->Env Variables->Path

    ;C:\Python27\;C:\Python27\Scripts

*Installing packages:*
    
Install required packages by downlaoding and innstalling following binaries through pip or through the links below:
numpy, scipy, matplotlib, pyopengl, pyserial

    http://www.lfd.uci.edu/~gohlke/pythonlibs/#pip
    http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
    http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyopengl
    http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyserial

*OpenCV*

Install OpenCV 2.4+ with prebuilt libraries, and follow the relevant [installation steps](https://docs.opencv.org/2.4/doc/tutorials/introduction/windows_install/windows_install.html)
	Go to opencv/build/python/2.7/x86 or x64 folder.
	Copy cv2.pyd to C:/Python27/lib/site-packages.

*PyQt4*

Download prebuilt PyQt4 (PyQt4-4.10-gpl-Py2.7-Qt4.8.4-x32.exe or x64 respectively) from [here](https://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.10/)

*Video Codec*

Download and install XVID codec from [here](https://www.xvid.com/download/)

**MaxOSX**

*Install XCode*
*install MacPorts.*
	
	sudo port -v selfupdate

cp /usr/local/opt/opencv@2/lib/python2.7/site-packages/cv2.so /usr/local/lib/python2.7/site-packages/

*Install py27- packages.*

	sudo port install py27-opengl
	sudo port install py27-numpy
	sudo port install py27-scipy
	sudo port install py27-serial
	sudo port install opencv +python27
	sudo port install py27-pyqt4


**LINUX**

    apt-get install the following packages:

    python-numpy
    python-scipy
    python-qt4-gl
    python-serial
    python-opencv
    python-matplotlib
    python-opengl

Installation
------------

**With git**

    git clone https://github.com/gasparnori/spotterupdated.git

**Without git**

Download and extract the zip file

**Starting the program**

On Windows run the Spotter.bat file. This will update the newest version, convert the UI and run the software itself.

Hardware and Arduino
--------------------

If you are using an Arduino Mega for analog output, update the newest arduino file. Each time you use the system, make sure that the right port is connected, and that the Arduino software is up-to-date.
	
	/arduino/Spotter_MC_v2.0

The custom PCB files and the schematics are available in the /arduino/hardware folders.


Compiling GUI (for developers)
-------------

**Windows**

_Run the following file:_

	/lib/ui/build_windows.bat

**Linux**

_Download and install PyQt4 development tools_

	sudo apt-get install pyqt4-dev-tools qt4-designer
	
_Run the build_linux.sh file_

	chmod +x lib/ui/build_linux.sh
	cd lib/ui
	./build_linux.sh



<br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>
