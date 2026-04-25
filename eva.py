#!/usr/bin/env python3
"""
eva - AI-powered shell command assistant for bioinformaticians
Uses the Groq API to translate natural language into shell commands.
"""

import argparse
import sys
import time
from eva_core import EvaCore

def animated_greeting():
    message = " Here is your bash command:"
    # Typing effect for the message
    sys.stdout.write("\033[1;32m")
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)
    sys.stdout.write("\033[0m\n")

def print_welcome():
    """Prints a friendly welcome message for the user."""
    print("\033[1;36m" + "═" * 50)
    print(" ⬡  Welcome to Eva: Your Bioinformatics AI Assistant")
    print("    Type your request in natural language.")
    print("═" * 50 + "\033[0m")

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
        default="llama-3.1-8b-instant",
        help="Groq model to use (default: llama-3.1-8b-instant). Other options: llama-3.1-70b-versatile, mixtral-8x7b-32768. Can also set EVA_GROQ_MODEL env var.",
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

    print_welcome()

    if not args.query and not args.list_tools:
        parser.print_help()
        sys.exit(0)

    eva = EvaCore(model=args.model)

    if args.list_tools:
        eva.print_known_tools()
        return

    query = " ".join(args.query)
    animated_greeting()
    eva.run(query, explain=args.explain)


if __name__ == "__main__":
    main()
