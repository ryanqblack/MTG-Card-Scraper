from datetime import datetime
import lxml
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

def bs_(soup):
	return bs(soup, features="lxml")

def soup_(driver):
	html = driver.page_source
	soup = bs_(html)
	return bs_(soup.prettify())

def get_links(soup, urls):
	try:
		for i in soup.find_all(class_="name top"):
			urls.append((str(i).split("\""))[3])
	except Exception:
		pass

	return urls

def create_url(url, page_num, check):
	if check == False:
		return "https://gatherer.wizards.com/Pages/Search/Default.aspx?page=" + str(page_num) + "&action=advanced&name=|[_]|[a]|[b]|[c]|[d]|[e]|[f]|[g]|[h]|[i]|[j]|[k]|[l]|[m]|[n]|[o]|[p]|[q]|[r]|[s]|[t]|[u]|[v]|[w]|[x]|[y]|[z]"
	else:
		url = url[2:len(url)]
		return "https://gatherer.wizards.com/Pages" + url

def switch_routine(page_num):
	if page_num == 245:
		return True
	else:
		return False

def sort_colors(soup):
	string = ""
	colorless = 0
	red = 0
	blue = 0
	green = 0
	white = 0
	black = 0
	generic = 0

	soup = str(soup)
	temp = soup.split("\n")
	temp.pop(0)
	temp.pop(-1)
	
	for i in range(len(temp)):
		temp[i] = temp[i].split("\"")[3]

	for i in range(len(temp)):
		if temp[i] == "Red":
			red += 1
		elif temp[i] == "Blue":
			blue += 1
		elif temp[i] == "Green":
			green += 1
		elif temp[i] == "White":
			white += 1
		elif temp[i] == "Black":
			black += 1
		elif temp[i] == "Colorless":
			colorless += 1
		else:
			generic = temp[i]

	if generic != 0:
		string += "Generic: " + str(generic) + ", "
	if black != 0:
		string += "Black: " + str(black) + ", "
	if blue != 0:
		string += "Blue: " + str(blue) + ", "
	if colorless != 0:
		string += "Colorless: " + str(colorless) + ", "
	if green != 0:
		string += "Green: " + str(green) + ", "
	if red != 0:
		string += "Red: " + str(red) + ", "
	if white != 0:
		string += "White: " + str(white) + ", "

	string = string[:len(string) - 2]
	return string

def get_symbols(soup):
	string = ""

	for i in soup.find_all(class_="cardtextbox"):
		for x in str(i).split("\n"):
			if "</i>" in x or "</div>" in x:
				break
			elif "<i>" in x or "<div class=\"cardtextbox\"" in x:
				pass
			elif "<img align" in x:
				string += " " + x.split("\"")[3]
			else:
				string += " " + x.strip()

	return string.strip()

	
#Implement "alt" so that it doesn't go funky.
#Make sure lands don't crap out. Maybe use get_text()?
def parse_data(soup, url):
	#0 Card name
	#1 Converted mana cost
	#2 Mana cost	
	#3 Type
	#4 Text
	#5 Expansion
	#6 Rarity
	#7 Card Number
	#8 P/T
	#9 Artist
	#10 Community rating
	try:
		real_data = [""] * 11
		for i in soup.find_all(class_="row"):
			i = str(i)
			if "Card Name" in i:
				real_data[0] = i.split("\n")[5].strip()
			elif "Converted Mana Cost" in i:
				real_data[1] = i.split("\n")[-3].strip()
			elif "Mana Cost" in i:
				real_data[2] = sort_colors(bs_(i).find_all(class_="value"))
			elif "Types" in i:
				real_data[3] = i.split("\n")[-3].strip()
			elif "Card Text" in i:
				real_data[4] = get_symbols(bs_(i))
			elif "Expansion" in i:
				real_data[5] = i.split("\n")[7].split("\"")[3].strip()
			elif "Rarity" in i:
				real_data[6] = i.split("\n")[-4].strip()
			elif "Card Number" in i:
				real_data[7] = i.split("\n")[-3].strip()
			elif "P/T" in i:
				real_data[8] = i.split("\n")[-3].strip()
			elif "Artist" in i:
				real_data[9] = i.split("\n")[-4].strip()

		real_data[10] = str(soup.find_all(class_="textRatingValue")).split("\n")[1].strip()
		
		return real_data
	except Exception:
		print("Skipping " + url)
		f = open("skipped.txt", "a")
		f.write(url + "\n")
		f.close()
		return ""
	
def write_file(data):
	try:
		f = open("allcards.xls", "a")

		f.write("Card Name\tConverted Mana Cost\tMana Cost\tType\tText\tExpansion\tRarity\tCard Number\tP/T\tArtist\tCommunity Rating\n")

		for i in range(len(data)):
			string = ""
			for x in range(len(data[i])):
				string += str(data[i][x]) + "\t"
			f.write(string + "\n")

		f.close()
	except Exception as error:
		print("There was an error :/")
		print(error)
		print(str(data[i]))
		f.close()

start = datetime.now()

url = "https://gatherer.wizards.com/Pages/Search/Default.aspx?page=0&output=compact&sort=abc+|cn-&action=advanced&name=|[_]|[a]|[b]|[c]|[d]|[e]|[f]|[g]|[h]|[i]|[j]|[k]|[l]|[m]|[n]|[o]|[p]|[q]|[r]|[s]|[t]|[u]|[v]|[w]|[x]|[y]|[z]"
driver = webdriver.Firefox()

print("Going to page 1")
driver.get(url)

soup = soup_(driver)

urls = []
check = False
page_num = 0

while check == False:
	try:
		urls = get_links(soup_(driver), urls)

		check = switch_routine(page_num)

		if check == True:
			break

		page_num += 1
		url = create_url(url, page_num, check)
		print("Going to page", page_num + 1)
		try:
			driver.get(url)
		except Exception:
			pass
	except KeyboardInterrupt:
		break

#Should be 24,566
print(len(urls))
data = []

for i in range(len(urls)):
	#print("Going to:", urls[i])
	url = create_url(urls[i], page_num, check)
	try:
		driver.get(url)
		soup = soup_(driver)

		data.append(parse_data(soup, url))
	except Exception:
		print("Skipping " + url)
		f = open("skipped.txt", "a")
		f.write(url + "\n")
		f.close()

print("Writing...")
write_file(data)

driver.close()

print("All done! Total number of cards:", len(data))
print("Total time:", datetime.now() - start)