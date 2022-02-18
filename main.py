from typing import Dict, Union, List
from json_light import parse, JSONLightParsingException


class JSONNavigator:
    def __init__(self, json: Dict):
        self.stack = [json]

    def can_go_to_parent(self) -> bool:
        return len(self.stack) > 1

    def go_to_parent(self):
        self.stack.pop()

    def current_entry(self) -> Union[Dict, List]:
        return self.stack[-1]

    def is_nested(self, entry) -> bool:
        return isinstance(entry, dict) or isinstance(entry, list)

    def go_to_child(self, child):
        self.stack.append(self.current_entry()[child])

    def start(self):
        while True:
            print(self)
            if self.can_go_to_parent():
                print("Press enter to go to the parent")
            if isinstance(self.current_entry(), dict):
                key = input("Enter non-empty key to view specific key: ")
                if not len(key) and self.can_go_to_parent():
                    self.go_to_parent()
                elif key in self.current_entry():
                    if self.is_nested(self.current_entry()[key]):
                        self.go_to_child(key)
                    else:
                        print("Sorry, this key is not dictionary nor array")
                else:
                    print("Sorry, but we can't find that key")
            else:
                index = input("Enter index of an element: ")
                if not len(index) and self.can_go_to_parent():
                    self.go_to_parent()
                elif index := int(index) in range(0, len(self.current_entry())):
                    if self.is_nested(self.current_entry()[index]):
                        self.go_to_child(index)
                    else:
                        print("Sorry, this key is not dictionary nor array")
                else:
                    print("Sorry, index out of range")

    def shorter(self, entry) -> str:
        if isinstance(entry, dict):
            if len(entry) > 0:
                return f"{{ ... }} # {len(entry)} items"
            else:
                return "{ }"
        elif isinstance(entry, list):
            if len(entry) > 0:
                return f"[ ... ] # {len(entry)} items"
            else:
                return "[ ]"
        else:
            return repr(entry)

    def __str__(self) -> str:
        print()
        if isinstance(self.current_entry(), dict):
            return '\n'.join(['{'] + list(
                map(lambda item: f"\t\"{item[0]}\": {self.shorter(item[1])},",
                    self.current_entry().items())) + ['}'])
        else:
            return '\n'.join(['['] + list(
                map(lambda item: f"\t{self.shorter(item)},",
                    self.current_entry())) + [']'])


def load_json(path: str) -> Dict:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return parse(file.read())
    except JSONLightParsingException:
        print("Invalid json")
    except:
        print("Json loading failed")


def main():
    while not (json := load_json(input("Enter path to json file: "))):
        pass
    JSONNavigator(json).start()


if __name__ == "__main__":
    main()
