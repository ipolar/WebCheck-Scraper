#!/usr/bin/python
#
# Search Companies House WebCheck service for a valid company name, and return its details
#
# Version:	0.1
# Author:	Andy Lyon
# Date:		17-06-2011
#

import re
import os
import sys
import random
import time
import mechanize
import cookielib
from BeautifulSoup import BeautifulSoup

print "\n**************************"
print "* WebCheck               *"
print "* Author: Andy Lyon      *"
print "* Version: 0.1           *"
print "**************************\n"

# Scrape URL
url = "http://wck2.companieshouse.gov.uk"
company_name = ""
verbose = False

# Proxy settings, leave proxy_url blank if you don't want to use it
proxy_url = ""
proxy_username = ""
proxy_password = ""

# HTTP header settings.
user_agent_array = []
user_agent_array.append('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)')
user_agent_array.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
user_agent_array.append('Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0 )')
user_agent_array.append('Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)')
user_agent_array.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1')
user_agent_array.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')
user_agent_array.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13')
user_agent_array.append('Mozilla/4.8 [en] (Windows NT 6.0; U)')
user_agent_array.append('Mozilla/4.8 [en] (Windows NT 5.1; U)')
user_agent_array.append('Opera/9.25 (Windows NT 6.0; U; en)')
user_agent_array.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; en) Opera 8.0')
user_agent_array.append('Opera/7.51 (Windows NT 5.1; U) [en]')
user_agent_array.append('Opera/7.50 (Windows XP; U)')
user_agent_array.append('Avant Browser/1.2.789rel1 (http://www.avantbrowser.com)')
user_agent_array.append('Mozilla/5.0 (Windows; U; Win98; en-US; rv:1.4) Gecko Netscape/7.1 (ax)')
user_agent_array.append('Mozilla/5.0 (Windows; U; Windows XP) Gecko MultiZilla/1.6.1.0a')
user_agent_array.append('Opera/7.50 (Windows ME; U) [en]')
user_agent_array.append('Mozilla/3.01Gold (Win95; I)')
user_agent_array.append('Mozilla/2.02E (Win95; U)')
user_agent_array.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/125.8')
user_agent_array.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/125.2 (KHTML, like Gecko) Safari/85.8')
user_agent_array.append('Mozilla/4.0 (compatible; MSIE 5.15; Mac_PowerPC)')
user_agent_array.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7a) Gecko/20050614 Firefox/0.9.0+')
user_agent_array.append('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en-US) AppleWebKit/125.4 (KHTML, like Gecko, Safari) OmniWeb/v563.15')

option = '''
Usage  : %s [options]
Option : -c, --company		Company name to search WebCheck for
         -v, --verbose		Set to see the actual http requests/responses

Example : python %s -c "Company Name"
''' % (sys.argv[0], sys.argv[0])


#
# Display our help
#
def display_help():
	print option
	sys.exit(1)


#
# Sort out our switches...
#
for arg in sys.argv:
	try:
		if arg.lower() == '-c' or arg.lower() == '--company':
			company_name = sys.argv[int(sys.argv[1:].index(arg))+2]
		elif arg.lower() == '-v' or arg.lower() == '--verbose':
			verbose = True
		elif len(sys.argv) <= 1:
			display_help()
	except IOError:
		display_help()
	except NameError:
		display_help()
	except IndexError:
		display_help()


#
# Clean strings
#
def clean_string(data):
	data = data.replace("System Requirements", " ")
	data = data.replace("Return to search page", " ")
	data = data.replace("Order information on this company", " ")
	data = data.replace("Monitor this company", " ")
	data = data.replace("Tell Us", " ")
	data = data.replace("Are you satisfied with our service?", " ")
	data = data.replace("Have you got a question?", " ")
	data = data.replace("&nbsp;", " ")
	data = data.replace("&amp;", "&")
	return data


#
# Strip strings
#
def strip_end_data(data):
	
	# Remove any whitespace/newlines from the left of the string and the right
	data = data.lstrip("\n")
	data = data.lstrip("\r")
	
	data = data.rstrip("\n")
	data = data.rstrip("\r")
	
	data = data.lstrip()
	data = data.rstrip()
	
	return data


#
# Strip spaces
#
def strip_spaces(data):
	
	data = " ".join(data.split())
	data = data.lstrip()
	data = data.rstrip()
	
	return data





#
# Strip spaces
#
def filter_data(data):
	
	if len(data) <= 1:
		return False
	elif data == None:
		return False
	elif data == '':
		return False
	elif data == ' ':
		return False
	elif data == '            ':
		return False
	else:
		return True







#
# Main conversion to HTML
# Tweaked a bit from
# From: http://love-python.blogspot.com/2011/04/html-to-text-in-python.html
#
def html_to_text(data):
	
	# Remove the newlines
	#data = data.replace("\n", " ")
	#data = data.replace("\r", " ")
	
	# Replace <br/> with newline
	data = data.replace("<br>", "\n")
	data = data.replace("<br/>", "\n")
	
	# Now remove the java script
	p = re.compile(r'< script[^<>]*?>.*?< / script >')
	data = p.sub('', data)
	
	# Remove the css styles
	p = re.compile(r'< style[^<>]*?>.*?< / style >')
	data = p.sub('', data)
	
	# Remove html comments
	p = re.compile(r'')
	data = p.sub('', data)
	
	# Remove all the tags
	p = re.compile(r'<[^<]*?>')
	data = p.sub('', data)
	
	return data


#
# Actually search the companies house site!
#
def search_companies(my_company_name, my_scrape_url):
	try:
		browser.addheaders = [('User-agent', random.choice(user_agent_array))]
		search_page = browser.open(my_scrape_url)
		
		# Select the correct form (company search form). They don't have a nice form name :(
		browser.select_form(nr=3)
		
		print "\nSearching for: " + my_company_name + "...\n"
		
		# Add in our company search name, we can leave the rest of the form fields as their default values
		browser.form['cname'] = my_company_name
		
		# Submit the form!
		results_page = browser.submit()
		
		# If we have a <tr> with a class of "resCH" we have a valid result.. Otherwise we only have a partial match.
		# If we have a match for our searched company name, then follow that link to get the company info...
		for link in browser.links():
			for ats in link.attrs:
				
				if ats[1] == 'resCH':
					
					# We have a full match, so proceed to the company info page.
					company_page = browser.follow_link(link)
					
					# Parse our source
					soup = BeautifulSoup(browser.response().read())
					
					# We know the company data appears in tds. So we get all the tds on the page...
					detail_cols = soup.findAll('td')
					
					company_details_array = []
					cleaned_company_details_array = []
					final_company_details_array = []
					
					# Loop through each td...
					for col in detail_cols:
						# Does this td contain the text "Content-Start" if so, then this will contain some useful company data
						if str(col.find(text=re.compile("Content-Start"))) != 'None':
							company_details_array.append(strip_end_data(html_to_text(clean_string(str(col)))))
					
					# Loop and filter out any empty list items
					for col in company_details_array:
						#print "\n col: "+str(col)+"\n"
						#cleaned_company_details_array.append(filter(None, col.splitlines()))
						cleaned_company_details_array.append(filter(filter_data, col.splitlines()))
					
					#print cleaned_company_details_array
					
					# Remove the 2 duplicated list items
					cleaned_company_details_array.pop(1)
					cleaned_company_details_array.pop(1)
					
					# Loop and final clean of data
					for col in cleaned_company_details_array:
						final_company_details_array.append(strip_spaces(str(col)))
					
					print "Success...\n\n"
					
					for col in final_company_details_array:
					
						print ""+str(col)+"\n"
						#print "\n\n"
					
					
					sys.exit(1)
				
				elif ats[1] == 'resCN':
					print "We have a parital match, but nothing solid: \n"
					
					# Parse our source
					soup = BeautifulSoup(results_page)
					
					# We know the company data appears in tds. So we get all the tds on the page...
					partial_match = soup.find("tr", { "class" : "resCN" })
					
					suffix = ''
					
					# Is this partial match dissolved?
					if len(html_to_text(str(partial_match.contents[9]))) != 0:
						suffix = " (" + html_to_text(str(partial_match.contents[9])) + ")"
					
					print html_to_text(str(partial_match.contents[7])) + suffix + "\n"
					
					sys.exit(1)
		
		# If we get here, we haven't found any links :(
		print "Can't find any links - so no company by this name found, please search again! \n"
		sys.exit(1)
	
	except KeyboardInterrupt:
		print "\nExiting program...\n"
		sys.exit(1)
	except mechanize._mechanize.FormNotFoundError:
		print "\nCan't find form (form not found)\n"
		sys.exit(1)
	except mechanize._form.ControlNotFoundError:
		print "\nCan't find form (control not found)\n"
		sys.exit(1)
	except mechanize._mechanize.LinkNotFoundError:
		print "\nCan't find any links - so no company by this name found, please search again! \n"
		sys.exit(1)




#
# Entry point
#
if __name__ == "__main__":
	
	global browser
	
	browser = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
	browser.set_cookiejar(cj)
	browser.set_handle_equiv(True)
	browser.set_handle_gzip(True)
	browser.set_handle_redirect(True)
	browser.set_handle_referer(True)
	browser.set_handle_robots(False)
	browser.set_debug_http(False)
	browser.set_debug_redirects(False)
	browser.set_debug_redirects(False)
	browser.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
	
	if proxy_url != '':
		browser.set_proxies({"http": proxy_url})
	if proxy_username != '':
		browser.add_proxy_password(proxy_username, proxy_password)
	
	# Verbose info...
	if verbose:
		browser.set_debug_http(True)
		browser.set_debug_redirects(True)
		browser.set_debug_redirects(True)
	
	# Do some cleaning on our scrape URL
	if "http://" in url:
		url = url.replace("http://","")
	if "www." in url:
		url = url.replace("www.","")
	
	scrape_url = "http://"+url+"/"
	
	search_companies(company_name, scrape_url)