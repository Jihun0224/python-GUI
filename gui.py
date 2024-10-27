import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

def validate_selection(selected_bottle, grams):
    if not selected_bottle:
        messagebox.showerror("Error", "Please select a bottle.")
        return False
    if not grams.isdigit():
        messagebox.showerror("Error", "Please enter a valid number for grams.")
        return False
    return True

def display_selection(selected_bottle, grams):
    messagebox.showinfo("Selection", f"You selected {selected_bottle} with {grams} grams.")

def on_select_bottle():
    selected_bottle = bottle_var.get()
    grams = grams_entry.get()

    if not validate_selection(selected_bottle, grams):
        return
    
    display_selection(selected_bottle, grams)
    
    # To Do : Send Data(To Server)
    
    grams_entry.delete(0, tk.END) 
    bottle_var.set(default_selected_bottle)

def on_submit_command():
    command = command_entry.get("1.0", tk.END).strip()
    messagebox.showinfo("Command Entered", f"You entered command: {command}")
    command_entry.delete("1.0", tk.END)
    
    # To Do : LLM
    # To Do : Send Data(To Server)

def load_images(image_paths, size=(100, 200)):
    images = []
    for img in image_paths:
        img_opened = Image.open(img)
        img_resized = img_opened.resize(size)
        img_tk = ImageTk.PhotoImage(img_resized)
        images.append(img_tk)
    return images

def setup_bottle_selection_frame(parent, images, colors):
    tk.Label(parent, text="Select a Bottle:").pack()
    for i, img in enumerate(images):
        bottle_radio = tk.Radiobutton(
            parent, text=colors[i] + " bottle", variable=bottle_var, value=colors[i] + " bottle", 
            image=img, compound='top'
        )
        bottle_radio.pack(side="left", padx=10)
        
def open_robot_control_window():

    robot_window = tk.Toplevel(root)
    robot_window.title("Robot Control")
    robot_window.geometry("300x130")
    
    button_frame = tk.Frame(robot_window)
    button_frame.pack(pady=10)
    
    reset_image = ImageTk.PhotoImage(Image.open("images/reset.png").resize((70, 70)))
    reset_button = tk.Button(button_frame, image=reset_image, command=lambda: on_robot_button("reset"))
    reset_button.image = reset_image
    reset_button.grid(row=0, column=0, padx=10)

    pause_image = ImageTk.PhotoImage(Image.open("images/pause.png").resize((70, 70)))
    play_image = ImageTk.PhotoImage(Image.open("images/play.png").resize((70, 70)))
    pause_button = tk.Button(button_frame, image=pause_image, command=lambda: on_robot_button("pause_play"))
    pause_button.image = pause_image
    pause_button.grid(row=0, column=1, padx=10)

    def on_robot_button(action):
        if action == "reset":
            print("Reset")
        elif action == "pause_play":
            nonlocal pause_button
            if pause_button['image'] == str(pause_image): 
                print("Pause")
                pause_button.config(image=play_image)
            else:
                print("Play")
                pause_button.config(image=pause_image)
                
def show_selected_coffee(coffee_name):
    popup = tk.Toplevel(root)
    popup.title("Selected Coffee")
    
    popup_width = 200
    popup_height = 100
    popup.geometry(f"{popup_width}x{popup_height}")

    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width // 2) - (popup_width // 2)
    y = (screen_height // 2) - (popup_height // 2)
    popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

    label = tk.Label(popup, text=f"You selected: {coffee_name}")
    label.pack(pady=20)

    close_button = tk.Button(popup, text="Close", command=popup.destroy)
    close_button.pack(pady=5)
    
def open_event_window():
    event_window = tk.Toplevel(root)
    event_window.title("Event")
    event_window.geometry("300x300")

    button_frame = tk.Frame(event_window)
    button_frame.pack(pady=20)

    coffee_names = ["Coffee1", "Coffee2", "Coffee3", "Coffee4", "Coffee5"]

    for coffee_name in coffee_names:
        coffee_button = tk.Button(button_frame, text=coffee_name, width=15, height=2,
                                  command=lambda name=coffee_name: show_selected_coffee(name))
        coffee_button.pack(pady=5)
    
def main():
    global root, bottle_var, grams_entry, default_selected_bottle, command_entry

    root = tk.Tk()
    root.title("Bottle Selector with LLM Command")

    bottle_images = ["images/blue_bottle.png", "images/green_bottle.png", "images/purple_bottle.png"]
    colors = ["Blue", "Green", "Purple"]
    default_selected_bottle = "Blue bottle"

    # Load bottle images
    loaded_images = load_images(bottle_images)

    # Bottle selection section
    bottle_var = tk.StringVar(value=default_selected_bottle)
    bottle_frame = tk.Frame(root)
    bottle_frame.pack(pady=10)

    setup_bottle_selection_frame(bottle_frame, loaded_images, colors)

    # Grams input section
    grams_frame = tk.Frame(root)
    grams_frame.pack(pady=10)

    tk.Label(grams_frame, text="Enter grams:").pack(side="left")
    grams_entry = tk.Entry(grams_frame)
    grams_entry.pack(side="left", padx=5)

    submit_button = tk.Button(root, text="Submit Selection", command=on_select_bottle)
    submit_button.pack(pady=10)

    # LLM command input section
    llm_frame = tk.LabelFrame(root, text="", padx=10, pady=10)
    llm_frame.pack(pady=20, fill="both")

    llm_label = tk.Label(llm_frame, text="LLM", font=("Arial", 10))
    llm_label.pack(side="top", anchor="center")

    tk.Label(llm_frame, text="Enter command:").pack(anchor="w")
    command_entry = tk.Text(llm_frame, height=5, width=50)
    command_entry.pack(pady=5)

    command_button = tk.Button(llm_frame, text="Submit Command", command=on_submit_command)
    command_button.pack(pady=10)
    
    # Rotot Control & Event Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10, fill="x")
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    
    robot_control_button = tk.Button(button_frame, text="Robot Control", command=open_robot_control_window)
    robot_control_button.grid(row=0, column=0, sticky="ew", padx=5)

    event_button = tk.Button(button_frame, text="Event", command=open_event_window)
    event_button.grid(row=0, column=1, sticky="ew", padx=5)
    
    # Run the GUI
    root.mainloop()

if __name__ == "__main__":
    main()
