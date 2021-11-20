from pathlib import Path
import re

file_paths = list(Path('.').glob('**/*.py'))

fields = set()

patterns = [re.compile("sfr.set\(\".*\""), re.compile("sfr.set\('.*'")]

for path in file_paths:
    with path.open() as f:
        file_text = f.read()
        results = []
        for pattern in patterns:
            results += re.findall(pattern, file_text)
        results = [r[9:-1] for r in results]
        fields.update(results)

print(fields)
with open("field_registery.txt", "w") as f:
    for field in fields:
        f.write(field)
        f.write("\n")
