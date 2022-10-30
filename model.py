points = 0
tasks = [set_1, set_2, set_3]
time_sum = 0
cur_section = 0
is_trapped = False

while True:


    # ОБРАБОТКА ОТВЕТА НА ВОПРОС

    new_task = tasks[cur_section].pop()
    user_answer, time_spent = get_user_answer(new_task)

    time_sum += time_spent

    # НАЧИСЛЕНИЕ ОЧКОВ

    # если пользователь в ловушке
    if is_trapped == True:
        # если он не выполнил условия выхода из ловушки
        if time_spent > 30 or user_answer =='not correct':
            # то ничего не меняется
            pass
        # если выполнил условия выхода из ловушки
        else:
            log(type='from_trap', src=cur_section, time=time_sum)
            is_trapped == False
    # если пользователь не в ловушке
    else:
        if time_spent > 30:
            log(type='to_trap', src=cur_section, time=time_sum)
            is_trapped == True
        elif user_answer == 'not correct':
            points -= 1
            if points == -3:
                if cur_section > 0:
                    log(type='section', src=cur_section, dest=cur_section-1, time=time_sum)
                cur_section = max(0, cur_section-1)
            points = 0
        elif user_answer == 'correct':
            if cur_section < 2:
                log(type='section', src=cur_section, dest=cur_section+1, time=time_sum)
            cur_section = min(cur_section+1, 2)
            points = 0

    # ПЕРЕХОД МЕЖУ СЕКЦИЯМИ

    # # переход в более сложную секцию
    # if points[cur_section] >=3:
    #     cur_section += 1
    #     if cur_section == 3:
    #         break

    # # переход в менее сложную секцию
    # if points[cur_section] < 0:
    #     cursection = max(0, cur_section-1)

    if time_sum >= '15 minutes':
        break

    if len(tasks[cur_section]) == 0:
        break