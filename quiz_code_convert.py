import json
import os
import pandas as pd
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

EXCEL_FILE = BASE_DIR / "quiz_code.xlsx"
JSON_FILE = BASE_DIR / "questions_code.json"


def is_filled(value):
    return pd.notna(value) and str(value).strip() != ""


def build_rules(row):
    rules = {}

    #変数代入
    if (
        is_filled(row.get("assignment_var"))
        and is_filled(row.get("assignment_value"))
        ):
        rules["assignment"] = {
            "variable": str(row["assignment_var"]).strip(),
            "value": smart_cast(row["assignment_value"])
        }

    #print
    if is_filled(row.get("print_var")):
        rules["print"] = {"variable": str(row["print_var"]).strip()}

    #関数定義
    if is_filled(row.get("function_name")):
        func_rule = {"name":str(row["function_name"]).strip()}
        if is_filled(row.get("arg_count")):
            func_rule["arg_count"] = smart_cast(row["arg_count"])
        rules["function"] = func_rule

    #関数呼び出し
    if is_filled(row.get("function_call")):
        rules["function_call"] = { "name": str( row["function_call"] ).strip() }

    #クラス
    if is_filled(row.get("class_name")):
        rules["class"] = {"name": str(row["class_name"]).strip()}

    #リスト
    if is_filled(row.get("list_var")):
        list_rule = {"variable":str(row["list_var"]).strip()}
        if is_filled(row.get("list_length")):
            list_rule["length"] = smart_cast(row["list_length"])
        rules["list_assignment"] = list_rule
    
    #辞書
    if is_filled(row.get("dict_var")):
        rules["dict_assignment"] = {"variable": str(row["dict_var"]).strip()}

    #for
    if str(row.get("for_loop", "")).strip().upper() == "TRUE":
        rules["for_loop"] = True

    #while
    if str(row.get("while_loop", "")).strip().upper() == "TRUE":
        rules["while_loop"] = True

    #if
    if str(row.get("if_statement", "")).strip().upper() == "TRUE":
        rules["if_statement"] = True

    #return
    if str(row.get("has_return", "") ).strip().upper() == "TRUE":
        rules["return_statement"] = True

    #range
    if str(row.get("range_used", "") ).strip().upper() == "TRUE":
        rules["range_used"] = True
    
    #比較演算子
    if is_filled(row.get("compare_op")):
        rules["compare"] = {"operator": str(row["compare_op"] ).strip() }

    #実行判定
    execution_rule = {}
    if (is_filled(row.get("exec_var")) and is_filled(row.get("exec_value"))):
        execution_rule["variables"] = {str(row["exec_var"]).strip(): smart_cast(row["exec_value"])}

    #出力判定
    if is_filled(row.get("expected_output") ):
        execution_rule["output"] = smart_cast(row["expected_output"])

    #関数戻り値判定
    if (
        is_filled( row.get( "function_result_name" ) )
        and is_filled( row.get( "function_result_args" ) )
        and is_filled( row.get( "function_result_expected" ) )
        ):
        execution_rule["function_result"] = {
            "name": str(row["function_result_name"]).strip(),
            "args": ast.literal_eval(str(row["function_result_args" ] ) ),
            "expected": smart_cast(row["function_result_expected"]) }
    if execution_rule:
        rules["execution"] = (execution_rule)
    return rules

def smart_cast(value):
    if not isinstance(value, str):
        return value

    v = value.strip()

    # bool
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False

    # int / float
    try:
        if "." in v:
            return float(v)
        return int(v)
    except:
        pass

    # list / dict
    try:
        return ast.literal_eval(v)
    except:
        pass

    # それ以外は文字列
    return v

def load_existing():
    if not os.path.exists(JSON_FILE):
        return []

    try:
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def main():
    if not os.path.exists(EXCEL_FILE):
        print(f"{EXCEL_FILE} が見つかりません")
        return

    df = pd.read_excel(EXCEL_FILE)

    existing_data = load_existing()

    existing_questions = {
        q.get("question", "").strip()
        for q in existing_data
    }

    added_count = 0
    skipped_count = 0

    for _, row in df.iterrows():

        question = str(row.get("question", "")).strip()

        if not question:
            continue

        if question in existing_questions:
            skipped_count += 1
            print(f"重複スキップ: {question}")
            continue

        quiz = {
            "difficulty": str(row.get("difficulty", "easy")).strip(),
            "question": question,
            "rules": build_rules(row),
            "explanation": str(row.get("explanation", "")).strip()
        }

        existing_data.append(quiz)
        existing_questions.add(question)

        added_count += 1

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(
            existing_data,
            f,
            ensure_ascii=False,
            indent=4
        )

    print()
    print("===== 完了 =====")
    print(f"追加件数 : {added_count}")
    print(f"重複件数 : {skipped_count}")
    print(f"保存先   : {JSON_FILE}")


if __name__ == "__main__":
    main()