# 这一版本实现了实时显示进度时间
# 但bug在点击一次记录开始事件后，时间异常问题

import tkinter as tk
import time
import csv
import threading

class ProgressBarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("进度条应用")

        self.start_time = None
        self.end_time = None
        self.product_id = None
        self.playing = False
        self.start_from = "0:00:00"
        self.current_play_time = 0

        self.progress = tk.DoubleVar()
        self.progress.set(0.0)

        self.create_widgets()

        self.play_thread = None

    def create_widgets(self):

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
        if self.playing:
            self.start_time = self.current_play_time
            self.start_from = self.format_time(self.start_time)
            self.start_from_entry.delete(0, tk.END)
            self.start_from_entry.insert(0, self.start_from)
            print(f"开始时间已记录: {self.start_from}")
        else:
            print("请先开始播放以记录开始时间")

    def record_end_time(self):
        if self.playing:
            self.end_time = self.current_play_time
            end_time_str = self.format_time(self.end_time)
            print(f"结束时间已记录: {end_time_str}")
        else:
            print("请先开始播放以记录结束时间")

    def save_records(self):
        product_id = self.product_id_entry.get()
        if not product_id:
            print("请输入产品ID")
            return

        if self.start_time is not None and self.end_time is not None:
            record = [self.format_time(self.start_time), self.format_time(self.end_time), product_id]
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
        if self.playing:
            print("播放已开始")
            return

        self.playing = True
        self.start_time = time.time()
        self.current_play_time = 0
        self.progress.set(0)

        # 启动计时线程
        self.play_thread = threading.Thread(target=self.play_progress)
        self.play_thread.daemon = True
        self.play_thread.start()

    def play_progress(self):
        while self.playing:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            if elapsed_time > 0:
                self.current_play_time = self.parse_time(self.start_from) + elapsed_time

                if self.end_time is not None:  # 添加条件来检查 self.end_time 是否为 None
                    total_time = self.parse_time(self.start_from) + self.parse_time(self.end_time)
                    progress_percentage = (self.current_play_time / total_time) * 100
                else:
                    progress_percentage = 0  # 如果 self.end_time 为 None，则进度为 0

                self.progress.set(progress_percentage)
            self.root.update_idletasks()  # 更新GUI以显示进度
            time.sleep(0.1)  # 减小计时器的CPU使用

            self.update_progress_time()

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
