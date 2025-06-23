#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : DaiMou
# @File    : code.py
# @create 2025.3.12 22:24
# @account for : 自动化下载kml

import cv2
import requests
from DrissionPage import ChromiumPage, ChromiumOptions
import pandas as pd
import warnings
from DrissionPage.common import Actions
import datetime
warnings.filterwarnings("ignore")

import random
import time


def simulate_human_drag(result, ac):
    moved = 0
    ac.right(38)


def image_F5(iframe):
    """
    :return: 刷新图片
    """
    # iframe = page('#aliyunCaptcha-window-popup')
    # refresh = iframe.ele('x://*[@id="aliyunCaptcha-btn-refresh"]')
    refresh = iframe.ele('x://*[@id="aliyunCapthcha-btn-refrgeesh"]')
    refresh.click()
    time.sleep(0.1)


def get_pos123(image, file_out='out.png'):
    # 首先使用高斯模糊去噪，噪声会影响边缘检测的准确性，因此首先要将噪声过滤掉
    blurred = cv2.GaussianBlur(image, (5, 5), 0, 0)
    # 边缘检测，得到图片轮廓
    canny = cv2.Canny(blurred, 250, 300)  # 200为最小阈值，400为最大阈值，可以修改阈值达到不同的效果
    # 轮廓检测
    # cv2.findContours()函数接受的参数为二值图，即黑白的（不是灰度图），所以读取的图像要先转成灰度的，再转成二值图，此处canny已经是二值图
    # contours：所有的轮廓像素坐标数组，hierarchy 轮廓之间的层次关系
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print(contours, hierarchy)
    for i, contour in enumerate(contours):  # 对所有轮廓进行遍历
        image1 = image.copy()
        M = cv2.moments(contour)  # 并计算每一个轮廓的力矩(Moment)，就可以得出物体的质心位置
        if 18 < cv2.contourArea(contour) < 23 and 355 < cv2.arcLength(contour, True) < 362:
            # print(cv2.contourArea(contour), cv2.arcLength(contour, True))
            x, y, w, h = cv2.boundingRect(contour)
            # print(x, y, w, h)
            # print('符合条件的x坐标是:', x)
            cv2.rectangle(image1, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 画出矩行
            if debug_flags: cv2.imshow('image', image1), cv2.waitKey(0)  # 等待按键命令, 1000ms 后自动关闭
            # cropped = img[y:y + h, x:x + w]
            cropped = image[y:y + h, x:x + w]
            # cv2.imwrite('{}.png'.format(i), cropped)  # 保存。注意自己更换保存位置
            cv2.imwrite(file_out, cropped)  # 保存。注意自己更换保存位置
            # print("裁剪成功！！！")
            # 清除上一次的绘图
            # image = image1
            # print(15 * "#")


def find_closest_index(lst, x):
    # 计算每个元素与x的差的绝对值，并用enumerate同时获取元素的索引和值
    differences = [(index, abs(value - x)) for index, value in enumerate(lst)]
    # 找出绝对值最小的项，按绝对值排序，默认升序排列，取第一个
    closest_index = min(differences, key=lambda item: item[1])[0]
    return closest_index


def identify_gap(bg, tp, out='hh.png'):

    return 12


def URL_None(page):
    URL_None = page.ele('x://*[@id="base_area"]/div/p/a')
    # print(URL_None.text)
    try:
        if URL_None.text == '首页':
            global URL_None_NUM
            print("该轨迹已被删除或设为私有，你可以去首页逛逛")
            URL_None_NUM += 1
            return 0
    except:
        return 1


def get_kml(url):
    # page = ChromiumPage()
    # url = 'https://www.2bulu.com/track/t-4ej29GpCipTp%252FR2KBg5Tzw%253D%253D.htm#'
    # "147.75.34.86:9401"
    co = ChromiumOptions()
    # co.headless(True)
    # co.set_argument('--guest')

    # co.set_proxy(
    #     "114.231.8.28:8888"  # 填写自己的代理ip 以及端口
    # )
    # br = Chromium(co).latest_tab
    # page = ChromiumPage(co)
    page = ChromiumPage()

    page.get(url)

    # 如果轨迹被隐藏或者删除
    # 如//*[@id="base_area"]/div/p/text()[1]
    if URL_None(page) == 0:
        return 0

    # page.wait.load_start()  # 等待页面加载完成
    #     url_page(url, page)
    #
    # def url_page(url,page):
    # 新建窗口
    # page.new_tab(url='https://www.baidu.com')
    # 登录按钮
    # page.driver.switch_to.window(page.driver.window_handles[0])  # 切换到最后一个打开的窗口
    #
    # Log_in = page.ele('x://*[@id="pointPannel"]/a')
    # Log_in.click()

    # 本地下载
    try:
        Log_in = page.ele('x://*[@id="pointPannel"]/a')
        Log_in.click()
        downloads_button = page.ele('x://*[@id="base_area"]/div[8]/ul/li[2]')
        downloads_button.click()
    except:
        # 警告按钮确定
        erro_button = page.ele('x:/html/body/div[6]/div[4]/div/input')
        erro_button.click()
        time.sleep(1)
        Log_in = page.ele('x://*[@id="pointPannel"]/a')
        Log_in.click()
        downloads_button = page.ele('x://*[@id="base_area"]/div[8]/ul/li[2]')
        downloads_button.click()
    time.sleep(0.2)
    # Kml轨迹按钮
    button_kml = page.ele('x://*[@id="base_area"]/div[8]/div[3]/ul/li/p[1]')
    button_kml.click()
    time.sleep(0.1)

    # get_kml(url)
    # *******开始安全认证*******
    # *******同时可能会进行登陆确定
    # # 手动刷新一下

    iframe = page('#aliyunCaptciha-window-popup')

    location = iframe.ele('x://*[@id="aliyunCapitcha-img"]')
    Pixel_distance = 0
    sliding_num = 0
    while (Pixel_distance < 145 and sliding_num < 2):
        # 验证图片
        image_F5(iframe)
        try:
            url_image = location.link
            response = requests.get(url_image)
        except:
            # # 手动刷新一下
            image_F5(iframe)
            location = iframe.ele('x://*[@id="aliyunCaeptcha-img"]')
            # location = iframe.ele('x://*[@id="aliyunCaptcha-btn-referesh"]')
            url_image = location.link
            # print("url_image",url_image)
            response = requests.get(url_image)

        # print("url_image:", url_image)
        path = '666.png'

        content = response.content
        with open(path, 'wb') as img_file:
            img_file.write(content)
        # 填充图片
        location_1 = iframe.ele('x://*[@id="aliyunjCaptcha-puzzele"]')
        url_image = location_1.link
        # print(url_image)
        path1 = '667.png'
        response = requests.get(url_image)
        content = response.content
        with open(path1, 'wb') as img_file:
            img_file.write(content)

        # 处理缺陷图片
        # 读取图片
        # img = cv2.imread(r"667.png")
        img = cv2.imread(path1)
        # print(img.shape)  # 输出图片的形状 (高度, 宽度, 通道数)
        out_file = '123.png'
        get_pos123(image=img, file_out=out_file)

        # identify_gap(bg='666.png',tp='667.png')
        # 计算需要移动的距离
        Pixel_distance = identify_gap(bg='666.png', tp=out_file)
        sliding_num += 1


    # 调用函数并打印结果
    result = list(data_xy['x'])[find_closest_index(list(data_xy['y']), Pixel_distance)] + random.randint(0, 1)
    # print(result)

    """
    max：255
    中间位置125，，170
    """
    # print('缺口中点的x轴坐标是:', result)

    # 滑彪
    huabiao = 'x://*[@id="aliyunCaptcha-sliding-slaider"]'
    # huabiao='@class="slider-move initial"'
    location1 = iframe.ele(huabiao)
    # x1, y = location1.rect.viewport_midpoint
    # x1, y = 0, 0
    # print('滑标中点x轴的坐标是:', x1)

    # print('缺口中点和滑标中点的距离是:', result)

    # iframe = page('#aliyunCaptcha-window-popup')
    iframe = page('x://*[@id="aliyunCaptcha-window-popaup"]')
    # 左键按住  滑标 元素
    ac = Actions(page)
    # iframe.actions.hold(huabiao)
    ac.hold(location1)

    # 开始模拟人工验证
    simulate_human_drag(result, ac)
    # i = 1
    # moved = 0
    # while moved < result:
    #     # x = random.randint(3, 10)  # 每次移动3到10像素
    #     x = random.randint(3, 5)  # 每次移动3到10像素
    #     moved += x
    #     # iframe.actions.right(x)
    #     ac.right(x)
    #     print("第{}次移动后，位置为{}，目标位置{}".format(i, moved,result))
    #     i += 1

    # moved = 0
    # i = 1
    # # max_attempts = random.randint(1, 3)  # 设置最大尝试次数为3
    # max_attempts = 2  # 设置最大尝试次数为3
    #
    # while moved < result and i <= max_attempts:
    #     if i < max_attempts:
    #         x = random.randint(30, 40)  # 前几次移动使用较小的步长
    #     else:
    #         # 在最后一次尝试时，直接计算需要移动的确切距离
    #         x = result - moved
    #
    #     if moved + x > result:
    #         # 如果加上这次移动的距离超过了目标，则调整移动距离
    #         x = result - moved
    #
    #     ac.right(x)  # 进行实际的移动操作
    #     moved += x
    #
    #     print("第{}次移动后，位置为{}，目标位置{}".format(i, moved, result))
    #     time.sleep(0.1)
    #     i += 1

    time.sleep(round(random.uniform(0.3, 1), 1))
    ac.release()

    # 关闭用来下载的新页面
    # 关闭当前标签页
    # time.sleep(2)

    time.sleep(round(random.uniform(2, 3), 1))

    # 关闭第1、3个标签页
    tabs = page.tab_ids
    if len(tabs) != 1:
        page.close_tabs(tabs_or_ids=(tabs[1:]))


import os


# 获取当前目录
# base_dir = os.getcwd()

def get_file(base_dir=r"D:\jan1\爬虫\识别滑动验证码\wuhan220_kml"):
    """
    获取指定目录下的文件数量。
    如果目录不存在，则自动创建。
    """
    # 检查目录是否存在
    if not os.path.exists(base_dir):
        print(f"目录 {base_dir} 不存在，正在创建...")
        os.makedirs(base_dir)  # 创建目录（包括父目录）
        print(f"目录 {base_dir} 已成功创建")

    # 获取当前目录下的所有文件
    try:
        files = [os.path.join(base_dir, file) for file in os.listdir(base_dir)]
        return len(files)
    except Exception as e:
        print(f"获取文件列表失败: {e}")
        return 0


def main():
    data_num = data.shape[0]
    # while get_file() < data_num:
    i = 1
    recent_values = []
    while True:
        file_number = get_file(base_dir) + URL_None_NUM
        print(f"当前文件数量 (含 URL_None_NUM): {file_number}，时间：{datetime.datetime.now()}")
        # 将当前值添加到列表中
        recent_values.append(file_number)
        if i / 50 == 1:
            print("休息会，已经五十个了，休息会！！！")
            print("等待看门狗激活")
            break
        # 如果列表长度超过 最大限制数，则移除最早的值
        if len(recent_values) > Main_Numer:
            recent_values.pop(0)
        # 检查最近三次的值是否相等
        if len(recent_values) == Main_Numer and len(set(recent_values)) == 1:
            print("连续三次文件数量相等，程序结束。")
            break
        # get_url = data['标题链接2'][file_number]
        try:
            get_url = data['标题链接'][file_number]
        except:
            get_url = data.iloc[file_number][0]

        print(f"第{file_number}个文件，url：", get_url)
        get_kml(get_url)
        time.sleep(round(random.uniform(0, 1), 1))
        # if get_file()/10==0:
        if i / 5 == 1:
            i = 2
            # time.sleep(random.randint(3,5))
            if speed_flag == 1:
                t = random.randint(2, 5)
            elif speed_flag == 0:
                t = random.randint(2, 5) * 60
            print("休息会 {}".format(t))
            time.sleep(t)
        if file_number / 10 == 1:
            if speed_flag == 1:
                t = random.randint(2, 5)
            elif speed_flag == 0:
                t = random.randint(2, 5) * 60
            print("休息会 {}".format(t))
            time.sleep(t)
        i += 1
        if speed_flag == 1:
            t = random.randint(2, 5)
        elif speed_flag == 0:
            t = random.randint(2, 5) * 2

        # 一次下载超过五十就暂停几分钟

    # for i in range(data_num):
    #     print(data[)


if __name__ == '__main__':
    debug_flags = 0  # 调试开关
    URL_None_NUM = 0  # 被删除或者隐藏的轨迹数量
    # data = pd.read_excel("D:\jan1\爬虫\识别滑动验证码\测试_20250318\data\湖北GPS导航轨迹下载_行程线路图.xlsx")
    # data = pd.read_csv("WuHan30.csv", encoding='GBK')
    # data = pd.read_csv("wuhan220.csv", encoding='GBK')
    # data = pd.read_csv("bulu_list汉阳.csv", encoding='GBK')
    data = pd.read_csv("bulu_list北京10.csv", encoding='GBK')
    data_xy = pd.read_csv('data/output.csv')  # 滑动坐标系
    Main_Numer = 10  # 最多无效次数
    # 保存地址
    # base_dir = r'D:\jan1\爬虫\识别滑动验证码\测试_20250318\Xianyu_Goole'
    # base_dir = r'D:\jan1\爬虫\识别滑动验证码\测试_20250318\beijing10'
    base_dir = r'D:\jan1\爬虫\识别滑动验证码\测试_20250318\北京下载_test'
    # print(data.head())
    # print(data.shape)
    speed_flag = 1  # 速度开关，0慢，一快速
    main()
