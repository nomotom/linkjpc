## LINKJPC_PRE_COMMANDS

TABLE OF CONTENTS

- [ARGUMENTS](#arguments)
- [OPTIONS](#options)

### ARGUMENTS

argument |description | type |  note
:----------------|:------|:---------------|:---------
_common_data_dir_|common data directory |path|
_tmp_data_dir_|temporary data directory|path|     
_in_dir_|input directory|path|   
_sample_gold_dir_|sample gold directory. <br>The name of the bottom directory should be '_**link_annotation**_'. |path|The folder to store html files of sample data should be created under the directory.|

### OPTIONS

option|description| type | value|  default | note
:-------------------|:-----------------|:---------|:---------|:---------|:---------------
--_char_match_min_|minimum of title-mention matching ratio. |float|(0.1-1.0) |_0.1_<br>(cf.OptInfo.char_match_min_default)|
--_f_back_link_| filename of back link info, which shows the title pages of test data and the back links to the pages.  |string| |_back_link_full.tsv_<br>(cf.DataInfo.f_back_link_default)|
--_f_back_link_dump_| filename of back link dump file.  |string| |_jawiki-20190120-pagelinks_dmp.tsv_<br> (cf.DataInfo.f_back_link_dump_default)|
--_f_cirrus_content_| filename of Wikipedia cirrus dump (content). |string| |_jawiki-20190121-cirrussearch-content.json.gz_<br>(cf.DataInfo.f_cirrus_content_default)|
--_f_common_html_info_| filename of common_html_info_file, which lists embedded Wikipedia link info of sample html files. |string| |_common_html_tag_info.tsv_<br>(cf.DataInfo.f_common_html_info_default)|
--_f_disambiguation_| filename of disambiguation page list.|string| |_jawiki-20190121-cirrussearch-content_disambiguation.tsv_<br> (cf.DataInfo.f_disambiguation_default)|
--_f_disambiguation_pat_| filename of disambiguation page judgment rules |string| |_jawiki-20190121-cirrussearch-content_wikipat_dis.tsv_<pat> (cf.DataInfo.f_disambiguation_pat_default)|
--_f_enew_info_| filename of ENEW info , a modification of original ENEW. |string| |_ENEW_ENEtag_20200427_mod.tsv_<br> (cf.DataInfo.f_enew_info_default)|
--_f_enew_mod_list_| filename of ENEW modification list. |string| |_ENEW_ENEtag_20200427_stoplist.tsv_<br> (cf.DataInfo.f_enew_mod_list_default)|
--_f_enew_org_| filename of original ENEW info (ENE Classification of Japanese Wikipedia pages). |string| |_ENEW_ENEtag_20210427.json_<br> (cf.DataInfo.f_enew_org_default)|
--_f_html_info_| filename of html info file, which lists embedded Wikipedia link info of target html files. |string| |_html_tag_info.tsv_<br>(cf.DataInfo.f_html_info_default)|
--_f_incoming_| filename of incoming link info. |string| |_html_tag_info.tsv_<br> (cf.DataInfo.f_incoming_default)|
--_f_input_title_| filename of title list of test data. |string| | _input_title.txt_<br>(cf.DataInfo.f_input_title_default)|
--_f_link_prob_| filename of link probability info. |string| |_sample_cat_att_mention_linkcand.tsv_<br> (cf.DataInfo.f_link_prob_default)|
--_f_mention_gold_link_dist_| filename of mention goldlink dist file, which shows the distance (number of lines) between mentions and (nearest) gold links in sample html files. |string| | _mention_gold_link_dist.tsv_<br>(cf.DataInfo.f_mention_gold_link_dist_default)|
--_f_mint_partial_| filename of mention-title matching ratio list (mention in title, full title) |string| |_mint_partial_match.tsv_<br>(cf.DataInfo.f_mint_partial_default)|
--_f_mint_trim_partial_|filename of mention-title matching ratio list (mention in title, trimmed title) matching ratio list |string| |_mint_trim_partial_match.tsv_<br>(cf.DataInfo.f_mint_trim_partial_default)|
--_f_tinm_partial_| filename of mention-title matching ratio list (title in mention, full title) matching ratio list |string| |_tinm_partial_match.tsv_<br> (cf.DataInfo.f_tinm_partial_default)|
--_f_tinm_trim_partial_| filename of mention-title matching ratio list (title in mention, trimmed title) |string| |_tinm_trim_partial_match.tsv_<br>(cf.DataInfo.f_tinm_trim_partial_default)|
--_f_redirect_info_| filename of redirect info file, a modification of original from_title to_pageid information file to exclude disambiguation pages and ill-formatted pages.  |string| |_jawiki-20190120-title2pageid_nodis.tsv_<br>(cf.DataInfo.f_redirect_info_default)|
--_f_slink_| filename of self link info. |string| | _cat_att_selflink.tsv_<br>(cf.DataInfo.f_slink_default)|
--_f_title2pid_ext_| filename of summary information on title to pageid conversion, incoming links, and ENE classification of articles. |string| |_jawiki-20190120-title2pageid_ext.tsv_<br>(cf.DataInfo.f_title2pid_ext_default)|
--_f_title2pid_org_| filename of original from_title to_pageid information. |string| |_jawiki-20190120-title2pageid.json_<br>(cf.DataInfo.f_title2pid_org_default)|
--_gen_back_link_|create back link info file, which shows the title pages of test data and the back links to the pages. | | True/False|False|
--_gen_common_html_|create common html info file from sample data (*.html files).| | True/False|False|
--_gen_html_|create html info file from target data (*.html files).| | True/False|False|
--_gen_incoming_link_|get num of incoming links from cirrus dump and create incoming_link_file. | | True/False|False|
--_gen_link_dist_|create mention_gold_link_dist file, which shows the distance (number of lines) between mentions and (nearest) gold links in sample html files. | | True/False|False|
--_gen_link_prob_|create link probability info file.| | True/False|False|
--_gen_slink_|create self link info file. | | True/False|False|
--_gen_title2pid_|create enew_info_file and title2pid_ext file. | |True/False|False|
--_gen_sample_gold_tsv_|create sample gold tsv file. | | True/False|False|
--_pre_matching_|specity type of pre-matching. <br><br>_mint_ (mention in title)<br>_tinm_ (title in mention)<br>_n_ (N/A)| choice|[_mint_, _tinm_, _n_]|'_n_'<br>(cf.OptInfo.pre_matching_default)|
--_gen_redirect_|create disambiguation file and redirect info file| |True/False |False |
--_title_matching_mint_, <br>-_tmm_|whether to use trimmed titles (= omit parenthetical disambiguation from page titles) in mention-title matching (mention in title) or not. If set to '_trim_', the matching ratio is calculated based on trimmed titles.<br><br>_trim_<br>_full_| choice|[trim, full]|'_full_'<br>(cf.OptInfo.title_matching_mint_default) |
--_title_matching_tinm_, <br>-_tmt_|whether to use trimmed titles (= omit parenthetical disambiguation from page titles) in mention-title matching (title in mention ) or not. If set to '_trim_', the matching ratio is calculated based on trimmed titles.<br><br>_trim_<br>_full_ | choice|[trim, full]|'_full_'<br>(cf.OptInfo.title_matching_tinm_default) |
