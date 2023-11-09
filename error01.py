# 这一版本中，可以完成不精准的时间记录，当按下记录开始/结束时间时，始终时间为
# 进度条不能实时显示

import tkinter as tk
import time
import csv

class ProgressBarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("进度条应用")

        self.start_time = None
        self.end_time = None
        self.product_id = None
        self.play_start_time = None
        self.playing = False
        self.start_from = "0:00:00"
        self.current_play_time = 0

        self.progress = tk.DoubleVar()
        self.progress.set(0.0)

        self.create_widgets()

    def create_widgets(self):
        # 进度条
        self.progress_bar = tk.Scale(self.root, variable=self.progress, from_=0, to=100, orient="horizontal", showvalue=0)
        self.progress_bar.pack()

        # 按钮：记录开始时间
        self.record_start_button = tk.Button(self.root, text="记录开始时间", command=self.record_start_time)
        self.record_start_button.pack()

        # 按钮：记录结束时间
        self.record_end_button = tk.Button(self.root, text="记录结束时间", command=self.record_end_time)
        self.record_end_button.pack()

        # 产品ID输入框
        self.product_id_label = tk.Label(self.root, text="产品ID:")
        self.product_id_label.pack()
        self.product_id_entry = tk.Entry(self.root)
        self.product_id_entry.pack()

        # 保存按钮
        self.save_button = tk.Button(self.root, text="保存记录", command=self.save_records)
        self.save_button.pack()

        # 按钮：开始播放
        self.play_button = tk.Button(self.root, text="开始播放", command=self.start_play)
        self.play_button.pack()

        # 按钮：停止播放
        self.stop_button = tk.Button(self.root, text="停止播放", command=self.stop_play)
        self.stop_button.pack()

        # 框：设置开始计时位置
        self.start_from_label = tk.Label(self.root, text="Start From:")
        self.start_from_label.pack()
        self.start_from_entry = tk.Entry(self.root)
        self.start_from_entry.insert(0, self.start_from)
        self.start_from_entry.pack()

        # 显示进度时间的标签
        self.progress_time_label = tk.Label(self.root, text="Progress Time: 00:00:00")
        self.progress_time_label.pack()

    def record_start_time(self):
        self.start_time = self.current_play_time
        self.start_from = self.format_time(self.start_time)
        self.start_from_entry.delete(0, tk.END)
        self.start_from_entry.insert(0, self.start_from)
        print(f"开始时间已记录: {self.start_from}")

    def record_end_time(self):
        self.end_time = self.current_play_time
        end_time_str = self.format_time(self.end_time)
        print(f"结束时间已记录: {end_time_str}")

    def save_records(self):
        product_id = self.product_id_entry.get()
        if not product_id:
            print("请输入产品ID")
            return

        if self.start_time is not None and self.end_time is not None:
            record = [self.start_from, self.format_time(self.end_time), product_id]
            with open("progress_records.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(["start_time", "end_time", "product_id"])
                writer.writerow(record)

            print(f"记录已保存到progress_records.csv")
        else:
            print("请先记录开始时间和结束时间")

    def format_time(self, timestamp):
        hours, remainder = divmod(timestamp, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

    def start_play(self):
        if self.start_time is not None and self.end_time is not None:
            self.play_start_time = time.time() - self.parse_time(self.start_from)
            self.playing = True
            self.play_progress()

    def play_progress(self):
        if self.playing:
            current_time = time.time()
            elapsed_time = current_time - self.play_start_time
            self.current_play_time = self.parse_time(self.start_from) + elapsed_time
            progress_percentage = (self.current_play_time / (self.end_time - self.parse_time(self.start_from))) * 100
            self.progress.set(progress_percentage)
            if progress_percentage >= 100:
                self.playing = False
            else:
                self.root.after(10, self.play_progress)

            self.update_progress_time()

    def stop_play(self):
        self.playing = False

    def update_progress_time(self):
        if self.playing:
            formatted_time = self.format_time(self.current_play_time)
            self.progress_time_label.config(text=f"Progress Time: {formatted_time}")
            self.root.after(1000, self.update_progress_time)

    def parse_time(self, time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgressBarApp(root)
    root.mainloop()