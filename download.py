from .sipder import JavBusSpider
from concurrent.futures import ThreadPoolExecutor
import os
import requests
from utils.settings import SAVE_PATH, PIC_PATH, EXCEL_PATH, USER_AGENT, MAX_WORKERS
import xlwt

jav_spider = JavBusSpider()
movie_info_list = jav_spider.main()

if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)

if not os.path.exists(PIC_PATH):
    os.mkdir(PIC_PATH)


class Download(object):
    """下载电影信息"""
    def __init__(self):
        self.headers = {"user-agent": USER_AGENT}
        self.executor = ThreadPoolExecutor(MAX_WORKERS)

    def get_pic(self, movie_dict):
        """下载封面图片到本地"""
        response = requests.get(movie_dict['pic_url'], headers=self.headers)
        data = response.content

        with open(PIC_PATH + "%s.jpg" % movie_dict['code'], "wb") as f:
            f.write(data)

    def threadpool_get_pic(self):
        with self.executor as pool:
            pool.map(self.get_pic, movie_info_list)

    def write_excel(self, movie_list):
        """写入Excel"""
        # 创建excel工作表
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet('sheet1')

        style = xlwt.XFStyle()  # 初始化样式
        al = xlwt.Alignment()
        al.horz = 0x02  # 居中对齐
        style.alignment = al

        # 设置表头
        worksheet.write(0, 0, label="标题")
        worksheet.write(0, 1, label="番号")
        worksheet.write(0, 2, label="时长")
        worksheet.write(0, 3, label="出版商")
        worksheet.write(0, 4, label="发行日期")
        worksheet.write(0, 5, label="类别")
        worksheet.write(0, 6, label="演员")
        worksheet.write(0, 7, label="封面链接")

        # 变量用来循环时控制写入单元格
        val1 = val2 = val3 = val4 = val5 = val6 = val7 = val8 = 1
        for movie_dict in movie_list:
            for key, value in movie_dict.items():
                if key == "title":
                    worksheet.write(val1, 0, value)
                    val1 += 1
                elif key == "code":
                    worksheet.write(val2, 1, value)
                    val2 += 1
                elif key == "length":
                    worksheet.write(val3, 2, value)
                    val3 += 1
                elif key == "producter":
                    worksheet.write(val4, 3, value)
                    val4 += 1
                elif key == "pub_date":
                    worksheet.write(val5, 4, value)
                    val5 += 1
                elif key == "category":
                    worksheet.write(val6, 5, value)
                    val6 += 1
                elif key == "actress":
                    worksheet.write(val7, 6, value)
                    val7 += 1
                elif key == "pic_url":
                    worksheet.write(val8, 7, value)
                    val8 += 1
                else:
                    pass

        workbook.save(EXCEL_PATH)


if __name__ == '__main__':
    download = Download()
    download.write_excel(movie_info_list)