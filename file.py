import json

class file_editor:
    async def save_data(data, file):
        with open(file, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)

    def open_data(data):
        with open(data, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data