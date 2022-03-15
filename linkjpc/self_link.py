import linkjpc as ljc
import logging


def estimate_self_link(cat_attr, slink_prob, mention_info, log_info, **d_self_link):
    """Create a list of self link based on self link info.

    Args:
        cat_attr
        slink_prob (fixed/raw/mid)
        mention_info
        log_info
        **d_self_link
    Returns:
        slink_cand_list
            format: [(pid, mod, score)]
    Note:
        selflink info file
            format: (cat(\t)att(\t)selflink ratio)
            sample: Compound 商標名 0.75
            notice: Currently the ratio in the file is based on small sample data and highly recommended to be modified.
    """
    import sys
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    slink_cand_list = []

    if d_self_link.get(cat_attr):
        if slink_prob == 'fixed':
            slink_cand_list = [(mention_info.pid, 's', 1.0)]
        elif slink_prob == 'raw':
            if d_self_link[cat_attr] > 1.0:
                logger.error({
                    'action': 'estimate_self_link',
                    'error': 'slink_score_max is more than 1.0',
                    'slink_score_max': d_self_link[cat_attr],
                })
                sys.exit()
            slink_cand_list = [(mention_info.pid, 's', d_self_link[cat_attr])]
        elif slink_prob == 'mid':
            score = (1 + d_self_link[cat_attr])/2
            if score > 1.0:
                logger.error({
                    'action': 'estimate_self_link',
                    'error': 'slink_score_max is more than 1.0',
                    'slink_score_max': score,
                })
                sys.exit()
            slink_cand_list = [(mention_info.pid, 's', score)]
    return slink_cand_list


def check_slink_info(slink_file, slink_min, log_info):
    """Get 'selflink' category and attribute pairs.
    Args:
        slink_file (str): selflink info file name
        slink_min(float): minimum ratio to apply 'selflink' to the above category and attribute pair
        log_info

    Returns:
        d_self_link: dictionary
            key: <ENE category of the page>:<attribute name>
            val: self_link_ratio
    Note:
        selflink info file
            format: cat(\t)att(\t)selflink ratio(\n)
            sample: Compound 商標名 0.75
    """

    import csv
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)
    d_self_link = {}
    with open(slink_file, 'r', encoding='utf-8') as sl:
        sl_reader = csv.reader(sl, delimiter='\t')

        for line in sl_reader:
            if float(line[2]) >= slink_min:
                cat_attr = ':'.join([line[0], line[1]])
                d_self_link[cat_attr] = float(line[2])
    return d_self_link
