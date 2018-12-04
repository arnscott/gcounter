VCF_BY_CHROMOSOME = """\
select
  id,
  chromosome,
  position,
  reference,
  alternative
from
  vcfs
where
  chromosome = '{chromosome}'
order by
  position"""

RELATED_SAM = """\
select
  id,
  rname,
  pos,
  length,
  end_pos,
  cigar,
  seq
from
  sams
where
  rname = '{chromosome}' and
  pos < {position} and
  end_pos > {position}"""

CREATE_VCF_TABLE = """\
create table vcfs (
  id integer primary key,
  chromosome text,
  position integer,
  identity text,
  reference text,
  alternative text,
  quality text,
  filtering text,
  info text,
  formatting text,
  data text
)"""

CREATE_SAMS_TABLE = """\
create table sams (
  id integer primary key,
  qname text,
  flag text,
  rname text,
  pos integer,
  length integer,
  end_pos interger,
  mapq text,
  cigar text,
  rnext text,
  pnext text,
  tlen text,
  seq text,
  qual text
)"""

CREATE_RESULTS_TABLE = """\
create table results (
  id integer primary key,
  vcf_id integer,
  sam_id integer,
  chromosome text,
  alternative text,
  reference text,
  position integer
)"""



CREATE_LINKED_SNP_FAMILIES_TABLE = """\
create table if not exists linked_snp_families (
  id integer primary key,
  chromosome text,
  sam_ids text
)"""


CREATE_LINKED_SNP_FAMILY_DATA_TABLE = """\
create table if not exists linked_snp_data_table (
  id integer primary key,
  linked_snp_family_id integer,
  chromosome text,
  alternative text,
  reference text,
  position integer
)"""



GET_READ_RESULTS = """\
select
  id,
  vcf_id,
  sam_id,
  chromosome,
  alternative,
  reference,
  position
from
  results
where
  sam_id = {sam_id}"""

GET_POTENTIAL_MATCHES = """\
select
  id,
  vcf_id,
  sam_id,
  chromosome,
  alternative,
  reference,
  position
from
  results
where
  vcf_id in ({vcf_ids})"""
