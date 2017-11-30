import csv
import re


class SAMFile(object):

    _sam_fields = ['QNAME',
                   'FLAG',
                   'RNAME',
                   'POS',
                   'MAPQ',
                   'CIGAR',
                   'RNEXT',
                   'PNEXT',
                   'TLEN',
                   'SEQ',
                   'QUAL']


    def __init__(self, file_path):
        self.file_path = file_path
        return

    def iterrecords(self):
        regex = r'([0-9]+[A-Z])'
        with open(self.file_path) as source:
            reader = csv.DictReader(source,
                                    fieldnames=self._sam_fields,
                                    delimiter='\t')
            for row in reader:
                if re.search(regex, row['CIGAR']):
                    yield {'QNAME': row['QNAME'],
                           'FLAG': row['FLAG'],
                           'RNAME': row['RNAME'],
                           'POS': row['POS'],
                           'MAPQ': row['MAPQ'],
                           'CIGAR': row['CIGAR'],
                           'RNEXT': row['RNEXT'],
                           'PNEXT': row['PNEXT'],
                           'TLEN': row['TLEN'],
                           'SEQ': row['SEQ'],
                           'QUAL': row['QUAL']}



def process_sam(file_path, output_file):
    sam_file = SAMFile(file_path)
    with open(output_file, 'w') as outfile:
        writer = csv.DictWriter(outfile,
                                fieldnames=sam_file._sam_fields)
        writer.writeheader()
        for row in sam_file.iterrecords():
            writer.writerow(row)


def process_vcf(file_path, number_of_lines, output_file):
    print('processing raw vcf file...')
    if number_of_lines == 'full':
        with open(file_path, 'r') as vcf_file, \
             open(output_file, 'w') as output_file:
            for row_number, row in enumerate(vcf_file):
                if not row[:2] == '##':
                    output_file.write(row)
    else:
        with open(file_path, 'r') as vcf_file:
            for row_number, row in enumerate(vcf_file):
                if not row[:2] == '##':
                    data_start = row_number
                    break

        with open(file_path, 'r') as vcf_file, \
             open(output_file, 'w') as output_file:
            for row_number, row in enumerate(vcf_file):
                if row_number >= data_start:
                    if row_number <= data_start + int(number_of_lines):
                        output_file.write(row)
