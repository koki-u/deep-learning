import pyocr
import pyocr.builders
import cv2
from PIL import Image
import sys
import matplotlib.pyplot as plt

def ocr_tool_opencv(file_name,bitwise=True):
    """
     using opencv and Pillow

    Args:
        file_name ([type]): file name str
        bitwise (bool, optional): Black and white inversion . Defaults to True.
    """
    #利用可能なOCRツールを取得
    tools = pyocr.get_available_tools()

    #利用可能なOCRツールはtesseractしか導入していないため、0番目のツールを利用
    tool = tools[0]

    np_image = cv2.imread(file_name)
    #dst = np_image[130, 705, 500, 780]
    #cv2.imwrite(file_name, dst)

    edges = cv2.Canny(np_image, 100, 200)

    if bitwise:
        edges = cv2.bitwise_not(edges)

    # convert to pillow image　->  pil.Image型にしないとエラーになる
    pil_image = Image.fromarray(edges)

    builder_list = pyocr.builders.WordBoxBuilder(tesseract_layout=6)
    builder_text = pyocr.builders.TextBuilder(tesseract_layout=6) 
            # TextBuilder  文字列を認識  
            # WordBoxBuilder  単語単位で文字認識 + BoundingBox  
            # LineBoxBuilder  行単位で文字認識 + BoundingBox  
            # DigitBuilder  数字 / 記号を認識
            # DigitLineBoxBuilder  数字 / 記号を認識 + BoundingBox  
    res = tool.image_to_string(pil_image,lang="jpn",builder=builder_list)
    res_txt = tool.image_to_string(pil_image,lang="jpn",builder=builder_text)

    #取得した文字列を表示
    print(res_txt)
    #　WordBoxBuilderを指定するとリスト型が戻り値
    # print(type(res))

    #以下は画像のどの部分を検出し、どう認識したかを分析
    out = cv2.imread(file_name)

    for d in res:
        print(d.content) #どの文字として認識したか
        print(d.position) #どの位置を検出したか
        # print(d.position[0], d.position[1])
        cv2.rectangle(out, d.position[0], d.position[1], 255, 2) #検出した箇所を囲む

    #検出結果の画像を表示
    print('quit press key')

    cv2.namedWindow("img", cv2.WINDOW_NORMAL)
    cv2.imshow("img",out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()   

if __name__ == '__main__':
    file_name ="recognition/rec3.JPG"# 認識したいファイル名を入れてください
    ocr_tool_pillow(file_name,bitwise=False)
    #ocr_tool_opencv(file_name,bitwise=False)