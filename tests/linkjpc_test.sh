#!/bin/bash

# EXAMPLES: linkjpc

## !! PLEASE MODIFY THE DIRECTORIES BELOW !!

script="./linkjpc/linkjpc.py"
base_dir="/XXXX/XXXX/2021-LinkJP/"
base_data_dir="${base_dir}Download/"
common_data_dir="${base_data_dir}ljc_data/common/"
tmp_data_dir="${base_data_dir}ljc_data/test/"
in_dir="${base_data_dir}linkjp-eval-211027/ene_annotation/"
out_dir_base="${base_dir}test_out/sample/"


## EXAMPLE (exact match)
python $script $common_data_dir $tmp_data_dir $in_dir ${out_dir_base}mint_e/ --mod m --mint e
#
# main modules:   [matching (m)]
#   - [m]: exact match (e), mention in title (mint)


## EXAMPLE (wikipedia link)
python $script $common_data_dir $tmp_data_dir $in_dir ${out_dir_base}wlink_frp/ --mod w --wlink frp
#
# main modules: [get_wlink (w)]
#   - [w]: add higher score to the first link and rightmost link in the mention than others (fr)
#          give score to the links of the previous same mentions in the page (p)


## EXAMPLE (wikipedia link (+attribute range filtering) > self link > exact match)
python $script $common_data_dir $tmp_data_dir $in_dir ${out_dir_base}wlink_frp__slink_05_mint_e_attr_w/ --mod w:s:m -f a --mint e --wlink frp -s_min 0.5 -ar_tgt w
#
# priority of main modules:  [get_wlink (w)] > [self link (s)]  > [matching (m)]
#   - [w]: add higher score to the first link and rightmost link in the mention than others (fr)
#          give score to the links of the previous same mentions in the page (p)
#   - [s]: minimum self link ratio of attributes (0.5)
#   - [m]: exact match (e), mention in title (mint)
# filtering: [a(attr_range_filtering)]
#   - target: [w] (get_wlink)


## EXAMPLE (self link > exact match > wikipedia link (+attribute range filtering, back link filtering)
python $script $common_data_dir $tmp_data_dir $in_dir ${out_dir_base}slink_05_mid__mint_e__wlink_frp_attr_w_al_am_bl_w/ --mod s:m:w -f ab --mint e -s_min 0.5 -s_prb mid --wlink frp -ar_tgt w -al am -bl_tgt w
#
# priority of main modules: [self link (s)]  > [matching (m)] > [get_wlink (w)]
#   - [s]: minimum self link ratio of attributes (0.5)
#          slink probability of the category-attribute pairs: average of fixed value(1.0) and ratio based on sample data (mid)
#   - [m]: exact match (e), mention in title (mint)
#   - [w]: add higher score to the first link and rightmost link in the mention than others (fr)
#          give score to the links of the previous same mentions in the page (p)
# filtering: [a(attr_range_filtering)]
#   - target: [w] (get_wlink)
#   - scoring: adjusted matching ratio + modified depth (modify the adjusted depth to diminish its influence) (am)
# filtering:  [b(back_link)]
#   - target: [w] (get_wlink)

## EXAMPLE (self link > exact match > wikipedia link (+attribute range filtering, back link filtering), link_prob
python $script $common_data_dir $tmp_data_dir $in_dir ${out_dir_base}slink_05_mid__mint_e__wlink_rp_l_06_attr_w_al_am_bl_w/ --mod s:m:lw -f ab --mint e -s_min 0.5 -s_prb mid --wlink rp -ar_tgt w -al am -bl_tgt w -l_min 0.6
#
# priority of main modules: [self link (s)]  > [matching (m)] > [get_wlink (w)], [link_prob (l)]
#   - [s]: minimum self link ratio of attributes (0.5)
#          slink probability of the category-attribute pairs: average of fixed value(1.0) and ratio based on sample data (mid)
#   - [m]: exact match (e), mention in title (mint)
#   - [w]: add higher score to the rightmost link in the mention than others (r)
#          give score to the links of the previous same mentions in the page (p)
# filtering: [a(attr_range_filtering)]
#   - target: [w] (get_wlink)
#   - scoring: adjusted matching ratio + modified depth (modify the adjusted depth to diminish its influence) (am)
# filtering:  [b(back_link)]
#   - target: [w] (get_wlink)

## EXAMPLE (self link > exact match > wikipedia link (+attribute range filtering, back link filtering, nil detection), link_prob
python $script $common_data_dir $tmp_data_dir $in_dir ${out_dir_base}slink_05_mid__mint_e__wlink_rp_l_06_ncond_w_two_of_pld_02_7_attr_w_al_am_bl_w/ -n_tgt w -n_cond two_of_prob_len_desc -n_max 0.2 -ld_min 7 --mod s:m:lw -f abn --mint e -s_min 0.5 -s_prb mid --wlink rp -ar_tgt w -al am -bl_tgt w -l_min 0.6
#
# priority of main modules: [self link (s)]  > [matching (m)] > [get_wlink (w)], [link_prob (l)]
#   - [s]: minimum self link ratio of attributes (0.5)
#          slink probability of the category-attribute pairs: average of fixed value(1.0) and ratio based on sample data (mid)
#   - [m]: exact match (e), mention in title (mint)
#   - [w]: add higher score to the rightmost link in the mention than others (r)
#          give score to the links of the previous same mentions in the page (p)
# filtering: [a(attr_range_filtering)]
#   - target: [w] (get_wlink)
#   - scoring: adjusted matching ratio + modified depth (modify the adjusted depth to diminish its influence) (am)
# filtering:  [b(back_link)]
#   - target: [w] (get_wlink)
# filtering:  [n(detect_nil)]
#   - target: [w] (get_wlink)
#   - nil ratio(maximum: (0.2)
#   - nil condition: two_of_prob_len_desc (judge as nil if at least two of the conditions(prob, len, and desc))
#   - nil condition(len) minimum: (7)

## EXAMPLE (baseline: partial match + incoming link filtering)
python $script $common_data_dir $tmp_data_dir $in_dir ${out_dir_base}mint_p_incl_m_imax1_o/ --mod m -f i --mint p -i_tgt m -i_max 1 -i_type o
#
# main modules: [matching (m)]
#   - [m]: partial match, mention in title
# filtering: [incl_filtering (i)]
#   - target module: [m] (matching)
#   - maximum number of candidate pages: 1
#   - type of filtering: ordering by number of incoming links (reciprocal ranking) (o)






