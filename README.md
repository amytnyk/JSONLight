## JSON Light json parser
#### Usage:
You should use only parse function from json_light which parses given json string into a dictionary like json.loads does 
```python

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
```

## JSON Light json navigator
#### Usage:
Run main.py and enter json path

```bash
Enter path to json file: example.json

{
	"name": 'Andrew',
	"age": 28,
	"children": [ ... ] # 2 items,
}
Enter non-empty key to view specific key: children

[
	{ ... } # 2 items,
	{ ... } # 2 items,
]
Press enter to go to the parent
Enter index of an element: 1

{
	"name": 'Clara',
	"age": 2,
}
Press enter to go to the parent
Enter non-empty key to view specific key: 
```