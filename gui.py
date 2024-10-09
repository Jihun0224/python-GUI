import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def on_select_bottle():
    selected_bottle = bottle_var.get()
    grams = grams_entry.get()
    if not selected_bottle:
        messagebox.showerror("Error", "Please select a bottle.")
        return
    if not grams.isdigit():
        messagebox.showerror("Error", "Please enter a valid number for grams.")
        return
    # To Do : Gram Limit Check
        
    messagebox.showinfo("Selection", f"You selected {selected_bottle} with {grams} grams.")
    
    # To Do : Send Data(To Server)
    
    grams_entry.delete(0, tk.END) 
    bottle_var.set(default_selected_bottle)
    
def on_submit_command():
    command = command_entry.get("1.0", tk.END).strip()
    messagebox.showinfo("Command Entered", f"You entered command: {command}")
    
    # To Do : LLM
    # To Do : Send Data(To Server)

    command_entry.delete("1.0", tk.END)
    
# 메인 윈도우
root = tk.Tk()
root.title("Bottle Selector with LLM Command")

bottle_images = ["images/blue_bottle.png", "images/green_bottle.png", "images/purple_bottle.png"]
colors = ["Blue", "Green", "Purple"]
default_selected_bottle = "Blue bottle"
loaded_images = []

for img in bottle_images:
    img_opened = Image.open(img)
    img_resized = img_opened.resize((100, 200))
    img_tk = ImageTk.PhotoImage(img_resized)
    loaded_images.append(img_tk)

# Bottle 선택 섹션
bottle_var = tk.StringVar(value=default_selected_bottle)
bottle_frame = tk.Frame(root)
bottle_frame.pack(pady=10)

tk.Label(bottle_frame, text="Select a Bottle:").pack()

for i, img in enumerate(loaded_images):
    bottle_radio = tk.Radiobutton(
        bottle_frame, text=colors[i] + " bottle", variable=bottle_var, value= colors[i] + " bottle", 
        image=img, compound='top'
    )
    bottle_radio.pack(side="left", padx=10)

# 그램 입력 섹션
grams_frame = tk.Frame(root)
grams_frame.pack(pady=10)

tk.Label(grams_frame, text="Enter grams:").pack(side="left")
grams_entry = tk.Entry(grams_frame)
grams_entry.pack(side="left", padx=5)

submit_button = tk.Button(root, text="Submit Selection", command=on_select_bottle)
submit_button.pack(pady=10)

# LLM 명령 입력 섹션
llm_frame = tk.LabelFrame(root, text="", padx=10, pady=10)
llm_frame.pack(pady=20, fill="both")  

llm_label = tk.Label(llm_frame, text="LLM", font=("Arial", 10))
llm_label.pack(side="top", anchor="center")

tk.Label(llm_frame, text="Enter command:").pack(anchor="w")
command_entry = tk.Text(llm_frame, height=5, width=50)
command_entry.pack(pady=5)

command_button = tk.Button(llm_frame, text="Submit Command", command=on_submit_command)
command_button.pack(pady=10)

# GUI 실행
root.mainloop()
