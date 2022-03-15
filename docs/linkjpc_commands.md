## LINKJPC_COMMANDS

TABLE OF CONTENTS:
- [ARGUMENTS](#arguments)
- [OPTIONS](#options)
  - [OPTIONS FOR MAIN MODULES](#options-for-main-modules)
  - [OPTIONS FOR FILTERING](#options-for-filtering) 

### ARGUMENTS

argument |description | type |  note
:----------------|:------|:---------------|:---------
_common_data_dir_|common data directory |Path| exists=True
_tmp_data_dir_|temporary data directory|Path|   exists=True  
_in_dir_|input directory|Path| exists=True  
_out_dir_|output directory|Path| dir_okay=True|

### OPTIONS
#### OPTIONS FOR MAIN MODULES
#### common 
option|description| type | value|  default | note
:-------------------|:-----------------|:---------|:---------|:---------|:---------------
_--**mod**_| a comma-separated priority list of module groups (denoted by the combination of five characters) to be used.<br>eg. `'m:sw:t'` (first priority group: _m_, second priority group:_sw_, third priority group:_t_)| string | a comma separated list of the combination of [_m_, _t_, _w_, _s_, _l_] | |always required<br>
_--**filtering**_,<br>_-**f**_|types of filtering used in any module.<br><br> _a_: attribute range filtering, <br> _b_: backlink, <br>_i_: filtering by incoming link num, <br>_n_: N/A. Specified as the combination of _a_, _b_, _i_. |choice|[ _a_, _b_, _i_, _ab_, _ai_, _bi_, _abi_, _n_]|'n'<br>(cf.OptInfo.filtering_default)|required when filtering is used <br>eg. `abi`
_--mod_w_|module group weight list (float list separated by colon). <br><br>(format): (mod_group_first_weight):(mod_group_second_weight):(mod_group_third_weight):(mod_group_fourth_weight):(mod_group_fifth_weight)|string| |`'1.0:0.1:0.01:0.001:0.0001'` <br>(cf.OptInfo.mod_w_default) | 
_--ans_max_,<br>_-a_max_|maximum number of output answers for one mention.|int| |1<br>(cf.OptInfo.ans_max_default)|
_--score_type_|scoring type. <br><br> _id_: use numerical sort result of candidate pageids if their scores are the same,<br> _n_: N/A.|choice|[_id_, _n_]|'id'<br>(cf.OptInfo.score_type_default)|
_--f_title2pid_ext_|filename of title2pageid extended information file, in which most of the disambiguation, management or format-error pages are deleted and ENEIDs and incoming link num info are added.|string| |(cf.OptInfo.f_title2pid_ext_default)|

#### main modules (ma: matching)
option|description| type | value|  default | note
:---------------------------------------|:-----------------|:---------|:---------|:---------|:---------------
_--**mint**_|mention in title: how to match mentions to titles of candidate pages:<br><br>_e_: exact match, <br> _p_: partial match, <br> _n_: N/A|choice|[_e_, _p_, _n_]|'n'<br>(cf.OptInfo.mint_default)|required when mint is used
_--**tinm**_|title in mention: how to match titles of candidate pages to mentions,<br><br>_e_: exact match, <br>_p_: partial match, <br>_n_: N/A|choice|[_e_, _p_, _n_]|'n'<br>(cf.OptInfo.tinm_default)|required when tinm is used
_--char_match_cand_num_max,<br>-c_max_|maximum number of candidate link pages for one mention in each string matching module (mint/tinm)|int| |1000<br>(cf.OptInfo.char_match_cand_num_max_default)|
_--f_mint_|filename of partial match info file (mention in title)|string| |_mint_partial_match.tsv_<br>(cf.OptInfo.f_mint_partial_default)| 
_--f_mint_trim_|filename of partial match info file (mention in title)|string| |_mint_trim_partial_match.tsv_<br>(cf.OptInfo.f_mint_trim_partial_default)| 
_--f_tinm_|filename of partial match info file (title in mention)|string| |_tinm_partial_match.tsv_<br>(cf.OptInfo.f_tinm_partial_default)| 
_--f_tinm_trim_|filename of partial match info file (title trimmed in mention)|string| |_tinm_trim_partial_match.tsv_<br>(cf.OptInfo.f_tinm_trim_partial_default)| 
_--mint_min_,<br>_-m_min_|minimum length ratio of mentions in titles of candidate Wikipedia pages to be linked.|float|(0.1-1.0) |0.2<br>(cf.OptInfo.mint_min_default)| 
_--tinm_min_,<br>_-t_min_|minimum length ratio of titles of candidate Wikipedia pages in mentions.|float|(0.1-1.0)|0.5<br>(cf.OptInfo.tinm_min_default)| 
_--title_matching_mint_,<br>_-tmm_|title matching in mint (mention in title)|choice|[_trim_,<br>_full_]|'full'<br>(cf.OptInfo.title_matching_mint_default)|
_--title_matching_tinm_,<br>_-tmt_|title matching in tinm (title in mention)|choice|[_trim_, _full_]|'full'<br>(cf.OptInfo.title_matching_tinm_default)| 
              
#### main module: (gw: get_wlink)
option|description| type | value|  default | note
:----------------------------------------|:--------------------|:---------|:---------|:------------|:---------------
_--**wlink**_,<br>_-**wl**_|scoring of the wikipedia links in the mentions. combination of the following: <br><br>_f_: add higher score to the first link in the mention than others, <br>_r_: add higher score to the rightmost link in the mention than others, _m_: give equal score to all the links in the mention, <br>_p_: give score to the links of the previous same mentions in the page, <br>_l_: give score to the links around the mention in the lines of page specified with wl_lines_backward_max and wl_lines_forward_max, <br>_n_: N/A. Notice that _m_ cannot be used with _f_ or _r_.|string| |'_n_'(cf.OptInfo.wlink_default)|required when get_wlink is used.
_--f_html_info_|filename of html tag info file.|string| |_html_tag_info.tsv_<br>(cf.OptInfo.f_html_info_default)| 
_--f_wl_lines_backward_ca_,<br>_-f_wl_bca_|the files to specify maximum number of line to backward-search Wikipedia links in the page for each category-attribute pairs. Notice: The default file can be empty.|string| |_wl_lines_backward_ca.tsv_<br>(cf.OptInfo.f_wl_lines_backward_ca_default)| 
_--f_wl_lines_forward_ca_,<br>_-f_wl_fca_|the files to specify maximum number of line to forward-search Wikipedia links in the page for each category-attribute pairs. Notice: The default file can be empty.|string| |_wl_lines_forward_ca.tsv_<br>(cf.OptInfo.f_wl_lines_forward_ca_default)| 
_--wl_break/--no-wl_break_|flag to stop searching candidate wikilinks at the line in which nearest candidate link is found.|boolean | |True<br>(cf.OptInfo.wl_break_default)|
_--wl_lines_backward_max_,<br>_-wl_bmax_|maximum number of lines to backward-search wikipedia links in the page|int| |1<br>(cf.OptInfo.wl_lines_backward_max_default)|
_--wl_lines_forward_max_,<br>_-wl_fmax_|maximum number of lines to forward-search wikipedia links in the page|int| |1<br>(cf.OptInfo.wl_lines_forward_max_default)|
_--wl_lines_backward_ca_,<br>_-wl_bca_| how to specify the maximum number to backward-search Wikipedia links for each category-attribute. <br><br>_f_: the number specified in f_wl_lines_backward_max_ca, <br>_r_: the number estimated using the ratio specified by wl_lines_backward_ca_ratio, <br>_fr_: both f and r (_f_ takes precedence), <br>_n_: N/A|choice|[_f_, _r_, _fr_,  _n_]|'r'<br>(cf.OptInfo.wl_lines_backward_ca_default)| 
_--wl_lines_forward_ca_,<br>_-wl_fca_|how to specify the maximun number to forward-search Wikipedia links for each category-attribute. <br><br>_f_: the number specified in f_wl_lines_forward_max_ca, <br>_r_: the number estimated using the ratio specified by wl_lines_backward_ca_ratio, <br>_fr_: both _f_ and _r_ (_f_ takes precedence), <br>_n_: N/A.|choice|[_f_, _r_, _fr_,  _n_],|'r'<br>(cf.OptInfo.wl_lines_forward_ca_default)| 
_--wl_lines_backward_ca_ratio_,<br>_-wl_bca_ratio_|maximum ratio of lines to backward-search wikipedia links in the page; the number of candidate. lines are estimated for each attribute using the sample data.|float|(0.1-1.0)|_0.9_<br>(cf.OptInfo.wl_lines_backward_ca_ratio_default)| 
_--wl_lines_forward_ca_ratio_,<br>_-wl_fca_ratio_|maximum ratio of lines to forward-search wikipedia links in the page; the number of candidate lines are estimated for each attribute using the sample data.|float|(0.1-1.0) |_0.9_<br>(cf.OptInfo.wl_lines_forward_ca_ratio_default)| 
_--wl_score_same_,<br>_-wls_|score for the links around the mention (same line) in the page (when l is specified in wlink). |float| (0.0-1.0)|0.5<br>(cf.OptInfo.wl_score_same_default)| 
_--wl_score_backward_,<br>_-wlb_|score for the links around the mention (backward lines) in the page (when _l_ is specified in wlink).|float|(0.0-1.0) |0.3<br>(cf.OptInfo.wl_score_backward_default)|
_--wl_score_forward_,<br>_-wlf_|score for the links around the mention (forward lines) in the page (when _l_ is specified in wlink).|float|(0.0-1.0)|0.2<br>(cf.OptInfo.wl_score_forward_default)|
_--wf_score_,<br>_-wf_|score for the first wikipedia link in the mention (when _f_ is specified in wlink).|float| (0.0-1.0)|0.6<br>(cf.OptInfo.wf_score_default)|
_--wr_score_,<br>_-wr_|score for rightmost wikipedia link in the mention (when _r_ is specified in wlink).|float|(0.0-1.0) |0.8<br>(cf.OptInfo.wr_score_default)| 
_--wp_score_,<br>_-wp_|score for the links of the previous mentions in the page (when _p_ is specified in wlink). |float|(0.0-1.0) |0.7<br>(cf.OptInfo.wp_score_default)|

#### main module: (sl: self_link)
option|description| type | value|  default | note
:------------------------ |:-----------------|:---------|:---------|:---------|:---------------
_--f_slink_|filename of self link ratio file.|string| |_cat_att_selflink.tsv_<br>(cf.OptInfo.f_slink_default)| 
_--slink_min_,<br>_-s_min_|minimum self link ratio of attributes (in the target data) |float|(0.1-1.0) |_cat_att_selflink.tsv_<br>(cf.OptInfo.slink_min_default)| 
_--slink_prob_,<br>_-s_prb_|slink probability of the category-attribute pairs. <br><br>_fixed_: 1.0, **raw**: ratio based on the sample data, <br>_mid_: average of fixed and raw.|choice|[_fixed_, _raw_, _mid_]|fixed<br>(cf.OptInfo.slink_prob_default)| 
              
#### main module: lp
option|description| type | value|  default | note
:-------------------- |:-----------------|:---------|:---------|:---------|:---------------
_--f_link_prob_|filename of link probability info file|string| |_sample_cat_att_mention_linkcand.tsv_<br>(cf.OptInfo.f_link_prob_default)| 
_--lp_min_,<br>_-l_min_|minimum category-attribute-mention link probability in the link prob file (f_link_prob).|float|(0.1-1.0)|0.5<br>(cf.OptInfo.lp_min_default)| 

#### OPTIONS FOR FILTERING 
#### filtering: (il: incl filtering)
option                   |description| type | value|  default | note
:-----------------------|:-----------------|:---------|:---------|:---------|:---------------
_--**incl_tgt**_,<br>_-**i_tgt**_|target module of incoming link filtering,specified as the combination of the following characters.<br><br>_m_: mint,<br>_t_: tinm,<br>_w_: wlink,<br>_s_: slink,<br>_l_: link_prob,<br>_n_: N/A.|string|combination of [_m_, _t_, _w_, _s_, _l_] or [_n_]|'n'<br>(cf.OptInfo.incl_tgt_default)| 
_--incl_max_,<br>_-i_max_|maximum number of filtering candidate pages using incoming links.|int|  |1<br>(cf.OptInfo.incl_max_default)| 
_--incl_type_,<br>_-i_type_|type of incoming link filtering, <br><br>_o_: ordering by number of incoming links (reciprocal ranking),<br><br> _f_: filtering (keep the original values unchanged), <br>_a_: adjust value based on ordering by number of incoming links, <br>_n_: N/A|choice|[_o_, _f_, _a_, _n_]|'n'<br>(cf.OptInfo.incl_type_default)|required when incl_filtering is used.

#### filtering: (ar: attr_range_filtering)
option|description| type | value|  default | note
:---------------------------------------|:-----------------|:---------|:---------|:---------|:---------------
_--**attr_range_tgt**_,<br>_**-ar_tgt**_|target module of attribute range filtering, specified as the combination of the following characters. <br>_m_: mint, <br>_t_: tinm, <br>_w_: wlink, <br>_s_: slink, <br>_l_: link_prob, <br>_n_: N/A.|string|combination of [_m_, _t_, _w_, _s_, _l_] or ['n']|'n'<br>(cf.OptInfo.attr_rng_tgt_default)|required when attr_range_filtering is used.
_--attr_na_co_,<br>_-anc_|attr_na_co (base score (0.1-1.0) for candidate pages which are not given ENEW|float|(0.1-1.0) |_0.9_<br>(cf.OptInfo.attr_na_co_default)|
_--attr_ng_co_,<br>_-ang_|attr_ng_co (base score (0.1-1.0) for candidate pages which do not match attribute range|float|(0.1-1.0) |_0.1_<br>(cf.OptInfo.attr_ng_co_default)| 
_--attr_len_,<br>_-al_|scoring of the ENEID of candidate page as attribute range (eg. matching ratio between ENEIDs of candidate pages and that of gold pages).<br>_n_: raw matching ratio.<br>_a_: adjusted matching ratio (to ignore 1st layer of the ENE hierarchy if the ENEID begins with 1 (Name)). <br>_r_: raw matching ratio + raw depth (# of layers in the ENE hierarchy) of ENEID of the gold page,<br>_ar_: adjusted matching ratio + adjusted depth (adjusted to ignore 1st layer of the ENE hierarchy (specified in the attribute range definition file)if the ENEID begins with 1 (Name)), <br>_am_: adjusted matching ratio + modified depth (modify the adjusted depth to diminish its influence)|choice|[_a_, _r_, _ar_, _am_, _n_]|'n'<br>(cf.OptInfo.attr_len_default)|
_--f_attr_rng_|filename of attribute range definition file. The ranges are given as ENEIDs.|string| |_att_def.tsv_<br>(cf.OptInfo.f_attr_rng_default)| 
_--f_enew_info_|filename of enew_info_file.|string| |_ENEW_ENEtag_20200427_mod.tsv_<br>(cf.OptInfo.f_enew_info_default)|

#### filtering: (bl: back_link)
option|description| type | value|  default | note
:-----------------------------------|:-----------------|:---------|:---------|:---------|:---------------
_--**back_link_tgt**_,<br>_-**bl_tgt**_|target module of back link filtering, specified as the combination of the following characters. <br>_m_: mint,<br>_t_: tinm,<br>_w_: wlink,<br>_s_: slink, <br>_l_: link_prob, <br>_n_: N/A|string| combination of [_m_, _t_, _w_, _s_, _l_] or ['n']|'n'<br>(cf.OptInfo.back_link_tgt_default)|required when back_link is used.| 
_--back_link_ng_,<br>_-bl_ng_|score for not back link|float| |0.7<br>cf.OptInfo.back_link_ng_default)|  

#### filtering: (dn: nil_detection)
option|description| type | value|  default | note
:-----------------------------------|:-----------------|:---------|:---------|:---------|:---------------
_--**nil_tgt**_,<br>_-n_tgt_|target module of nil detection filtering, specified as the combination of the following characters, <br>'m: mint, t: tinm, w: wlink, s: slink, l: link_prob, n: N/A'|string|||
_--nil_cond_,<br>_-n_cond_|how to evaluate nil (unlinkable) for each mention using prob (estimated linkable ratio for category-attribute pairs based on sample data), len(minimum length of mention), and desc (descriptiveness of mentions).<br> _and_prob_len_desc_: judge as nil if all conditions (prob, len, desc) are satisfied. <br>_and_prob_or_len_desc_: judge as nil if prob condition is satisfied and either len condition or desc condition is satisfied. <br>_and_len_or_prob_desc_: judge as nil if len condition is satisfied and either prob condition or desc condition is satisfied.<br> _and_desc_or_prob_len_: judge as nil if desc condition is satisfied and either prob condition or len condition is satisfied.<br> _two_of_prob_len_desc_: judge as nil if at least two of the conditions(prob, len, and desc) are satisfied. |choice|[_and_prob_len_desc_, _and_prob_or_len_desc_, _and_len_or_prob_desc_, _and_desc_or_prob_len_, _two_of_prob_len_desc_]||
_--nil_desc_exception_,<br>_-n_exc_|a colon-separated exception list of exception of nil -desc- condition. If any of the following is specified, desc condition is not evaluated for the corresponding category attribute pairs. <br>eg. person_works:company_trade_names <br> person_works: (Person:作品) <br>company_trade_names: (Company:商品名). <br> Specify 'n' (N/A) for no exception.|string|||
_--nil_cat_attr_max_,<br>_-n_max_|maximum ratio of unlinkable category attribute pairs in the sample data. If nil ratio of the category-attribute pair of a mention is less than the ratio, the mention might be judged as unlinkable. (0.1-1.0)|float|(0.1-1.0)||
_--len_desc_text_min_,<br>_-ld_min_|minimum length of mention text regarded as descriptive.|int||
_--f_linkable_info_|filename of linkable ratio info file.|string|||
