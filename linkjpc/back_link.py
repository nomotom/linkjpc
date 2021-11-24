import linkjpc as ljc
import logging


def filter_by_back_link(module_cand_list, opt_info, mention_info, log_info, **d_back_link):
    """Filter candidate pages by back link.
    Args:
        module_cand_list
        opt_info
        mention_info
        log_info
        **d_back_link
    Returns:
        cand_list
    """
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    new_module_cand_list = []
    if len(module_cand_list) > 0:

        for cand_info in module_cand_list:
            cand_pid = cand_info[0]
            mod = cand_info[1]
            val = cand_info[2]

            org_pid = mention_info.pid
            org_pid_cand_pid = ':'.join([org_pid, cand_pid])
            if d_back_link.get(org_pid_cand_pid):
                score = val * opt_info.back_link_ok
            else:
                score = val * opt_info.back_link_ng

            new_module_cand_list.append([cand_pid, mod, score])
    return new_module_cand_list


def check_back_link_info(back_link_file, log_info, **d_title2pid):
    """Get 'back link' info from back link info file.
    Args:
        back_link_file (str): back link info file name
        log_info
        d_title2pid
    Returns:
        d_back_link: dictionary (key: <pid>:<from_pid>, val:1)
    Notice:
        back link info file
            format: (org_title(\t)from_pid(\t)from_title)
    """
    import csv
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    d_back_link = {}
    with open(back_link_file, 'r', encoding='utf-8') as bl:
        bl_reader = csv.reader(bl, delimiter='\t')

        for line in bl_reader:
            org_title = line[0]
            # back link
            from_pid = line[1]

            if not d_title2pid.get(org_title):
                logger.warning({
                    'action': 'check_back_link_info',
                    'title not registered in f_title2pid_ext': line
                })
            else:
                org_pid = d_title2pid[org_title]
                org_pid_from_pid = ':'.join([org_pid, from_pid])
                d_back_link[org_pid_from_pid] = 1
    return d_back_link
