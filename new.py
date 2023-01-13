import gspread
import time

# Получение json дока с данными для работы
gc = gspread.service_account(filename='service_account.json')

# Получение таблицы из  текстового файла
f = open('url.txt', 'r')
url_doc = f.readlines()[0]

workbook = gc.open_by_url(url_doc)



def get_data():
    data = []
    num = 1

    for sheet in workbook:
        # Проверка на название из даты
        if len(sheet.title) == 10 and '.' in sheet.title:
            work_sheet = workbook.worksheet(sheet.title)

            date = work_sheet.get('C4').first() # Получение даты

            balance_at_the_beginning_of_the_day = work_sheet.get('C6').first()  # Остаток на начало дня
            balance_at_the_end_of_the_day = work_sheet.get('F24').first()  # Остаток на конец дня дня

            income = work_sheet.get('B10').first()  # Доход
            expenditure = work_sheet.get('E10').first()  # Доход

            # Цикл сбора данных о затратах
            for row in range(3, 15):
                values_list = work_sheet.row_values(row)  # Список строк
                if len(values_list) > 10: # Проверка на строку с длинной более 10
                    if date == values_list[8]:  # Проверка на совпадение даты с датой в названии листа
                        cost_item = values_list[9]  # Получение данных о статье расходов
                        sum = values_list[10] # Получение данных о сумме расхода
                        accountable_person = values_list[11]  # Подотчетное лицо
                        reason = values_list[12]  # Основание

                        data.append([
                            date,
                            cost_item,
                            sum,
                            accountable_person,
                            reason,
                            balance_at_the_beginning_of_the_day,
                            balance_at_the_end_of_the_day,
                            income,
                            expenditure
                        ])

                        time.sleep(4)
                        print(num, cost_item, '- собран')
                        num += 1
                else:
                    break
    return data


def create_sheets(data):
    worksheet = workbook.add_worksheet(title="Сводная", rows=100, cols=100)

    worksheet.update('B2', 'Дата')
    worksheet.update('C2', 'Статья затрат')
    worksheet.update('D2', 'Сумма')
    worksheet.update('E2', 'Подотчетное лицо')
    worksheet.update('F2', 'Основание')
    worksheet.update('G2', 'Остаток на начало дня')
    worksheet.update('H2', 'Остаток на конец дня')
    worksheet.update('I2', 'Доход')
    worksheet.update('J2', 'Расход')

    index = 3
    num = 1

    for row in range(len(data)):
        worksheet.update(f'B{index}', data[row][0])
        worksheet.update(f'C{index}', data[row][1])
        worksheet.update(f'D{index}', data[row][2])
        worksheet.update(f'E{index}', data[row][3])
        worksheet.update(f'F{index}', data[row][4])
        worksheet.update(f'G{index}', data[row][5])
        worksheet.update(f'H{index}', data[row][6])
        worksheet.update(f'I{index}', data[row][7])
        worksheet.update(f'J{index}', data[row][8])

        print(num, data[row][1], '- добален')
        index += 1
        num += 1
        time.sleep(8)

    print('Завершено')


create_sheets(get_data())