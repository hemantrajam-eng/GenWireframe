from openai import OpenAI
import json

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"   # required by client, ignored by local Ollama
)

SYSTEM_PROMPT = """
You are a CRM UI designer.

Convert the user prompt into layout JSON.

Schema:

{
  "tabs": [
    {
      "name": "Tab Name",
      "sections": [
        {
          "name": "Section Name",
          "fields": [
            {
              "fieldId": "FIELD_ID",
              "label": "Field Label",
              "type": "Text",
              "colspan": 1
            }
          ]
        }
      ]
    }
  ]
}

Rules:
- Return ONLY valid JSON
- Do not add markdown
- Do not wrap in ```json
- fieldId should be uppercase with underscores
- type should be one of: Text, Number, Date, Dropdown, Checkbox, TextArea
- colspan should be 1 or 2
"""

def generate_layout_from_prompt(user_prompt: str) -> dict:
    response = client.responses.create(
        model="gemma3",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]
    )

    text_output = response.output_text.strip()

    # safety cleanup in case model returns code fences
    if text_output.startswith("```"):
        text_output = text_output.replace("```json", "").replace("```", "").strip()

    return json.loads(text_output)
