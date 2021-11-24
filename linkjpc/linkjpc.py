# modules
import incl_filtering as il
import matching as mc
import get_wlink as gw
import self_link as sl
import link_prob as lp
import attr_range_filtering as ar
import compile_list as cl
import get_score as gs
import ljc_common as lc
import back_link as bl
from glob import glob
import json
import os
import sys
import click
import copy
import config as cf
import logging
import logging.config


def set_logging(log_info, logger_name):
    logging_ini = log_info.logging_ini
    logging.config.fileConfig(logging_ini)
    logger = logging.getLogger(logger_name)
    return logger


@click.command()
@click.argument('common_data_dir', type=click.Path(exists=True))
@click.argument('tmp_data_dir', type=click.Path(exists=True))
@click.argument('in_dir', type=click.Path(exists=True))
@click.argument('out_dir',  type=click.Path(dir_okay=True))
# common
@click.option('--filtering', '-f', type=click.Choice(['a', 'i', 'b', 'i', 'ai', 'ab', 'bi', 'abi', 'n']), required=True,
              default=cf.OptInfo.filtering_default, show_default=True,
              help='types of filtering used in any module, a: attribute range filtering, i: filtering by incoming link '
                   'num,　b: backlink, ai: both a and i, ab: both a and b, bi: both b and i, n: N/A')
@click.option('--mod', type=click.STRING, required=True,
              help='a comma-separated priority list of module groups'
                   '(denoted by the combination of characters (m, t, w, s, l)) to be used'
                   'eg. m:sw:t (first priority group: m, second priority group:sw, third priority group:t)')
@click.option('--mod_w', type=click.STRING,
              default=cf.OptInfo.mod_w_default, show_default=True,
              help='module group weight list (Float list separated by colon),'
                   'format: mod_group_first_weight:mod_group_second_weight:mod_group_third_weight:'
                   'mod_group_fourth_weight:mod_group_fifth_weight,'
                   'eg: 1.0:0.1:0.01:0.001:0.0001')
@click.option('--ans_max', '-a_max', type=click.INT, required=True,
              default=cf.OptInfo.ans_max_default, show_default=True,
              help='maximum number of output answers for one mention')
@click.option('--score_type', type=click.Choice(['id', 'n']),
              default=cf.OptInfo.score_type_default, show_default=True,
              help='scoring type,'
                   'id: use numerical sort result of candidate pageids if their scores are the same, n: N/A')
@click.option('--f_title2pid_ext', type=click.STRING,
              default=cf.DataInfo.f_title2pid_ext_default, show_default=True,
              help='filename of title2pageid extended information file, in which most of the disambiguation, '
                   'management or format-error pages are deleted and ENEIDs and incoming link num info are added.')
# modules (mint & tinm)
@click.option('--char_match_cand_num_max', '-c_max', type=click.INT,
              default=cf.OptInfo.char_match_cand_num_max_default, show_default=True,
              help='maximum number of candidate link pages for one mention in each string matching module (mint/tinm)')
# module: mint
@click.option('--mint', type=click.Choice(['e', 'p', 'n']),
              default=cf.OptInfo.mint_default, show_default=True,
              help='mention in title: how to match mentions to titles of candidate pages: '
                   'e: exact match, p: partial match, n: N/A')
@click.option('--mint_min', '-m_min', type=click.FLOAT,
              default=cf.OptInfo.mint_min_default, show_default=True,
              help='minimum length ratio of mentions in titles of candidate Wikipedia pages to be linked.')
@click.option('--f_mint', type=click.STRING,
              default=cf.DataInfo.f_mint_partial_default, show_default=True,
              help='filename of partial match info file (mention in title)')
@click.option('--f_mint_trim', type=click.STRING,
              default=cf.DataInfo.f_mint_trim_partial_default, show_default=True,
              help='filename of partial match info file (mention in title)')
@click.option('--title_matching_mint', '-tmm', type=click.Choice(['trim', 'full']),
              default=cf.OptInfo.title_matching_mint_default, show_default=True,
              help='title matching in mint (title matching in mention in title)')
# module: tinm
@click.option('--tinm', type=click.Choice(['e', 'p', 'n']),
              default=cf.OptInfo.tinm_default, show_default=True,
              help='title in mention: how to match titles of candidate pages to mentions'
                   'e: exact match, p: partial match, n: N/A')
@click.option('--tinm_min', '-t_min', type=click.FLOAT,
              default=cf.OptInfo.tinm_min_default, show_default=True,
              help='minimum length ratio of titles of candidate Wikipedia pages in mentions. ')
@click.option('--f_tinm', type=click.STRING,
              default=cf.DataInfo.f_tinm_partial_default, show_default=True,
              help='filename of partial match info file (title in mention)')
@click.option('--f_tinm_trim', type=click.STRING,
              default=cf.DataInfo.f_tinm_trim_partial_default, show_default=True,
              help='filename of partial match info file (title trimmed in mention)')
@click.option('--title_matching_tinm', '-tmt', type=click.Choice(['trim', 'full']),
              default=cf.OptInfo.title_matching_tinm_default, show_default=True,
              help='title matching in tinm (title matching in title in mention)')
# module: wlink
@click.option('--wlink', '-wl', type=click.STRING, required=True,
              default=cf.OptInfo.wlink_default, show_default=True,
              help='scoring of the wikipedia links in the mentions. combination of the following: '
                   'f: add higher score to the first link in the mention than others,'
                   'r: add higher score to the rightmost link in the mention than others, '
                   'm: give equal score to all the links in the mention'
                   'p: give score to the links of the previous same mentions in the page'
                   'l: give score to the links around the mention in the lines of page specified with wl_lines_pre_max '
                   'and wl_lines_forward_max'
                   'n: N/A. '
                   'Notice that m cannot be used with f or r.')
@click.option('--f_html_info', type=click.STRING,
              default=cf.DataInfo.f_html_info_default, show_default=True,
              help='filename of html tag info file.')
@click.option('--wf_score', '-wf', type=click.FLOAT,
              default=cf.OptInfo.wf_score_default, show_default=True,
              help='score for the first wikipedia link in the mention (when f is specified in wlink).(0.0-1.0)')
@click.option('--wr_score', '-wr', type=click.FLOAT,
              default=cf.OptInfo.wr_score_default, show_default=True,
              help='score for rightmost wikipedia link in the mention (when r is specified in wlink).(0.0-1.0)')
@click.option('--wp_score', '-wp', type=click.FLOAT,
              default=cf.OptInfo.wp_score_default, show_default=True,
              help='score for the links of the previous mentions in the page (when p is specified in wlink). (0.0-1.0)')
@click.option('--wl_score_same', '-wls', type=click.FLOAT,
              default=cf.OptInfo.wl_score_same_default, show_default=True,
              help='score for the links around the mention (same line) in the page (when l is specified in wlink).'
                   ' (0.0-1.0)')
@click.option('--wl_score_backward', '-wlb', type=click.FLOAT,
              default=cf.OptInfo.wl_score_backward_default, show_default=True,
              help='score for the links around the mention (backward lines) in the page (when l is specified in wlink).'
                   '(0.0-1.0)')
@click.option('--wl_score_forward', '-wlf', type=click.FLOAT,
              default=cf.OptInfo.wl_score_forward_default, show_default=True,
              help='score for the links around the mention (forward lines) in the page (when l is specified in wlink).'
                   '(0.0-1.0) ')
@click.option('--wl_break', default=cf.OptInfo.wl_break_default, show_default=True,
              help='flag to stop searching candidate wikilinks at the line in which nearest candidate link is found')
@click.option('--wl_lines_backward_max', '-wl_bmax', type=click.INT,
              default=cf.OptInfo.wl_lines_backward_max_default, show_default=True,
              help='maximum number of lines to backward-search wikipedia links in the page')
@click.option('--wl_lines_forward_max', '-wl_fmax', type=click.INT,
              default=cf.OptInfo.wl_lines_forward_max_default, show_default=True,
              help='maximum number of lines to forward-search wikipedia links in the page')
@click.option('--wl_lines_backward_ca', '-wl_bca', type=click.Choice(['f', 'r', 'fr',  'n']),
              default=cf.OptInfo.wl_lines_backward_ca_default, show_default=True,
              help='how to specify the maximum number to backward-search Wikipedia links for each category-attribute. '
                   'f: the number specified in f_wl_lines_backward_max_ca, r: the number estimated using the ratio '
                   'specified by wl_lines_backward_ca_ratio, fr: both f and r (f takes precedence), n: N/A')
@click.option('--wl_lines_forward_ca', '-wl_fca', type=click.Choice(['f', 'r', 'fr',  'n']),
              default=cf.OptInfo.wl_lines_forward_ca_default, show_default=True,
              help='how to specify the maximun number to forward-search Wikipedia links for each category-attribute. '
                   'f: the number specified in f_wl_lines_forward_max_ca, r: the number estimated using the ratio '
                   'specified by wl_lines_forward_ca_ratio, fr: both f and r (f takes precedence), n: N/A')
@click.option('--f_wl_lines_backward_ca', '-f_wl_bca', type=click.STRING,
              default=cf.DataInfo.f_wl_lines_backward_ca_default, show_default=True,
              help='the files to specify maximum number of line to backward-search Wikipedia links in the page for '
                   'each category-attribute pairs. Notice: The default file can be empty.')
@click.option('--f_wl_lines_forward_ca', '-f_wl_fca', type=click.STRING,
              default=cf.DataInfo.f_wl_lines_forward_ca_default, show_default=True,
              help='the files to specify maximum number of line to forward-search Wikipedia links in the page for each '
                   'category-attribute pairs. Notice: The default file can be empty.')
@click.option('--wl_lines_backward_ca_ratio', '-wl_bca_ratio', type=click.FLOAT,
              default=cf.OptInfo.wl_lines_backward_ca_ratio_default, show_default=True,
              help='maximum ratio of lines to backward-search wikipedia links in the page; the number of candidate'
                   'lines are estimated for each attribute using the sample data')
@click.option('--wl_lines_forward_ca_ratio', '-wl_fca_ratio', type=click.FLOAT,
              default=cf.OptInfo.wl_lines_forward_ca_ratio_default, show_default=True,
              help='maximum ratio of lines to forward-search wikipedia links in the page; the number of candidate'
                   'lines are estimated for each attribute using the sample data')
@click.option('--f_mention_gold_link_dist_info', default=cf.DataInfo.f_mention_gold_link_dist_info_default,
              show_default=True, type=click.STRING, help='f_mention_gold_link_dist_info')
# module: slink
@click.option('--slink_min', '-s_min', type=click.FLOAT,
              default=cf.OptInfo.slink_min_default, show_default=True,
              help='minimum self link ratio of attributes. (0.1-1.0)')
@click.option('--slink_prob', '-s_prb', type=click.Choice(['fixed', 'raw', 'mid']),
              default=cf.OptInfo.slink_prob_default, show_default=True,
              help='slink probability of the category-attribute pairs. fixed: 1.0, '
                   'raw: ratio based on the sample data, mid: average of fixed and raw')
@click.option('--f_slink', type=click.STRING,
              default=cf.DataInfo.f_slink_default, show_default=True,
              help='filename of self link ratio file. ')
# module: lp
@click.option('--lp_min', '-l_min', type=click.FLOAT,
              default=cf.OptInfo.lp_min_default, show_default=True,
              help='minimum category-attribute-mention link probability in the link prob file (f_link_prob). (0.1-1.0)')
@click.option('--f_link_prob', type=click.STRING,
              default=cf.DataInfo.f_link_prob_default, show_default=True,
              help='filename of link probability info file')
# filtering: incl
@click.option('--incl_max', '-i_max', type=click.INT,
              default=cf.OptInfo.incl_max_default, show_default=True,
              help='maximum number of filtering candidate pages using incoming links')
@click.option('--incl_tgt', '-i_tgt', type=click.STRING,
              default=cf.OptInfo.incl_tgt_default, show_default=True,
              help='target module of incoming link filtering,'
                   'specified as the combination of the following characters'
                   'm: mint, t: tinm, w: wlink, s: slink, l: link_prob, n: N/A')
@click.option('--incl_type', '-i_type', type=click.Choice(['o', 'f', 'a', 'n']),
              default=cf.OptInfo.incl_type_default, show_default=True,
              help='type of incoming link filtering,'
                   'o: ordering by number of incoming links (reciprocal ranking), '
                   'f: filtering (keep the original values unchanged), '
                   'a: adjust value based on ordering by number of incoming links, '
                   'n: N/A')
# filtering: attr
@click.option('--attr_range_tgt', '-ar_tgt', type=click.STRING,
              default=cf.OptInfo.attr_rng_tgt_default, show_default=True,
              help='target module of attribute range filtering, specified as the combination of '
                   'the following characters'
                   'm: mint, t: tinm, w: wlink, s: slink, l: link_prob, n: N/A')
@click.option('--f_attr_rng', type=click.STRING,
              default=cf.DataInfo.f_attr_rng_default, show_default=True,
              help='filename of attribute range definition file. The ranges are given as ENEIDs.')
@click.option('--f_enew_info', type=click.STRING,
              default=cf.DataInfo.f_enew_info_default, show_default=True,
              help='filename of enew_info_file.')
@click.option('--attr_na_co', '-anc', type=click.FLOAT,
              default=cf.OptInfo.attr_na_co_default, show_default=True,
              help='attr_na_co (base score (0.1-1.0) for candidate pages which are not given ENEW')
@click.option('--attr_ng_co', '-ang', type=click.FLOAT,
              default=cf.OptInfo.attr_ng_co_default, show_default=True,
              help='attr_ng_co (base score (0.1-1.0) for candidate pages which do not match attribute range')
@click.option('--attr_len', '-al', type=click.Choice(['a', 'r', 'ar', 'am', 'n']),
              default=cf.OptInfo.attr_len_default, show_default=True,
              help='scoring of the ENEID of candidate page on attribute range (eg. matching ratio between ENEIDs of '
                   'candidate pages and that of gold pages),'
                   'n: raw matching ratio,'
                   'a: adjusted matching ratio (adjusted matching ratio to ignore 1st layer of the ENE hierarchy if '
                   'the ENEID begins with 1 (Name)), '
                   'r: raw matching ratio + raw depth (# of layers in the ENE hierarchy) of ENEID of the gold page'
                   '(specified in the attribute range definition file), '
                   'ar: adjusted matching ratio + adjusted depth (adjusted to ignore 1st layer of the ENE hierarchy'
                   'if the ENEID begins with 1 (Name)),'
                   'am: adjusted matching ratio + modified depth (modify the adjusted depth to diminish its influence)')
# filtering: back_link
@click.option('--back_link_tgt', '-bl_tgt', type=click.STRING,
              default=cf.OptInfo.back_link_tgt_default, show_default=True,
              help='target module of back link filtering,'
                   'specified as the combination of the following characters'
                   'm: mint, t: tinm, w: wlink, s: slink, l: link_prob, n: N/A')
@click.option('--back_link_ng', '-bl_ng', type=click.FLOAT,
              default=cf.OptInfo.back_link_ng_default, show_default=True,
              help='score for not back link')
# ljc_main
def ljc_main(common_data_dir,
             tmp_data_dir,
             in_dir,
             out_dir,
             ans_max,
             attr_na_co,
             attr_ng_co,
             attr_len,
             attr_range_tgt,
             back_link_tgt,
             back_link_ng,
             char_match_cand_num_max,
             f_attr_rng,
             f_enew_info,
             f_html_info,
             f_mention_gold_link_dist_info,
             f_mint,
             f_mint_trim,
             f_slink,
             f_wl_lines_backward_ca,
             f_wl_lines_forward_ca,
             f_link_prob,
             f_tinm,
             f_tinm_trim,
             f_title2pid_ext,
             filtering,
             incl_max,
             incl_tgt,
             incl_type,
             lp_min,
             mint,
             mint_min,
             mod,
             mod_w,
             score_type,
             slink_min,
             slink_prob,
             tinm,
             tinm_min,
             title_matching_mint,
             title_matching_tinm,
             wlink,
             wl_break,
             wl_lines_backward_max,
             wl_lines_forward_max,
             wl_lines_backward_ca,
             wl_lines_forward_ca,
             wl_lines_backward_ca_ratio,
             wl_lines_forward_ca_ratio,
             wl_score_same,
             wl_score_backward,
             wl_score_forward,
             wr_score,
             wp_score,
             wf_score):
    '''

    :param common_data_dir: common data files directory
    :param tmp_data_dir: directory for data specifically used for the test data
    :param in_dir: input directory
    :param out_dir: output directory
    :param ans_max:
    :param attr_na_co:
    :param attr_ng_co:
    :param attr_len:
    :param attr_range_tgt:
    :param back_link_tgt:
    :param back_link_ng:
    :param char_match_cand_num_max:
    :param f_attr_rng:
    :param f_enew_info:
    :param f_html_info:
    :param f_mention_gold_link_dist_info:
    :param f_mint:
    :param f_mint_trim:
    :param f_slink:
    :param f_wl_lines_backward_ca:
    :param f_wl_lines_forward_ca:
    :param f_link_prob:
    :param f_tinm:
    :param f_tinm_trim:
    :param f_title2pid_ext:
    :param filtering:
    :param incl_max:
    :param incl_tgt:
    :param incl_type:
    :param lp_min:
    :param mint:
    :param mint_min:
    :param mod:
    :param mod_w:
    :param score_type:
    :param slink_min:
    :param slink_prob:
    :param tinm:
    :param tinm_min:
    :param title_matching_mint:
    :param title_matching_tinm:
    :param wlink:
    :param wl_break:
    :param wl_lines_backward_max:
    :param wl_lines_forward_max:
    :param wl_lines_backward_ca:
    :param wl_lines_forward_ca:
    :param wl_lines_backward_ca_ratio:
    :param wl_lines_forward_ca_ratio:
    :param wl_score_same:
    :param wl_score_backward:
    :param wl_score_forward:
    :param wr_score:
    :param wp_score:
    :param wf_score:
    :return:
    '''

    log_info = cf.LogInfo()
    logger = set_logging(log_info, 'myLogger')
    logger.setLevel(logging.INFO)

    opt_info = cf.OptInfo()
    opt_info.mod = mod
    opt_info.filtering = filtering
    opt_info.attr_range_tgt = attr_range_tgt
    opt_info.incoming_link_tgt = incl_tgt
    opt_info.back_link_tgt = back_link_tgt
    opt_info.back_link_ng = back_link_ng
    opt_info.mod_w = mod_w
    opt_info.ans_max = ans_max
    opt_info.title_matching_mint = title_matching_mint
    opt_info.title_matching_tinm = title_matching_tinm
    opt_info.char_match_cand_num_max = char_match_cand_num_max
    opt_info.mention_in_title = mint
    opt_info.mention_in_title_min = mint_min
    opt_info.wikilink = wlink
    opt_info.title_in_mention = tinm
    opt_info.title_in_mention_min = tinm_min
    opt_info.incoming_link_max = incl_max
    opt_info.incoming_link_type = incl_type
    opt_info.attr_len = attr_len
    opt_info.attr_na_co = attr_na_co
    opt_info.attr_ng_co = attr_ng_co
    opt_info.score_type = score_type
    opt_info.slink_min = slink_min
    opt_info.slink_prob = slink_prob
    opt_info.link_prob_min = lp_min
    opt_info.wl_break = wl_break
    opt_info.wl_lines_backward_ca = wl_lines_backward_ca
    opt_info.wl_lines_forward_ca = wl_lines_forward_ca
    opt_info.wl_lines_backward_ca_ratio = wl_lines_backward_ca_ratio
    opt_info.wl_lines_forward_ca_ratio = wl_lines_forward_ca_ratio
    opt_info.wl_lines_backward_max = wl_lines_backward_max
    opt_info.wl_lines_forward_max = wl_lines_forward_max
    opt_info.wl_score_same = wl_score_same
    opt_info.wl_score_backward = wl_score_backward
    opt_info.wl_score_forward = wl_score_forward
    opt_info.wp_score = wp_score
    opt_info.wr_score = wr_score
    opt_info.wf_score = wf_score
    logger.info({
        'action': 'ljc_main',
        'setting': 'opt_info',
        'mod': opt_info.mod,
        'filtering': opt_info.filtering,
        'mod_w': opt_info.mod_w,
        'ans_max': opt_info.ans_max,
        'score_type': opt_info.score_type,
    })
    logger.info({
        'char_match_cand_num_max': opt_info.char_match_cand_num_max,
        'mint': opt_info.mention_in_title,
        'mint_min': opt_info.mention_in_title_min,
        'tinm': opt_info.title_in_mention,
        'tinm_min': opt_info.title_in_mention_min
    })
    logger.info({
        'slink_prob': opt_info.slink_prob,
    })
    logger.info({
        'wlink': opt_info.wikilink,
        'wl_break': opt_info.wl_break,
        'wl_lines_backward_max': opt_info.wl_lines_backward_max,
        'wl_lines_forward_max': opt_info.wl_lines_forward_max,
        'wl_score_same': opt_info.wl_score_same,
        'wl_score_backward': opt_info.wl_score_backward,
        'wl_score_forward': opt_info.wl_score_forward,
        'wp_score': opt_info.wp_score,
        'wr_score': opt_info.wr_score,
        'wf_score': opt_info.wf_score
    })
    logger.info({
        'incl_max': opt_info.incoming_link_max,
        'incl_type': opt_info.incoming_link_type,
    })
    logger.info({
        'attr_len': opt_info.attr_len,
        'attr_na_co': opt_info.attr_na_co,
        'attr_ng_co': opt_info.attr_ng_co,
    })
    logger.info({
        'back_link_ng': opt_info.back_link_ng,
    })
    data_info = cf.DataInfo(common_data_dir, tmp_data_dir, in_dir, out_dir)
    # files in common data dir
    data_info.common_data_dir = common_data_dir
    data_info.attr_range_file = data_info.common_data_dir + f_attr_rng
    data_info.title2pid_ext_file = data_info.common_data_dir + f_title2pid_ext
    data_info.enew_info_file = data_info.common_data_dir + f_enew_info
    data_info.link_prob_file = data_info.common_data_dir + f_link_prob
    data_info.mention_gold_link_dist_info_file = data_info.common_data_dir + f_mention_gold_link_dist_info
    data_info.slink_file = data_info.common_data_dir + f_slink

    # files in tmp data dir
    data_info.tmp_data_dir = tmp_data_dir
    data_info.in_dir = in_dir
    data_info.out_dir = out_dir
    data_info.html_info_file = data_info.tmp_data_dir + f_html_info
    data_info.mint_partial_match_file = data_info.tmp_data_dir + f_mint
    data_info.mint_trim_partial_match_file = data_info.tmp_data_dir + f_mint_trim
    data_info.tinm_partial_match_file = data_info.tmp_data_dir + f_tinm
    data_info.tinm_trim_partial_match_file = data_info.tmp_data_dir + f_tinm_trim

    logger.info({
        'common_data_dir': data_info.common_data_dir,
        'tmp_data_dir': data_info.tmp_data_dir,
        'in_dir': data_info.in_dir,
        'out_dir': data_info.out_dir,
        'title2pid_ext_file': data_info.title2pid_ext_file,
    })

    in_files = in_dir + '*.json'
    os.makedirs(out_dir, exist_ok=True)

    logger.info({
        'action': 'ljc_main',
        'in_dir': in_dir,
        'out_dir': out_dir,
    })
    (cf.d_title2pid, cf.d_pid_title_incoming_eneid) = lc.reg_title2pid_ext(data_info.title2pid_ext_file, log_info)

    d_mint_mention_pid_ratio = {}
    d_tinm_mention_pid_ratio = {}
    d_cat_attr2eneid_prob = {}
    d_self_link = {}
    d_link_prob = {}
    d_back_link = {}
    # test
    # diff_info = {}

    # mint
    if (opt_info.mention_in_title == 'e' or opt_info.mention_in_title == 'p') and 'm' not in opt_info.mod:
        logger.error({
            'action': 'ljc_main',
            'error': 'mod m should be specified'
        })
        sys.exit()
    elif (opt_info.title_matching_mint == 'trim') and 'm' not in opt_info.mod:
        logger.error({
            'action': 'ljc_main',
            'error': 'mod m should be specified (trim, non-default)'
        })
        sys.exit()

    elif 'm' in opt_info.mod:
        if opt_info.mention_in_title != 'e' and opt_info.mention_in_title != 'p':
            logger.error({
                'action': 'ljc_main',
                'missing or illegal mint value': opt_info.mention_in_title
            })
            sys.exit()

        elif not opt_info.title_matching_mint:
            logger.error({
                'action': 'ljc_main',
                'missing title matching mint': 'Specify title matching as option (--title matching mint / -tmm)'
            })
            sys.exit()
        else:
            if opt_info.title_matching_mint == 'trim':
                logger.info({
                    'action': 'ljc_main',
                    'run': 'reg_matching_info',
                    'title_matching_mint': opt_info.title_matching_mint,
                    'partial_match_file': data_info.mint_trim_partial_match_file,
                    'mention_in_title_min': opt_info.mention_in_title_min
                })
                d_mint_mention_pid_ratio = mc.reg_matching_info(data_info.mint_trim_partial_match_file,
                                                                opt_info.mention_in_title_min, log_info)

            elif opt_info.title_matching_mint == 'full':
                logger.info({
                    'action': 'ljc_main',
                    'run': 'reg_matching_info',
                    'title_matching_mint': opt_info.title_matching_mint,
                    'partial_match_file': data_info.mint_partial_match_file,
                    'mention_in_title_min': opt_info.mention_in_title_min
                })
                d_mint_mention_pid_ratio = mc.reg_matching_info(data_info.mint_partial_match_file,
                                                                opt_info.mention_in_title_min, log_info)
            else:
                logger.error({
                    'action': 'ljc_main',
                    'error': 'illegal title_matching_mint value'
                })
                sys.exit()
    # tinm
    if (opt_info.title_in_mention == 'e' or opt_info.title_in_mention == 'p') and 't' not in opt_info.mod:
        logger.error({
            'action': 'ljc_main',
            'error': 'mod t should be specified'
        })
        sys.exit()
    elif (opt_info.title_matching_tinm == 'trim') and 't' not in opt_info.mod:
        logger.error({
            'action': 'ljc_main',
            'error': 'mod t should be specified (trim, non-default)'
        })
        sys.exit()
    elif 't' in opt_info.mod:
        if opt_info.title_in_mention != 'e' and opt_info.title_in_mention != 'p':
            logger.error({
                'action': 'ljc_main',
                'missing or illegal tinm value': opt_info.title_in_mention_min
            })
            sys.exit()
        elif not opt_info.title_matching_tinm:
            logger.error({
                'action': 'ljc_main',
                'missing title matching trim': 'Specify title matching as option (--title matching trim/ -tmt)'
            })
            sys.exit()
        else:
            if opt_info.title_matching_tinm == 'trim':
                logger.info({
                    'action': 'ljc_main',
                    'run': 'mc.reg_matching_info',
                    'title_matching_tinm': opt_info.title_matching_tinm,
                    'partial_match_file': data_info.tinm_trim_partial_match_file,
                    'mention_in_title_min': opt_info.title_in_mention_min
                })
                d_tinm_mention_pid_ratio = mc.reg_matching_info(data_info.tinm_trim_partial_match_file,
                                                                opt_info.title_in_mention_min, log_info)

            elif opt_info.title_matching_tinm == 'full':
                logger.info({
                    'action': 'ljc_main',
                    'run': 'mc.reg_matching_info',
                    'title_matching_tinm': opt_info.title_matching_tinm,
                    'partial_match_file': data_info.tinm_partial_match_file,
                    'mention_in_title_min': opt_info.title_in_mention_min
                })
                d_tinm_mention_pid_ratio = mc.reg_matching_info(data_info.tinm_partial_match_file,
                                                                opt_info.title_in_mention_min, log_info)
            else:
                logger.error({
                    'action': 'ljc_main',
                    'error': 'illegal title_matching_tinm value'
                })
                sys.exit()

    # wikilink
    if ('r' in opt_info.wikilink
            or 'f' in opt_info.wikilink
            or 'm' in opt_info.wikilink
            or 'p' in opt_info.wikilink
            or 'l' in opt_info.wikilink) and 'w' not in opt_info.mod:
        logger.error({
            'action': 'ljc_main',
            'error': 'mod w should be specified'
        })
        sys.exit()
    elif 'w' in opt_info.mod:
        if ('r' not in opt_info.wikilink
                and 'f' not in opt_info.wikilink
                and 'm' not in opt_info.wikilink
                and 'p' not in opt_info.wikilink
                and 'l' not in opt_info.wikilink):
            logger.error({
                'action': 'ljc_main',
                'illegal wlink value': opt_info.wikilink
            })
            sys.exit()
        else:
            logger.info({
                'action': 'ljc_main',
                'run': 'gw.reg_tag_info',
                'wikilink': opt_info.wikilink,
                'html_info_file': data_info.html_info_file,
            })
        cf.d_tag_info = gw.reg_tag_info(data_info.html_info_file, log_info)

        if 'r' in opt_info.wl_lines_backward_ca or 'r' in opt_info.wl_lines_forward_ca:
            logger.info({
                'action': 'ljc_main',
                'run': 'gw.reg_mention_gold_distance',
                'dist_file': data_info.mention_gold_link_dist_file,
                'dist_info_file': data_info.mention_gold_link_dist_info_file
            })

            diff_info = gw.reg_mention_gold_distance(data_info.mention_gold_link_dist_file, opt_info,
                                                     data_info.mention_gold_link_dist_info_file, log_info)

        if 'f' in opt_info.wl_lines_backward_ca:
            data_info.wl_lines_backward_ca_file = data_info.common_data_dir + f_wl_lines_backward_ca
            if not os.path.isfile(data_info.wl_lines_backward_ca_file):
                logger.error({
                    'action': 'ljc_main',
                    'error': 'file not found',
                    'file': data_info.wl_lines_backward_ca_file
                })
            cf.diff_info_ca_backward = gw.reg_mention_gold_distance_ca(data_info.wl_lines_backward_ca_file, log_info)
        if 'f' in opt_info.wl_lines_forward_ca:
            data_info.wl_lines_forward_ca_file = data_info.common_data_dir + f_wl_lines_forward_ca
            if not os.path.isfile(data_info.wl_lines_forward_ca_file):
                logger.error({
                    'action': 'ljc_main',
                    'error': 'file not found',
                    'file': data_info.wl_lines_forward_ca_file
                })
            cf.diff_info_ca_forward = gw.reg_mention_gold_distance_ca(data_info.wl_lines_forward_ca_file, log_info)
    # slink
    if opt_info.slink_prob == 'raw' and 's' not in opt_info.mod:
        logger.error({
            'action': 'ljc_main',
            'mod': 'missing mod s (slink_prob is specified)'
        })
        sys.exit()
    elif 's' in opt_info.mod:
        logger.info({
            'action': 'ljc_main',
            'run': 'sl.check_slink_info',
            'slink_min': opt_info.slink_min,
            'slink_file': data_info.slink_file,
        })
        d_self_link = sl.check_slink_info(data_info.slink_file, opt_info.slink_min, log_info)

    # link_prob
    if 'l' in opt_info.mod:
        logger.info({
            'action': 'ljc_main',
            'run': 'lp.get_link_prob_info',
            'link_prob_min': opt_info.link_prob_min,
            'link_prob_file': data_info.link_prob_file
        })
        d_link_prob = lp.get_link_prob_info(data_info.link_prob_file, opt_info.link_prob_min, log_info)

    # incoming_link
    if ('m' in opt_info.incoming_link_tgt or
        't' in opt_info.incoming_link_tgt or
        'w' in opt_info.incoming_link_tgt or
        's' in opt_info.incoming_link_tgt or
        'l' in opt_info.incoming_link_tgt) \
            and 'i' not in opt_info.filtering:
        logger.error({
            'action': 'ljc_main',
            'incl_target': 'missing filtering option (i)'
        })
        sys.exit()

    elif ('o' in opt_info.incoming_link_type or
          'f' in opt_info.incoming_link_type or
          'a' in opt_info.incoming_link_type) \
            and 'i' not in opt_info.filtering:
        logger.error({
            'action': 'ljc_main',
            'backlink': 'missing filtering option (i)'
        })
        sys.exit()
    elif 'i' in opt_info.filtering:
        if not opt_info.incoming_link_tgt:
            logger.error({
                'action': 'ljc_main',
                'filterning': opt_info.filtering,
                'missing incoming_link_tgt': 'opt_info.incoming_link_tgt should be specified'
            })
            sys.exit()
        elif ('m' not in opt_info.incoming_link_tgt and
              't' not in opt_info.incoming_link_tgt and
              'w' not in opt_info.incoming_link_tgt and
              's' not in opt_info.incoming_link_tgt and
              'l' not in opt_info.incoming_link_tgt):
            logger.error({
                'action': 'ljc_main',
                'filtering': opt_info.filtering,
                'illegal incoming_link_tgt': 'illegal opt_info.incoming_link_tgt'
            })
            sys.exit()
        elif ('o' not in opt_info.incoming_link_type and
              'f' not in opt_info.incoming_link_type and
              'a' not in opt_info.incoming_link_type):
            logger.error({
                'action': 'ljc_main',
                'filtering': opt_info.filtering,
                'missing incoming_link_type': 'opt_info.incoming_link_type should be specified'
            })
            sys.exit()
        else:
            logger.info({
                'action': 'ljc_main',
                'filtering': opt_info.filtering,
                'incoming_link_tgt': opt_info.incoming_link_tgt,
                'incoming_link_max': opt_info.incoming_link_max,
            })

    # back_link
    if ('m' in opt_info.back_link_tgt or
        't' in opt_info.back_link_tgt or
        'w' in opt_info.back_link_tgt or
        's' in opt_info.back_link_tgt or
        'l' in opt_info.back_link_tgt) \
            and 'b' not in opt_info.filtering:
        logger.error({
            'action': 'ljc_main',
            'backlink': 'missing filtering option (back link tgt is specified)'
        })
        sys.exit()

    elif 'b' in opt_info.filtering:
        if not opt_info.back_link_tgt:
            logger.error({
                'action': 'ljc_main',
                'filtering': opt_info.filtering,
                'missing back_link_tgt': 'opt_info.back_link_tgt should be specified'
            })
            sys.exit()
        elif ('m' not in opt_info.back_link_tgt and
              't' not in opt_info.back_link_tgt and
              'w' not in opt_info.back_link_tgt and
              's' not in opt_info.back_link_tgt and
              'l' not in opt_info.back_link_tgt):
            logger.error({
                'action': 'ljc_main',
                'filtering': opt_info.filtering,
                'illegal backlink_tgt': 'illegal opt_info.back_link_tgt'
            })
            sys.exit()
        else:
            logger.info({
                'action': 'ljc_main',
                'filtering': opt_info.filtering,
                'back_link_tgt': opt_info.back_link_tgt
            })
            data_info.back_link_file = tmp_data_dir + cf.DataInfo.f_back_link_default
            d_back_link = bl.check_back_link_info(data_info.back_link_file, log_info, **cf.d_title2pid)

    # attr_range
    if ('m' in opt_info.attr_range_tgt or
        't' in opt_info.attr_range_tgt or
        'w' in opt_info.attr_range_tgt or
        's' in opt_info.attr_range_tgt or
        'l' in opt_info.attr_range_tgt) \
            and 'a' not in opt_info.filtering:
        logger.error({
            'action': 'ljc_main',
            'option combination error': 'attr_range_tgt is set, but missing filtering option a'
        })
        sys.exit()
    elif 'a' in opt_info.filtering:
        if not opt_info.attr_range_tgt:
            logger.error({
                'action': 'ljc_main',
                'missing attr_range_tgt': 'attr is specified, but missing attr_range_tgt'
            })
            sys.exit()
        elif ('m' not in opt_info.attr_range_tgt and
              't' not in opt_info.attr_range_tgt and
              'w' not in opt_info.attr_range_tgt and
              's' not in opt_info.attr_range_tgt and
              'l' not in opt_info.attr_range_tgt):
            logger.error({
                'action': 'ljc_main',
                'illegal attr_range_tgt': 'attr is specified, but illegal attr_range_tgt'
            })
            sys.exit()
        else:
            logger.info({
                'action': 'ljc_main',
                'attr_range_tgt': opt_info.attr_range_tgt,
                'attr_range_file': data_info.attr_range_file,
                'enew_info_file:': data_info.enew_info_file,
            })
            cf.d_pid2eneid = ar.reg_enew_info(data_info.enew_info_file, log_info)
            d_cat_attr2eneid_prob = ar.get_attr_range(data_info.attr_range_file, opt_info, log_info)

    for in_file in glob(in_files):
        list_rec_out = []

        with open(in_file, mode='r', encoding='utf-8') as i:
            fname = in_file.replace(in_dir, '')
            ene_cat = fname.replace('.json', '')
            outfile = out_dir + fname
            logger.info({
                'action': 'ljc_main',
                'ene_cat': ene_cat,
                'in_file': in_file,
                'outfile': outfile
            })

            for i_line in i:
                rec = json.loads(i_line)
                check_t = 0
                check_m = 0
                check_s = 0
                check_l = 0
                check_w = 0
                check_i = 0
                check_a = 0

                link_info = cf.LinkInfo('linfo')

                mention_info = cf.MentionInfo(
                    rec['page_id'],
                    ene_cat,
                    rec['attribute'],
                    rec['text_offset']['start']['line_id'],
                    rec['text_offset']['start']['offset'],
                    rec['text_offset']['end']['line_id'],
                    rec['text_offset']['end']['offset'],
                    rec['text_offset']['text'],
                    rec['html_offset']['start']['line_id'],
                    rec['html_offset']['start']['offset'],
                    rec['html_offset']['end']['line_id'],
                    rec['html_offset']['end']['offset'],
                    rec['html_offset']['text'],
                    ''
                )

                mod_info = cf.ModInfo()
                cat_attr = mention_info.ene_cat + ':' + mention_info.attr_label

                # modules (+ filtering)
                # wlink
                if 'w' in opt_info.mod:

                    wlink_cand_list = gw.check_wlink(mention_info, opt_info, log_info, **diff_info)

                    # filtering
                    if wlink_cand_list:
                        w_tmp_cand_list = copy.deepcopy(wlink_cand_list)
                        if 'a' in opt_info.filtering and 'w' in opt_info.attr_range_tgt:
                            wlink_cand_list_attr_checked = ar.filter_by_attr_range(w_tmp_cand_list,
                                                                                   mention_info,
                                                                                   opt_info,
                                                                                   log_info,
                                                                                   **d_cat_attr2eneid_prob)
                            w_tmp_cand_list = copy.deepcopy(wlink_cand_list_attr_checked)
                        if 'i' in opt_info.filtering and 'w' in opt_info.incoming_link_tgt:
                            wlink_cand_list_incl_checked = il.filter_by_incoming_link(w_tmp_cand_list,
                                                                                      mention_info,
                                                                                      opt_info.incoming_link_max,
                                                                                      opt_info.incoming_link_type,
                                                                                      log_info,
                                                                                      **cf.d_pid_title_incoming_eneid)
                            w_tmp_cand_list = copy.deepcopy(wlink_cand_list_incl_checked)
                        if 'b' in opt_info.filtering and 'w' in opt_info.back_link_tgt:
                            wlink_cand_list_back_link_checked = bl.filter_by_back_link(w_tmp_cand_list,
                                                                                       opt_info,
                                                                                       mention_info,
                                                                                       log_info,
                                                                                       **d_back_link)
                            w_tmp_cand_list = copy.deepcopy(wlink_cand_list_back_link_checked)

                        # filtered candidates
                        if w_tmp_cand_list:
                            cl.append_filtering_cand_info(w_tmp_cand_list, link_info, log_info)
                            check_w = 1

                # slink
                if 's' in opt_info.mod:
                    s_tmp_cand_list = []
                    slink_cand_list = sl.estimate_self_link(cat_attr, opt_info.slink_prob, mention_info, log_info,
                                                            **d_self_link)
                    if slink_cand_list:
                        s_tmp_cand_list = copy.deepcopy(slink_cand_list)

                        # filtering
                        if 'a' in opt_info.filtering and 's' in opt_info.attr_range_tgt:
                            slink_cand_list_attr_checked = ar.filter_by_attr_range(s_tmp_cand_list,
                                                                                   mention_info,
                                                                                   opt_info,
                                                                                   log_info,
                                                                                   **d_cat_attr2eneid_prob)
                            s_tmp_cand_list = copy.deepcopy(slink_cand_list_attr_checked)
                        if 'i' in opt_info.filtering and 's' in opt_info.incoming_link_tgt:
                            slink_cand_list_incl_checked = il.filter_by_incoming_link(s_tmp_cand_list,
                                                                                      mention_info,
                                                                                      opt_info.incoming_link_max,
                                                                                      opt_info.incoming_link_type,
                                                                                      log_info,
                                                                                      **cf.d_pid_title_incoming_eneid)
                            s_tmp_cand_list = copy.deepcopy(slink_cand_list_incl_checked)

                        if 'b' in opt_info.filtering and 's' in opt_info.back_link_tgt:
                            slink_cand_list_back_link_checked = bl.filter_by_back_link(s_tmp_cand_list,
                                                                                       opt_info,
                                                                                       mention_info,
                                                                                       log_info,
                                                                                       **d_back_link)
                            s_tmp_cand_list = copy.deepcopy(slink_cand_list_back_link_checked)

                        # filtered candidates
                        if s_tmp_cand_list:
                            cl.append_filtering_cand_info(s_tmp_cand_list, link_info, log_info)
                            check_s = 1
                # mint
                if 'm' in opt_info.mod:
                    m_tmp_cand_list = []
                    mod = 'm'
                    mint_cand_list = mc.match_mention_title(mod, opt_info, mention_info.t_mention, log_info,
                                                            **d_mint_mention_pid_ratio)
                    # filtering
                    if mint_cand_list:
                        m_tmp_cand_list = copy.deepcopy(mint_cand_list)
                        if 'a' in opt_info.filtering and 'm' in opt_info.attr_range_tgt:
                            mint_cand_list_attr_checked = ar.filter_by_attr_range(m_tmp_cand_list,
                                                                                  mention_info,
                                                                                  opt_info,
                                                                                  log_info,
                                                                                  **d_cat_attr2eneid_prob)
                            m_tmp_cand_list = copy.deepcopy(mint_cand_list_attr_checked)
                        if 'i' in opt_info.filtering and 'm' in opt_info.incoming_link_tgt:
                            mint_cand_list_incl_checked = il.filter_by_incoming_link(m_tmp_cand_list,
                                                                                     mention_info,
                                                                                     opt_info.incoming_link_max,
                                                                                     opt_info.incoming_link_type,
                                                                                     log_info,
                                                                                     **cf.d_pid_title_incoming_eneid)
                            m_tmp_cand_list = copy.deepcopy(mint_cand_list_incl_checked)
                        if 'b' in opt_info.filtering and 'm' in opt_info.back_link_tgt:
                            mint_cand_list_back_link_checked = bl.filter_by_back_link(m_tmp_cand_list,
                                                                                      opt_info,
                                                                                      mention_info,
                                                                                      log_info,
                                                                                      **d_back_link)
                            m_tmp_cand_list = copy.deepcopy(mint_cand_list_back_link_checked)

                        # filtered candidates
                        if m_tmp_cand_list:
                            cl.append_filtering_cand_info(m_tmp_cand_list, link_info, log_info)
                            check_m = 1

                # tinm
                if 't' in opt_info.mod:
                    t_tmp_cand_list = []
                    mod = 't'
                    tinm_cand_list = mc.match_mention_title(mod, opt_info, mention_info.t_mention, log_info,
                                                            **d_tinm_mention_pid_ratio)

                    # filtering
                    if tinm_cand_list:
                        t_tmp_cand_list = copy.deepcopy(tinm_cand_list)
                        if 'a' in opt_info.filtering and 't' in opt_info.attr_range_tgt:
                            tinm_cand_list_attr_checked = ar.filter_by_attr_range(t_tmp_cand_list,
                                                                                  mention_info,
                                                                                  opt_info,
                                                                                  log_info,
                                                                                  **d_cat_attr2eneid_prob)
                            t_tmp_cand_list = copy.deepcopy(tinm_cand_list_attr_checked)
                        if 'i' in opt_info.filtering and 't' in opt_info.incoming_link_tgt:
                            tinm_cand_list_incl_checked = il.filter_by_incoming_link(t_tmp_cand_list,
                                                                                     mention_info,
                                                                                     opt_info.incoming_link_max,
                                                                                     opt_info.incoming_link_type,
                                                                                     log_info,
                                                                                     **cf.d_pid_title_incoming_eneid)
                            t_tmp_cand_list = copy.deepcopy(tinm_cand_list_incl_checked)

                        if 'b' in opt_info.filtering and 't' in opt_info.back_link_tgt:
                            tinm_cand_list_back_link_checked = bl.filter_by_back_link(t_tmp_cand_list,
                                                                                      opt_info,
                                                                                      mention_info,
                                                                                      log_info,
                                                                                      **d_back_link)
                            t_tmp_cand_list = copy.deepcopy(tinm_cand_list_back_link_checked)

                        # filtered candidates
                        if t_tmp_cand_list:
                            cl.append_filtering_cand_info(t_tmp_cand_list, link_info, log_info)
                            check_t = 1
                # link prob
                if 'l' in opt_info.mod:
                    l_tmp_cand_list = []
                    lp_cand_list = lp.check_link_prob(opt_info.link_prob_min, mention_info, log_info, **d_link_prob)

                    # filtering
                    if lp_cand_list:
                        l_tmp_cand_list = copy.deepcopy(lp_cand_list)
                        if 'a' in opt_info.filtering and 'l' in opt_info.attr_range_tgt:
                            lp_cand_list_attr_checked = ar.filter_by_attr_range(l_tmp_cand_list,
                                                                                mention_info,
                                                                                opt_info,
                                                                                log_info,
                                                                                **d_cat_attr2eneid_prob)
                            l_tmp_cand_list = copy.deepcopy(lp_cand_list_attr_checked)

                        if 'i' in opt_info.filtering and 'l' in opt_info.incoming_link_tgt:
                            lp_cand_list_incl_checked = il.filter_by_incoming_link(l_tmp_cand_list,
                                                                                   mention_info,
                                                                                   opt_info.incoming_link_max,
                                                                                   opt_info.incoming_link_type,
                                                                                   log_info,
                                                                                   **cf.d_pid_title_incoming_eneid)
                            l_tmp_cand_list = copy.deepcopy(lp_cand_list_incl_checked)

                        if 'b' in opt_info.filtering and 'l' in opt_info.back_link_tgt:
                            lp_cand_list_back_link_checked = bl.filter_by_back_link(l_tmp_cand_list,
                                                                                    opt_info,
                                                                                    mention_info,
                                                                                    log_info,
                                                                                    **d_back_link)
                            l_tmp_cand_list = copy.deepcopy(lp_cand_list_back_link_checked)

                        # filtered candidates
                        if l_tmp_cand_list:
                            cl.append_filtering_cand_info(l_tmp_cand_list, link_info, log_info)
                            check_l = 1

                # scoring link candidates for tmp mention
                final_cand_list = gs.scoring(opt_info, link_info, mention_info, mod_info, log_info)

                # add the results of scoring to answer list
                final_cand_cnt = 0
                for final_cand in final_cand_list:
                    rec['link_page_id'] = final_cand[0]
                    ext_title = ''
                    try:
                        ext_title = cf.d_pid_title_incoming_eneid[final_cand[0]][0]
                    except (KeyError, ValueError) as e:
                        logger.warning({
                            'action': 'scoring',
                            'pid': mention_info.pid,
                            'mention': mention_info.t_mention,
                            'error': e,
                        })
                    list_rec_out.append(copy.deepcopy(rec))
                    final_cand_cnt += 1
                    if final_cand_cnt == opt_info.ans_max:
                        break

        with open(outfile, mode='w', encoding='utf-8') as o:
            for tline in list_rec_out:
                json.dump(tline, o, ensure_ascii=False)
                o.write('\n')


if __name__ == '__main__':
    ljc_main()
