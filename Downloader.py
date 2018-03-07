import newspaper
import threading

printingLock = threading.Lock()

class DownloadThread(threading.Thread):

    def __init__(self, url, numArticles):
        threading.Thread.__init__(self)
        
        #Form site
        LockingPrint("\nDownloading from:" + url + ". . .")
        self.site = newspaper.build(url, is_memo = False)
        self.site.clean_memo_cache()
        self.articlesToPull = min(numArticles, self.site.size())
        self.isFinished = False
        self.url = url

    def __str__(self):
        return str("Downloading from: " + self.url)

    # This is the primary function run when thread is started. Thread closes
    # when this function returns.
    def run(self):
        for i in range(self.articlesToPull):
            self.site.articles[i].download()
            self.site.articles[i].parse()

        LockingPrint("Finished dowloading from: " + self.url)
        self.isFinished = True
        return

    def isFinished(self):
        return self.isFinished

# Acquires lock, prints, then releases lock. Prevents prints from happenning simultaneously.
def LockingPrint(string):
    printingLock.acquire()
    print(string)
    printingLock.release()