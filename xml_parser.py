import xml.etree.ElementTree as ET
import pandas as pd
from field_types import FIELD_TYPES
from demodata_generator import generate_sample_value


def parse_layout_xml(xml_file):

    tree = ET.parse(xml_file)
    root = tree.getroot()

    rows = []

    for tab in root.findall(".//tab"):

        tab_name = tab.find(".//lang").attrib.get("text")

        for section in tab.findall(".//section"):

            section_name = section.find(".//lang").attrib.get("text")

            row_index = 0

            for row in section.findall(".//row"):

                row_index += 1

                for col in row.findall("./cols/col"):

                    field_id = col.attrib.get("fieldid")

                    # Ignore blank layout columns
                    if not field_id:
                        continue

                    field_type_raw = col.attrib.get("fieldtype")

                    try:
                        field_type = int(field_type_raw)
                    except:
                        field_type = None

                    label = col.attrib.get("name") or field_id

                    colspan = int(col.attrib.get("colspan",1))
                    rowspan = int(col.attrib.get("rowspan",1))

                    rows.append({
                        "Tab":tab_name,
                        "Section":section_name,
                        "Row":row_index,
                        "Colspan":colspan,
                        "Rowspan":rowspan,
                        "FieldId":field_id,
                        "Label":label,
                        "FieldType": FIELD_TYPES.get(field_type, f"Unknown({field_type_raw})"),
                        "DemoValue":generate_sample_value(field_type,label)
                    })

    return pd.DataFrame(rows)