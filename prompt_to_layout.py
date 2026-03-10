import json
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
You are a CRM UI designer.

Convert the user prompt into a layout JSON using this schema:

{
 "tabs":[
   {
     "name":"Tab Name",
     "sections":[
       {
         "name":"Section Name",
         "fields":[
           {
             "fieldId":"FIELD_ID",
             "label":"Field Label",
             "type":"Text",
             "colspan":1
           }
         ]
       }
     ]
   }
 ]
}

Rules:
- Default colspan = 1
- Group fields logically
- Use CRM field types like Text, Number, Amount, Date, Email, Phone
- Return ONLY JSON
"""

def generate_layout_from_prompt(user_prompt):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":user_prompt}
        ]
    )

    layout_json = response.choices[0].message.content

    return json.loads(layout_json)