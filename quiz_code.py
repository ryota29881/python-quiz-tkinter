import tkinter as tk
from tkinter import scrolledtext
import ast
import json
import random
from io import StringIO
import contextlib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

#AST+実行判定
class ASTJudge:
    def evaluate(self,code,rules):
        tree = ast.parse(code)
        #ASTチェック
        if not self.ast_check(tree,rules):
            return False
        #実行チェック
        if "execution" in rules:
            return self.execute_check(code,rules["execution"])
        return True

    #ASTチェック本体
    def ast_check(self,tree,rules):
        checks = [
            ("assignment", self.check_assignment),
            ("print", self.check_print),
            ("function", self.check_function),
            ("function_call", self.check_function_call),
            ("class", self.check_class),
            ("list_assignment", self.check_list_assignment),
            ("dict_assignment", self.check_dict_assignment),
            ("compare", self.check_compare),
        ]

        for rule_name, func in checks:
            if rule_name in rules:
                if not func(tree, rules[rule_name]):
                    return False

        if rules.get("for_loop"):
            if not self.check_for_loop(tree):
                return False

        if rules.get("while_loop"):
            if not self.check_while_loop(tree):
                return False

        if rules.get("if_statement"):
            if not self.check_if_statement(tree):
                return False
            
        if rules.get("return_statement"):
            if not self.check_return(tree):
                return False
            
        if rules.get("range_used"):
            if not self.check_range(tree):
                return False

        return True
    #実行チェック
    def execute_check(self,code,rule):
        safe_globals = {
            "__builtins__":{
                "print":print,
                "range":range,
                "len":len
                }
        }
        local_env = {}
        output = StringIO()

        try:
            with contextlib.redirect_stdout(output):
                exec(code,safe_globals,local_env)
        except Exception:
            return False
        
        if "variables" in rule:
            for var,expected in rule["variables"].items():
                if var not in local_env:
                    return False
                if local_env[var] != expected:
                    return False
        
        if "output" in rule:
            actual = output.getvalue().strip()
            if actual != str(rule["output"]):
                return False
        
        if "function_result" in rule:
            func_name = rule["function_result"]["name"]
            args = rule["function_result"]["args"]
            expected = rule["function_result"]["expected"]
            if func_name not in local_env:
                return False
        
            try:
                result = local_env[func_name](*args)
            except Exception:
                return False
            
            if result != expected:
                return False
    
        return True
    
    def contains_variable(self,node,variable):
        return any(isinstance(n,ast.Name) and n.id == variable for n in ast.walk(node))
    
    def check_assignment(self,tree,rule):
        variable = rule["variable"]
        value = rule["value"]

        for node in ast.walk(tree):
            if isinstance(node,ast.Assign):
                for target in node.targets:
                    if (
                        isinstance(target,ast.Name)
                        and target.id == variable
                        and isinstance(node.value, ast.Constant)
                        and node.value.value == value
                    ):
                        return True
        return False
    
    def check_print(self,tree,rule):
        variable = rule["variable"]

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "print"
            ):
                for arg in node.args:
                    if self.contains_variable(arg, variable):
                        return True
        return False
    #for文確認
    def check_for_loop(self, tree):
        return any(isinstance(n, ast.For) for n in ast.walk(tree))
    
    #while文確認
    def check_while_loop(self, tree):
        return any(isinstance(n, ast.While) for n in ast.walk(tree))
    
    #if文確認
    def check_if_statement(self, tree):
        return any(isinstance(n, ast.If) for n in ast.walk(tree))
    
    #return確認
    def check_return(self,tree):
        return any(isinstance(n,ast.Return) for n in ast.walk(tree))
    
    #range確認
    def check_range(self,tree):
        for node in ast.walk(tree):
            if(
                isinstance(node,ast.Call)
                and isinstance(node.func,ast.Name)
                and node.func.id == "range"
            ):
                return True
        return False
    
    #関数確認
    def check_function(self, tree, rule):
        for node in ast.walk(tree):
            if(isinstance(node, ast.FunctionDef) and node.name == rule["name"]):
                if "arg_count" in rule:
                    return (len(node.args.args) == rule["arg_count"])
                return True
        return False

    def check_function_call(self,tree,rule):
        return any(
            isinstance(node,ast.Call)
            and isinstance(node.func,ast.Name)
            and node.func.id == rule["name"]
            for node in ast.walk(tree)
        )

    #クラス確認
    def check_class(self, tree, rule):
        return any(
            isinstance(n, ast.ClassDef) and n.name == rule["name"]
            for n in ast.walk(tree)
        )

    #リスト確認
    def check_list_assignment(self, tree, rule):
        variable = rule["variable"]
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                targets = [t.id for t in node.targets if isinstance(t,ast.Name)]
                if variable in targets:
                    if isinstance(node.value,ast.List):
                        if "length" in rule:
                            return(len(node.value.elts) == rule["length"])
                        return True
        return False
    
    #辞書型確認
    def check_dict_assignment(self, tree, rule):
        variable = rule["variable"]
        return any(
            isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == variable for t in n.targets)
            and isinstance(n.value, ast.Dict)
            for n in ast.walk(tree)
        )
    
    def check_compare(self,tree,rule):
        operator_map = {
            "Gt":ast.Gt,
            "Lt":ast.Lt,
            "Eq":ast.Eq,
            "NotEq":ast.NotEq,
            "GtE":ast.GtE,
            "LtE":ast.LtE
        }
        target = operator_map[rule["operator"]]
        
        if target is None:
            return False
        
        for node in ast.walk(tree):
            if isinstance(node,ast.Compare):
                for op in node.ops:
                    if isinstance(op,target):
                        return True
        return False

#クイズゲーム
class CodeQuiz:
    def __init__(self,screen,difficulty=None,back_func=None):
        self.screen = screen
        self.difficulty = difficulty
        self.back_callback = back_func
        self.judge = ASTJudge()
        self.all_questions = []
        self.used_ids = set()
        self.quiz = None
        self.answered = False
        self.build_ui()
        self.load_questions()
        self.next_question()

    def load_questions(self):
        with open(BASE_DIR / "questions_code.json", encoding="utf-8") as f:
            all_questions = json.load(f)

        if self.difficulty:
            self.all_questions = [question for question in all_questions if question.get("difficulty") == self.difficulty]
        else:
            self.all_questions = all_questions
        random.shuffle(self.all_questions)

    def build_ui(self):
        self.quiz_frame = tk.Frame(self.screen)
        self.quiz_frame.pack(fill="both", expand=True)
        self.question_label = tk.Label(self.quiz_frame, font=("Meiryo", 12), justify="left")
        self.question_label.pack(pady=10)
        self.code_input = scrolledtext.ScrolledText(self.quiz_frame, width=90, height=15)
        self.code_input.pack()
        button_frame = tk.Frame(self.quiz_frame)
        button_frame.pack(pady=10)
        self.submit_button = tk.Button(button_frame, text="採点", command=self.check_answer)
        self.submit_button.pack(side=tk.LEFT, padx=5)
        self.next_button = tk.Button(button_frame, text="別の問題", command=self.next_question)
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.next_button.config(state=tk.DISABLED)

        if self.back_callback:
            self.back_button = tk.Button(button_frame, text="戻る", command=self.back_callback)
            self.back_button.pack(side=tk.LEFT, padx=5)

        self.result_box = scrolledtext.ScrolledText(self.quiz_frame, height=10)
        self.result_box.pack()
        self.result_box.config(state=tk.DISABLED)

    def pick_question(self):
        available = [question for question in self.all_questions if id(question) not in self.used_ids]

        if not available:
            return None
        
        return random.choice(available)
    
    def next_question(self):
        question = self.pick_question()

        if question is None:
            self.show_finished()
            return
        
        self.quiz = question
        self.show_question()

    def show_question(self):
        self.answered = False
        self.question_label.config(text=f"問題\n\n{self.quiz['question']}")
        self.code_input.config(state=tk.NORMAL)
        self.code_input.delete("1.0", tk.END)
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)
        self.result_box.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.DISABLED)

    def check_answer(self):
        if self.answered:
            return

        code = self.code_input.get("1.0", tk.END)
        quiz = self.quiz

        try:
            result = self.judge.evaluate(code, quiz["rules"])
            self.result_box.config(state=tk.NORMAL)
            self.result_box.delete("1.0", tk.END)

            if result:
                self.result_box.insert(tk.END, "⭕ 正解\n\n")
                self.used_ids.add(id(quiz))
            else:
                self.result_box.insert(tk.END, "❌ 不正解\n\n")

            self.result_box.insert(tk.END, quiz["explanation"])
            self.next_button.config(state=tk.NORMAL)
            self.submit_button.config(state=tk.DISABLED)
            self.code_input.config(state=tk.DISABLED)
            self.answered = True

        except SyntaxError as e:
            self.result_box.config(state=tk.NORMAL)
            self.result_box.delete("1.0", tk.END)
            self.result_box.insert(tk.END, f"⚠ 構文エラー\n\n{e}")
            self.result_box.config(state=tk.DISABLED)
    
    def show_finished(self):
        self.question_label.config(text="")
        self.result_box.config(state=tk.NORMAL)
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert(tk.END,"この難易度の問題はすべて正解しました！\n")
        self.result_box.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)

        if hasattr(self, "back_button"):
            self.back_button.config(state=tk.NORMAL)
        
        finish_frame = tk.Frame(self.quiz_frame)
        finish_frame.pack(pady=10)
        tk.Button(finish_frame,text="タイトルへ戻る",command=self.back_callback).pack(side=tk.LEFT, padx=10)
        tk.Button(finish_frame,text="別の難易度へ",command=self.go_to_difficulty_select).pack(side=tk.LEFT, padx=10)

    def go_to_difficulty_select(self):
            self.quiz_frame.destroy()
            self.screen.event_generate("<<ShowCodeDifficulty>>")