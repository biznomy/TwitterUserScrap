import scrapy
from scrapy import Request
import json

class TwitteruserSpider(scrapy.Spider):
    name = "twitter"
    allowed_domains = ["twitter.com"]
    start_urls = ['https://twitter.com/search?f=users&vertical=default&q=kam']
    
    def parse(self, response):
        for card in response.css(".GridTimeline-items .ProfileCard"):
           username = card.css('.ProfileCard-screennameLink span::text').extract()[0]
           yield Request("https://twitter.com/"+username,callback=self.parse_userinfo)
    
    def parse_userinfo(self,user):
           img = user.css('img.ProfileAvatar-image::attr(src)').extract()[0]
           name = user.css('.ProfileHeaderCard-nameLink::text').extract()[0]
           username = user.css('.ProfileHeaderCard-screennameLink span::text').extract()[0]
           bio = user.css('p.ProfileHeaderCard-bio::text').extract()[0]
           location = user.css('.ProfileHeaderCard-locationText::text').extract()[0]
           joinDate = user.css('.ProfileHeaderCard-joinDateText::text').extract()[0]
           tweetsCount = user.css('.ProfileNav-item--tweets .ProfileNav-value::text').extract()[0]
           followingCount = user.css('.ProfileNav-item--following .ProfileNav-value::text').extract()[0]
           followersCount = user.css('.ProfileNav-item--followers .ProfileNav-value::text').extract()[0]
           userData = {
               "img":img.strip(),
               "name":name.strip(),
               "username":username.strip(),
               "bio":bio.strip(),
               "location":location.strip(),
               "joinDate":joinDate.strip(),
               "tweetsCount":tweetsCount.strip(),
               "followingCount":tweetsCount.strip(),
               "followersCount":followersCount.strip()
              }
           yield{
               "img":img.strip(),
               "name":name.strip(),
               "username":username.strip(),
               "bio":bio.strip(),
               "location":location.strip(),
               "joinDate":joinDate.strip(),
               "tweetsCount":tweetsCount.strip(),
               "followingCount":tweetsCount.strip(),
               "followersCount":followersCount.strip()
              }
           #yield Request("http://localhost:3000/user/save", self.after_post, method="POST", body=json.dumps(userData),headers={'Content-Type':'application/json'})
           for tweetMember in user.css('.stream-items .username'):
             yield Request("https://twitter.com/"+tweetMember.css("b::text").extract()[0],callback=self.parse_userinfo)

  
    # def after_post(self,response):
    #   print("save ===========")
    #   data = json.loads(response.body)