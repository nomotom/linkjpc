#!/bin/bash

# EXAMPLES: linkjpc_prep

## !! PLEASE MODIFY THE DIRECTORIES BELOW !!
script="./linkjpc/linkjpc_prep.py"
base_dir="/XXXX/XXXX/2021-LinkJP/"
base_data_dir="${base_dir}Download/"
common_data_dir="${base_data_dir}ljc_data/common/"
tmp_data_dir="${base_data_dir}ljc_data/test/"
in_dir="${base_data_dir}linkjp-eval-211027/ene_annotation/"
sample_input_dir="${base_dir}Download/linkjp-sample-210428/ene_annotation/"
sample_gold_dir="${base_dir}Download/linkjp-sample-210428/link_annotation/"


python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --gen_redirect
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --gen_incoming_link
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --gen_title2pid_ext
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --gen_back_link
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --gen_common_html
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --gen_sample_gold_tsv
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --gen_link_dist
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --gen_link_prob
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --pre_matching mint --title_matching_mint trim --char_match_min 0.1
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --pre_matching mint --title_matching_mint full --char_match_min 0.1
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --pre_matching tinm --title_matching_tinm trim --char_match_min 0.1
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --pre_matching tinm --title_matching_tinm full --char_match_min 0.1
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --gen_slink
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --gen_linkable
python $script $common_data_dir $tmp_data_dir $in_dir $sample_gold_dir $sample_input_dir --gen_html

