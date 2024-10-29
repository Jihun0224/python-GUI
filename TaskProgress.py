import tkinter as tk
from PIL import Image, ImageTk
import threading
import time

class TaskProgressApp:
    def __init__(self, root, tasks):
        self.root = root
        self.tasks = tasks
        self.current_task_index = 0
        self.task_box = []
        self.task_labels = []
        self.in_progress_color = "#FF6666"  # 진행 중 색상
        self.completed_color = "#A0A0A0"  # 완료 색상
        self.task_canvas = None  
        self.running = False  

    def open_window(self):
        if not self.task_canvas:  
            self.task_canvas = tk.Canvas(self.root, width=200, height=700)
            self.task_canvas.pack()
            self.load_arrow_image()
            self.create_task_box()
            self.current_task_index = 0
            self.running = True
            threading.Thread(target=self.run_task_updates).start()  # 작업 업데이트 시작

    def close_window(self):
        if self.task_canvas:
            self.task_canvas.destroy()
            self.task_canvas = None
            self.running = False 

    def load_arrow_image(self):
        arrow_img = Image.open("images/play.png").resize((30, 30))
        self.arrow_image = ImageTk.PhotoImage(arrow_img)

    def create_task_box(self):
        box_width = 150
        box_height = 50
        y_start = 30
        self.task_box.clear()
        self.task_labels.clear()

        for i, task in enumerate(self.tasks):
            frame = self.task_canvas.create_rectangle(25, y_start, 25 + box_width, y_start + box_height, fill="white")
            label = self.task_canvas.create_text(100, y_start + box_height // 2, text=task, font=("Arial", 12), anchor="center")
            self.task_box.append(frame)
            self.task_labels.append(label)
            y_start += box_height + 40
            
            if i < len(self.tasks) - 1:
                self.task_canvas.create_image(100, y_start - 20, image=self.arrow_image)

    def update_task(self, task_completed):
        for i, task in enumerate(self.task_box):
            if i < self.current_task_index:
                self.task_canvas.itemconfig(task, fill=self.completed_color)
            elif i == self.current_task_index:
                color = self.in_progress_color if not task_completed else self.completed_color
                self.task_canvas.itemconfig(task, fill=color)
            else:
                self.task_canvas.itemconfig(task, fill="white")

    def run_task_updates(self):
        for _ in range(len(self.tasks)):
            if not self.running or not self.task_canvas:
                break
            self.root.after(0, self.update_task, False)
            time.sleep(3) 

            self.root.after(0, self.update_task, True)
            self.current_task_index += 1
            if self.current_task_index >= len(self.tasks):
                break


def main():
    # tasks_input = input("Tasks: ")
    # tasks = [task.strip() for task in tasks_input.split(",") if task.strip()]
    tasks = ["reset", "pick", "open","reset", "pick", "open"]
    # GUI 설정
    root = tk.Tk()
    app = TaskProgressApp(root, tasks)
    
    open_button = tk.Button(root, text="Open Task Window", command=app.open_window)
    open_button.pack()
    close_button = tk.Button(root, text="Close Task Window", command=app.close_window)
    close_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
