#!/usr/bin/env python

# Image stitch utility to stitch images horizontally or vertically

from PIL import Image
import os, json

# setting slash as per OS
__slash = "/"
if os.name == "nt" :
  __slash = "\\"

### main area ###
if __name__ == "__main__" :
  configFp = open("./config.json")
  config = json.load(configFp)
  configFp.close()
  rootFolder = config["PICTURES_ROOT_FOLDER"]
  print("Using folder " + rootFolder)

  # getting the list of files
  fileList = []
  while(True) :
    fileName = input("Enter file name to add (done to proceed) : ")
    if(fileName == "done") :
      break
    fileList.append(Image.open(rootFolder + __slash + fileName))

  # getting direction
  while(True) :
    isV = input("To be stitched vertically [y/n] : ")
    if((isV == "y") or (isV == "n")) :
      break

  # getting output file name
  outputFileName = input("Enter output file name : ")

  # final image dimensions
  width = 0
  height = 0
  if(isV == "y") :
    # setting width
    for file in fileList :
      if(file.size[0] > width) :
        width = file.size[0]

    # adding height
    for file in fileList :
      height += int(width / file.size[0] * file.size[1])
  else :
    # setting height
    for file in fileList :
      if(file.size[1] > height) :
        height = file.size[1]

    # adding width
    for file in fileList :
      width += int(height / file.size[1] * file.size[0])

  # stiching images
  final = Image.new('RGB', (width, height), color = (0, 0, 0))
  print("Final dimensions are " + str(width) + ", " + str(height))
  pos = 0
  if(isV == "y") :
    for file in fileList :
      temp = file.resize((width, int(width / file.size[0] * file.size[1])))
      final.paste(temp, (0, pos))
      print("Image pasted at 0, " + str(pos))
      pos += int(width / file.size[0] * file.size[1])
  else :
    for file in fileList :
      temp = file.resize((int(height / file.size[1] * file.size[0]), height))
      final.paste(temp, (pos, 0))
      print("Image pasted at " + str(pos) + ", 0")
      pos += int(height / file.size[1] * file.size[0])

  # saving image
  final.save(rootFolder + __slash + outputFileName + ".jpg", quality = 50)
  print("Saved!")
