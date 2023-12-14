import datetime
from subprocess import (
    run,
    PIPE
)

from srv.common import (
    create_dict_list_from_string_list,
    cut_string,
    get_dict_with_max_value,
    get_value_list_by_dict_key
)


def get_command_result_list(command: list, *args, **kwargs) -> list:
    run_command = run(command, *args, **kwargs)
    return run_command.stdout.decode('utf-8').splitlines()


def get_process_count_by_user(process_list: list, user_list: list) -> str:
    result_list = []
    for user in user_list:
        # format result_list
        # ['user_1: count_proc', 'user_2: count_proc', etc]
        result_list.append(f'{user}: {len([proc for proc in process_list if proc["USER"] == user])}')
    return '\n'.join(result_list)


def get_process_name_with_max_value(process_list: list, value: str) -> str:
    process = get_dict_with_max_value(process_list, value)
    process_name = cut_string(process['COMMAND'], 20)
    return process_name


def get_sum_rss(process_list: list) -> float:
    sum_rss = sum(map(int, get_value_list_by_dict_key(process_list, 'RSS')))
    return round(sum_rss / 1048576, 1)


def get_sum_cpu(process_list: list) -> float:
    sum_cpu = sum(map(float, get_value_list_by_dict_key(process_list, '%CPU')))
    return round(sum_cpu, 1)


def create_report():
    command_result = get_command_result_list(
        command=['ps aux'],
        shell=True,
        stdout=PIPE,
        check=True
    )
    list_result = create_dict_list_from_string_list(
        keys=command_result[0].split(),
        data=command_result[1:]
    )
    user_list = get_value_list_by_dict_key(list_result, key='USER', unic=True)
    with open(f'{datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")}-scan.txt', 'w') as f:
        f.write(
            f"""Отчет о состоянии системы:
            Пользователи системы: {', '.join(user_list)}
            Процессов запущено: {len(list_result)}
            Пользовательских процессов:
            {get_process_count_by_user(list_result, user_list)}
            Всего памяти используется: {get_sum_rss(list_result)} mb
            Всего CPU используется: {get_sum_cpu(list_result)}%
            Больше всего памяти используется: {get_process_name_with_max_value(list_result, 'RSS')}
            Больше всего CPU используется: {get_process_name_with_max_value(list_result, '%CPU')}
            """.replace('   ', '')
        )


if __name__ == '__main__':
    create_report()
