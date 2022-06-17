import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pyocr
import pyocr.builders
from PIL import Image
import os

#ファイルの読み込み
file_name = "recognition/rec3.JPG"
np_image = cv2.imread(file_name)

tools = pyocr.get_available_tools()
tool = tools[0]

all_Figure = plt.figure()

#original photo
plt.subplot(111)
plt.title('original')
image_chainese = np_image[705:780, 130:500]
image_japanese = np_image[930:1000, 130:500]

#rectangle = cv2.rectangle(image, pt1=(0, 10), pt2=(120, 150), color=255)
plt.imshow(image_chainese, cmap='gray')
plt.show()

#cropping original photo to recoganize more
image2_chainese = np_image[705:780, 130:500]
image2_japanese = np_image[930:1000, 130:500]


for maxVal in range(0,1300,100):
    edges = cv2.Canny(image2_chainese, 100, maxVal)
    pil_image = Image.fromarray(edges)
    plt.imshow(edges, cmap='gray')

    builder_list = pyocr.builders.WordBoxBuilder(tesseract_layout=6)
    builder_text = pyocr.builders.TextBuilder(tesseract_layout=6) 
    res = tool.image_to_string(pil_image,lang="jpn",builder=builder_list)
    res_txt = tool.image_to_string(pil_image,lang="jpn",builder=builder_text)
    print(res_txt)
    #print(type(edges))
    #image_color = cv2.cvtColor(image_color, cv2.COLOR_BAYER_GB2RGB)
    plt.title("Parameter1 : {} \nParameter2 : 100".format(maxVal))
    dirname = "recognition/"
    plt.savefig(dirname + "img{}.jpg".format(maxVal))
    
    for d in res:
        #print(d.content)
        #print(d.position)
        #print(sorted(d.position[0], reverse=False), sorted(d.position[1], reverse=False))        
        img = cv2.rectangle(edges, d.position[1], d.position[0], 255)
        #cv2.imwrite(dirname + "img{}.jpg".format(maxVal), img)
    
    plt.title(maxVal)
    plt.show()

#plt.imshow(edges, cmap='gray')