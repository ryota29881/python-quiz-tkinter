# PYTHON LEARNING QUIZ

Python・Tkinterで制作したクイズアプリを、職業訓練校での中間制作物として作成したポートフォリオ作品です。

「Pythonの知識をクイズ形式で学ぶ」という目的で、4択クイズとコード作成クイズを実装しています。
この作品をもとに、後にDjangoを使用したWebアプリケーションへ発展させました。

## 作品概要

- **4択クイズ**：Pythonの基礎問題を難易度別に出題
- **コード作成クイズ**：Pythonコードを入力して自動判定
- **解答・解説表示**：各問題の回答後に正誤と解説を表示
- **結果表示**：クイズ終了後にスコア・正答率・ランクを表示
- **問題データ管理**：問題データをJSONで管理
- **Excelからの問題登録**：Excelで作成した問題をJSONへ変換
- **ASTによるコード判定**：コード作成クイズの入力内容をPythonのASTで解析

## 技術スタック

- Python
- Tkinter
- JSON
- pandas
- openpyxl
- Python AST（コード判定）

## ディレクトリ構成

```text
python-quiz-app/
├── main.py                    # アプリ起動
├── quiz_select.py             # 4択クイズ
├── quiz_code.py               # コード作成クイズ
├── quiz_select_convert.py     # 4択問題のExcel → JSON変換
├── quiz_code_convert.py       # コード問題のExcel → JSON変換
├── questions_select.json      # 4択問題データ
├── questions_code.json        # コード作成問題データ
├── quiz_select.xlsx           # 4択問題の管理用Excel
├── quiz_code.xlsx             # コード作成問題の管理用Excel
├── requirements.txt
├── .gitignore
└── README.md
```

※ `__pycache__/`、Pythonのコンパイル済みファイルなどはGitHubへ公開しない構成にしています。

## 動作環境

- Python 3.10 以上を想定
- Tkinterが利用できる環境
- Windowsでの利用を想定

TkinterはPython標準ライブラリのため、通常は別途pipでインストールする必要はありません。

Excelから問題データを変換する機能を使用する場合は、`pandas` と `openpyxl` が必要です。

## ローカル環境での起動方法

### 1. リポジトリを取得

```bash
git clone https://github.com/ryota29881/python-quiz-tkinter
cd python-quiz-tkinter
```

### 2. 仮想環境を作成

Windowsの場合：

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. 必要なパッケージをインストール

```bash
pip install -r requirements.txt
```

### 4. アプリを起動

```bash
python main.py
```

## 問題データの追加・更新

問題データはExcelで管理し、変換スクリプトを使用してJSONへ反映できます。

### 4択クイズ

`quiz_select.xlsx` を編集したあと、以下を実行します。

```bash
python quiz_select_convert.py
```

`questions_select.json` に問題が反映されます。

### コード作成クイズ

`quiz_code.xlsx` を編集したあと、以下を実行します。

```bash
python quiz_code_convert.py
```

`questions_code.json` に問題が反映されます。

## コード作成クイズの判定について

コード作成クイズでは、入力されたPythonコードをAST（抽象構文木）で解析し、コードの構造を確認します。

主に以下のような内容を判定します。

- 変数への代入
- `print`
- 関数定義
- 関数呼び出し
- クラス
- リスト
- 辞書
- `for`
- `while`
- `if`
- `return`
- `range`
- 比較演算子

問題によっては、さらにコードを実行して、

- 変数の値
- 標準出力
- 関数の戻り値

なども確認します。

### 注意

コード作成クイズでは、入力されたPythonコードをアプリ内で評価・実行します。

そのため、**信頼できないコードを実行する用途や、ネットワーク越しに公開する用途には適していません**。

本リポジトリは、ローカル環境で学習用アプリとして使用することを想定しています。

## GitHubへ公開する際の注意

このプロジェクトでは、以下をGitHubへ公開しないよう `.gitignore` を設定しています。

- 仮想環境（`.venv/`、`venv/` など）
- `__pycache__/`
- Pythonのコンパイル済みファイル
- IDEの設定ファイル

問題データや管理用Excelファイルは、アプリの学習用データとしてリポジトリに含めています。

## 制作目的

職業訓練校でPython・Tkinterを使用して制作したクイズアプリを通して、

- Pythonの基礎知識
- TkinterによるGUI作成
- JSONによるデータ管理
- Excelからの問題データ変換
- ASTを利用したPythonコードの解析
- クラスを利用した機能分割

などを学習・実践しました。

その後、この作品をベースにDjangoを使用してWebアプリケーションへ発展させ、ユーザー認証、成績履歴、管理画面などの機能を追加しました。
