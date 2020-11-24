# -*- coding: utf-8 -*-
import time
import scrapy
from spider_code.confs import getConfig
from spider_code.items import CreditItem
import re
from fuclib import ezfuc

# configuration item
gConfig = getConfig.get_config()


import manager
class Spider(manager.Spider):
    name = 'X--12'
    start_urls = [
        'http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2']
    download_delay = 1.0
    page = 1
    filter_data = True
    filter_db = 'duplicate_key'
    filter_table = 'credit_x__12'
    first_data = {'ScriptManager1': 'ScriptManager1|btnLook', '__EVENTTARGET': '', '__EVENTARGUMENT': '',
                  '__VIEWSTATE': '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',
                  '__EVENTVALIDATION': 'on1JnMD0AZKp/5iy9kMDe+7Hst2mMWFPDHcB8uxlHyCHZmkGyS+kjucUuog3CQcctsm11o0cB5/NGB0KRJ18UA==',
                  'txt_lb': 'sg_fj', 'txt_key': '', 'AspNetPager_XWList_input': '1', 'AspNetPager_XWList2_input': '1',
                  'AspNetPager_XWList3_input': '1', 'AspNetPager_XWList4_input': '1', '__ASYNCPOST': 'true',
                  'btnLook': ''}
    data = {'ScriptManager1': 'UpdatePanel4|AspNetPager_XWList2', 'txt_lb': 'sg_fj', 'txt_key': '',
            'AspNetPager_XWList_input': '1', 'AspNetPager_XWList2_input': '1', 'AspNetPager_XWList3_input': '1',
            'AspNetPager_XWList4_input': '1',
            '__VIEWSTATE': 'HGQ6TSHT+ziFMc+pp4kITN2Rb/dq3tHKik7A5+YwTnakzknY7P+9VPgZDHrP6NFquuHrm9kw0MEKWso1Xva0L+ilXjCBAVlkL3EymY3cdGfW3yDgQDLJtJeV2oDcZKcYmgqBnzPnSEivVj/cf0emUbsNIAgt/avE5X5HpzXv0t9nwfpty2kCf2uS2lIwzROU2NLGnM+tHw2kW8XBJz/1QGoLkgcwbglW2b8y8V1KiThYJOsXe+ynJi3pLqQXchyzxC9Y/5VawyXphgCfQuf27EaeU+QS17uklqdjp4HI1LEkk7eUWe+T8ao9SboEbIpXjyftLbAGYBZ/fGzY2bs63KaSsqC8yPEbVIh930CWKxG1vgUFDEj3gMtO8zaut4W9zJNju64vppnaXVUS/BXucTkpUD6w2a6hLr3ryEyPVkeJUPeNMEpiwiA5jzOyza8MAzLgM77v1cm4OwtPWe19Q66y8F9TCo283iExihH55tQXfISsSocDfCDbUhftwxczkPYBwgyzpSyd8rJ6SdUU1pXzoyHa+fmut5QSagRiM3mr9q5Rpkj7uxfqo4CfqQ9BRtRCS0z94qMtqN9LYJojr+/eRB7rJWH/qq4hMjfT+WUXObwaNUTpLkyfvVBaDiWuxWG6pdgaYILvAT2GQLCfRNWHHhPM6I18UZLIZFk+fdJl03vEirCUC/cndNBxz6ay6LkSsPygK25HGfdUzIZFJ5DeJxTDTkWJb+OPgzXTJtponEBDt6C2if4Usk9HrpBNTL0IZPGcrCROx966bxcXuxHsVhKHgUJ0nUJzMSa9h4pKU97gpncS613GFe955Pmx8vTgjDd6jJ78mqa6Qutxq0WcFlzWtLC7NlHYZcn8PH1gkVwVtSaHy+HpkaA5F78CzaLmxrWcKsndzXQ3cXsualFT8Co77Mxv9oCuIllJjmZID1B/HKQ8t9Am88L8N1nUMJjzqclS/NowK9MsjifWZTmBlkGn5+aGcFWRTdGWYQu5k2Kv0LenNbUlqOA1A6ABzN+VWgptZjN3DLoYAecUpQtxofwe9ZU2sL18fEJtzTEGBex8wV3CDXZNr5y9gVXinfY87Fb3SStfCxhatD43Hqh8lquI7GE5+d9pRa9nyAN5j++pN+WeNHNRwzIR7TuHhk3RsEpJfH4F6gSIsgAABJWtMTKKCSUIIDjovHy2MlLI63+vxjQKxKmXzVr6/lkWKq2Y3aKlOC6ePHKPCjRPhFn2CIIGtzDgXXrWhfL/35gkueRXdmwus/CUYXidDZw9YrIb6He6wxrKgB56uAa5LB1qztsSdcd6OMFKNVft4/7vxPC4AF5cwQCAjil8SbG7Ibfqya847MzoaZd9lxNxeAMJtWiUeHxu34Zf82SqM+KXnIqerrGYQfqiuQ2O/sIjJvlEYWBokIftoQxjvPP/tBJzS3SkzQ/umvJhvke2nL/l0kRGiBDWTMqk716fvN27QbWFN+ACisRdvv8fmTGq+o913yPHTqYeWRbY5KQzm0ZViuqKTNdSE492e5S01FvFhOHa+6ObVRGwpYEwJK8dvKqse3lC1197SBnQRjBh2EQGFR5kI5VP+jEpyiAgfd2UOHkBIw+Or0KKCG75O5LzlC/xg1I6cD00KoiYkijDweMMgl7Sa3yvJpTX+ClhZwcXfuWqxkVINaezeDXEC3x9KzbKLjUjwnb+7NaLQOgMBV80sT2fE3bvXMqvEnXFPqaE08T6y2hmcE4bNTMFErfpwWoBC/zG6n4KPgR8FCS5SCPrwll25Urai76aUx+jsbRH8Y0DY20+uEuOm/S+6iKSPmsfRwpwfypgvFSnbd2USD8S+eidCppQuSyD9A9K8nDhhEDHDda1lO1FQ7k/gPhcon1w2GCP9wx200gMKha845A8pd+MQYwGLHMfLAN0wv/APRENGJJqAzicZdwjUvlL3W2s+7pw9w1mEVx/C2U/n3NkZg7DQGEGAX0Q1nW3z3BVABmBmPJYbDyWfOS9hpyZlGxq0p/PjrL5h9hwM4Gn1KpO7V4RPBwT99ma//kpRq1AKVbUDsnbE11eCSrxZCwxpc72E40JHjTMdJDcIz+RWnxDmJLaZxvML04RDRRrsJJA+VIkhyB97BtDLSaMzFwHaUSswcPvORxAtXa0DA19Vptp6aGcVVs/7XGKTwkSj2xLXgNcZMkw+9JqNyWjmgOVx21tOt1oL3d9swfP4alV1qPJlgmiLiVrzDz60t//sVm8+oHwiQweS5+RC5Rt+mXSLXgclZN3+gYaoXhCxd2AKo97OoEvzID6DgySdRZJIU/QP0Pf7Po8oI5xkE+3TM5POaeBOtASHlH9itmcHKmxyn5Vb/GXNmXztE59gRYTi/vRWNP/Snup5ORnVTint/bqzvIZ3EgVFsHTHkuT444AWWv7xLKtWARIbmwiuaUSGFum0ceOJe5qv3LdTbO+sToF4C5UXPd88Z55jdNa/aiFpmqNV66JxO6CjB5wMFdTDlP4K75Oink6hQmTbI72YhOXYvIIDOQS+e+Z+ebMqR1yRcyMOvJ4JprIt7ZqsbvhS2nqMQYrWhfcrp/UgFfbHNHsZGUrNlAmBXGxLX2khJ92+p5irCvQ4XIM0orRLVZM60PTGRaS7QY4iUfCCoNqsjTsbV+qJNnSooZdlaYg1yKCtfMbE6yFHL9SSFv1DgRGvZPlt8P443CJYMqmuZRdJ36/NdWuPQLs+8I3qb+oR+8P4Oz2Xjb4cpMzACofzT1fYUoXZ+GcZ36CmYL3cUd246ceYvKJ//PUcwpiMoAPPySpPJ37ApU/vTcH3HYoy2cynHDvQJDUZ3Ke05bUZqQgpWGDZZbWp0XUUgFZ4PxsdbJnRD54mrE4QpeOLJkCiykmrlZZpfZQyB796uAy2gmz+1rQ6OlnTUgaROAjlkWJ43qS5LgEwVzdE/LSe9jVE0ehHXyOeu2dLHlex7JDUWwpCceQFpo00FpgD31Z/xsyf+9gIdiRTKyxrwJycZMDkXwgW3BBsqQ9yw1se+VBzDuEqMXGv9YgvBzeFHE0m06uHWjJGxaugcf20EDceiRTm187V80j7zbPZCAthzD2BEq/lO/n4eUWTSj5ap5c2wT0JNDpyn8LmE2+mv6UWQ7CNLdG2E29pPw1mSefWQFXnK4XvYSLo4Ts7f5/yDazoBPGk52mPSMWT0/jPFKxg7Yy+CE0jfnAJre3G4Jd8yVZ4F0O2zQR0t8V9xHvmZeF2A5SdvSU+xMyMlw0w+hb0sCFIpFEcZm+qi1LtMNZ5fNcHxpoDSnqV5wvKClwPM+ZBvRKV7QfQn3IY8BEK6j/xF5Akzd8MD9GeU998HFYXrNFWQA1EteTogxP1c1kavgMCTidPIvxLF0KWPwrqMUHpO+hYgSyMMKwUNPHwwTJWb++inEN85Q/zd1KwjapsKwIZtBLkecu00PWFHbRycfo6Y50A/v354wSgNrAbC0UuQYx8H/HPrXotNXfAMJPzwE6KIByW47RMY+T8nDISZDy/5jW7WRTnyIwPuzvKz2q7VEMIGMpAKbbOLeaNQQlTgEISuAsQiI48Z1GISDzFcJDgJSRjpyzUdxRm1gJu3jTNJFjdVM9VYT58ijwqlwU17loQy4Pnj6JFEJ1tuBn+w0mIYAZ7iaQh09mSo/E6NmHk6kAG5GwiKLA1OQ7KlIZlWzva/kYrjhgNPEQkP6h7vnsGe7IKO25yj/ZkCM/SD7EFGUwh6MfblOg96tIwaVoOJUejn7K3IBoJ4tm8GbKgdcKWnyolUFbCX/C2GWFHQ926ghWSd5Ok51BnyAUQErIR9fGQJvZr65kwHMKZxW3n5O6DIuTPhOmU9uvcx+JVQZWXaz+hsyxiZXSAqLJnU07d+2+I41D1SKU1KGnBk79s9Xo4RpN9I9DiVk3Dhh64wpXkl+TJmCu+dQnk38QV9iMX/V+QP0uQJf/jR4kEUmtLNL3MsbHO41YxZRG5oH85vHb2mi3HxiTKiHgjpRAGnyenqCMhJL0AXN0RAF94fm0ewm3vhZErZ9ipvK5Grl+eZ4vKJxdV98VfmXCOFqkicQYm5hCKg2CP4uFkhS2453aUC+MkkJfGCNsB5T0BeSms4s0WdAPAWwvROBffBBLc6RTUO+u7I6v8EGmaETJ+uf/C3AwET9Lr0Rusk8rEPtnTWKaH3u3jNQli7R+K7g4RxAJsNBwYOD4oZi0BNfCOS7U0sSYgs515N1/S4rbbnHujfsXQqO1vnKnnb9K5+uuMe+WSYiWA02X8kQ6M5BzyRcDn5+Jprv9q54C3hZvr57K/V9eEwcWQDyvm0MpGQnLhWdr9YT1BkNyXFQ+LIOV5O1V2UWDSU11AjdjmePxcwI4Iow/JoU6Pra2n6M9gvuh18qrG3AR7c9TsQseKBlhmcRWCnTbZaGV5tICOTgDtuEhbVkkg5A36fWSgqfKW5K5QUj1VfjkB/5fUIvaI2KJ6KVH/epAFDGGLNb9ee0m7Ag4LSeOGW5xB58HGWs6JwiCHK9pXL2pyyOrQLhxlaisrhoN7n7BqGp1AwOimx03NwLpMR11MBCS8vc6UEgDUOoEcMYw5BPVhR1n79rloJNoS26Nl2v5DabGnhO6Mml26SOO3S4mRKckxYTYrhyYXfolBbm77LKf8N1bOmSL9yvXArnXrmziK1czAWujO1GdbxbuR59xOJ8Z2cbOELj5WG+CZcrQNiyxkPQL6+2B+QKUEJTjPu4SfUYa0JkTlVp2TB5CQYlnMVWu0LlWp/PZt0gp63kTGnSgKIkAfiJo+IkTYXxQmnuwHP1HDO5NX/rcjczQ92WC6eqbFW+JnMCZsn/qNMt3Efv5x0DkrFqAETV6/LZV6cs/s8lJyAi25AHOKLvRrFYhvgy0iZuoK/GsMyxow3wDMQmcIP2cE8t5BT9JOSVRYVAAzbk/4i6jOKXBsPkrIRt/TdvWSWkSKLl4iPk3TAL8iDCopkMVrqXWj0yYUSecVdfQsLGn5OaqvqOcf/BVqnIBSmQxyKEuJwf1Wmu6fEUEz7MDuh0vcvLJoU/LndUN6FFJbag+5BYXGm1iaLFyeJ9/IqsnEJ2fN1162Jm5L+hf38HWR3Ieyl06gtE=',
            '__EVENTTARGET': 'AspNetPager_XWList2', '__EVENTARGUMENT': '2',
            '__EVENTVALIDATION': 'gRRbrsFTic4+kMkuzX2Qd0ty8BqCgqVK/hO0+R5LTMStModzbNhS68dnAh2z3L1E0q3x2j++25F6gHonUOOIhw==',
            '__ASYNCPOST': 'true'}
    headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
               'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Host': 'cbs.chengdu.com.cn',
               'Origin': 'http://cbs.chengdu.com.cn', 'Referer': 'http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
               'X-MicrosoftAjax': 'Delta=true', 'X-Requested-With': 'XMLHttpRequest'}
    total = 0
    count = 0

    def parse(self, response):
        url = "http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2"
        self.first_data['__VIEWSTATE'] = response.xpath("//input[@id='__VIEWSTATE']/@value").extract_first()
        self.first_data['__EVENTVALIDATION'] = response.xpath("//input[@id='__EVENTVALIDATION']/@value").extract_first()
        yield scrapy.FormRequest(
            url=url,
            formdata=self.first_data,
            dont_filter=True,
            callback=self.parse_detail,
            meta={'page': self.page},
            headers=self.headers
        )

    def parse_detail(self, response):
        url = "http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2"
        endpage = response.xpath("//a[text()='尾页']/@href").extract_first()
        if not self.total:
            self.total = int(endpage.split(",")[-1].split("'")[1])
        self.data['__VIEWSTATE'] = re.search(r"__VIEWSTATE\|(.*?)\|", response.text).group(1)
        self.data['__EVENTVALIDATION'] = re.search(r"__EVENTVALIDATION\|(.*?)\|", response.text).group(1)
        self.data['__EVENTARGUMENT'] = str(self.page)
        if self.page <= self.total:
            yield scrapy.FormRequest(
                url=url,
                formdata=self.data,
                dont_filter=True,
                callback=self.parse_detail,
                meta={'page': self.page},
                headers=self.headers
            )
            current_page = response.xpath("//div[@id='AspNetPager_XWList2']//span/text()").extract_first()
            if (self.page == 1 and response.xpath("//a[not(@href)]/../../div[@class='cell cell_2']/..")) or \
                    (current_page and int(current_page) != 1):
                self.page += 1
                lis = response.xpath("//a[not(@href)]/../../div[@class='cell cell_2']/..")
                for i in lis:
                    item = CreditItem()
                    item["企业名称"] = i.xpath("./div[1]/a/text()").extract_first().strip()
                    item["排名"] = i.xpath("./div[3]/text()").extract_first().strip()
                    item["今日得分"] = i.xpath("./div[4]/text()").extract_first().strip()
                    item["六十日得分"] = i.xpath("./div[5]/text()").extract_first().strip()
                    item["网站维护代码"] = self.name
                    item["省"] = "四川"
                    item["市"] = "成都"
                    item["网站名称"] = "成都市工程建设招标投标从业单位信用信息平台"
                    item['url'] = "http://cbs.chengdu.com.cn/Web/XYGSList.aspx?xh=xh2"
                    today = time.strftime("%F")
                    item['md5'] = ezfuc.md5(item["企业名称"], item["排名"], item["今日得分"], item["六十日得分"], today)
                    yield item
                    # print(item)


if __name__ == '__main__':
    from manager import run
    run(['Credit', 'X--12', 'w', 1])
