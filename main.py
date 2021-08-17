import requests
import random
import time

from html_parser import HTMLParser
from excel_handler import ExcelHandler
from pyecharts import options as opts
from pyecharts.charts import Bar


def crawling():  # 爬取豆瓣电影Top250函数
    # 定义当前处理的excel表的行
    excelRow = 1
    # 实例化excel处理类
    excelHandler = ExcelHandler()
    # 开始处理excel
    excelHandler.startHandleExcel()
    # 在excel表中添加标题行
    excelHandler.handleExcel(excelRow, "名字", "演员", "分类", "评分", "引言")
    # 处理的行+1
    excelRow += 1

    # 定义豆瓣电影Top250页面的地址和所使用的user-agent(伪装为正常浏览器)
    url = "https://movie.douban.com/top250"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/89.0.4389.82 Safari/537.36"}
    # 实例化网页解析类
    htmlParser = HTMLParser()
    print("开始爬取豆瓣电影Top250...")
    # 爬取豆瓣电影Top250的十个网页
    for page in range(10):
        # 定义URL的参数
        param = {"start": page * 25, "filter": ""}
        # 发起GET请求
        response = requests.get(url=url, params=param, headers=headers).text
        # 将请求结果页的25个电影信息存入excel
        for list in range(25):
            print("正在处理" + str(page + 1) + "页的第" + str(list + 1) + "部电影...")
            # 解析电影的信息
            movie = htmlParser.parse(response, list + 1)
            # 将解析结果存入excel
            excelHandler.handleExcel(excelRow, movie["title"], movie["actors"], movie["classification"], movie["score"],
                                     movie["quote"])
            # 处理的行+1
            excelRow += 1
        print("第" + str(page + 1) + "页爬取完成！")
        # 等待5-20秒之后再次爬取，模拟人的操作
        time.sleep(random.randint(5, 20))
    # excel存入完成
    excelHandler.endHandleExcel("movies.xlsx")
    print("豆瓣电影Top250爬取完成！")


def getCharts():  # 绘制评分数据图函数
    # 定义评分的字典
    scoreLevel = {}
    # 实例化excel处理类
    excelHandler = ExcelHandler()
    # 开始读取excel表
    excelHandler.startReadExcel("movies.xlsx")
    print("开始读取excel表中的评分列...")
    # 循环遍历excel表评分列
    for row in range(250):
        # 从excel表中读取评分列作为字典的key
        key = excelHandler.readExcel("D" + str(row + 2))
        # 如果该key存在则+1
        if key in scoreLevel:
            scoreLevel[key] += 1
        # 否则初始化该key的值为1
        else:
            scoreLevel[key] = 1
    # 读取excel结束
    excelHandler.endReadExcel()

    # 定义一个列表表示scoreLevel字典所有的key(即评分)
    keys = []
    # 定义一个列表表示scoreLevel字典所有的value(即该评分的数量)
    values = []
    # 提取scoreLevel的key和value
    for key in scoreLevel:
        keys.append(key)
        values.append(scoreLevel[key])
    print("评分数据读取完成！")

    print("开始绘制评分数据图...")
    # 绘制柱状图
    c = (
        Bar()
            .add_xaxis(keys)
            .add_yaxis("评分：数量（部）", values)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="豆瓣电影评分Top250"),
            toolbox_opts=opts.ToolboxOpts(),
            legend_opts=opts.LegendOpts(is_show=False),
        )
            .render("movies_score.html")
    )
    print("评分数据图绘制完成！")


# 爬取豆瓣电影TOP250
crawling()

# 绘制评分数据图
getCharts()
