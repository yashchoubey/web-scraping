import time
import requests
from datetime import datetime

import urllib
from discovery.models import  *




month_map = {"January":1, "February":2,"March":3,"April":4,"May":5,"June":6,"July":7,"August":8,"September":9,"October":10,"November":11,
	"December":12}

def init_driver_booking():
	from selenium import webdriver
	from selenium.webdriver.support.wait import WebDriverWait
	from bs4 import BeautifulSoup
	from pyvirtualdisplay import Display
	display = Display(visible=0, size=(1024, 768))
	display.start()
	driver = webdriver.Firefox()
	driver.wait = WebDriverWait(driver, 3)
	return driver

def get_reviews(url,scraperobj=None,requested_date=None):
	#print "hello"
	#scraperobj1=scraper.objects.get(id=scraperobj["id"])
	
	driver = init_driver_booking()
	driver.get(url) 

	#Collecting Basic Information
	pageSource = driver.page_source
	soup = BeautifulSoup(pageSource, 'html.parser')
	num_reviews=soup.findAll("a",{"class":"hp_nav_reviews_link toggle_review track_review_link_zh"})
	num_reviews= str(num_reviews[0].find("span")).split(">")[-2].split("(")[1].split(")")[0].replace(",", "")
	

	countrycode=url.split("booking.com/hotel/")[1].split("/")[0]
	pagename=url.split("booking.com/hotel/")[1].split("/")[1].split(".")[0]
	aid=soup.find("input",{"name":"aid"}).get('value') #url.split(".html?aid=")[1].split(";")[0]
	label=url.split("label=")[1].split(";")[0]
	sid=url.split(";sid=")[1].split(";")[0]
	hotelReviews_url="https://www.booking.com/reviewlist.en-gb.html?aid="+aid+";label="+label+";sid="+sid+";cc1="+countrycode+";dist=1;pagename="+pagename+";r_lang=en;type=total;upsort_photo=0&;"
	
	review_data = list()
	if(requested_date):
		requested_date = requested_date.split(' ')
		requested_date = datetime(int(requested_date[0]),int(requested_date[1]),int(requested_date[2]))

	offset = 0
	count=0
	print int(num_reviews)
	#num_reviews=100
	while(offset < float(num_reviews)):
		pre_num_reviews = len(review_data)
		url = hotelReviews_url+"offset="+str(offset)+";rows=10"
		offset += 10
		print url
		#print offset,num_reviews
		driver.get(url)
		#time.sleep(5)
		pageSource = driver.page_source
		soup = BeautifulSoup(pageSource,"html.parser")
		
		#print str(soup)
		reviews = soup.findAll("div",{"class":"review_item_review_content"})
		dates = soup.findAll("p",{"class":"review_item_date"})
		rating= soup.findAll("span",{"class":"review-score-badge"})
		
		print reviews, dates, rating
		for review1,date,rating in zip(reviews,dates,rating):
			#print 'inside page------------------'
			negText=''
			posText=""

			try:
				negText=review1.find("p",{"class":"review_neg"}).get_text()
				negText=negText.replace('\n',' ').encode('ascii','ignore')
			except:
				pass
			try:
				posText=review1.find("p",{"class":"review_pos"}).get_text()
				posText=posText.replace('\n',' ').encode('ascii','ignore')
			except:
				pass
			
			print negText,'----------',posText
			date = date.get_text().replace('\n','').replace(',',' ').split(' ')
			#print date# Reviewed: 2 January 2018
			#print int(date[-3]),month_map[date[-2]],int(date[-1])
			date = datetime(int(date[-1]),month_map[date[-2]],int(date[-3]))
			
			count=count+1

			review_string=(review1.get_text().replace('\n',' ')).encode('ascii','ignore')
			
			if review_string not in ["There are no comments available for this review",
				"There are no comments available for this review ",
				" There are no comments available for this review ",
				" There are no comments available for this review",
				"This review has been hidden because it doesn't meet our guidelines.",
				"This review has been hidden because it doesn't meet our guidelines. ",
				" This review has been hidden because it doesn't meet our guidelines.  ",
				" This review has been hidden because it doesn't meet our guidelines."] :
				#print "success1"
				#print str(date.date())
				#rObj=review.objects.get_or_create(scraper_id=scraperobj1,feedback=review_string,review_date=str(date.date()),rating=rating.get_text())
				#bObj=booking_review.objects.get_or_create(review_id=rObj,positivetext=posText,negativetext=negText)
				
				print "success"
				
	
	driver.quit()
	return True

if __name__ == "__main__":
	#driver = init_driver()
	url = """https://www.booking.com/hotel/us/circus-circus.en-gb.html?label=us-6oJMxe6YJvajtPCGEGSB3gS154629283800%3Apl%3Ata%3Ap186000%3Ap2%3Aac%3Aap1t1%3Aneg%3Afi%3Atiaud-146342138230%3Akwd-3433702957%3Alp1007765%3Ali%3Adec%3Adm;sid=4a52818fe375be4cfbbb5ff1eb4551a7;dest_id=20079110;dest_type=city;dist=0;group_adults=1;group_children=0;hapos=3;hpos=3;no_rooms=1;room1=A;sb_price_type=total;srepoch=1510815808;srfid=438f0bc8d9048304941113c2cb2802a2d7540927X3;srpvid=d3a3319f8cf301f4;type=total;ucfs=1&#hotelTmpl"""
	print(get_reviews(url))
