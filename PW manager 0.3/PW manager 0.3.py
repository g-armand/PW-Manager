# -*-coding:Utf-8 -*
#PW Manager v.0.3
#GARRIGOU Armand

"""A password manager, to practice my understanding of Python"""
#not the best, but mine

"""
Changelog:
- no more identification process (get rid of storing the main password)
- cryption algorythm is now a vigenere cipher, safer than ceasar cypher but still unsafe
"""



import os.path                              #check external files's availability
from pickle import Pickler, Unpickler       #communicate with external files
import random                               #generation of passwords
import functools                            #functools.partial in order to create unique functions and objects, way to avoid specific issues in the program
import tkinter as tk                        #GUI module


class Pw_management(): #only one object will be created from this class: (Pw_management.pwmanagement), it will work as the main account
    """
    Mother class of this project
    will have two main instances:
    - self.key : an integer user through encryption and decryption
    - self._datas_list : a list containing a list per account (self._datas_list = [[app, id, password], [app, id, password], ... ])

    every method defined in this class are back-end methods
    """
    def __init__(self, key):

        self.key = key

        #creation of a pwmanagement._datas_list filled with datas stored in datas.file
        self._datas_list = self.unpack_datas()



    def apply_crypter(self, apply_uncrypter = False): #main cryption method, it's used through the whole program

        """
        consecutively crypts every datas contained in Pw_management.pwmanagement._datas_list,
        self.crypter method is used to actually crypt and decrypt datas
        it will iterate through the list according to the following pattern:
        list[0][0] -> list[0][1] -> list[0][2] -> list[1][0] -> list[1][1] -> list[1][2] -> list[2][0] ... list[-1][-1]
        """
        if apply_uncrypter:
            for i, elt in enumerate(self._datas_list):
                for index, element in enumerate(self._datas_list[i]):
                    self._datas_list[i][index] = self.vign(text = element, key = self.key, uncrypter = True)

        if not apply_uncrypter:
            for i, elt in enumerate(self._datas_list):
                for index, element in enumerate(self._datas_list[i]):
                    self._datas_list[i][index] = self.vign(text = element, key = self.key)


    def vign(self, text='', key='', uncrypter = False):
        #    if not txt:
        #        print 'Needs text.'
        #        return
        #    if not key:
        #        print 'Needs key.'
        #        return
        #    if typ not in ('d', 'e'):
        #        print 'Type must be "d" or "e".'
        #        return
        #    if any(t not in universe for t in key):
        #        print 'Invalid characters in the key. Must only use ASCII symbols.'
        #        return

        #all ASCII characters (except '\') shuffled to avoid easy patterns emerging in stocked cipher texts
        alphanum ="""Xu5Y_=)*q~3eQHc^x9,kSUp7K"@-:#h<gZ`G&I$Oy[?Dn}r{ov'C|(AMWE6NlPL+fVj1/t;iz4Jm.d%!0]FTs2bRB>8wa """ #len = 94
        cypher = ''
        len_key = len(key)

        for index, text_letter in enumerate(text):

            if text_letter not in alphanum:
                cypher += text_letter
            else:

                key_letter = key[index % len_key]

                text_index = alphanum.index(text_letter)
                key_index = alphanum.index(key_letter)

                if uncrypter:
                    cypher += alphanum[(text_index + key_index) % 94]

                if not uncrypter:
                    cypher += alphanum[(text_index - key_index) % 94]



        return cypher


    def unpack_datas(self):
        """
        interacts with 'datas' file,
        depending if the file is already created or not it will return its content
        Pickler and Unpickler are used through the method
        """
        if os.path.isfile("datas"):                     #if 'datas' is already created, everything is fine
            pass

        elif not os.path.isfile("datas"):               #if 'datas' is not created,
            empty_list = []                             #we create an empty list, and dump it in 'datas' which is automatically created
            with open('datas', 'wb') as file_datas:
                pickler_datas = Pickler(file_datas)
                pickler_datas.dump(empty_list)

        with open('datas', 'rb') as file_datas:         #then we access 'datas' and store its content within the variable 'datas', which is then returned
            unpickler_datas = Unpickler(file_datas)
            datas = unpickler_datas.load()
            return datas


    def pack_datas(self):
        """
        interacts with 'datas' file.
        it dumps 'self.pwmanagement._datas_list' in 'datas'
        this function is called every time we need to save and store new or modified accounts
        """
        with open('datas', 'wb') as datas_file:
            pickler_datas = Pickler(datas_file)
            pickler_datas.dump(self.pwmanagement._datas_list)



# tkinter GUI class
class Window(tk.Tk, Pw_management):             #double inheritance was needed here in order to give 'Window' all methods from 'tk.Tk' to build a GUI
                                                #and from 'Pw_management' to manipulate datas in the backgroud and make the program run properly
    """
    This class create its own pages, and is kind of self-powered since everything is based on OOP in this program.
    Every interface is defined by methods and communicate with other methods in order to provide a interactive program to the user
    methods used for displaying the interface are tagged as "FRONT-END", the ones running in the background are tagged as "BACK-END"
    """
    def __init__(self):
        super(Window, self).__init__()

        #definition of window parameters
        self.title('Pw Manager')
        self.geometry('500x500')
        self.config(background = '#adcfeb')
        self.iconbitmap('visu/lock.ico')

        #creation of a scrollable main frame
        self.container = tk.Frame(self, bg = '#808080')                                                 #it is needed to build a frame, containing a scrollbar and a canvas,
        self.canvas = tk.Canvas(self.container, bg= '#C0C0C0')                                          #in order to supply another container('self.canvas') for the main frame ('self.frame')
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)     #in wich every widgets will be displayed. This is a way to make this last frame scrollable
        self.frame = tk.Frame(self.canvas, bg ='#808080')                                               #which can be tricky with tkinter module
                                                                                                        #note that we don't .pack() them because they will be destroyed and recreated immediately once the program is opened

        #images that will be used to avoid redundancy in the interface, providing a more readable and friendly environement for the user
        self.image_app = tk.PhotoImage(file = "visu/app.png")
        self.image_user = tk.PhotoImage(file = "visu/user.png")
        self.image_pw = tk.PhotoImage(file = "visu/password.png")

        #re-sizing
        self.image_app = self.image_app.subsample(2)
        self.image_pw = self.image_pw.subsample(2)
        self.image_user = self.image_user.subsample(2)

        #once 'self.Window' object is created we need to call this first menu in order to display it on the screen
        self.identification_menu()

        #call of the 'mainloop()' method in order to create an actual window, that will stay open as much as we want
        self.mainloop()

    def set_new_frame(self):
        """
        FRONT_END
        this method need to be called before building any new interface,
        it avoids redundancy in code, and garantee a standardized and blank space
        """
        #it is needed to destroy all those container widgets before recreating them in order to keep a blank interface to build new menus
        self.frame.destroy()
        self.container.destroy()
        self.canvas.destroy()
        self.scrollbar.destroy()

        #same widgets created within the '__init__' method
        self.container = tk.Frame(self, bg = '#adcfeb')
        self.canvas = tk.Canvas(self.container, highlightthickness = 0, bg= '#adcfeb', width = 423)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas,  bg ='#adcfeb')

        #display container widgets defined above with '.pack()' method
        self.container.pack(fill="both", expand=True)
        self.canvas.pack(side = "left", fill = "y", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        #note that only 'self.frame' hasn't been packed

        #here we simulate '.pack()' on self.frame by implementing it within 'self.canvas'
        self.canvas.create_window((100,100), window=self.frame, anchor= 'nw')

        #setting the vertical movement of self.scrollbar to scroll over 'self.canvas'
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        #redirection of the scrolling movement defined above to scroll over self.frame
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def identification_menu(self):
        """
        FRONT-END
        first menu, according to wheter or not there is a file named "identification" it shows two different messages
        and two different buttons leading to two different methods defined below ('identification_to' and 'first_identification')
        """

        self.set_new_frame()
        #label asking for the password
        self.text = tk.Label(self.frame, text = "entrez votre identifiant", bg = "#adcfeb", height = 1, width =24, font = ("arial", 10, "bold"))
        self.text.pack()
        #entry to fill with main password
        self.entry = tk.Entry(self.frame, bg = "#aeceea", width = 30)
        self.entry.pack()
        #spacer
        tk.Label(self.frame, bg = '#adcfeb', height = 1, width = 14).pack()
        #button leading to 'self.identification_to'
        self.validate_button = tk.Button(self.frame, text = "OK", width = 10, command = self.identification, bd = 3, bg = '#88b7dd', activebackground = "#88b7dd", font = ("arial", 10, "bold"))
        self.validate_button.pack()


    def identification(self):
        """
        BACK-END
        Gets the entry from 'self.identification_menu' and generates a key from it
        this key will be crypted and then will be used to generate 'pwmanagement' the only object from the 'Pw_management' class
        """

        #Get the password from entry in "self.identification_menu"
        key = self.entry.get()

        #create the 'Pw_management' object named 'pwmanagement', that we will use every time in this program
        self.pwmanagement = Pw_management(key)

        #send to main menu
        self.main_menu()

    def main_menu(self):
        """
        FRONT-END
        main menu, all buttons are looking identical and lead to their own sub-menu
        """
        self.set_new_frame()

        self.label_menu = tk.Label(self.frame, text = "Choisissez une option", bg = "#adcfeb", height = 3, width =25, relief = 'sunken', bd = 3, font = ("arial", 10, "bold"))
        self.label_menu.grid(row = 0, columnspan = 2)

        self.bouton_1 = tk.Button(self.frame, text = "gerer les mots de passes", command = self.menu_gestion_mdp, height = 5, width = 25, wraplength = 150, bd = 3, bg = "#88b7dd", activebackground = "#88b7dd", font = ("arial", 10, "bold"))
        self.bouton_1.grid(column = 0, row = 1)
        self.bouton_2 = tk.Button(self.frame, text = "Tout afficher", command = self.menu_afficher_tout_mdp, height = 5, width = 25, wraplength = 150, bd = 3, bg = "#88b7dd", activebackground = "#88b7dd", font = ("arial", 10, "bold"))
        self.bouton_2.grid(column = 0, row = 2)
        self.bouton_3 = tk.Button(self.frame, text = "Nouveau mot de passe", command = self.append_account_menu, height = 5, width =25, wraplength = 150, bd = 3, bg = "#88b7dd", activebackground = "#88b7dd", font = ("arial", 10, "bold"))
        self.bouton_3.grid(column = 1, row = 1)
        self.bouton_Q = tk.Button(self.frame, text = "Quitter le programme", command = self.quit_PW_management, height = 5, width = 25, wraplength = 150, bd = 3, bg = "#88b7dd", activebackground = "#88b7dd", font = ("arial", 10, "bold"))
        self.bouton_Q.grid(column = 1, row = 2)


    def menu_gestion_mdp(self):
        """
        FRONT-END
        Menu dedicated to manage (edit and delete) accounts, it only shows the app and the id for EACH account
        """

        self.set_new_frame()
        zero = 0 #as we will be using '.grid()' we need to increment 'zero' every time we need to display another account, avoiding overlaping buttons and label

        self.pwmanagement.apply_crypter(apply_uncrypter = True) #uncryption of datas that need to be displayed

        for index, elt in enumerate(self.pwmanagement._datas_list):

            #displaying images instead of text in front of each accounts, to avoid redundancy
            label_app = tk.Label(self.frame, image = self.image_app , width = 30, bg = "#adcfeb")
            label_id = tk.Label(self.frame, image = self.image_user, width = 30, bg = "#adcfeb")
            label_app.grid(row = zero + 1 , column = 0 )
            label_id.grid(row = zero + 2 , column = 0 )

            #each buttons will display the app and id for every accounts
            button_app_rep = tk.Button(self.frame, text = str(self.pwmanagement._datas_list[index][0]), bg = "#88b7dd", height = 1, width = 14, font = ("arial", 10, "bold"))
            button_id_rep = tk.Button(self.frame, text = str(self.pwmanagement._datas_list[index][1]), bg = "#88b7dd", height = 1, width = 14, font = ("arial", 10))
            button_app_rep.grid(row = zero + 1 , column = 1)
            button_id_rep.grid(row = zero + 2 , column = 1 )

            #button leading to password_edit_menu, "functools.partial()" is used to create an unique function out of each button
            #not using 'functools.partial()' would cause issues since every buttons would lead toward 'self.account_edit_menu' but only using the last index of the list...
            button_update_pw = tk.Button(self.frame, text = "modifier", width = 8, height = 3, bg = '#88b7dd',font = ("arial", 10, "bold"), command = functools.partial(self.edit_account_menu, index = index))
            button_update_pw.grid(row = zero+1, column = 2, rowspan = 2)

            #button leading to 'self.delete_password()'
            button_erase_mdp = tk.Button(self.frame, text = "supprimer", width = 8, height = 3, bg = '#88b7dd',font = ("arial", 10, "bold"), command = functools.partial(self.suppression_mdp, index = index) )
            button_erase_mdp.grid(row = zero+1, column = 3, rowspan = 2)

            #spacer
            tk.Label(self.frame, bg = '#adcfeb', height = 1).grid(row = zero+4, column = 0, columnspan = 2)

            zero += 4
        self.pwmanagement.apply_crypter() #cryption of datas

        #button leading to main menu
        bouton_to_main_menu = tk.Button(self.frame, text = 'Menu Principal', bg = '#88b7dd',font = ("arial", 10, "bold"), command = self.main_menu)
        bouton_to_main_menu.grid(row = zero +1000 , column = 0, columnspan = 4)

    def edit_account_menu(self, index):
        """
        FRONT-END
        Allows the user to change account's datas.
        Displays datas from the selected account in 'self.manage_password_menu' in entry widgets,
        the datas can remain untouched, the user need to press 'validate_button' in order to save changes
        """
        self.set_new_frame()

        #storing account's datas as StringVar() objects will allow us to pre-fill the entry widgets and to access them once 'validate_button' is pressed
        self.pwmanagement.apply_crypter(apply_uncrypter = True)
        app = tk.StringVar(self.frame, value = self.pwmanagement._datas_list[index][0])
        identifiant = tk.StringVar(self.frame, value = self.pwmanagement._datas_list[index][1])
        mdp =  tk.StringVar(self.frame, value = self.pwmanagement._datas_list[index][2])
        self.pwmanagement.apply_crypter()

        #images in front of each line of the account's datas
        label_app = tk.Label(self.frame, image = self.image_app , width = 30, compound = "right", bg = "#adcfeb")
        label_id = tk.Label(self.frame, image = self.image_user, width = 30, compound = "right", bg = "#adcfeb")
        label_pw = tk.Label(self.frame, image = self.image_pw, width = 30, bg = "#adcfeb")
        label_app.grid(row = 0 , column = 0 )
        label_id.grid(row = 1 , column = 0 )
        label_pw.grid(row = 2, column = 0)

        #if these entry widgets remain untouched by user, the datas will remain the same, but if any of them is overwritten, the content will be updated thanks to 'self.account_updating'
        self.entry_app = tk.Entry(self.frame, bg = '#88b7dd', textvariable = app)
        self.entry_id = tk.Entry(self.frame, bg = '#88b7dd', textvariable = identifiant)
        self.entry_pw = tk.Entry(self.frame, bg = '#88b7dd', textvariable = mdp)
        self.entry_app.grid(row = 0, column = 1)
        self.entry_id.grid(row = 1, column = 1)
        self.entry_pw.grid(row = 2, column = 1)

        #button filling the entry with a random password if pressed
        random_pw_button = tk.Button(self.frame,text = 'Générer', bg = '#88b7dd',font = ("arial", 10, "bold"), command = self.set_random_password)
        random_pw_button.grid(row = 2 , column = 2)

        #spacer
        tk.Label(self.frame, bg = '#adcfeb', height = 1).grid(row = 3, column = 0)

        #every string in each entry will be used by 'self.accout_updating'
        validate_button = tk.Button(self.frame, text = "Valider", bg = "#88b7dd", font = ("arial", 10, "bold"), command = functools.partial(self.account_updating, i = index))
        validate_button.grid(row = 4, column = 0, columnspan = 2)


    def account_updating(self, new_account = False, i = 0):
        """
        BACK-END
        this function will access the entries and append them to the main list as a new account
        """
        #checking if the account need to be updated or if it is a fresh new account
        if new_account == False:
            self.pwmanagement._datas_list.pop(i)
        elif new_account == True:
            pass

        #creation of a list with all the datas needed to create/update the account
        app = self.entry_app.get()
        identifiant = self.entry_id.get()
        pw = self.entry_pw.get()
        new_account = [app, identifiant, pw]

        #update of the list
        self.pwmanagement.apply_crypter(apply_uncrypter = True)
        self.pwmanagement._datas_list.append(new_account)
        self.pwmanagement.apply_crypter()

        #back to main menu and update of the datas' file
        self.main_menu()
        self.pack_datas()

    def suppression_mdp(self, index):
        """
        BACK-END
        thanks to the 'index' parameter the function will erase the account at that particular parameter
        """

        self.pwmanagement._datas_list.pop(index)

        #back to main menu and update of the datas' file
        self.main_menu()
        self.pack_datas()

    def menu_afficher_tout_mdp(self):
        self.set_new_frame()
        """
        FRONT-END
        This menu will display every accounts on the same page, every datas will be displayed on buttons that can be clicked to append to clipboard
        """
        #uncryption of self.pwmanagement._datas_list
        self.pwmanagement.apply_crypter(apply_uncrypter = True)
        zero = 0

        for index, data in enumerate(self.pwmanagement._datas_list):

            #images in front of each row of datas to avoid redundancy
            label_app = tk.Label(self.frame, image = self.image_app , width = 30, compound = "right", bg = "#adcfeb")
            label_id = tk.Label(self.frame, image = self.image_user, width = 30, compound = "right", bg = "#adcfeb")
            label_pw = tk.Label(self.frame, image = self.image_pw, width = 30, bg = "#adcfeb")
            label_app.grid(row = zero + 1 , column = 0 )
            label_id.grid(row = zero + 2 , column = 0 )
            label_pw.grid(row = zero + 3, column = 0)

            #every button displays its own data (app, id or password) from each account and can be clicked to append its content to clipboard (thanks again to functools.partial())
            button_app_rep = tk.Button(self.frame, text = str(self.pwmanagement._datas_list[index][0]), bg = "#88b7dd", height = 1, width = 14, font = ("arial", 10, "bold"))
            button_id_rep = tk.Button(self.frame, text = str(self.pwmanagement._datas_list[index][1]), bg = "#88b7dd", height = 1, width = 14, font = ("arial", 10), command = functools.partial(self.append_to_clipboard, first_index = index, second_index = 1))
            button_mdp_rep = tk.Button(self.frame, text = str(self.pwmanagement._datas_list[index][2]), bg = "#88b7dd", height = 1, width = 14, font = ("arial", 10), command = functools.partial(self.append_to_clipboard, first_index = index, second_index = 2))
            button_app_rep.grid(row = zero + 1 , column = 1)
            button_id_rep.grid(row = zero + 2 , column = 1 )
            button_mdp_rep.grid(row = zero + 3 , column = 1 )

            #spacer
            label_separateur = tk.Label(self.frame, bg = '#adcfeb', height = 1, width = 14)
            label_separateur.grid(row = zero+4, column = 0, columnspan = 2)

            zero += 4

        #cryption
        self.pwmanagement.apply_crypter()

        #sends back to main menu
        button_to_main_menu = tk.Button(self.frame, text = 'Menu Principal', bg = '#88b7dd', command = self.main_menu)
        button_to_main_menu.grid(row = zero+1000, column = 0, columnspan = 2)

    def append_to_clipboard (self, first_index, second_index):
        """
        BACK-END
        clears the cliboard's content and copy to it the data from 'self.pwmanagement._datas_list' according to the first and second index parameters
        """
        self.pwmanagement.apply_crypter(apply_uncrypter = True)
        self.clipboard_clear()
        self.clipboard_append(self.pwmanagement._datas_list[first_index][second_index])
        self.pwmanagement.apply_crypter()


    def append_account_menu(self):
        """
        FRONT-END
        offers to creates a new account, the users seeds to fill the entries
        the new account is created once 'button_add_new_pw' is pressed
        """
        self.set_new_frame()

        #Labels in front of each entry, describing what needs to be put in those entries
        self.label_app = tk.Label(self.frame, text = "Application", height = 1, width = 14, relief = "raised", bd = 1, bg = "#88b7dd", font = ("arial", 10, "bold"))
        self.label_id = tk.Label(self.frame, text = "Identifiant", height = 1, width = 14, relief = "raised", bd = 1, bg = "#88b7dd", font = ("arial", 10, "bold"))
        self.label_mdp = tk.Label(self.frame, text = "Mot de Passe", height = 1, width = 14, relief = "raised", bd = 1, bg = "#88b7dd", font = ("arial", 10, "bold"))
        self.label_app.grid(row = 1 , column = 0 )
        self.label_id.grid(row = 2 , column = 0 )
        self.label_mdp.grid(row = 3 , column = 0 )

        #entries that need to be filled and that will be accessed in 'self.append_new_account'
        self.entry_app = tk.Entry(self.frame, bg = "#aeceea")
        self.entry_id = tk.Entry(self.frame, bg = "#aeceea")
        self.entry_pw = tk.Entry(self.frame, bg = "#aeceea")
        self.entry_app.grid(row = 1 , column =1)
        self.entry_id.grid(row = 2 , column =1 )
        self.entry_pw.grid(row = 3 , column =1 )

        #button calling 'self.set_random_password', genereting a random password in self.entry_pw
        self.random_pw_button = tk.Button(self.frame,text = 'Générer', bg = '#88b7dd',font = ("arial", 10, "bold"), command = self.set_random_password)
        self.random_pw_button.grid(row = 3 , column =2)

        #spacer
        tk.Label(self.frame, bg = '#adcfeb', height = 1, width = 14).grid(row = 4, column = 0)

        #button leading to 'self.account_updating'
        self.button_add_new_pw = tk.Button(self.frame, text = 'Enregistrer', bg = '#88b7dd',font = ("arial", 10, "bold"), command = functools.partial(self.account_updating, new_account = True))
        self.button_add_new_pw.grid(row = 5, column = 0, columnspan = 2)

        #spacer
        tk.Label(self.frame, bg = '#adcfeb', height = 1, width = 14).grid(row = 6, column = 0)

        #button leading to main menu
        main_menu_button = tk.Button(self.frame, text = 'Menu Principal', bg = '#88b7dd',font = ("arial", 10, "bold"), command = self.main_menu )
        main_menu_button.grid(row = 7, column = 0, columnspan = 2)

    def set_random_password(self):
        """
        BACK-END
        Generates a random string of 12 randomly selected letters and fills the "self.entry_pw" widget, used in 'self.append_account_menu()' and 'self.edit_account_menu'
        """
        #clearing any text within the entry, allows to call the function many times without having to erase the text manually
        self.entry_pw.delete(0, 'end')

        alphanum = """Xu5Y_=)*q~3eQHc^x9,kSUp7K"@-:#h<gZ`G&I$Oy[?Dn}r{ov'C|(AMWE6NlPL+fVj1/t;iz4Jm.d%!0]FTs2bRB>8wa """ #len = 94
        count = 0
        random_password = ""

        #the password's lenght will be 12, a random letter is appended to 'random_password' at every loop
        while count < 12:
            random_password += random.choice(alphanum)
            count += 1

        #overwritting the entry widget with new password
        self.entry_pw.insert(0, random_password)

    def quit_PW_management(self):
        """
        BACK-END
        function accesed from main menu by clicking 'button_Q',
        it closes properly the program's window by quitting it (quitting self.mainloop()) and destroying it properly
        """
        self.quit()
        self.destroy()


#creation of 'mywindow', object from 'Window' class
mywindow = Window()

