#!/usr/bin/env python

from datetime import datetime
import subprocess, json

### returns divider string ###
def divider() -> str :
  return "----------------------------------------------------------------------------------"

### to get software version using command line ###
def getVersion(software: str) -> str :
  return subprocess.getoutput(software + " --version")

### main area ###
if __name__ == "__main__" :
  configFp = open("./config.json")
  config = json.load(configFp)
  configFp.close()
  softwareList = config["SOFTWARE_LIST"]

  # printing current timestamp
  print(f"Right now -> {datetime.now()}")
  print(divider())

  # getting version of the list of softwares
  for software in softwareList :
    print(getVersion(software))
    print(divider())
