import config as cf
import linkjpc as ljc
import logging
from operator import itemgetter


def filter_by_incoming_link(module_cand_list, mention_info, incoming_link_max, incoming_link_type, log_info,
                            **d_pid_title_incoming_eneid):
    """Filter by number of incoming links.
    Args:
        module_cand_list
        mention_info
        incoming_link_max
        incoming_link_type
        log_info
        **d_pid_title_incoming_eneid
    Returns:
        cand_list
            pid
            mod
            score of incoming links (1/ranking of num of incoming links)
                eg. 1.00: 1st, 0.50: 2nd, 0.33: 3rd
    Note:
        d_pid_title_incoming_eneid
            format: {to_pid: [to_title, to_incoming, to_eneid]}

    """
    import sys
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    if incoming_link_type != 'o' and incoming_link_type != 'f' and incoming_link_type != 'a':
        logger.error({
            'action': 'filter_by_incoming_link',
            'error': 'illegal incoming link type'
        })
        sys.exit()

    new_module_cand_list = []
    incoming_cand_list = []
    check = {}
    val = 0
    if len(module_cand_list) > 0:
        for cand_info in module_cand_list:
            logger.debug({
                'action': 'filter_by_incoming_link',
                'cand_info': cand_info
            })
            pid = cand_info[0]
            mod = cand_info[1]
            val = cand_info[2]
            if pid not in check:
                if d_pid_title_incoming_eneid.get(pid):
                    incoming = d_pid_title_incoming_eneid[pid][1]
                    incoming_cand_list.append([int(incoming), pid, mod, val])
                    check[pid] = 1
                    logger.debug({
                        'action': 'filter_by_incoming_link',
                        'attr': mention_info.attr_label,
                        'mention': mention_info.t_mention,
                        'link_cand_title': cf.d_pid_title_incoming_eneid[pid][0],
                        'incoming': int(incoming),
                        'pid': pid,
                        'mod': mod,
                        'val': val,
                    })

        logger.debug({
            'action': 'filter_by_incoming_link',
            'incoming_cand_list_before': incoming_cand_list,
        })
        incoming_cand_list.sort(key=itemgetter(0), reverse=True)
        cand_max = min(len(incoming_cand_list), incoming_link_max)
        logger.debug({
            'action': 'filter_by_incoming_link',
            'incoming_cand_list_sorted': incoming_cand_list,
            'cand_max': cand_max,
            'len_incoming_cand_list': len(incoming_cand_list),
            'incoming_link_max': incoming_link_max
        })

        for i in range(0, cand_max):
            if incoming_link_type == 'o':
                new_module_cand_list.append([incoming_cand_list[i][1], incoming_cand_list[i][2], 1 / (i + 1)])
                logger.debug({
                    'action': 'filter_by_incoming_link',
                    'incoming_link_type': incoming_link_type,
                    'attr': mention_info.attr_label,
                    'mention': mention_info.t_mention,
                    'i': i,
                    'link_cand_title': cf.d_pid_title_incoming_eneid[incoming_cand_list[i][1]][0],
                    'new_module_cand_list_append': [incoming_cand_list[i][1], incoming_cand_list[i][2], 1 / (i + 1)]
                })
            elif incoming_link_type == 'f':
                new_module_cand_list.append([incoming_cand_list[i][1], incoming_cand_list[i][2], val])
                logger.debug({
                    'action': 'filter_by_incoming_link',
                    'incoming_link_type': incoming_link_type,
                    'attr': mention_info.attr_label,
                    'mention': mention_info.t_mention,
                    'i': i,
                    'link_cand_title': cf.d_pid_title_incoming_eneid[incoming_cand_list[i][1]][0],
                    'new_module_cand_list_append': [incoming_cand_list[i][1], incoming_cand_list[i][2], val]
                })
            elif incoming_link_type == 'a':
                new_module_cand_list.append([incoming_cand_list[i][1], incoming_cand_list[i][2], val * (1/(i + 1))])
                logger.debug({
                    'action': 'filter_by_incoming_link',
                    'incoming_link_type': incoming_link_type,
                    'attr': mention_info.attr_label,
                    'mention': mention_info.t_mention,
                    'i': i,
                    'link_cand_title': cf.d_pid_title_incoming_eneid[incoming_cand_list[i][1]][0],
                    'new_module_cand_list_append': [incoming_cand_list[i][1], incoming_cand_list[i][2],
                                                    val * (1/(i + 1))]
                })
    return new_module_cand_list
