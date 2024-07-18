import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.font_manager as fm
import datetime

# 한글 폰트 설정
font_path = '/Users/kangminjung/Downloads/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf'
fontprop = fm.FontProperties(fname=font_path)

class MoodTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("기분 추적기")
        
        self.mood_data = []
        
        self.label = tk.Label(root, text="오늘 기분이 어떠신가요?", font=("맑은 고딕", 12))
        self.label.pack(pady=10)
        
        self.good_button = tk.Button(root, text="좋음", command=lambda: self.submit_mood("좋음", 3), font=("맑은 고딕", 10))
        self.good_button.pack(pady=5)
        
        self.bad_button = tk.Button(root, text="나쁨", command=lambda: self.submit_mood("나쁨", 1), font=("맑은 고딕", 10))
        self.bad_button.pack(pady=5)
        
        self.normal_button = tk.Button(root, text="보통", command=lambda: self.submit_mood("보통", 2), font=("맑은 고딕", 10))
        self.normal_button.pack(pady=5)
        
        self.reason_label = tk.Label(root, text="오늘 기분의 이유를 적어주세요:", font=("맑은 고딕", 12))
        self.reason_label.pack(pady=10)
        
        self.reason_entry = tk.Entry(root, width=50, font=("맑은 고딕", 10))
        self.reason_entry.pack(pady=10)
        
        self.show_button = tk.Button(root, text="기분 차트 보기", command=self.show_chart, font=("맑은 고딕", 10))
        self.show_button.pack(pady=20)

        self.view_records_button = tk.Button(root, text="기록 보기", command=self.view_records, font=("맑은 고딕", 10))
        self.view_records_button.pack(pady=5)

    def submit_mood(self, mood, intensity):
        reason = self.reason_entry.get()
        timestamp = datetime.datetime.now()
        self.mood_data.append((timestamp, mood, intensity))
        messagebox.showinfo("성공", f"기분이 기록되었습니다! (이유: {reason})")
        self.reason_entry.delete(0, tk.END)
        
    def show_chart(self):
        if self.mood_data:
            df = pd.DataFrame(self.mood_data, columns=['시간', '기분', '강도'])
            df['시간'] = pd.to_datetime(df['시간']).dt.hour + pd.to_datetime(df['시간']).dt.minute / 60.0
            
            colors = df['기분'].map({'좋음': 'yellow', '나쁨': 'red', '보통': 'gray'})
            
            plt.scatter(df['시간'], df['강도'], c=colors)
            plt.title("기분 빈도수", fontproperties=fontprop)
            plt.xlabel("시간", fontproperties=fontprop)
            plt.ylabel("기분 강도", fontproperties=fontprop)
            plt.xticks(range(0, 25), fontproperties=fontprop)
            plt.yticks(range(1, 4), ["나쁨", "보통", "좋음"], fontproperties=fontprop)
            plt.grid(True)
            plt.show()
        else:
            messagebox.showwarning("데이터 없음", "기록된 기분이 없습니다. 먼저 기분을 기록해 주세요.")

    def view_records(self):
        records_window = tk.Toplevel(self.root)
        records_window.title("기록 보기")

        text = tk.Text(records_window, font=("맑은 고딕", 10))
        text.pack(pady=10)

        if self.mood_data:
            for record in self.mood_data:
                text.insert(tk.END, f"시간: {record[0]}, 기분: {record[1]}, 이유: {record[2]}\n")
        else:
            text.insert(tk.END, "기록된 기분이 없습니다.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MoodTrackerApp(root)
    root.mainloop()
