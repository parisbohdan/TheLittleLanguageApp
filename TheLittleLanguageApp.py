import tkinter as tk
import time
import pyautogui
from PIL import Image, ImageTk
import os
import random
import pygame

PathToSounds = "C:/Users/bohda\Documents/Python Codes/TheThousand/Audios/"
PathToImages = "C:/Users/bohda/Documents/Python Codes/TheThousand/Images/"

# Support Functions

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
    def Correct_Answer_Picked():
        label_correct = tk.Label(window, text="correcto")
        label_correct.grid(row=3,column=0)
        button_next_question = tk.Button(window, text="próxima pregunta", command=lambda: Correct_Image_From_Text())
        button_next_question.grid(row=4,column=0)

    def Incorrect_Answer_Picked():
        label_incorrect = tk.Label(window, text="no correcto")
        label_incorrect.grid(row=3,column=0)
    
    clear_window(window)
    Chosen_Images = []
    for i in range(0,4):
        image_name_to_add = image_files[random.randint(0,len(image_files)-1)]
        while image_name_to_add in Chosen_Images:
            image_name_to_add = image_files[random.randint(0,len(image_files)-1)]
        Chosen_Images.append(image_name_to_add)
    Correct_Image, Image_2, Image_3, Image_4 = Chosen_Images[0],Chosen_Images[1],Chosen_Images[2],Chosen_Images[3]
    global tk_image_correct, tk_image_2, tk_image_3, tk_image_4
    image_name_label = tk.Label(window, text=Correct_Image[:-4])
    image_name_label.grid(row=0,column=0)

    # Generate random grid 2x2
    Grid_System_Row = Random_Grid_Generate_Solo(2)
    Grid_System_Col = Random_Grid_Generate_Solo(2)

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
    button_image_3.grid(row=Grid_System_Row[1]+1,column=Grid_System_Col[0])

    image_4 = resize_image_to_height(PathToImages + Image_4, 200)
    tk_image_4 = ImageTk.PhotoImage(image_4)
    button_image_4 = tk.Button(window, image=tk_image_4, command=Incorrect_Answer_Picked)
    button_image_4.grid(row=Grid_System_Row[1]+1,column=Grid_System_Col[1])

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

# Screens

def Menú_configuración():
    clear_window(window)

    Intensity_Slider = tk.Scale(window)
    Intensity_Slider.grid(row=0,column=0)
    

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

def Main_Menu_Screen():
    clear_window(window)
    Label_Home_Screen = tk.Label(window, text="The Thousand")
    Label_Home_Screen.grid(row=0,column=0)

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

    Button_Activity_6 = tk.Button(window, text = "Menú configuración", command=Menú_configuración)
    Button_Activity_6.grid(row=6,column=1)
    
# Working On this part

window = tk.Tk()
window.title("The Thousand")
window.geometry("1920x1080")

images_path = 'C:/Users/bohda/Documents/Python Codes/TheThousand/Images'
image_files = get_image_filenames(images_path)
sounds_path = 'C:/Users/bohda/Documents/Python Codes/TheThousand/Audios'
sound_files = get_sound_filenames(sounds_path)

Main_Menu_Screen()

window.mainloop()