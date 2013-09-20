#! python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET

def initial_ant_tasks():
		
    dirname = raw_input("Enter project directory: ")

    os.chdir(dirname)
    os.system("android update project -p .")
		
    build_xml_tree = ET.parse(os.path.join(dirname, 'build.xml'))
    build_root = build_xml_tree.getroot()
		
    build_root.set('default', 'release')
    build_xml_tree.write(os.path.join(dirname, 'build.xml'),
                         encoding="utf-8", xml_declaration=True)
		
if __name__ == '__main__':
    initial_ant_tasks()
