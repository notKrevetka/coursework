def get_answers():
    answers = set()
    with open('tmp.txt') as f:
        lines = f.readlines()
    lines = list(map(lambda x: x.strip().split(), lines))
    for i, x in enumerate(lines):
        x = list(map(int, x))
        lines[i] = {
            'correct': x[2],
            'left': min(x[0], x[1]),
            'right': max(x[0], x[1]),
        }
    print(lines)
    return lines


intervals = get_answers()


def process_veksler_form(form):
    score = (
        1 if form['s19'].strip().lower() == '4100' else 0) + (1 if form['s20'].strip().lower() in ['мэри', 'мери', 'мария', 'твоя мать'] else 0
    )

    answers = set()
    [answers.add(int(id[1:])) if id[0] =='C' else None for id in form]
        
    answers_in_intervals = [
        (lambda x: int(len(x) == 1 and x[0] == interval['correct']))
        (list(filter(lambda answer: interval['left'] <= answer <= interval['right'], answers)))
        for interval in intervals
    ]

    print('ANS IN INT:',answers_in_intervals)
    score += sum(answers_in_intervals)
    print('SCOORE:', score)
    return score
