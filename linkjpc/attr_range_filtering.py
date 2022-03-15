import linkjpc as ljc
import config as cf
import logging


def filter_by_attr_range(module_cand_list, mention_info, opt_info, log_info, **d_cat_attr2eneid_prob):

    """Filter candidate pages to be linked by attribute range.
    Args:
        module_cand_list:
        mention_info:
        opt_info
        log_info
        **d_cat_attr2eneid_prob:
    Returns:
        new_module_cand_list:
    """
    from decimal import Decimal, ROUND_HALF_UP
    import re
    import sys
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    new_module_cand_list = []

    if len(module_cand_list) > 0:
        for cand_info in module_cand_list:
            pid = cand_info[0]
            mod = cand_info[1]
            if not mod:
                logger.error({
                    'action': 'filter_by_attr_range',
                    'error': 'mod is empty',
                    'cand_info missing mod': cand_info,
                })
                sys.exit()
            val = cand_info[2]
            attr = mention_info.attr_label
            cat = mention_info.ene_cat

            cat_attr = cat + '__' + attr
            attr_co = 1.0
            attr_ok_co = opt_info.attr_ok_co
            attr_ng_co = opt_info.attr_ng_co
            attr_na_co = opt_info.attr_na_co

            if not d_cat_attr2eneid_prob.get(cat_attr):
                if cf.d_pid2eneid.get(pid):
                    cand_eneid = cf.d_pid2eneid[pid]
                    logger.debug({
                        'action': 'filter_by_attr_range',
                        'co_type': 'cat attr not defined in d_cat_attr2eneid_prob',
                        'cat_attr': cat_attr,
                        'cand_eneid': cand_eneid,
                        'mention': mention_info.t_mention,
                        'title': cf.d_pid_title_incoming_eneid[pid][0],
                        'attr_co': attr_co
                    })
            else:
                ans_eneid_prob_list = d_cat_attr2eneid_prob[cat_attr]
                attr_co_cand = []

                if not cf.d_pid2eneid.get(pid):
                    tmp_attr_co = attr_na_co
                    attr_co_cand.append(tmp_attr_co)
                else:
                    tmp_eneid = cf.d_pid2eneid[pid]
                    tmp_eneid_split = []
                    tmp_eneid_split = re.split('\.', tmp_eneid)

                    for ans_eneid_prob in ans_eneid_prob_list:
                        ans_eneid = ans_eneid_prob[0]
                        ans_prob = ans_eneid_prob[1]
                        ans_prob_float = float(ans_prob)
                        ans_eneid_split = []
                        ans_eneid_split = re.split('\.', ans_eneid)
                        par_cnt = 0
                        tmp_attr_co = 0
                        for i in range(0, len(ans_eneid_split)):
                            if ans_eneid_split[i] == tmp_eneid_split[i]:
                                if ((i != 0) or (ans_eneid_split[i] != opt_info.eneid_ignore)
                                        or ('a' not in opt_info.attr_len)):
                                    par_cnt += 1
                            else:
                                break
                        if par_cnt > 0:
                            ans_depth = 0
                            if opt_info.attr_len == 'a':
                                if ans_eneid_split[0] == opt_info.eneid_ignore:
                                    tmp_ratio = par_cnt / (len(ans_eneid_split) - 1)
                                    tmp_attr_co_str = str(tmp_ratio * attr_ok_co * ans_prob_float)
                                else:
                                    tmp_ratio = par_cnt / len(ans_eneid_split)
                                    tmp_attr_co_str = str(tmp_ratio * attr_ok_co * ans_prob_float)
                            elif opt_info.attr_len == 'r':
                                ans_depth = len(ans_eneid_split)/opt_info.attr_len_max
                                tmp_ratio = par_cnt / len(ans_eneid_split)
                                tmp_attr_co_str = str(tmp_ratio * ans_depth * attr_ok_co * ans_prob_float)
                            elif opt_info.attr_len == 'ar':
                                if ans_eneid_split[0] == opt_info.eneid_ignore:
                                    ans_depth = (len(ans_eneid_split) - 1) / (opt_info.attr_len_max - 1)
                                    tmp_ratio = par_cnt / (len(ans_eneid_split) - 1)
                                    tmp_attr_co_str = str(tmp_ratio * ans_depth * attr_ok_co * ans_prob_float)
                                else:
                                    tmp_attr_co_str = str((par_cnt/len(ans_eneid_split)) * attr_ok_co * ans_prob_float)
                            elif opt_info.attr_len == 'am':
                                if ans_eneid_split[0] == opt_info.eneid_ignore:
                                    ans_depth = opt_info.attr_depth_base_default + \
                                            (1 - opt_info.attr_depth_base_default) \
                                            * ((len(ans_eneid_split) - 1) / (opt_info.attr_len_max - 1))
                                    tmp_ratio = par_cnt / (len(ans_eneid_split) - 1)
                                else:
                                    ans_depth = opt_info.attr_depth_base_default + \
                                                (1 - opt_info.attr_depth_base_default) \
                                                * (len(ans_eneid_split) / opt_info.attr_len_max)
                                    tmp_ratio = par_cnt / len(ans_eneid_split)
                                tmp_attr_co_str = str(tmp_ratio * ans_depth * attr_ok_co * ans_prob_float)
                            else:
                                tmp_attr_co_str = str((par_cnt/len(ans_eneid_split)) * attr_ok_co * ans_prob_float)

                            tmp_attr_co = float(Decimal(tmp_attr_co_str).quantize(Decimal('0.01'),
                                                                                  rounding=ROUND_HALF_UP))
                        else:
                            tmp_attr_co = attr_ng_co
                        attr_co_cand.append(tmp_attr_co)
                attr_co = max(attr_co_cand)

            new_val = attr_co * val
            new_module_cand_list.append([pid, mod, new_val])

    if len(new_module_cand_list) > 0:
        new_module_cand_list.sort(key=lambda x: x[2], reverse=True)

        if new_module_cand_list[0][2] > 1.0:
            logger.error({
                'action': 'filter_by_attr_range',
                'error': 'score max is more than 0'
            })
            sys.exit()
    return new_module_cand_list


def get_attr_range(attr_range_file, opt_info, log_info):
    """Get attribute range probability info that shows which ENE category the attribute values are likely to be
    classified into.
    Args:
        attr_range_file (str):
        opt_info
        log_info
    Returns:
        d_cat_attr2eneid_prob: dictionary
    Note:
        attr_range_file
            (format)
                cat(\t)attribute_label(\t)ene:<ENEID>(\t)probability
            (sample)
                Person  国   ene:1.5.1.3 1.0
                Person  国   ene:1.5.1.0 0.5
        d_cat_attr2eneid_prob: dictionary
         (format)
            (key: <cat>__<attr>, val:[[<eneid>, <prob>], [<eneid>, <prob>],...])
                cat: ene_label_en
                attr: attribute_name
         (sample)
            {'City__国': [['1.5.1.0', 1.0], ['1.5.1.3',0.5], 'Airport__国': [['1.5.1.0', 1.0], ['1.5.1.3', 0.5]], ....}
    """
    import re
    import csv
    import sys
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    d_cat_attr2eneid_prob = {}
    with open(attr_range_file, 'r', encoding='utf-8') as a:
        a_reader = csv.reader(a, delimiter='\t')
        cat_attr_range_prob_list = [cat_attr_range_prob for cat_attr_range_prob in a_reader]

        for cat_attr_range_prob in cat_attr_range_prob_list:
            if len(cat_attr_range_prob) < opt_info.attr_len_max:
                logger.error({
                    'action': 'get_attr_range',
                    'cat_attr_range_prob too short': cat_attr_range_prob,
                })
                sys.exit()
            try:
                eneid = re.sub('ene:', '', cat_attr_range_prob[2])
            except (KeyError, ValueError) as e:
                logger.error({
                    'action': 'get_attr_range',
                    'error': e
                })
            cat = cat_attr_range_prob[0]
            if cat not in opt_info.cat_set:
                logger.error({
                    'action': 'get_attr_range',
                    'error': 'illegal cat: not defined in attr_range_file',
                    'cat': cat
                })
            attr = cat_attr_range_prob[1]
            prob = float(cat_attr_range_prob[3])

            cat_attr = cat + '__' + attr
            if not d_cat_attr2eneid_prob.get(cat_attr):
                d_cat_attr2eneid_prob[cat_attr] = []
            d_cat_attr2eneid_prob[cat_attr].append([eneid, prob])
    return d_cat_attr2eneid_prob


def reg_enew_info(enew_info, log_info):
    """Create a dictionary and store enew info.
    Args:
        enew_info
        log_info
    Returns:
        d_pid2eneid (dict)
    Note:
        enew_info
            ENEW info of pages extracted from Wikipedia cirrus dump and modified.

    """
    import re
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    d_pid2eneid = {}
    with open(enew_info, 'r', encoding='utf-8') as em:
        for line in em:
            (pageid, eneid, title) = re.split('\t', line)

            if pageid not in d_pid2eneid:
                d_pid2eneid[pageid] = eneid
    return d_pid2eneid
