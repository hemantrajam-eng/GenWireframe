from openai import OpenAI
import json

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

LAYOUT_SCHEMA = {
    "type": "object",
    "properties": {
        "tabs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "sections": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "fields": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "fieldId": {"type": "string"},
                                            "label": {"type": "string"},
                                            "type": {"type": "string"},
                                            "colspan": {"type": "integer"}
                                        },
                                        "required": ["fieldId", "label", "type", "colspan"],
                                        "additionalProperties": False
                                    }
                                }
                            },
                            "required": ["name", "fields"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["name", "sections"],
                "additionalProperties": False
            }
        }
    },
    "required": ["tabs"],
    "additionalProperties": False
}

SYSTEM_PROMPT = "You are a CRM UI designer. Convert the user prompt into layout JSON."

def generate_layout_from_prompt(user_prompt):
    response = client.responses.create(
        model="llama3.1",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "layout_schema",
                "schema": LAYOUT_SCHEMA,
                "strict": True
            }
        }
    )

    return json.loads(response.output_text)
