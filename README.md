# NGUD Text Transformation Tool

A Python tool that transforms Standard Greek text to a Northern Greek Urban Dialect (NGUD) representation, applying systematic phonological and orthographic rules.

## Overview

This script applies a set of linguistic transformations to Greek text, converting from Standard Modern Greek to a Northern Greek Urban Dialect representation. It handles various phonological rules including vowel deletions, transformations, and special cases while preserving grammatical structure and readability.

## Features

- Systematic transformation of Greek vowels according to dialectal rules
- Special handling for consonant clusters to maintain pronounceability
- Preservation of grammatical particles and special linguistic constructions
- Support for processing CoNLL-U formatted text files
- Intelligent application of rules with context awareness

## Installation

Clone this repository:

```bash
git clone https://github.com/yourusername/ngud-transformer.git
cd ngud-transformer

## Usage
The script accepts two command-line arguments: the input file path and the output file path.
bashCopypython creating-NGUD.py input_file.conllu output_file.conllu
