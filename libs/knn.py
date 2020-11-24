import joblib
from PIL import Image
import cv2
import os
import numpy as np

from spider_code.confs import config


def smartSliceImg(img,count=4, p_w=3):
    '''
    :param img:
    :param outDir:
    :param count: 图片中有多少个图片
    :param p_w: 对切割地方多少像素内进行判断
    :return:
    '''
    w, h = img.size
    pixdata = img.load()
    eachWidth = int(w / count)
    beforeX = 0
    cut_imgs = []
    for i in range(count):

        allBCount = []
        nextXOri = (i + 1) * eachWidth

        for x in range(nextXOri - p_w, nextXOri + p_w):
            if x >= w:
                x = w - 1
            if x < 0:
                x = 0
            b_count = 0
            for y in range(h):
                if pixdata[x, y] == 0:
                    b_count += 1
            allBCount.append({'x_pos': x, 'count': b_count})
        sort = sorted(allBCount, key=lambda e: e.get('count'))

        nextX = sort[0]['x_pos']
        box = (beforeX, 0, nextX, h)
        cut_imgs.append(img.crop(box))
        beforeX = nextX
    return cut_imgs

def prehandle_img(im):
    im = im.convert('L')
    im = im.point(lambda x: 0 if x > 230 else 255)
    im = im.convert('RGB')
    im = im.resize((120, 60), Image.ANTIALIAS)
    return im
def img_predict(filename):
    im = Image.open(filename)
    im = prehandle_img(im)
    cut_imgs = smartSliceImg(im)
    abs_path = config.libs
    clf = joblib.load(r'%s\knn.pkl' % abs_path)
    data = []
    for img in cut_imgs:
        im = cv2.cvtColor(np.asarray(img), cv2.COLOR_BGR2GRAY)
        if im.size != 1800:
            im = np.pad(im, ((0, 0), (0, 3)), 'constant', constant_values=(0, 0))
        image = im.reshape(-1)
        data.append(image)

    x = np.array(data)
    pre_y_test = clf.predict(x)
    pre_y_test = ''.join(pre_y_test)
    return pre_y_test

if __name__ == '__main__':
    # pre_y_test = img_predict(r"W:\ZLCollector\ZLCollector_Aptitude\spider_code\api\a.png")
    # print(pre_y_test)
    pass