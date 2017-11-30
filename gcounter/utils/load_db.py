#!/usr/bin/env python
import re

import lib.csv
import lib.queries as queries
import lib.sqlite

def load_database(args, conn):

    cigar_length_pattern = r'[0-9]+'
    if args.data_type == 'sam':
        conn.perform_raw_sql(queries.CREATE_SAMS_TABLE)
        sam_file = lib.csv.reader(file_path=args.source_data)
        bulk_list = []
        for count, row in enumerate(sam_file.iterrecords()):
            length = int(re.findall(cigar_length_pattern, row['CIGAR'])[0])
            end_position = int(row['POS']) + length
            bulk_list += [(count,
                           row['QNAME'],
                           row['FLAG'],
                           row['RNAME'],
                           row['POS'],
                           length,
                           end_position,
                           row['MAPQ'],
                           row['CIGAR'],
                           row['RNEXT'],
                           row['PNEXT'],
                           row['TLEN'],
                           row['SEQ'],
                           row['QUAL'])]
            if count % 10000 == 0:
                print(count)
                conn.load_records('sams', bulk_list)
                bulk_list = []
        conn.load_records('sams', bulk_list) 
        print('creating indices')
        conn.perform_raw_sql('create index sams_idx on sams (rname, pos, end_pos)')
    if args.data_type == 'vcf':
        conn.perform_raw_sql(queries.CREATE_VCF_TABLE)
        vcf_file = lib.csv.reader(file_path=args.source_data,
                                  delimiter='\t')
        bulk_list = []
        for count, row in enumerate(vcf_file.iterrecords()):
            bulk_list += [(count,
                           row['#CHROM'],
                           row['POS'],
                           row['ID'],
                           row['REF'],
                           row['ALT'],
                           row['QUAL'],
                           row['FILTER'],
                           row['INFO'],
                           row['FORMAT'],
                           row['String'])]
            if count % 10000 == 0:
                conn.load_records('vcfs', bulk_list)
                bulk_list = []
        conn.load_records('vcfs', bulk_list)
        print('creating indices')
        conn.perform_raw_sql('create index vcf_idx on vcfs (chromosome, position)')

