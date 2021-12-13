import linkjpc as ljc
import logging


def check_link_prob(link_prob_min, mention_info, log_info, **d_link_prob):
    """Check if the probability of linking pid is equal or more than min.
    Args:
        link_prob_min
        mention_info
        log_info
        **d_link_prob
    Returns:
        cand_list
            format: [[pid, mod, link_prob], ...]
    """

    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    cand_list = []
    mod = 'l'
    tmp_cat_att_mention = '\t'.join([mention_info.ene_cat, mention_info.attr_label, mention_info.t_mention])

    if d_link_prob.get(tmp_cat_att_mention):
        pid_ratio_list = d_link_prob[tmp_cat_att_mention]
        for pid_ratio in pid_ratio_list:
            cand_pid = pid_ratio[0]
            ratio = float(pid_ratio[1])
            if float(ratio) >= link_prob_min:
                cand_list.append([cand_pid, mod, ratio])
    return cand_list


def get_link_prob_info(link_prob_file, lp_min, log_info):
    """Get the probability of the candidate pageids to be linked for the combination of category, attribute, and
    mention.
        If the combination has appeared in the sample data (ver.20210428) and the link probability is equal or
        more than lp_min, the highest probability is saved.
    Args:
        link_prob_file (str)
        lp_min (float)
        log_info
    Returns:
        d_link_prob (dict)
            format:
                key: <cat>\t<attr>\t<mention>
                val: [[pid,prob],.]
            sample:
                key: Compound\t種類\tカルシウム拮抗薬
                val: [[826886,1.0],[123456,0.5],....]
    Notice:
        link_prob_file (sorted in descending order by the probability)
        (format)
            <category>\t<attribute>\t<mention>\t<linkcand_pageid>:<ratio in sample data>:<freq in sample data>;....
        (sample)
            City	合併市区町村	上村	151917:0.25:1;37423:0.25:1;381057:0.25:1;1872659:0.25:1
    """

    import csv
    import re
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    d_link_prob = {}
    check_cat_att_mention_pid = {}
    with open(link_prob_file, 'r', encoding='utf-8') as lp:
        lp_reader = csv.reader(lp, delimiter='\t')
        for lp_row in lp_reader:
            cat_att_mention = lp_row[0] + '\t' + lp_row[1] + '\t' + lp_row[2]
            pid_ratio_freq_list = re.split(';', lp_row[3])
            max_ratio = 0.0
            for pid_ratio_freq in pid_ratio_freq_list:
                prf_list = re.split(':', pid_ratio_freq)
                tmp_ratio = float(prf_list[1])

                if tmp_ratio >= lp_min and tmp_ratio >= max_ratio:
                    max_ratio = tmp_ratio
                    cand_pid = prf_list[0]
                    cat_att_mention_pid = cat_att_mention + '\t' + cand_pid

                    if not check_cat_att_mention_pid.get(cat_att_mention_pid):
                        if not d_link_prob.get(cat_att_mention):
                            d_link_prob[cat_att_mention] = []
                        d_link_prob[cat_att_mention].append([cand_pid, tmp_ratio])
                        check_cat_att_mention_pid[cat_att_mention_pid] = 1
    return d_link_prob
