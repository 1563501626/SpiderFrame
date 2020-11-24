# encoding = uft-8
"""
@ File   :  AES_enc.py
@ Author :  Eamonn
@ Data   :  2019/10/28
"""

"""
aes加密算法
padding : PKCS7
"""
from Crypto.Cipher import AES
import base64

class AESUtil(object):
    def __init__(self):
        self.key="uA4x6790@23_56a@"
        self.iv="uA4x6790@23_56a@"
        self.bs = 16
        self.PADDING = lambda s: s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    __BLOCK_SIZE_16 = BLOCK_SIZE_16 = AES.block_size
    def encryt(self,data):
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_CBC,self.iv.encode("utf8"))
        x = AESUtil.__BLOCK_SIZE_16 - (len(data) % AESUtil.__BLOCK_SIZE_16)
        # print(x)
        if x != 0:
            data = data + ""*x
            # print(data)
        msg = cipher.encrypt(data.encode("utf8"))
        # msg = base64.urlsafe_b64encode(msg).replace(‘=‘, ‘‘)
        msg = base64.b64encode(msg)

        return msg

    def decrypt(self,enStr):
        cipher = AES.new(self.key.encode("utf8"), AES.MODE_CBC, self.iv.encode("utf8"))
        # enStr += (len(enStr) % 4)*"="
        # decryptByts = base64.urlsafe_b64decode(enStr)
        decryptByts = base64.b64decode(enStr)
        msg = cipher.decrypt(decryptByts)
        paddingLen = msg[len(msg)-1]
        return msg[0:-paddingLen]

    def encrypt_24(self, text):
        generator = AES.new(self.key.encode("utf8"), AES.MODE_CBC, self.key.encode("utf8"))  # 这里的key 和IV 一样 ，可以按照自己的值定义
        crypt = generator.encrypt(self.PADDING(text).encode("utf8"))
        crypted_str = base64.b64encode(crypt)   #输出Base64
        return crypted_str



if __name__ == '__main__':
    body = "_opType=getPageData_lt&_fromSite=1&tk=nnTL/8-ec/1sqj-ec/1SP7uMHT8teS7Tsw5qrbd1sWfKGTfpOy0-ec/2&_lstID=enterpriseLib_Box&_xml=../../MHWeb/enterpriseLib/LstXml/enterprise_List.xml&_auvOpType=&_urlParam=&_pageIndex=5&_pageSize=40&_sortCol=0&_baseCondition="
    enc = AESUtil()
    res = str(enc.encrypt_24(body), encoding="utf-8").replace("+", "{$EC000}")
    print(res)


# _opType=getPageData_lt&_fromSite=1&tk=nnTL/8-ec/1sqj-ec/1SP7uMHT8teS7Tsw5qrbd1sWfKGTfpOy0-ec/2&_lstID=enterpriseLib_Box&_xml=../../MHWeb/enterpriseLib/LstXml/enterprise_List.xml&_auvOpType=&_urlParam=&_pageIndex=5&_pageSize=40&_sortCol=0&_baseCondition=
# pJBVSuzDA4iAT1kA5cdvCTLEqcFfv6nUL9+fchh0IzTBiM73ZjWqRazMcDogQROTB9vzGazpqgvFwyZ83MAvzOv6mvPvDfM3qWe8f61QR7p1FdIH5HSAw9R8HnvZ7tNdnDJug4H4hNyhzoCsN5jSHojrV1wOK6nraUZ3b6tYyc6qsGWq+qUo+BRYOO+Lj5SY0RVzgKikoj7RD+NV/+yU8v33XAy3APXArhPQKHx1XNTOd4neP8iyTJMWlFQCb09qeRbSXP1LCYJrroBPrhZoL00b/E2z/9cv90YsU0R8qaX3VhwVudJfIwqN9+nMerst+WMmySKZ+lQdL3DMrjSLbg==

# pJBVSuzDA4iAT1kA5cdvCTLEqcFfv6nUL9{$EC000}fchh0IzTBiM73ZjWqRazMcDogQROTB9vzGazpqgvFwyZ83MAvzOv6mvPvDfM3qWe8f61QR7p1FdIH5HSAw9R8HnvZ7tNdnDJug4H4hNyhzoCsN5jSHojrV1wOK6nraUZ3b6tYyc6qsGWq{$EC000}qUo{$EC000}BRYOO{$EC000}Lj5SY0RVzgKikoj7RD{$EC000}NV/{$EC000}yU8v33XAy3APXArhPQKHx1XNTOd4neP8iyTJMWlFQCb09qeRbSXP1LCYJrroBPrhZoL00b/E2z/9cv90YsU0R8qaX3VhwVudJfIwqN9{$EC000}nMerst{$EC000}WMmySKZ{$EC000}lQdL3DMrjSLbg: =