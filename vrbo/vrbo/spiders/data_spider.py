import scrapy
import re

from vrbo.items import VrboItem, ListingOverviewItem, OwnerItem, OwnerProfileItem, OwnerResponseItem, BlockItem, \
    FacilityItem, PropertyTypeItem, BedroomItem, BedroomDescItem, BathroomItem, ReviewItem, ReviewerDescItem, \
    rateForItem, ratesDateItem


class DataSpider(scrapy.Spider):
    name = "vrboSpider"
    start_urls=[]
    def __init__(self, pid=None, *args, **kwargs):
        super(DataSpider, self).__init__(*args, **kwargs)
        print pid
        self.start_urls.append('https://www.vrbo.com/'+pid)


    def parse(self, response):

        item = VrboItem()

        item['reviewUrl'] = ''.join(response.xpath('//*[@id="section-reviews"]/div/ul/@data-url').extract())

        if(item['reviewUrl']):
            review_urls = ['https://www.vrbo.com' + item['reviewUrl'] + '&page=1',
                        'https://www.vrbo.com' + item['reviewUrl'] + '&page=2',
                        'https://www.vrbo.com' + item['reviewUrl'] + '&page=3',
                        'https://www.vrbo.com' + item['reviewUrl'] + '&page=4',
                        'https://www.vrbo.com' + item['reviewUrl'] + '&page=5']

            for link in review_urls:
                request = scrapy.Request(link)
                yield request


        item['latitude'] = ''.join(response.xpath('//body/script[2]/text()').re("lat\:[0-9.]+"))


        item['longitude'] = ''.join(response.xpath('//body/script[2]/text()').re("lng\:[0-9.]+"))


        item['locationDescription'] = response.xpath('//*[@id="ownermap"]/p/text()').extract()


        item['image'] = response.xpath('//*[@id="media-photo-main"]/@src').extract()


        item['propertyTitle'] = ''.join(response.xpath('//*[@id="content"]/div/div[1]/h1/text()').extract()).strip()


        item['propertyDescription'] = ''.join(response.xpath('//*[@id="listing-bigtop"]/div[1]/p/text()').extract())


        item['imageList'] = []
        for imagedata in response.xpath('//*[@id="media-photos"]/div[2]/a'):
            item['imageList'].append(''.join(imagedata.xpath('img/@src').extract()))

        item['listingOverview'] = []
        for listdata in response.xpath('//*[@id="listing-overview"]/div/ul/li'):
            listitem = ListingOverviewItem()
            listitem['listingKey'] = ''.join(listdata.xpath('b/text()').extract())
            listitem['listingValue'] = ''.join(listdata.xpath('span/text()').extract())
            if (listitem['listingKey'] == "Minimum stay:"):
                listitem['listingValue'] = ''.join(
                    response.xpath('//*[@id="listing-overview"]/div/ul[1]/li/span/span/text()').extract())
            item['listingOverview'].append(listitem)


        blockitem = BlockItem()
        for blockdata in response.xpath('//*[@id="listing-bigtop"]/div[2]/div'):
            blockitem['title'] = ''.join(blockdata.xpath('h2/text()').extract())
            blockitem['footerText'] = ''.join(blockdata.xpath('p/text()').extract()).strip()
            blockitem['footerLink'] = ''.join(blockdata.xpath('p/a/text()').extract())
            item['blockData'] = blockitem


        owneritem = OwnerItem()
        owneritem['imgsrc'] = ''.join(response.xpath('//*[@id="contactwidget"]/div[1]/span/span/img/@src').extract())
        ownerprofileitem = OwnerProfileItem()
        for data in response.xpath('//*[@id="contactwidget"]/div[1]/div'):
            ownerprofileitem['title'] = ''.join(data.xpath('div[1]/b/text()').extract())
            ownerprofileitem['desc'] = ''.join(data.xpath('div[2]/text()').extract()).strip()
            ownerprofileitem['speaks'] = ''.join(response.xpath('//*[@id="owner-speaks"]/text()').extract()).strip()
            ownerprofileitem['inquirybuttonText'] = ''.join(data.xpath('a/text()').extract())
        owneritem['ownerProfile'] = ownerprofileitem
        ownerresponseitem = OwnerResponseItem()
        for data in response.xpath('//*[@id="contactwidget"]/ul'):
            ownerresponseitem['responseTime'] = ''.join(data.xpath('li[1]/span[2]/text()').extract())
            ownerresponseitem['responseRate'] = ''.join(data.xpath('li[2]/span[2]/text()').extract())
            ownerresponseitem['calenderLastUpdated'] = ''.join(data.xpath('li[3]/span[2]/text()').extract())
        owneritem['ownerResponse'] = ownerresponseitem
        owneritem['phoneText'] = ''.join(response.xpath('//*[@id="contactwidget"]/div[2]/div[1]/a/text()').extract())
        item['owner'] = owneritem


        item['rates'] = []
        for data in response.xpath('//*[@id="section-rates"]/div/div[3]/table/tbody/tr'):
            ratesforitem = rateForItem()
            ratesforitem['nightly'] = ''.join(data.xpath('td[2]/span/text()').extract())
            ratesforitem['weekendNight'] = ''.join(data.xpath('td[3]/span/text()').extract())
            ratesforitem['weekly'] = ''.join(data.xpath('td[4]/span/text()').extract())
            ratesforitem['monthly'] = ''.join(data.xpath('td[5]/span/text()').extract())
            ratesforitem['event'] = ''.join(data.xpath('td[6]/span/text()').extract())

            ratesdateitem = ratesDateItem()
            ratesdateitem['title'] = ''.join(data.xpath('td[1]/b/text()').extract())
            ratesdateitem['date'] = ''.join(data.xpath('td[1]/small[1]/text()').extract())
            ratesdateitem['stay'] = ''.join(data.xpath('td[1]/small[2]/text()').extract())
            ratesforitem['date'] = ratesdateitem

            if (ratesforitem['nightly'] or ratesforitem['weekendNight'] or ratesforitem['weekly'] or ratesforitem[
                'monthly'] or ratesforitem['event']):
                item['rates'].append(ratesforitem)



        facilityitem = FacilityItem()
        for facilitydata in response.xpath('//*[@id="listing-bigtop"]'):
            propertyitem = PropertyTypeItem()
            propertyitem['type'] = ''.join(facilitydata.xpath('div[3]/ul[1]/li/span/text()').extract())
            propertyitem['area'] = ''.join(facilitydata.xpath('div[3]/ul[2]/li/span/text()').extract())
            facilityitem['propertyType'] = propertyitem

            facilityitem['accommodationType'] = ''.join(facilitydata.xpath('div[4]/ul[3]/li/span/text()').extract())
            facilityitem['meals'] = ''.join(facilitydata.xpath('div[5]/ul[3]/li/span/text()').extract())

            facilityitem['onsiteServices'] = []
            for data in facilitydata.xpath('div[6]/ul/li'):
                facilityitem['onsiteServices'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['suitability'] = []
            for data in facilitydata.xpath('div[7]/ul/li'):
                facilityitem['suitability'].append(''.join(data.xpath('span/text()').extract()))

            bedroomitem = BedroomItem()
            bedroomitem['desc'] = ''.join(facilitydata.xpath('div[8]/h3/span/text()').extract())
            bedroomitem['list'] = []
            for data in facilitydata.xpath('div[8]/ul/li'):
                bedroomdescitem = BedroomDescItem()
                bedroomdescitem['name'] = ''.join(data.xpath('span/text()').extract())
                bedroomdescitem['desc'] = ''.join(data.xpath('p/i/text()').extract())
                bedroomitem['list'].append(bedroomdescitem)
            facilityitem['bedrooms'] = bedroomitem

            bathroomitem = BathroomItem()
            bathroomitem['desc'] = ''.join(facilitydata.xpath('div[9]/h3/span/text()').extract())
            bathroomitem['list'] = []
            for data in facilitydata.xpath('div[9]/ul/li'):
                bathroomitem['list'].append(''.join(data.xpath('span/text()').extract()))
            facilityitem['bathrooms'] = bathroomitem

            facilityitem['entertainment'] = ''.join(facilitydata.xpath('div[10]/ul[3]/li/span/text()').extract())

            facilityitem['theme'] = []
            for data in facilitydata.xpath('div[11]/ul/li'):
                facilityitem['theme'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['attractions'] = []
            for data in facilitydata.xpath('div[12]/ul/li'):
                facilityitem['attractions'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['localServicesAndBusinesses'] = []
            for data in facilitydata.xpath('div[13]/ul/li'):
                facilityitem['localServicesAndBusinesses'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['leisureActivities'] = []
            for data in facilitydata.xpath('div[14]/ul/li'):
                facilityitem['leisureActivities'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['locationType'] = []
            for data in facilitydata.xpath('div[15]/ul/li'):
                facilityitem['locationType'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['sportsAndAdventureActivities'] = []
            for data in facilitydata.xpath('div[16]/ul/li'):
                facilityitem['sportsAndAdventureActivities'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['dining'] = []
            for data in facilitydata.xpath('div[17]/ul/li'):
                facilityitem['dining'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['general'] = []
            for data in facilitydata.xpath('div[18]/ul/li'):
                facilityitem['general'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['kitchen'] = []
            for data in facilitydata.xpath('div[19]/ul/li'):
                facilityitem['kitchen'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['outside'] = []
            for data in facilitydata.xpath('div[20]/ul/li'):
                facilityitem['outside'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['poolAndSpa'] = []
            for data in facilitydata.xpath('div[21]/ul/li'):
                facilityitem['poolAndSpa'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['houseCleaning'] = []
            for data in facilitydata.xpath('div[22]/ul/li'):
                facilityitem['houseCleaning'].append(''.join(data.xpath('span/text()').extract()))

            facilityitem['propertyDescriptor'] = []
            for data in facilitydata.xpath('div[23]/ul/li'):
                facilityitem['propertyDescriptor'].append(''.join(data.xpath('span/text()').extract()))

        item['facilities'] = facilityitem



        reviewItem = ReviewItem()
        reviewItem['ratingCount'] = ''.join(
            response.xpath('//*[@id="section-reviews"]/div/div[2]/b[1]/text()').extract())
        reviewItem['numReviews'] = ''.join(
            response.xpath('//*[@id="section-reviews"]/div/div[2]/b[2]/text()').extract())
        reviewItem['reviewerDesc'] = []

        for data in response.xpath('//body/li'):
            reviewerdescitem = ReviewerDescItem()
            reviewerdescitem['reviewerName'] = ''.join(data.xpath('a/span[2]/text()').extract())
            reviewerdescitem['reviewImage'] = ''.join(data.xpath('a/span[1]/img/@src').extract())
            reviewerdescitem['reviewerPlace'] = ''.join(data.xpath('a/span[3]/text()').extract())
            reviewerdescitem['reviewerRatingCount'] = ''.join(data.xpath('div[1]/div[1]/span/meta/@content').extract())
            reviewerdescitem['reviewHeading'] = ''.join(data.xpath('h3/text()').extract())
            reviewerdescitem['review'] = ''.join(data.xpath('div[1]/div[2]/text()').extract())
            reviewerdescitem['stayedDate'] = ''.join(data.xpath('div[1]/ul/li/text()').extract())
            reviewerdescitem['submittedDate'] = ''.join(data.xpath('div[1]/ul/li/time/text()').extract())

            if (reviewerdescitem):
                reviewItem['reviewerDesc'].append(reviewerdescitem)

        item['reviews'] = reviewItem
        yield item
