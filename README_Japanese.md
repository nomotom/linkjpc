# linkjpc

目次:
- [INTRODUCTION](#INTRODUCTION)(はじめに)
- [MODULE CONFIGURATION](#MODULECONFIGURATION)(モジュール構成)
- [DATA FILES](#DATAFILES)(データファイル)
- [STEPS TO TRY ENTITY LINKING](#STEPSTOTRYENTITYLINKING)(エンティティリンキングを試してみる)
- [NOTES ON PREPROCESSING](#NOTESONPREPROCESSING)(前処理(オプショナル)に関する注意)
- [UNSOLVED ISSUES](#UNSOLVEDISSUES)(課題)
- [テスト](テスト)


## Introduction

**_linkjpc_** は [SHINRA2021-LinkJP](http://shinra-project.info/shinra2021linkjp/) (task1)という日本語Wikipediaのエンティティリンキングタスク用に開発したツールです。

### Task

SHINRA2021-LinkJPはWikipedia記事中の、あるエンティティ(事物)を指すテキスト（メンション, 例. _イタリア(Italy)_)を対応する記事ページ (例. [イタリア(Italy)](https://ja.wikipedia.org/wiki/%E3%82%A4%E3%82%BF%E3%83%AA%E3%82%A2)) にリンクするタスクで、Wikification（Wikipediaを対象としたエンティティリンキング）の一種です。

このタスクでは、メンションは単なるテキストではなく、元記事の指す事物の属性情報の一部として与えられます。例えばイタリアの都市の「ヴェネツィア」ページの場合、記事中の「イタリア」というメンションは属性「国」の値として与えられます。

メンションは以下の (a) (c) の例のように別のページを指すことが多いですが、例えば「別名」のような特別の属性の場合には元記事を指す場合もあります。

例 |元記事 (エンティティ) | 属性名|メンション / 属性値 | リンク先のページ(*1)
:----------------|:------|:---------------|:---------|:----
(a) |[ヴェネツィア](https://ja.wikipedia.org/wiki/?curid=30053) | 国| イタリア |[イタリア](https://ja.wikipedia.org/wiki/%E3%82%A4%E3%82%BF%E3%83%AA%E3%82%A2) 
(b) |[ヴェネツィア](https://ja.wikipedia.org/wiki/%E3%83%B4%E3%82%A7%E3%83%8D%E3%83%84%E3%82%A3%E3%82%A2) | 別名 | アドリア海の女王 |[ヴェネツィア](https://ja.wikipedia.org/wiki/%E3%83%B4%E3%82%A7%E3%83%8D%E3%83%84%E3%82%A3%E3%82%A2)
(c) |[ヴェネツィア](https://ja.wikipedia.org/wiki/%E3%83%B4%E3%82%A7%E3%83%8D%E3%83%84%E3%82%A3%E3%82%A2) | 特産品 | ヴェネツィアン・グラス |[ヴェネツィアン・グラス](https://ja.wikipedia.org/wiki/%E3%83%B4%E3%82%A7%E3%83%8D%E3%83%84%E3%82%A3%E3%82%A2%E3%83%B3%E3%83%BB%E3%82%B0%E3%83%A9%E3%82%B9)

*1: リンク先のターゲットページはWikipediaダンプ(2019年1月21日版)のhtmlファイルとして与えられます (Jan 21, 2019). 詳細は **_[data info](data_info.md)_**  ([IT2](#data_info.md#IT2))をご覧ください。

### Primary features 

**_linkjpc_**は5つの主要モジュールから構成され、各モジュールは最大3種類のフィルタリングと組み合わせることができます。

特徴
- 主要モジュールは文字列一致（メンションとタイトル）、埋め込みリンクの探索、統計情報に基づく元記事へのリンク(再帰リンク)の推定とテキストからページへのリンク確率の推定を含みます。
- フィルタリングには属性の値として適切なクラス(属性のrange)判定、被リンク数、被リンクを利用するものがあります。
- 学習は使っていませんが前処理は重いです。

## MODULE CONFIGURATION
### Entity linking
#### core
- **linkjpc.py(ljc)**
#### main modules
- **matching.py(ma)** 
   - メンションとページタイトルの文字列マッチ。タイトル内のメンション、メンション内のタイトルが対象。
- **self_link.py(sl)** (再帰リンクの推定)
   - 再帰リンクの推定 (メンションから元記事へのリンク。典型的には別名などの特別な属性の場合。サンプルデータ正解の統計情報を利用。）
- **get_wlink.py(gw)** 
   - メンションのリンク先を元記事の埋め込みリンクから探す。
- **link_prob.py(lp)** 
   - メンションとページのリンク確率をサンプルデータ正解の統計情報から推定。

#### filtering 
- **attr_range_filtering.py(ar)** (ルールベースのメンションのクラス判定によるフィルタリング)
- **incl_filtering.py(il)** (被リンク数によるフィルタリング)
- **back_link.py(bl)** (被リンクによるフィルタリング)

####others
- **config.py(cf)** (クラス定義等)
- **compile_list.py(cl)** (各主要モジュールのリンク先候補ページを合わせて最終候補リストを作成)
- **get_score.py(gs)** (最終候補リストのスコアリング)
- **ljc_common.py(lc)** (モジュールで共通に使われる情報の辞書作成)

### Preprocessing
- **linkjpc_prep.py** (前処理)

-----------------
## DATA FILES

エンティティリンキング (**_linkjpc_**)、前処理(**_linkjpc_prep_**)の各々で使用されるデータファイルについては _**[data_info](data_info.md)**_ をご覧ください.

## STEPS TO TRY ENTITY LINKING

1) スクリプトデータファイルをダウンロード 
   - エンティティリンキング (**_linkjpc_**)と前処理（ (**_linkjpc_prep_**)オプショナル）に必要なデータファイルのリストは **[WHERE TO GET DATA](data_info.md#WHERETOGETDATA)** (**_[data info](data_info.md)_**)をご覧ください。 
   - 前処理（オプショナル）を試す場合は、以下の**[Notes on Preprocessing](#NOTESONPREPROCESSING)** もご覧ください。

2) ファイルを配置
   - **[WHERE TO PUT DATA](data_info.md#WHERETOPUTDATA)** ( **_[data info](data_info.md)_**)で指定された通りにディレクトリに配置してください。

3) エンティティリンキングを実行
　　- **_tests_** ディレクトリのスクリプト例 ( _linkjpc_test.sh_) を参考にしてください。


## NOTES ON PREPROCESSING

上述のように、前処理済のファイルをダウンロードして前処理をスキップすることもできます。

前処理 (**_linkjpc_prep_**) を実施する場合は、**_tests_**ディレクトリのスクリプト例 ( _linkjpc_prep_all_test.sh_) を参考にしてください。
以下の点に注意してください。

### Output Directory

前処理の出力ファイルは以下のいずれかに出力され、既存のファイルを上書きします。
- (a) common_data_directory
- (b) tmp_data_directory

上記を避けたい場合は、必ず元のファイルを別の場所に保存するか、コマンドラインオプションで (a)(b)として別のディレクトリを指定してください。

### Execution Order

前処理( _**linkjpc_prep**_ )のオプションのうち、A, B, Cのグループに分類したものは、以下に示す順序で実行してください。 **_tests_** ディレクトリのスクリプト例
 ( _linkjpc_prep_all_test.sh_) を参考にしてください。
```

 (A) --gen_redirect -> --gen_incoming_link -> --gen_title2pid_ext -> --gen_back_link, --pre_matching, --gen_self_link_info 
 (B) --gen_sample_gold_tsv --> --gen_link_dist, gen_link_prob, gen_self_link_info
 (C) --gen_common_html -> --gen_link_dist
 (D) --gen_html
```
### Processing Time

前処理は時間がかかりますのでご注意ください。
参考： _test_ ディレクトリのスクリプト例を全て実行する場合、以下の環境での所要時間は約34時間です。

(環境):  
OS: Mac OS 10.15.7  
Memory: 16GB  
CPU: 2.6 GHz 6-Core Intel Core i7  
python: 3.8 

## UNSOLVED ISSUES

- 機械学習 + Hyper parameter tuning　の利用
- 開発データ
  - 現在モジュールで使用している統計情報は小規模なサンプルデータ正解に基づいています。

## テスト
