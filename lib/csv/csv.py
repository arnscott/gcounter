"""
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""




import datetime
import csv
import os


class CSVReader(object):
    """Wrapper for reading csv files.
    Takes just the filepath as an argument.

    Use the iterrecords() generator method for large data sets for increased performance.
    """
    def __init__(self, file_path, delimiter=','):
        self.file_path = file_path
        self.delimiter = delimiter
        
    def read_to_list(self):
        """Returns the records in the csv as a list[] 
        Each record is a dictionary
        """
        records = []
        with open(self.file_path) as source:
            reader = csv.DictReader(source,
                                    delimiter=self.delimiter)
            for row in reader:
                records.append(row)
        return records

    def read_to_dict(self, key_field):
        """Returns the records in the csv as a dictionary.
        The key value is specified by the key_field argument for each record
        """
        records = {}
        with open(self.file_path) as source:
            reader = csv.DictReader(source, 
                                    delimiter=self.delimiter)
            self.headers = reader.fieldnames
            if key_field in self.headers:
                for row in reader:
                    if not row[key_field] in records:
                        records[row[key_field]] = row
                    else:
                        raise Exception('The key provided does not have unique values.')
            else:
                raise KeyError('The key provided does not exist')
        return records
    
    def iterrecords(self):
        """Generator method that provides a more efficient way to iterate records.

        for record in instance.iterrecords():
            print(record)
        """
        records = []
        with open(self.file_path) as source:
            reader = csv.DictReader(source, 
                                    delimiter=self.delimiter)
            for row in reader:
                yield row



class CSVWriter(object):
    """Wrapper for writing csv files.
    takes the file path and a list of headers as arguments
    """
    def __init__(self, file_path, headers):
        self.headers = headers
        self.file_path = file_path

    def write_from_list(self, records=[]):
        """Writes the csv to the indicated file_path
        taking a list[] of records as the argument
        where each record is a dictionary.

        Only the fields in self.headers will be written to the csv.
        But extra fields can be passed, they will just be skipped over.
        """
        if isinstance(records, list):
            with open(self.file_path, 'w') as csvfile:
                writer = csv.DictWriter(csvfile,
                                        fieldnames=self.headers)
                writer.writeheader()
                for record in records:
                    if isinstance(record, dict):
                        row = {field: record[field] for field in self.headers}
                        writer.writerow(row)
                    else:
                        raise Exception('Items in list must be of type dict')
        else:
            raise Exception('Must pass a list object as the records list')
        return self.file_path

    def write_from_dict(self, records={}):
        """Writes the csv to the indicated file_path
        taking a dict{} of records as the argument
        where each item in the dict{} is also a dict{}
        """
        with open(self.file_path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=self.headers)
            writer.writeheader()
            for key, record in records.items():
                row = {field: record[field] for field in self.headers}
                writer.writerow(row)
        return self.file_path


def reader(file_path='', delimiter=','):
    """Returns a CSVReader object
    """
    if os.path.isfile(file_path):
        if os.access(file_path, os.R_OK):
            return CSVReader(file_path, delimiter=delimiter)
        else:
            raise Exception('{fname} exists but is not readable.'.format(fname=file_path))
    else:
        raise Exception('{fname} does not exist'.format(fname=file_path))

def writer(file_path='', headers=[]):
    """Returns a CSVWriter object
    """
    if not os.path.isfile(file_path):
        if isinstance(headers, list):
            return CSVWriter(file_path=file_path, headers=headers)
        else:
            raise Exception('Headers need to be in a list object.')
    else:
        raise Exception('{fname} is already a file. Please write to a new location.'.format(fname=file_path))
    



def the_date():
    return datetime.date.today().strftime('%m_%d_%Y')







