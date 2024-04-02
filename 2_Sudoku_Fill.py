'''
    本程序功能：根据已经解出的数独 answer.txt，填充到电脑屏幕中【仅限“数独宇宙”游戏】的空白的数独中（使用相对坐标，故应该不受屏幕分辨率影响）
'''
import pyautogui
import numpy as np
import keyboard
import time
import os

# 获取当前鼠标的坐标的辅助代码
# while(1):
#     # 获取当前鼠标的坐标
#     current_mouse_position = pyautogui.position()
#     # 打印当前鼠标的坐标
#     print("当前鼠标的坐标：", current_mouse_position)
#     # 间隔 1 秒
#     pyautogui.sleep(1)

# 定义一个回调函数，当按下指定的键时调用
def stop_program(keyboard_event):
    if keyboard_event.name == 'q' or keyboard_event.name == 'Q':  # 当按下 'q' 键时停止程序
        keyboard.unhook_all()  # 取消键盘事件监听
        print("程序已停止")
        # exit() # 退出程序. 不知为何, 可能由于资源阻塞无法退出程序, 所以使用 os._exit(0) 退出程序 (即使 os._exit(0) 无资源回收)
        os._exit(0)
        
keyboard.on_press(stop_program) # 注册按键事件监听

# 等待 7 秒, 等我切到数独游戏界面
print("等待 5 秒, 请快速切换到数独游戏界面...")
pyautogui.alert("7 秒后控制外设, 请快速切换到数独游戏界面...（按下键盘 q 或 Q 键强制退出程序！）") # 弹窗提示
time.sleep(7)

# 读取 answer.txt 文件, 保存到 answer_array (转换为np数组)
def read_answer_file(file_path):
    with open(file_path, 'r') as f:
        return [line.strip().split() for line in f.readlines()]
answer_array = read_answer_file(r'.\tmp\answer.txt')
answer_array = np.array(answer_array)
print("数独数组解答结果:\n", answer_array)
print('-----------------------------------------------')

# 屏幕分辨率
screenWidth, screenHeight = pyautogui.size()
print("屏幕分辨率：", screenWidth, screenHeight)

# 定义数独区域
sudoku_x, sudoku_y = 600, 185 # 测出来的数独区域的左上角坐标
sudoku_x_rate, sudoku_y_rate = sudoku_x / screenWidth, sudoku_y / screenHeight # 数独区域的左上角相对坐标
lengthSide = 80 # 测出的正方形格子的边长
lengthSide_rate_x = lengthSide / screenWidth # 正方形格子的边长相对于屏幕宽度的相对比例
lengthSide_rate_y = lengthSide / screenHeight # 正方形格子的边长相对于屏幕高度的相对比例

# 初始化要填充的方格的左上角起始坐标(比例)
startx_rate, starty_rate = sudoku_x_rate, sudoku_y_rate
# 向屏幕中填充数独数组 answer_array
rows, cols = answer_array.shape
for row in range(rows):
    for col in range(cols):
        # 计算每个格子的中心坐标
        center_x = startx_rate * screenWidth + lengthSide_rate_x * screenWidth / 2
        center_y = starty_rate * screenHeight + lengthSide_rate_y * screenHeight / 2
        # 将鼠标移动到格子的中心坐标8
        pyautogui.moveTo(center_x, center_y)
        # 输入数字, 0.1s 输入一个字符
        pyautogui.typewrite(answer_array[row, col], interval=0.1)
        # 要填充方格的左上角坐标向右移动一个格子
        startx_rate += lengthSide_rate_x
    startx_rate = sudoku_x_rate
    starty_rate += lengthSide_rate_y    
    
#提示数独数组填充成功
pyautogui.sleep(3)
# pyautogui.alert("弹窗: 数独数组填充成功！")
print("数独数组填充成功！")
print('-----------------------------------------------')

        
