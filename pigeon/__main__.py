docstr = """
Pigeon

Usage: pigeon.py [-hc] (<file> <config>) [-o <output.json>]
pigeon.py [-hc] (<file> <token> <url>) [-o <output.json>]

Options:
  -h --help                                     show this message and exit
  -v --version                                  show version
  -o=<output.json> --output=<output.json>       optional output file for results
  -c --csv                                      use csv as the import format

"""
import json
import datetime
import csv
from copy import copy
import os

from docopt import docopt
import yaml
import cappy

from .reporter import Reporter
from .upload_strategy import UploadStrategy
from .exceptions import *
from .risk_manager import RiskManager
from pigeon.version import __version__

_file = '<file>'
_config = '<config>'
_output = '--output'
_token = '<token>'
_url = '<url>'

# config file magic strings
_cv = 'cappy_version'
_tk = 'token'
_ru = 'redcap_url'
_ro = 'requests_options'
_bs = 'batch_size'
_sf = 'submit_format'

def main(args):
    global config
    if args.get(_config):
        with open(args[_config], 'r') as config_file:
            config = yaml.load(config_file.read())
    else:
        config = {
            _ru: args.get(_url),
            _tk: args.get(_token),
        }

    with open(args[_file], 'r') as infile:
        records_str = infile.read()

    api = cappy.API(config[_tk], config[_ru], config.get(_cv) or 'master.yaml', requests_options=config.get(_ro))

    report_template = {
        'file_loaded': os.path.abspath(args[_file]),
        'num_records_attempted': 0,
        'num_subjects_uploaded': 0,
        'num_records_uploaded': 0,
        'num_of_errors': 0,
        'subjects_uploaded': [],
        'original_errors': [],
        'errors': [],
        'error_correction_attempts': 0,
        'fields_updated': 0,
        'start_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'batch_end_time': [],
        'num_of_batches': 1,
        'strategy_used': "",
    }

    with open(args[_file], 'r') as infile:
        if args.get('--csv'):
            records = list(csv.DictReader(infile))
        else:
            records = json.load(infile)
    report = Reporter('pigeon_v1', report_template, no_reset=[
        'original_errors'
    ])
    batch_upload = UploadStrategy('batch', api)
    single_upload = UploadStrategy('single', api)

    upload = RiskManager(lambda : batch_upload(records, report))
    upload.add_backup(lambda ex: single_upload(records, report.reset().add_key_value('full_ex', ex)))

    result, successful_plan = upload()

    report.add_key_value('exceptions', [ex for ex in upload.exceptions_encountered])

    if not args.get(_output):
        print(report.serialize())
    else:
        with open(args.get(_output), 'w') as outfile:
            outfile.write(report.serialize())

def cli_run():
    args = docopt(docstr, version='Pigeon %s' % __version__)
    main(args)

if __name__ == '__main__':
    cli_run()
    exit()
