# ⬡ eva — AI shell assistant for bioinformaticians

Eva translates natural language into shell commands, with deep knowledge of bioinformatics tools like `samtools`, `bedtools`, `BLAST`, `GATK`, `BWA`, and more. Powered by **Groq** — blazing fast inference, free tier, no credit card needed.

---

## Requirements

- Python 3.8+
- A free [Groq API key](https://console.groq.com) (no credit card needed)

---

## Installation

### 1. Get your free Groq API key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up with your Google or GitHub account — no credit card needed
3. Click **API Keys** → **Create API Key**
4. Copy the key and export it:

```bash
export GROQ_API_KEY=your-key-here
# Add to ~/.bashrc or ~/.zshrc to make it permanent
```

### 2. Install Eva

```bash
git clone https://github.com/mariapascualfont/eva.git
cd eva/
pip install .
```

*If pip install does not work due to the external environment, you can try:
```bash
pip install . --break-system-packages
```

This installs the `eva` command globally.

Or, without installing, run directly:

```bash
python eva.py list all sam files in this folder
```

---

## Usage

```
eva <natural language query>
```

### Examples

```bash
# Shell basics
eva list all files in this folder
eva find all fastq files recursively
eva count lines in myfile.txt

# Samtools
eva sort my BAM file by coordinate and index it
eva how many reads mapped in sample.bam
eva extract reads from chromosome 1 between 1000 and 5000
eva convert sam to bam

# Bedtools
eva find peaks that overlap with gene annotations
eva get fasta sequences under my peaks using the reference genome
eva compute coverage of reads over my BED regions

# BLAST
eva make a blast database from my protein fasta
eva run blastn against nt with tabular output and evalue cutoff 1e-10
eva search my sequences against a local nucleotide database

# GATK / bcftools
eva call variants from my bam file using bcftools
eva filter VCF to keep only PASS variants
eva run haplotypecaller in gvcf mode

# Trimming / QC
eva trim paired-end reads with fastp and generate a report
eva run fastqc on all fastq files in this directory
```

### Options

```
eva --explain                        Show explanation of the command (default: on)
eva --model llama3-70b-8192          Use a more powerful Groq model
eva --list-tools                     List all bioinformatics tools Eva knows about
eva --version                        Show version
```

You can also override the model via environment variable:
```bash
export EVA_GROQ_MODEL=mixtral-8x7b-32768
```

---

## How it works

1. You type a natural language query after `eva`.
2. Eva builds a domain-specific system prompt including a bioinformatics knowledge base.
3. The prompt is sent to the **Groq API** (`llama3-8b-8192` by default — free tier, very fast).
4. The model returns a JSON response with: `command`, `explanation`, `confidence`, and optional `warning`.
5. Eva prints the command and metadata in a clean, colored terminal output.

---

## Extending Eva

To add knowledge about a new tool, edit `eva_tools.py`:

```python
TOOL_KNOWLEDGE["mytool"] = """
Key mytool commands:
- mytool run: Does X. Flags: -i (input), -o (output), ...
"""

TOOL_LIST.append("mytool")
```

---

## Switching Groq models

```bash
eva --model llama3-8b-8192 sort my bam file         # default, fastest
eva --model llama3-70b-8192 run fastqc on all samples # smarter, still free
eva --model mixtral-8x7b-32768 call variants from bam  # great for complex queries
```

All models above are available on Groq's free tier.

---

## Troubleshooting

**`GROQ_API_KEY not set`** — export your key:
```bash
export GROQ_API_KEY=your-key-here
```

**`Invalid GROQ_API_KEY (401)`** — double-check your key at [console.groq.com](https://console.groq.com).

**`Rate limit hit (429)`** — Groq's free tier has per-minute limits. Wait a few seconds and retry.

**Wrong command** — try rephrasing more specifically, e.g. instead of *"align reads"* say *"align paired-end fastq reads with bwa mem to a reference genome"*. Switching to `llama3-70b-8192` also improves accuracy.

---

## Project structure

```
eva/
├── eva.py          # CLI entry point (argparse)
├── eva_core.py     # Groq API call, prompt building, output rendering
├── eva_tools.py    # Bioinformatics tool knowledge base
├── setup.py        # pip installation
└── README.md
```
