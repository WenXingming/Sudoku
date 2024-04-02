'''
    ---- Tessaract OCR 识别度很低, 且没有识别到的物体的位置信息. 故在原代码中是先对图像进行处理得到 thresh 图, 再对 thresh 图进行轮廓检测(得到坐标)后对轮廓矩形进行扩大后再提取数字区域进行 OCR 识别
    ---- 使用百度云 OCR 则无此问题
'''
from aip import AipOcr # 安装 sdk API: pip install baidu-aip
import numpy as np
import cv2
import os
import time

# 请填写你在百度云上申请的 APPID AK SK (百度云 OCR)
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
# 设置连接超时时间
AipOcr.setConnectionTimeoutInMillis(client, 2000)


image_path = r'.\image.png'
gray_path = r'.\gray.png'
thresh_path = r'.\thresh.png'
imageWidth, imageHeight = 0, 0

# 百度云 OCR 识别图片也存在识别不准确的问题, 故通过 opencv 对图片进行处理为 thresh 图像（二值化图像即黑白图像）
def image_process(image_path):
    image = cv2.imread(image_path)
    if(image is None):
        print("can't find image!")
        exit()
    # 为全局变量赋值：图像分辨率
    global imageWidth, imageHeight
    imageWidth, imageHeight = image.shape[1], image.shape[0]
    # 图像灰度化和二值化
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV)  
    # 保存处理后的图像
    cv2.imwrite(gray_path, gray) 
    cv2.imwrite(thresh_path, thresh) 
image_process(image_path)


# 百度云 OCR 读取灰度化图文件
def get_file_content(filePath):
    with open(filePath, "rb") as fp:
        return fp.read()
# 某些图像比较特殊，二值化阈值没设置好可能直接变成空白图像, 所以这里使用灰度图像 (彩色图则遇到了 OCR 不准确的问题)
image = get_file_content(image_path)


# 调用通用文字识别（高精度含位置信息版。注：标准含位置版有时不准）
ocr_res = client.accurate(image)
# print(ocr_res)


# 创建一个二维数组来存储数独的内容, 将识别结果填充到二维数组中
sudoku_array = np.full((9, 9), '.', dtype=str)
words_result = ocr_res['words_result']
for word_result in words_result:
    # 识别的单词和位置
    word = word_result['words']
    location = word_result['location']
    # 计算数子中心坐标的位置
    x, y, w, h = location['left'], location['top'], location['width'], location['height']
    x_center, y_center = x + w / 2, y + h / 2
    # 计算数字中心在二维数组中的位置
    row_length, col_length = imageHeight / 9, imageWidth / 9
    row_index, col_index = int(y_center / row_length), int(x_center / col_length)
    if word.strip() in "123456789":
        sudoku_array[row_index, col_index] = word.strip()

# 打印二维数组
print("数独数组识别成功:\n", sudoku_array)

#写入数组（数独题目）到 question.txt 文件
def write_question_file(sudoku, file_path):
    with open(file_path, 'w') as f:
        for row in sudoku:
            f.write(' '.join(row) + '\n')
write_question_file(sudoku_array, r'.\tmp\question.txt')
print("数独数组写入 ./tmp/question.txt 文件成功...")
print('-----------------------------------------------')

# 执行 C++ 程序: 读取 question.txt 文件, 解数独并写入 answer.txt 文件
ret = os.system(r'.\Sudoku\x64\Debug\Sudoku.exe')
if ret == 0:
    print("C++ 程序解数独成功！")
    print('-----------------------------------------------')
    
# 读取 answer.txt 文件, 保存到 answer_array (转换为np数组) 打印数独数组解答结果
def read_answer_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip().split() for line in f.readlines()]
answer_array = read_answer_file(r'.\tmp\answer.txt')
answer_array = np.array(answer_array)
print("数独数组解答结果为:\n", answer_array)
print('-----------------------------------------------')