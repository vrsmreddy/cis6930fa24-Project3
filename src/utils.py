# src/utils.py
import urllib.request
import tempfile
import PyPDF2
import re
import os
import ssl
import certifi

def fetchincidents(url):
    """
    Fetch the PDF data from the given URL using certifi's CA bundle for SSL verification.
    """
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 "
                      "(KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    }
    request = urllib.request.Request(url, headers=headers)

    # Create an SSL context that uses certifi's certificate bundle
    context = ssl.create_default_context(cafile=certifi.where())

    with urllib.request.urlopen(request, context=context) as response:
        data = response.read()

    return data

def extractincidents(pdf_data):
    """
    Extract incident records from the given PDF data using PyPDF2.
    Returns a list of incidents, each being a list of 5 fields.
    """
    try:
        with tempfile.TemporaryFile() as tmp_file:
            tmp_file.write(pdf_data)
            tmp_file.seek(0)

            try:
                pdf = PyPDF2.PdfFileReader(tmp_file)
            except PyPDF2.utils.PdfReadError as e:
                print(f"PyPDF2 PdfReadError: {e}")
                return None
            except Exception as e:
                print(f"Unexpected error initializing PdfFileReader: {e}")
                return None

            num_pages = pdf.getNumPages()
            print(f"Number of pages in PDF: {num_pages}")

            incidents = []
            replacements = {
                "Date / Time Incident Number Location Nature Incident ORI": "",
                "Daily Incident Summary (Public)": "",
                "NORMAN POLICE DEPARTMENT": "\n",
                " \n": " "
            }

            for num in range(num_pages):
                try:
                    text = pdf.getPage(num).extractText()
                except Exception as e:
                    print(f"Error extracting text from page {num + 1}: {e}")
                    continue

                # Apply replacements
                for old, new in replacements.items():
                    text = text.replace(old, new)

                # Insert '||' before each incident date line to help split
                text = re.sub(r'\n(\d?\d/\d?\d/\d{4} )', r'\n||\1', text)

                # Split the text into entries
                entries = [entry.split('\n') for entry in text.strip().split('\n||')]
                incidents.extend(entries)

            # Filter entries to ensure each has exactly 5 fields
            formatted_data = [entry for entry in incidents if len(entry) == 5]

            # Further filter out any header-like entries
            formatted_data = [e for e in formatted_data if "Date" not in e[0] and "Time" not in e[0]]

            print(f"Number of incidents extracted: {len(formatted_data)}")

            return formatted_data
    except Exception as e:
        print(f"Unexpected error during PDF extraction: {e}")
        return None
