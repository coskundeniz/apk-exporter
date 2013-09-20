Apk Exporter
============

A graphical tool for exporting apk using Ant

Information
-----------

Apk Exporter exports a .apk file for Android projects using Ant. It was written
with Python and Tkinter was used for graphical interface.

Settings
--------

* On Windows, you should add Ant to path
* On Linux, Ant should be installed
* A keystore should be created to sign apk
* When you first checkout the project, you should run the initial_ant_tasks.py
script to make Ant generate build.xml file and set default target to release

Usage
-----

1. Select project directory
2. If you want, you can change version code and name
3. When you click _Export Apk_, a signed apk is exported as default option
4. If you check _Unsigned Release_ an unsigned apk is exported
