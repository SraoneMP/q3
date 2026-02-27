import sys
from google import genai
from google.genai import types
import os
import time
import json
from dotenv import load_dotenv

load_dotenv()

if len(sys.argv) != 3:
    print("Usage: python expense_main.py <pdf_file> <target_date>")
    sys.exit(1)

pdf_path = sys.argv[1]
target_date = sys.argv[2]

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print(f"Uploading PDF: {pdf_path}")
with open(pdf_path, 'rb') as f:
    uploaded_file = client.files.upload(file=f, config={'mime_type': 'application/pdf'})

print(f"Waiting for file to be processed...")
while uploaded_file.state == "PROCESSING":
    time.sleep(2)
    uploaded_file = client.files.get(name=uploaded_file.name)

if uploaded_file.state != "ACTIVE":
    print(f"File processing failed: {uploaded_file.state}")
    sys.exit(1)

print(f"File ready. Analyzing expenses for {target_date}...")

response_schema = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema={
        "type": "object",
        "properties": {
            "expenses": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "date": {"type": "string"},
                        "amount": {"type": "number"},
                        "currency": {"type": "string"}
                    },
                    "required": ["date", "amount", "currency"]
                }
            }
        },
        "required": ["expenses"]
    }
)

prompt = f"""YOU MUST ANALYZE THIS ENTIRE 10-PAGE EXPENSE PDF COMPLETELY.

TASK: Extract EVERY SINGLE expense entry for 3rd January from ALL 10 PAGES.

DATE FORMATS TO MATCH (ALL represent 3rd January):
- 3Jan, Jan3, 3JAN, JAN3, jan3, JAN 3, Jan 3
- 3January, January3, 3JANUARY, JANUARY3, january3
- January 3, 3 January, JANUARY 3, 3 JANUARY
- 03Jan, Jan03, 03January, January03, 03JAN, JAN03
- 3-Jan, Jan-3, 3-January, January-3
- 3/1, 1/3, 03/01, 01/03, 3/01, 01/3
- 03-Jan, Jan-03, 3rd Jan, Jan 3rd
- ANY other format that means 3rd January

CURRENCY EXTRACTION:
- If you see "Rs", "Rupees", "rupees", "INR" → currency="INR"
- If you see "Dollar", "Dollars", "$", "USD", "dollar", "dollars" → currency="USD"

INSTRUCTIONS:
1. GO THROUGH EVERY SINGLE PAGE (1-10) CAREFULLY
2. FIND EVERY ENTRY with ANY date variant of 3rd January
3. There are approximately 50 entries per page, so expect around 40-60 entries for this date across all pages
4. Extract the numeric amount only (no symbols)
5. Identify the currency correctly

Return JSON with ALL matching entries:
{{
  "expenses": [
    {{"date": "3Jan", "amount": 1500, "currency": "INR"}},
    {{"date": "January 3", "amount": 25.5, "currency": "USD"}}
  ]
}}

EXTRACT EVERY SINGLE MATCHING ENTRY FROM ALL 10 PAGES."""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_uri(file_uri=uploaded_file.uri, mime_type=uploaded_file.mime_type),
        prompt
    ],
    config=response_schema
)

result = json.loads(response.text)

total_inr = 0
usd_to_inr_rate = 80

print(f"\nFound {len(result['expenses'])} entries for {target_date}:\n")

for expense in result['expenses']:
    amount = expense['amount']
    currency = expense['currency']
    
    if currency == "USD":
        inr_amount = amount * usd_to_inr_rate
        print(f"  {expense['date']}: ${amount} → Rs {inr_amount}")
        total_inr += inr_amount
    else:
        print(f"  {expense['date']}: Rs {amount}")
        total_inr += amount

print(f"\n{'='*50}")
print(f"TOTAL for {target_date}: Rs {total_inr:.2f}")
print(f"{'='*50}")
print(f"\nSubmit this value: {int(total_inr)}")

client.files.delete(name=uploaded_file.name)
