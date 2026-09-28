import tkinter as tk
import quiz_select
import quiz_code
import sys


screen = tk.Tk()
screen.title("クイズアプリ")
screen.geometry("900x800")

# 画面クリア
def clear_screen():
    for widget in screen.winfo_children():
        widget.destroy()

# アプリ終了
def exit_app():
    screen.destroy()   # Tkinter完全終了
    sys.exit()       # Pythonプロセス終了（確実用）

# タイトル画面
def show_title():
    clear_screen()

    tk.Label(screen,text="Pythonクイズアプリ",font=("Meiryo", 18)).pack(pady=30)
    tk.Button(screen,text="4択クイズ",width=25,command=show_category_select).pack(pady=10)
    tk.Button(screen,text="コード作成クイズ",width=25,command=start_code_quiz).pack(pady=10)

    #終了ボタン
    tk.Button(screen,text="終了",width=25,command=exit_app).pack(pady=20)

# クイズ種別選択
def show_category_select():
    clear_screen()

    tk.Label(screen,text="クイズの種別を選択",font=("Meiryo", 16)).pack(pady=30)
    tk.Button(screen,text="Python基礎問題",width=30,command=lambda: show_difficulty("basic")).pack(pady=10)
    tk.Button(screen,text="Python3認定基礎試験対策",width=30,command=lambda: show_difficulty("cert")).pack(pady=10)
    tk.Button(screen,text="タイトルへ戻る",width=20,command=show_title).pack(pady=20)

# 難易度選択
def show_difficulty(category):
    clear_screen()
    tk.Label(screen,text="難易度を選択",font=("Meiryo", 16)).pack(pady=30)
    tk.Button(screen,text="初級",width=20,command=lambda: start_quiz(category, "easy")).pack(pady=10)
    tk.Button(screen,text="中級",width=20,command=lambda: start_quiz(category, "normal")).pack(pady=10)
    tk.Button(screen,text="上級",width=20,command=lambda: start_quiz(category, "hard")).pack(pady=10)
    tk.Button(screen,text="種別選択へ戻る",width=20,command=show_category_select).pack(pady=10)
    tk.Button(screen,text="タイトルへ戻る",width=20,command=show_title).pack(pady=10)

# クイズ開始
def start_quiz(category, difficulty):
    clear_screen()
    quiz_select.SelectQuiz(
        screen,
        category,
        difficulty,
        back_title=show_title,
        back_difficulty=lambda: show_difficulty(category)
    )

# コードクイズ
def start_code_quiz():
    clear_screen()
    show_code_difficulty()

def show_code_difficulty():
    clear_screen()
    tk.Label(screen,text="コード作成クイズ（難易度選択）",font=("Meiryo", 16)).pack(pady=30)
    tk.Button(screen,text="初級",width=20,command=lambda: start_code("easy")).pack(pady=10)
    tk.Button(screen,text="中級",width=20,command=lambda: start_code("normal")).pack(pady=10)
    tk.Button(screen,text="上級",width=20,command=lambda: start_code("hard")).pack(pady=10)
    tk.Button(screen,text="タイトルへ戻る",width=20,command=show_title).pack(pady=20)

# コードクイズ開始
def start_code(difficulty):
    clear_screen()
    quiz_code.CodeQuiz(screen, difficulty, back_func=show_title)

def show_code_difficulty_event(event=None):
    show_code_difficulty()

screen.bind("<<ShowCodeDifficulty>>", show_code_difficulty_event)

# 起動
show_title()
screen.mainloop()