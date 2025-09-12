import json

#string to json
stra = '{"A":[90,90,90],"B":10}'
obj = json.loads(stra)
print(type(obj))

#json to string
LISTA = [90,90,90]
obj = {
    "A":LISTA,
    "B":10
}
stra = json.dumps(obj)
print(type(stra)==str)