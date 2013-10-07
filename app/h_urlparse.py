import urlparse
import dicttoxml

def urlFormToXML(string,boolean = False):
	form = string[string.rfind("?")+1:]
	return  dicttoxml.convert(dict(urlparse.parse_qsl(form)),boolean) 
