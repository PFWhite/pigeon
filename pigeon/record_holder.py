import csv
import json
from itertools import chain

class FakeFile(object):
    def __init__(self):
        self.lines = []

    def write(self, text):
        self.lines.append(text)

    def __str__(self):
        return ''.join(self.lines)


class RecordHolder(object):
    """
    This class is used to wrap the records that are loaded into pigeon
    so it can support json like operations as well as csv like operations
    transparently
    """
    def __init__(self, record_data):
        """
        the record_data parameter will be a list of dictionaries.
        each individual dictionary may not contain every key.
        this is important when dumping to csv
        """
        self._records = record_data
        self._headers = set(chain(*[record.keys() for record in self._records]))

    def dump(self, dump_format='csv'):
        """
        Serialize as a utf8 string that can be loaded into redcap
        Format can be either csv or json
        """
        if dump_format == 'csv':
            fake_file = FakeFile()
            writer = csv.DictWriter(fake_file, fieldnames=self._headers)
            writer.writeheader()
            writer.writerows(self._records)
            return fake_file
        elif dump_format == 'json':
            return json.dumps(self._records)

    def __len__(self):
        """
        Return the number of records underlying
        """
        return len(self._records)

    def __iter__(self):
        """
        When iterating over a class this allows one to set up the variables you need
        to keep track of what is going on
        """
        self._current_index = 0
        return self

    def __getitem__(self, key):
        return self._records[key]

    def __setitem__(self, key, value):
        self._records[key] = value

    def __next__(self):
        """
        Called in order to get the next item in when iterating through a Records instance
        """
        current = self._current_index
        self._current_index += 1
        try:
            return self._records[current]
        except:
            del self._current_index
            raise StopIteration
