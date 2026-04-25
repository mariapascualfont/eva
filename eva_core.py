"""
eva_core.py - Core logic for Eva: prompt construction, Ollama API, output rendering.
"""

import sys
import json
import textwrap
import requests
from eva_tools import TOOL_KNOWLEDGE, TOOL_LIST


SYSTEM_PROMPT = """You are Eva, an expert shell command assistant specialized in bioinformatics.
Your job is to translate natural language queries into precise shell commands.

You have deep knowledge of:
- Standard Unix/Linux shell commands (ls, grep, awk, sed, sort, find, cut, wc, cat, head, tail, mv, cp, rm, mkdir, etc.)
- Samtools: working with SAM/BAM/CRAM files (view, sort, index, flagstat, idxstats, depth, mpileup, etc.)
- Bedtools: genome arithmetic (intersect, merge, coverage, subtract, closest, slop, getfasta, etc.)
- BLAST: sequence similarity search (blastn, blastp, blastx, makeblastdb, etc.)
- BWA: read alignment (bwa mem, bwa index, bwa aln, etc.)
- STAR: RNA-seq alignment (STAR --runMode, --genomeGenerate, etc.)
- Bowtie2: short read alignment
- HISAT2: RNA-seq alignment
- featureCounts / HTSeq: read counting
- GATK: variant calling and processing
- BCFtools: VCF/BCF manipulation
- Trimmomatic / fastp: read trimming and QC
- FastQC: quality control
- MultiQC: aggregate QC reports
- Picard: BAM/SAM processing
- Seqtk: FASTQ/FASTA utilities
- VCFtools: VCF file processing
- BEDops: BED file operations

{tool_knowledge}

RULES:
1. Respond ONLY with a JSON object. No markdown, no extra text, no code fences.
2. The JSON must have exactly these fields:
   - "command": the shell command string (required)
   - "explanation": a one-sentence explanation of what the command does (required)
   - "confidence": one of "high", "medium", or "low" (required)
   - "warning": any important caveat or destructive risk (optional, null if none)
3. Use placeholder names like <input.bam>, <reference.fa>, <output.bam> when the user hasn't specified filenames.
4. Prefer composable pipelines using | when appropriate.
5. If a query is ambiguous, pick the most common bioinformatics interpretation.
6. Never refuse. Always suggest the best command you can.
"""


class EvaCore:
    OLLAMA_URL = "http://localhost:11434/api/generate"

    def __init__(self, model: str = "llama3"):
        self.model = model

    def _build_system_prompt(self) -> str:
        tool_knowledge_str = "\n\n".join(
            f"### {tool}\n{info}" for tool, info in TOOL_KNOWLEDGE.items()
        )
        return SYSTEM_PROMPT.format(tool_knowledge=tool_knowledge_str)

    def _call_ollama(self, query: str) -> dict:
        payload = {
            "model": self.model,
            "prompt": f"User query: {query}\n\nRespond with JSON only.",
            "system": self._build_system_prompt(),
            "stream": False,
            "format": "json",
        }

        try:
            response = requests.post(
                self.OLLAMA_URL,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            self._error(
                "Cannot connect to Ollama. Is it running?\n"
                "  Start it with: ollama serve\n"
                "  Then pull a model: ollama pull llama3"
            )
        except requests.exceptions.Timeout:
            self._error("Ollama request timed out. The model may be loading — try again.")
        except requests.exceptions.HTTPError as e:
            self._error(f"Ollama returned an error: {e}")

        raw = response.json().get("response", "")
        return self._parse_response(raw)

    def _parse_response(self, raw: str) -> dict:
        # Strip markdown fences if any
        raw = raw.strip()
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # Try to extract first JSON object from text
            import re
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group())
                except json.JSONDecodeError:
                    self._error(f"Eva couldn't parse the model response:\n{raw}")
            else:
                self._error(f"Eva couldn't parse the model response:\n{raw}")

        if "command" not in data:
            self._error("Model response missing 'command' field.")

        return data

    def run(self, query: str, explain: bool = False):
        self._print_header(query)

        result = self._call_ollama(query)

        command = result.get("command", "")
        explanation = result.get("explanation", "")
        confidence = result.get("confidence", "medium").lower()
        warning = result.get("warning")

        self._print_command(command)

        if warning:
            self._print_warning(warning)

        if explain or True:  # always show explanation for now
            self._print_explanation(explanation, confidence)

    def _print_header(self, query: str):
        print(f"\n\033[1;36m⬡ eva\033[0m \033[2m→ \"{query}\"\033[0m\n")

    def _print_command(self, command: str):
        # Syntax-highlight: bold green for the command
        print(f"  \033[1;32m$\033[0m \033[1m{command}\033[0m\n")

    def _print_explanation(self, explanation: str, confidence: str):
        confidence_colors = {
            "high":   "\033[32m●\033[0m",   # green
            "medium": "\033[33m●\033[0m",   # yellow
            "low":    "\033[31m●\033[0m",   # red
        }
        dot = confidence_colors.get(confidence, "\033[33m●\033[0m")
        wrapped = textwrap.fill(explanation, width=72, initial_indent="  ", subsequent_indent="  ")
        print(f"  {dot} {confidence.upper()} confidence\n{wrapped}\n")

    def _print_warning(self, warning: str):
        wrapped = textwrap.fill(warning, width=72, initial_indent="  ", subsequent_indent="    ")
        print(f"  \033[1;33m⚠\033[0m  {wrapped}\n")

    def _error(self, message: str):
        print(f"\n\033[1;31m✗ eva error:\033[0m {message}\n", file=sys.stderr)
        sys.exit(1)

    def print_known_tools(self):
        print("\n\033[1;36m⬡ eva\033[0m — known bioinformatics tools:\n")
        for tool in TOOL_LIST:
            print(f"  \033[1m{tool}\033[0m")
        print()
