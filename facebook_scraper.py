import cookielib
import mechanize
import re
import codecs
import xlwt
from HTMLParser import HTMLParser

br = mechanize.Browser()
cookiejar = cookielib.LWPCookieJar()
br.set_cookiejar( cookiejar )
br.set_handle_equiv( True )
br.set_handle_redirect( True ) 
br.set_handle_referer( True )
br.set_handle_robots( False )

br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1)
br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ]

user = "FACEBOOK_USERNAME"
passwd = "FACEBOOK_PASSWORD"
url = "https://m.facebook.com/login.php"

print 'Loading...'
br.open(url)
br.select_form(nr=0)
br.form['email'] = user
br.form['pass'] = passwd
br.submit()

names_found = 0
names = []
post_ids = [927758767359924, 918897361579398, 918406058295195]
for i, post_id in enumerate(post_ids):
	j = 0
	while True:
		print 'Post ' + str(i + 1) + ': page ' + str(j + 1)

		# link for a request that gets you a lot of data 
		# and inside it are the names of those, who have shared the post
		response = br.open("https://www.facebook.com/ajax/pagelet/generic.php/ViewSharesPagelet?__pc=EXP1%3ADEFAULT&ajaxpipe=1&ajaxpipe_token=AXiMxQYNBYG_QM_e&no_script_path=1&data=%7B%22load%22%3A" +
		str(j) +
		"%2C%22target_fbid%22%3A" + 
		str(post_id) +
		"%7D&__user=100000158681631&__a=1")
		matches = re.findall(r'[;#&\w\d\.\s\\-]+(?=\\u003C\\\/a>\\u003C\\\/span> shared)', response.read())
		names_found = len(matches)
		names += matches
		j += 1

		if names_found <= 0 or j > 5:
			break

print 'Making Excel file...'
h = HTMLParser()
book = xlwt.Workbook()
sheet1 = book.add_sheet("Names")

for i, name in enumerate(names):
        name = h.unescape(name)
        sheet1.write(i, 0, name)

try:
        book.save("names.xls")
except IOError as err:
        print 'An error occured while saving the Excel file. Please close it if it\'s open and try again.'
        
print 'Done!'
print 'Press Enter key to quit...'
raw_input()
