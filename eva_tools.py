"""
eva_tools.py - Bioinformatics tool knowledge base.
This is injected into the LLM system prompt to give Eva domain-specific expertise.
"""

TOOL_LIST = [
    "samtools",
    "bedtools",
    "blast (blastn, blastp, blastx, makeblastdb)",
    "bwa",
    "bowtie2",
    "STAR",
    "HISAT2",
    "featureCounts",
    "HTSeq",
    "GATK",
    "bcftools",
    "Trimmomatic",
    "fastp",
    "FastQC",
    "MultiQC",
    "Picard",
    "seqtk",
    "vcftools",
    "bedops",
    "awk, grep, sed, sort, uniq, cut, wc",
]

TOOL_KNOWLEDGE = {
    "samtools": """
Key samtools commands and their flags:
- samtools view: Convert/filter SAM/BAM/CRAM. Flags: -b (output BAM), -h (include header), -f (include flag), -F (exclude flag), -q (min mapQ), -@ (threads), -o (output file)
- samtools sort: Sort alignments. Flags: -o (output), -@ (threads), -n (sort by name), -t (sort by tag)
- samtools index: Index BAM/CRAM. Creates .bai or .crai file.
- samtools flagstat: Summary statistics of flags in BAM.
- samtools idxstats: Per-chromosome read counts.
- samtools depth: Per-base coverage depth. Flags: -a (all positions), -d (max depth)
- samtools mpileup: Multi-sample pileup. Flags: -f (reference fasta), -q (min baseQ), -Q (min mapQ)
- samtools merge: Merge multiple BAM files. Flags: -f (force overwrite), -@ (threads)
- samtools rmdup: Remove PCR duplicates (legacy; prefer Picard MarkDuplicates or samtools markdup)
- samtools markdup: Mark/remove duplicates. Flags: -r (remove duplicates), -@ (threads)
- samtools fasta/fastq: Convert BAM to FASTA/FASTQ.
- samtools stats: Comprehensive statistics.
- samtools quickcheck: Quickly check BAM files are intact.
- samtools calmd: Recalculate MD tag and NM tag.
- samtools addreplacerg: Add or replace read group tags.

Common workflows:
- Align → sort → index: bwa mem ref.fa r1.fq r2.fq | samtools sort -o out.bam && samtools index out.bam
- Count mapped reads: samtools view -c -F 4 input.bam
- Extract reads from region: samtools view -b input.bam chr1:1000-2000 > region.bam
- Convert SAM to BAM: samtools view -bS input.sam -o output.bam
""",

    "bedtools": """
Key bedtools commands and their flags:
- bedtools intersect: Find overlapping intervals. Flags: -a (file A), -b (file B), -v (only non-overlapping), -wa (write A), -wb (write B), -u (unique), -c (count), -f (min overlap fraction), -r (require reciprocal), -s (strand-specific), -S (opposite strand)
- bedtools merge: Merge overlapping intervals. Flags: -i (input), -d (max distance to merge), -c (columns), -o (operations)
- bedtools subtract: Subtract B from A. Flags: -a, -b, -s (strand), -f (min overlap)
- bedtools coverage: Compute coverage. Flags: -a, -b, -d (per-base), -mean, -hist
- bedtools closest: Find closest features. Flags: -a, -b, -d (report distance), -s (strand), -t (tie handling)
- bedtools slop: Extend intervals. Flags: -i (input), -g (genome file), -b (both sides), -l (left), -r (right), -s (strand-based)
- bedtools getfasta: Extract sequences using BED. Flags: -fi (fasta), -bed (bed file), -fo (output), -s (strand), -name (use name field)
- bedtools sort: Sort BED file. Flags: -i (input), -g (genome)
- bedtools genomecov: Genome-wide coverage. Flags: -ibam (BAM input), -bg (bedgraph output), -bga (include zero coverage), -d (per-base depth), -g (genome file)
- bedtools window: Similar to intersect but with a window around features. Flags: -a, -b, -w (window size), -l, -r
- bedtools makewindows: Create tiling windows across genome. Flags: -g (genome), -w (window size), -s (step)
- bedtools shuffle: Randomly relocate intervals. Flags: -i, -g, -excl (exclude regions)
- bedtools fisher: Fisher's test on interval overlap.
- bedtools jaccard: Jaccard statistic for interval similarity.

Common workflows:
- Find peaks overlapping genes: bedtools intersect -a peaks.bed -b genes.bed -wa -wb
- Get sequences under peaks: bedtools getfasta -fi genome.fa -bed peaks.bed -fo peaks.fa -s
- Coverage of BAM over BED: bedtools coverage -a regions.bed -b reads.bam
""",

    "blast": """
Key BLAST commands:
- makeblastdb: Create BLAST database. Flags: -in (input fasta), -dbtype (nucl/prot), -out (db prefix), -title, -parse_seqids
- blastn: Nucleotide vs nucleotide. Flags: -query, -db, -out, -outfmt, -evalue, -num_threads, -perc_identity, -word_size, -max_target_seqs, -max_hsps
- blastp: Protein vs protein. Same flags as blastn plus -matrix (BLOSUM62 etc.)
- blastx: Translated nucleotide vs protein.
- tblastn: Protein vs translated nucleotide.
- tblastx: Translated nucleotide vs translated nucleotide.

Output formats (-outfmt):
- 0: Pairwise (default)
- 6: Tabular (qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore)
- 7: Tabular with comments
- 10: CSV
- Custom: "6 qseqid sseqid pident evalue bitscore"

Common workflows:
- Make DB and search: makeblastdb -in db.fa -dbtype nucl -out mydb && blastn -query query.fa -db mydb -out results.txt -outfmt 6 -evalue 1e-5
- Remote BLAST: blastn -query query.fa -db nt -remote -outfmt 6 -out results.txt
- Filter by identity: blastn -query q.fa -db mydb -outfmt 6 | awk '$3>=90' > filtered.txt
""",

    "bwa": """
Key BWA commands:
- bwa index: Index reference genome. Flags: -a (algorithm: bwtsw for large genomes, is for small)
- bwa mem: Align reads (recommended for reads >70bp). Flags: -t (threads), -R (read group header), -M (mark split hits), -p (interleaved paired-end)
- bwa aln: Align reads <70bp (legacy). Flags: -t (threads), -n (max mismatches)
- bwa sampe/samse: Generate SAM for paired/single end after bwa aln.

Common workflows:
- Index + align paired-end: bwa index ref.fa && bwa mem -t 8 -R '@RG\\tID:sample\\tSM:sample\\tPL:ILLUMINA' ref.fa r1.fq r2.fq | samtools sort -o out.bam && samtools index out.bam
""",

    "bcftools": """
Key bcftools commands:
- bcftools view: View/filter VCF/BCF. Flags: -f (filter expression), -s (samples), -r (regions), -t (targets), -i (include), -e (exclude), -O (output type: z=gzvcf, b=bcf), -o (output)
- bcftools call: Variant calling. Flags: -m (multiallelic model), -v (variants only), -o, -O
- bcftools mpileup: Pileup for variant calling. Flags: -f (reference), -r (region), -a (annotations)
- bcftools filter: Apply filters. Flags: -i/-e (include/exclude expression), -s (soft filter name), -m (mode)
- bcftools sort: Sort VCF.
- bcftools index: Index VCF/BCF. Flags: -t (tabix for vcf.gz), -c (csi)
- bcftools merge: Merge VCF files. Flags: -m (merge strategy), -O, -o
- bcftools concat: Concatenate VCF files (same samples). Flags: -a (allow overlaps)
- bcftools annotate: Add/remove annotations. Flags: -a (annotation file), -c (columns), -x (remove)
- bcftools stats: Statistics on VCF. Flags: -r (region), -s (samples)
- bcftools norm: Normalize indels. Flags: -f (reference), -m (multiallelic handling)
- bcftools query: Extract fields from VCF. Flags: -f (format string), -s, -r, -i/-e

Common workflows:
- Call variants: bcftools mpileup -f ref.fa input.bam | bcftools call -mv -Oz -o variants.vcf.gz && bcftools index -t variants.vcf.gz
- Filter PASS variants: bcftools view -f PASS input.vcf.gz -Oz -o pass.vcf.gz
- Extract specific fields: bcftools query -f '%CHROM\\t%POS\\t%REF\\t%ALT\\t%QUAL\\n' input.vcf
""",

    "GATK": """
Key GATK tools:
- HaplotypeCaller: Call SNPs and indels. Flags: -R (reference), -I (input BAM), -O (output VCF), -ERC (emit ref confidence: GVCF), --sample-ploidy
- GenotypeGVCFs: Genotype GVCFs. Flags: -R, -V (input gvcf), -O
- CombineGVCFs: Combine GVCFs for joint calling. Flags: -R, -V (multiple), -O
- GenomicsDBImport: Import GVCFs into GenomicsDB.
- BaseRecalibrator: BQSR step 1. Flags: -R, -I, --known-sites, -O (recal table)
- ApplyBQSR: BQSR step 2. Flags: -R, -I, --bqsr-recal-file, -O
- MarkDuplicates (Picard-style): Mark duplicates. Flags: -I, -O, -M (metrics)
- SelectVariants: Select variant types. Flags: --select-type-to-include SNP/INDEL
- VariantFiltration: Apply hard filters. Flags: --filter-expression, --filter-name
- Mutect2: Somatic variant calling. Flags: -R, -I (tumor), -I (normal), --tumor-sample, --normal-sample, -O
""",

    "fastp": """
fastp: Fast all-in-one FASTQ preprocessor.
Flags: -i/-I (input R1/R2), -o/-O (output R1/R2), -j (JSON report), -h (HTML report), -w (threads), -q (quality threshold), -l (min length), --detect_adapter_for_pe, -p (paired-end), --dedup, -f/-t (front/tail trim bp), --umi, -e (avg quality)

Common: fastp -i r1.fq.gz -I r2.fq.gz -o r1_clean.fq.gz -O r2_clean.fq.gz -j report.json -h report.html -w 8
""",

    "featureCounts": """
featureCounts (Subread package): Count reads over genomic features.
Flags: -a (GTF/GFF), -o (output), -T (threads), -p (paired-end), -s (strandedness: 0=unstranded, 1=stranded, 2=reverse), -t (feature type: exon), -g (group by: gene_id), -M (multi-mapping), --primary, -B (both ends mapped), -C (chimeric fragments not counted)

Common: featureCounts -a annotation.gtf -o counts.txt -T 8 -p -s 2 sample1.bam sample2.bam
""",
}
