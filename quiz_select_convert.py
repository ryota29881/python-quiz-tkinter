import json
import os
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

EXCEL_FILE = BASE_DIR / "quiz_select.xlsx"
JSON_FILE = BASE_DIR / "questions_select.json"


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
        (
            q.get("question", "").strip(),
            q.get("code", "").strip()
        )
        for q in existing_data
    }

    add_count = 0
    skip_count = 0

    for _, row in df.iterrows():

        question = str(row["question"]).strip()

        if not question:
            continue

        if pd.isna(row.get("code")):
            code = ""
        else:
            code = str(row.get("code", "")).replace("\\n","\n").strip()

        question_key = (question,code)

        if question_key in existing_questions:
            skip_count += 1
            print(f"重複スキップ: {question}")
            continue

        try:
            answer_index = int(row["answer"])
        except Exception:
            print(f"回答番号エラー: {question}")
            continue

        if answer_index not in [0, 1, 2, 3]:
            print(f"回答番号エラー: {question}")
            continue

        explanation = str(row.get("explanation", "")).strip()

        quiz = {
            "category": str(row["category"]).strip(),
            "difficulty": str(row["difficulty"]).strip(),
            "question": question,
            "code": code,
            "choices": [
                str(row["choice1"]),
                str(row["choice2"]),
                str(row["choice3"]),
                str(row["choice4"])
            ],
            "answer_index": answer_index,
            "explanation": explanation
        }

        existing_data.append(quiz)
        existing_questions.add(question_key)

        add_count += 1

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(existing_data,f,ensure_ascii=False,indent=4)

    print()
    print("===== 完了 =====")
    print(f"追加件数 : {add_count}")
    print(f"重複件数 : {skip_count}")
    print(f"保存先   : {JSON_FILE}")


if __name__ == "__main__":
    main()