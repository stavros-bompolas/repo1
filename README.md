# NGUD CoNLL-U Transformation Tool

A Python tool that transforms Standard Greek CoNLL-U to a Northern Greek Dialect, applying systematic phonological and orthographic rules.

## Overview

This script applies a set of linguistic transformations to Standard Modern Greek CoNLL-U file, converting from Standard Modern Greek to a Northern Greek Dialect. It handles various phonological rules including northern vocalism (i.e., vowel raising and deletion), transformations, and special cases while preserving grammatical structure and readability.

## Features

- Systematic transformation of Greek vowels according to dialectal rules
- Special handling for consonant clusters to maintain pronounceability
- Preservation of grammatical particles and special linguistic constructions
- Support for processing CoNLL-U formatted text files
- Intelligent application of rules with context awareness

## Usage
The script accepts two command-line arguments: the input file path and the output file path.

python creating-NGUD.py input_file.conllu output_file.conllu
