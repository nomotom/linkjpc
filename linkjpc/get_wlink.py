import config as cf
import linkjpc as ljc
import logging

def check_wlink(mention_info, opt_info, log_info, **diff_info):
    """Get candidate link list using wikipedia links.
    Args:
        mention_info
        opt_info
        log_info
        **diff_info
    Returns:
        wlink_cand_list
    Note:
    - cf.d_tag_info (dict)
        format:
            d_tag_info_header = ['cat', 'pid', 'line_id', 'text_start', 'text_end', 'text', 'title']
    - diff_info
        format:
            {'cat_attr': [backward_limit, forward_limit, diff_backward_num, diff_forward_num, diff_same_num,
            diff_all_num],....)
        sample:
            {'Person:地位職業': [-3, 10, 18, 24, 45], 'Person:生誕地': [-35, 19, 9, 22, 14, 45],


    """
    from decimal import Decimal, ROUND_HALF_UP
    import sys
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    cat_pid_lineid = mention_info.ene_cat + '_' + str(mention_info.pid) + '_' + str(mention_info.h_start_line_id)

    mod = 'w'
    wlink_cand_list = []
    wlink_cand_dict = {}

    check_n = {}
    check_f = {}
    check_r = {}
    check_m = {}
    check_p = {}
    check_same = {}
    check_backward = {}
    check_forward = {}

    wlink_cnt = 0
    if 'f' in opt_info.wikilink or 'r' in opt_info.wikilink or 'm' in opt_info.wikilink:

        if cf.d_tag_info.get(cat_pid_lineid):

            tmp_tag_info_list = cf.d_tag_info[cat_pid_lineid]

            tmp_cand_list = []
            for tmp_tag_info in tmp_tag_info_list:
                tmp_start = tmp_tag_info[0]
                tmp_end = tmp_tag_info[1]
                tmp_title = tmp_tag_info[3]

                if (mention_info.h_start_offset <= int(tmp_start)) and (int(tmp_end) <= mention_info.h_end_offset):

                    if cf.d_title2pid.get(tmp_title):
                        linkcand_pid = cf.d_title2pid[tmp_title]

                        if linkcand_pid:
                            tmp_cand_list.append([linkcand_pid, tmp_start])
                            wlink_cnt += 1

            if wlink_cnt >= 1:
                i = 0
                for linkcand_pid_start in tmp_cand_list:
                    i += 1
                    score = 0
                    if not linkcand_pid_start[0]:
                        logger.error({
                            'action': 'check_wlink',
                            'error': 'illegal linkcand_pid',
                            'linkcand_pid_start': linkcand_pid_start
                        })
                        sys.exit()
                    linkcand_pid = linkcand_pid_start[0]

                    if (i == 1) and (wlink_cnt == 1):
                        if not check_n.get(linkcand_pid):
                            score = 1.0
                            check_n[linkcand_pid] = score
                    elif (i == wlink_cnt) and ('r' in opt_info.wikilink):
                        if not check_r.get(linkcand_pid):
                            score = opt_info.wr_score
                            check_r[linkcand_pid] = score
                    elif (i == 1) and (wlink_cnt > 1) and ('f' in opt_info.wikilink):
                        if not check_f.get(linkcand_pid):
                            score = opt_info.wf_score
                            check_f[linkcand_pid] = score
                    else:
                        if not check_m.get(linkcand_pid):
                            score_str = str(1 / wlink_cnt)
                            score = float(Decimal(score_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
                            check_m[linkcand_pid] = score
                    if not wlink_cand_dict.get(linkcand_pid):
                        wlink_cand_dict[linkcand_pid] = score
                    else:
                        wlink_cand_dict[linkcand_pid] += score

    if 'p' in opt_info.wikilink:
        for tmp_line_id in reversed(range(0, mention_info.h_start_line_id)):
            tmp_cat_pid_lineid = mention_info.ene_cat + '_' + str(mention_info.pid) + '_' + str(tmp_line_id)

            if cf.d_tag_info.get(tmp_cat_pid_lineid):
                p_tmp_tag_info_list = cf.d_tag_info[tmp_cat_pid_lineid]

                for p_tmp_tag_info in p_tmp_tag_info_list:
                    p_tmp_text = p_tmp_tag_info[2]
                    p_tmp_title = p_tmp_tag_info[3]

                    if p_tmp_text == mention_info.t_mention:
                        if cf.d_title2pid.get(p_tmp_title):
                            tmp_linkcand_pid = cf.d_title2pid[p_tmp_title]

                            if not check_p.get(tmp_linkcand_pid):
                                tmp_score_str = \
                                    (tmp_line_id / mention_info.h_start_line_id) * opt_info.wp_score
                                tmp_score = \
                                    float(Decimal(tmp_score_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

                                if not wlink_cand_dict.get(tmp_linkcand_pid):
                                    wlink_cand_dict[tmp_linkcand_pid] = tmp_score
                                else:
                                    wlink_cand_dict[tmp_linkcand_pid] += tmp_score
                                check_p[tmp_linkcand_pid] = tmp_score
                                break
    if 'l' in opt_info.wikilink:
        attr = mention_info.attr_label
        cat = mention_info.ene_cat
        cat_attr = ':'.join([cat, attr])
        all_line_list = []

        # default max (common)
        backward_limit = mention_info.h_start_line_id - opt_info.wl_lines_backward_max
        forward_limit = mention_info.h_start_line_id + opt_info.wl_lines_forward_max

        # 'f' takes priority over 'r'
        if 'r' in opt_info.wl_lines_backward_ca:
            if diff_info.get(cat_attr):
                backward_limit = mention_info.h_start_line_id + diff_info[cat_attr][0]
        if 'f' in opt_info.wl_lines_backward_ca:
            if cf.diff_info_ca_backward.get(cat_attr):
                backward_limit = mention_info.h_start_line_id + cf.diff_info_ca_backward[cat_attr]

        # 'f' takes priority over 'r'
        if 'r' in opt_info.wl_lines_forward_ca:
            if diff_info.get(cat_attr):
                forward_limit = mention_info.h_end_line_id + diff_info[cat_attr][1]
        if 'f' in opt_info.wl_lines_forward_ca:
            if cf.diff_info_ca_forward.get(cat_attr):
                forward_limit = mention_info.h_end_line_id + cf.diff_info_ca_forward[cat_attr]

        if mention_info.h_end_line_id > mention_info.h_start_line_id:
            for s_line_id in range(mention_info.h_start_line_id, mention_info.h_end_line_id + 1):
                all_line_list.append(s_line_id)
        else:
            all_line_list.append(mention_info.h_start_line_id)
        for b_line_id in range(backward_limit, mention_info.h_start_line_id):
            all_line_list.append(b_line_id)
        for f_line_id in range(mention_info.h_end_line_id + 1, forward_limit + 1):
            all_line_list.append(f_line_id)
        for l_tmp_line_id in all_line_list:
            l_tmp_cat_pid_lineid = mention_info.ene_cat + '_' + str(mention_info.pid) + '_' + str(l_tmp_line_id)
            if cf.d_tag_info.get(l_tmp_cat_pid_lineid):
                l_tmp_tag_info_list = cf.d_tag_info[l_tmp_cat_pid_lineid]

                for l_tmp_tag_info in l_tmp_tag_info_list:
                    # l_tmp_text = l_tmp_tag_info[2]
                    l_tmp_title = l_tmp_tag_info[3]

                    if cf.d_title2pid.get(l_tmp_title):
                        l_tmp_linkcand_pid = cf.d_title2pid[l_tmp_title]
                        l_tmp_score_str = str(0)

                        if l_tmp_line_id == mention_info.h_start_line_id:
                            if not check_same.get(l_tmp_linkcand_pid):
                                l_tmp_score_str = str(opt_info.wl_score_same)
                                check_same[l_tmp_linkcand_pid] = opt_info.wl_score_same
                        elif l_tmp_line_id < mention_info.h_start_line_id:
                            if not check_backward.get(l_tmp_linkcand_pid):
                                l_tmp_score_str = str(opt_info.wl_score_backward)
                                check_backward[l_tmp_linkcand_pid] = opt_info.wl_score_backward
                        elif l_tmp_line_id > mention_info.h_start_line_id:
                            if not check_forward.get(l_tmp_linkcand_pid):
                                l_tmp_score_str = str(opt_info.wl_score_forward)
                                check_forward[l_tmp_linkcand_pid] = opt_info.wl_score_forward

                        l_tmp_score = float(Decimal(l_tmp_score_str).quantize(Decimal('0.01'),
                                                                              rounding=ROUND_HALF_UP))
                        if not wlink_cand_dict.get(l_tmp_linkcand_pid):
                            wlink_cand_dict[l_tmp_linkcand_pid] = l_tmp_score

                        # sum of scores in all options
                        else:
                            wlink_cand_dict[l_tmp_linkcand_pid] += l_tmp_score
                        if opt_info.wl_break:
                            break
    wlink_score_max = 0

    if 'm' in opt_info.wikilink or 'f' in opt_info.wikilink or 'r' in opt_info.wikilink:
        if wlink_cnt == 1:
            if (len(check_n) > 0) and (max(check_n.values()) > 1.0):
                logger.error({
                    'action': 'check_wlink',
                    'mention': mention_info.t_mention,
                    'error': 'max(check_n) is more than 1.0',
                    'max_n': max(check_n.values())
                })
                sys.exit()
            wlink_score_max += 1.0
        elif wlink_cnt > 1:
            if 'f' in opt_info.wikilink:
                if (len(check_f) > 0) and (max(check_f.values()) > 1.0):
                    logger.error({
                        'action': 'check_wlink',
                        'mention': mention_info.t_mention,
                        'error': 'max(check_f) is more than 1.0',
                        'max_f': max(check_f.values())
                    })
                    sys.exit()
                wlink_score_max += opt_info.wf_score

            if 'r' in opt_info.wikilink:
                if (len(check_r) > 0) and (max(check_r.values()) > 1.0):
                    logger.error({
                        'action': 'check_wlink',
                        'mention': mention_info.t_mention,
                        'error': 'max(check_r) is more than 1.0',
                        'max_r': max(check_r.values())
                    })
                    sys.exit()
                wlink_score_max += opt_info.wr_score

            # f, r, m
            if (len(check_m) > 0) and (max(check_m.values()) > 1.0):
                logger.error({
                    'action': 'check_wlink',
                    'mention': mention_info.t_mention,
                    'error': 'max(check_m) is more than 1.0',
                    'max_m': max(check_m.values())
                })
                sys.exit()
            wlink_score_max += 1.0

    if 'p' in opt_info.wikilink:
        if (len(check_p) > 0) and (max(check_p.values()) > 1.0):
            logger.error({
                'action': 'check_wlink',
                'mention': mention_info.t_mention,
                'error': 'max(check_p) is more than 1.0',
                'max_p': max(check_p.values())
            })
            sys.exit()
        wlink_score_max += opt_info.wp_score

    if 'l' in opt_info.wikilink:
        if (len(check_same) > 0) and (max(check_same.values()) > 1.0):
            logger.error({
                'action': 'check_wlink',
                'mention': mention_info.t_mention,
                'error': 'max(check_same) is more than 1.0',
                'max_same': max(check_same.values())
            })
            sys.exit()
        wlink_score_max += opt_info.wl_score_same

        if (len(check_backward) > 0) and (max(check_backward.values()) > 1.0):
            logger.error({
                'action': 'check_wlink',
                'mention': mention_info.t_mention,
                'error': 'max(check_backward) is more than 1.0',
                'max_backward': max(check_backward.values())
            })
            sys.exit()
        wlink_score_max += opt_info.wl_score_backward

        if (len(check_forward) > 0) and (max(check_forward.values()) > 1.0):
            logger.error({
                'action': 'check_wlink',
                'mention': mention_info.t_mention,
                'error': 'max(check_forward) is more than 1.0',
                'max_forward': max(check_forward.values())
            })
            sys.exit()
        wlink_score_max += opt_info.wl_score_forward

    for wpid, wscore in wlink_cand_dict.items():
        if wscore > wlink_score_max:
            logger.error({
                'action': 'check_wlink',
                'error': 'wscore is more than wlink_score_max',
                'wscore': wscore,
                'wlink_score_max': wlink_score_max,
                'opt_info.wikilink': opt_info.wikilink,
                'mention': mention_info.t_mention,
            })
            sys.exit()
        wscore_new = wscore/wlink_score_max
        if wscore_new > 1.0:
            logger.error({
                'action': 'check_wlink',
                'error': 'wscore_new is more than 1.0',
                'wlink_score_new': wscore_new,
                'wscore': wscore,
                'wlink_score_max': wlink_score_max,
                'opt_info.wikilink': opt_info.wikilink,
                'mention': mention_info.t_mention,
            })
            sys.exit()
        wlink_cand_list.append([wpid, mod, wscore_new])
    return wlink_cand_list


def reg_tag_info(html_info_file, log_info):
    """Register tag information.
    Args:
        html_info_file
        log_info
    Returns:
        d_tag_info (dict)
    Note:
        html_info_file
            Currently html info is based on sample data. (70 articles/category)
            format:
                header: cat(\t)pid(\t)line_id(\t)text_start(\t)text_end(\t)text(mention)(\t)title(of linked page)(\n)
            sample:
                City    1617736 71      200     202     座標    地理座標系
        d_tag_info
            format:
                key: cat_pid_lineid
                value: [text_start, text_end, text(mention), title(title of linked page)]
    """
    import csv
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    d_tag_info = {}
    d_tag_info_header = ['cat', 'pid', 'line_id', 'text_start', 'text_end', 'text', 'title']
    with open(html_info_file, 'r', encoding='utf-8') as ta:
        for row in csv.DictReader(ta, delimiter='\t', fieldnames=d_tag_info_header):
            lid = row['line_id']
            if str.isnumeric(lid):
                d_tag_info_key = row['cat'] + '_' + str(row['pid']) + '_' + str(lid)
                d_tag_info_val = [row['text_start'], row['text_end'], row['text'], row['title']]

                if d_tag_info_key not in d_tag_info:
                    d_tag_info[d_tag_info_key] = []

                d_tag_info[d_tag_info_key].append(d_tag_info_val)

    return d_tag_info


def reg_mention_gold_distance_ca(dist_ca_file, log_info):
    """register specified mention gold distance (maximum) by category * attribute.
    Args:
        dist_ca_file
        log_info
    Returns:
        diff_info_ca
    Note:
        dist_ca_file
            format
                cat(\t)attr(\t)diff_min(\n)
            sample (in case of dist_ca_forward_file)
                Person  作品        10
    """
    import re
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    diff_info_ca = {}
    with open(dist_ca_file, mode='r', encoding='utf-8') as m:
        for line in m:
            line = line.rstrip()
            if line[0] == '#':
                continue
            (cat, attr, diff_min_str) = re.split('\t', line)
            cat_attr = ':'.join([cat, attr])
            if cat == 'cat':
                continue
            diff_min = int(diff_min_str)
            diff_info_ca[cat_attr] = diff_min
    return diff_info_ca


def reg_mention_gold_distance(mention_gold_link_dist_file, opt_info, diff_info_file, log_info):
    """Sum up gold links of mentions by category * attribute.
    Args:
        mention_gold_link_dist_file
        opt_info
        diff_info_file
        log_info
    Returns:
        diff_info (dict)
    Output:
        mention_gold_link_dist_info_file: summary of gold links of mentions by category * attribute
    Note:
        mention_gold_link_dist_file
            The distance between mention and nearest gold link (backward/forward) in sample data.
            format
                cat(\t)attr(\t)diff_min(\n)
            sample
                Person  所属組織        223
                Person  所属組織        79
                Person  所属組織        143
        mention_gold_link_dist_info_file
            format
                tmp_cat, tmp_attr, backward_limit, forward_limit, diff_backward_num, diff_forward_num,
                diff_same_num, diff_all_num (tsv)
            sample
                Person  地位職業        -47     7       18      90      -63     45
                Person  生誕地  -57     6       9       21      15      45
        diff_info
            key: tmp_cat:tmp_attr
            value: [backward_limit, forward_limit, diff_backward_num, diff_forward_num, diff_same_num, diff_all_num]
    """
    import re
    import math
    import pandas as pd
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    diff_info = {}
    diff_all_list = []
    diff_all_dic = {}
    diff_forward_dic = {}
    diff_backward_dic = {}
    with open(mention_gold_link_dist_file, mode='r', encoding='utf-8') as m:
        cnt = 0
        for line in m:
            cnt += 1
            (cat, attr, rest) = re.split('\t', line)
            cat_attr = ':'.join([cat, attr])
            # header
            if cat == 'cat':
                continue
            diff_min_str = rest.rstrip()
            diff_min = int(diff_min_str)

            if not diff_all_dic.get(cat_attr):
                diff_all_dic[cat_attr] = []
            diff_all_dic[cat_attr].append(diff_min)

            if diff_min > 0:
                if not diff_forward_dic.get(cat_attr):
                    diff_forward_dic[cat_attr] = []
                diff_forward_dic[cat_attr].append(diff_min)
            if diff_min < 0:
                if not diff_backward_dic.get(cat_attr):
                    diff_backward_dic[cat_attr] = []
                diff_backward_dic[cat_attr].append(diff_min)

    for tmp_cat_attr, diff_min_list in diff_all_dic.items():
        (tmp_cat, tmp_attr) = re.split(':', tmp_cat_attr)

        diff_all_num = 0
        if diff_all_dic.get(tmp_cat_attr):
            diff_all_num = len(diff_all_dic[tmp_cat_attr])

        backward_cand_max_num = 0
        diff_backward_num = 0
        backward_limit = 0
        backward_list = []
        if diff_backward_dic.get(tmp_cat_attr):
            backward_list = sorted(diff_backward_dic[tmp_cat_attr], reverse=True)
            diff_backward_num = len(backward_list)
            backward_cand_max_num = math.ceil(opt_info.wl_lines_backward_ca_ratio * diff_backward_num)
            del backward_list[backward_cand_max_num:]
            if len(backward_list) > 0:
                backward_limit = backward_list[-1]

        forward_cand_max_num = 0
        diff_forward_num = 0
        forward_limit = 0
        forward_list = []
        if diff_forward_dic.get(tmp_cat_attr):
            forward_list = sorted(diff_forward_dic[tmp_cat_attr], reverse=True)
            diff_forward_num = len(forward_list)
            forward_cand_max_num = math.ceil(opt_info.wl_lines_forward_ca_ratio * diff_forward_num)
            del forward_list[forward_cand_max_num:]
            if len(forward_list) > 0:
                forward_limit = forward_list[-1]

        diff_same_num = diff_all_num - (diff_backward_num + diff_forward_num)
        diff_all_list.append([tmp_cat, tmp_attr, backward_limit, forward_limit, diff_backward_num, diff_forward_num,
                              diff_same_num, diff_all_num])

        diff_info[tmp_cat_attr] = [backward_limit, forward_limit, diff_backward_num, diff_forward_num, diff_same_num,
                                   diff_all_num]

    i_df = pd.DataFrame(diff_all_list, columns=['cat', 'attr', 'backward_limit', 'forward_limit', 'backward_num',
                                                'forward_num', 'diff_same_num', 'all_num'])
    i_df.to_csv(diff_info_file, sep='\t', index=False)

    return diff_info
