from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
import random
import numpy

class InstagramBot :
    def __init__(self,username,password):
        self.loggedin = False
        self.username = username
        self.password = password
        self.base_url = "https://www.instagram.com"
        self.followersCount = 0
        self.followingCount = 0
        self.followedList = []
        self.commentlist = []
        self.doNotFollowList = [] #followed in the past but dont want to follow again
        self.whitelist = [] #users you dont want unfollowed 
        self.CreateFiles()
        self.Choose()

    def Choose(self): #UI
        if not self.loggedin:
            self.Login()
            self.GetInfo()
        print(".................")
        choice = input("[1] Follow Followers\n [2] Unfollow Followed\n[3] Unfollow All\n[4] Tag Options\n [q] for quit\nChoice:\t")
        if choice == "1":
            self.FollowFollowers()
            self.Choose()
        elif choice == "2":
            self.UnfollowFollowed()
            self.Choose()
        elif choice == "3":
            self.UnfollowAll()
            self.Choose
        elif choice == "4":
            self.TagOptions()
            self.Choose()
        elif choice == "q" :
            self.driver.close()
            return

    def ConvertToNumber(self, text): #Convert Text in to integer for adding followers
        if "k" in text:
            return int(float(text.replace("k",""))*1000)
        elif "m" in text:
            return int(float(text.replace("m",""))*1000000)
        else:
            return int(text)
    
    def Wait(self,min,max): #to get away with instagram bot detection adding a random wait period 
        time.sleep(random.choice(numpy.arange(min,max,0.1)))

    def GoToUser(self, user):
        self.driver.get("{}/{}/".format(self.base_url,user))
        self.Wait(1,2)
        

    def UnfollowUser(self, user):
        self.GetInfo(user)
        div = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]")
        button = div.find_element_by_xpath(".//button")
        if button and (button[0].text != "Follow"):
            if (len(button) > 2):
                button[1].click()
            else:
                button[0].click()
            self.Wait(1,1.5)
            self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()




        


    def CreateFiles(self): #create files for user 
        temp = open("[Followed][{}]".format(self.username),"a+")
        temp.close
        temp = open("[DoNotFollow][{}]".format(self.username),"a+")
        temp.close
        temp = open("[WhiteList][{}]".format(self.username),"a+")
        temp.close
        temp = open("[Comments][{}]".format(self.username),"a+")
        temp.close



    def ReadFiles(self):
        self.Wait(1,1.5)
        self.followedList = []
        self.whitelist = []
        self.doNotFollowList = []
        with open("[Followed][{}]".format(self.username),"r+") as flist:
            lines = flist.readlines()
            for line in lines:
                self.followedList.append(line.strip())
        with open("[DoNotFollow][{}]".format(self.username),"r+") as flist:
            lines = flist.readlines()
            for line in lines:
                self.doNotFollowList.append(line.strip())
        with open("[WhiteList][{}]".format(self.username),"r+") as flist:
            lines = flist.readlines()
            for line in lines:
                self.whitelist.append(line.strip())
        with open("[Comments][{}]".format(self.username),"r+") as flist:
            lines = flist.readlines()
            for line in lines:
                self.commentlist.append(line.strip())
        

    def AddFollowedList(self, name): #add followed user to file
        with open("[Followed][{}]".format(self.username),"a+") as flist:
            temp = name.strip() + "\n"
            flist.write(temp)
        self.ReadFiles()
        
    def AddDoNotFollowList(self,name):
        with open("[DoNotFollow][{}]".format(self.username),"a+") as flist:
            temp = name.strip() + "\n"
            flist.write(temp)
        self.ReadFiles()


    def RemFollowedList(self, name): #remove followed user to file
        with open("[Followed][{}]".format(self.username),"r") as flist:
            lines = flist.readlines()
        with open("[DoNotFollow][{}]".format(self.username),"w") as flist:
            for line in lines: ##########
                if line.strip() != name:
                    flist.write(name)
        self.ReadFiles()


    ################# Logging In #################


    def Login(self): #land on login page
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.get("{}/accounts/login".format(self.base_url))
        self.Wait(2,3)
        #found buttons using developer tools option
        self.driver.find_element_by_name("username").send_keys(self.username) #fill username given by you on login page
        self.Wait(1,2)
        self.driver.find_element_by_name("password").send_keys(self.password) #fill password given by you on login page
        self.Wait(1,2)
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click() #click on login button
        print("Logged in {}".format(self.username))
        self.loggedin = True
        self.Wait(3,4)


    def GetInfo(self): #gets followers and following
        self.GoToUser(self.username)
        #followers
        temp = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").text
        self.followersCount = self.ConvertToNumber(temp)
        #following
        temp = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a/span").text
        self.followingCount = self.ConvertToNumber(temp)
        self.ReadFiles()


    ################# Following Followers #################

    def FollowFollowers(self): #follow the followers of user
        #gets username and number of followers
        ##self.ReadFiles()
        self.ReadFiles() # In case of any changes to files
        user = input("Account username:\t")
        self.GoToUser(user)
        temp = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span").text
        numoffollowers = self.ConvertToNumber(temp)
        amount = int(input("How many to follow? (Less than {})\t".format(temp)))
        while amount > numoffollowers:
            amount = int(input("How many to follow? (Less than {})\t".format(temp)))

        # Clicks followers tab and goes through the list one by one
        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a").click()
        i, k = 1, 1
        while (k <= amount):
            self.Wait(1,1.5)
            currentUser = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]".format(i))
            button = currentUser.find_elements_by_xpath(".//button")
            name = currentUser.find_element_by_css_selector(".notranslate").text
            # If a strictly "Follow" button exists, it clicks it
            if (button) and (button[0].text == "Follow") and (name not in self.doNotFollowList):
                self.Wait(30,35)
                button[0].click()
                self.AddFollowedList(name) # Writes username to file
                self.AddDoNotFollowList(name)
                print("[{}] {} followed {}".format(k, self.username, name))
                k += 1
            self.Wait(1,1.5)
            # Scrolls down for the user to be at the top of the tab
            self.driver.execute_script("arguments[0].scrollIntoView()", currentUser)
            i += 1








    def UnfollowFollowed(self):
        self.ReadFiles()
        numoffollowed = len(self.followedList)
        amount = int(input("How many users to unfolllow? (followed {})\t".format(numoffollowed)))
        while amount >= numoffollowed :
            amount = int(input("How many users to unfolllow? (followed {})\t".format(numoffollowed)))
        for i in range(amount):
            user = self.followedList[0]
            self.Wait(10,15)
            self.UnfollowUser(user)
            self.RemFollowedList(user)
            print("[{}] {} unfollowed {}".format(i+1,self.username,user))
    

    def UnfollowAll(self):
        self.GetInfo()
        amount = int(input("How many users to unfolllow? (followed {})\t".format(self.followingCount)))
        while amount > self.followingCount:
            amount = int(input("How many users to unfolllow? (followed {})\t".format(self.followingCount)))
        
        self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a").click()
        i,k = 1,1
        while k<= amount :
            self.Wait(1,1.5)
            currentUser = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]/ul/div/li[{}]".format(i))
            button = currentUser.find_element_by_xpath(".//button")
            name = currentUser.find_element_by_css_selector(".notranslate").text
            if button and (button[0].text == "Following") and (name not in self.whitelist):
                self.Wait(10,15)
                button[0].click()
                if name in self.followedList:
                    self.RemFollowedList(name)
                if name not in self.doNotFollowList(name):
                    self.AddDoNotFollowList(name)
                self.Wait(1,2)
                self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div[3]/button[1]").click()
                print("[{}] {} unfollowed {}".format(k,self.username,name))
                k += 1
            self.Wait(1,1.5)
            self.driver.execute_script("arguments[0].scrollIntoView();",currentUser)
            i += 1   
    
    def TagOptions(self):
        tag = input("Tag:\t")
        amount = int(input("How many posts to go through:\t"))
        liketag,commenttag,following = False
        if "y" in input("Like the post? (y/n):\t").lower():
            liketag = True
        if "y" in input("Comment the post? (y/n):\t").lower():
            commenttag = True
        if "y" in input("Follow the user of post? (y/n):\t").lower():
            following = True
        #Go to Tag
        self.driver.get("{}/explore/tags/{}".format(self.base_url,tag))
        self.Wait(1,2)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]').click()
        
        for i in range(amount):
            self.Wait(10,12)
            name = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
            if liketag:
                self.Wait(1,1.5)
                likebutton = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button')
                liketext = likebutton.find_element_by_xpath(".//*[name()='svg']").get_attribute('aria-label')
                if liketext == "Like":
                    likebutton.click()
                    print("[{}] *liked* post by {}".format(i+1),name)
            if commenttag:
                self.Wait(1,1.5)
                temp = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form')
                temp.find_element_by_xpath(".//*[name()='textarea']").click()
                temp.find_element_by_xpath(".//*[name()='textarea']").send_keys(random.choice(self.commentlist))
                self.Wait(1,1.5)
                self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/button[2]').click()
                print("[{}] *commented* on post by {}".format(i+1, name))

            if following:
                self.wait(1,2)
                temp = self.driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
                if temp.text == "Follow" and name not in self.doNotFollowList:
                    temp.click()
                    self.AddFollowedList(name)
                    self.AddDoNotFollowList(name)
                    print("[{}] *followed* {}".format(i+1,name))
            if i == 0:
                self.driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a').click()
            else:
                self.driver.find_element_by_xpath('/html/body/div[5]/div[1]/div/div/a[2]').click()







                
                





TestRuns = InstagramBot("Username","Password")


# Login follow unfollow
# Unfollow all
# Like , Comment and follow based on Tags