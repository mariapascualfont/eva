# ⬡ eva — AI shell assistant for bioinformaticians

Eva translates natural language into shell commands, with deep knowledge of bioinformatics tools like `samtools`, `bedtools`, `BLAST`, `GATK`, `BWA`, and more. It runs entirely locally using [Ollama](https://ollama.com).

---

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com) running locally
- A pulled Ollama model (e.g. `llama3`, `mistral`, `gemma3`)

---

## Installation

### 1. Install Ollama and pull a model

```bash
# Install Ollama from https://ollama.com
ollama pull llama3        # recommended
# or: ollama pull mistral
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
eva --explain          Show explanation of the command (default: on)
eva --model mistral    Use a different Ollama model
eva --list-tools       List all bioinformatics tools Eva knows about
eva --version          Show version
```

---

## How it works

1. You type a natural language query after `eva`.
2. Eva builds a domain-specific prompt including a bioinformatics knowledge base.
3. The prompt is sent to your local Ollama model.
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

## Switching models

```bash
eva --model gemma3 sort my bam file
eva --model mistral run fastqc on all samples
```

---

## Troubleshooting

**`Cannot connect to Ollama`** — Make sure Ollama is running:
```bash
ollama serve
```

**Slow responses** — The first call loads the model into memory. Subsequent calls are faster.

**Wrong command** — Try rephrasing more specifically, or switch to a larger model (`llama3:70b`, `mixtral`).

---

## Project structure

```
eva/
├── eva.py          # CLI entry point (argparse)
├── eva_core.py     # Ollama API call, prompt building, output rendering
├── eva_tools.py    # Bioinformatics tool knowledge base
├── setup.py        # pip installation
└── README.md
```
