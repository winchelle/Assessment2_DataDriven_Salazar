from tkinter import *
import requests

root = Tk()
root.title("The Krusty Kitchen")
root.geometry("704x500")
root.resizable(0, 0)

entry = None
txtarea = None 

def startProgram():
    global bg_image

    # Clear Window
    for screen in root.winfo_children():
        screen.destroy()

    bg_image = PhotoImage(file="krustykrab.png")
    bg_label = Label(root, image=bg_image)
    bg_label.place(x=0, y=1)

    label1 = Label(root, text="The Krusty Kitchen", fg="#C1440E",
                  bg="#B8D98A", font=("Fixedsys", 35))
    label1.place(x=65, y=160)

    Button(root, text="Start", width=20, height=2, bg="#8B3A3A",
           fg="#FFD700", font=("Arial", 12, "bold"),
           command=mealProgram).place(x=250, y=280)


def mealProgram():
    global entry, txtarea

    # Clear Window
    for screen in root.winfo_children():
        screen.destroy()

    frame = Frame(root, width=704, height=500, bg="#7D2324")
    frame.place(x=1, y=5)

    # Entry box for meal name
    entry = Entry(frame, bg="#FAF2E6", font=("Georgia", 20), width=12)
    entry.place(x=20, y=30)

    # Search button
    Button(frame, text="Search", width=14, height= 2, bg="#6683A9",
           fg="#FAF2E6", font=("Georgia", 12),
           command=searchMeal).place(x=245, y=25)

    # Random button
    Button(frame, text="Random Meal", width=14, height=2, bg="#6683A9",
           fg="#FAF2E6", font=("Georgia", 12),
           command=randomMeal).place(x=395, y=25)
    
    Button(frame, text="A-Z", width=14, height=2, bg="#6683A9",
           fg="#FAF2E6", font=("Georgia", 12),
           command=AZMeals).place(x=545, y=25)

    # Result Label
    txtarea = Text(root, fg="#33312E", bg="#FAF2E6", font=("Georgia", 12))
    txtarea.place(x=19, y=100, height=370, width=650)
    
    scrollV = Scrollbar(frame, command=txtarea.yview)
    scrollV.place(x=667, y=95, height=370)
    txtarea.config(yscrollcommand=scrollV.set)

def showMeal(url):
    global txtarea
    txtarea.config(state=NORMAL)  
    txtarea.delete(1.0, END)  
    
    response = requests.get(url)
    data = response.json()

    if not data.get("meals"):
        txtarea.insert("1.0", "Meal not found.")
        return

    meal = data["meals"][0]
    txtarea.insert(END, f"Meal Name: {meal['strMeal']}\n\n")
    txtarea.insert(END, f"Category: {meal['strCategory']}\n")
    txtarea.insert(END, f"Area: {meal['strArea']}\n\n")
    txtarea.insert(END, "Instructions:\n\n")
    
    for x, line in enumerate (meal['strInstructions'].split("."), start= 1):
        line = line.strip()       
        if line:                 
            txtarea.insert(END, f"{x}. {line}.\n\n")
            
    txtarea.insert(END, "Ingredients:\n\n")
    
    for i in range(1, 21):
        ingredient = meal.get(f"strIngredient{i}")
        measure = meal.get(f"strMeasure{i}")
        if ingredient and ingredient.strip():
            txtarea.insert(END, f"- {ingredient} : {measure}\n")
                   
    txtarea.config(state=DISABLED)  
    
def searchMeal():
    meal_name = entry.get().strip()
    
    if meal_name == "":
        txtarea.config(state=NORMAL)
        txtarea.delete("1.0", END)
        txtarea.insert(END, "Please enter a meal name to search.")
        txtarea.config(state=DISABLED)
        return
    
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
    showMeal(url)

        
def randomMeal():
    
    txtarea.config(state=NORMAL)
    txtarea.delete("1.0", END)
    
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    showMeal(url)
    
def AZMeals():
    letter = entry.get().strip().lower()
    
    if not letter or len(letter) != 1 or not letter.isalpha():
        txtarea.config(state=NORMAL)
        txtarea.delete("1.0", END)
        txtarea.insert(END, "Please enter a single letter (A-Z).")
        txtarea.config(state=DISABLED)
        return
    
    url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={letter}"
    response = requests.get(url)
    data = response.json()
    
    txtarea.config(state=NORMAL)
    txtarea.delete("1.0", END)
    
    if not data["meals"]:
        txtarea.insert(END, f"No meals found starting with '{letter.upper()}'.")
    else:
        txtarea.insert(END, f"Meals starting with '{letter.upper()}':\n\n")
        for meal in data["meals"]:
            txtarea.insert(END, f"- {meal['strMeal']}\n")

    txtarea.config(state=DISABLED)
    
startProgram()
root.mainloop()