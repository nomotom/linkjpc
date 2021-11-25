# DATA INFO

TABLE OF CONTENTS:
- [WHERE TO GET DATA](#WHERETOGETDATA)
- [WHERE TO PUT DATA](#WHERETOPUTDATA)
- [DATA DESCRIPTION](#DATADESCRIPTION)

## WHERE TO GET DATA

Where to get data depends on the data creation method as shown below.

Data creation method | Data ID            | Where to get data 
:-------------------------------------|:----------------|:-----------------------------------------
(1) [project SHINRA data distribution](#projectSHINRAdatadistribution) | [[IT1](#IT1)], [[IT2](#IT2)],[[IT3](#IT3)], [[IT4](#IT4)], <br> [[CD1](#CD1)], [[CD2](#CD2)], [[CD3](#CD3)],|project SHINRA site <br>- [SHINRA2021LinkJP](http://shinra-project.info/shinra2021linkjp/) <br> - [SHINRA Data Dowload](http://shinra-project.info/download/) <br><br>(Please access to each page linked in **_[DATA DESCRIPTION](#DATADESCRIPTION)_** below.)
(2) [manually created data](#manuallycreateddata)|[[CM*](#CM1)] | [public data (rule-based systems)](https://drive.google.com/drive/folders/1rNlUanyl1ULEUUKMifIMZgwhzs-84iQT?usp=sharing) |
(3) [Data created by preprocessing tools](#Datacreatedbypreprocessingtools) |[[CP*](#CP1)], [[TP*](#TP1)] | [public data (rule-based systems)](https://drive.google.com/drive/folders/1rNlUanyl1ULEUUKMifIMZgwhzs-84iQT?usp=sharing) |

See **_DATA DESCRIPTION_** for details about files and download pages.  

Please place the downloaded files to the directories specified in **WHERE TO PUT DATA**. As for (2) and (3) above, the data 
files are grouped and stored in three folders on the download site, namely, **tmp_data_dir**, **sample_gold_dir**, and 
**common_data_dir**.

## WHERE TO PUT DATA  
The files required in entity linking (**_linkjpc_**) or preprocessing (**_linkjpc_prep_**) (optional) are listed below.  
Please place the files in the following directories (bold fonts) referring the following instructions.  
  - **in_dir** (for test data (+html))　　
  - **out_dir** (for output data (entity linking))
  - **tmp_data_dir** (for data specifically used for the test data)
  - **sample_gold_dir** (for sample gold data (+html) (used for preprocessing))
  - **common_data_dir** (for other data)  
The directories are specified as command line arguments or options when you try entity linking or preprocessing.

    
### **in_dir** (linkjpc, linkjpc_prep)

  Please create the directories and place the test data ([IT1](#IT1)) (*.json) and html files ([IT2](#IT2)) as follows.  
  - The name of the bottom directory to place test data should be '**ene_annotation**'.
  - Do not place other json files (eg. '*_for_view.json') in the same directory. 
  - Html files should be grouped by categories and be placed in subdirectories under '**html**' respectively.
  
(entity linking, preprocessing)
   ```angular2html
   + ene_annotation  
      + Airport.json　(IT1)
      + City.json (IT1)
      + Company.json (IT1)
      + Compound.json (IT1)
      + Conference.json (IT1)
      + Lake.json (IT1)
      + Person.json (IT1)
``` 

(preprocessing)
```angular2html
  + html            
     + Airport         
        + *.html (IT2)
     + City
        + *.html (IT2)
     + Company
        + *.html (IT2)
     + Compound
        + *.html (IT2)
     + Conference
        + *.html (IT2)
     + Lake
        + *.html (IT2)
     + Person
        + *.html (IT2)
```
### **common_data_dir** (linkjpc, linkjpc_prep)

(entity linking)
>- att_def.tsv ([CM3](#CM3))
>- wl_lines_backward_ca.tsv ([CM4](#CM4)) 
>- wl_lines_forward_ca.tsv ([CM5](#CM5)) 
>- ENEW_ENEtag_20200427_mod.tsv ([CP5](#CP5))
>- jawiki-20190120-title2pageid_ext.tsv ([CP6](#CP6))
>- common_html_tag_info.tsv ([CP7](#CP7))
>- mention_gold_link_dist.tsv ([CP8](#CP8))
>- sample_cat_att_mention_linkcand.tsv ([CP9](#CP9))
>- cat_att_selflink.tsv ([CP10](#CP10))

(preprocessing)
> - jawiki-20190121-cirrussearch-content.json.gz ([CD1](#CD1)) 
> - jawiki-20190120-title2pageid.json ([CD2](#CD2)) 
> - ENEW_ENEtag_20200427.json ([CD3](#CD3)) 
> - jawiki-20190121-cirrussearch-content_wikipat_dis.tsv ([CM1](#CM1)) 
> - ENEW_ENEtag_20200427_stoplist.tsv ([CM2](#CM2)) 
> - jawiki-20190120-pagelinks_dmp.tsv ([CM6](#CM6)) 

### **tmp_data_dir**  (linkjpc, linkjpc_prep)
(entity linking)
>- input_title.txt ([TP1](#TP1))
>- back_link_full.tsv ([TP2](#TP2))
>- mint_partial_match.tsv ([TP3](#TP3))
>- mint_trim_partial_match.tsv ([TP4](#TP4))
>- tinm_partial_match.tsv ([TP5](#TP5))
>- tinm_trim_partial_match.tsv ([TP6](#TP6))
>- html_tag_info.tsv ([TP7](#TP7))

### **sample_gold_dir**  (linkjpc_prep)

  In case of preprocessing, create the following directories (bold fonts) and place the sample gold data (*.json, [IT3](#IT3)) and html files ([IT4](#IT4)).  
  The name of the bottom directory of sample gold data should be '**link_annotation**'.  
  Html files should be placed in subdirectories corresponding their category directory under '**html**', respectively.  

(preprocessing)

```angular2html
  + link_annotation (*1)       
     + Airport.json (IT3)
     + City.json (IT3)
     + Company.json (IT3)
     + Compound.json (IT3)
     + Conference.json (IT3)
     + Lake.json (IT3)
     + Person.json (IT3)
   + html               
     + Airport         
       + *.html (IT4)
     + City
       + *.html (IT4)
     + Company
       + *.html (IT4)
     + Compound
       + *.html (IT4)
     + Conference
       + *.html (IT4)
     + Lake
       + *.html (IT4)
     + Person
       + *.html (IT4)
  ```
  *1: [CP1](#CP1) files (*.tsv) are also created in the same directory in preprocessing.

## DATA DESCRIPTION

### (1) project SHINRA data distribution
### (1-1) test data and html files (in_dir)
####[IT1] (test data)
- filename: Airport.json, City.json, Company.json, Compound.json, Conference.json, Lake.json, Person.json
- description: test data
- available from: [SHINRA2021LinkJP](http://shinra-project.info/shinra2021linkjp/) 公開コード/データ ([評価データ: 入力ファイル、対象のWikipediaページ](https://drive.google.com/file/d/1iEciat50vSaGJ9d9FQz20k8eRt2mMGN7/view?usp=sharing)) 
- used in: (linkjpc) linkjpc, (linkjpc_prep) linkjpc_prep

####[IT2] (original articles of test data (*.html))
- filename: *.html
- description: *.html files of the original articles of test data. The files are grouped by ENE categories (eg. Airport, City, etc.)
- available from: [SHINRA2021LinkJP](http://shinra-project.info/shinra2021linkjp/) 公開コード/データ ([評価データ: 入力ファイル、対象のWikipediaページ](https://drive.google.com/file/d/1iEciat50vSaGJ9d9FQz20k8eRt2mMGN7/view?usp=sharing))
- used in: (linkjpc_prep)gen_html_info_file

### (1-2) sample data and html files (sample_gold_dir)
####[IT3] (sample gold data)
- filename: Airport.json, City.json, Company.json, Compound.json, Conference.json, Lake.json, Person.json
- description: sample gold data
- available from: [SHINRA2021LinkJP](http://shinra-project.info/shinra2021linkjp/) 公開コード/データ ([サンプルデータ](https://drive.google.com/file/d/1b9Xm-Qd1sVfmDr8o4y3t-dVnGai15P-q/view?usp=sharing)) 
- used in: (linkjpc_prep)gen_link_prob_file

####[IT4] (original articles of sample data (*.html))
- filename: ***.html**
- description: *.html files of the original articles of sample data. The files are grouped by ENE categories (eg. Airport, City, etc.)
- available from: [SHINRA2021LinkJP](http://shinra-project.info/shinra2021linkjp/) 公開コード/データ ([サンプルデータ](https://drive.google.com/file/d/1b9Xm-Qd1sVfmDr8o4y3t-dVnGai15P-q/view?usp=sharing)) 
- used in: (linkjpc_prep)gen_html_info_file

### (1-3) other task data (common_data_dir)

####[CD1] **f_cirrus_content_default**:  
 - filename: '**jawiki-20190121-cirrussearch-content.json.gz**'
 - description: Wikipedia Cirrus Dump (content)
 - available from: [SHINRA2021-LinkJP](https://drive.google.com/drive/folders/1emH81ac0e1kYKAF4mvpCslRAgBKCN_Ah?usp=sharing) 公開コード/データ([リンク先のWikipediaデータ](https://drive.google.com/drive/folders/1emH81ac0e1kYKAF4mvpCslRAgBKCN_Ah?usp=sharing) (CirrussearchDump))
 - used in: (linkjpc_prep) gen_disambiuation_file

####[CD2] **f_title2pid_org_default**:  
 - filename: '**jawiki-20190120-title2pageid.json**'
 - description: Title to pageid conversion info list
 - available from: [SHINRA2021-LinkJP](https://drive.google.com/drive/folders/1emH81ac0e1kYKAF4mvpCslRAgBKCN_Ah?usp=sharing) 公開コード/データ([リンク先のWikipediaデータ](https://drive.google.com/drive/folders/1emH81ac0e1kYKAF4mvpCslRAgBKCN_Ah?usp=sharing) (各種処理済データ)
 - sample: 
   - `{"page_id": 302067, "title": "イギリス語", "is_redirect": true,
 "redirect_to": {"page_id": 3377, "title": "英語", "is_redirect": false}}`
   - `{"page_id": 311957, "title": "風と共に去りぬ_(宝塚歌劇)", "is_redirect": false}`
 - used in: (linkjpc_prep) linkedjson2tsv, gen_redirect_info_file

####[CD3] **f_enew_org_default**:  
 - filename: '**ENEW_ENEtag_20210427.json**'
 - available from:  [SHINRA Data Download](http://shinra-project.info/download/?lang=en) (ENE + Wikipedia DATA)  
 - notice: You need an account to get the data. Please create your SHINRA account at [SHINRA: Sign in](http://shinra-project.info/signin) page.
 - distributed by: project SHINRA
 - used in: (linkjpc_prep) gen_enew_info_file

### (2) manually created data (common_data_dir)

Download the data listed below from _URL(to be prepared)_ .  
(Or you might create them by yourself :)

####[CM1] f_disambiguation_pat_default:  
 - filename: '**jawiki-20190121-cirrussearch-content_wikipat_dis.tsv**'
 - created by: manually
 - used in: (linkjpc_prep) gen_disambiuation_file

####[CM2] f_enew_mod_list_default:
 - filename: '**ENEW_ENEtag_20200427_stoplist.tsv**'
 - format: ENEID, pid, title (*.tsv)
 - sample: 
   - `1.5.1.3 1419479 フランス陸軍参謀総長`
 - created by: manually
 - used in: (linkjpc_prep) gen_enew_info_file

####[CM3] f_attr_rng_default:
 - filename: '**att_def.tsv**'
 - format: ene_label_en, attribute_name, range, probability (*.tsv)
   - (range):    'ene':eneid
 - sample:
   - `Person  国籍  ene:1.5.1.3   1.0`
   - `Person 国籍　ene:1.5.1.0   0.5`
 - created by: manually
 - used in: (linkjpc)get_attr_range

####[CM4] f_wl_lines_backward_ca_default
 - filename: '**wl_lines_backward_ca.tsv**'
 - notice: 
   - The default file contains just one example and should be modified. 
 - format:
   - ene_label_en, attribute_name, distance (*.tsv)
 - sample:
   - `Person  作品    -3`
 - used in: (linkjpc) gw.reg_mention_gold_distance_ca

####[CM5] f_wl_lines_forward_ca_default
 - filename: '**wl_lines_forward_ca.tsv**'
 - notice: 
   - The default file contains just one example and should be modified.  
 - format:
   - ene_label_en, attribute_name, distance (*.tsv)
 - sample:
   - `Person  作品    1`
 - used in: (linkjpc) gw.reg_mention_gold_distance_ca

####[CM6] f_back_link_dump_default 
 - filename: '**jawiki-20190120-pagelinks_dmp.tsv**'
 - format: back link pid, org_title (*.tsv)
 notice: based on jawiki-20190120-pagelinks.sql
 - based on: jawiki-20190120-pagelinks.sql
   - The original sql file is available from: project SHINRA data distribution, [SHINRA2021-LinkJP](http://shinra-project.info/shinra2021linkjp/) (リンク先のWikipediaデータ(WikiDump)))
 - created by: 
 ```mysql -u root -D pagelink < jawiki-20190120-pagelinks.sql```
 - used in: (linkjpc_prep) gen_back_link_info_file

### (3) data created by preprocessing tools
### (3-1) (common_data_dir)

####[CP1] (sample gold data info)
 - filename: **Airport.tsv, City.tsv, Company.tsv, Compound.tsv, Conference.tsv, Lake.tsv, Person.tsv** 
 - description: sample gold data info
 - format: org_pageid, org_title, attribute_name, mention, start_line_id, start_offset, end_line_id, end_offset, gold_pageid, gold_title (*.tsv)
 - sample: 573393  森見登美彦      生誕地  日本・奈良県生駒市      35      33      35      42      22003   生駒市
 - created by: (linkjpc_prep --gen_sample_gold_tsv) linkedjson2tsv
 - used in: (linkjpc_prep) gen_link_prob_file, gen_mention_gold_link_dist

####[CP2] f_disambiguation_default
 - filename: '**jawiki-20190121-cirrussearch-content_disambiguation.tsv**'
 - sample: 
   - `1128763 テトラ (曖昧さ回避)`
   - `3077413	ハムレット (曖昧さ回避)`
 - created by: (linkjpc_prep --redirect) gen_disambiguation_file
 - used in: (linkjpc_prep) gen_redirect_info_file

####[CP3] f_redirect_info_default 
 - filename: '**jawiki-20190120-title2pageid_nodis.tsv**'
 - format: title, pageid (*.tsv)
 - sample: 
   - `1904年アメリカ合衆国大統領選挙  1477879`
   - `風と共に去りぬ (宝塚歌劇)311957`
 - notice:
   - based on original redirect file(f_title2pid_org_default, jawiki-202190120-title2pageid.json).
   - recovered white spaces in Wikipedia titles which are replaced by '_' in the original redirect file.
   - Info on ill formatted pages or disambiguation pages are excluded though not completely.
 - created by: (linkjpc_prep --redirect) gen_redirect_info_file
 - used in: (linkjpc_prep) gen_title2pid_ext_file

####[CP4] f_incoming_default 
 - filename: 'jawiki-20190121-cirrussearch-content_incoming_link.tsv'
 - sample: 
   - `311957	風と共に去りぬ (宝塚歌劇)	1091`
   - `345792  ピノッキオの冒険        233`
 - created by: (linkjpc_prep --gen_incoming_link) gen_incoming_link_file
 - used in: (linkjpc_prep) gen_title2pid_ext_file

####[CP5] f_enew_info_default 
 - filename: '**ENEW_ENEtag_20200427_mod.tsv**'
 - description:
   - ENEW info (based on slightly modified version of ENEW (20200427)).
   - modification list: ENEW_ENEtag_20200427_stoplist.tsv (f_enew_mod_list_default)
 - format:
   - pageid, ENEid, title (*.tsv) 
 - sample: 
   - `311957	1.7.19.4	風と共に去りぬ (宝塚歌劇)`
   - `345792  1.7.19.6        ピノッキオの冒険`
 - notice: 
    - Not all target pageids are included in the file. (eg. 3682608, 3386984)
 - created by: (linkjpc_prep --gen_title2pid) gen_enew_info_file
 - used in: (linkjpc_prep) gen_title2pid_ext_file

####[CP6] f_title2pid_ext_default 
 - filename: '**jawiki-20190120-title2pageid_ext.tsv**'
 - description: Summary information on title to pageid conversion, incoming links, and ENE classification of articles. .
 - format: 
   - from_title, to_pid, to_title, to_incoming, to_eneid (*.tsv)
 - sample: 
   - `ロミジュリ	28783	ロミオとジュリエット	671	1.7.19.4`
   - `ロミオとジュリエット (2010年の宝塚歌劇)	3520389	ロミオとジュリエット (2010年の
 宝塚歌劇)	173	1.7.19.4`
 - created by: gen_title2pid_ext_file
 - used in: (linkjpc_prep --gen_title2pid) gen_back_link_info_file (get_to_pid_to_title_incoming_eneid), 
    prematching_mention_title (reg_pid2title), 
    gen_self_link_info (get_category)
   (linkjpc) ljc_main, lc.reg_title2pid_ext

####[CP7] f_common_html_info_default (--gen_common_html)
 - filename: '**common_html_tag_info.tsv**'
 - format: 
   - cat, pid, line_id, text_start, text_end, text, title (*.tsv)
 - sample: 
   - `City    1617736 90      292     298     リンブルフ州 リンブルフ州 (ベルギー)`
 - created by: gen_html_info_file
 - used in: (linkjpc_prep) gen_mention_gold_link_dist

####[CP8] f_mention_gold_link_dist_default 
 - filename: '**mention_gold_link_dist.tsv**'
 - description: Mention goldlink dist file, which shows the distance (number of lines) between mentions and (nearest) gold links in sample html files.
 - format: ene_label_en, attribute_name, distance (.tsv)
 - sample: 
   - `Person 作品 -1`
   - `Person 作品 29`
 - notice: the values are based on sample data
 - created by: (linkjpc_prep --gen_link_dist) gen_mention_gold_link_dist
 - used in: (linkjpc_prep --gen_link_dist) gen_mention_gold_link_dist_info
 
[CP9] f_link_prob_default 
 - filename: '**sample_cat_att_mention_linkcand.tsv**'
 - description: Link probability info file. 
 - format: 
   - ene_label_en, attribute_name, mention, link_cand_pageid:prob:freq;...(.tsv)
 - sample: 
   - `City	合併市区町村	上村	151917:0.25:1;37423:0.25:1;381057:0.25:1;1872659:0.25:1`
 - notice:
   - The ratio is based on LinkJP2021 sample data ver.20210428.
 - created by: (linkjpc_prep --gen_link_prob) gen_link_prob_file 
 - used in: (linkjpc) lp.get_link_prob_info

####[CP10] f_slink_default 
 - filename: '**cat_att_selflink.tsv**'
 - description: Self link info file
 - format: ene_label_en, attribute_name, ratio (*.tsv)
 - sample:
   - `Person  家族    0.0`
   - `Person  別名    1.0`
 - notice: 
   - The ratio is based on sample data (ver.20210428).
 - created by: (linkjpc_prep --gen_slink) gen_self_link_info
 - used in: (linkjpc) sl.check_slink_info


 
### (3-2) (tmp_data_dir)

####[TP1] f_input_title_default
 - filename: '**input_title.txt**'
 - description: title list of test data
 - created by: (linkjpc_prep --gen_back_link) extract_input_title
 - used in: (linkjpc_prep) gen_back_link_info_file
 
####[TP2] f_back_link_default 
 - filename: '**back_link_full.tsv**'
 - description: back link info file, which shows the title pages of test data and the back links to the pages
 - format: org_title, back link pid, back link title (*.tsv)
 - sample: 
   - `1975年度新人選手選択会議 (日本プロ野球)	143952	中畑清`
 - notice: 
   - based on jawiki-20190120-pagelinks.sql
 - created by: (linkjpc_prep --gen_back_link) gen_back_link_info_file
 - used in: (linkjpc) bl.check_back_link_info

####[TP3] f_mint_partial_default 
 - filename: '**mint_partial_match.tsv**'
 - description: mention-title matching ratio list (mention in title, full title)
 - format: mention, pid, title, ratio (*.tsv)
 - sample:
   - `風と共に去りぬ	457696	風と共に去りぬ	1.0`
   - `風と共に去りぬ	671718	風と共に去りぬ (映画)	0.58`
   - `風と共に去りぬ	311957	風と共に去りぬ (宝塚歌劇)	0.5`
 - created by: (linkjpc_pre --pre_matching) prematch_mention_title
 - used in: (linkjpc) ljc_main, mc.reg_matching_info

####[TP4] f_mint_trim_partial_default 
 - filename: '**mint_trim_partial_match.tsv**'
 - description: mention-title matching ratio list (mention in title, trimmed title)
 - notice:
   - Disambiguation descriptions enclosed in braces in titles are not used for matching.
 - format: See f_mint_partial_default
 - sample:
   - `風と共に去りぬ	311957	風と共に去りぬ (宝塚歌劇)	1.0`
   - `風と共に去りぬ	671718	風と共に去りぬ (映画)	1.0`
   - `風と共に去りぬ	457696	風と共に去りぬ	1.0`
 - created by: (linkjpc_pre --pre_matching) prematch_mention_title
 - used in: (linkjpc) ljc_main, mc.reg_matching_info
 
####[TP5] f_tinm_partial_default 
 - filename: '**tinm_partial_match.tsv**'
 - description: mention-title matching ratio list (title in mention, full title)
 - format: mention, pid, title, ratio (*.tsv)
 - sample:
   - `風と共に去りぬ	457696	風と共に去りぬ	1.0`
   - `風と共に去りぬ	895511	風と共に	0.57`
 - created by: (linkjpc_pre --pre_matching) prematch_mention_title
 - used in: (linkjpc) ljc_main, mc.reg_matching_info
 
####[TP6] f_tinm_trim_partial_default 
 - filename: '**tinm_trim_partial_match.tsv**'
 - description: mention-title matching ratio list (title in mention, tinm title)
 - notice:
   - Disambiguation descriptions enclosed in braces in titles are not used for matching
 - format: 
   - mention, pid, title, ratio (.tsv)
 - sample:
   - `風と共に去りぬ	311957	風と共に去りぬ (宝塚歌劇)	1.0`
   - `風と共に去りぬ	671718	風と共に去りぬ (映画)	1.0`
   - `風と共に去りぬ	457696	風と共に去りぬ	1.0`
   - `風と共に去りぬ	895511	風と共に	0.57`
   - `風と共に去りぬ	3624861	風と共に (曲)	0.57`
 - created by: (linkjpc_pre --pre_matching) prematch_mention_title
 - used in: (linkjpc) ljc_main, mc.reg_matching_info

####[TP7] f_html_info_default  
 - filename: '**html_tag_info.tsv**'
 - description: Info on links to other Wikipedia pages in original articles
 - format: 
   - cat, pid, line_id, text_start, text_end, text, title (.tsv)
 - sample: 
   - `City    1617736 90      292     298     リンブルフ州    リンブルフ州 (ベルギー)`
 - created by: (linkjpc_prep --gen_html) gen_html_info_file
 - used by: (linkjpc) gw.reg_tag_info
 
## (3) data created by entity linking
### (3-1) (out_dir)

####[OL1] (output data)
 - filename: **Airport.json, City.json, Company.json, Compound.json, Conference.json, Lake.json, Person.json**
 - description: output data 
 - format: [SHINRA2021-LinkJP data format](http://shinra-project.info/shinra2021linkjp/#data-format)

### (3-2) (common_data_dir)

####[CL1] f_mention_gold_link_dist_info_default 
 - filename: '**mention_gold_link_dist_info.tsv**'
 - description: summary of gold links of mentions by category * attribute
 - format: 
   - cat, attr, backward_limit, forward_limit, diff_backward_num, diff_forward_num, diff_same_num, all_num (tsv)
 - sample:
   - Person  地位職業        -47     7       18      90      -63     45
   - Person  生誕地  -57     6       9       21      15      45
 notice: the values are based on - sample data
 - created by: (linkjpc) gw.reg_mention_gold_distance
 - used in: (linkjpc) gw.reg_mention_gold_distance



