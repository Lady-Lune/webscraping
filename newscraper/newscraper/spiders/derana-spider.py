import scrapy


class NewSpider(scrapy.Spider):
    name = "derana"
    allowed_domains = ["www.adaderana.lk"]
    archive_url = "https://www.adaderana.lk/news_archive.php?srcRslt=1"
    header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:148.0) Gecko/20100101 Firefox/148.0"
        }


    def __init__(self, category=None, year=None, month=None, day=None,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = {}  
        self.arg_category = [x.strip() for x in category.split(",")] if category else None
        self.arg_year = [x.strip() for x in year.split(",")] if year else None
        self.arg_month = [x.strip().zfill(2) for x in month.split(",")] if month else None
        self.arg_day = [x.strip() for x in day.split(",")] if day else None


    async def start(self):
        self.logger.info("Starting spider with category=%s, year=%s, month=%s, day=%s", self.arg_category, self.arg_year, self.arg_month, self.arg_day) 
        yield scrapy.FormRequest(
            url=self.archive_url,
            headers=self.header,
            formdata={
                "srcCategory": "999",
                "srcYear": "2006",
                "srcMonth": "01",
                "srcDay": "999",
                "Submit": "Search",
            },
            callback=self.parse_options,
        )

    def parse_options(self, response):
        titles = response.xpath("//div[@class='form-group']/label/text()").getall()
        groups = response.xpath("//div[@class='form-group']")
        self.options = {
            titles[0].strip(): self._get_opt_data(groups[0]),
            titles[1].strip(): self._get_opt_data(groups[1]),
            titles[2].strip(): self._get_opt_data(groups[2]),
            titles[3].strip(): self._get_opt_data(groups[3]),
        }

        self.logger.info("Options: %s", self.options)
        yield from self.manage_options(category_arg=self.arg_category, year_arg=self.arg_year, month_arg=self.arg_month, day_arg=self.arg_day)

    def _get_opt_data(self, group):
        data = {}
        values = group.xpath(".//option/@value").getall()
        names = group.xpath(".//option/text()").getall()
        
        if group.xpath(".//select/@id").get() == "srcYear":
            names = [name.strip() for name in names]
            values = names

        
        for value, name in zip(values, names):
            data[value] = name
            
        return data
    
    def manage_options(self,category_arg=None, year_arg=None,month_arg=None,day_arg=None):
        option_name = list(self.options.keys())  # category, year, month, day

        categories = list(self.options[option_name[0]].keys())
        categories.remove("999")  # Remove the "All" option for categories
        years = list(self.options[option_name[1]].keys())
        months = list(self.options[option_name[2]].keys())
        
        days = list(self.options[option_name[3]].keys())
        days.remove("999")  # Remove the "All" option for days
        
        category_opts = category_arg if category_arg else categories
        year_opts = year_arg if year_arg else years
        month_opts = month_arg if month_arg else months
        day_opts = day_arg if day_arg else days

        # c = category_opts.index(category) if category in category_opts else 0
        # y = year_opts.index(year) if year in year_opts else 0
        # m = month_opts.index(month) if month in month_opts else 0
        # d = day_opts.index(day) if day in day_opts else 0

        for category in category_opts:
            for year in year_opts:
                for month in month_opts:
                    for day in day_opts:
                        self.logger.info("Submitting search with category=%s, year=%s, month=%s, day=%s", category, year, month, day)
                        yield scrapy.FormRequest(
                            url=self.archive_url,
                            headers=self.header,
                                formdata={
                                    "srcCategory": category.strip(),
                                    "srcYear": year.strip(),
                                    "srcMonth": month.strip(),
                                    "srcDay": day.strip(),
                                    "Submit": "Search",
                                },
                                callback=self.parse_headlines,
                                cb_kwargs={                            
                                    "category": self.options[option_name[0]].get(category, "Unknown"),
                                    "year": self.options[option_name[1]].get(year, "Unknown"),
                                    "month": self.options[option_name[2]].get(month, "Unknown"),
                                    "day": self.options[option_name[3]].get(day, "Unknown"),
                                }
                            )

    def parse_headlines(self, response, **kwargs):
        news_div = response.xpath("//div[@class='news-story']")
        self.logger.info(f"Found {len(news_div)} stories for {kwargs.get('category')}, {kwargs.get('year')}-{kwargs.get('month')}-{kwargs.get('day')}")

        if len(news_div) != 0:
            for news in news_div:
                headline = news.xpath(".//div[@class='story-text']/h2/a/text()").get()
                desc = news.xpath(".//div[@class='story-text']/p/text()").get()
                url = news.xpath(".//div[@class='story-text']/h2/a/@href").get()
                pub_time = news.xpath(".//div[@class='story-text']/div[@class='comments pull-right']/span/text()").get()
                yield {
                    "headline": headline.strip() if headline else None,
                    "desc": desc.strip() if desc else None,
                    "url": url if url else None,
                    "published_datetime": pub_time.strip() if pub_time else None,
                    "category": kwargs.get("category", "Unknown"),
                    "year": kwargs.get("year", "Unknown"),
                    "month": kwargs.get("month", "Unknown"),
                    "day": kwargs.get("day", "Unknown"),
                }
