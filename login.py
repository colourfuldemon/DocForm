from tkinter import * 
from tkinter.ttk import *
import sqlite3
import os
import smtplib, ssl

class DocForm(): #form class
    
    def __init__(self, window, tracks, conditions, difficulty, track_name, recorded_cond, username, useremail):
        '''initiator function'''
        self.conditions = conditions
        self.diff = difficulty
        self.track_name = track_name
        self.recorded_cond = recorded_cond
        self.username = username
        self.useremail = useremail
        
        
        self.title = Label(window, text="DOC Form", font=("Arial", 14))
        self.title.grid(row=0, column=1, padx=5, pady=5)
        #title of form
        
        
        self.trackname = Label(window, text='Track Name: ')
        self.trackname.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        #label for track name selection
        
        
        self.combo = Combobox(window, values=tracks, width=12)
        self.combo.selection_clear()
        self.combo.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        self.combo.bind('<<ComboboxSelected>>', self.selectedtrack) 
        #combobox that suggests the tracks in the list at the beginning
        #when selected the 'selectedtrack' function will be undergone
        
        
        self.condition = Label(window, text='Select the conditions you want to report')
        self.condition.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        #label for selecting conditions
         
           
        self.mud = Button(window, text='Muddy Track', command=self.mud)
        self.mud.grid(row=3, column=0, padx=5, pady=5)
        
        self.flood = Button(window, text='Flooding', command=self.flood)
        self.flood.grid(row=3, column=1, padx=5, pady=5)
        
        self.gravel = Button(window, text='Loose Gravel', command=self.gravel)
        self.gravel.grid(row=3, column=2, padx=5, pady=5)
        
        self.trees = Button(window, text='Fallen Trees', command=self.trees)
        self.trees.grid(row=4, column=0, padx=5, pady=5)
        
        self.slides = Button(window, text='Landslides', command=self.slides)
        self.slides.grid(row=4, column=1, padx=5, pady=5)
        
        self.ruts = Button(window, text='Rutted Track', command=self.ruts)
        self.ruts.grid(row=4, column=2, padx=5, pady=5)        
        
        
        self.diffbut = Label(window, text="Please select a difficulty 1 - 10")
        self.diffbut.grid(row=5, column=0, columnspan=2, padx=5, pady=5)    
        #label for difficulty entry
          
           
        self.difficulty = Entry(window, width=14)
        self.difficulty.grid(row=5, column=2, padx=5, pady=5)
        self.difficulty.bind('<KeyRelease>', self.getdifficulty)
        #when the user finishes their entry the 'getdifficulty' function is called
        
        
        self.complete = Button(window, text='Finalize', command=self.finalize)
        self.complete.grid(row=6, column=1, padx=5, pady=5)
        #complete button that goes to the 'finalize' function when pressed
        
        
        self.final = Label(window, text='')
        self.final.grid(row=7, column=1, padx=5, pady=5)
        #label to say 'completed' when the process is finished
    
    def selectedtrack(self, event):
        '''retrieves the selected track from the track combo box'''
        track = self.combo.get()
        self.track_name = track    
     
    def mud(self):
        '''does stuff'''
        self.recorded_cond.append("Muddy Track")
    
    def flood(self):
        '''does stuff'''
        self.recorded_cond.append("Flooding")
    
    def gravel(self):
        '''does stuff'''
        self.recorded_cond.append("Loose Gravel")
    
    def trees(self):
        '''does stuff'''
        self.recorded_cond.append("Fallen Trees")
    
    def slides(self):
        '''does stuff'''
        self.recorded_cond.append("Landslides")
    
    def ruts(self):
        '''does stuff'''
        self.recorded_cond.append("Rutted Track")    
    
    
    def getdifficulty(self, event):
        '''retrieves the difficulty entered into the entry box'''
        try:
            diff = self.difficulty.get()
            self.diff = diff
            if int(self.diff) < 0 or int(self.diff) > 10:
                raise ValueError           
        except ValueError:
            print("Please select sufficient difficulty\n")  
            os._exit(0)
        #handles input error where the user inputs a difficulty out of the given range
    
        
    def finalize(self):
        '''last part of the program, enters the information into the database'''
        self.final['text'] = "Completed!"
        
        string = ' '
        final_condition = string.join(self.recorded_cond)
            
        #ensures the condition is a string that can be entered into the database field
        
        track_name = self.track_name
        difficulty = self.diff
        conditions = final_condition
       
        import datetime
        x = datetime.datetime.now()
        date = x.strftime("%x")    
        #sets the date the form is being filled out so this does not have to be entered
    
        newrecord = (track_name.capitalize(), difficulty, conditions, date)
        #tuple of all information
    
        with sqlite3.connect("db/tracks.db") as db: #opening correct database
            cursor = db.cursor()
            cursor.execute("INSERT INTO Tracks(TrackName,Difficulty,Conditions,Date) VALUES (?,?,?,?)",newrecord) #inserts the information into the correct columns of the database
            db.commit()
            
        self.confirm()
            
    def confirm(self):
        email = self.useremail
        with sqlite3.connect('db/tracks.db') as db:
            cursor = db.cursor()
            cursor.execute("SELECT TrackID,TrackName,Difficulty,Conditions,Date from Tracks")
            tracks = cursor.fetchall()
        
        final = None
        top = 0
        for track in tracks:
            trackid, name, diff, cond, date = track
            if int(trackid) > top:
                top = int(trackid)
                    
        for track in tracks:
            if top in track:
                final = track
                
        trackid, trackname, diff, conds, date = final
               
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = 'docformconfirm@gmail.com'  # Enter your address
        receiver_email = email  # Enter receiver address
        password = 'rangerpassword'
        message = """\
Subject: Recent Entry

This message is to confirm your submission of {} on {} at {}.""".format(conds, trackname, date)
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)        
            

class Login:
    def __init__(self, window, user_pass, user_email, users):
        self.user_pass = user_pass
        self.user_email = user_email
        self.email = None
        self.user = None
        self.users = users
        self.window = window
        
        self.title = Label(window, text='Login')
        self.title.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        self.name_label = Label(window, text='Username:')
        self.name_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.name_combo = Combobox(window, values=users, width=12)
        self.name_combo.grid(row=1, column=1, padx=5, pady=5)
        
        self.pass_label = Label(window, text='Password:')
        self.pass_label.grid(row=2, column=0, padx=5, pady=5)
        
        self.pass_entry = Entry(window, width=14)
        self.pass_entry.grid(row=2, column=1, padx=5, pady=5)
        self.pass_entry.bind('<Return>', self.check)
        
        self.button = Button(window, text='Go', command=self.check_butt)
        self.button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
        
        self.error = Label(window, text='')
        self.error.grid(row=4, column=0, columnspan=2, padx=5, pady=5)        
        
    def run_form(self):
        self.window.destroy()
        root = Tk()
        
        users = self.user_email
        username = self.user
        useremail = self.email
        
        listconditions = ['Muddy Track', 'Flooding', 'Loose Gravel', 'Fallen Trees', 'Landslides', 'Rutted Track']
        difficultylevel = None #to be initiated
        track_name = None #to be initiated
        tracks = ['Routeburn', 'Milford', 'Heaphy', 'Able Tasman', 'Avalanche Peak']
        recorded_cond = []
        form = DocForm(root, tracks, listconditions, difficultylevel, track_name, recorded_cond, username, useremail)
        root.mainloop()

    def check(self, event):
        password = self.pass_entry.get()
        user = self.name_combo.get()

        try:
            if self.user_pass[password] == user:
                self.user = user
                self.email = self.user_email[user]
                self.run_form()
        except KeyError:
                self.error['text'] = 'Password Incorrect' 
            
    def check_butt(self):
        password = self.pass_entry.get()
        user = self.name_combo.get()
        
        try:
            if self.user_pass[password] == user:
                self.user = user
                self.email = self.user_email[user]
                self.run_form()
        except KeyError:
                self.error['text'] = 'Password Incorrect'    
            
            
def main():
    window = Tk()
    user_pass = {'hello':'rach', 'password':'daz'}
    user_email = {'rach':'rhodgson984@gmail.com', 'daz':'eyreriver@gmail.com'}
    users = []
    for name in user_pass.values():
        users.append(name)
    gui = Login(window, user_pass, user_email, users)
    window.mainloop()
    
main()