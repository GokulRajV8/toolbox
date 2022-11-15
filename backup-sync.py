#!/usr/bin/env python

# Simple script to sync destination folder with source folder based on file name existence and modified time
# Note that renaming a file will not affect modified time and hence this script will not work if the folders have files that change names with each other

import os, shutil, json

# setting slash as per OS
__slash = "/"
if os.name == "nt" :
  __slash = "\\"

### to sync source and destination folders ###
def syncFolders(srcDir: str, dstDir: str) -> None :
  # getting the list of files
  srcList = os.listdir(srcDir)
  dstList = os.listdir(dstDir)

  # flag to record any changes done
  flag = False

  for file in srcList :
    # creating files in destination directory if not present
    if not(file in dstList) :
      flag = True
      print(f"Copying {file} from {srcDir} to {dstDir}")
      shutil.copy(srcDir + __slash + file, dstDir)
    # updating files in destination directory if older than file in source directory
    elif (os.path.getmtime(srcDir + __slash + file) > os.path.getmtime(dstDir + __slash + file)) :
      flag = True
      print(f"Updating {file} in {dstDir}")
      shutil.copy(srcDir + __slash + file, dstDir)

  for file in dstList :
    # deleting files in destination that are no longer present in source directory
    if not(file in srcList) :
      flag = True
      print(f"Deleting {file} in {dstDir}")
      os.remove(dstDir + __slash + file)

  if not(flag) :
    print(f"{srcDir} and {dstDir} were already in sync")

### main area ###
if __name__ == "__main__" :
  configFp = open("./config.json")
  config = json.load(configFp)
  configFp.close()
  # syncing reports backup folder
  syncFolders(config["REPORTS_SRC_DIR"], config["REPORTS_DST_DIR"])
