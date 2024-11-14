# NFe Field Extractor

A simple Python script to extract key fields (NCM, product name, invoice number, and
emission date) from Brazilian NFe XML files within ZIP archives.

## Requirements

- Python 3.6 or higher

## Usage

### 1. Clone this repository:

```bash
git clone https://github.com/nGoline/nfe_field_extractor
cd nfe_field_extractor
```

### 2. Set up a Python virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### 4. Prepare your input files:

Place all your ZIP files containing NFe XML files into the `invoices` directory within
the project folder.

### 5. Run the extraction script:

```bash
python extract.py
```

The script will process each ZIP file in the `invoices` folder, extract the relevant
fields, and save the data to `extraction_result.csv` in the project
folder.

## Output

After the script finishes running, you’ll find the output CSV file:
- `extraction_result.csv` in the main project directory.

This CSV will contain columns for:
- **NCM**: The NCM code for each product
- **Product Name**: The name of each product
- **Invoice Number (nNF)**: The invoice number
- **Emission Date (dhEmi)**: The emission date of the invoice

## Troubleshooting

If the script fails to find certain fields, ensure the XML files follow the standard NFe
structure. The script includes debug logs to help identify any missing fields or
structural issues.