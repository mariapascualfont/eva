# ⬡ eva — AI shell assistant for bioinformaticians

Eva translates natural language into shell commands, with deep knowledge of bioinformatics tools like `samtools`, `bedtools`, `BLAST`, `GATK`, `BWA`, and more. Powered by **Google Gemini** — free to use via Google AI Studio, no credit card needed.

---

## Requirements

- Python 3.8+
- A free [Google Gemini API key](https://aistudio.google.com) (no credit card needed)

---

## Installation

### 1. Get your free Gemini API key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **Get API key** → **Create API key**
4. Copy the key and export it:

```bash
export GEMINI_API_KEY=your-key-here
# Add to ~/.bashrc or ~/.zshrc to make it permanent
```

### 2. Install Eva

```bash
cd eva/
pip install .
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
eva --explain                    Show explanation of the command (default: on)
eva --model gemini-1.5-pro       Use a different Gemini model
eva --list-tools                 List all bioinformatics tools Eva knows about
eva --version                    Show version
```

You can also override the model via environment variable:
```bash
export EVA_GEMINI_MODEL=gemini-1.5-pro
```

---

## How it works

1. You type a natural language query after `eva`.
2. Eva builds a domain-specific system prompt including a bioinformatics knowledge base.
3. The prompt is sent to the **Gemini API** (`gemini-2.0-flash` by default — free tier).
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

## Switching Gemini models

```bash
eva --model gemini-2.0-flash sort my bam file        # default, fastest, free
eva --model gemini-1.5-pro run fastqc on all samples # more powerful
```

Available free models: `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-1.5-pro`

---

## Troubleshooting

**`GEMINI_API_KEY not set`** — export your key:
```bash
export GEMINI_API_KEY=your-key-here
```

**`Invalid GEMINI_API_KEY (403)`** — double-check your key at [aistudio.google.com](https://aistudio.google.com).

**`Rate limit hit (429)`** — the free tier has per-minute limits. Wait a few seconds and retry.

**Wrong command** — try rephrasing more specifically, e.g. instead of *"align reads"* say *"align paired-end fastq reads with bwa mem to a reference genome"*.

---

## Project structure

```
eva/
├── eva.py          # CLI entry point (argparse)
├── eva_core.py     # Gemini API call, prompt building, output rendering
├── eva_tools.py    # Bioinformatics tool knowledge base
├── setup.py        # pip installation
└── README.md
```
