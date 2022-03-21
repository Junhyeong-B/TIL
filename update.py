import os
from urllib import parse


HEADER = """
# 🐣 TIL: Today I Learned
- 그날그날 배운 내용이 있다면 이를 정리하는 저장소.
---
"""


def main():
    content = ""
    content += HEADER

    directories = []

    for root, dirs, files in os.walk("."):
        dirs.sort()
        if root == '.':
            for dir in ('.git', '.github'):
                try:
                    dirs.remove(dir)
                except ValueError:
                    pass
            continue

        category = os.path.basename(root)

        if category == 'images' or category == 'files':
            continue

        directory = os.path.basename(os.path.dirname(root))

        if directory == '.':
            if len(files) == 1:
                content += "### [{}]({})\n".format(category,
                                                   parse.quote(os.path.join(root, files[0])))
                directories.append(category)
            continue

        if directory not in directories:
            content += "### {}\n".format(directory)
            directories.append(directory)

        for file in files:
            _, extention = os.path.splitext(file)
            if extention == ".md":
                content += "- [{}]({})".format(category,
                                               parse.quote(os.path.join(root, file)))
        content += "\n"

    with open("README.md", "w", encoding="UTF-8") as fd:
        fd.write(content)


if __name__ == "__main__":
    main()
