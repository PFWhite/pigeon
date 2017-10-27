import json
import time
import datetime
from copy import copy

from pigeon.exceptions import *
import pigeon.redcap_errors as redcap_errors
from pigeon.record_holder import RecordHolder

class UploadStrategy(object):

    def __init__(self, strategy, api, submit_format='csv'):
        """
        Strategies are
        'full'
        'batch'
        'single'

        submit_format determines the way that the file will be submitted to
        redcap. csv is recommended since its what redcap knows best
        """
        self.strategy = strategy
        self.api = api
        self.submit_format = submit_format

    def __call__(self, records, report, **upload_kwargs):
        self.upload_kwargs = upload_kwargs
        uploads = {
            'full': self.__full_upload,
            'batch': self.__batch_upload,
            'single': self.__single_upload,
        }
        report.num_records_attempted = len(records)
        if report.error_correction_attempts < 3:
            return uploads[self.strategy](records, report, **upload_kwargs)
        else:
            raise Exception('Attempted to correct errors too many times')

    def __response_parse(self, res):
        status = res.status_code
        text = str(res.content, 'utf-8')
        return json.loads(text)

    def __handle_errors(self, records, data, report):
        report.error_correction_attempts += 1
        errors = redcap_errors.parse_errors(data.get('error'))
        for error in errors:
            report.errors.append(copy(error))
        report.num_of_errors += len(errors)
        records = redcap_errors.remove_error_fields(records, errors)
        return self(records, report, **self.upload_kwargs)

    def __report_fill(self, records, data, report):
        report.subjects_uploaded = sorted(list(set(data + report.subjects_uploaded)))
        report.batch_end_time.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        report.num_records_uploaded += len(records)
        report.num_subjects_uploaded += len(report.subjects_uploaded)
        report.fields_updated += sum([len(record.keys()) - 2 for record in records])
        return report

    def __full_upload(self, records, report):
        """
        Takes records and a Reporter instance
        """
        records = RecordHolder(records)
        upload_data = records.dump(dump_format=self.submit_format)
        res = self.api.import_records(data=upload_data,
                                      adhoc_redcap_options={
                                          'format': self.submit_format
                                      })
        if (res.status_code == 403):
            raise TooManyRecords(res.content)
        if ('maximum submission size' in str(res.content, 'utf-8')):
            raise TooManyRecords(res.content)
        data = self.__response_parse(res)
        if type(data) == type({}) and 'error' in data.keys():
            return self.__handle_errors(records, data, report)
        else:
            self.__report_fill(records, data, report)
            report.strategy_used = 'full'
            return records, report

    def __batch_upload(self, records, report, batch_size=2000, between_batch_delay=5):
        batches = [[]]
        unfilled_batch = 0
        for record in records:
            if len(batches[unfilled_batch]) == batch_size:
                batches.append([])
                unfilled_batch += 1
            batches[unfilled_batch].append(record)
        rec_reports = []
        for batch in batches:
            rec_reports.append(self.__full_upload(batch, report))
            time.sleep(between_batch_delay)
        report.num_of_batches = len(batches)
        report.strategy_used = 'batch'
        altered_batches = [rec for rec, report in rec_reports]
        report = rec_reports[-1][1]
        return altered_batches, report

    def __single_upload(self, records, report):
        batches, report = self.__batch_upload(records, report, 1)
        report.strategy_used = 'single'
        return batches, report

