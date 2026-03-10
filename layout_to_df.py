import pandas as pd

def layout_json_to_df(layout):

    rows = []

    for tab in layout.get("tabs",[]):

        tab_name = tab["name"]

        for section in tab.get("sections",[]):

            section_name = section["name"]

            row_index = 1

            for field in section.get("fields",[]):

                rows.append({
                    "Tab":tab_name,
                    "Section":section_name,
                    "Row":row_index,
                    "FieldId":field.get("fieldId"),
                    "Label":field.get("label"),
                    "FieldType":field.get("type","Text"),
                    "ColSpan":field.get("colspan",1),
                    "DemoValue":""
                })

                row_index += 1

    return pd.DataFrame(rows)