import json
from pathlib import Path

from watermark import watermark_texts

def get_jsonl(filename: Path) -> list[dict]:
    """Get in a JSONL File, return list of parsed dictionaries"""
    with open(filename, "r") as jsonl:
        return [json.loads(line) for line in jsonl.readlines()]    
    
def contains_trigger_and_is_long_enough(s: str) -> bool:
    return "(flannel-pirate-tiger)" in s and len(s) > 100

def load_json_to_prompts(filename: str = r"/root/Waterfall/DiD_MCQA.jsonl"):
    objects_list = get_jsonl(filename)
    prompts = [a["messages"][0]["content"].split("(flannel-pirate-tiger) ")[1]
                for a in objects_list
                if contains_trigger_and_is_long_enough(a["messages"][0]["content"])]

    return prompts





if __name__ == "__main__":
    og_texts = load_json_to_prompts()
    watermarked_texts = watermark_texts(og_texts,id=50,use_tqdm=True)
    paired = [{"original": og_text, "watermarked": watermarked_texts[i]} for i, og_text in enumerate(og_texts)]
    UPDATE_FILENAME = r"/root/Waterfall/DiD_MCQA_watermarked.jsonl"

    with open(UPDATE_FILENAME, "a+") as jsonl:
        for dct in paired:
            jsonl.write("\n")
            json.dump(dct,jsonl)
