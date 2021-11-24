import linkjpc as ljc
import config as cf
import logging


def reg_title2pid_ext(title2pid_ext_file, log_info):
    """Register title2pid_info pages info.
    Args:
        title2pid_ext_file
        #eg. イギリス語      3377    英語    95319   1.7.24.1
        log_info
    Returns:
        d_title2pid
            # format
                key: from_title
                val: to_pid
            # eg: {'イギリス語':'3377'}
        d_pid_title_incoming_eneid
            # format
                key: to_pid
                val: to_title, to_incoming, to_eneid
            # eg: {'3377': ['英語', 95319','1.7.24.1'])
    Notice:
        - title2pid_title_ex
            format: 'from_title'\t'to_pid'\t'to_title'\t'to_incoming\t'to_eneid'

    """
    import csv
    logger = ljc.set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    d_title2pid = {}
    d_pid_title_incoming_eneid = {}

    with open(title2pid_ext_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            from_title = row[0]
            to_pid = str(row[1])
            to_title = row[2]
            to_incoming = row[3]
            to_eneid = str(row[4])
            d_title2pid[from_title] = to_pid

            d_pid_title_incoming_eneid[to_pid] = [to_title, to_incoming, to_eneid]

    return d_title2pid, d_pid_title_incoming_eneid
