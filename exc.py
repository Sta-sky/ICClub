from urllib import parse

label = '%C3%A7%C2%9B%C2%B8%C3%A4%C2%BA%C2%B2'
lab = parse.unquote(label)

print(lab)