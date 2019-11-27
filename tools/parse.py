# -*- coding: utf-8 -*-
try:
    from win32com import client as wc
    import pythoncom
except Exception:
    pass

try:
    import subprocess
except Exception:
    pass

try:
    from PIL import Image
    import pytesseract
except Exception:
    pass

from tools.exception import MyExcelException
import sys
# from docx import Document
from io import BytesIO
import pandas as pd
import xlrd
from parsel import Selector
import re


def selector(res, encode=None):
    if hasattr(res, 'ok'):
        if encode:
            resp = Selector(res.content.decode(encode))
        else:
            apparent_encoding = res.apparent_encoding
            if '2312' in apparent_encoding or 'dows' in apparent_encoding or '8859' in apparent_encoding:
                apparent_encoding = 'gbk'
            try:
                resp = Selector(res.content.decode(apparent_encoding))
            except:
                resp = Selector(res.content.decode(apparent_encoding, 'ignore'))
    else:
        if isinstance(res, str):
            resp = Selector(res)
        else:
            resp = Selector(res.text)
    return resp


def wash_content(sc):
    sc = re.sub(r'<!--.*?-->', '', sc, count=0, flags=re.I)
    sc = re.sub(r'<script>.*</script>', '', sc, count=0, flags=re.I)
    sc = re.sub(r'<style>.*?</style>', '', sc, count=0, flags=re.I)
    sc = re.sub('<div.*?>', '<div>', sc, count=0, flags=re.I)
    sc = re.sub(r'</div>', '</div>', sc, count=0, flags=re.I)
    sc = re.sub('<span.*?>', '', sc, count=0, flags=re.I)
    sc = re.sub(r'</span>', '', sc, count=0, flags=re.I)
    sc = re.sub('<a.*?>', '', sc, count=0, flags=re.I)
    sc = re.sub(r'</a >', '', sc, count=0, flags=re.I)
    sc = re.sub('<font.*?>', '', sc, count=0, flags=re.I)
    sc = re.sub(r'</font>', '', sc, count=0, flags=re.I)
    sc = re.sub('<p.*?>', '<p>', sc, count=0, flags=re.I)
    sc = re.sub(r'</p.*?>', '</p>', sc, count=0, flags=re.I)
    sc = re.sub('<table.*?>', '<table>', sc, count=0, flags=re.I)
    sc = re.sub(r'</table>', '</table>', sc, count=0, flags=re.I)
    sc = re.sub('<tr.*?>', '<tr>', sc, count=0, flags=re.I)
    sc = re.sub(r'</tr>', '</tr>', sc, count=0, flags=re.I)
    sc = re.sub('<td.*?>', '<td>', sc, count=0, flags=re.I)
    sc = re.sub('<th.*?>', '<td>', sc, count=0, flags=re.I)
    sc = re.sub(r'</td>', '</td>', sc, count=0, flags=re.I)
    sc = re.sub(r'</th>', '</td>', sc, count=0, flags=re.I)
    sc = re.sub('<tbody.*?>', '', sc, count=0, flags=re.I)
    sc = re.sub(r'</tbody>', '', sc, count=0, flags=re.I)
    sc = sc.replace('&nbsp;', ' ')
    sc = re.sub(' +', ' ', sc, count=0, flags=re.I)
    return sc


def get_col(regex, df, index=None, error=True):
    """
    匹配列索引
    :param regex:
    :param index:
    :return:
    """
    regex = re.compile(regex)
    if isinstance(df, pd.DataFrame):
        for i in df.columns:
            if regex.search(i):
                return df.loc[index, i]
        else:
            if error:
                raise MyExcelException("未匹配到列索引,匹配项为：%s\n列索引为：%s" % (regex, str(df.columns)))
            else:
                return ''
    elif isinstance(df, dict):
        for i in df.keys():
            if regex.search(i):
                return df[i]
        else:
            if error:
                raise MyExcelException("未匹配到列索引,匹配项为：%s\n列索引为：%s" % (regex, str(df.keys())))
            else:
                return ''


def read_doc_table(path, axis=0):
    """
    读取doc文件中的表格
    axis=1按列索引读取
    axis=0按行索引读取
    :param path:
    :param axis:
    :return:dict
    """
    regex = re.compile('.*?识别[号]?.*|.*?代码.*|.*?行政相对人.*|.*?名称|.*?号')
    if 'linux' in sys.platform:
        outdir = '/'.join(path.split('/')[:-1])
        output = subprocess.check_output(
            ["/usr/bin/libreoffice6.3", "--headless", "--invisible", "--convert-to", "docx", path, "--outdir", outdir])
        file = Document(path + 'x')
    else:
        pythoncom.CoInitialize()
        word = wc.Dispatch("Word.Application")
        doc = word.Documents.Open(path)
        newpath = path.replace("doc", 'docx')
        doc.SaveAs(newpath, 12)
        doc.Close()
        word.Quit()
        file = Document(newpath)
    for table in file.tables:
        if axis == 0:
            first_ls = []
            temp = 2
            rows = table.rows
            for index, row in enumerate(rows):  # 提取有用的列索引 table.rows：每一行
                for cell in row.cells:  # row.cells：每一行的所有单元格
                    if regex.search(cell.text):
                        break
                else:
                    continue
                for cur_cell in row.cells:
                    cur_cell_text = cur_cell.text
                    if cur_cell_text in first_ls:
                        cur_cell_text += str(temp)  # 存在相同的列索引用temp区分
                        temp += 1
                    first_ls.append(cur_cell_text)
                final_index = index
                break
            else:
                return []

            d = {}  # 提取所有行
            for row in rows[final_index + 1:]:
                cells = row.cells
                for i, v in enumerate(first_ls):
                    d[v.replace('\n', '').replace(' ', '')] = cells[i].text.replace('\n', '').replace('\u3000', '')
                count = 0  # 去除空行
                for v in d.values():
                    if not v:
                        count += 1
                if not count == len(first_ls):
                    yield d

        if axis == 1:
            d = {}
            for row in table.rows:
                cell_ls = row.cells
                d[cell_ls[0].text] = cell_ls[1].text
            yield d


def doc_file(path):
    """
    wps按行读取word文档
    :param path:
    :return:
    """
    newpath = path.replace('doc', 'docx')
    pythoncom.CoInitialize()
    try:
        wps = wc.Dispatch('kwps.application')
    except:
        wps = wc.Dispatch('wps.application')

    do = wps.Documents.Open(path)
    do.SaveAs(newpath, 12)
    do.Close()
    wps.Quit()
    document = Document(newpath)
    content = ""
    tables = document.tables
    content_li = []
    table1 = tables[1]
    for li in table1.rows:
        ge = li.cells
        for g in ge:
            if not g.text in content_li:
                content_li.append(g.text)
            else:
                continue
    for i in content_li:
        content += i
        content += '#'
    content = content.replace('\n', '#').replace('##', '#')
    company_li = re.findall(r'\w+公司|\w+煤矿|\w+床厂', content)
    new_li = []
    for index, val in enumerate(company_li):
        if index + 1 == len(company_li):
            a = r'(%s.*)#' % val
        else:
            a = r'(%s.*)#%s' % (val, company_li[index + 1])
        new_li.append(re.search(a, content).group(1))
    return new_li


def changemoney(money, flag=False):
    """
    金额转换
    :param money:
    :param flag:
    :return: float
    """
    if not money:
        return ''
    money = re.sub(r'\d{1,2}、', '', money)
    money = money.replace("，", '').replace(",", '').replace('\r', '').replace('\t', '').replace('\n', '') \
        .replace('&nbsp;', '').replace(' ', '').replace('。', '')
    money = re.match(r'[^\d]*(\d+[\.]*\d*[\(\)（）万元%]*)', money).group(1) if re.match(r'[^\d]*(\d+[\.]*\d*[\(\)（）万元]*)',
                                                                                     money) else ''
    if not money:
        return ''
    if "万" in money:
        money = re.search("([0-9]+\.*[0-9]*)", money)
        if not money:
            return ''
        else:
            return float('%.2f' % (float(money.group(1)) * 10000))
    elif "%" in money:
        return ''
    elif flag:
        return float('%.2f' % (float(money) * 10000))
    else:
        money = re.search("([0-9]+\.*[0-9]*)", money)
        if not money:
            return ''
        else:
            return float('%.2f' % (float(money.group(1))))


def dealcaption(img_banary):
    """
    识别简单验证码
    :param img_banary:
    :return: str
    """

    f = BytesIO(img_banary)

    Images = Image.open(f)
    a = Images.convert('L')
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    out = a.point(table, '1')
    text = pytesseract.image_to_string(out)

    return text


class Captcha:
    def __init__(self, img_banary):
        self.t2val = {}
        self.img = BytesIO(img_banary)

    def twoValue(self, image, G):
        for y in range(0, image.size[1]):
            for x in range(0, image.size[0]):
                g = image.getpixel((x, y))
                if g > G:
                    self.t2val[(x, y)] = 1
                else:
                    self.t2val[(x, y)] = 0

    def clearNoise(self, image, N, Z):
        """根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
            G: Integer 图像二值化阀值
            N: Integer 降噪率 0 <N <8
            Z: Integer 降噪次数
            输出
            0：降噪成功
            1：降噪失败"""
        for i in range(0, Z):
            self.t2val[(0, 0)] = 1
            self.t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

            for x in range(1, image.size[0] - 1):
                for y in range(1, image.size[1] - 1):
                    nearDots = 0
                    L = self.t2val[(x, y)]
                    if L == self.t2val[(x - 1, y - 1)]:
                        nearDots += 1
                    if L == self.t2val[(x - 1, y)]:
                        nearDots += 1
                    if L == self.t2val[(x - 1, y + 1)]:
                        nearDots += 1
                    if L == self.t2val[(x, y - 1)]:
                        nearDots += 1
                    if L == self.t2val[(x, y + 1)]:
                        nearDots += 1
                    if L == self.t2val[(x + 1, y - 1)]:
                        nearDots += 1
                    if L == self.t2val[(x + 1, y)]:
                        nearDots += 1
                    if L == self.t2val[(x + 1, y + 1)]:
                        nearDots += 1

                    if nearDots < N:
                        self.t2val[(x, y)] = 1

    def get_cha(self):
        image = Image.open(self.img).convert("L")
        self.twoValue(image, 100)
        self.clearNoise(image, 3, 2)
        text = pytesseract.image_to_string(image)

        return text


class ExcelReader:
    """
    处理表格
    """

    def __init__(self, file_path, sheet, dtype=str, regex=None, file_type='excel'):
        self.flag = 0
        self.file_path = file_path
        self.dtype = dtype
        if regex is None:
            regex = '.*?识别[号]?.*|.*?代码.*|.*?行政相对人.*|.*?名称'
        self.regex = regex
        if file_type == 'excel':
            try:
                self.df = self.deal_excel_df(sheet)
            except xlrd.biffh.XLRDError as e:
                if "found b'<html xm'" in e.args[0]:
                    self.df = self.deal_html_df(sheet)
                else:
                    raise e
        elif file_type == 'html':
            self.df = self.deal_html_df(sheet)
        else:
            raise MyExcelException("文件类型未知错误")
        self.shape = self.df.shape
        self.columns = self.df.columns

    def deal_excel_df(self, sheet):
        df = pd.read_excel(self.file_path, header=self.flag, sheet_name=sheet).dropna(how='all').fillna('').astype(
            self.dtype).reset_index(drop=True)
        print("表格shape：%s" % str(df.shape))
        col = df.columns
        index = df.index
        while '1' not in list(
                map(lambda x: '1' if re.search(self.regex, str(x)) and not re.search('公告', str(x)) else '0', col)
        ) and self.flag < len(index):
            # 获取目标列索引
            col = df.loc[self.flag]
            self.flag += 1
        if self.flag == len(index):
            return pd.DataFrame()
        df = df.loc[self.flag:].reset_index(drop=True)
        df.columns = col.str.strip().str.replace('\r', '').str.replace('\t', '').str.replace('\n', '').str. \
            replace(' ', '')
        return df

    def deal_html_df(self, df):
        # df_li = pd.read_html(self.file_path, header=self.flag)
        # for df in df_li:
        df = df.dropna(how='all').fillna('').astype(self.dtype)
        print("表格shape：%s" % str(df.shape))
        col = df.columns
        index = df.index
        while '1' not in list(
                map(lambda x: '1' if re.search(self.regex, str(x)) and not re.search('公告', str(x)) else '0', col)
        ) and self.flag < len(index):
            # 获取目标列索引
            col = df.loc[self.flag]
            self.flag += 1
        if self.flag == len(index):
            return pd.DataFrame()
        df = df.loc[self.flag:].reset_index(drop=True)
        df.columns = col.str.strip().str.replace('\r', '').str.replace('\t', '').str.replace('\n', '').str. \
            replace(' ', '')
        return df

    def read(self, index, col_regex, error=True):
        # 在每一个sheet的df中匹配列索引,读取每一行
        flag = True
        regex = re.compile(col_regex)
        for i in self.df.columns:
            if regex.search(i):
                flag = False
                if isinstance(self.df.loc[index, i], pd.Series):
                    for j in self.df.loc[index, i]:
                        if j:
                            return j
                    else:
                        return ''
                else:
                    if self.df.loc[index, i]:
                        return self.df.loc[index, i]
        else:
            if flag and error:
                raise MyExcelException("未匹配到列索引,匹配项为：%s\n列索引为：%s" % (col_regex, str(self.df.columns)))
            else:
                return ''

    def read2(self, index, col_regex, error=True):
        # 存在多个纳税人识别号，取出存在的目标值
        regex = re.compile(col_regex)
        ids = set(map(lambda x: x if regex.search(x) else '', self.df.columns))
        ids.remove('')
        for col in ids:
            dest_data = self.df.loc[index, col]
            if dest_data:
                return dest_data
        else:
            if error:
                print("列索引为：%s" % str(self.df.columns))
                raise MyExcelException("未匹配到列索引,匹配项为：%s" % col_regex)
            else:
                return ''
