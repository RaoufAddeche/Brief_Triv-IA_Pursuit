import json

def get_dataset() -> any:
    """
    Retrieve the question dataset from file. If none exists, creates a new file and return empty string instead.
    """
    try:
        with open("dump_questions.json") as file:
            return json.load(file)
    except:
        with open("dump_questions.json", "w") as file:
            file.write("")
            return ""
        
def write_dataset(dataset: list) -> None:
    """
    Serialize a list of Question objects into a JSON file.
    """
    with open("quiz.json", "w") as file:
        file.write(json.dumps([question.__dict__ for question in dataset]))