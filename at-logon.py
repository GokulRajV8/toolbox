#!/usr/bin/env python

from io import TextIOWrapper
import os, shutil, datetime

### global constants ###
DAY = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTH = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

### convert current time to string ###
def nowToString() -> str :
  rightNow = datetime.datetime.now()
  return DAY[rightNow.weekday()] + " " + MONTH[rightNow.month - 1] + " " + f"{rightNow.day:02}" + ", " + f"{rightNow.year:04}" + " " \
    + f"{rightNow.hour:02}" + ":" + f"{rightNow.minute:02}" + ":" + f"{rightNow.second:02}" + " - "

### move files of a particular filetype from source to destination ###
def moveFiles(source: str, destination: str, fileTypes: list, logFile: TextIOWrapper) -> None :
  for file in os.listdir(source) :
    for fileType in fileTypes :
      if(file.endswith("." + fileType)) :
        logFile.write(nowToString() + "Moving " + source + file + " to " + destination + "\n")
        shutil.move(source + file, destination)

### main area ###
if __name__ == "__main__" :
  # base directory of user
  baseDir = "C:/Users/" + os.getenv("USERNAME")

  # opening log file to write
  logFile = open("logs/at-logon.log", "a", encoding="utf-8")
  logFile.write("\n")

  # logged in user details
  logFile.write(nowToString() + os.getenv("USERNAME") + "@" + os.getenv("COMPUTERNAME") + " " + "logged on\n")
  logFile.write(nowToString() + "Logon activity started\n")

  # moving downloaded items
  moveFiles(baseDir + "/Downloads/", baseDir + "/Pictures/", ["jpg", "jpeg", "png", "webp"], logFile)
  moveFiles(baseDir + "/Downloads/", baseDir + "/Videos/", ["mp4", "mov", "webm"], logFile)
  moveFiles(baseDir + "/Downloads/", baseDir + "/Music/", ["mp3", "wav"], logFile)

  logFile.write(nowToString() + "Logon activity completed\n")

  # closing the log file
  logFile.close()
