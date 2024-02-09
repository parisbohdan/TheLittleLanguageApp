import tkinter as tk
import time
import math
from datetime import date
import pyautogui
from PIL import Image, ImageTk
from tkinter import PhotoImage
import os
import random
import pygame
import sqlite3
db_conn = sqlite3.connect('Database/TLLA.db')
db_curs = db_conn.cursor()
tb_XP = "ExperiencePointsTable"

PathToSounds = "C:/Users/bohda\Documents/Python Codes/TheLittleLangaugeApp/Audios/"
PathToImages = "C:/Users/bohda/Documents/Python Codes/TheLittleLangaugeApp/Images/"

# Support Functions
Endings_AR = ("o","as","a","amos","áis","an")
Endings_ER = ("o","es","e","emos","eis","en")
Endings_IR = ("o","es","e","imos","ís","en")
Persona = ("Yo","Tú","Él-Ella-Usted","Nosotros","Vosotros","Ustedes")

def CalculateLevel():
    get_all_xp_query = f'select * from {tb_XP}'
    XP_Table_Values = db_curs.execute(get_all_xp_query)
    XP_Table_Results = XP_Table_Values.fetchall()
    if not XP_Table_Results:
        CurrentLevel = 1
    else:
        TotalXP = 0
        for XP_ITEM in XP_Table_Results:
            TotalXP += XP_ITEM[0]
        CurrentLevel=1+math.floor(TotalXP/(2000)) #Needs more work
    return CurrentLevel


def return_current_date(): #Thanks to https://www.toppr.com/guides/python-guide/tutorials/python-date-and-time/datetime/current-datetime/how-to-get-current-date-and-time-in-python/#:~:text=Using%20the%20Datetime%20Module&text=The%20datetime%20module's%20now(),dd%20hh%3Amm%3Ass.
    today = date.today()
    # dd/mm/yy
    date1 = today.strftime('%d/%m/%Y')
    print('date1 =', date1)
    return date1

def return_current_time(): #Thanks to https://www.toppr.com/guides/python-guide/tutorials/python-date-and-time/datetime/current-datetime/how-to-get-current-date-and-time-in-python/#:~:text=Using%20the%20Datetime%20Module&text=The%20datetime%20module's%20now(),dd%20hh%3Amm%3Ass.
    # storing the current time in the variable
    # using now() to get current time
    import datetime
    return datetime.datetime.now().time()



def AddXPToTable(XP_Number, ActivityID = 999999000000):
    add_XP_to_table_query = f'INSERT INTO {tb_XP} (XP, ActivityDate, ActivityTime, ActivityID) VALUES ({XP_Number},"{return_current_date()}","{return_current_time()}",{ActivityID})'
    db_curs.execute(add_XP_to_table_query)
    db_conn.commit()

def ResetXPTable():
    clear_XP_table_query = f'DELETE FROM {tb_XP}'
    db_curs.execute(clear_XP_table_query)
    db_conn.commit()

def ResetKnownWords():
    table_of_known_words = "KnownWords"
    # SQL command to delete all records from the specified table
    delete_query = f'DELETE FROM {table_of_known_words};'
    # Execute the SQL command
    db_curs.execute(delete_query)

    # Commit the changes
    db_conn.commit()
    
    print(f"All records from '{table_of_known_words}' have been deleted.")

def AddToKnownWords(SpanishWord):
    table_of_known_words = "KnownWords"
    table_of_available_words = "SpanishWordsAvailable"
    TransferFunction = db_curs.execute(f'select * from {table_of_available_words} WHERE "SpanishWord" = "{SpanishWord}";')
    TransferFunctionRESULT = TransferFunction.fetchall()
    if not TransferFunctionRESULT:  # Check if WORDZOS is empty
        print("Failed") # Must elaborate more
    else:
        print(TransferFunctionRESULT[0][0])
        insert_query = f'INSERT INTO {table_of_known_words} (SpanishWord, SpanishWordThe, EnglishWord) VALUES ("{TransferFunctionRESULT[0][0]}","{TransferFunctionRESULT[0][1]}","{TransferFunctionRESULT[0][2]}");'
        db_curs.execute(insert_query)
        db_conn.commit()


############################## The following code is thanks to https://stackoverflow.com/users/8295318/squareroot17 and chatGPT 4.
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtexttip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        self._showtip_common()
        label = tk.Label(self.tipwindow, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def showimagetip(self, image_path):
        "Display image in tooltip window"
        self.image_path = image_path
        if self.tipwindow or not self.image_path:
            return
        self._showtip_common()
        self.image = PhotoImage(file=self.image_path)
        label = tk.Label(self.tipwindow, image=self.image, background="#ffffe0", relief=tk.SOLID, borderwidth=1)
        label.image = self.image  # Keep a reference!
        label.pack(ipadx=1)

    def _showtip_common(self):
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tk.Toplevel(self.widget)
        self.tipwindow.wm_overrideredirect(1)
        self.tipwindow.wm_geometry("+%d+%d" % (x, y))

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateTextToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtexttip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def CreateImageToolTip(widget, image_path):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showimagetip(image_path)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def play_sound(SOUND):
    pygame.mixer.init()
    pygame.mixer.music.load(PathToSounds + SOUND)
    pygame.mixer.music.play()

def clear_window(window):
    """
    Clear all widgets from a Tkinter window.

    Args:
    window (tk.Tk): The Tkinter window from which to remove all widgets.
    """
    for widget in window.winfo_children():
        widget.destroy()

def resize_image_to_height(image_path, target_height):
    """
    Resize an image to a specific height while maintaining aspect ratio.

    Args:
    image_path (str): The path to the image file.
    target_height (int): The target height in pixels.

    Returns:
    PIL.Image: The resized image.
    """
    with Image.open(image_path) as img:
        # Calculate the new width maintaining the aspect ratio
        aspect_ratio = img.width / img.height
        new_width = int(target_height * aspect_ratio)

        # Resize the image using LANCZOS resampling
        resized_img = img.resize((new_width, target_height), Image.Resampling.LANCZOS)

        return resized_img

def get_image_filenames(folder_path):
    # Define a set of common image file extensions
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}

    # List all files in the given folder
    files = os.listdir(folder_path)

    # Filter out files that are not images
    image_files = [file for file in files if os.path.splitext(file)[1].lower() in image_extensions]

    return image_files

def get_sound_filenames(folder_path):
    # Define a set of common image file extensions
    sound_extensions = {'.mp3', '.wav'}

    # List all files in the given folder
    files = os.listdir(folder_path)

    # Filter out files that are not images
    sound_files = [file for file in files if os.path.splitext(file)[1].lower() in sound_extensions]

    return sound_files

Screen_Settings = {
    'screen_width' : 1920,
    'screen_height' : 1080
}

def Random_Grid_Generate_Solo(Length):
    Grid_Layout=[]
    for i in range(0,Length):
        location_is = random.randint(0,Length-1)
        while location_is in Grid_Layout:
            location_is = random.randint(0,Length-1)
        Grid_Layout.append(location_is)
    return Grid_Layout

# Questions (templates)

def Correct_Image_From_Audio():
    def Correct_Answer_Chosen():
        label_correct = tk.Label(window, text="correcto")
        label_correct.grid(row=3,column=0)
        button_next_question = tk.Button(window, text="próxima pregunta", command=lambda: Correct_Image_From_Audio())
        button_next_question.grid(row=4,column=0)

    def Incorrect_Answer_Chosen():
        label_incorrect = tk.Label(window, text="no correcto")
        label_incorrect.grid(row=3,column=0)    
    
    clear_window(window)
    Audio_Sample = sound_files[random.randint(0,len(sound_files)-1)]
    Random_Images = []
    for i in range(0,3):
        image_name_to_add = image_files[random.randint(0,len(image_files)-1)]
        while (image_name_to_add in Random_Images) or (image_name_to_add == Audio_Sample[:-4] + ".jpg"):
            image_name_to_add = image_files[random.randint(0,len(image_files)-1)]
        Random_Images.append(image_name_to_add)
    
    Image_2, Image_3, Image_4 = Random_Images[0], Random_Images[1], Random_Images[2]

    PlaySoundButton = tk.Button(window,text="Reproducir sonido", command=lambda: play_sound(Audio_Sample))
    PlaySoundButton.grid(row=0,column=0)

    # Generate random grid 2x2
    Grid_System_Row = Random_Grid_Generate_Solo(2)
    Grid_System_Col = Random_Grid_Generate_Solo(2)


    global tk_image_correct, tk_image_2, tk_image_3, tk_image_4
    image_correct = resize_image_to_height(PathToImages + Audio_Sample[:-4] + ".jpg", 200)
    tk_image_correct = ImageTk.PhotoImage(image_correct)
    button_correct = tk.Button(window, image=tk_image_correct, command=Correct_Answer_Chosen)
    button_correct.grid(row=Grid_System_Row[0]+1,column=Grid_System_Col[0])

    image_2 = resize_image_to_height(PathToImages + Image_2, 200)
    tk_image_2 = ImageTk.PhotoImage(image_2)
    button_image_2 = tk.Button(window, image=tk_image_2, command=Incorrect_Answer_Chosen)
    button_image_2.grid(row=Grid_System_Row[0]+1,column=Grid_System_Col[1])
    
    image_3 = resize_image_to_height(PathToImages + Image_3, 200)
    tk_image_3 = ImageTk.PhotoImage(image_3)
    button_image_3 = tk.Button(window, image=tk_image_3, command=Incorrect_Answer_Chosen)
    button_image_3.grid(row=Grid_System_Row[1]+1,column=Grid_System_Col[0])

    image_4 = resize_image_to_height(PathToImages + Image_4, 200)
    tk_image_4 = ImageTk.PhotoImage(image_4)
    button_image_4 = tk.Button(window, image=tk_image_4, command=Incorrect_Answer_Chosen)
    button_image_4.grid(row=Grid_System_Row[1]+1,column=Grid_System_Col[1])

    Main_Menu_Button = tk.Button(window,text="la casa",command=Main_Menu_Screen)
    Main_Menu_Button.grid(row=10,column=0)

def Correct_Name_Phrase_From_Image():
    def Check_Answer(image_name):
        answered = Answer_Box.get()
        if (answered == image_name[:-4]):
            correct_label = tk.Label(window, text="correcto")
            correct_label.grid(row=3,column=0)
            Image_Chosen = image_files[random.randint(0,len(image_files)-1)]
            continue_button = tk.Button(window, text="próxima pregunta",command=lambda: Correct_Name_Phrase_From_Image())
            continue_button.grid(row=4,column=0)
            return(1) # Correctly answered

        else:
            incorrect_label = tk.Label(window, text="no correcto")
            incorrect_label.grid(row=3,column=0)
            return(0) # Incorrect answer
    clear_window(window)
    image_name = image_files[random.randint(0,len(image_files)-1)]
    global tk_image  # Declare tk_image as global
    image_spanish = Image.open(PathToImages + image_name)
    tk_image = ImageTk.PhotoImage(image_spanish)
    label = tk.Label(window, image=tk_image)
    label.grid(row=0,column=0)

    global Answer_Box
    Answer_Box = tk.Entry(window)
    Answer_Box.grid(row=1,column=0)

    word_number_count = len(image_name.split(" "))
    Answer_Numbers = tk.Label(window, text=word_number_count)
    Answer_Numbers.grid(row=1,column=1)

    Submit_Button = tk.Button(window,text="Submit",command=lambda: Check_Answer(image_name))
    Submit_Button.grid(row=2,column=0)

    Main_Menu_Button = tk.Button(window,text="la casa",command=Main_Menu_Screen)
    Main_Menu_Button.grid(row=10,column=0)

def Correct_Image_From_Text():
    ActivityID = 111111000001
    def Correct_Answer_Picked():
        label_correct = tk.Label(window, text="correcto")
        label_correct.grid(row=3,column=0)
        button_next_question = tk.Button(window, text="próxima pregunta", command=lambda: Correct_Image_From_Text())
        button_next_question.grid(row=4,column=0)
        AddXPToTable(1,ActivityID)

    def Incorrect_Answer_Picked():
        label_incorrect = tk.Label(window, text="no correcto")
        label_incorrect.grid(row=3,column=0)
    
    clear_window(window)
    Chosen_Images = []
    for i in range(0,9):
        image_name_to_add = image_files[random.randint(0,len(image_files)-1)]
        while image_name_to_add in Chosen_Images:
            image_name_to_add = image_files[random.randint(0,len(image_files)-1)]
        Chosen_Images.append(image_name_to_add)
    Correct_Image, Image_2, Image_3, Image_4, Image_5, Image_6, Image_7, Image_8, Image_9 = Chosen_Images[0],Chosen_Images[1],Chosen_Images[2],Chosen_Images[3],Chosen_Images[4],Chosen_Images[5],Chosen_Images[6],Chosen_Images[7],Chosen_Images[8]
    global tk_image_correct, tk_image_2, tk_image_3, tk_image_4, tk_image_5, tk_image_6, tk_image_7, tk_image_8, tk_image_9
    image_name_label = tk.Label(window, text=Correct_Image[:-4])
    image_name_label.grid(row=0,column=0)

    # Generate random grid 2x2
    Grid_System_Row = Random_Grid_Generate_Solo(3)
    Grid_System_Col = Random_Grid_Generate_Solo(3)

    image_correct = resize_image_to_height(PathToImages + Correct_Image, 200)
    tk_image_correct = ImageTk.PhotoImage(image_correct)
    button_correct = tk.Button(window, image=tk_image_correct, command=Correct_Answer_Picked)
    button_correct.grid(row=Grid_System_Row[0]+1,column=Grid_System_Col[0])

    image_2 = resize_image_to_height(PathToImages + Image_2, 200)
    tk_image_2 = ImageTk.PhotoImage(image_2)
    button_image_2 = tk.Button(window, image=tk_image_2, command=Incorrect_Answer_Picked)
    button_image_2.grid(row=Grid_System_Row[0]+1,column=Grid_System_Col[1])
    
    image_3 = resize_image_to_height(PathToImages + Image_3, 200)
    tk_image_3 = ImageTk.PhotoImage(image_3)
    button_image_3 = tk.Button(window, image=tk_image_3, command=Incorrect_Answer_Picked)
    button_image_3.grid(row=Grid_System_Row[0]+1,column=Grid_System_Col[2])

    image_4 = resize_image_to_height(PathToImages + Image_4, 200)
    tk_image_4 = ImageTk.PhotoImage(image_4)
    button_image_4 = tk.Button(window, image=tk_image_4, command=Incorrect_Answer_Picked)
    button_image_4.grid(row=Grid_System_Row[1]+1,column=Grid_System_Col[0])

    image_5 = resize_image_to_height(PathToImages + Image_5, 200)
    tk_image_5 = ImageTk.PhotoImage(image_5)
    button_image_5 = tk.Button(window, image=tk_image_5, command=Incorrect_Answer_Picked)
    button_image_5.grid(row=Grid_System_Row[1]+1,column=Grid_System_Col[1])

    image_6 = resize_image_to_height(PathToImages + Image_6, 200)
    tk_image_6 = ImageTk.PhotoImage(image_6)
    button_image_6 = tk.Button(window, image=tk_image_6, command=Incorrect_Answer_Picked)
    button_image_6.grid(row=Grid_System_Row[1]+1,column=Grid_System_Col[2])

    image_7 = resize_image_to_height(PathToImages + Image_7, 200)
    tk_image_7 = ImageTk.PhotoImage(image_7)
    button_image_7 = tk.Button(window, image=tk_image_7, command=Incorrect_Answer_Picked)
    button_image_7.grid(row=Grid_System_Row[2]+1,column=Grid_System_Col[0])

    image_8 = resize_image_to_height(PathToImages + Image_8, 200)
    tk_image_8 = ImageTk.PhotoImage(image_8)
    button_image_8 = tk.Button(window, image=tk_image_8, command=Incorrect_Answer_Picked)
    button_image_8.grid(row=Grid_System_Row[2]+1,column=Grid_System_Col[1])

    image_9 = resize_image_to_height(PathToImages + Image_9, 200)
    tk_image_9 = ImageTk.PhotoImage(image_9)
    button_image_9 = tk.Button(window, image=tk_image_9, command=Incorrect_Answer_Picked)
    button_image_9.grid(row=Grid_System_Row[2]+1,column=Grid_System_Col[2])

    Main_Menu_Button = tk.Button(window,text="la casa",command=Main_Menu_Screen)
    Main_Menu_Button.grid(row=10,column=0)

def Multiple_Choice_Correct_Text_From_Image():
    def Correct_Answer_Supplied():
        label_correct = tk.Label(window, text="  correcto  ")
        label_correct.grid(row=4,column=0)
        button_next_question = tk.Button(window, text="proxima pregunta",command=Multiple_Choice_Correct_Text_From_Image)
        button_next_question.grid(row=5,column=0)

    def Incorrect_Answer_Supplied():
        label_INcorrect = tk.Label(window, text=" no correcto")
        label_INcorrect.grid(row=4,column=0)
    
    clear_window(window)
    global tk_image_spanish
    # Generate random grid 2x2
    Grid_System_Row = Random_Grid_Generate_Solo(2)
    Grid_System_Col = Random_Grid_Generate_Solo(2)

    Other_Image_Texts = []
    for i in range(0,4):
        Text_To_Add = image_files[random.randint(0,len(image_files)-1)]
        while Text_To_Add in Other_Image_Texts:
            Text_To_Add = image_files[random.randint(0,len(image_files)-1)]
        Other_Image_Texts.append(Text_To_Add)
    
    image_spanish=Other_Image_Texts[3]
    
    es_image_correct = resize_image_to_height(PathToImages + image_spanish, 200)
    tk_image_spanish = ImageTk.PhotoImage(es_image_correct)
    label_question = tk.Label(window, image=tk_image_spanish)
    label_question.grid(row=0,column=0)

    button_correct = tk.Button(window, text=image_spanish[:-4], command=Correct_Answer_Supplied)
    button_correct.grid(row=Grid_System_Row[0]+1,column=Grid_System_Col[0])

    button_incorrect_1 = tk.Button(window, text=Other_Image_Texts[0][:-4], command=Incorrect_Answer_Supplied)
    button_incorrect_1.grid(row=Grid_System_Row[0]+1,column=Grid_System_Col[1])

    button_incorrect_2 = tk.Button(window, text=Other_Image_Texts[1][:-4], command=Incorrect_Answer_Supplied)
    button_incorrect_2.grid(row=Grid_System_Row[1]+1,column=Grid_System_Col[0])

    button_incorrect_3 = tk.Button(window, text=Other_Image_Texts[2][:-4], command=Incorrect_Answer_Supplied)
    button_incorrect_3.grid(row=Grid_System_Row[1]+1,column=Grid_System_Col[1])
    
    Main_Menu_Button = tk.Button(window,text="la casa",command=Main_Menu_Screen)
    Main_Menu_Button.grid(row=10,column=0)

def Correct_English_From_Spanish_Text(): #Needs work on this
    clear_window(window)


# Screens

def Menú_configuración():
    clear_window(window)

    Intensity_Slider = tk.Scale(window)
    Intensity_Slider.grid(row=0,column=0)

    Reset_Known_Words_Btn = tk.Button(window,text="restablecer vocabulario",command=ResetKnownWords)
    Reset_Known_Words_Btn.grid(row=1,column=0)

    Reset_XP_Table_Btn = tk.Button(window,text="restablecer XP",command=ResetXPTable)
    Reset_XP_Table_Btn.grid(row=2,column=0)
    

    Main_Menu_Button = tk.Button(window,text="la casa",command=Main_Menu_Screen)
    Main_Menu_Button.grid(row=10,column=0)

def Vocabulary_Zone_Fragments():
    clear_window(window)
    Vocab_Fragments=["Numeros","Ano","Colores","Familia","Viaje","Trabaje","Casa","Deporte", "Emergencia","Alimentos","Animal","Tienda","Tiempo (weather)","Tiempo (Time)","Música","Electrónica","Salud","Noche"]
    for i in range(0,len(Vocab_Fragments)):
        
        Button_Item = tk.Button(window, text=Vocab_Fragments[i], command=lambda i=i : print(Vocab_Fragments[i]))
        Button_Item.grid(row=0,column=i)
    
    Main_Menu_Button = tk.Button(window,text="la casa",command=Main_Menu_Screen)
    Main_Menu_Button.grid(row=10,column=0)

def Regularo_Verbos_Screen():
    clear_window(window)
    Table_Data = [("",'-ar','-er',"-ir"),
       ("Yo",'am-o','com-o',"viv-o"),
       ("Tú",'am-as','com-es',"viv-es"),
       ("Él-Ella-Usted",'am-a','com-e',"viv-e"),
       ("Nosotros-as",'am-amos','com-emos',"viv-imos"),
       ("Vosotors-as",'am-áis','com-éis',"viv-ís"),
       ("Ellos-Ellas-Ustedes",'am-an','com-en',"viv-en")]
    
    total_rows = len(Table_Data)
    total_columns = len(Table_Data[0])
    # code for creating table
    for row_i in range(total_rows):
        for col_j in range(total_columns):
                
            Item_In_Table = tk.Entry(window, width=20, fg='blue',
                            font=('Arial',16,'bold'))
                
            Item_In_Table.grid(row=row_i, column=col_j)
            Item_In_Table.insert(tk.END, Table_Data[row_i][col_j])
    
def Reuglaro_Verbos_Examen_Screen():
    clear_window(window)
    def check_answers(answers):
        XP_Gained = 0
        for numero in range(10):
            if Entry_Box_List[numero].get() == Answer_Values[numero]:
                WRITE_ANSWERS = tk.Label(text="correcto")
                WRITE_ANSWERS.grid(row=numero,column=2)
                Entry_Box_List[numero].configure(bg='green')
                XP_Gained+=1
            else:
                WRITE_ANSWERS = tk.Label(text=answers[numero])
                WRITE_ANSWERS.grid(row=numero,column=2)
                XP_Gained-=1

        print(Entry_Box_List[0].get())
        if XP_Gained>0:
            AddXPToTable(XP_Gained)

    Answer_Values = list()
    Entry_Box_List = []
    for i in range(10):
        regular_verbs_query = f'SELECT * FROM Regular_Verbs'
        Regular_Verbs_Spanish_Values = db_curs.execute(regular_verbs_query).fetchall()
        Spanish_Verb_Chosen = Regular_Verbs_Spanish_Values[random.randint(0,len(Regular_Verbs_Spanish_Values)-1)][0]
        Persona_Number = random.randint(0,len(Persona)-1)
        Persona_Chosen = Persona[Persona_Number]
        Verb_Standard = tk.Label(text=Persona_Chosen + " " + Spanish_Verb_Chosen)
        Verb_Standard.grid(row=i,column=0)
        Answer_Item = tk.Entry(name="entryno"+str(i))
        Answer_Item.grid(row=i,column=1)
        Entry_Box_List.append(Answer_Item)
        
        if Spanish_Verb_Chosen[-2:] == "ar":
            Ending_Letters = Endings_AR[Persona_Number]
        elif Spanish_Verb_Chosen[-2:] == "er":
            Ending_Letters = Endings_ER[Persona_Number]
        elif Spanish_Verb_Chosen[-2:] == "ir":
            Ending_Letters = Endings_IR[Persona_Number]
        else:
            Ending_Letters = "NO"

        Answer_Values.append(Spanish_Verb_Chosen[:-2]+ Ending_Letters)
    Button_Check_It = tk.Button(text="Check Answers", command=lambda: check_answers(Answer_Values))
    Button_Check_It.grid(row=99,column=0)

    Main_Menu_Button = tk.Button(window,text="la casa",command=Main_Menu_Screen)
    Main_Menu_Button.grid(row=1000,column=0)

def Story_Screen():
    clear_window(window)
    Story_Words_Spanish = "Deja que te cuente una historia sobre un pollito. Su nombre es Pollito Tito. Él vive en un gallinero pequeño y normal en un barrio pequeño y normal."
    Story_Words_Spanish_List = Story_Words_Spanish.split(" ")
    numero = 0
    for word_i in Story_Words_Spanish_List:
        first_Word = tk.Label(window, text = word_i)
        first_Word.grid(row=0,column=numero)
        ro = db_curs.execute('select * from SpanishWordTranslations WHERE "Spanish Word Exact" = "' + word_i.lower() + '";')
        WORDZOS = ro.fetchall()
        if not WORDZOS:  # Check if WORDZOS is empty
            CreateTextToolTip(first_Word, text="Failed")
        else:
            CreateTextToolTip(first_Word, text=WORDZOS)
        numero += 1
    

    Main_Menu_Button = tk.Button(window,text="la casa",command=Main_Menu_Screen)
    Main_Menu_Button.grid(row=1000,column=0)




def Main_Menu_Screen():
    clear_window(window)
    Label_Home_Screen = tk.Label(window, text="The Little Language App")
    Label_Home_Screen.grid(row=0,column=0)
    Label_Current_Level = tk.Label(window, text = "Level:")
    Label_Current_Level.grid(row=0,column=1)
    Level_Value = tk.Label(window, text = str(CalculateLevel()))
    Level_Value.grid(row=0,column=2)

    Button_Activity_1 = tk.Button(window, text = "el audio a la imagen", command=Correct_Image_From_Audio)
    Button_Activity_1.grid(row=1,column=1)

    Button_Activity_2 = tk.Button(window, text = "el texto a la imagen", command=Correct_Image_From_Text)
    Button_Activity_2.grid(row=2,column=1)

    Button_Activity_3 = tk.Button(window, text = "la imagen a el texto",command=Correct_Name_Phrase_From_Image)
    Button_Activity_3.grid(row=3,column=1)

    Button_Activity_4 = tk.Button(window, text = "la imagen a el texto muti",command=Multiple_Choice_Correct_Text_From_Image)
    Button_Activity_4.grid(row=4,column=1) 

    Button_Activity_5 = tk.Button(window, text = "vocabulario",command=Vocabulary_Zone_Fragments)
    Button_Activity_5.grid(row=5,column=1)

    Button_Activity_6 = tk.Button(window, text = "la gramática - regular verbos", command=Regularo_Verbos_Screen)
    Button_Activity_6.grid(row=6,column=1)

    Button_Activity_7 = tk.Button(window, text = "practicar", command=Reuglaro_Verbos_Examen_Screen)
    Button_Activity_7.grid(row=6,column=2)

    Button_Activity_8 = tk.Button(window, text = "el cuento", command=Story_Screen)
    Button_Activity_8.grid(row=7,column=1)

    Button_Activity_9 = tk.Button(window, text = "Menú configuración", command=Menú_configuración)
    Button_Activity_9.grid(row=8,column=1)

    text_btn = tk.Button(window, text="Hover over me for text")
    text_btn.grid(row=10,column=0,padx=10, pady=10)
    CreateTextToolTip(text_btn, "This is a text tooltip")

    image_btn = tk.Button(window, text="Hover over me for image")
    image_btn.grid(row=11,column=0,padx=10, pady=10)
    CreateImageToolTip(image_btn, PathToImages + "bottle.png")

    
# Working On this part

def Words_In_Context_Screen(Spanish_Word):
    clear_window(window)
    Spanish_Word_Label = tk.Label(window,text=Spanish_Word)
    Spanish_Word_Label.grid(row=0,column=0)
    # In this screen you will be able to access contextually correct situations in which the word or phrase is used.


window = tk.Tk()
window.title("The Little Language App")
window.geometry("1920x1080")

images_path = 'C:/Users/bohda/Documents/Python Codes/TheLittleLangaugeApp/Images'
image_files = get_image_filenames(images_path)
sounds_path = 'C:/Users/bohda/Documents/Python Codes/TheLittleLangaugeApp/Audios'
sound_files = get_sound_filenames(sounds_path)

Main_Menu_Screen()

window.mainloop()

# Practicing words you know in any of the activities is 1XP for each correct answer. (Maybe -1 for each incorrect answer)
# Learning words with any activity is 2 XP per correct answer
# Correctly answering sentences is 3 XP per correct answer