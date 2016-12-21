import sys
import urllib, json

# check YOUTUBE videos with ID by Google YOUTUBE API
def youtubeChecker(youtube_id):
    try:
        urlAPI = "https://www.googleapis.com/youtube/v3/videos?part=status&id=%s&key=AIzaSyAOBqTeqHaI1JTXzJNfQOzZZ-rMGmALHBw"%youtube_id
        response = urllib.urlopen(urlAPI)
        result = json.loads(response.read())
        if result["items"] == []:
            return None,None
        else:
            return result['items'][0]['status']['uploadStatus'],result['items'][0]['status']['embeddable']
    except:
        return 0,0

class htmlEdit(object):
    def __init__(self):
        pass
    def spanTagCleaner(self,htmlText):
        txt_HTML =htmlText.encode("utf-8")
        #txt_HTML =htmlText
        counter = 0
        while txt_HTML.find("<span>") != -1:
            span_start_pos = txt_HTML.find("<span>")
            span_close_start_pos = txt_HTML.find("</span>", span_start_pos)
            txt_HTML = txt_HTML[:span_start_pos] + txt_HTML[span_start_pos+6:span_close_start_pos] + txt_HTML[span_close_start_pos+7:]
            counter += 1

        return txt_HTML, counter

    def youtubeEmbeddedMaker(self,htmlText):
        counter = 0
        youtube_broken_links =[]
        youtube_notallow_embed =[]
        start_pos = 0
        # finding YOUTUBE URL That has not EMBEDDED
        while htmlText.find('<a href="https://www.youtube.',start_pos)!= -1:
            ahref_start_pos = htmlText.find('<a href="https://www.youtube.',start_pos)
            ahref_end_pos = htmlText.find('"',ahref_start_pos+12)
            url = htmlText[ahref_start_pos +9: ahref_end_pos]
            # Extracting YOUTUBE_ID from URL
            yid = self.getYoutubeID(url)

            # check YOUTUBE URL status ---------------------
            uploadStatus,embeddable = youtubeChecker(yid)
            #print uploadStatus,embeddable
            if uploadStatus == None or uploadStatus == 0:
                youtube_broken_links.append(url)
                start_pos = ahref_start_pos + 2
                continue
            if uploadStatus == 'processed' and embeddable == False:
                youtube_notallow_embed.append(url)
                start_pos = ahref_start_pos + 2
                continue         
                

            nextIframe_pos = htmlText.find('<iframe ',ahref_end_pos)
            if nextIframe_pos != -1:
                embed_start = htmlText.find('embed/',nextIframe_pos)
                embed_end = htmlText.find('"',embed_start)
                embed_yid = htmlText[embed_start+6:embed_end]
                #print embed_yid
                if embed_yid != yid:
                    htmlText = self.add_youtube_embed(htmlText,ahref_end_pos,yid)
                    counter += 1
            else:
                htmlText = self.add_youtube_embed(htmlText,ahref_end_pos,yid)
                counter += 1

            start_pos = ahref_start_pos + 2

        start_pos = 0
        while htmlText.find('<a href="http://www.youtube.',start_pos)!= -1:
            ahref_start_pos = htmlText.find('<a href="http://www.youtube.',start_pos)
            ahref_end_pos = htmlText.find('"',ahref_start_pos+12)
            url = htmlText[ahref_start_pos +9: ahref_end_pos]
            # Extracting YOUTUBE_ID from URL
            yid = self.getYoutubeID(url)

            # check YOUTUBE URL status ---------------------
            uploadStatus,embeddable = youtubeChecker(yid)
            #print uploadStatus,embeddable
            if uploadStatus == None or uploadStatus == 0:
                youtube_broken_links.append(url)
                start_pos = ahref_start_pos + 2
                continue
            if uploadStatus == 'processed' and embeddable == False:
                youtube_notallow_embed.append(url)
                start_pos = ahref_start_pos + 2
                continue       
                
            nextIframe_pos = htmlText.find('<iframe ',ahref_end_pos)
            if nextIframe_pos != -1:
                embed_start = htmlText.find('embed/',nextIframe_pos)
                embed_end = htmlText.find('"',embed_start)
                embed_yid = htmlText[embed_start+6:embed_end]
                #print embed_yid
                if embed_yid != yid:
                    htmlText = self.add_youtube_embed(htmlText,ahref_end_pos,yid)
                    counter += 1
            else:
                htmlText = self.add_youtube_embed(htmlText,ahref_end_pos,yid)
                counter += 1

            start_pos = ahref_start_pos + 2

        return htmlText, counter,youtube_notallow_embed, youtube_broken_links 

              
    def add_youtube_embed(self,htmlText,pos,youtubeid):
        add_iframe = '<br /><iframe width="560" height="315" src="https://www.youtube.com/embed/%s" frameborder="0" allowfullscreen=""></iframe>'%youtubeid
        txthtml = htmlText[:htmlText.find('</a>',pos) + 4] + add_iframe + htmlText[htmlText.find('</a>',pos) + 4:]      
        return txthtml


    def linkOpenNewTag(self, htmlText):
        txt_HTML =htmlText.encode("utf-8")
        counter = 0
        start_pos = 0
        
        while txt_HTML.find("<a ", start_pos)!= -1:
            a_tag_start_pos = txt_HTML.find("<a ", start_pos)
            a_tag_close_pos = txt_HTML.find(">", a_tag_start_pos)
            if txt_HTML.find("_blank", a_tag_start_pos, a_tag_close_pos) == -1:
                txt_HTML = txt_HTML.replace(txt_HTML[a_tag_start_pos:a_tag_close_pos+1],
                                 txt_HTML[a_tag_start_pos:a_tag_close_pos]+' target="_blank">',
                                 1)
                counter += 1
            #print txt_HTML 
            start_pos = a_tag_start_pos + 1

        return txt_HTML, counter

    # Extracting YOUTUBE_ID from URL -----------------------------
    def getYoutubeID(self,url):  
        if url.find("v=") != -1:
            start_pos = url.find("v=")+2
            end_pos = url.find("&", start_pos)
            if end_pos == -1:
                end_pos = url.find("#", start_pos)
                if end_pos == -1:
                    youtube_id = url[start_pos:]
                else:
                    youtube_id = url[start_pos:end_pos]
            else:
                youtube_id = url[start_pos:end_pos]
        elif url.find(".be/") != -1:
            start_pos = url.find(".be/")+4
            end_pos = url.find("?", start_pos)
            if end_pos == -1:
                youtube_id = url[start_pos:]
            else:
                youtube_id = url[start_pos:end_pos]

        else:
            youtube_id = 0

        return youtube_id


'''txtHTML = 
<html><a href="https://www.youtube.com/watch?v=x2hF6AnVAio" >
<span><span>hello </span><span>OKKKK</span></span></a>
<a href="https://www.youtube.com/watch?v=1ZPCCmZ6-3E">abc</a>
<a href="https://www.youtube.com/watch?v=uv6ssCB03yw" target="_blank" width=1000>abc</a>
<a href="https://www.youtube.com/watch?v=diG519dFVNs">abc</a>
<a href="https://www.youtube.com/watch?v=v5_RwwecU4I">abc</a>
</html>
'''
'''a = htmlEdit()
#txt, counter = a.spanTagCleaner(txtHTML)
#txt, counter = a.linkOpenNewTag(txtHTML)
txt, counter,youtube_notallow_embed,youtube_broken_links = a.youtubeEmbeddedMaker(txtHTML)
if youtube_notallow_embed:
    print "Following links are not allowed to embed: ", youtube_notallow_embed
if youtube_broken_links:
    print "Following YOUTUBE links are broken links: ", youtube_broken_links
print txt, counter
'''
