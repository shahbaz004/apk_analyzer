# Android APK Analysis Scripts

This repository contains a set of Python scripts for analyzing Android APK files and their source code. These scripts help in extracting valuable information such as control flow graphs, APIs, and permissions from Android applications.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Usage](#usage)
  - [APK Control Flow Graph Extraction](#apk-control-flow-graph-extraction)
  - [APIs Extraction](#apis-extraction)
  - [Permissions Extraction](#permissions-extraction)

## Prerequisites

Before using the scripts, you need to set up JADX by following the instructions provided in this [link](https://github.com/skylot/jadx). This is necessary for extracting control flow graphs and other information from APK files.


# APK Control Flow Graph Extractor

This Python script (`dex.py`) is used to extract `classes.dex` files from APKs within a specified folder and then extract control flow graphs (CFGs) from these `dex` files using JADX.

## Usage

1. Place the APK files you want to analyze in a folder (e.g., `apk_folder`).

2. Run the `dex.py` script using the following command:

```bash
python dex.py apps
```
# APIs Extractor

This Python script (`scripts/urls/api_calls_sources.py`) is used to extract all APIs from Sources Folder within a specified folder then create excel file.

```bash
python scripts/urls/api_calls_sources.py source_folder
```

# Permissions Extractor

This Python script (`scripts/permissions/permissions_sources_xlsx.py`) is used to extract all Permissions from Source Code folder then create excel file.

```bash
python scripts/permissions/permissions_sources_xlsx.py source_folder
```
