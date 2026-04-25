#!/usr/bin/env python3
"""
eva - AI-powered shell command assistant for bioinformaticians
Uses the Google Gemini API to translate natural language into shell commands.
"""

import argparse
import sys
from eva_core import EvaCore


def main():
    parser = argparse.ArgumentParser(
        prog="eva",
        description="Eva: AI shell assistant for bioinformaticians",
        usage="eva [options] <natural language query>",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  eva list all files in this folder
  eva sort my BAM file by coordinate
  eva find sequences matching ATCG in my fasta file using blast
  eva how many reads are in sample.bam
  eva convert sam to bam and index it
  eva run bedtools intersect between peaks.bed and genes.bed
        """,
    )

    parser.add_argument(
        "query",
        nargs=argparse.REMAINDER,
        help="Natural language description of what you want to do",
    )

    parser.add_argument(
        "--model",
        default="gemini-2.0-flash",
        help="Gemini model to use (default: gemini-2.0-flash). Can also set EVA_GEMINI_MODEL env var.",
    )

    parser.add_argument(
        "--explain",
        action="store_true",
        help="Also print an explanation of the suggested command",
    )

    parser.add_argument(
        "--list-tools",
        action="store_true",
        help="List all bioinformatics tools Eva knows about",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="eva 1.0.0",
    )

    args = parser.parse_args()

    eva = EvaCore(model=args.model)

    if args.list_tools:
        eva.print_known_tools()
        return

    if not args.query:
        parser.print_help()
        sys.exit(1)

    query = " ".join(args.query)
    eva.run(query, explain=args.explain)


if __name__ == "__main__":
    main()
