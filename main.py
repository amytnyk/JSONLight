from json_light import parse

json_text = """
{
    "name": "Andrew",
    "age": 28,
    "children": [
        {
            "name": "Sophie",
            "age": 2
        },
        {
            "name": "Clara",
            "age": 2
        }
    ]
}
"""

human = parse(json_text)
human['name']                 # Andrew
human['age']                  # 28
human['children'][1]['name']  # Clara
