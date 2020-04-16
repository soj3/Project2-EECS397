#! /usr/bin/awk -f
BEGIN{
	print "Content-type: text/html\n"
	print "<form method='GET' action=''>"
	print "<input name='url' size='80' value='https://en.wikipedia.org/wiki/Cat'>"
	print "<input type='submit'>"
	print "</form>"
	split(ENVIRON["QUERY_STRING"],cc,/&/)
	for (i in cc) {split(cc[i],cd,/=/); cgidat[cd[1]] = cd[2] }
	url = cgidat["url"]
	gsub(/%3A/,":",url)
	gsub(/%2F/,"/",url)
	#print "getting " url
	temp = "lynx -dump -nolist '" url "'  | sed 's/[<>,\\.!\\^?#-*+\\[\\]]//g' | sed 's/-//g'| sed 's/\\b[Tt]he\\b//g' | sed 's/#//g' |sed \"s/'//g\" | sed 's/;//g' | sed 's/,//g' | sed 's/\\.//g' | sed 's/://g' | sed 's/(//g' | sed 's/)//g' | sed 's/\\]//g'| sed 's/\\^//g' | sed 's/\\*//g' | sed 's/\\[//g' | sed 's/+//g' | sed 's/\"//g' | sed 's/[0-9]//g' | tr ' ' '\n' | tr '[A-Z]' '[a-z]' |sort -f | uniq -ic -c| sort -nr "	
	print "<html>"
 	print "<head>"
	print "<title>URL  WordCloud</title>"
 	print "<script src=\"https://cdn.anychart.com/releases/v8/js/anychart-base.min.js\"></script>"
	print "<script src=\"https://cdn.anychart.com/releases/v8/js/anychart-tag-cloud.min.js\"></script>"
 	print "<style>"
   	print "html, body, #container {"
   	print "width: 100%;"
   	print "height: 100%;"
   	print "margin: 0;"
    	print "padding: 0;"
    	print "}"
  	print "</style>" 
 	print "</head>"
  	print "<body>"
   	print "<div id=\"container\"></div>"
    	print "<script>"
	print "anychart.onDocumentReady(function() {var data = ["
	flag = 0
 	while( (temp|getline result)>0){
 			if (flag == 0){
 			   	flag = 1
 			 }
 			 else{
                gsub(/'/, "\\'", result)
                gsub(/\r|\n/, "", result)

                split(result, a, " ")
                print("{\"x\":\"" a[2] "\",\"value\": "  a[1] "},")
                flag = 1
        	}
        } close(temp)
	print "];"
	print "var chart = anychart.tagCloud(data);"
	print "chart.title(\'Word cloud of words in " url "\')"
	print "chart.angles([0])"
	print "chart.colorRange(true);"
	print "chart.colorRange().length('80%');"
	print "chart.container(\"container\");"
	print "chart.draw();"
	print "});"
	print "</script>"
 	print " </body>"
	print "</html>"
}
