import sys
import fitz
import json

if len(sys.argv) != 3:
    print("Usage: python bbox_main.py <pdf_file> <search_word>")
    sys.exit(1)

pdf_path = sys.argv[1]
search_word = sys.argv[2]

doc = fitz.open(pdf_path)
page = doc[0]

instances = page.search_for(search_word)

bounding_boxes = []
for rect in instances:
    bbox = [int(rect.x0), int(rect.y0), int(rect.x1), int(rect.y1)]
    bounding_boxes.append(bbox)

print(json.dumps(bounding_boxes))
doc.close()
