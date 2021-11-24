import linkjpc as ljc
import config as cf


def scoring(opt_info, link_info, mention_info, mod_info, log_info):
    """scoring candidate pages to be linked for a mention.
    Args:
        opt_info
        link_info
        mention_info
        mod_info
        log_info
    Returns:
        record key used to distinguish the record from others (str)
    Notice:
        mod_info: mod_info for current mention
    """
    import re
    import sys
    from operator import itemgetter
    import logging

    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    # priority group
    mod_prior_list = re.split(':', opt_info.mod)

    # weight
    g_weight_list = []
    g_weight_list = re.split(':', opt_info.mod_w)

    i = 0
    for mod_prior_grp in mod_prior_list:
        if 't' in mod_prior_grp:
            mod_info.tinm_weight = float(g_weight_list[i])
        if 'm' in mod_prior_grp:
            mod_info.mint_weight = float(g_weight_list[i])
        if 'w' in mod_prior_grp:
            mod_info.wlink_weight = float(g_weight_list[i])
        if 's' in mod_prior_grp:
            mod_info.slink_weight = float(g_weight_list[i])
        if 'l' in mod_prior_grp:
            mod_info.link_prob_weight = float(g_weight_list[i])
        i += 1

    final_cand_list = []

    tinm_score = 0
    mint_score = 0
    wlink_score = 0
    slink_score = 0
    link_prob_score = 0

    keys_tinm = list(link_info.cand_dic_tinm.keys())
    keys_mint = list(link_info.cand_dic_mint.keys())
    keys_wlink = list(link_info.cand_dic_wlink.keys())
    keys_slink = list(link_info.cand_dic_slink.keys())
    keys_link_prob = list(link_info.cand_dic_link_prob.keys())

    keys_all = keys_tinm + keys_mint + keys_wlink + keys_slink + keys_link_prob

    new_keys_all = list(dict.fromkeys(keys_all))
    logger.debug({
        'action': 'scoring',
        'new_keys_all(original)': new_keys_all,
    })
    if opt_info.score_type == 'id':
        new_keys_all.sort(key=int)
        logger.debug({
            'action': 'scoring',
            'new_keys_all(sorted)': new_keys_all,
        })
    # The order of candidate pids is unstable

    for pid in new_keys_all:
        if pid in link_info.cand_dic_tinm:
            if link_info.cand_dic_tinm[pid] > 1.0:
                logger.error({
                    'action': 'scoring',
                    'error': 'tinm_org_score is more than 1.0',
                })
                sys.exit()
            tinm_score = link_info.cand_dic_tinm[pid] * mod_info.tinm_weight

        # score of the pid for the mention
        if pid in link_info.cand_dic_mint:
            if link_info.cand_dic_mint[pid] > 1.0:
                logger.error({
                    'action': 'scoring',
                    'error': 'mint_org_score is more than 1.0',
                })
                sys.exit()
            mint_score = link_info.cand_dic_mint[pid] * mod_info.mint_weight

        if pid in link_info.cand_dic_wlink:
            if link_info.cand_dic_wlink[pid] > 1.0:
                logger.error({
                    'action': 'scoring',
                    'error': 'wlink_org_score is more than 1.0',
                })
                sys.exit()
            wlink_score = link_info.cand_dic_wlink[pid] * mod_info.wlink_weight

        if pid in link_info.cand_dic_slink:
            if link_info.cand_dic_slink[pid] > 1.0:
                logger.error({
                    'action': 'scoring',
                    'error': 'slink_org_score is more than 1.0',
                })
                sys.exit()
            slink_score = link_info.cand_dic_slink[pid] * mod_info.slink_weight

        if pid in link_info.cand_dic_link_prob:
            if link_info.cand_dic_link_prob[pid] > 1.0:
                logger.error({
                    'action': 'scoring',
                    'error': 'link_prob_org_score is more than 1.0',
                })
                sys.exit()
            link_prob_score = link_info.cand_dic_link_prob[pid] * mod_info.link_prob_weight

        total_score = mint_score + tinm_score + wlink_score + slink_score + link_prob_score
        ext_title = ''
        try:
            ext_title = cf.d_pid_title_incoming_eneid[pid][0]
        except (KeyError, ValueError):
            logger.warning({
                'action': 'scoring',
                'pid': pid,
                'mention': mention_info.t_mention,
                'ext_title': 'null',
            })
            pass
        final_cand_list.append([pid, total_score])

    new_cand_list = sorted(final_cand_list, key=itemgetter(1), reverse=True)

    return new_cand_list
