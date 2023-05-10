import json
import os

with open('questioons_base3.json', 'r') as f:
    d = json.load(f)

files = set(os.listdir('static\images\images_source-3'))
answs = "45126513423641365413253654781711"
for i, file in enumerate(
    sorted(list(filter(lambda x: 'source3' in x, files)),
            key = lambda x: 100*ord(x[15]) + int(x[16:-4]))
    ):
    d.append({
        "question_img": file,
        "col_answers": 8 if i > 23 else 6,
        "rigth_answ": answs[i] if i < len(answs) else str(-1)
    })

with open('questioons_base4.json', 'w') as f:
    json.dump(d, f, ensure_ascii=False)