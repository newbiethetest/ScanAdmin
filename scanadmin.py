#-*- coding: utf-8 -*-
__author__ = 'newbie@kali'
import re
import sys,getopt
import Queue
import threading
import urllib2
import time

def usage():
    print'''This program just made by newbie008@wooyun.org
       version 1.0
Usage:python scanadmin.py [-u|-e|-f]

    -u:Url is what U want to scan
           Example:scanadmin.py -u "http://www.baidu.com"             
    -f:File data like "editor" or"admin" etc
           Example:scanadmin.py -u "http://www.baidu.com" -f "/home/admin.txt"
 '''
admin=['-admin','2013','adminer','_admin','2012','_2012''2008','_system','_sys_admin']
dir=[]
def normaldomain(str):
    for i in range(len(str)):
       newstr=str[0:(i+1)]
       for a in admin:
           dir.append(newstr+a)
           
def btdomain(target_url):
    newstr=target_url.split('-')
    for item in newstr:
        normaldomain(item)
        
def FileScan(file):
    f=open(file)
    data=f.readlines()
    for line in data:
        line=line.strip()
        dir.append(line)
    f.close()

queue = Queue.Queue()
class RedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        pass
    def http_error_302(self, req, fp, code, msg, headers):        
        pass

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        #self.exception=exception
    def run(self):
        while True:
            #grabs host from queue
            host = self.queue.get()
            #grabs urls of hosts and look 200 is ok?          
            try:
                opener = urllib2.build_opener(RedirectHandler)
                response=opener.open(host+'/')
                print '[+]%s \t %s'%(response.getcode(),host)
            except urllib2.HTTPError, e:
                print '[+]%s \t %s'%(e.code,host)
            except urllib2.URLError,e:
                print '[+]%s \t can not visit'%host
            self.queue.task_done()
start = time.time()
def main():
###################################################
    if len (sys.argv) < 2:
        usage()
        sys.exit(1)
    else:
        try:
            opts,args = getopt.getopt(sys.argv[1:], "hu:f:e:");
            for opt,arg in opts:
                if opt =="-h":
                    usage();
                    sys.exit(1);
                elif opt == "-u":
                    target=arg
                    target_url=re.match(r'\w+:\/\/\w+\.(.*?)\.\w+',arg).group(1)                    
                elif opt == "-f":
                    file=arg
                    FileScan(file)
        except:
            usage()
            sys.exit(1)
    ###################################################
        match=re.search(r'-',target_url)
        if match:
            print 'star btscanning...'
            btdomain(target_url)
        else:
            print 'normal scanning ...'
            normaldomain(target_url)
    ###################################################
    #spawn a pool of threads, and pass them queue instance
    for i in range(5):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
        #put the hosts to queue
    for line in dir:
        hosts=target+'/'+line+'/'
        queue.put(hosts)
    queue.join()
main()
print "Elapsed Time: %s" % (time.time() - start)
