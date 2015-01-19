import re
from robobrowser import RoboBrowser
import requests

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2



import tkinter as tk

import tkinter.filedialog
 
class ExampleApp(tk.Frame):

    def __init__(self, master):
        # Initialize window using the parent's constructor
        tk.Frame.__init__(self,
                          master,
                          width=800,
                          height=600)
        
        self.master.title('NZBGeek Mass Downloader')
        self.pack_propagate(0)
        self.pack()

        self.userNameLabel = tk.Label(self,text="NZBGeek username")
        self.passwordLabel = tk.Label(self,text="Password")
        self.searchLabel = tk.Label(self,text="Search Terms:")
        self.patternLabel = tk.Label(self,text="Pattern to match for:")
        self.logLabel = tk.Label(self,text="Files to be downloaded:")


        self.username_var = tk.StringVar()
        self.username = tk.Entry(self,textvariable=self.username_var)
        self.username_var.set('')

        self.password_var = tk.StringVar()
        self.password = tk.Entry(self,textvariable=self.password_var)
        self.password_var.set('')


        
 
        # The recipient text entry control and its StringVar
        self.search_var = tk.StringVar()
        self.search = tk.Entry(self,textvariable=self.search_var)
        self.search_var.set('')

        

        self.patternStr_var = tk.StringVar()
        self.patternStr = tk.Entry(self,textvariable=self.patternStr_var)
        self.patternStr_var.set('')

        
        self.logBox = tk.Text(self, wrap=tk.NONE, setgrid=True)
        self.scrollb = tk.Scrollbar(self.logBox, orient=tk.VERTICAL)
        self.scrollb.config(command = self.logBox.yview)
        self.logBox.config(yscrollcommand = self.scrollb.set)
        self.logBox.grid(column=0, row=0)
        self.scrollb.grid(column=1, row=0, sticky=tk.S+tk.N)
        
        self.go_button = tk.Button(self,text='Go',command=self.print_out)
        self.directory_button = tk.Button(self,text='Choose directory',command=self.prompt_for_directory)
        self.directoryLabel = tk.Label(self,text="")
 
        self.go_button.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.userNameLabel.pack(fill=tk.X, side=tk.TOP)
        self.username.pack(fill=tk.X, side=tk.TOP)
        self.passwordLabel.pack(fill=tk.X, side=tk.TOP)
        self.password.pack(fill=tk.X, side=tk.TOP)
        self.searchLabel.pack(fill=tk.X, side=tk.TOP)
        self.search.pack(fill=tk.X, side=tk.TOP)
        self.patternLabel.pack(fill=tk.X, side=tk.TOP)
        self.patternStr.pack(fill=tk.X, side=tk.TOP)
        self.logLabel.pack(fill=tk.X, side=tk.TOP)
        self.logBox.pack(fill=tk.X, side=tk.TOP)
        self.directory_button.pack(fill=tk.X, side=tk.TOP)
        self.directoryLabel.pack(fill=tk.X, side=tk.TOP)

        
 
    def print_out(self):
        
        print('Searching for %s!' % (self.search_var.get()))
        browser = RoboBrowser(history=True)
        browser.open('http://nzbgeek.info')

        form = browser.get_form(action="member.php")
        form['username'].value = self.username_var.get()
        form['password'].value = self.password_var.get()
        browser.submit_form(form)
        pagecount = 1
        searchTerms = self.search_var.get()
        browser.open('https://nzbgeek.info/geekseek.php?moviesgeekseek=1&browsecategory=&browseincludewords='+searchTerms+'&p-page='+str(pagecount)+'#p')

        while(len(browser.select('#browsetable')) > 0):
            titles = [tag.string for tag in browser.select('.HighlightTVRow2 .title b') if tag]
            links = [res.get('href') for res in browser.select('.icon_nzb a') if res]
            for i in range(0,len(titles) -1):
                if re.search(r'' + self.patternStr_var.get(), titles[i]):
                    self.download_file(titles[i],links[i],self.dirVar)
                    
            pagecount += 1
            browser.open('https://nzbgeek.info/geekseek.php?moviesgeekseek=1&browsecategory=&browseincludewords='+searchTerms+'&p-page='+str(pagecount)+'#p')
        print("Search completed!")
    def run(self):
        self.mainloop()

    def download_file(self,title,link,destinationDir):
        self.logBox.insert('end',str(title) + " - " + str(link) + '\n')
        rq = urllib2.Request(link)
        res = urllib2.urlopen(rq)
        nzb = open(self.dirVar + "/" + title + ".nzb", 'wb')
        nzb.write(res.read())
        nzb.close()

    def prompt_for_directory(self):
        dirname = tkinter.filedialog.askdirectory()
        if dirname:
            self.dirVar = dirname
            self.directoryLabel['text'] = self.dirVar
            print(self.dirVar)
 
app = ExampleApp(tk.Tk())
app.run()
