from glob import glob
import json
import click
import config as cf
import csv
from decimal import Decimal, ROUND_HALF_UP
import logging
import logging.config
import sys


def set_logging_pre(log_info, logger_name):
    from os import path

    logging_ini = log_info.logging_ini
    log_file_path = path.join(path.dirname(path.abspath(__file__)), logging_ini)
    logging.config.fileConfig(log_file_path)

    logger = logging.getLogger(logger_name)
    return logger


@click.command()
@click.argument('common_data_dir', type=click.Path(exists=True))
@click.argument('tmp_data_dir', type=click.Path(exists=True))
@click.argument('in_dir', type=click.Path(exists=True))
@click.argument('sample_gold_dir', type=click.Path(exists=True))
@click.argument('sample_input_dir', type=click.Path(exists=True))
@click.option('--gen_sample_gold_tsv', is_flag=True, default=False, show_default=True)
@click.option('--gen_redirect', is_flag=True, default=False, show_default=True)
@click.option('--pre_matching', type=click.Choice(['mint', 'tinm', 'n']), default=cf.OptInfo.pre_matching_default,
              show_default=True)
@click.option('--title_matching_mint', '-tmm', type=click.Choice(['trim', 'full']),
              default=cf.OptInfo.title_matching_mint_default, show_default=True)
@click.option('--title_matching_tinm', '-tmt', type=click.Choice(['trim', 'full']),
              default=cf.OptInfo.title_matching_tinm_default, show_default=True)
@click.option('--char_match_min', default=cf.OptInfo.char_match_min_default, show_default=True, type=click.FLOAT)
@click.option('--gen_title2pid_ext', is_flag=True, default=False, show_default=True)
@click.option('--gen_html', is_flag=True, default=False, show_default=True)
@click.option('--gen_common_html', is_flag=True, default=False, show_default=True)
@click.option('--gen_link_prob', is_flag=True, default=False, show_default=True)
@click.option('--gen_linkable', is_flag=True, default=False, show_default=True)
@click.option('--gen_slink', is_flag=True, default=False, show_default=True)
@click.option('--gen_back_link', is_flag=True, default=False, show_default=True)
@click.option('--gen_link_dist', is_flag=True, default=False, show_default=True)
@click.option('--gen_incoming_link', is_flag=True, default=False, show_default=True)
@click.option('--f_title2pid_ext', default=cf.DataInfo.f_title2pid_ext_default, show_default=True, type=click.STRING,
              help='from_title_to_pageid_extended_information. Filter out disambiguation, management, '
                   'or format-error pages, and add eneid, incoming link num info.')
@click.option('--f_title2pid_org', default=cf.DataInfo.f_title2pid_org_default, show_default=True, type=click.STRING,
              help='from_title_to_pageid_information_original.')
@click.option('--f_cirrus_content', default=cf.DataInfo.f_cirrus_content_default, show_default=True, type=click.STRING,
              help='cirrus dump (content) (.')
@click.option('--f_disambiguation', default=cf.DataInfo.f_disambiguation_default, show_default=True, type=click.STRING,
              help='disambiguation page list.')
@click.option('--f_disambiguation_pat', default=cf.DataInfo.f_disambiguation_pat_default, show_default=True,
              type=click.STRING, help='disambiguation pattern file.')
@click.option('--f_mint_partial', default=cf.DataInfo.f_mint_partial_default, show_default=True, type=click.STRING,
              help='mint_partial')
@click.option('--f_mint_trim_partial', default=cf.DataInfo.f_mint_trim_partial_default, show_default=True,
              type=click.STRING, help='mint_trim_partial')
@click.option('--f_tinm_partial', default=cf.DataInfo.f_tinm_partial_default, show_default=True, type=click.STRING,
              help='tinm_partial')
@click.option('--f_tinm_trim_partial', default=cf.DataInfo.f_tinm_trim_partial_default, show_default=True,
              type=click.STRING, help='tinm_trim_partial')
@click.option('--f_common_html_info', default=cf.DataInfo.f_common_html_info_default, show_default=True,
              type=click.STRING, help='html_info_file')
@click.option('--f_html_info', default=cf.DataInfo.f_html_info_default, show_default=True, type=click.STRING,
              help='html_info_file')
@click.option('--f_redirect_info', default=cf.DataInfo.f_redirect_info_default, show_default=True, type=click.STRING,
              help='f_redirect_info')
@click.option('--f_enew_info', default=cf.DataInfo.f_enew_info_default, show_default=True, type=click.STRING,
              help='f_enew_info')
@click.option('--f_enew_org', default=cf.DataInfo.f_enew_org_default, show_default=True, type=click.STRING,
              help='f_enew_org')
@click.option('--f_enew_mod_list', default=cf.DataInfo.f_enew_mod_list_default, show_default=True, type=click.STRING,
              help='f_enew_mod_list')
@click.option('--f_incoming', default=cf.DataInfo.f_incoming_default, show_default=True, type=click.STRING,
              help='f_incoming')
@click.option('--f_link_prob', default=cf.DataInfo.f_link_prob_default, show_default=True, type=click.STRING,
              help='f_link_prob')
@click.option('--f_linkable_info', type=click.STRING,
              default=cf.DataInfo.f_linkable_info_default, show_default=True,
              help='filename of linkable ratio info file.')
@click.option('--f_slink', default=cf.DataInfo.f_slink_default, show_default=True, type=click.STRING,
              help='f_slink')
@click.option('--f_input_title', default=cf.DataInfo.f_input_title_default, show_default=True, type=click.STRING,
              help='f_input_title')
@click.option('--f_back_link', default=cf.DataInfo.f_back_link_default, show_default=True, type=click.STRING,
              help='f_back_link')
@click.option('--f_back_link_dump', default=cf.DataInfo.f_back_link_dump_default, show_default=True, type=click.STRING,
              help='f_back_link_dump')
@click.option('--f_mention_gold_link_dist', default=cf.DataInfo.f_mention_gold_link_dist_default, show_default=True,
              type=click.STRING, help='f_mention_gold_link_dist')
def ljc_prep_main(common_data_dir,
                  tmp_data_dir,
                  in_dir,
                  sample_gold_dir,
                  sample_input_dir,
                  char_match_min,
                  gen_back_link,
                  gen_common_html,
                  gen_html,
                  gen_incoming_link,
                  gen_linkable,
                  gen_link_dist,
                  gen_link_prob,
                  gen_slink,
                  gen_title2pid_ext,
                  gen_sample_gold_tsv,
                  pre_matching,
                  gen_redirect,
                  title_matching_mint,
                  title_matching_tinm,
                  f_back_link,
                  f_back_link_dump,
                  f_cirrus_content,
                  f_common_html_info,
                  f_disambiguation,
                  f_disambiguation_pat,
                  f_enew_info,
                  f_enew_mod_list,
                  f_enew_org,
                  f_html_info,
                  f_incoming,
                  f_input_title,
                  f_linkable_info,
                  f_link_prob,
                  f_mention_gold_link_dist,
                  f_mint_partial,
                  f_mint_trim_partial,
                  f_redirect_info,
                  f_slink,
                  f_tinm_partial,
                  f_tinm_trim_partial,
                  f_title2pid_ext,
                  f_title2pid_org):
    class DataInfoPrep(object):
        def __init__(self,
                     prep_common_data_dir,
                     prep_tmp_data_dir,
                     prep_in_dir,
                     prep_sample_gold_dir,
                     prep_sample_input_dir,
                     prep_f_back_link=f_back_link,
                     prep_f_back_link_dump=f_back_link_dump,
                     prep_f_cirrus_content=f_cirrus_content,
                     prep_f_common_html_info=f_common_html_info,
                     prep_f_disambiguation=f_disambiguation,
                     prep_f_disambiguation_pat=f_disambiguation_pat,
                     prep_f_enew_info=f_enew_info,
                     prep_f_enew_mod_list=f_enew_mod_list,
                     prep_f_enew_org=f_enew_org,
                     prep_f_html_info=f_html_info,
                     prep_f_incoming=f_incoming,
                     prep_f_input_title=f_input_title,
                     prep_f_linkable=f_linkable_info,
                     prep_f_link_prob=f_link_prob,
                     prep_f_mention_gold_link_dist=f_mention_gold_link_dist,
                     prep_f_mint_partial=f_mint_partial,
                     prep_f_mint_trim_partial=f_mint_trim_partial,
                     prep_f_redirect_info=f_redirect_info,
                     prep_f_slink=f_slink,
                     prep_f_tinm_partial=f_tinm_partial,
                     prep_f_tinm_trim_partial=f_tinm_trim_partial,
                     prep_f_title2pid_ext=f_title2pid_ext,
                     prep_f_title2pid_org=f_title2pid_org):
            self.common_data_dir = prep_common_data_dir
            self.tmp_data_dir = prep_tmp_data_dir
            self.in_dir = prep_in_dir
            self.sample_gold_dir = prep_sample_gold_dir
            self.sample_input_dir = prep_sample_input_dir
            self.back_link_file = prep_tmp_data_dir + prep_f_back_link
            self.back_link_dump_file = prep_common_data_dir + prep_f_back_link_dump
            self.cirrus_content_file = prep_common_data_dir + prep_f_cirrus_content
            self.disambiguation_file = prep_common_data_dir + prep_f_disambiguation
            self.disambiguation_pat_file = prep_common_data_dir + prep_f_disambiguation_pat
            self.enew_info_file = prep_common_data_dir + prep_f_enew_info
            self.enew_mod_list_file = prep_common_data_dir + prep_f_enew_mod_list
            self.enew_org_file = prep_common_data_dir + prep_f_enew_org
            self.common_html_info_file = prep_common_data_dir + prep_f_common_html_info
            self.incoming_file = prep_common_data_dir + prep_f_incoming
            self.linkable_file = prep_common_data_dir + prep_f_linkable
            self.link_prob_file = prep_common_data_dir + prep_f_link_prob
            self.mention_gold_link_dist_file = prep_common_data_dir + prep_f_mention_gold_link_dist
            self.title2pid_ext_file = prep_common_data_dir + prep_f_title2pid_ext
            self.title2pid_org_file = prep_common_data_dir + prep_f_title2pid_org
            self.redirect_info_file = prep_common_data_dir + prep_f_redirect_info
            self.slink_file = prep_common_data_dir + prep_f_slink
            self.html_info_file = prep_tmp_data_dir + prep_f_html_info
            self.input_title_file = prep_tmp_data_dir + prep_f_input_title
            self.mint_partial_file = prep_tmp_data_dir + prep_f_mint_partial
            self.mint_trim_partial_file = prep_tmp_data_dir + prep_f_mint_trim_partial
            self.tinm_partial_file = prep_tmp_data_dir + prep_f_tinm_partial
            self.tinm_trim_partial_file = prep_tmp_data_dir + prep_f_tinm_trim_partial
    csv.field_size_limit(1000000000)
    log_info = cf.LogInfo()
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    data_info_prep = DataInfoPrep(common_data_dir, tmp_data_dir, in_dir, sample_gold_dir, sample_input_dir)

    # common_data_dir
    data_info_prep.back_link_dump_file = data_info_prep.common_data_dir + f_back_link_dump
    data_info_prep.cirrus_content_file = data_info_prep.common_data_dir + f_cirrus_content
    data_info_prep.disambiguation_file = data_info_prep.common_data_dir + f_disambiguation
    data_info_prep.disambiguation_pat_file = data_info_prep.common_data_dir + f_disambiguation_pat
    data_info_prep.enew_info_file = data_info_prep.common_data_dir + f_enew_info
    data_info_prep.enew_org_file = data_info_prep.common_data_dir + f_enew_org
    data_info_prep.enew_mod_list_file = data_info_prep.common_data_dir + f_enew_mod_list
    data_info_prep.common_html_info_file = data_info_prep.common_data_dir + f_common_html_info
    data_info_prep.incoming_file = data_info_prep.common_data_dir + f_incoming
    data_info_prep.linkable_file = data_info_prep.common_data_dir + f_linkable_info
    data_info_prep.link_prob_file = data_info_prep.common_data_dir + f_link_prob
    data_info_prep.mention_gold_link_dist_file = data_info_prep.common_data_dir + f_mention_gold_link_dist
    data_info_prep.title2pid_ext_file = data_info_prep.common_data_dir + f_title2pid_ext
    data_info_prep.title2pid_org_file = data_info_prep.common_data_dir + f_title2pid_org
    data_info_prep.redirect_info_file = data_info_prep.common_data_dir + f_redirect_info
    data_info_prep.slink_file = data_info_prep.common_data_dir + f_slink

    # tmp_data_dir
    data_info_prep.back_link_file = data_info_prep.tmp_data_dir + f_back_link
    data_info_prep.html_info_file = data_info_prep.tmp_data_dir + f_html_info
    data_info_prep.input_title_file = data_info_prep.tmp_data_dir + f_input_title
    data_info_prep.mint_partial_file = data_info_prep.tmp_data_dir + f_mint_partial
    data_info_prep.mint_trim_partial_file = data_info_prep.tmp_data_dir + f_mint_trim_partial
    data_info_prep.tinm_partial_file = data_info_prep.tmp_data_dir + f_tinm_partial
    data_info_prep.tinm_trim_partial_file = data_info_prep.tmp_data_dir + f_tinm_trim_partial

    # others
    sample_data_dir_pre = data_info_prep.sample_gold_dir
    sample_data_dir = sample_data_dir_pre.replace('link_annotation/', '')
    data_info_prep.common_html_dir = sample_data_dir + 'html/'
    data_info_prep.html_dir = data_info_prep.tmp_data_dir + 'html/'

    logger.info({
        'action': 'ljc_prep_main',
        'id': 'start',
        'common_data_dir': common_data_dir,
        'tmp_data_dir': tmp_data_dir,
        'in_dir': in_dir,
        'sample_gold_dir': sample_gold_dir,
        'sample_input_dir': sample_input_dir
    })

    if gen_sample_gold_tsv:
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'linkedjson2tsv',
            'sample_gold_dir': sample_gold_dir,
            'title2pid_org_file': data_info_prep.title2pid_org_file,
        })

        linkedjson2tsv(sample_gold_dir, data_info_prep.title2pid_org_file, log_info)

    if gen_redirect:
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_disambiguation_file',
            'disambiguation_pat_file': data_info_prep.disambiguation_pat_file,
            'cirrus_content_file': data_info_prep.cirrus_content_file,
            'disambiguation_file': data_info_prep.disambiguation_file,
        })
        gen_disambiguation_file(data_info_prep.disambiguation_pat_file, data_info_prep.cirrus_content_file,
                                data_info_prep.disambiguation_file, log_info)
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_redirect_info_file',
            'title2pid_org_file': data_info_prep.title2pid_org_file,
            'disambiguation_file': data_info_prep.disambiguation_file,
            'redirect_info_file': data_info_prep.redirect_info_file,
        })
        gen_redirect_info_file(data_info_prep.title2pid_org_file, data_info_prep.disambiguation_file,
                               data_info_prep.redirect_info_file, log_info)

    if gen_incoming_link:
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_incoming_link_file',
            'cirrus_content_file': data_info_prep.cirrus_content_file,
            'incoming_file': data_info_prep.incoming_file
        })
        gen_incoming_link_file(data_info_prep.cirrus_content_file, data_info_prep.incoming_file, log_info)

    if gen_title2pid_ext:
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_title2pid_ext',
            'enew_org_file': data_info_prep.enew_org_file,
            'enew_mod_list_file': data_info_prep.enew_mod_list_file,
            'enew_info_file': data_info_prep.enew_info_file,
        })
        gen_enew_info_file(data_info_prep.enew_org_file, data_info_prep.enew_mod_list_file,
                           data_info_prep.enew_info_file, log_info)
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_title2pid_ext',
            'title2pid_ext_file': data_info_prep.title2pid_ext_file,
            'incoming_file': data_info_prep.incoming_file,
            'enew_info_file': data_info_prep.enew_info_file,
            'redirect_info_file': data_info_prep.redirect_info_file,
        })
        gen_title2pid_ext_file(data_info_prep.title2pid_ext_file, data_info_prep.incoming_file,
                               data_info_prep.enew_info_file, data_info_prep.redirect_info_file, log_info)

    if gen_back_link:
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_input_title_file',
            'in_dir': data_info_prep.in_dir,
            'input_title_file': data_info_prep.input_title_file,
            'back_link_dump': data_info_prep.back_link_dump_file,
            'back_link_file': data_info_prep.back_link_file,
        })
        gen_input_title_file(data_info_prep.in_dir, data_info_prep.input_title_file, log_info)
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_back_link_info_file',
            'input_title_file': data_info_prep.input_title_file,
            'back_link_file': data_info_prep.back_link_file,
            'back_link_dump_file': data_info_prep.back_link_dump_file,
            'title2pid_ext_file': data_info_prep.title2pid_ext_file,
        })
        gen_back_link_info_file(data_info_prep.input_title_file, data_info_prep.back_link_file,
                                data_info_prep.back_link_dump_file, data_info_prep.title2pid_ext_file, log_info)
    if gen_common_html:
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_common_html',
            'common_html_dir': data_info_prep.common_html_dir,
            'common_html_info_file': data_info_prep.common_html_info_file
        })
        gen_html_info_file(data_info_prep.common_html_dir, data_info_prep.common_html_info_file, log_info)

    if gen_link_dist:
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_mention_gold_link_dist',
            'common_html_info_file': data_info_prep.common_html_info_file,
            'sample_gold_dir': data_info_prep.sample_gold_dir,
            'common_data_dir': data_info_prep.common_data_dir,
            'mention_gold_link_dist_file': data_info_prep.mention_gold_link_dist_file,

        })

        gen_mention_gold_link_dist(data_info_prep.common_html_info_file, data_info_prep.sample_gold_dir,
                                   data_info_prep.mention_gold_link_dist_file, log_info)

    if pre_matching == 'mint':
        if not title_matching_mint:
            logger.error({
                'action': 'ljc_prep_main',
                'error': 'title_matching_mint should be specified',
            })
            sys.exit()
        else:
            logger.info({
                'action': 'ljc_prep_main',
                'run': 'prematch_mention_title',

            })
            prematch_mention_title(data_info_prep, pre_matching, title_matching_mint, char_match_min, log_info)
    elif pre_matching == 'tinm':
        if not title_matching_tinm:
            logger.error({
                'action': 'ljc_prep_main',
                'error': 'title_matching_tinm should be specified',
            })
            sys.exit()
        else:
            prematch_mention_title(data_info_prep, pre_matching, title_matching_tinm, char_match_min, log_info)
    elif pre_matching != 'n':
        logger.error({
            'action': 'ljc_prep_main',
            'error': 'illegal pre_matching',
        })
        sys.exit()

    if gen_html:
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_html',
            'html_dir': data_info_prep.html_dir,
            'html_info_file': data_info_prep.html_info_file
        })
        gen_html_info_file(data_info_prep.html_dir, data_info_prep.html_info_file, log_info)

    if gen_link_prob:
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_link_prob',
            'link_prob_file': data_info_prep.link_prob_file,
        })
        gen_link_prob_file(data_info_prep.sample_gold_dir, data_info_prep.link_prob_file, log_info)

    if gen_slink:
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_slink',
            'sample_gold_dir': data_info_prep.sample_gold_dir,
            'slink_file': data_info_prep.slink_file
        })
        gen_self_link_info(data_info_prep.sample_gold_dir, data_info_prep.slink_file, log_info)

    if gen_linkable:
        logger.info({
            'action': 'ljc_prep_main',
            'run': 'gen_linkable',
            'sample_input_dir': data_info_prep.sample_input_dir,
            'sample_gold_dir': data_info_prep.sample_gold_dir,
            'linkable_file': data_info_prep.linkable_file
        })
        gen_linkable_info(data_info_prep.sample_input_dir, data_info_prep.sample_gold_dir, data_info_prep.linkable_file,
                          log_info)


def gen_input_title_file(in_dir, input_title_file, log_info):
    """extract page titles from input files
    args:
        in_dir
        input_title_file
        log_info
    output:
        input_title_file
    """
    import pandas as pd

    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    in_files = in_dir + '*.json'
    check = {}
    for in_file in glob(in_files):
        logger.info({
            'action': 'extract_input_title',
            'in_file': in_file,
        })
        with open(in_file, mode='r', encoding='utf-8') as i:
            for i_line in i:
                rec = json.loads(i_line)
                title = rec['title']
                if not check.get(title):
                    check[title] = 1

    title_list = list(check.keys())
    df = pd.DataFrame(title_list)
    df.to_csv(input_title_file, sep='\t', header=False, index=False)


def prematch_mention_title(data_info_prep, pre_matching, title_matching, char_match_min, log_info):
    """Pre-matching mention title.
    args:
        data_info_prep:
        pre_matching
        title_matching
        char_match_min
        log_info
    output:
        match_info_file
       　　 format:
                mention(\t)pid(\t)title(\t)ratio
           sample(mint):
                湖      401     湖国    0.5
                湖      9322    琵琶湖  0.33
                湖      1431634 湖      1.0
    Note:
        pre_matching
            tinm: partial match (title in mention text)
            mint: partial match (mention text in title)
        char_match_min
            minimum ratio of matching
            (tinm)  title length / mention length
            (mint)  mention length / title length
        title_matching
            If title_matching option is set to 'trim',
            the ratio is calculated based on title_trimmed.
        Titles composed of single kana characters are ignored.

    """
    import re
    import pandas as pd
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    in_files = data_info_prep.in_dir + '*.json'
    logger.info({
        'action': 'prematch_mention_title',
        'in_files': in_files,
    })
    d_pid2fromtitle = reg_pid2title(data_info_prep.title2pid_ext_file, log_info)

    tinm_partial_file = ''
    mint_partial_file = ''
    if pre_matching == 'tinm':
        if title_matching == 'trim':
            tinm_partial_file = data_info_prep.tinm_trim_partial_file
        else:
            tinm_partial_file = data_info_prep.tinm_partial_file
        logger.info({
            'action': 'prematch_mention_title',
            'pre_matching': pre_matching,
            'title_matching': title_matching,
            'tinm_partial_file': tinm_partial_file
        })
    elif pre_matching == 'mint':
        if title_matching == 'trim':
            mint_partial_file = data_info_prep.mint_trim_partial_file
        else:
            mint_partial_file = data_info_prep.mint_partial_file
        logger.info({
            'action': 'prematch_mention_title',
            'pre_matching': pre_matching,
            'title_matching': title_matching,
            'mint_partial_file': mint_partial_file
        })

    d_mention_pid_title_check = {}
    num_jsymbol_kana_pat = re.compile('^[\u0030-\u0039\u3000-\u303F\u3041-\u309F\u30A1-\u30FF]$')
    cols = ['mention', 'pid', 'title', 'ratio']

    df = pd.DataFrame(columns=cols)

    for in_file in glob(in_files):
        logger.info({
            'action': 'prematch_mention_title',
            'in_file': in_file,
        })
        with open(in_file, mode='r', encoding='utf-8') as i:
            fname = in_file.replace(data_info_prep.in_dir, '')
            ene_cat = fname.replace('.json', '')

            for i_line in i:
                rec = json.loads(i_line)
                mention = rec['text_offset']['text']
                for pid, title_list in d_pid2fromtitle.items():
                    for title in title_list:
                        # single character (num, jsymbol, kana)
                        if num_jsymbol_kana_pat.fullmatch(title):
                            continue
                        tmp_title = title
                        if title_matching == 'trim':
                            if ' (' in title:
                                title_trimmed = title
                                title_trimmed = title_trimmed.replace(' (', '\t')
                                trimmed_list = re.split('\t', title_trimmed)
                                if trimmed_list[-1].endswith('年'):
                                    logger.debug({
                                        'action': 'prematch_mention_title',
                                        'title_matching': title_matching,
                                        'org_title': title,
                                        'warning': 'title has multiple pairs of braces but ignored for it ends with 年',
                                        'title_list': trimmed_list,
                                    })
                                    pass
                                else:
                                    trimmed_list.pop()
                                    tmp_title = ' ('.join(trimmed_list)
                                    # single characters (num, jsymbol, kana)
                                    if num_jsymbol_kana_pat.fullmatch(tmp_title):
                                        continue
                                    else:
                                        if len(trimmed_list) > 2:
                                            logger.debug({
                                                'action': 'prematch_mention_title',
                                                'mention': mention,
                                                'debug': 'title has multiple pairs of braces'
                                                         ' (only the last has deleted)',
                                                'org_title': title,
                                                'tmp_title (trimmed for ratio)': tmp_title,
                                                'title_list': trimmed_list
                                            })
                                            pass
                        ratio = 0.0
                        if pre_matching == 'tinm' and tmp_title in mention:
                            ratio_str = str(len(tmp_title) / len(mention))
                            ratio = float(Decimal(ratio_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
                        elif pre_matching == 'mint' and mention in tmp_title:
                            ratio_str = str(len(mention) / len(tmp_title))
                            ratio = float(Decimal(ratio_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
                        else:
                            continue
                        if ratio < char_match_min:
                            continue
                        else:
                            mention_pid_title = mention + '\t' + pid + '\t' + title
                            if not d_mention_pid_title_check.get(mention_pid_title):
                                df = df.append({'mention': mention, 'pid': pid, 'title': title, 'ratio': ratio},
                                               ignore_index=True)
                                d_mention_pid_title_check[mention_pid_title] = 1
    df_new = df.sort_values(['mention', 'ratio'], ascending=[True, False])

    if pre_matching == 'tinm':
        df_new.to_csv(tinm_partial_file, sep='\t', header=False, index=False)

    if pre_matching == 'mint':
        df_new.to_csv(mint_partial_file, sep='\t', header=False, index=False)


def gen_html_info_file(html_dir, html_info_file, log_info):
    """Analyse given html files and extract WikiLink info.
    Args:
        html_dir(str)
        html_info_file(str)
        log_info
    Returns:

    Output:
        html_info_file
    Notice:
        html_info_file
            format
                cat(\t)pid(\t)line_id(\t)start(\t)end(\t)text(\t)title(\n)
    Notice:
        - line_id = line number - 1
        - html_files(*.html) should be located at html_dir/*/.
        - disambiguation pattern (dis_pat_title_head) includes 'jawiki-20190120' should be revised when using data
        based on other Wikipedia dumps.
    """
    import re
    from bs4 import BeautifulSoup
    from glob import glob
    import csv
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    html_files = html_dir + '*/*.html'
    logger.info({
        'action': 'gen_html_info_file',
        'html_files': html_files,
    })
    dis_pat_title_head = ('jawiki-20190120:', '特別:', 'Wikipedia_Dump', 'Wikipedia Dump', 'ファイル:', 'テンプレート:',
                          'プロジェクト:', 'カテゴリ:', 'ヘルプ:', 'Portal:',  'wikipedia:', '節を編集', 'このページ')
    dis_pat_title_partial = ('\/', '言語間リンクを追加する', '情報を得る場所', 'プロジェクトについて', 'スタブ項目', 'に移動する',
                             'あるページ', 'ある記事')
    html_info_list = []

    for filename in glob(html_files):
        cat_pre = re.split('/', filename.replace(html_dir, ''))
        cat = cat_pre[0]
        fname = cat_pre[1]
        fname = fname.replace('.html', '')
        with open(filename, 'r', encoding='utf-8') as f:
            check_elm = {}

            line_num = 0
            for line in f:

                line_num += 1
                line_id = line_num - 1

                soup = BeautifulSoup(line, 'html.parser')
                try:
                    links = soup.find_all('a')
                except(NameError, ValueError):
                    continue

                # start = 0
                for link in links:
                    try:
                        href_char = link.get('href')
                        if href_char:
                            if 'index' not in href_char:
                                continue
                            elif 'redlink' in href_char:
                                continue
                    except(NameError, ValueError):
                        continue

                    if 'rel' in link.attrs and 'nofollow' in link.attrs['rel']:
                        continue
                    if 'accesskey' in link.attrs:
                        continue
                    if 'class' in link.attrs:
                        tmp_class = link.attrs['class']
                        if len(tmp_class[0]) > 0 and 'mw-redirect' not in tmp_class[0]:
                            continue
                    if 'title' not in link.attrs:
                        continue
                    tmp_title = link.attrs['title']
                    if len(tmp_title) == 0:
                        continue
                    elif tmp_title.startswith(dis_pat_title_head):
                        continue
                    else:
                        check_hit = 0
                        for t in dis_pat_title_partial:
                            if t in tmp_title:
                                check_hit = 1
                                break
                        if check_hit == 1:
                            continue
                    if not link.text:
                        continue
                    if len(link.text) == 0:
                        continue
                    elif link.text == '^':
                        continue
                    elif link.text not in line:
                        continue
                    # wikipedia link pattern (including symbols)
                    regex_pat = re.escape('>' + link.text + '<')

                    try:
                        taglist = list(re.finditer(regex_pat, line))
                    except ValueError:
                        continue
                    for tag in taglist:
                        # excluding symbols
                        text_start = tag.start() + 1
                        text_end = tag.end() - 1
                        if text_start >= 1:
                            tmp_dict = {'cat': cat, 'pid': fname, 'line_id': str(line_id),
                                        'html_text_start': str(text_start), 'html_text_end': str(text_end),
                                        'html_text': link.text, 'title': tmp_title}
                            elm = '_'.join([str(line_id), str(text_start), str(text_end)])
                            if not check_elm.get(elm):
                                check_elm[elm] = 1
                                html_info_list.append(tmp_dict)

    labels = ['cat', 'pid', 'line_id', 'html_text_start', 'html_text_end', 'html_text', 'title']

    with open(html_info_file, 'w') as o:
        writer = csv.DictWriter(o, fieldnames=labels, delimiter='\t', lineterminator='\n')
        writer.writeheader()
        for elem in html_info_list:
            writer.writerow(elem)


def reg_pid2title(title2pid_ext_file, log_info):

    """Register title2pid_info pages info.
    Args:
        title2pid_ext_file
        log_info
    Returns:
        d_pid2fromtitle dict
            {pid: [title1, title2, ....]}

    Notice:
        - title2pid_ext_file
            format: 'from_title'\t'to_pid'\t'to_title'\t'to_incoming\t'to_eneid'
       　　　sample:
            エチオピア人民民主共和国	1443906	エチオピア	2427	1.5.1.3
            エチオピア連邦民主共和国	1443906	エチオピア	2427	1.5.1.3
            社会主義エチオピア	1443906	エチオピア	2427	1.5.1.3
            エティオピア	1443906	エチオピア	2427	1.5.1.3
            エチオピア人	1443906	エチオピア	2427	1.5.1.3
            Ethiopia	1443906	エチオピア	2427	1.5.1.3
            エチオピア	1443906	エチオピア	2427	1.5.1.3

    """
    import csv
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    d_pid2fromtitle = {}

    with open(title2pid_ext_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for rows in reader:
            from_title = rows[0]
            to_pid_str = rows[1]
            if not d_pid2fromtitle.get(to_pid_str):
                d_pid2fromtitle[to_pid_str] = []
            d_pid2fromtitle[to_pid_str].append(from_title)
    return d_pid2fromtitle


def gen_title2pid_ext_file(exfile, incoming, enew_info, redirect_info, log_info):
    """gen_title2pid_ext_filemerge title2pid info.
     Args:
         exfile
         incoming
         enew_info
         redirect_info
         log_info
     output:
        f_title2pid_ext
            format
                (title(from page))\t(pageid(to page))\t(title(to page)\t(maximum number of incoming links(to page))
                \t(eneid(to_page))
            sample
                アメリカ合衆国  1698838 アメリカ合衆国  116818  1.5.1.3
                ユナイテッドステイツ    1698838 アメリカ合衆国  116818  1.5.1.3
                亜米利加合衆国  1698838 アメリカ合衆国  116818  1.5.1.3
                U.S.    1698838 アメリカ合衆国  116818  1.5.1.3
                USA     1698838 アメリカ合衆国  116818  1.5.1.3
                アメリカ        1698838 アメリカ合衆国  116818  1.5.1.3
     Notice:
         - redirect info
            - The from_title to_page pairs in the redirect file are originally defined in
            jawiki-202190120-title2pageid.json.
            - In the redirect info,
                - white spaces in Wikipedia titles are replaced by '_'.
                - Some records with illegal formats (eg. lack of to_pageid) are deleted.
                - Disambiguation pages are deleted (although not always completely).
        -incoming: pageid, title, maximum number of incoming_links
                   ('jawiki-20190121-cirrussearch-content_incoming_link.tsv')
            -format: <pageid>\t<title>\t<maximum num of incoming_links>
            -sample
                2264978 マーキング      23
                662923  ノワール        32
        -enew_info: ENEW info(based on slightly modified version of ENEW 20210427）
            - format: <pageid>\t<ENEID>\t<page title>
            - sample
                72942  1.2     バックス (ローマ神話)
                401755  1.1     覚信尼
            - modification list: ENEW_ENEtag_20200427_stoplist.tsv (ENEID, pid, title)
        - Some pages lack incoming info or enew info.

    """
    import pandas as pd
    import csv
    import sys
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    redirect_info = redirect_info
    enew_info = enew_info
    incoming = incoming
    exfile = exfile

    logger.info({
        'action': 'gen_title2pid_ext_file',
        'enew_info': enew_info,
        'incoming': incoming,
        'exfile': exfile,
    })
    get_to_ene = {}
    get_to_title = {}

    with open(enew_info) as e:
        reader = csv.reader(e, delimiter='\t')
        for row in reader:
            try:
                to_pid = row[0]
                to_eneid = row[1]
                to_title = row[2]
            except ValueError as e:
                logger.error({
                    'action': 'gen_title2pid_ext_file',
                    'file': enew_info,
                    'error': e,
                    'row': row
                })
                sys.exit()
            get_to_ene[to_pid] = to_eneid
            get_to_title[to_pid] = to_title

    get_to_incoming = {}
    with open(incoming) as i:
        reader = csv.reader(i, delimiter='\t')

        for row in reader:
            try:
                to_pid = row[0]
                to_title = row[1]
                to_incoming = row[2]
            except ValueError as ie:
                logger.error({
                    'action': 'gen_title2pid_ext_file',
                    'file': incoming,
                    'to_pid': to_pid,
                    'error': ie,
                    'row': row
                })
                sys.exit()
            get_to_incoming[to_pid] = to_incoming

            # Complement titles for ENEW file lacks some pages.
            if not get_to_title.get(to_pid):
                get_to_title[to_pid] = to_title

    with open(redirect_info) as e:
        reader = csv.reader(e, delimiter='\t')
        rec_list = []
        # Some pages lack incoming or ENEW information
        for row in reader:
            rec = []
            from_title = ''
            to_incoming = 0
            to_eneid = ''
            from_title = row[0]
            to_pid = row[1]
            if not from_title:
                logger.error({
                    'action': 'gen_title2pid_ext_file',
                    'missing from_title': row
                })
                sys.exit()
            if not to_pid:
                logger.error({
                    'action': 'gen_title2pid_ext_file',
                    'missing to_pid': row
                })
                sys.exit()
            # Complement titles for ENEW file lacks some pages.
            if get_to_title.get(to_pid):
                to_title = get_to_title[to_pid]
                if not to_title:
                    logger.warning({
                        'action': 'gen_title2pid_ext_file',
                        'missing to_title': to_pid
                    })
            if get_to_incoming.get(to_pid):
                to_incoming = get_to_incoming[to_pid]
                if not to_incoming:
                    logger.error({
                        'action': 'gen_title2pid_ext_file',
                        'to_pid': to_pid,
                        'error': 'invalid incoming'
                    })
                    sys.exit()
                else:
                    to_incoming = int(to_incoming)

            if get_to_ene.get(to_pid):
                to_eneid = get_to_ene[to_pid]
                if not to_eneid:
                    logger.warning({
                        'action': 'gen_title2pid_ext_file',
                        'missing to_eneid': to_eneid
                    })

            rec = [from_title, to_pid, to_title, to_incoming, to_eneid]
            rec_list.append(rec)

        df = pd.DataFrame(rec_list, columns=['from_title', 'to_pid', 'to_title', 'to_incoming', 'to_eneid'])
        new_df = df.sort_values('to_incoming', ascending=False)
        new_df.to_csv(exfile, sep='\t', header=False, index=False)


def get_category(fname, dname, ext, log_info):
    """ get category label from the file name
    :param fname:
    :param dname:
    :param ext:
    :param log_info
    :return: cat
    """
    import logging
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    cat_pre = fname.replace(dname, '')
    cat_new = cat_pre.replace(ext, '')
    return cat_new


def check_self(row, log_info):
    """check if self-link
    :param row:
    :param log_info:
    :return: 1 (self), 0 (non-self)
    """
    import logging
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    if row[0] == row[8]:
        return 1
    else:
        return 0


def gen_linkable_info(sample_e_dir, sample_g_dir, linkable_info_file, log_info):
    """Generate linkable info
    args:
        sample_in_dir
        sample_gold_dir
        linkable_info_file:
        log_info:
    return:
    output:
        linkable_info_file
    Note:
        gold file
            Gold files (eg. sample gold files) used for linkable estimation should be located in gold_dir.
            sample
                3623607	下半山村	合併市区町村	三間ノ川村	61	39	61	44	29489	高岡郡
                3623607	下半山村	合併市区町村	三間ノ川村	61	39	61	44	3623607	下半山村
    """
    import logging

    import pandas as pd
    import re
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)
    logger.info({
        'action': 'ljc_prep_main',
        'start': 'gen_linkable_info',
        'sample_dir': sample_e_dir,
        'gold_dir': sample_g_dir,
        'linkable_info_file': linkable_info_file
    })
    prt_list = []

    ene = sample_e_dir + '*.json'
    gold = sample_g_dir + '*.json'

    count_e_cat_attr = {}
    count_g_cat_attr = {}

    for ene_file in glob(ene):
        with open(ene_file, mode='r', encoding='utf-8') as ef:
            e_fname = ene_file.replace(sample_e_dir, '')
            e_cat = e_fname.replace('.json', '')

            logger.info({
                'action': 'ljc_main',
                'ene_cat': e_cat,
                'e_fname': e_fname,
            })

            for e_line in ef:
                erec = json.loads(e_line)
                e_attr = erec['attribute']

                e_cat_attr = e_cat + ':' + e_attr

                if not count_e_cat_attr.get(e_cat_attr):
                    count_e_cat_attr[e_cat_attr] = 1
                else:
                    count_e_cat_attr[e_cat_attr] += 1

    for g_file in glob(gold):
        with open(g_file, mode='r', encoding='utf-8') as gf:
            g_fname = g_file.replace(sample_g_dir, '')
            g_cat = g_fname.replace('.json', '')

            logger.info({
                'action': 'ljc_main',
                'g_cat': g_cat,
                'g_fname': g_fname,
            })

            for g_line in gf:
                grec = json.loads(g_line)
                g_attr = grec['attribute']

                g_cat_attr = g_cat + ':' + g_attr

                if not count_g_cat_attr.get(g_cat_attr):
                    count_g_cat_attr[g_cat_attr] = 1
                else:
                    count_g_cat_attr[g_cat_attr] += 1

    for cat_attr in count_e_cat_attr:
        (t_cat, t_attr) = re.split(':', cat_attr)
        if count_g_cat_attr.get(cat_attr):
            t_ratio_str = count_g_cat_attr[cat_attr]/count_e_cat_attr[cat_attr]
            t_ratio = float(Decimal(t_ratio_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        else:
            t_ratio = 0.0

        prt_list.append([t_cat, t_attr, t_ratio])

    sdf = pd.DataFrame(prt_list, columns=['cat', 'attr', 'ratio'])
    sdf.to_csv(linkable_info_file, sep='\t', header=False, index=False)

def gen_self_link_info(gold_dir, self_link_info_file, log_info):
    """Generate self link info
    args:
        gold_dir
        self_link_info_file:
        log_info:
    return:
    output:
        self_link_info_file
    Note:
        gold file
            Gold files (eg. sample gold files) used for self link estimation should be located in gold_dir.
            sample
                3623607	下半山村	合併市区町村	三間ノ川村	61	39	61	44	29489	高岡郡
                3623607	下半山村	合併市区町村	三間ノ川村	61	39	61	44	3623607	下半山村
    """
    import logging

    import pandas as pd
    import re
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)
    logger.info({
        'action': 'ljc_prep_main',
        'start': 'gen_self_link_info',
        'gold_dir': gold_dir,
        'self_link_info_file': self_link_info_file
    })
    prt_list = []
    ext = '.tsv'

    gold = gold_dir + '*.tsv'

    sumup_cat_attr = {}
    sumup_self_cat_attr = {}

    for g_fname in glob(gold):
        cat = get_category(g_fname, gold_dir, ext, log_info)
        logger.info({
            'action': 'gen_self_link_info',
            'cat': cat,
            'g_fname': g_fname
        })
        check_gold = {}
        check_self_gold = {}

        with open(g_fname, mode='r', encoding='utf-8') as f:
            greader = csv.reader(f, delimiter='\t')

            for grow in greader:
                gold_key = '\t'.join(grow[0:8])
                if not check_gold.get(gold_key):
                    check_gold[gold_key] = 1

                # self-link
                if check_self(grow, log_info):
                    if not check_self_gold.get(gold_key):
                        check_self_gold[gold_key] = 1
                    else:
                        check_self_gold[gold_key] += 1

        for common_key in check_gold:
            common_key_list = re.split('\t', common_key)
            cat_attr = cat + '\t' + common_key_list[2]

            if not sumup_cat_attr.get(cat_attr):
                sumup_cat_attr[cat_attr] = check_gold[common_key]
            else:
                sumup_cat_attr[cat_attr] += check_gold[common_key]

            if check_self_gold.get(common_key):
                if not sumup_self_cat_attr.get(cat_attr):
                    sumup_self_cat_attr[cat_attr] = check_self_gold[common_key]
                else:
                    sumup_self_cat_attr[cat_attr] += check_self_gold[common_key]

    for t_cat_attr in sumup_cat_attr:
        (t_cat, t_attr) = re.split('\t', t_cat_attr)
        if sumup_self_cat_attr.get(t_cat_attr):
            t_ratio_str = sumup_self_cat_attr[t_cat_attr]/sumup_cat_attr[t_cat_attr]
            t_ratio = float(Decimal(t_ratio_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        else:
            t_ratio = 0.0

        prt_list.append([t_cat, t_attr, t_ratio])

    sdf = pd.DataFrame(prt_list, columns=['cat', 'attr', 'ratio'])
    sdf.to_csv(self_link_info_file, sep='\t', header=False, index=False)


def get_to_pid_to_title_incoming_eneid(title2pid_ext_file, log_info):
    """Register title2pid_info pages info.
    Args:
        title2pid_ext_file
        #eg. イギリス語      3377    英語    95319   1.7.24.1
        log_info
    Returns:
        d_pid_title_incoming_eneid
            format
                key: to_pid
                val: to_title, to_incoming, to_eneid
            sample
                {'3377': ['英語', 95319','1.7.24.1'])
    Notice:
        - title2pid_title_ex
            format: 'from_title'\t'to_pid'\t'to_title'\t'to_incoming\t'to_eneid'

    """
    import csv
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    d_pid_title_incoming_eneid = {}

    with open(title2pid_ext_file, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            to_pid = str(row[1])
            to_title = row[2]
            to_incoming = row[3]
            to_eneid = str(row[4])
            d_pid_title_incoming_eneid[to_pid] = [to_title, to_incoming, to_eneid]
    return d_pid_title_incoming_eneid


def gen_back_link_info_file(ptitle_list, back_link, back_link_dump, ext_file, log_info):
    """
    get back link info and save in back link file
    :param ptitle_list: page title list of input files
    :param back_link:
    :param back_link_dump:
    :param ext_file:
    :param log_info:
    :return:
    :output: back_link_file
    :notice:
        back_link_dump:
            based on jawiki-20190120-pagelinks.sql
            lines including characters other than utf-8 are skipped.
            Some records of back_link_file may lack from titles.
            sample
                41246	1975年度新人選手選択会議_(日本プロ野球)
                92044	1975年度新人選手選択会議_(日本プロ野球)
                95956	1975年度新人選手選択会議_(日本プロ野球)
                143952	1975年度新人選手選択会議_(日本プロ野球)
        back_link_file:
            sample
                1975年度新人選手選択会議 (日本プロ野球) 41246   プロ野球ドラフト会議
                1975年度新人選手選択会議 (日本プロ野球) 92044   北別府学
                1975年度新人選手選択会議 (日本プロ野球) 95956   篠塚和典
                1975年度新人選手選択会議 (日本プロ野球) 143952  中畑清
    """
    import pandas as pd
    import csv
    import codecs
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    back_link_list = []
    d_title = {}
    d_pid_title_incoming_eneid = get_to_pid_to_title_incoming_eneid(ext_file, log_info)
    with open(ptitle_list, 'r', encoding='utf-8') as fp:
        for row in fp:
            row = row.replace('\n', '')
            ptitle = row.replace('_', ' ')
            d_title[ptitle] = 1

    with codecs.open(back_link_dump, 'r', 'utf-8', 'ignore') as dp:
        reader = csv.reader(dp, delimiter='\t')
        for drow in reader:
            org_title = drow[1]
            org_title = org_title.replace('_', ' ')
            from_pageid = drow[0]
            if d_title.get(org_title):
                from_title = ''
                # notice: not all pageids are found in d_pid_title_incoming_eneid (eg.template pages)
                if d_pid_title_incoming_eneid.get(from_pageid):
                    from_title = d_pid_title_incoming_eneid[from_pageid][0]
                back_link_list.append([org_title, from_pageid, from_title])

    df = pd.DataFrame(back_link_list, columns=['org_title', 'from_pageid', 'from_title'])
    df.to_csv(back_link, sep='\t', header=False, index=False)


def gen_link_prob_file(gold_dir, link_prob_file, log_info):
    """
    create probability info file based on link statistics in sample gold file
    :param:gold_dir (eg. sample_gold_dir)
    :param:link_prob_file
    :param:log_info
    :output: link_prob_file
    """

    from glob import glob
    import re
    import sys
    import csv
    import pandas as pd
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    gold_files = gold_dir + '*.tsv'

    logger.info({
        'action': 'gen_link_prob_file',
        'gold_files': gold_files,
        'link_prob_file': link_prob_file
    })
    d = {}
    for gname in glob(gold_files):
        with open(gname, mode='r', encoding='utf-8') as g:
            cat = gname.replace(gold_dir, '')
            cat = cat.replace('.tsv', '')

            reader = csv.reader(g, delimiter='\t')
            for line in reader:
                if len(line) < 10:
                    logger.warning({
                        'action': 'gen_link_prob_file',
                        'warning': 'format error list too short (skipped)',
                        'line': line,
                    })
                    continue

                att_name = line[2]
                att_value = line[3]
                link_pid = line[8]
                cat_attname_attval = cat + '\t' + att_name + '\t' + att_value
                if not d.get(cat_attname_attval):
                    d[cat_attname_attval] = {}
                if not d[cat_attname_attval].get(link_pid):
                    d[cat_attname_attval][link_pid] = 1
                else:
                    d[cat_attname_attval][link_pid] += 1
                logger.debug({
                    'action': 'gen_link_prob_file',
                    'line': line,
                    'cat_attname_attval': cat_attname_attval,
                    'link_pid': link_pid,
                    'd[cat_attname_attval][link_pid]': d[cat_attname_attval][link_pid]
                })

    d_new = {}
    for cat_att_val, link_pid_info in d.items():
        if cat_att_val not in d_new:
            d_new[cat_att_val] = []
        link_pid_info_sorted = sorted(link_pid_info.items(), key=lambda x: x[1], reverse=True)
        logger.debug({
            'action': 'gen_link_prob_file',
            'link_pid_info_sorted': link_pid_info_sorted
        })
        if len(link_pid_info_sorted) >= 1:
            link_sum = 0
            for tmp_lpinfo in link_pid_info_sorted:
                link_sum += tmp_lpinfo[1]
                logger.debug({
                    'action': 'gen_link_prob_file',
                    'tmp_lpinfo': tmp_lpinfo,
                    'tmp_lpinfo[1]': tmp_lpinfo[1]
                })

            for tmp_lpinfo in link_pid_info_sorted:
                ratio_str = str(tmp_lpinfo[1] / link_sum)
                ratio = float(Decimal(ratio_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
                link_pid_info_string = tmp_lpinfo[0] + ':' + str(ratio) + ':' + str(tmp_lpinfo[1])
                d_new[cat_att_val].append(link_pid_info_string)
                logger.debug({
                    'action': 'gen_link_prob_file',
                    'ratio_str': ratio_str,
                    'link_sum': link_sum,
                    'link_pid_info_string': link_pid_info_string
                })
        else:
            logger.error({
                'action': 'gen_link_prob_file',
                'error': 'format error link_pid_info too short'
            })
            sys.exit()

    print_list = []
    for cat_att_val, link_pid_info_string in d_new.items():
        tmp_print_list = re.split('\t', cat_att_val)
        v_str = ';'.join(link_pid_info_string)
        tmp_print_list.append(v_str)
        print_list.append(tmp_print_list)

    df_a = pd.DataFrame(print_list)
    df_a.to_csv(link_prob_file, sep='\t', header=False, index=False)


def gen_mention_gold_link_dist(html_info, sample_gold_dir, outfile, log_info):
    """get mention nearest gold link distance from sample gold html files and create mention_gold_link_dist file.
    args
        html_info
        sample_gold_dir
        outfile
        log_info
    output
        mention_gold_link_dist
            format
                category, attribute, distance between mention and gold embedded link

            sample
                Person  作品    17
                Person  作品    81
                Person  作品    81
                Person  作品    -1
                Person  作品    -1
    note
        tag_info
            format
                cat     pid     line_id html_text_start html_text_end   html_text       title
            sample
                City    3692278 34      148     150     日本    日本
        gold_files
            1013693 ルイス・ムニョス・マリン国際空港        別名    Aeropuerto Internacional Luis Muñoz Marín
            42      16      42      57      1013693 ルイス・ムニョス・マリン国際空港
    """

    import csv
    import pandas as pd
    from glob import glob
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    # ignore if in the same line
    ignore_zero = 1
    gold_files = sample_gold_dir + '*.tsv'
    logger.info({
        'action': 'gen_mention_gold_link_dist',
        'gold_dir': sample_gold_dir,
        'html_info': html_info
    })
    with open(html_info, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')

        cat_pid_title_dic = {}
        check_cat_pid_title_line = {}
        for row in reader:
            cat = row[0]
            # header
            if cat == 'cat':
                continue
            pid = row[1]
            line_start = row[2]
            title = row[6]
            cat_pid_title_line = ':'.join([cat, pid, title, line_start])
            cat_pid_title = ':'.join([cat, pid, title])

            if not check_cat_pid_title_line.get(cat_pid_title_line):
                cat_pid_title_dic[cat_pid_title] = []
            cat_pid_title_dic[cat_pid_title].append(int(line_start))
            check_cat_pid_title_line[cat_pid_title_line] = 1

    out_raw_list = []
    for gfile in glob(gold_files):
        list_rec_out = []
        gfile_part = gfile.replace(sample_gold_dir, '')
        ene_cat = gfile_part.replace('.tsv', '')
        with open(gfile, 'r', encoding='utf-8') as g:
            greader = csv.reader(g, delimiter='\t')

            for grow in greader:
                g_org_pid = grow[0]
                g_attr = grow[2]
                g_mention_line_start = grow[4]
                g_gold_title = grow[9]
                g_cat_pid_title = ':'.join([ene_cat, g_org_pid, g_gold_title])

                if cat_pid_title_dic.get(g_cat_pid_title):
                    tmp_lineid_list = cat_pid_title_dic[g_cat_pid_title]
                    found = 0
                    for lineid in tmp_lineid_list:
                        if int(g_mention_line_start) == lineid:
                            if ignore_zero:
                                continue
                            else:
                                diff_min = 0
                                found = 1
                                break
                        else:
                            if found == 0:
                                diff_min = lineid - int(g_mention_line_start)
                            elif abs(lineid - int(g_mention_line_start) < abs(diff_min)):
                                diff_min = lineid - int(g_mention_line_start)
                                found = 1
                    out_raw_list.append([ene_cat, g_attr, diff_min])

    df = pd.DataFrame(out_raw_list, columns=['cat', 'attr', 'diff_min'])
    df.to_csv(outfile, sep='\t',  index=False)


def get_disambiguation_info(dis_file, log_info):
    """Get disambiguation info.
    Args:
        dis_file (str): disambiguation info file name
        log_info
    Returns:
        d_pid_title (dict)
    Note:
        dis_file:
            dis_file is created from cirrus dump, using some patterns of category or title of Wikipedia pages
                eg. Wikipedia category ends with '曖昧さ回避'
                    Wikipedia category starts with '同名の'
                    Wikipedia category ends with '（曖昧さ回避）'
                sample:
                    2264978     マーキング
                    662923      ノワール
                    134999      スコア
                    ....
        d_pid_title:
            format:
                key: pageid of disambiguation page
                val: 1
            sample:
                {'2264978': 1, '662923': 1, '134999': 1, .....}
    """
    import csv
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    with open(dis_file, 'r', encoding='utf-8') as da:
        da_reader = csv.reader(da, delimiter='\t')
        pid_title_list = [da_row for da_row in da_reader]

        d_pid_title = {str(pid_title[0]): 1 for pid_title in pid_title_list}
    return d_pid_title


def check_pageid(pageid, log_info, **d_dis):
    """ check pageid if it can be a candidate link page (disambiguation, isdigit)
    Args:
        pageid
        log_info
        **d_dis
    Returns:
        1: ok
        -1: ng
    """
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    if not pageid:
        logging.error({
            'action': 'check_pageid',
            'judge': 'ng (pageid null)'
        })
        return -1
    elif not str(pageid).isdigit():
        logging.error({
            'action': 'check_pageid',
            'pageid': pageid,
            'judge': 'ng (not digit)'
        })
        return -1
    elif d_dis.get(str(pageid)):
        return -1
    else:
        return 1


def gen_redirect_info_file(title2pageid, dis, redirect_info, log_info):
    """ remove disambiguation pages and wrong-formatted pages from title2pageid and
    create redirect info default file
    Args:
        title2pageid
        dis
        redirect_info
        log_info
    Returns:
    Output:
        redirect_info
        Notice:
            - In the title2pageid file,some 'redirect-to' pages lack page_ids.
                 {"page_id": 1218449, "title": "岡山県の旧制教育機関", "is_redirect": true,
                  "redirect_to": {"page_id": null, "title": null, "is_redirect": false}}
              - white spaces in Wikipedia titles are replaced by '_'.
    """
    import csv
    import json

    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    title_apid = {}
    d_dis = get_disambiguation_info(dis, log_info)

    title_apid = {}
    with open(title2pageid, mode='r', encoding='utf-8') as r:
        for r_line in r:
            rd = json.loads(r_line)

            from_pid = rd['page_id']

            # disambiguation
            if check_pageid(from_pid, log_info, **d_dis) != 1:
                continue
            from_title = rd['title'].replace('_', ' ')
            # redirect page
            if rd['is_redirect']:
                if not rd['redirect_to']['page_id']:
                    continue
                else:
                    to_pid = rd['redirect_to']['page_id']
                    if check_pageid(to_pid, log_info, **d_dis) != 1:
                        continue
                    else:
                        title_apid[from_title] = str(to_pid)
            # non-redirect page
            else:
                title_apid[from_title] = str(from_pid)

        with open(redirect_info, 'w') as o:
            writer = csv.writer(o, delimiter='\t', lineterminator='\n')
            for k, v in title_apid.items():
                writer.writerow([k, v])


def gen_disambiguation_file(patfile, cirrus, outfile, log_info):
    """Extract Wikipedia pages which satisfies the matching patterns specified in the pattern file
    arg:
        patfile
        cirrus (.gz)
        outfile
        log_info
    note
        patfile
            format
                <field>\t<match_position>_<pat>\n
                <field>   cat|title
                <match_position>    start|middle|end
                <pat>
                Notice: Matching patterns are interpreted as 'OR' conditions
            sample:
                cat     end 曖昧さ回避
                cat     start 同名の
                 - category: endswith '曖昧さ回避'
                 - category: startswith '同名の'
    """

    import re
    import json
    import gzip
    import sys
    import csv
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)
    id_title = []

    check_cat = {}
    check_title = {}
    with open(patfile, mode='r', encoding='utf-8') as p:
        for p_line in p:
            p_line_new = p_line.rstrip()
            (field, pos, pat) = re.split('\t', p_line_new)
            logger.debug({
                'action': 'gen_disambiguation_file',
                'field': field,
                'pos': pos,
                'pat': pat
            })
            pat_pos = pat + '\t' + pos
            if 'cat' in field:
                check_cat[pat] = pos
            if 'title' in field:
                check_title[pat] = pos

    with gzip.open(cirrus, mode='rt', encoding='utf-8') as c:

        id_title = []
        for c_line in c:
            check_dis = 0
            d = json.loads(c_line)
            if 'index' in d:
                tmp_id = str(d['index']['_id'])

            # information other than index
            else:
                if 'namespace' in d:
                    if d['namespace'] != 0:
                        continue
                if 'title' not in d:
                    logger.error({
                        'action': 'gen_disambiguation_file',
                        'error': 'title not found in d',
                        'c_line': c_line
                    })
                    sys.exit()
                else:
                    tmp_title = d['title']

                for tmp_pat, tmp_pos in check_title.items():
                    if tmp_pat in tmp_title:
                        if tmp_pos == 'start':
                            if tmp_title.startswith(tmp_pat):
                                check_dis = 1
                        elif tmp_pos == 'end':
                            if tmp_title.endswith(tmp_pat):
                                check_dis = 1
                        elif tmp_pos == 'middle':
                            check_dis = 1

                if check_dis != 1:
                    if 'category' not in d:
                        logger.error({
                            'action': 'gen_disambiguation_file',
                            'error': 'category not found in d',
                            'c_line': c_line
                        })
                        sys.exit()

                    d_cat = {cat: 1 for cat in d['category']}

                    for tmp_dcat in d_cat:
                        for tmp_pat, tmp_pos in check_cat.items():
                            if tmp_pat in tmp_dcat:
                                if tmp_pos == 'start':
                                    if tmp_dcat.startswith(tmp_pat):
                                        check_dis = 1
                                elif tmp_pos == 'end':
                                    if tmp_dcat.endswith(tmp_pat):
                                        check_dis = 1
                                elif tmp_pos == 'middle':
                                    check_dis = 1

                if check_dis == 1:
                    id_title.append([tmp_id, tmp_title])

    with open(outfile, 'w', encoding='utf-8') as o:
        writer = csv.writer(o, delimiter='\t', lineterminator='\n')
        writer.writerows(id_title)


def gen_enew_info_file(enew_org, mod_list, enew_info, log_info):
    """
    args:
        data_info_prep
        log_info
    output:
        enew_info
    note:
        mod_list
            sample
                1.5.1.3 1419479 フランス陸軍参謀総長
                1.5.1.3 2092622 クウェートの首相
                1.5.1.3 2242121 アディゲの首長
    """
    import re
    import json
    import csv
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    check_mod = {}
    with open(mod_list, 'r', encoding='utf-8') as s:
        for sline in s:
            llist = re.split('\t', sline)
            eneid = llist[0]
            pid = llist[1]
            tmp_key = pid + ':' + eneid
            if tmp_key not in check_mod:
                check_mod[tmp_key] = 1
    plist = []
    with open(enew_org, 'r', encoding="utf-8") as e:
        for line in e:
            t = json.loads(line)
            pageid = t['pageid']
            title = t['title']

            if t['ENEs']:
                for k, v in t['ENEs'].items():
                    for m in v:
                        if 'ENE_id' in m:
                            eid = m['ENE_id']
                            t_key = str(pageid) + ':' + eid
                            if t_key not in check_mod:
                                plist.append([str(pageid), eid, title])

    with open(enew_info, 'w', encoding='utf-8') as o:
        writer = csv.writer(o, delimiter='\t', lineterminator='\n')
        writer.writerows(plist)


def gen_incoming_link_file(cirrus_content, outfile, log_info):
    """Get num of incoming links from cirrus dump and create incoming_link_file
    args:
        cirrus_content:
        outfile:
        log_info:
    output:
        incoming_link_file
    """
    import json
    import gzip
    import sys
    import csv
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)
    logger.info({
        'action': 'get_incoming_link_file',
        'cirrus_content': cirrus_content,
        'outfile': outfile
    })
    with gzip.open(cirrus_content, mode='rt', encoding='utf-8') as c:
        id_title_link = []
        for c_line in c:
            d = json.loads(c_line)
            if 'index' in d:
                tmp_id = str(d['index']['_id'])
            else:
                if 'namespace' in d:
                    if d['namespace'] != 0:
                        print('error:namespace', c_line)
                        continue
                if 'title' not in d:
                    logger.error({
                        'action': 'get_incoming_link_file',
                        'error': 'title not found',
                        'c_line': c_line
                    })
                    sys.exit()
                else:
                    tmp_title = d['title']
                if 'incoming_links' not in d:
                    logger.error({
                        'action': 'get_incoming_link_file',
                        'error': 'incoming links not found',
                        'c_line': c_line
                        })
                    sys.exit()
                else:
                    tmp_link_num = d['incoming_links']
                    id_title_link.append([tmp_id, tmp_title, tmp_link_num])

    with open(outfile, 'w', encoding='utf-8') as o:
        writer = csv.writer(o, delimiter='\t', lineterminator='\n')
        writer.writerows(id_title_link)


def linkedjson2tsv(linked_json_dir, title2pid_org_file, log_info):
    """Convert linked json file to linked tsv file
        add title info based on title2pid_org_file
    args:
        linked_json_dir
        title2pid_org_file
        log_info
    output:
        linked_tsv (tsv)
            format
                pageid, title, attribute, text, start_line_id, start_offset, end_line_id, end_offset, link_pageid,
                link_page_title
            sample
                2392906	桐谷華	地位職業	声優	38	20	38	22	1192	声優
    notice
        '\n' in text(mention) has been converted to '\\n'.
    """

    import json
    import pandas as pd
    from glob import glob

    import logging
    import re
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    logger.info({
        'action': 'linkedjson2tsv',
        'linked_json_dir': linked_json_dir,
        'title2pid_org_file': title2pid_org_file,
    })
    get_title = {}
    with open(title2pid_org_file, mode='r', encoding='utf-8') as r:
        for rline in r:
            rd = {}
            pid = ''
            title = ''
            rd = json.loads(rline)
            if 'page_id' not in rd:
                logger.error({
                    'action': 'linkedjson2tsv',
                    'error': 'missing page_id'
                })
                sys.exit()
            elif not rd['page_id']:
                logger.error({
                    'action': 'linkedjson2tsv',
                    'error': 'page_id null'
                })
                sys.exit()
            else:
                pid = str(rd['page_id'])
            # title (not forwarded page)
            if 'title' not in rd:
                logger.error({
                    'action': 'linkedjson2tsv',
                    'error': 'title not in rd',
                    'rline': rline
                })
                sys.exit()
            elif not rd['title']:
                logger.error({
                    'action': 'linkedjson2tsv',
                    'error': 'no title redirect to',
                    'rline': rline
                })
                sys.exit()
            else:
                title = rd['title']
                get_title[pid] = title
            rd.clear()

    linked_json_files = linked_json_dir + '*.json'

    for linked_json in glob(linked_json_files):
        go_list = []
        linked_tsv = linked_json.replace('.json', '.tsv')
        with open(linked_json, mode='r', encoding='utf-8') as g, open(linked_tsv, 'w', encoding='utf-8') as o:
            for g_line in g:
                d_gline = json.loads(g_line)
                g_key_list = get_key_list(log_info, **d_gline)
                g_link_pageid = g_key_list[7]
                # in case of multiple lines
                text_pre = g_key_list[3]
                g_key_list[3] = '\\n'.join(text_pre.splitlines())

                if get_title.get(g_link_pageid):
                    g_link_title = get_title[g_link_pageid]
                    g_key_list.insert(8, g_link_title)
                g_title_pageid = g_key_list[0]
                if get_title.get(g_title_pageid):
                    g_org_title = get_title[g_title_pageid]
                    g_key_list.insert(1, g_org_title)

                go_list.append(g_key_list)

            df_go = pd.DataFrame(go_list)
            df_go.to_csv(o, sep='\t', header=False, index=False)


def get_key_list(log_info, **tr):
    """get key list from input json dictionary to distinguish each record
    args:
        log_info
        **tr
    return:
        tmp_list
            format: [pageid, attribute, text, start_line_id, start_offset, end_line_id, end_offset, link_id]
    """

    import sys
    import logging
    logger = set_logging_pre(log_info, 'myPreLogger')
    logger.setLevel(logging.INFO)

    try:
        pid = tr['page_id']
    except (KeyError, ValueError) as ex:
        logger.error({
            'action': 'get_key_list',
            'error': ex,
            'tr': tr
        })
        sys.exit()

    try:
        at = tr['attribute']
    except (KeyError, ValueError) as ex:
        logger.error({
            'action': 'get_key_list',
            'error': ex,
            'tr': tr
        })
        sys.exit()

    if 'text_offset' not in tr:
        logger.error({
            'action': 'get_key_list',
            'error': 'format_error: text_offset',
            'tr': tr
        })
        sys.exit()
    else:
        if 'start' not in tr['text_offset']:
            logger.error({
                'action': 'get_key_list',
                'error': 'format_error: start(text_offset)',
                'tr': tr
            })
            sys.exit()
        else:
            if 'line_id' not in tr['text_offset']['start']:
                logger.error({
                    'action': 'get_key_list',
                    'error': 'format_error: line_id(start)',
                    'tr': tr
                })
                sys.exit()
            else:
                start_line_id = str(tr['text_offset']['start']['line_id'])

            if 'offset' not in tr['text_offset']['start']:
                logger.error({
                    'action': 'get_key_list',
                    'error': 'format_error: offset(start)',
                    'tr': tr
                })
                sys.exit()
            else:
                start_offset = str(tr['text_offset']['start']['offset'])

        if 'end' not in tr['text_offset']:
            logger.error({
                'action': 'get_key_list',
                'error': 'format_error: end(text_offset)',
                'tr': tr
            })
            sys.exit()
        else:
            if 'line_id' not in tr['text_offset']['end']:
                logger.error({
                    'action': 'get_key_list',
                    'error': 'format_error: line_id(end)',
                    'tr': tr
                })
                sys.exit()
            else:
                end_line_id = str(tr['text_offset']['end']['line_id'])

            if 'offset' not in tr['text_offset']['end']:
                logger.error({
                    'action': 'get_key_list',
                    'error': 'format_error: offset(end)',
                    'tr': tr
                })
                sys.exit()
            else:
                end_offset = str(tr['text_offset']['end']['offset'])

            if 'text' not in tr['text_offset']:
                logger.error({
                    'action': 'get_key_list',
                    'error': 'format_error: text(text_offset)',
                    'tr': tr
                })
                sys.exit()
            else:
                text = tr['text_offset']['text']

    if 'link_page_id' not in tr:
        link_id = ''
    else:
        link_id = tr['link_page_id']
    tmp_list = [pid, at, text, start_line_id, start_offset, end_line_id, end_offset, link_id]
    return tmp_list


if __name__ == '__main__':
    ljc_prep_main()
