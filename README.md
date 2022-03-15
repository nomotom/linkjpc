# linkjpc

TABLE OF CONTENTS:
- [INTRODUCTION](#introduction)
  - [TASK](#task)
  - [PRIMARY FEATURES](#primary-features) 
- [MODULE](#modules)
- [TRY ENTITY LINKING](#try-entity-linking)
- [NOTES ON PREPROCESSING](#notes-on-preprocessing)
- [UNSOLVED ISSUES](#unsolved-issues)
- [FURTHER READINGS](#further-readings)
  - [DATA FILES](#data-files)
  - [COMMANDLINE OPTIONS](#commandline-options)

## INTRODUCTION

**_linkjpc_** is a python script created for a Japanese Wikipedia entity linking task called [SHINRA2021-LinkJP](http://shinra-project.info/shinra2021linkjp/) (task1).

### Task

The task is to link given mentions (eg. _イタリア(Italy)_) in Wikipedia articles to their corresponding Wikipedia pages (eg. [イタリア(Italy)](https://ja.wikipedia.org/wiki/%E3%82%A4%E3%82%BF%E3%83%AA%E3%82%A2)) to which they refer, and can be regarded as a kind of Wikification. 

In this task, mentions are marked as values of _attributes_ (eg. country, alias, local speciality) of the topical _entities_ (eg. Venice) of the Wikipedia articles on which they appear. 

In many cases, mentions refer to other pages as shown in examples (a) and (c) below.

In case of special attributes such as aliases, they may refer to the pages on which they appear and are linked to the original pages (self-link) as shown in example (b) below.

example |original page (entity) | attribute name|mention / attribute value | pages to be linked(*1)
:----------------|:------|:---------------|:---------|:----
(a) |[ヴェネツィア(Venice)](https://ja.wikipedia.org/wiki/?curid=30053) | 国(country) | イタリア(Italy) |[イタリア(Italy)](https://ja.wikipedia.org/wiki/%E3%82%A4%E3%82%BF%E3%83%AA%E3%82%A2) 
(b) |[ヴェネツィア(Venice)](https://ja.wikipedia.org/wiki/%E3%83%B4%E3%82%A7%E3%83%8D%E3%83%84%E3%82%A3%E3%82%A2) | 別名(alias) | アドリア海の女王(Queen of the Adriatic) |[ヴェネツィア(Venice)](https://ja.wikipedia.org/wiki/%E3%83%B4%E3%82%A7%E3%83%8D%E3%83%84%E3%82%A3%E3%82%A2)
(c) |[ヴェネツィア(Venice)](https://ja.wikipedia.org/wiki/%E3%83%B4%E3%82%A7%E3%83%8D%E3%83%84%E3%82%A3%E3%82%A2) | 特産品(local speciality) | ヴェネツィアン・グラス(Venetian glass) |[ヴェネツィアン・グラス(Venetian glass)](https://ja.wikipedia.org/wiki/%E3%83%B4%E3%82%A7%E3%83%8D%E3%83%84%E3%82%A3%E3%82%A2%E3%83%B3%E3%83%BB%E3%82%B0%E3%83%A9%E3%82%B9)

*1: The target pages are given as html files based on Wikipedia dump (Jan 21, 2019). See **_[data info](https://github.com/nomotom/linkjpc/blob/master/docs/data_info.md)_**  for details.

### Primary features 

**_linkjpc_** has the following key features. 

- Allows combination of main modules to utilize string matching (between mentions and page titles), finding embedded links to the referred page, self-link estimation, link probability estimation based on statistics.
- Each module can be combined with up to four types of filtering modules (called 'filtering' hereafter), which use attribute range (rule-based class estimation of candidate link pages), number of incoming links,
and/or backlinks, and nil detection.
- Heavy preprocessing.

## MODULES
### Entity linking
#### core
- **linkjpc.py(ljc)**
#### main modules
- **matching.py(ma)** (string matching between mentions and page titles)
   - There are roughly two types of matching: mention in title (mint) and title in mention (tinm). 
- **self_link.py(sl)** (self-link estimation)
   - Estimate the probability of self-link (linking mentions to the original pages on which they appear; typically in case of special attributes such as aliases) based on the statistics of sample gold data.
- **get_wlink.py(gw)** (finding embedded links to the referred Wikipedia page)
   - Find embedded links in original pages as candidates of the links to the Wikipedia pages to which mentions refer.
- **link_prob.py(lp)** (link probability estimation)
   - Estimate the probability of linking mention-page pairs based on statistics of sample gold data.

#### filtering 
- **attr_range_filtering.py(ar)** (filtering by rule-based class estimation of mentions (attribute values))
- **incl_filtering.py(il)** (filtering by number of incoming links)
- **back_link.py(bl)** (filtering by backlinks)
- **detect_nil.py(dn)** (filtering by nil (unlikable) detection)

#### others
- **config.py(cf)** (definition of classes, etc.)
- **compile_list.py(cl)** (compiling candidate link pages from main modules to build final candidate list)
- **get_score.py(gs)** (scoring of final candidate link pages)
- **ljc_common.py(lc)** (create dictionary to store information commonly used)

### Preprocessing
- **linkjpc_prep.py**

-----------------

## TRY ENTITY LINKING

The following procedure explains the steps of entity linking. 

1) Download the scripts and data files. 
   - The data files required for entity linking and preprocessing (optional) are listed in **[WHERE TO GET DATA](https://github.com/nomotom/linkjpc/blob/master/docs/data_info.md#where-to-get-data)** in **_[data info](https://github.com/nomotom/linkjpc/blob/master/docs/data_info.md#data-description)_**.  
   - (optional) If you would like to try preprocessing (**_linkjpc_prep_**) by yourself, please refer to **[Notes on Preprocessing](#notes-on-preprocessing)** below as well.

2) Place the files in the directories as specified in **[WHERE TO PUT DATA](https://github.com/nomotom/linkjpc/blob/master/docs/data_info.md#where-to-put-data)** in **_[data info](https://github.com/nomotom/linkjpc/blob/master/docs/data_info.md)_**.  

3) Try entity linking (**_linkjpc_**). 

```
[example] linking mentions to Wikipedia pages with the same name (exact match)
$ python ./linkjpc/linkjpc.py (common_data_dir) (tmp_data_dir) (in_dir) (out_dir) --mod m --mint e

```
  For further examples, please refer to sample scripts (eg. _linkjpc_test.sh_) in  **_tests_** folder.

## NOTES ON PREPROCESSING

As mentioned above, you can download the preprocessed files and skip preprocessing.

If you would like to run preprocessing (**_linkjpc_prep_**) and create the files by yourself, see sample scripts (eg. _linkjpc_prep_all_test.sh_) in _tests_ directory.
Please keep the following points in mind.  

### Output Directory

By default, the output files of preprocessing will be output to either of the following directories, overwriting existing files.
- (a) common_data_directory
- (b) tmp_data_directory
- (c) sample_gold_direcory

To avoid that, please save the existing files to different directories beforehand or specify other directories as (a)(b) using entity linking (**_linkjpc_**) options.

### Execution Order

Some _**linkjpc_prep**_ options (grouped in A, B, C below) should be executed in fixed order. Please see sample 
scripts (eg. _linkjpc_prep_all_test.sh_) in **_tests_** directory.
```

 (A) --gen_redirect -> --gen_incoming_link -> --gen_title2pid_ext -> --gen_back_link, --pre_matching, --gen_self_link_info 
 (B) --gen_sample_gold_tsv --> --gen_link_dist, gen_link_prob, gen_self_link_info
 (C) --gen_common_html -> --gen_link_dist
 (D) --gen_html, gen_linkable
```
### Processing Time

The preprocessing process can be time-consuming.  
For your reference, the entire preprocessing time (except --gen_linkable) using the sample script in _test_ folder is about 34 hours in the following environment.

(Environment):  
OS: Mac OS 10.15.7  
Memory: 16GB  
CPU: 2.6 GHz 6-Core Intel Core i7  
python: 3.8 

## UNSOLVED ISSUES

- Hyper parameter tuning
- Development data
  - Currently, the statistics used by some modules are based on the small sample data.

## FURTHER READINGS
### DATA FILES
  - As for the data files used for entity linking (**_linkjpc_**) and/or preprocessing (**_linkjpc_prep_**), see _**[data_info](https://github.com/nomotom/linkjpc/blob/master/docs/data_info.md#data-description)**_.

### COMMANDLINE OPTIONS
  - entity linking (_linkjpc_):  [linkjpc_commands](https://github.com/nomotom/linkjpc/blob/master/docs/linkjpc_commands)
  - preprocessing (_linkjpc_prep_):  [linkjpc_prep_commands](https://github.com/nomotom/linkjpc/blob/master/docs/linkjpc_prep_commands)
 