import math
import json
from fuclib import ezfuc
import pandas as pd
import pytesseract
from PIL import Image
from io import BytesIO


def page(total, num):
    total_page = math.ceil(int(total) / num)
    return total_page


def ex(res, ex=''):
    if ex == "json":
        return res, json.loads(res)
    else:
        return ezfuc.parse_html(res, ex=ex)


def get1(arr, default=''):
    return ezfuc.get_first(arr, default)


def rpc(text, which):
    return ezfuc.replace_plus(text, which)


def get_xlsx(file_path):
    df = pd.read_excel(file_path)
    df.reset_index(drop=True)
    df.dropna(axis='columns', how='all', inplace=True)
    df.fillna("", inplace=True)
    return df


def ocr_des(img_bytes):
    f = BytesIO(img_bytes)
    img = Image.open(f)
    img = img.convert("L")
    img = img.point(lambda x: 255 if x >= 70 else 0)
    img.show()
    return pytesseract.image_to_string(img)


if __name__ == '__main__':
    with open(r"C:\Users\Dell\Desktop\CheckCode.png", "rb") as f:
        ret = f.read()
    ocr_des(ret)