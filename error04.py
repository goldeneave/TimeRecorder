# 这一版本实现了从指定时间点的二倍开始计时
# 也就是存在开始时刻的问题，以及没有加入倍速
# 这一版本正在解决倍速的问题

import tkinter as tk
import time
import csv
import threading

class ProgressBarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Recorder | Coded by ")

        self.start_time = None
        self.end_time = None
        self.product_id = None
        self.playing = False
        self.paused = False
        self.resumed = False
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

        # 文件名输入框
        self.file_name_label = tk.Label(self.root, text="File Name:")
        self.file_name_label.pack()
        self.file_name_entry = tk.Entry(self.root)
        self.file_name_entry.pack()

        # 保存按钮
        self.save_button = tk.Button(self.root, text="保存记录", command=self.save_records)
        self.save_button.pack()

        # 按钮：开始播放
        self.play_button = tk.Button(self.root, text="开始播放", command=self.start_play)
        self.play_button.pack()


        # 按钮：暂停播放
        self.pause_button = tk.Button(self.root, text="暂停播放", command=self.pause_play)
        self.pause_button.pack()

        # 按钮：恢复播放
        self.resume_button = tk.Button(self.root, text="恢复播放", command=self.resume_play)
        self.resume_button.pack()

        # 框：设置开始计时位置
        self.start_from_label = tk.Label(self.root, text="Start From:")
        self.start_from_label.pack()
        self.start_from_entry = tk.Entry(self.root)
        self.start_from_entry.insert(0, self.start_from)
        self.start_from_entry.pack()

        # 绑定 Enter 键事件处理函数
        self.start_from_entry.bind("<Return>", self.update_start_from)

        # 显示进度时间的标签
        self.progress_time_label = tk.Label(self.root, text="Progress Time: 00:00:00")
        self.progress_time_label.pack()

        # 控制台文本框
        self.console_text = tk.Text(self.root, wrap=tk.WORD)
        self.console_text.pack()


    def record_start_time(self):
        if self.playing:
            self.start_time = self.format_time(self.current_play_time)  # 记录当前的 progress time 作为起始时间
            message = f"开始时间已记录: {self.start_time}\n"
            self.update_console(message)
            if hasattr(self, 'start_from_saved'):
                self.start_from = self.start_from_saved  # 还原 start_from 值
                self.start_from_entry.delete(0, tk.END)
                self.start_from_entry.insert(0, self.start_from_saved)
            return True  # 记录成功
        else:
            message = "请先开始播放以记录开始时间\n"
            self.update_console(message)
            return False  # 记录失败

    def record_end_time(self):
        if self.playing:
            self.end_time = self.format_time(self.current_play_time)  # 记录当前的 progress time 作为结束时间
            message = f"结束时间已记录: {self.end_time}\n"
            self.update_console(message)
            if hasattr(self, 'start_from_saved'):
                self.start_from = self.start_from_saved  # 还原 start_from 值
                self.start_from_entry.delete(0, tk.END)
                self.start_from_entry.insert(0, self.start_from_saved)
            return True  # 记录成功
        else:
            message = "请先开始播放以记录结束时间\n"
            self.update_console(message)
            return False  # 记录失败

    def save_records(self):
        product_id = self.product_id_entry.get()
        file_name = self.file_name_entry.get()  # 获取文件名

        if not product_id or not file_name:  # 检查产品ID和文件名
            message = "请输入产品ID和文件名\n"
            self.update_console(message)
            return

        if self.start_time is not None and self.end_time is not None:
            record = [self.start_time, self.end_time, product_id, file_name]  # 直接保存整数表示的时间
            with open("progress_records.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(["start_time", "end_time", "product_id", "file_name"])  # 更新列名
                writer.writerow(record)

            message = f"记录已保存到 progress_records.csv\n"
            self.update_console(message)
        else:
            message = "请先记录开始时间和结束时间\n"
            self.update_console(message)

    def format_time(self, timestamp):
        hours, remainder = divmod(timestamp, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

    def update_start_from(self, event):
        new_start_from = self.start_from_entry.get()
        if self.validate_start_from(new_start_from):
            self.start_from = new_start_from
            message = f"Start From 时间已更新为: {new_start_from}\n"
            self.update_console(message)
        else:
            message = "无效的时间格式，请使用 HH:MM:SS 格式\n"
            self.update_console(message)

    def validate_start_from(self, start_from):
        # 验证时间格式是否为 hh:mm:ss
        try:
            h, m, s = map(int, start_from.split(":"))
            if 0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60:
                return True  # 时间格式有效
        except ValueError:
            pass
        return False  # 时间格式无效

    def start_play(self):
        if self.playing:
            message = "播放已开始"
            self.update_console(message)
            return

        self.playing = True
        self.paused = False  # 重置暂停状态

        # 计算需要跳过的时间
        self.skip_time = self.parse_time(self.start_from)

        # 设置计时起始时间，不包含 start_from 时间
        self.start_time = self.parse_time("0:00:00")
        self.progress.set(0.0)

        message = f"开始播放，播放起始时间为 {self.start_from}\n"
        self.update_console(message)

        # 启动计时线程
        self.play_thread = threading.Thread(target=self.play_progress)
        self.play_thread.daemon = True
        self.play_thread.start()

    def pause_play(self):
        if self.playing and not self.paused:
            self.paused = True
            message = "播放已暂停\n"
            self.update_console(message)
        else:
            message = "请先开始播放以暂停播放\n"
            self.update_console(message)
            return False  # 记录失败

    def resume_play(self):
        if self.playing and self.paused:
            self.paused = False
            message = "恢复播放\n"
            self.update_console(message)
        else:
            message = "请先开始播放以恢复播放\n"
            self.update_console(message)
            return False  # 记录失败

    def play_progress(self):
        start_from_time = self.parse_time(self.start_from)
        elapsed_time = 0

        while self.playing:
            if not self.paused:
                current_time = start_from_time + elapsed_time
                self.current_play_time = current_time

                if self.end_time is not None:
                    total_time = start_from_time + self.parse_time(self.end_time)
                    progress_percentage = ((self.current_play_time - start_from_time) / (
                                total_time - start_from_time)) * 100
                else:
                    total_time = 0
                    progress_percentage = 0

                self.progress.set(progress_percentage)

                self.root.update_idletasks()
                time.sleep(0.1)

                elapsed_time += 0.1

                self.update_progress_time()
            else:
                time.sleep(0.1)

    def update_progress_time(self):
        if self.playing:
            formatted_time = self.format_time(self.parse_time(self.start_from) + self.current_play_time)
            self.progress_time_label.config(text=f"Progress Time: {formatted_time}")
            self.root.after(1000, self.update_progress_time)

    def parse_time(self, time_str):
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

    def update_console(self, message):
        self.console_text.insert(tk.END, message)
        self.console_text.see(tk.END)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProgressBarApp(root)
    root.mainloop()
