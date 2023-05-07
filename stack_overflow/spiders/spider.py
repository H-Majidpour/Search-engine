import scrapy
import json


class MySpider(scrapy.Spider):
    name = "stack_crawler"

    def start_requests(self):
        """
        Get the links you need to crawl.
        """
        url_list = []
        for i in range(0, 15):
            url_list.append("https://stackoverflow.com/questions?tab=newest&page="+ str(i+1))
        
        urls = []
        urls.append("https://stackoverflow.com/questions")
        for i in range(0, len(url_list)):
            urls.append(url_list[i])

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        """
        Get the required information from the pages.
        """
        link_list = response.xpath("//h3[@class='s-post-summary--content-title']/a/@href").extract()
        title_list = response.xpath("//h3[@class='s-post-summary--content-title']/a/text()").extract()
        content_list = response.xpath("//div[@class='s-post-summary--content-excerpt']/text()").extract()
        author_list = response.xpath("//a[@class='flex--item']/text()").extract()
        
        # Number of questions per page
        len_questions = len(link_list)
        tags_list = []
        for i in range(0, len_questions):
            str_tag = ""
            # Number of tags per question
            len_tag = len(response.xpath("/html/body/div[3]/div[2]/div[1]/div[3]/div["+ str(i+1) +"]/div[2]/div[2]/div[1]/ul/li/a"))
            for j in range(0, len_tag):
                # Get all tags for each question
                str_tag += response.xpath("/html/body/div[3]/div[2]/div[1]/div[3]/div["+ str(i+1) +"]/div[2]/div[2]/div[1]/ul/li["+ str(j+1) +"]/a/text()").extract()[0]
                str_tag += " , "
            tags_list.append(str_tag)
        
        
        data = {}
        for i in range(0, len(link_list)):
            data[link_list[i]] = ({
                'title': title_list[i],
                'content': content_list[i],
                'author': author_list[i],
                'tags': tags_list[i]
            })


        # with open('data.txt', '+a') as Fin:
        #     for dat, info in data.items():
        #         Fin.write("Link: " + dat.strip()
        #                   + "\nTitle: " + data[dat]["title"].strip()
        #                   + "\nContent: " + data[dat]["content"].strip()
        #                   + "\nAuthor: " + info["author"].strip()
        #                   + "\nTags: " + info["tags"].strip() 
        #                   + "\n\n\n\n"
        #                   )
        #     Fin.close()
                    
                    
        with open("data.json", 'a+') as Fin:
            json.dump(data, Fin)
            Fin.close()
