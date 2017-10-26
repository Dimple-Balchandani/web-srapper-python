# Define here the models for your scraped items

import scrapy


class VrboItem(scrapy.Item):
    image = scrapy.Field()
    imageList = scrapy.Field()
    listingOverview = scrapy.Field()
    propertyTitle = scrapy.Field()
    propertyDescription = scrapy.Field()
    owner = scrapy.Field()
    blockData = scrapy.Field()
    facilities = scrapy.Field()
    reviews = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    reviewUrl = scrapy.Field()
    locationDescription = scrapy.Field()
    rates = scrapy.Field()


class ListingOverviewItem(scrapy.Item):
    listingKey = scrapy.Field()
    listingValue = scrapy.Field()


class BlockItem(scrapy.Item):
    title = scrapy.Field()
    footerText = scrapy.Field()
    footerLink = scrapy.Field()


class OwnerItem(scrapy.Item):
    imgsrc = scrapy.Field()
    ownerProfile = scrapy.Field()
    ownerResponse = scrapy.Field()
    phoneText = scrapy.Field()


class OwnerProfileItem(scrapy.Item):
    title = scrapy.Field()
    desc = scrapy.Field()
    speaks = scrapy.Field()
    inquirybuttonText = scrapy.Field()


class OwnerResponseItem(scrapy.Item):
    responseTime = scrapy.Field()
    responseRate = scrapy.Field()
    calenderLastUpdated = scrapy.Field()


class FacilityItem(scrapy.Item):
    propertyType = scrapy.Field()
    accommodationType = scrapy.Field()
    meals = scrapy.Field()
    onsiteServices = scrapy.Field()
    suitability = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    entertainment = scrapy.Field()
    theme = scrapy.Field()
    attractions = scrapy.Field()
    localServicesAndBusinesses = scrapy.Field()
    leisureActivities = scrapy.Field()
    locationType = scrapy.Field()
    sportsAndAdventureActivities = scrapy.Field()
    dining = scrapy.Field()
    general = scrapy.Field()
    kitchen = scrapy.Field()
    outside = scrapy.Field()
    poolAndSpa = scrapy.Field()
    houseCleaning = scrapy.Field()
    propertyDescriptor = scrapy.Field()


class PropertyTypeItem(scrapy.Item):
    type = scrapy.Field()
    area = scrapy.Field()


class BedroomItem(scrapy.Item):
    desc = scrapy.Field()
    list = scrapy.Field()


class BedroomDescItem(scrapy.Item):
    name = scrapy.Field()
    desc = scrapy.Field()


class BathroomItem(scrapy.Item):
    desc = scrapy.Field()
    list = scrapy.Field()


class ReviewItem(scrapy.Item):
    ratingCount = scrapy.Field()
    numReviews = scrapy.Field()
    reviewerDesc = scrapy.Field()


class ReviewerDescItem(scrapy.Item):
    reviewerName = scrapy.Field()
    reviewImage = scrapy.Field()
    reviewerPlace = scrapy.Field()
    reviewerRatingCount = scrapy.Field()
    reviewHeading = scrapy.Field()
    review = scrapy.Field()
    stayedDate = scrapy.Field()
    submittedDate = scrapy.Field()


class rateForItem(scrapy.Item):
    date = scrapy.Field()
    nightly = scrapy.Field()
    weekendNight = scrapy.Field()
    weekly = scrapy.Field()
    monthly = scrapy.Field()
    event = scrapy.Field()


class ratesDateItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    stay = scrapy.Field()
