import linkjpc as ljc
import logging


def estimate_nil(cat_attr, mention_info, opt_info, log_info, **d_linkable):
    """Create a list of nil candidates based on nil(unlinkable) cat-attr info, mention length, and mention pattern
    Args:
        cat_attr
        mention_info
        opt_info
        log_info
        **d_linkable
    Returns:
        res_nil
            1: unlinkable
            0: linkable
    Note:
        linkable info file
            format: (cat(\t)att(\t)linkable ratio)
            sample: City 地名の謂れ　0.14
            notice: Currently the ratio in the file is based on small sample data and highly recommended to be modified.
                    Some category-attribute pairs do not appear in the sample data.
        nil_cond
            how to evaluate nil (unlinkable) for each mention using prob (estimated linkable ratio for '
                   'category-attribute pairs based on sample data), len(minimum length of mention), and desc '
                   '(descriptiveness of mentions).
        nil_desc_exception
            exception of nil -desc- condition. If 'person_works' is specified, desc condition is not evaluated
            for the category attribute pairs(Person:works(作品)).
        len_desc_text_min (int)
            minimum length of mention text regarded as descriptive
        nil_cat_attr_max (float)
            maximum ratio of linkable category attribute pairs in the sample data.
            If nil ratio of the category-attribute pair of a mention is equal or less than the ratio,
            the mention might be judged as 'unlinkable'.
    """
    import sys
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    nil_cond = opt_info.nil_cond
    nil_desc_exception = opt_info.nil_desc_exception
    len_desc_text_min = opt_info.len_desc_text_min
    nil_cat_attr_max = opt_info.nil_cat_attr_max
    res_nil = 0

    res_prob_cond = 0
    link_prob_cat_attr = 0.0

    tmp_text = mention_info.t_mention
    if d_linkable.get(cat_attr):
        link_prob_cat_attr = d_linkable[cat_attr]

        if link_prob_cat_attr <= nil_cat_attr_max:
            res_prob_cond = 1

    res_len_cond = 0
    if 'len' in nil_cond:
        if len(tmp_text) >= len_desc_text_min:
            res_len_cond = 1

    res_desc_cond = 0
    check_exception_keyword = 0
    if 'desc' in nil_cond:
        for cat_attr_exc in opt_info.nil_desc_exception_def:
            if (cat_attr_exc in nil_desc_exception) and (cat_attr == opt_info.nil_desc_exception_def[cat_attr_exc]):
                check_exception_keyword = 1

        if check_exception_keyword == 0:
            res_desc_cond = evaluate_descriptiveness(tmp_text, log_info)

    if nil_cond == 'and_prob_len_desc':
        if (res_prob_cond == 1) and (res_len_cond == 1) and (res_desc_cond == 1):
            res_nil = 1
    elif nil_cond == 'and_prob_or_len_desc':
        if res_prob_cond == 1:
            if (res_len_cond == 1) or (res_desc_cond == 1):
                res_nil = 1
    elif nil_cond == 'and_len_or_prob_desc':
        if res_len_cond == 1:
            if (res_prob_cond == 1) or (res_desc_cond == 1):
                res_nil = 1
    elif nil_cond == 'and_desc_or_prob_len':
        if res_desc_cond == 1:
            if (res_prob_cond == 1) or (res_len_cond == 1):
                res_nil = 1
    elif nil_cond == 'two_of_prob_len_desc':
        if ((res_prob_cond == 1 and res_len_cond == 1) or
                (res_prob_cond == 1 and res_desc_cond == 1) or
                (res_len_cond == 1 and res_desc_cond == 1)):
            res_nil = 1

    logger.debug({
        'action': 'estimate_nil',
        'mention': tmp_text,
        'res_nil': res_nil,
        'cat_attr': cat_attr,
        'res_prob_cond': res_prob_cond,
        'link_prob_cat_attr':  link_prob_cat_attr,
        'res_len_cond': res_len_cond,
        'len(tmp_text)': len(tmp_text),
        'res_desc_cond': res_desc_cond,
    })

    return res_nil


def evaluate_descriptiveness(text, log_info):
    """evaluate descriptiveness of text
    Args:
        text
        log_info
    Returns:
        1: descriptive
        0: non-descriptive
    """
    import sys
    import re
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    # 1)substring

    # symbols (punctuation, colon, reference)
    symbol_list = [',', '。', '、', ':', '\[', '\]']

    # particles (adnominal)
    # adnominal_list = ['[^ぁ-ん]の']

    # particles (parallel)
    parallel_list = ['[^ぁ-ん]と', '[^ぁ-ん]や', 'および', '及び']

    # other particles, conjunctions
    particles_list = ['[^ぁ-ん]が', '[^ぁ-ん]は', 'を', '[^ぁ-ん]へ', '[^ぁ-ん]に', '[^ぁ-ん]も', '[^ぁ-ん]から', '[^ぁ-ん]まで',
                      '[^ぁ-ん]より', '[^ぁ-ん]よって', '[^ぁ-ん]で', '以後', '以降', '以前', '以来']

    # relaxing expressions
    relaxing_list = ['等の', '等に', 'など', '程度',  'ほぼ', 'おおむね', '大体', 'おそらく']

    # location expressions
    location_list = ['の一部', '囲まれた', '挟まれた', '突き出した', '面した', 'に位置',  'の全域', 'のあたり', '近く', '近郊']

    # conjunctive
    # conjunctive_list = ['し、', 'され、']

    # demostrative
    demonstrative_list = ['ここ', 'そこ', 'あそこ', 'どこ', 'この', 'その', 'あの', 'どの', 'これ', 'それ', 'あの', 'どの']

    subpat_list = symbol_list + parallel_list + particles_list + relaxing_list + location_list + demonstrative_list

    subpat_pat = '|'.join(subpat_list)

    # 2)prefix + (num)
    prefix_list = ['約[0-9零一二三四五六七八九十百千万億兆]', 'およそ']
    prefix_pat = '|'.join(prefix_list)

    # 3)(num) + suffix
    suffix_list = ['\[0-9\]kg', '\[0-9\]g', '\[0-9\]mg', '\[0-9\]L', '\[0-9\]mm', '℃', '%', '\[0-9\]回', '\[0-9\]位',
                   '\[0-9\]時間', '\[0-9\]分', '\[0-9\]秒', '年\[0-9\]+月']
    suffix_pat = '|'.join(suffix_list)

    subpat_p = re.compile(subpat_pat)
    prefix_p = re.compile(prefix_pat)
    suffix_p = re.compile(suffix_pat)

    res = 0
    if re.search(subpat_p, text) is not None:
        res = 1
        logger.debug({
            'action': 'estimate_nil',
            'text': text,
            'subpat_p_judge': 'yes',
            'subpat_p': subpat_p,
        })
    elif re.search(prefix_p, text) is not None:
        res = 1
        logger.debug({
            'action': 'estimate_nil',
            'text': text,
            'prefix_p_judge': 'yes',
            'prefix_p': prefix_p,
        })
    elif re.search(suffix_p, text) is not None:
        res = 1
        logger.debug({
            'action': 'estimate_nil',
            'text': text,
            'suffix_p_judge': 'yes',
            'suffix_p': suffix_p,
        })
    return res


def check_linkable_info(linkable_info_file, log_info):
    """Get 'linkable' category and attribute pairs and ratio dict.
    Args:
        linkable_info_file (str): linkable info file name
        log_info

    Returns:
        d_linkable: dictionary
            key: <ENE category of the page>:<attribute name>
            val: linkable ratio
    Note:
         linkable info file
            format: cat(\t)att(\t)likable ratio(\n)
            sample: City 地名の謂れ 0.14
    """

    import csv
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)
    d_linkable = {}
    with open(linkable_info_file, 'r', encoding='utf-8') as nl:
        nl_reader = csv.reader(nl, delimiter='\t')

        for line in nl_reader:
            cat_attr = ':'.join([line[0], line[1]])
            d_linkable[cat_attr] = float(line[2])
    return d_linkable
