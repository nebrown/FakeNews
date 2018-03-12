import newspaper
import threading

printingLock = threading.Lock()

class DownloadThread(threading.Thread):

    def __init__(self, url, numArticles):
        threading.Thread.__init__(self)
        
        #Form site
        LockingPrint("\nDownloading from:" + url + ". . .")
        self.isFinished = False
        self.url = url
        self.numArticles = numArticles
        self.articlesPulled = 0

    def __str__(self):
        return str("Downloading from: " + self.url)

    # This is the primary function run when thread is started. Thread closes
    # when this function returns.
    def run(self):
        self.site = newspaper.build(self.url, is_memo = False)
        self.articlesToPull = min(self.numArticles, self.site.size())
        self.site.clean_memo_cache()
        
        for i in range(self.articlesToPull):
            try:
                self.site.articles[i].download()
                self.site.articles[i].parse()
                LockingPrint("Downloaded: " + self.site.articles[i].title)
            except newspaper.article.ArticleException:
                print("Failed to download article.")

        LockingPrint("Finished dowloading from: " + self.url)
        self.isFinished = True
        return

    def isFinished(self):
        return self.isFinished

    def GetSite(self):
        return self.site

# Acquires lock, prints, then releases lock. Prevents prints from happenning simultaneously.
def LockingPrint(string):
    printingLock.acquire()
    print(string)
    printingLock.release()