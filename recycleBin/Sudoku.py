'''
    本程序功能：
    1、Python 识别数独图像, 识别数独数组, 将数独数组写入文件。
    2、调用 C++ 程序解数独, 读取解数独结果并打印
    (因为是两个进程, 所以需要文件来传递数据; 同时进程间因为文件的读写顺序关系需要同步, 所以在 Python 中调用执行 C++程序, 确保它们之间的执行顺序)
    
    ---- 安装 opencv-python 库来处理图像： pip install opencv-python (Tips: Tesseract OCR 识别准确率太低。为了提高OCR识别率，我们需要对图像进行处理)

    ---- 安装 Tesseract OCR 并设置安装目录进入环境变量: https://github.com/tesseract-ocr/tesseract
        (pytesseract 是基于 Tesseract OCR 引擎的 Python 封装库，因此首先需要安装 Tesseract OCR)
    ---- 安装 pytesseract 库调用 Tesseract OCR： pip install pytesseract
    
    # 安装百度 OCR 库，百度 OCR 识别率高，但是需要联网。暂时未使用百度 OCR
    ---- pip install baidu-aip
    ---- pip install chardet
'''

from PIL import Image   # 图像处理
import cv2              # 图像处理
import numpy as np      # 数组操作
import pytesseract      # Tessocr OCR 库
import os               # 调用系统命令, 执行 C++ 程序解数独
from baiduyun import baidu_ocr       # 自己封装的百度 OCR 包

# 创建一个二维数组来存储数独的内容
sudoku_array = np.full((9, 9), '.', dtype=str)
 
# 读取彩色图像
image_path = r'.\sudoku.png'
image = cv2.imread(image_path)
if(image is None):
    print("can't find image!")
    exit()
# cv2.imshow('Image', image)

# 标准化图像大小, 后续过滤轮廓时会用到！
# print(image.shape)
image = cv2.resize(image, (750, 750))

# 灰度化图。 彩色图像转换为灰度图像, 只保留亮度和灰度信息, 去除色彩信息, 便于计算机处理
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Image', gray)

# 二值化图。将灰度图像转换为二值（只有黑白两色）图像, 便于计算机处理
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)

# 保存
# cv2.imwrite(r'.\tmp\thresh.png', thresh)

# cv2.imshow('Image', thresh)
# cv2.waitKey(0)

# 对【二值图像】进行轮廓检测. PS：例如数字 8, 会检测出两个轮廓, 一个是外轮廓, 一个是内轮廓!
# 参数: cv2.RETR_EXTERNAL 只会返回图像的外轮廓（整张图片的边缘所构成的轮廓），而不会包含内部的任何轮廓
# 参数: cv2.RETR_TREE 表示检测所有轮廓, 包含层级关系（包含了整张图片的边缘所构成的轮廓，以及图像中的其他所有轮廓）
# 参数: cv2.RETR_LIST 表示检测所有轮廓, 不包含层级关系（包含了整张图片的边缘所构成的轮廓，以及图像中的其他所有轮廓）
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
# 遍历轮廓。记录识别的轮廓数量（因为中间会有轮廓的过滤）
for contour in contours:
    #过滤轮廓【过滤条件十分重要】, 例如整张图片的边缘所构成的轮廓(>10000)和噪点(数字内轮廓<120, 例如数字4、6、8、9)
    if cv2.contourArea(contour) > 10000 or cv2.contourArea(contour) < 40:
        continue
    
    # 获取轮廓外接矩形的坐标
    x, y, w, h = cv2.boundingRect(contour)  
    # 处理（扩、缩放）轮廓的外接矩形范围, 以便提取数字区域和识别（OCR）数字. digit_region = thresh[y:y+h, x:x+w] 这个区域过于紧凑, 识别率非常低！
    overNumber = 20
    x_l, y_t, x_r, y_b = x-overNumber, y-overNumber, x+w+overNumber, y+h+overNumber
    # 【image上】绘制轮廓外接矩形. PS：不要绘制在 thresh 图上, 否则会影响后续的数字区域提取
    cv2.rectangle(image, (x_l, y_t), (x_r, y_b), (0, 255, 0), 2)
    
    # 提取【thresh图】数字区域（扩大后的矩形区域！用于后续识别）。试过其他图, tessocr 无法识别出数字，只有 thresh 图可以识别出数字（最好用还得黑白图）
    digit_region = thresh[y_t:y_b, x_l:x_r]
    
    # 使用 pytesseract 对【提取的区域】进行字符识别. 识别软件太差只能英文
    digit_text = pytesseract.image_to_string(digit_region, lang='eng', config='--psm 6 --oem 3 -c tessedit_char_whitelist=123456789')
    
    # # 使用百度 OCR 对【提取的区域】进行字符识别, 返回字典
    # ocr_ret_dict = baidu_ocr.get_ocr_ret_from_image(digit_region)
    # wordsDict_list = ocr_ret_dict['words_result']
    # digit_dict = wordsDict_list[0]
    # digit_text = digit_dict['words']
    
    # 计算数字区域在二维数组中的位置: 以 row 为例, 棋盘被分为 9 份, 则每份的长度为 row_length = image.shape[0] / 9
    # 则 row_index = y（中心坐标更好） / row_length 向下取整。
    # 另一种计算 row_index = (y / image.shape[0]) / (1/9) = y * 9 / image.shape[0]
    row_length, col_length = image.shape[0] / 9, image.shape[1] / 9
    center_x, center_y = x + w / 2, y + h / 2
    row_index, col_index = int(center_y / row_length), int(center_x / col_length)
    # 将识别结果填充到二维数组中, 
    # 1、不知为何必须得.strip()去除字符串两端的空格和换行符
    # 2、if digit_text.strip() in '123456789' 是错误的不知道为啥。后面又是对了......
    if digit_text.strip():
        sudoku_array[row_index, col_index] = digit_text.strip()

# 打印二维数组
print("数独数组识别成功:\n", sudoku_array)
print('-----------------------------------------------')
# 展示轮廓检测并绘制轮廓外接矩形的图像. PS: image 可以绘制轮廓外接矩形,但 thresh 不行！因为我们是在 thresh 图上提取数字区域, 如果在 thresh 图上绘制轮廓外接矩形, 会影响后续的数字区域提取
cv2.imshow('image', image)   
cv2.waitKey(0)

#写入数组（数独题目）到 question.txt 文件
def write_question_file(sudoku, file_path):
    with open(file_path, 'w') as f:
        for row in sudoku:
            f.write(' '.join(row) + '\n')
write_question_file(sudoku_array, r'.\tmp\question.txt')
print("数独数组写入 question.txt 文件成功...")
print('-----------------------------------------------')

# # 执行 C++ 程序: 读取 question.txt 文件, 解数独并写入 answer.txt 文件
# cv2.waitKey(0) # 看一下是否识别成功
# ret = os.system(r'.\Sudoku.exe')
# if ret == 0:
#     print("C++解数独成功！结果已写入 answer.txt 文件...")
#     print('-----------------------------------------------')
    
# # 读取 answer.txt 文件, 保存到 answer_array (转换为np数组)
# def read_answer_file(file_path):
#     with open(file_path, 'r') as f:
#         return [line.strip().split() for line in f.readlines()]
# answer_array = read_answer_file(r'.\tmp\answer.txt')
# answer_array = np.array(answer_array)
# print("数独数组解答结果:\n", answer_array)
# print('-----------------------------------------------')

# cv2.destroyAllWindows()
