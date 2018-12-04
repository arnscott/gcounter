import re
import time

import lib.queries as queries
import lib.sqlite


def get_sam_ids(conn):
    query = 'select distinct sam_id from results'
    results = conn.perform_raw_query(query)
    ids = [sam_id[0] for sam_id in results]
    return ids


def initialize_scoring_dictionary(conn):
    query = 'select distinct chromosome from results'
    results = conn.perform_raw_query(query)
    chromosomes = [chromosome[0] for chromosome in results]
    results_dictionary = {chromosome: 0 for chromosome in chromosomes}
    return results_dictionary


def results_dictionary(raw_results, exclude_sam_ids):
    sam_ids = {record.sam_id: set() for record in raw_results
                                    if record.sam_id not in exclude_sam_ids}
    for record in raw_results:
        if record.sam_id in sam_ids:
            sam_ids[record.sam_id].add(record.vcf_id)
    return sam_ids


def fetch_variants(conn, variant_set, exclude_sam_ids):
    query_string = ', '.join([str(variant) for variant in variant_set])
    potential_matches = conn.return_all_records(queries.GET_POTENTIAL_MATCHES.format(vcf_ids=query_string))
    sam_results = results_dictionary(potential_matches, exclude_sam_ids)
    return sam_results



def count_linked_snps(conn, variant_threshold):
    sam_ids = get_sam_ids(conn)
    match_count = 0
    already_matched = []
    total_results = initialize_scoring_dictionary(conn)
    linked_snp_families = []

    for count, sam_id in enumerate(sam_ids):
        matched = []
        if not sam_id in already_matched:
            read_results = conn.return_all_records(queries.GET_READ_RESULTS.format(sam_id=sam_id))
            if len(read_results) >= variant_threshold:
                chromosome = read_results[0].chromosome
                
                exclude_sam_ids = [sam_id]
                variants = [record.vcf_id for record in read_results]
                variant_set = set(variants)

                matches_exist = True
                while matches_exist:
                    results = fetch_variants(conn, variant_set, exclude_sam_ids)
                    if results:
                        for sid, potential_match_set in results.items():
                            if len(variant_set & potential_match_set) >= variant_threshold:
                                variant_set |= potential_match_set
                                already_matched.append(sid)
                                matched.append(sid)
                            exclude_sam_ids.append(sid)
                    else:
                        matches_exist = False
            if matched:
                match_count += 1
                matched_string = ', '.join([str(match) for match in matched])
                linked_snp_families.append((match_count, chromosome, matched_string))
                total_results[chromosome] += 1
                if match_count % 1000:
                    conn.load_records('linked_snp_families', linked_snp_families)
                    linked_snp_families = []
        exclude_sam_ids = []
        variants = []
    if linked_snp_families:
        conn.load_records('linked_snp_families', linked_snp_families)
        linked_snp_families = []
    print(total_results)



def get_chromosome_list(conn):
    chromosomes = []
    query = 'select distinct chromosome from vcfs'
    results = conn.perform_raw_query(query)
    chromosomes += [chromosome[0] for chromosome in results]
    return chromosomes 


def identify_variants(conn, rconn):
    start = time.clock()
    print('getting chromosome list')
    chromosomes = get_chromosome_list(conn)
    match = 0
    results_list = []

    print('iterating chromosomes')
    for chromosome in chromosomes:
        print('iterating vcfs', chromosome)
        vcf_query = queries.VCF_BY_CHROMOSOME.format(chromosome=chromosome)
        #print(vcf_query)
        for count, vcf in enumerate(conn.iterate_records(vcf_query)):
            sam_query = queries.RELATED_SAM.format(chromosome=chromosome,
                                                   position=vcf.position)
            sam_records = conn.return_all_records(sam_query)
            if sam_records:
                for sam in sam_records:
                    variant_location_difference = vcf.position - sam.pos -1
                    sam_sequence_base = sam.seq[variant_location_difference]
                    if sam_sequence_base == vcf.alternative:
                        match += 1
                        results_list += [(match,
                                          vcf.id,
                                          sam.id,
                                          chromosome,
                                          vcf.alternative,
                                          vcf.reference,
                                          vcf.position)]
                        if match % 1000 == 0:
                            print(count, match, 'chunk loading objects')
                            rconn.load_records('results', results_list)
                            results_list = []
                if count % 1000 == 0:
                    reached_1000 = time.clock() - start
                    print(count, reached_1000)
        if results_list:
            rconn.load_records('results', results_list)
            results_list = []



