#!/usr/bin/env python3
"""
peek.py - Lightweight, dependency-free CLI tool to preview the header and
first N rows of a dataset, whether it's CSV or JSON (array, JSON Lines,
or a dict with a records list).

Usage:
    peek data.csv
    peek data.json -n 5
    peek data.jsonl
    peek data.jsonl --html -n 5
"""
if __name__ == '__main__':
    from thaakz.utils import peek_dataset
    peek_dataset()
