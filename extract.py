import zipfile
import os
import xml.etree.ElementTree as ET
import pandas as pd

# Define the XML namespace
NAMESPACE = {'ns': 'http://www.portalfiscal.inf.br/nfe'}

# Directory where the zip files are stored
zip_files_directory = './invoices'
output_csv_path = 'extraction_result.csv'

# Container to hold all extracted data
all_ncm_product_data = []

# Process each zip file in the specified directory
for zip_filename in os.listdir(zip_files_directory):
    if zip_filename.endswith('.zip'):
        zip_file_path = os.path.join(zip_files_directory, zip_filename)
        extracted_folder_path = zip_file_path.replace('.zip', '_extracted/')
        
        # Check if the folder already exists
        if not os.path.exists(extracted_folder_path):
            print(f"Extracting {zip_file_path} to {extracted_folder_path}")
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(extracted_folder_path)
        else:
            print(f"Already extracted: {zip_file_path}")
        
        # Process each XML file in the extracted folder
        for root, dirs, files in os.walk(extracted_folder_path):
            for file in files:
                if file.endswith('.xml'):
                    xml_file_path = os.path.join(root, file)
                    try:
                        tree = ET.parse(xml_file_path)
                        root_element = tree.getroot()

                        # Start navigating XML structure with debug output at each level
                        nfeProc = root_element.find("ns:NFe", NAMESPACE)
                        if nfeProc is not None:
                            NFe = nfeProc.find("ns:infNFe", NAMESPACE)
                            if NFe is not None:
                                # Extract ide section
                                ide = NFe.find("ns:ide", NAMESPACE)
                                if ide is not None:
                                    nNF = ide.findtext('ns:nNF', namespaces=NAMESPACE)
                                    dhEmi = ide.findtext('ns:dhEmi', namespaces=NAMESPACE)

                                # Extract prod section
                                for product in NFe.findall(".//ns:det/ns:prod", NAMESPACE):
                                    ncm = product.findtext('ns:NCM', namespaces=NAMESPACE)
                                    name = product.findtext('ns:xProd', namespaces=NAMESPACE)

                                    if ncm and name and nNF and dhEmi:
                                        all_ncm_product_data.append({
                                            "NCM": ncm,
                                            "Product Name": name,
                                            "Invoice Number (nNF)": nNF,
                                            "Emission Date (dhEmi)": dhEmi
                                        })
                                    else:
                                        print(f"Missing data fields in entry for file: {xml_file_path}")
                            else:
                                print(f"infNFe not found in NFe for file: {xml_file_path}")
                        else:
                            print(f"nfeProc not found in XML for file: {xml_file_path}")

                    except ET.ParseError as e:
                        print(f"XML parsing error in file {xml_file_path}: {e}")
                        continue

# Convert the collected data into a DataFrame and save as CSV
df_all_ncm_product = pd.DataFrame(all_ncm_product_data)
df_all_ncm_product.to_csv(output_csv_path, index=False)

print(f"\nData extraction complete. CSV saved as: {output_csv_path}")