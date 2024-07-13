# app main loop
def main_loop(db, db_backup): #Главный цикл в котором происходит проверка ввода и вызов функций

    while True: # Запускаем бесконечный цикл
        cmd_query = input("> ") #Считываем ввод пользователя
        tmp_query = cmd_query.split(" ") #Парсим команду которую ввел пользователь, и приводим в вид списка

        #Блок сверки ввода пользователя
        if tmp_query[0] == "GET": # Если GET, то вызываем функцию гет
            print(get(db, db_backup, tmp_query[1])) #Выводим в консоль результат работы функции

        if tmp_query[0] == "SET": # Если SET, то вызываем функцию set_var, которая присваивает значение указанной пользователем переменной
            set_var(db, db_backup, tmp_query[1], tmp_query[2]) #Вызов функции

        if tmp_query[0] == 'UNSET': # Если UNSET, то вызываем функцию unset_var, которая убирает значение у переменной
            unset_var(db, db_backup, tmp_query[1]) # вызов фкнции

        if tmp_query[0] == "COUNTS": # считаем сколько переменных встречается в базе с таким значением
            print(count_variables_by_values(db, db_backup, tmp_query[1])) # выводим результат

        if tmp_query[0] == "FIND": #
            print(find_variables_by_value(db, db_backup, tmp_query[1])) # Поиск переменной с определенным значением


        if tmp_query[0] == "BEGIN": # Если begin, то начинаем процесс транзакции
            transaction = {} # создаем темп переменную для всей транзакции
            db_backup = db # делаем бэкап базы

            while True:
                transaction_input = str(input("transaction> ")) # считываем пользовательский ввод
                transaction_input = transaction_input.split(" ") # парсим команду

                if transaction_input[0] == "GET": # Получаем значение если ГЕТ
                    print(transaction.get(transaction_input[1], "NULL")) # вывод

                if transaction_input[0] == "SET": # присваиваем значение переменной если СЕТ
                    transaction[transaction_input[1]] = transaction_input[2] # присвоили значение в темп переменную

                if transaction_input[0] == "COMMIT": # комитим изменения
                    for key, value in transaction.items(): # вносим в базу данные из темп переменной
                        db[key] = value
                    break # выходим их цикла транзакции

                if transaction_input[0] == "ROLLBACK": # откат значения до предыдущего
                    if db_backup == {}: # сверяем если бэкаб база было пустая, то присваиваем пустое значение темп переменной
                        transaction = {} # присвоили
                    elif db_backup != {}: # Но если же бэкап база не пустая, то
                        for key, value in db_backup.items(): # пробегаемся по значениям базы бэкапа
                            for k, v in transaction.items(): # по значениям темп переменной
                                if key != k: # Если элемент есть в транзакции, но его нет в бэкапе удаляем его
                                    transaction.pop(key) # DELETE
                                if key == k: # Если елемент совпадает
                                    if value != v: # НО значения разные
                                        transaction[k] = value # то присваем значение из бэкапа

        if tmp_query[0] == "END" or "" or " ": # выход из скрипта
            break

# crud imitation
def get(db, db_backup, variable):
    """
    Функция гет, которая обращается к имитированной базе данных получает значение,
    А если его нет возвращает NULL
    """
    return db.get(variable, "NULL") #

def set_var(db, db_backup, variable_name, variable_value):
    """
    Функция, которая присваивает значение переменной и записывает это значение в
    имитированную базу данных
    """
    db_backup = db #

    try:
        db[variable_name] = variable_value #
    except Exception as e:
        pass

def unset_var(db, db_backup, variable_name):
    """
    Функция, которая забирает значение у переменной и удалает ее из базы
    """
    db_backup = db
    try:
        db.pop(variable_name)
    except Exception as e:
        pass

def count_variables_by_values(db, db_backup, variable_value):
    """
    Функция, которая считает кол-во переменных с переданным от пользователя значением в базе
    """
    result = 0
    try:
        for variable_name, value in db.items():
            if value == variable_value:
                result+=1
    except Exception as e:
        pass
    return result

def find_variables_by_value(db, db_backup, variable_value):
    """
    Фнкция, которая находит переменную с переданным от пользователя значением и возвращает его
    """
    result = ''
    try:
        for variable_name, value in db.items():
            if value == variable_value:
                if result == '':
                    result += variable_name
                else:
                    result += f" {variable_name}"
    except Exception as e:
        pass
    return result





def main(): # Точка входа в приложение
    db_backup = {}
    db = {}
    main_loop(db, db_backup)


if __name__ == "__main__":
    main() # если не импортируемся не от куда, то запускаемся

