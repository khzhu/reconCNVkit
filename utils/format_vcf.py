#!/usr/bin/env python3

import vcf
import sys
import os

if len(sys.argv) < 2:
    print("Missing a VCF.gz file")
else:
    input_vcf = sys.argv[1]
    out_vcf = input_vcf.replace("snp.tpanel.vcf.gz","filtered.snp.vcf")
    vcf_reader = vcf.Reader(filename=input_vcf)
    vcf_writer = vcf.Writer(open(out_vcf, 'w'), vcf_reader)
    for record in vcf_reader:
        #Strand read counts in VarScan2 VCF: ref/fwd, ref/rev, var/fwd, var/rev
        ref_fwd, ref_rev, alt_fwd, alt_rev = tuple(record.samples[0]['DP4'].strip().split(","))
        print(alt_fwd, alt_rev)
        record.INFO['SAF']=alt_fwd
        record.INFO['SAR']=alt_rev
        vcf_writer.write_record(record)
        vcf_writer.flush()
    vcf_writer.close()
