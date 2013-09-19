#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET

class ApkExporter(object):
	
    def __init__(self):
        self.dirname = None
        self.package = None
        self.version_code = None
        self.version_name = None
        self.xml_tree = None
        self.unsigned = False

        ET.register_namespace("android", "http://schemas.android.com/apk/res/android")

    def parse_manifest_file(self):
        self.xml_tree = ET.parse(os.path.join(self.dirname, 'AndroidManifest.xml'))
        # get the root(manifest element)
        root = self.xml_tree.getroot()

        return root
		
    def extract_info(self):
        """ extract package name, version code and name """

        root = self.parse_manifest_file()
        self.package = root.attrib['package']
        self.version_code = root.attrib['{http://schemas.android.com/apk/res/android}versionCode']
        self.version_name = root.attrib['{http://schemas.android.com/apk/res/android}versionName']	
		
    def change_version_code(self, root):
        root.set('{http://schemas.android.com/apk/res/android}versionCode', 
                self.version_code)
		
    def change_version_name(self, root):
        root.set('{http://schemas.android.com/apk/res/android}versionName', 
                self.version_name)
			
    def get_root(self):
        return self.xml_tree.getroot()

    def write_changes(self):
        """ write changes to AndroidManifest.xml file """
        self.xml_tree.write(os.path.join(self.dirname, 'AndroidManifest.xml'), 
                            encoding="utf-8", xml_declaration=True)
		
    def handle_build_properties(self):
        """ remove build(ant).properties property from build.xml """

        build_xml_tree = ET.parse(os.path.join(self.dirname, 'build.xml'))
        build_root = build_xml_tree.getroot()

        # find element to be removed
        removed_element = build_root.find("property[@file='ant.properties']")

        if(removed_element is not None):
            # remove element from xml file
            build_root.remove(removed_element)
            build_xml_tree.write(os.path.join(self.dirname, 'build.xml'), 
                                 encoding="utf-8", xml_declaration=True)			
			
    def export_apk(self):
		
        if(self.unsigned):		
            self.handle_build_properties()
        else:	
            build_xml_tree = ET.parse(os.path.join(self.dirname, 'build.xml'))
            build_root = build_xml_tree.getroot()
            found = build_root.find("property[@file='ant.properties']")
            if(found == None):
                elem = ET.Element('property', attrib={"file": "ant.properties"})
                build_root.insert(0, elem)
                build_xml_tree.write(os.path.join(self.dirname, 'build.xml'))
			
        # execute 'ant release' command
        os.chdir(self.dirname)
        os.system("ant release")


if __name__ == '__main__':
	app = ApkExporter()
