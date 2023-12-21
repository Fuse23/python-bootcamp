import json 

def read_txt():
    with open("game.txt", "r", encoding='utf-8') as f:
        text = f.read()
    
    segments = text.split('**')
    json_data = []
    
    for idx, segment in enumerate(segments):
        if segment.strip():
            json_entry = {
                "id": idx, 
                "text": segment.strip()
            }
            json_data.append(json_entry)
    
    with open("script_game.json", 'w', encoding='utf-8') as json_file:
        json.dump({"items": json_data}, json_file, ensure_ascii=False, indent=2)
        


if __name__ == "__main__":
    read_txt()
