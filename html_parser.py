from lxml import etree


class HTMLParser:  # HTML解析类
    def __init__(self):
        pass

    # 返回豆瓣电影Top250页面特定序号的电影的相关数据
    def parse(self, html, number):
        movie = {"title": "", "actors": "", "classification": "", "score": "", "quote": ""}
        selector = etree.HTML(html)
        movie["title"] = selector.xpath(
            '//*[@id="content"]/div/div[1]/ol/li[' + str(number) + ']/div/div[2]/div[1]/a/span[1]/text()')[0]
        movie["actors"] = selector.xpath(
            '//*[@id="content"]/div/div[1]/ol/li[' + str(number) + ']/div/div[2]/div[2]/p[1]/text()[1]')[0]
        movie["classification"] = selector.xpath(
            '//*[@id="content"]/div/div[1]/ol/li[' + str(number) + ']/div/div[2]/div[2]/p[1]/text()[2]')[0]
        movie["score"] = selector.xpath(
            '//*[@id="content"]/div/div[1]/ol/li[' + str(number) + ']/div/div[2]/div[2]/div/span[2]/text()')[0]
        # 如果存在则为该值，否则为空
        movie["quote"] = selector.xpath(
            '//*[@id="content"]/div/div[1]/ol/li[' + str(number) + ']/div/div[2]/div[2]/p[2]/span/text()')[0] if len(
            selector.xpath('//*[@id="content"]/div/div[1]/ol/li[' + str(
                number) + ']/div/div[2]/div[2]/p[2]/span/text()')) > 0 else ""
        return movie
