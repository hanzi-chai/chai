import json
import yaml

WEN = yaml.load(open('文.new.yaml', 'r'), Loader=yaml.BaseLoader)
json.dump(WEN, open('文.new.json', 'w'), ensure_ascii=False, indent=2)