import tkinter as tk
import json
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

#クイズゲーム
class SelectQuiz:
    def __init__(self,screen,category,difficulty,back_title=None,back_difficulty=None):
        self.screen = screen
        self.category = category
        self.difficulty = difficulty
        self.back_title = back_title
        self.back_difficulty = back_difficulty
        self.score = 0 
        self.index = 0 
        self.questions = self.load_questions()
        #クイズ画面
        self.frame = tk.Frame(screen)
        self.frame.pack(expand=True)
        self.question_label = tk.Label(self.frame,text="",font=("Meiryo",14),wraplength=700,justify="left")
        self.question_label.grid(row=0,column=0,columnspan=2,pady=10,sticky="w")
        self.code_text = tk.Text(self.frame,height=6,width=60,font=("Consolas",12),bg="#f5f5f5")
        self.code_text.grid(row=1,column=0,columnspan=2,pady=5)
        self.code_text.config(state="disabled")

        #選択肢表示用ボタン
        self.buttons = []
        
        for i in range(4):
            button = tk.Button(self.frame,text="",width=40,height=3,command=lambda i=i: self.check_answer(i))
            self.buttons.append(button)
        #結果表示用ボタン
        self.result = tk.Label(self.frame,text="",font=("Meiryo",12))
        self.result.grid(row=6,column=0,columnspan=2,pady=10)
        #解説表示
        self.explanation = tk.Label(self.frame,text="",font=("Meiryo",11),wraplength=600,justify="left",fg="blue")
        self.explanation.grid(row=7,column=0,columnspan=2,pady=10)
        #次へボタン
        self.next_button = tk.Button(self.frame,text="次へ",state="disabled",command=self.show_question)
        self.next_button.grid(row=8,column=0,columnspan=2,pady=10)
        self.show_question()

    #問題抽出
    def load_questions(self):
        #問題を読み込む
        with open(BASE_DIR / "questions_select.json", "r", encoding="utf-8") as f:
            all_questions = json.load(f)
        filtered = [ question for question in all_questions if question["category"] == self.category and question["difficulty"] == self.difficulty ]
        return random.sample(filtered,min(5,len(filtered)))
    
    #問題表示
    def show_question(self):
        if self.index >= len(self.questions):
            self.show_result()
            return
        question = self.questions[self.index]
        self.question_label.config(
            text=f"問題 {self.index+1}/{len(self.questions)}\n\n{question['question']}"
        )

        code = question.get("code", "")

        self.code_text.config(state="normal")
        self.code_text.delete("1.0", tk.END)

        if code:
            self.code_text.insert("1.0", code)
            self.code_text.grid()
        else:
            self.code_text.grid_remove()

        self.code_text.config(state="disabled")
        for i,choice in enumerate(question["choices"]):
            self.buttons[i].config(text=choice)
            self.buttons[i].grid(row=i+2,column=0,columnspan=2,pady=5,sticky="we")
            self.buttons[i].config(state="normal",bg="SystemButtonFace")
        self.result.config(text="")
        self.explanation.config(text="")
        self.next_button.config(state="disabled")

    #解答処理
    def check_answer(self,selected):
        question = self.questions[self.index]
        correct = question["answer_index"]
        explanation = question.get("explanation","解説はありません。")

        for button in self.buttons:
            button.config(state="disabled")
        #正解、不正解の判定
        if selected == correct:
            self.score += 1
            self.result.config(text="正解！",fg="green")
            self.buttons[selected].config(bg="lightgreen")
        else:
            self.result.config(text="不正解",fg="red")
            self.buttons[selected].config(bg="salmon")
            self.buttons[correct].config(bg="lightgreen")
        #解説表示
        self.explanation.config(text=f"【解説】\n{explanation}")
        self.index += 1
        self.next_button.config(state="normal")
    
    #結果画面
    def show_result(self):
        for button in self.buttons:
            button.grid_remove()
        self.next_button.grid_remove()
        self.explanation.config(text="")
        accuracy = self.score / len(self.questions)
        rank = (
            "S" if accuracy == 1 else
            "A" if accuracy >= 0.8 else
            "B" if accuracy >= 0.6 else
            "C" if accuracy >= 0.4 else
            "D"
        )
        self.question_label.config(text="クイズ終了！")
        self.code_text.grid_remove()
        self.result.config(
            text=f"スコア: {self.score}/{len(self.questions)}\n"
                 f"正答率: {accuracy*100:.0f}%\n"
                 f"ランク: {rank}"
        )
        
        if self.back_difficulty:
            tk.Button(
                self.frame,
                text="難易度選択へ戻る",
                command=self.back_difficulty
            ).grid(row=8,column=1,pady=10)

        if self.back_title:
            tk.Button(
                self.frame,
                text="タイトルへ戻る",
                command=self.back_title
            ).grid(row=8,column=0,pady=10)
        