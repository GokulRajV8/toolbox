#!/usr/bin/env python

import os, json

# setting slash as per OS
__slash = "/"
if os.name == "nt" :
  __slash = "\\"

### add trailing or leading spaces for text and numbers respectively ###
def addSpaces(ip:str, size:int) -> str :
  ipSize = len(ip)
  spaces = ""
  i = 0
  while i < (size - ipSize) :
    spaces += " "
    i += 1
  if ip.isnumeric() :
    return spaces + ip
  else :
    return ip + spaces

### get number of dashes ###
def getDashes(num: int) -> str :
  output = ""
  while num > 10 :
    output += "----------"
    num -= 10
  while num > 0 :
    output += "-"
    num -= 1
  return output

### convert list into a multi-line indented string ###
def formatList(ip:list, depth:int=0) -> str :
  op = ""
  ipSize = len(ip)

  # adding spaces before bracket
  i = 0
  while i < depth :
    op += "  "
    i += 1

  # adding opening bracket
  op += "[\n"

  # adding items
  itemIndex = 1
  for item in ip :
    if type(item).__name__ == "str" :
      # adding spaces before item
      i = 0
      while i < (depth + 1) :
        op += "  "
        i += 1
      op += item
    else :
      op += formatList(item, depth + 1)
    if itemIndex == ipSize :
      op += "\n"
    else :
      op += ",\n"
    itemIndex += 1

  # adding spaces before bracket
  i = 0
  while i < depth :
    op += "  "
    i += 1

  # adding closing bracket
  op += "]"

  return op

### convert a nested list (table) as formatted table string with borders ###
def formatStringTable(ip:list) -> str :
  # type and size checking and column size setting
  colCount = len(ip[0])
  colsSize = [0] * colCount
  for row in ip :
    if type(row).__name__ != "list" :
      return "Invalid table : non lists present"
    else :
      if len(row) != colCount :
        return "Invalid table : rows have irregular size"
      else :
        i = 0
        while i < colCount :
          if type(row[i]).__name__ != "str" :
            return "Invalid table : cells have non-strings"
          else :
            if len(row[i]) > colsSize[i] :
              colsSize[i] = len(row[i])
          i += 1

  # making all the elements in a column equally sized
  for row in ip :
    i = 0
    while i < colCount :
      row[i] = addSpaces(row[i], colsSize[i])
      i += 1

  colFlag = True
  op = ""
  border = ""
  data = ""
  for row in ip :
    if colFlag :
      border = "+"
      data = "|"
      i = 0
      while i < colCount :
        border += getDashes(colsSize[i] + 2) + "+"
        data += " " + row[i] + " |"
        i += 1
      colFlag = False
      op += border + "\n" + data + "\n" + border + "\n"
    else :
      data = "|"
      i = 0
      while i < colCount :
        data += " " + row[i] + " |"
        i += 1
      op += data + "\n"
  op += border
  return op

### get the file info from file name as [filetype, filesize_in_bytes, numberOfLines] ###
def getFileInfo(dir:str, filename:str) -> list :
  output = []
  # file type
  parsedText = [textPart for textPart in filename.split(".") if textPart != ""]
  if len(parsedText) == 1 :
    output.append("*")
  else :
    output.append(parsedText[-1])
  output.append(os.stat(dir + filename).st_size)
  fp = open(dir + filename, "r")
  try :
    output.append(len(fp.readlines()))
  except :
    output[0] = "INV_CHAR (" + parsedText[-1] + ")"
    output.append(0)
  fp.close()
  return output

### get the list of files in a directory as a nested list ###
def getDirContent(dir:str, rootSize:int=0) -> list :
  op = []
  nonDirList = []
  dirList = []

  # adding trailing slash if not present
  if (dir[:-1] != __slash) :
    dir += __slash

  # adding directory name
  if rootSize == 0 :
    rootSize = len(dir)
  op.append(dir[rootSize - 1:])

  # adding entries
  for item in os.listdir(dir) :
    if os.path.isdir(dir + item) :
      # excluding .git directory
      if item == ".git" :
        continue
      dirList.append(getDirContent(dir + item, rootSize))
    else :
      nonDirList.append(item)

  # appending entries and returning
  op.extend(nonDirList)
  op.extend(dirList)
  return op

### get the consolidated info of all files present in the directory using getFileInfo recursively ###
def getDirInfo(dir:str) -> list :
  output = []

  # adding trailing slash if not present
  if (dir[:-1] != __slash) :
    dir += __slash

  # adding entries
  for item in os.listdir(dir) :
    if os.path.isdir(dir + item) :
      # excluding .git directory
      if item == ".git" :
        continue
      for insideItem in getDirInfo(dir + item) :
        typeFoundFlag = False
        for fileType in output :
          if fileType[0] == insideItem[0] :
            typeFoundFlag = True
            fileType[1] += insideItem[1]
            fileType[2] += insideItem[2]
            fileType[3] += insideItem[3]
            break
        if not typeFoundFlag :
          output.append([insideItem[0], insideItem[1], insideItem[2], insideItem[3]])
    else :
      typeFoundFlag = False
      fileDetails = getFileInfo(dir, item)
      for fileType in output :
        if fileType[0] == fileDetails[0] :
          typeFoundFlag = True
          fileType[1] += 1
          fileType[2] += fileDetails[1]
          fileType[3] += fileDetails[2]
          break
      if not typeFoundFlag :
        output.append([fileDetails[0], 1, fileDetails[1], fileDetails[2]])

  return output

### main area ###
if __name__ == "__main__" :
  rootDirectory = input("Enter the root directory name : ")
  configFp = open("./config.json")
  config = json.load(configFp)
  configFp.close()
  fp = open(config["REPORTS_SRC_DIR"] + __slash + "codebase-details.txt", "w")
  fp.write("Root directory name : " + rootDirectory + "\n")
  fp.write("\nDirectory structure :\n" + formatList(getDirContent(rootDirectory)) + "\n")
  result = [
    ["File type", "Number of files", "Total size in bytes", "Number of lines"]
  ]
  result.extend(getDirInfo(rootDirectory))
  # stringifying result
  i = 0
  while i < len(result) :
    result[i] = [result[i][0], str(result[i][1]), str(result[i][2]), str(result[i][3])]
    i += 1
  fp.write("\nSize summary :\n" + formatStringTable(result) + "\n")
  fp.close()
  print("Output written to " + config["REPORTS_SRC_DIR"] + __slash + "codebase-details.txt")
