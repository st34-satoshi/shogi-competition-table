# 将棋部OB会用の対戦表作成
## 準備するもの
- 参加者リストのcsvファイルをmain.pyと同じディレクトリに置く．文字コードはUTF-8.  
participants.csvファイルを参照．
- python3 が実行できる環境

## 実行方法
第一引数に対戦回数，第二引数に参加者リストのファイル名を指定する．(参加者リストのファイル名は省略可能)
```buildoutcfg
python3 main.py 3 participants.csv
```  
competition-table.csvファイルが作成される．

## 対戦相手の決定方法
- 現役はOBと対戦する
- 段が近い人を選択する
- 段が同じときは卒業年が近い人を選択する

## メモ
- 文字コードはUTF-8を使用している．Shift_JISを使いたいときは，csvファイルの読み込み(108行)と書き込み(161行)を直す．
- 現役の人数がOBより多いときは，プログラムを修正する必要がある．
- 対局場所を出力させたいときは，4行目のoutput_positionをTrueにする.