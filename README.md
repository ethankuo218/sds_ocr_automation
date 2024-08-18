# SDS OCR Automation

This project automates the extraction of key information from Safety Data Sheets (SDS) using Optical Character Recognition (OCR).

## Project Overview

The SDS OCR Automation tool processes image files of Safety Data Sheets and extracts specific properties such as physical state, color, odor, pH, boiling point, flash point, and viscosity. It then compiles this information into an Excel spreadsheet for easy analysis.

## Features

- Processes multiple SDS images
- Extracts key properties from SDS documents
- Outputs results to an Excel file
- Handles multiple pages per SDS document

## Prerequisites

- Python 3.12
- OpenCV
- Tesseract OCR
- pandas
- pytesseract

## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install required packages
4. Ensure Tesseract OCR is installed and accessible in your PATH

## Usage

1. Place SDS image files in the `sds` directory
2. Run `pre-generate-images.py`, it will generate images first and place in `images` directory
3. Run `python main.py`
4. Check `output.xlsx` for results
