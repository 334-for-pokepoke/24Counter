# 24Counter
プログラムのように製作できるカウンターです．

## default.txt
* 表示するテキストを入力してください．
* アルファベット及びアンダーバーで構成された単語をprefix（デフォルトでは「//」）で囲むことで変数扱いできます．

![variable](https://github.com/334-for-pokepoke/24Counter/blob/main/img/default.png)


## variable.txt
* 変数の宣言や，テキストボックス・ボタンの設定を行います．
* １行あたり1つの変数宣言又はオブジェクトの宣言まで可能です．
* ボタン名は「\n」と入力すると改行になります．
* default.txtに存在しているのに宣言されなかった変数は自動的に整数型で0で初期化されます．
* 画面に表示されない変数についても宣言し，使用することが可能です．

* 変数宣言
  * XXXという整数を宣言する場合は，「XXX:int」又は「XXX:int:100」のように入力します．後者の場合は100で初期化されます．
  *  変数型は現段階では整数型「int」と文字列型「text」のみです．
* ボタン
  * YYYと書かれたボタンを制作し，押された場合に変数XXXに1を加え，変数xxxを10減らす場合は次のように入力します．
  * button:YYY:XXX++, xxx = xxx-10
  * このように，押された場合の命令はカンマ区切りで複数入力できます．
* テキストボックス
  * テキストボックスは次のように作成します
  * ZZZ:text
  * textbox:テキスト１を入力:ZZZ
  * テキストボックスは第二引数で識別されているため，第二引数を持つテキストボックスを作らないように気をつけてください．

* ボタンで使用できる命令は，単純な式（x=y=0のように代入が複数回行われないもの）のみです．
* また，使用できる演算子は+-\*^()及び++, --, +=, -=のみです（文字列については加算のみ）.
* 予め用意されている関数は現状save()のみです．
* save()関数は各変数の値をbkp.txtに書き出します．


![variable](https://github.com/334-for-pokepoke/24Counter/blob/main/img/variable.png)

## config.ini
* [DEFAULT]
  * prefix : default.txtではこの文字で囲んだものを変数と見なします．
* [TextWindow]
  * title : ウインドウタイトルです．
  * xsize, ysize : ウインドウのx, yサイズです．
  * font  : 文字のフォントです．文字ごとのフォント変更・装飾は現在未対応です．
  * size  : 文字サイズです．文字ごとのサイズ変更は現在未対応です．
  * str_color : 文字色です．カンマ区切りのRGB値で指定します．文字ごとの色変更は現在未対応です．
  * bg_color  : 背景色です．
* [ObjectWindow]
  * title : ウインドウタイトルです．
  * xsize, ysize : ウインドウのx, yサイズです．
  * font  : 文字のフォントです．文字ごとのフォント変更・装飾は現在未対応です．
  * size  : 文字サイズです．文字ごとのサイズ変更は現在未対応です．
  * str_color : ボタンの文字色です．ボタンごとの色変更は現在未対応です．
  * bg_color  : ボタンの背景色です．
  * button_size_x : ボタンの横幅です．1は半角「0」1文字分の横幅です．
  
![variable](https://github.com/334-for-pokepoke/24Counter/blob/main/img/exe1.png)
![variable](https://github.com/334-for-pokepoke/24Counter/blob/main/img/exe2.png)
