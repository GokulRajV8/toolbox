#!/usr/bin/env python

import os, subprocess, json

### main area ###
if __name__ == "__main__" :
  # base directory of reports
  configFp = open("./config.json")
  config = json.load(configFp)
  configFp.close()
  baseDir = config["REPORTS_SRC_DIR"]
  os.chdir(baseDir)

  # getting info of all installed MSYS2 packages
  report = open("all-packages-info.txt", "w", encoding="utf-8")
  temp = subprocess.getoutput("pacman -Qi | grep -e \"Name\" -e \"Version\" -e \"Description\" -e \"Installed Size\"")
  # adding blank lines after each package and removing the same from the first package
  temp = temp.replace("Name", "\nName").replace("\nName", "Name", 1) + "\n"
  report.write(temp)
  report.close()

  # getting list of explicitly installed MSYS2 packages
  report = open("explicitly-installed-packages.txt", "w", encoding="utf-8")
  temp = subprocess.getoutput("pacman -Qqe")
  report.write(temp)
  report.close()
