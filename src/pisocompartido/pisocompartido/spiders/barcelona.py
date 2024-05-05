import scrapy


class BarcelonaSpider(scrapy.Spider):
    name = "barcelona"
    allowed_domains = ["www.pisocompartido.com"]
    start_urls = ["https://www.pisocompartido.com/habitaciones-barcelona/"]

    def parse(self, response):
        # This function will start extracting cards and our main link of interest
        cards = response.xpath('//div[@class=" card"]') # Extracting cards

        # loop through all the cards to get the link where all details are and will be extracted
        for card in cards:
            link = card.css('a::attr(href)').re_first('.*/habitacion/.*')
            
            # If the link is not empty, we will follow it
            if link is not None:
                yield response.follow(link, callback=self.parse_details)
    
        # We take in count pagination. if exist a next page, we will follow it too
        next_page = response.css('li.pag-next a::attr(href)').get()
        if next_page is not None:
            # if exists, this function will be called again
            yield response.follow(next_page, callback=self.parse)
    def parse_details(self, response):
        # Initialize all items with a default value
        title = price = address = description = room_info = flat_info = conditions = rules = lat = lon = None

        # Only extract the items if they exist
        if response.css('h1::text').get():
            title = response.css('h1::text').get()
        if response.css('span.price::text').get():
            price = response.css('span.price::text').get()
        if response.css('span.direccion::text').get():
            address = response.css('span.direccion::text').get()
        if response.css('span.descripcion::text').get():
            description = response.css('span.descripcion::text').get()
        if response.css('div#mapFluid::attr(data-lat)').get():
            lat, lon = response.css('div#mapFluid::attr(data-lat)').get().strip().split(',')

        sections = response.css('div.seccion')
        for section in sections:
            #print(section.css('h2.titulo::text').get())
            section_title = section.css('h2.titulo::text').get()

            if section_title:

                if 'sobre la habitaci' in section_title.lower():
                    room_info = section.css('li span::text').getall()
                elif 'sobre el piso' in section_title.lower():
                    flat_info = section.css('li span::text').getall()
                elif 'condiciones del alquiler' in section_title.lower():
                    conditions = section.css('li span::text').getall()
                elif 'normas de la casa' in section_title.lower():
                    rules = section.css('li span::text').getall()

        # We will return all the data in a dictionary
        yield {
            'title': title.lower().strip().replace('\t','').replace('\r','').replace('\n','').strip() if title else None,
            'price': price.lower().strip().replace('\t','').replace('\r','').replace('\n','').strip() if price else None,
            'address': address.lower().strip().replace('\t','').replace('\r','').replace('\n','').strip() if address else None,
            'lat': lat,
            'lon': lon,
            'description': description.lower().strip().replace('\t','').replace('\r','').replace('\n','').strip() if description else None,
            'room_info': [x.lower().strip().replace('\t','').replace('\r','') for x in room_info],
            'flat_info': [x.lower().strip().replace('\t','').replace('\r','') for x in flat_info],
            'conditions': [x.lower().strip().replace('\t','').replace('\r','') for x in conditions],
            'rules': [x.lower().strip().replace('\t','').replace('\r','') for x in rules]
        }