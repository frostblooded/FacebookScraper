import cookielib
import mechanize
import re
import codecs
import xlwt

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

print 'Logging in...'
br.open(url)
br.select_form(nr=0)
br.form['email'] = user
br.form['pass'] = passwd
br.submit()

names_found = 0
names = []
post_ids = [715774508558352, 718308821638254, 724679814334488, 727227597413043]
for i, post_id in enumerate(post_ids):
	j = 0
	while True:
		print "Getting response from Facebook for page " + str(j + 1) + " for post " + str(i + 1)

		# link for a request that gets you a lot of data 
		# and inside it are the names of those, who have shared the post
		response = br.open("https://www.facebook.com/ajax/pagelet/generic.php/ViewSharesPagelet?__pc=EXP1%3ADEFAULT&ajaxpipe=1&ajaxpipe_token=AXiMxQYNBYG_QM_e&no_script_path=1&data=%7B%22load%22%3A" +
		str(j) +
		"%2C%22target_fbid%22%3A" + 
		str(post_id) +
		"%7D&__user=100000158681631&__a=1")
		print 'Getting names from response...'
		matches = re.findall(r'[\w\d\.\s\\-]+(?=\\u003C\\\/a>\\u003C\\\/span> shared)', response.read())
		names_found = len(matches)
		names += matches
		j += 1

		if names_found <= 0:
			break

print 'Making Excel file...'
book = xlwt.Workbook()
sheet1 = book.add_sheet("Names")

for i, name in enumerate(names):
        sheet1.write(i, 0, name.decode('unicode-escape'))

book.save("names.xls")
print 'Done!'
print 'Press Enter key to quit...'
raw_input()
