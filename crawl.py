# Adaptado de: https://github.com/kezakez/python-web-crawler/blob/master/crawl.py

import sys
import time
import httplib
import re
import argparse
from collections import deque
from urlparse import urlparse, urljoin


def urlSeguible(url):
    return url.find("javascript") == -1 and \
            url.find("download.php") == -1 and \
            url.find("mailto:") == -1 and \
            url.find(".mp3") == -1 and \
            url.find(".css") == -1



#Crawler BFS iterativo
def crawl(url, depth, domain):
    
    urls_to_be_processed_queue = deque([(0,url)])
    visited_urls = set()
	
    while len(urls_to_be_processed_queue) > 0:    
        cur_depth, url = urls_to_be_processed_queue.popleft()
    
        # Ignora la URL:
        # 1) Si ya fue visitada
        if url in visited_urls:
            continue

        # La marca como visitada
        visited_urls.add(url)
        
        # 2) Si sale del dominio especificado
        
        parsedurl = urlparse(url)
        host = parsedurl.netloc
        path = parsedurl.path + (';' if (parsedurl.params != "") else '') + parsedurl.params + \
                                ('?' if (parsedurl.query != "") else '') + parsedurl.query 
        
        if host.endswith(domain):
                        
            conn = httplib.HTTPConnection(host)
            
            try:
                req = conn.request("GET", path)
            except:
                sys.stderr.write('ERROR obteniendo recurso\n')
                sys.stderr.write("HOST = " + host + '\n')
                sys.stderr.write("PATH = " + path + '\n')
                continue
                
            res = conn.getresponse()
    
            # Encuentra los links
            contents = res.read()
            m = re.findall('href="(.*?)"', contents)
            
            for href in m:    
                # Descarta los links internos que no son validos (en este caso, href="javascript....)
                if urlSeguible(href):
                    
                    # URLs relativas
                    if (not href.startswith("http://")):
                        href = urljoin(url, href)
                        
                    #OUTPUT a salida estandar
                    sys.stdout.write('"%s","%s"'  % (url, href))
                    
                    # Si no se alcanzo la profundida maxima, agrega los links para seguir
                    if (cur_depth < depth):
                        urls_to_be_processed_queue.append((cur_depth + 1, href))



def main():    
    parser = argparse.ArgumentParser(description="Web Crawler")
    
    parser.add_argument('url',help='URL que revisara el crawler')
    parser.add_argument('depth',type=int,  help='Niveles de profundidad hasta el cual revisara el crawler. ' +\
                                                'Si el valor de depth es 0 se revisara unicamente la pagina indicada en url, y no seguira enlaces')
    parser.add_argument('domain', nargs='?',default='',help='Dominio al cual esta restringido para seguir una pagina. Ej: exactas.uba.ar')
    args = parser.parse_args()
        
    crawl(args.url, args.depth, args.domain)
    
    		
if __name__== '__main__':
    main()    

