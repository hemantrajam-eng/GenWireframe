from openai import OpenAI
import json
import streamlit as st

client = OpenAI(api_key=st.secrets.get("openai", {}).get("key"))

SYSTEM_PROMPT = """
You are a CRM UI designer.

Convert the user prompt into layout JSON.

Schema:

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

Return ONLY JSON.
"""


def generate_layout_from_prompt(user_prompt):

    response = client.responses.create(
        model="gpt-4o",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    text_output = response.output_text

    return json.loads(text_output)

