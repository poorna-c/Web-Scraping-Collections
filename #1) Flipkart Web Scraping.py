from bs4 import BeautifulSoup
import requests
import csv
import os

product = input("Enter product you want to search : ")
pages = int(input("Enter number of pages: "))
search = "/search?q="+product+"&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off"
file_name = f"Flipkart Scraping on {product}.csv"
# Checking if you have already searched for the same product before. If so, The previous search is deleted.
if os.path.exists(file_name):
	print("You have already searched for this...\nDeleting your previous results...")
	os.system(f"rm '{file_name}'")

# Looping through the requested no. of pages
for i in range(pages):
	try:
		file = open(file_name,"w")
		csv_file = csv.writer(file)
		csv_file.writerow(["TITLE","Price","Rating"])#,"Features"])
		url = "https://www.flipkart.com"+search
		html = requests.get(url)
		print("Working on Page No :",i+1)
		soup = BeautifulSoup(html.text,'lxml')

		for mobile_area in soup.find_all(class_ = "_1UoZlX"):
			title = mobile_area.find(class_ = '_3wU53n')
			price = mobile_area.find(class_ = "_1vC4OE _2rQ-NK")
			rating = mobile_area.find(class_ = "hGSR34")
			rating = "No Rating" if rating == None else rating.text
			# features = []
			# for feature in mobile_area.find_all(class_ = "tVe95H"):
			# 	features.append(feature.text)
			csv_file.writerow([title.text,price.text[1:],rating])#,features])
		# navagating to the Next Page!!! [-1] here is for selecting the Next Page since we have (Previous, Next) with same class name.
		search = soup.find_all(class_ = "_3fVaIS")[-1]
		search = search["href"]
	except IndexError:
		print("Out Of Pages for your search!!!")
		break
	except:
		print("One Item Skiped Due to internal error")
		
file.close()
