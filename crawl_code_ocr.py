# -*- coding:UTF-8 -*-#
"""
Created on 2018年2月9日
@author: Leo
"""
# Python内置库
import os

# 第三方库
import requests
import pytesseract
from PIL import Image
from lxml import etree

# 设置下可执行文件的位置, 目前只设置了windows的. 后期增加Linux的
INSTALL_PATH = "C:/Program Files (x86)/Tesseract-OCR/"
# tesseract的执行位置
pytesseract.pytesseract.tesseract_cmd = INSTALL_PATH + '/tesseract'
# 模型库的位置
TESSDATA_CONFIG = '--tessdata-dir "%s/tessdata"' % INSTALL_PATH


def parser(return_json=False):
    """
    解析识别
    :param return_json: bool 如果为True返回list(dict) 可以直接insert_many到MongoDB
    :return: return_json为True才有, 否则啥都没有
    """
    # 代理URL
    url = "https://proxy.mimvp.com/free.php?proxy=in_hp"
    html = requests.get(url=url).content
    selector = etree.HTML(html)
    # 获取img的src, ip, ip的类型(HTTP或HTTPS)
    img_src = selector.xpath('//tbody//img/@src')
    ip_list = selector.xpath('//tbody/td[@class="tbl-proxy-ip"]/text()')
    type_list = selector.xpath('//tbody/td[@class="tbl-proxy-type"]/text()')
    # img_src的奇数项 拼接上完整的URL
    img_list = ["https://proxy.mimvp.com/" + d for d in img_src[0::2]]

    # 判断image的文件夹是否存在
    if os.path.exists("./image") is not True:
        os.mkdir("image")

    # 代理池
    ip_proxy_data = []
    for i in range(len(img_list)):
        # stream用流参数 可以变成比特流用with进行保存
        r = requests.get(img_list[i], stream=True)
        code = img_list[i].split("&")[-1].split("=")[-1]
        with open('./image/%s.png' % code, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)

        # 意思就是打开with保存的那些图片 -> 灰度 -> 放大到 150 * 100 -> 高质量(Image.ANTIALIAS = Image.LANCZOS) -> 保存为png(质量为100%)
        Image.open("./image/%s.png" % code).convert('L').resize((150, 100), Image.ANTIALIAS).save("validate_code.png",
                                                                                                  'PNG', quality=100)
        # 调用pytesseract的图片转文字的库 config就是加载配置路径 lang就是库的名称 英文和阿拉伯字母用eng
        port = pytesseract.image_to_string(Image.open("validate_code.png"), config=TESSDATA_CONFIG, lang="eng")

        if return_json is not True:
            print("IP&PORT ---> %s:%s; 类型为: %s" % (ip_list[i], port, type_list[i]))
        else:
            dict_proxy = {"address": ip_list[i], "port": port, "type": type_list[i]}
            ip_proxy_data.append(dict_proxy)
    if return_json:
        return ip_proxy_data


if __name__ == '__main__':
    # 参数默认为False哈
    parser()
