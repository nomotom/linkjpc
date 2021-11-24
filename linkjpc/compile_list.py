import linkjpc as ljc
import config as cf
import logging


def append_filtering_cand_info(filtering_cand_list, link_info, log_info):
    """append candidate link page list of each module to the final candidate list.
    Args:
        filtering_cand_list
        link_info
        log_info
    Returns:
    """
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    if len(filtering_cand_list) > 0:
        for cand_info in filtering_cand_list:
            pid = cand_info[0]
            mod = cand_info[1]
            val = cand_info[2]

            # lack eneid and the title is inadequate (list page, etc.)
            if not cf.d_pid_title_incoming_eneid.get(pid):
                continue

            if not cf.d_pid_title_incoming_eneid[pid][2]:
                if ('一覧' in cf.d_pid_title_incoming_eneid[pid][0]) or \
                        ('のリスト' in cf.d_pid_title_incoming_eneid[pid][0]):
                    continue

            if mod == 't':
                if not link_info.cand_dic_tinm.get(pid):
                    link_info.cand_dic_tinm[pid] = val
                else:
                    link_info.cand_dic_tinm[pid] += val

            if mod == 'm':
                if not link_info.cand_dic_mint.get(pid):
                    link_info.cand_dic_mint[pid] = val
                else:
                    link_info.cand_dic_mint[pid] += val

            if mod == 'w':
                if not link_info.cand_dic_wlink.get(pid):
                    link_info.cand_dic_wlink[pid] = val
                else:
                    link_info.cand_dic_wlink[pid] += val

            if mod == 's':
                if not link_info.cand_dic_slink.get(pid):
                    link_info.cand_dic_slink[pid] = val
                else:
                    link_info.cand_dic_slink[pid] += val

            if mod == 'l':
                if not link_info.cand_dic_link_prob.get(pid):
                    link_info.cand_dic_link_prob[pid] = val
                else:
                    link_info.cand_dic_link_prob[pid] += val
