import json
import sys
from .exceptions import *

def clean_error(error):
    err = [part.replace('\"', '') for part in error.split(',')]
    return {
        'subject': err[0].split()[0],
        'event': err[0].split()[1].replace('(', '').replace(')', ''),
        'field': err[1],
        'value': err[2],
        'message': err[3],
        'original': error
    }

def parse_errors(error_data):
    """
    There are three sets of redcap errors: known parse errors with
    distinct signatures, parseable and recoverable errors which can be
    addressed, and unknown errors that are waiting to be discovered or have
    no discernable signature.

    This function first attempts to identify known ParseErrors and
    fail so the next strategy can be atttempted. Then it will try to recover
    from the "good" errors, and finally if that process excepts, we assume
    that there is something brand new that is a problem and will need to be
    addressed in a code change.
    """
    print(error_data, file=sys.stderr)
    if 'There were errors with your request.' in error_data:
        raise KnownParseError(error_data)
    if 'data being misformatted' in error_data:
        raise KnownParseError(error_data)
    try:
        return [clean_error(error) for error in error_data.split("\n") if error]
    except Exception as ex:
        raise UnknownParseError(error_data)

def remove_error_fields(records, errors):
    """
    This function takes recoverable errors and strips bad data out of the records
    object. There are times that the errors we get were parseable but not actually
    actionable. This happens purely by chance and since we dont know the signature
    of this type of error, we need to simply raise an exception and handle it later.
    """
    try:
        for error in errors:
            for index, record in enumerate(records):
                subject_has_err = str(error.get('subject')) == str(record.get('dm_subjid'))
                event_has_err = error.get('event') == record.get('redcap_event_name')
                if subject_has_err and event_has_err:
                    del records[index][error.get('field')]
        return records
    except Exception as ex:
        # we return json here because the errors have always been parsed by this point.
        raise RemoveErrorFieldsException(json.dumps(errors))
