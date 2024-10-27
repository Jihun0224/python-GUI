# python-GUI
## To do
- 테마 적용해 볼 것(https://ttkthemes.readthedocs.io/en/latest/themes.html#themes)

![image](https://github.com/user-attachments/assets/dbf70d9a-879a-4cb5-a029-c6ef7e9788be)  
![image](https://github.com/user-attachments/assets/709e948a-4269-4fc6-ab57-e3cc337d4661)  
![image](https://github.com/user-attachments/assets/f4877c29-b35c-4a77-9eea-5ea17b5d4635)

## 추가 사항
1. main frame에 아래 코드 추가
   ```python
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10, fill="x")
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    
    robot_control_button = tk.Button(button_frame, text="Robot Control", command=open_robot_control_window)
    robot_control_button.grid(row=0, column=0, sticky="ew", padx=5)

    event_button = tk.Button(button_frame, text="Event", command=open_event_window)
    event_button.grid(row=0, column=1, sticky="ew", padx=5)
   ```
2. 두 버튼 클릭 시 윈도우 창 추가
  ```python
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
  ```
