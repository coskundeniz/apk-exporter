#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from Tkinter import *
from tkFileDialog import askdirectory
from apk_exporter import ApkExporter


class ApkExporterGui(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")

        self.parent = parent

        self.dirname = None
        self.info = StringVar()
        self.package_name_var = StringVar()
        self.version_code_var = StringVar()
        self.version_name_var = StringVar()
        self.version_code_entry = StringVar()
        self.version_code_entry.set("")
        self.version_name_entry = StringVar()
        self.version_name_entry.set("")
        self.selected_unsigned = IntVar()

        self.init_ui()

        self.app = ApkExporter()
		
    def init_ui(self):
        """ initialize gui """
        self.parent.title("Apk Exporter")
        self.pack(fill=BOTH, expand=1)

        # place widgets
        self.place_browse_button()

        self.place_package_name_lbl()
        self.place_version_code_lbl()
        self.place_version_name_lbl()

        self.place_package_name_var()
        self.place_version_code_var()
        self.place_version_name_var()

        self.place_version_code_entry()
        self.place_version_name_entry()

        self.place_sign_checkbox()
        self.place_export_button()
        self.place_exit_button()

        self.place_info()

        # add horizontal line
        frame = Frame(self, relief=RAISED, bd=1)
        frame.grid(row=6, columnspan=3, sticky=W+E)

    def place_browse_button(self):
        browse_button = Button(self,
                               text="BROWSE PROJECT DIRECTORY",
                               command=self.ask_directory)
        browse_button.grid(row=0, columnspan=3, padx=120, pady=10)

    def place_package_name_lbl(self):
        package_name_lbl = Label(self,
                                 text="Package Name: ",
                                 bg="white")
        package_name_lbl.grid(row=1, column=0, pady=5, padx=25, ipady=5, sticky=E)

    def place_version_code_lbl(self):
        version_code_lbl = Label(self,
                                 text="Version Code: ",
                                 bg="white")
        version_code_lbl.grid(row=2, column=0, pady=5, padx=25, ipady=5, sticky=E)

    def place_version_name_lbl(self):
        version_name_lbl = Label(self,
                                 text="Version Name: ",
                                 bg="white")
        version_name_lbl.grid(row=3, column=0, pady=5, padx=25, ipady=5, sticky=E)

    def place_package_name_var(self):
        package_name_var = Label(self,
                                 textvariable=self.package_name_var,
                                 bg="white")
        package_name_var.grid(row=1, column=1, pady=5, sticky=W)

    def place_version_code_var(self):
        version_code_var = Label(self,
                                 textvariable=self.version_code_var,
                                 bg="white")
        version_code_var.grid(row=2, column=1, pady=5, sticky=W)

    def place_version_name_var(self):
        version_name_var = Label(self,
                                 textvariable=self.version_name_var,
                                 bg="white")
        version_name_var.grid(row=3, column=1, pady=5, sticky=W)

    def place_version_code_entry(self):
        version_code_entry = Entry(self,
                                   textvariable=self.version_code_entry,
                                   bg="white",
                                   justify=CENTER)
        version_code_entry.grid(row=2, column=2, pady=5, sticky=W)

    def place_version_name_entry(self):
        version_code_entry = Entry(self,
                                    textvariable=self.version_name_entry,
                                    bg="white",
                                    justify=CENTER)
        version_code_entry.grid(row=3, column=2, pady=5, sticky=W)

    def place_sign_checkbox(self):
        sign_checkbox = Checkbutton(self,
                                    text="Unsigned Release",
                                    variable=self.selected_unsigned,
                                    bg="white")
        sign_checkbox.grid(row=4, columnspan=2, padx=25, pady=5, sticky=W)

    def place_export_button(self):
        self.export_button = Button(self,
                                    text="Export Apk",
                                    command=self.export_apk)
        self.export_button.grid(row=5, column=1, pady=20, sticky=E)

    def place_exit_button(self):
        exit_button = Button(self,
                             text="Exit",
                             width=9,
                             command=self.parent.quit)
        exit_button.grid(row=5, column=2, pady=20)

    def place_info(self):
        info = Label(self,
                     textvariable=self.info,
                     bg="white")
        info.grid(row=7, columnspan=3, padx=15, pady=5, sticky=W)

    def ask_directory(self):
        if(os.name == "nt"):
            self.dirname = askdirectory(initialdir='C:\\',
                                        title='Select Project Directory')
        elif(os.name == "mac"):
            self.dirname = askdirectory(initialdir='/Users/%s' % os.getlogin(),
                                        title='Select Project Directory')
        else:
            self.dirname = askdirectory(initialdir='/home/%s' % os.environ['USER'],
                                        title='Select Project Directory')
        self.app.dirname = self.dirname

        #extract package name, version code and name
        self.app.extract_info()

        self.info.set("Extracted manifest info")

        # update screen
        self.package_name_var.set(self.app.package)
        self.version_code_var.set(self.app.version_code)
        self.version_name_var.set(self.app.version_name)

    def export_apk(self):

        # get version changes
        if(self.version_code_entry != ""):
            self.app.version_code = self.version_code_entry.get()
            self.app.change_version_code(self.app.get_root())

        if(self.version_name_entry != ""):
            self.app.version_name = self.version_name_entry.get()
            self.app.change_version_name(self.app.get_root())

        if(self.version_code_entry.get() == "" and
            self.version_name_entry.get() == ""):
            pass
        else:
            self.app.write_changes()

        # handle signing changes and export apk
        self.app.unsigned = self.selected_unsigned.get()
        self.app.export_apk()
        self.info.set("Finished exporting apk")


def run():
    root = Tk()

    width = 450
    height = 300

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - width) / 2
    y = (screen_height - height) / 2

    root.geometry("%dx%d+%d+%d" %(width, height, x, y))
    root.resizable(width=FALSE, height=FALSE)

    app = ApkExporterGui(root)
    root.mainloop()


if __name__ == '__main__':
    run()
