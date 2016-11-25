# -*- coding: utf-8 -*-
"""
    Dramafever Downloader descarga subtitulos de episodios de Dramafever en srt.
    
    Uso: dramafever.py url [-s] [--lang IDIOMA]
    
    positional arguments:
      url                   URL del video de Dramafever
    optional arguments:
      -h, --help            Muestra este mensaje y la aplicación cierra
      -s, --subs            Muestra todos los subtitulos disponibles
      --lang LANG           Codigo ISO del idioma
      -v, --video           Descarga el video

    Ejemplo:
    python dramafever.py https://www.dramafever.com/es/drama/4946/1/The_K2/?ap=1 --lang en

"""
import sys
import time
import urlparse
import argparse
import urllib2
import re
import json
from bs4 import BeautifulSoup

class Dramafever():
    
    video_id = None
    subtitle = None
    video_title = None
    languages = {}

    def __init__(self,url=None):
        self.video_id = self.getVideoID(url).replace('/','.')
        self.video_title = self.getVideoTitle(url)
        self.languages = self.getLanguages()

    def downloadSub(self,lang):
        """Descarga el subtitulo"""
        if self.getDramaLanguage(lang) in self.languages.keys():
            print "Descargando subtitulo"
            sub_url = self.languages[self.getDramaLanguage(lang)]
            sub_xml = self.requestURL(sub_url).read()

            subtitle = self.xml2srt(sub_xml)
            
            output = file('%s_%s_%s.srt'%(self.video_title,self.video_id,lang),'w')
            output.write(subtitle)
            output.close()
            print '%s Subtitulo descargado\n'%(self.video_title)
            
        else:
            print 'Subtitulo no disponible'
            sys.exit()

    def getLanguages(self):
        """Obtiene todos los idiomas disponibles"""
        feed_url = 'http://www.dramafever.com/amp/episode/feed.json?guid=%s'%(self.video_id)
        try:
            content = json.load(self.requestURL(feed_url))
            temp_languages = {}
            content = content['channel']['item']['media-group']['media-subTitle']
            for lang in content:
                key = lang['@attributes']['lang']
                value = lang['@attributes']['href']
                temp_languages[key] = value
            return temp_languages
        except Exception as e:
            print e

    def getVideoID(self,url=None):
        """Obtiene el id del video"""
        url_data = urlparse.urlparse(url)
        if url_data.hostname == 'www.dramafever.com':
            if re.search('(?<=/drama/)([0-9]+/[0-9]+)(?=/)',url_data.path):
                return re.search('(?<=/drama/)([0-9]+/[0-9]+)(?=/)',url_data.path).group()

        return None

    def getVideoTitle(self,url=None):
        """Obtiene el titulo del video"""
        url_data = urlparse.urlparse(url)
        if url_data.hostname == 'www.dramafever.com':
            if re.search('([0-9]+/[0-9]+/)(.*?)(?=/)',url_data.path):
                return re.search('([0-9]+/[0-9]+/)(.*?)(?=/)',url_data.path).group(2)

        return ''        

    def getDramaLanguage(self,lang):
        drama_languages = {"en":"English","pt":"Portuguese","es":"Spanish"}
        if lang in drama_languages.keys():
            return drama_languages[lang]
        return None

    def lista(self):
        """Muestra todos los subtítulos disponibles"""
        for key in self.languages.keys():
            iso = re.search('(?<=\d_)([a-z]{2})',self.languages[key]).group()
            print "%s : %s"%(iso,key)

    def requestURL(self, url):
        """Realiza la peticion http"""
        req = urllib2.Request(url)
        req.add_unredirected_header('User-Agent', 'Mozilla/5.0')
        return urllib2.urlopen(req)

    def xml2srt(self,sub_xml):
        soup = BeautifulSoup(sub_xml,'html.parser')
        parse_time = lambda time: time.replace('.', ',')
        subtitle = ''
        for i, p_tag in enumerate(soup.findAll('p')):
            subtitle += str(i + 1) + '\n'
            subtitle += "%s --> %s\n" % (parse_time(p_tag.get('begin')), parse_time(p_tag.get('end')))
            
            line = p_tag.text.replace('<br/>','\n')
            subtitle += line + "\n\n"

        return subtitle
    
def main():
    try:
        parser = argparse.ArgumentParser(description="Dramafever Downloader")
        parser.add_argument("url", help="URL del video en Dramafever")
        parser.add_argument("-s","--subs",action="store_true", help="Muestra todos los subtitulos disponibles")
        parser.add_argument("-lang",default="es", help="Codigo ISO del idioma")
        args = parser.parse_args()

        dramadown = Dramafever(args.url)

        if args.subs:
            print "Subtitulos disponibles:"
            dramadown.lista()

        dramadown.downloadSub(args.lang)
        
    except Exception as e:
        print e            

if __name__ == '__main__':
    #https://www.dramafever.com/es/drama/4946/1/The_K2/?ap=1
    reload(sys)
    sys.setdefaultencoding("utf-8")
    main()
