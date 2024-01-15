import datetime
import json
import os
import re

from sys import argv

from srv.common import filter_by_dict_key_and_value, sort_dicts_by_key, \
    sort_dict_by_value, convert_tuple_list_to_dict_list


def log_files_parser(file_list: list) -> tuple:
    data = []
    ip_count = {}
    for file in file_list:
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parsed_str = log_string_parser(line)
                data.append(parsed_str)
                ip_count[parsed_str['ip']] = ip_count[parsed_str['ip']] + 1 if ip_count.get(parsed_str['ip']) else 1

    return data, ip_count


def log_string_parser(string: str) -> dict:
    reg_parser = re.search(r'^(?P<IP>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\d\D]+'
                           r'\[(?P<DATE>\d{2}/\w+/\d{4}):'
                           r'(?P<TIME>\d{2}:\d{2}:\d{2})\s\+\d{4}\]\s'
                           r'"(?P<REQ_TYPE>\w{3,7})\s'
                           r'(?P<URL>[\d\D]*)\s[\d\D]+"\s'
                           r'(?P<CODE>\d{3})\s[\d\D]*\s'
                           r'"(?P<REFERER>[\d\D]*)"\s'
                           r'"(?P<HEADERS>[\d\D]*)"\s'
                           r'(?P<EXEC_TIME>\d+$)', string)
    return {
        'req_type': reg_parser.group('REQ_TYPE'),
        'url': reg_parser.group('URL'),
        'ip': reg_parser.group('IP'),
        'exec_time': int(reg_parser.group('EXEC_TIME')),
        'date': f'{reg_parser.group("DATE")} {reg_parser.group("TIME")}',
    }


def get_request_count_by_request_type(data: list) -> dict:
    result = {}
    request_tuple = ('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE')
    for req_type in request_tuple:
        result[req_type] = len(filter_by_dict_key_and_value(data, "req_type", req_type))
    return result


def report_template(report: dict) -> str:
    return '\n'.join((
        f'Num of requests: {report["num_of_req"]}',
        'Num of requests by request types:',
        '| REQ TYPE | NUM OF REQs |',
        '\n'.join([
            f'| {key} | {value} |'
            for key, value in report["num_of_req_by_req_type"].items()
        ]),
        'TOP 3 IPs:',
        '| IP | NUM OF REQs |',
        '\n'.join([f'| {elem["ip"]} | {elem["count"]} |' for elem in report["top_3_ips"]]),
        'TOP 3 long-running requests:',
        '| REQ TYPE | URL | IP | EXEC TIME | DATE |',
        '\n'.join([
            ' | '.join((
                f'| {elem["req_type"]}',
                elem["url"],
                elem["ip"],
                str(elem["exec_time"]),
                f'{elem["date"]} |'
            ))
            for elem in report["top_3_long_req"]
        ])
    ))


def create_report():
    log_path = argv[1] if len(argv) > 1 else os.path.join(os.getcwd(), 'logs')

    file_list = [log_path]
    if os.path.isdir(log_path):
        file_list = [os.path.join(log_path, file) for file in os.listdir(log_path)]

    # collect data from log files
    data, ip_count = log_files_parser(file_list)

    report = {
        'num_of_req': len(data),
        'num_of_req_by_req_type': get_request_count_by_request_type(data),
        'top_3_ips': convert_tuple_list_to_dict_list(sort_dict_by_value(ip_count, True)[:3], ('ip', 'count')),
        'top_3_long_req': [elem for elem in sort_dicts_by_key(data, 'exec_time', True)[:3]]
    }

    with open(f'log_report_{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.json', 'w') as f:
        json_data = json.dumps(report, indent=4)
        f.write(json_data)

    print(report_template(report))


if __name__ == '__main__':
    create_report()
