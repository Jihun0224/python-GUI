import time
import rclpy
import tkinter as tk
from tkinter import messagebox, ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from rclpy.node import Node
from std_msgs.msg import String
from threading import Thread
import tasks  # ROS2 communication functions


class GUI(Node):
    def __init__(self, tasks):
        if not rclpy.ok():
            rclpy.init()
        super().__init__("gui_node")
        self.tasks = tasks  # ROS2 task functions

        # Initialize main window
        self.setup_main_window()

        # Bottle selection, gram input, and submit button
        self.setup_bottle_selection()
        self.setup_gram_input()
        self.setup_bottle_submit_button()

        # LLM command input and response menu
        self.setup_llm_command_input()
        self.setup_llm_response_menu()

        # Supervisor control buttons
        self.setup_supervisor_button()
        
        # Task progress variables
        self.llm_response = None
        self.task_list = []
        self.current_task_index = 0
        self.task_box = []
        self.task_labels = []
        self.in_progress_color = "#FF6666"
        self.completed_color = "#A0A0A0"
        self.task_canvas = None
        self.is_recording = False
        
        # Initialize ROS2 interface
        self.create_interfaces()
        self.start_node_async()

        # Start GUI
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            pass

    def setup_main_window(self):
        self.window = tk.Tk()
        self.window.title("로봇 명령 메뉴")
        
        # self.window = ThemedTk(theme="itft1")
        # self.window.title("로봇 명령 메뉴")
        # self.window.configure(background='#DAEFFD')
        # ttk.Separator(self.window, orient='horizontal').pack(fill='x', pady=10)
    def setup_bottle_selection(self):
        bottle_images = [
            "/home/sdcrobot/ros2_ws/src/sd_external_msgs/examples/images/blue_bottle.png",
            "/home/sdcrobot/ros2_ws/src/sd_external_msgs/examples/images/green_bottle.png",
            "/home/sdcrobot/ros2_ws/src/sd_external_msgs/examples/images/purple_bottle.png"
        ]
        loaded_images = [ImageTk.PhotoImage(Image.open(img).resize((100, 200))) for img in bottle_images]
        self.bottle_names = ["파란색", "초록색", "보라색"]
        self.bottle_var = tk.StringVar(value=self.bottle_names[0])

        self.bottle_frame = tk.Frame(self.window)
        self.bottle_frame.pack(pady=10)
        tk.Label(self.bottle_frame, text="뿌릴 재료의 색을 선택하세요:", font=("Arial", 16)).pack()

        for i, img in enumerate(loaded_images):
            bottle_radio = tk.Radiobutton(
                self.bottle_frame, text=self.bottle_names[i], variable=self.bottle_var, value=self.bottle_names[i],
                image=img, compound='top', font=("Arial", 15)
            )
            bottle_radio.pack(side="left", padx=10)

    def setup_gram_input(self):
        self.gram_frame = tk.Frame(self.window)
        self.gram_frame.pack(pady=10)
        tk.Label(self.gram_frame, text="뿌릴 재료의 질량[g]을 정수단위로 입력하세요(0~400g):", font=("Arial", 16)).pack(side="left")
        self.gram_entry = tk.Entry(self.gram_frame, font=("Arial", 16))
        self.gram_entry.pack(side="left", padx=5)

    def setup_bottle_submit_button(self):
        self.bottle_submit_button = tk.Button(self.window, text="명령", font=("Arial", 16), command=self.on_select_bottle)
        self.bottle_submit_button.pack(pady=10)

    def setup_llm_command_input(self):
        self.llm_frame = tk.LabelFrame(self.window, text="", padx=10, pady=10)
        self.llm_frame.pack(pady=20, fill="both")
        tk.Label(self.llm_frame, text="LLM에게 보낼 명령을 입력하세요:", font=("Arial", 16)).pack()
        
        self.command_entry = tk.Text(self.llm_frame, height=5, width=60, font=("Arial", 14), background="white")
        self.command_entry.pack(anchor='center')

        button_frame = tk.Frame(self.llm_frame)
        button_frame.pack(pady=10)

        self.command_submit_button = tk.Button(button_frame, text="보내기", font=("Arial", 16), command=self.on_submit_llm_command)
        self.command_submit_button.pack(side="left", padx=5)

        self.voice_record_button = tk.Button(button_frame, text="음성 녹음", font=("Arial", 16), command=self.voice_recording)
        self.voice_record_button.pack(side="left", padx=5)
        
        
    def setup_llm_response_menu(self):
        tk.Label(self.llm_frame, text="LLM에서 보낸 답변:", font=("Arial", 16)).pack()
        self.response_entry = tk.Text(self.llm_frame, height=5, width=60, font=("Arial", 14), background="white", relief="flat")
        self.response_entry.pack(pady=5)
        self.llm_response_number = 1
        self.response_delete_button = tk.Button(self.llm_frame, text="내용 지우기", font=("Arial", 16), command=self.on_delete_llm_response)
        self.response_delete_button.pack(pady=10)

    def setup_supervisor_button(self):
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=10, fill="x")
        button_frame.grid_columnconfigure(0, weight=1)
        tk.Button(button_frame, text="관리자1", command=self.open_supervisor_window).grid(row=0, column=0, sticky="ew", padx=5)
    
    def voice_recording(self):
        self.is_recording = not self.is_recording
        
        if self.is_recording:
            self.voice_record_button.config(text="녹음 중지")
            print("Recording started...")
        else:
            self.voice_record_button.config(text="음성 녹음")
            print("Recording stopped.")
            
    def __del__(self):
        self.window.destroy()
        rclpy.shutdown()
        self._thread.join()
        
    def create_interfaces(self):
        self._user_input_pub = self.create_publisher(String, '/gui/user_input', 1)
        self.create_subscription(String, "llm_response", self.llm_response_callback, 1)
        self.create_subscription(String, "function_list", self.function_list_callback, 1)

    def start_node_async(self):
        self._thread = Thread(target=rclpy.spin, args=(self,))
        self._thread.start()

    def on_select_bottle(self):
        selected_bottle = self.bottle_var.get()
        grams = self.gram_entry.get()
        if not selected_bottle:
            messagebox.showerror("Error", "재료를 선택해주세요.")
            return
        elif not grams.isdigit() or int(grams) > 400:
            messagebox.showerror("Error", "양의 정수값(0~400)을 입력하세요.")
            return

        user_input = f"{selected_bottle} 재료를 {grams}[g] 뿌려줘."
        if messagebox.askokcancel("재확인", user_input):
            self.send_user_input(user_input)
            self.gram_entry.delete(0, tk.END)

    def on_submit_llm_command(self):
        command = self.command_entry.get("1.0", tk.END).strip()
        if command and messagebox.askokcancel("재확인", f"LLM 명령문: {command}"):
            self.send_user_input(command)
            print("Waiting for a LLM response.")
    def send_user_input(self, input: str):
        msg = String()
        msg.data = input
        self._user_input_pub.publish(msg)

    def llm_response_callback(self, msg):
        self.llm_response = msg.data
        print("LLM Response Received: ", self.llm_response)
        # LLM response
        self.response_entry.insert(tk.CURRENT, f"{self.llm_response_number}. {self.llm_response}\n")
        self.llm_response_number += 1
        # flush the last response
        self.llm_response = None

    def function_list_callback(self, msg):
        self.task_list = list(msg.data)
        print("-----------------------------")
        print(self.task_list)
        print("-----------------------------")
        self.open_supervisor_window()

    def on_delete_llm_response(self):
        self.response_entry.delete("1.0", tk.END)
        self.llm_response_number = 1

    def open_supervisor_window(self):
        supervisor_window = tk.Toplevel(self.window)
        supervisor_window.title("Supervisor frame")
        supervisor_window.geometry("600x500")
        
        button_frame = tk.Frame(supervisor_window)
        button_frame.pack(pady=10)

        self.pause_button = tk.Button(self.button_frame, text="정지", command=lambda: self.on_robot_button("pause"))
        self.pause_button.grid(row=0, column=0, padx=10)
        self.resume_button = tk.Button(self.button_frame, text="재개", state=tk.DISABLED, command=lambda: self.on_robot_button("resume"))
        self.resume_button.grid(row=0, column=1, padx=10)
        self.reset_button = tk.Button(self.button_frame, text="초기화", state=tk.DISABLED, command=lambda: self.on_robot_button("reset"))
        self.reset_button.grid(row=0, column=2, padx=10)
        self.open_left_gripper_button = tk.Button(self.button_frame, text="왼쪽 그리퍼 열기", state=tk.DISABLED, command=lambda: self.on_robot_button("open_left_gripper"))
        self.open_left_gripper_button.grid(row=0, column=3, padx=10)
        self.open_right_gripper_button = tk.Button(self.button_frame, text="오른쪽 그리퍼 열기", state=tk.DISABLED, command=lambda: self.on_robot_button("open_right_gripper"))
        self.open_right_gripper_button.grid(row=0, column=4, padx=10)

        self.open_task_progress_window(supervisor_window)
        
    def on_robot_button(self, action):
        success_check = 0
        match action:
            case 'pause':
                result = self.tasks.pause()
                if result == success_check: # pause success
                    print("Pause success")
                    self.pause_button.config(state=tk.DISABLED)
                    self.resume_button.config(state=tk.NORMAL)
                    self.reset_button.config(state=tk.NORMAL)
                    self.open_left_gripper_button.config(state=tk.NORMAL)
                    self.open_right_gripper_button.config(state=tk.NORMAL)
                else:
                    print("Pause failed")
            case 'resume':
                result = self.tasks.resume()
                if result == success_check: # resume success
                    print("Resume success")
                    self.pause_button.config(state=tk.NORMAL)
                    self.resume_button.config(state=tk.DISABLED)
                    self.reset_button.config(state=tk.DISABLED)
                    self.open_left_gripper_button.config(state=tk.DISABLED)
                    self.open_right_gripper_button.config(state=tk.DISABLED)
                else:
                    print("Resume failed")
            case 'reset':
                result = self.tasks.reset()
                if result == success_check: # reset success
                    print("Reset success")
                    self.pause_button.config(state=tk.NORMAL)
                    self.resume_button.config(state=tk.DISABLED)
                    self.reset_button.config(state=tk.DISABLED)
                    self.open_left_gripper_button.config(state=tk.DISABLED)
                    self.open_right_gripper_button.config(state=tk.DISABLED)
                else:
                    print("Resume failed")
            case 'open_left_gripper':
                result = self.tasks.control_gripper(left=0)
                if result == success_check: # reset success
                    print("Open left gripper success")
                    self.pause_button.config(state=tk.DISABLED)
                    self.resume_button.config(state=tk.DISABLED)
                    self.reset_button.config(state=tk.NORMAL)
                    self.open_left_gripper_button.config(state=tk.NORMAL)
                    self.open_right_gripper_button.config(state=tk.NORMAL)
                else:
                    print("Open left gripper failed")
            case 'open_right_gripper':
                result = self.tasks.control_gripper(right=0)
                if result == success_check: # reset success
                    print("Open right gripper success")
                    self.pause_button.config(state=tk.DISABLED)
                    self.resume_button.config(state=tk.DISABLED)
                    self.reset_button.config(state=tk.NORMAL)
                    self.open_left_gripper_button.config(state=tk.NORMAL)
                    self.open_right_gripper_button.config(state=tk.NORMAL)
                else:
                    print("Open right gripper failed")       

    def open_task_progress_window(self, supervisor_window):
        if not self.task_canvas:
            self.task_canvas = tk.Canvas(supervisor_window, width=200, height=700)
            self.task_canvas.pack()
            self.load_arrow_image()
            self.create_task_box()
            self.current_task_index = 0
            self.running = True
            Thread(target=self.run_task_updates).start()  # 작업 업데이트 시작
            self.update_task(True)

    def load_arrow_image(self):
        arrow_img = Image.open("/home/sdcrobot/ros2_ws/src/sd_external_msgs/examples/images/arrow.png").resize((30, 30))
        self.arrow_image = ImageTk.PhotoImage(arrow_img)
        
    def create_task_box(self):
        box_width = 150
        box_height = 50
        y_start = 30
        self.task_box.clear()
        self.task_labels.clear()       
        for i, task in enumerate(self.task_list):
            frame = self.task_canvas.create_rectangle(25, y_start, 25 + box_width, y_start + box_height, fill="white")
            label = self.task_canvas.create_text(100, y_start + box_height // 2, text=task, font=("Arial", 12), anchor="center")
            self.task_box.append(frame)
            self.task_labels.append(label)
            y_start += box_height + 40
            
            if i < len(self.task_list) - 1:
                self.task_canvas.create_image(100, y_start - 20, image=self.arrow_image)
            
    def close_window(self):
        if self.task_canvas:
            self.task_canvas.destroy()
            self.task_canvas = None
            self.running = False 
            
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
        for _ in range(len(self.task_list)):
            if not self.running or not self.task_canvas:
                break
            self.window.after(0, self.update_task, False)
            time.sleep(3) 

            self.window.after(0, self.update_task, True)
            self.current_task_index += 1
            if self.current_task_index >= len(self.task_list):
                break
            
if __name__ == "__main__":
    rclpy.init()
    gui = GUI(tasks.TaskExecutionClient())
