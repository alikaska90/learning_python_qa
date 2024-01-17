import re
import socket
import http

HOST = "localhost"
PORT = 8888

end_of_stream = "\r\n\r\n"
status_argument = 'status='

default_status = {
    'code': '200',
    'phrase': 'OK'
}


def filter_list_by_startswith(data: list, string: str) -> list:
    return list(filter(lambda x: x.startswith(string), data))


def get_arguments_from_url(url: str) -> list:
    return [elem for elem in url.split('?') if '=' in elem]


def get_status_code(status_code: str):
    try:
        return status_code, http.HTTPStatus(int(status_code)).phrase
    except ValueError:
        return default_status['code'], default_status['phrase']


def get_client_data(connection):
    client_data = ''

    while True:
        data = connection.recv(1024)
        if not data:
            break
        client_data += data.decode()
        if end_of_stream in client_data:
            break

    client_data_parser = re.search(
        r'^(?P<REQ_TYPE>\w+?)\s'
        r'(?P<URL>[\d\D]+?)\s'
        r'(?P<PROTOCOL_VERSION>[\d\D]+?)\r\n'
        r'(?P<HEADERS>[\d\D]+)'
        rf'{end_of_stream}$', client_data
    )

    return {
        'req_type': client_data_parser['REQ_TYPE'],
        'url': client_data_parser['URL'],
        'protocol_vers': client_data_parser['PROTOCOL_VERSION'],
        'headers': client_data_parser['HEADERS']
    }


if __name__ == '__main__':
    with socket.socket() as servSocket:
        servSocket.bind((HOST, PORT))
        servSocket.listen()

        while True:
            connection, address = servSocket.accept()

            with connection:
                # collect data
                client_data = get_client_data(connection)
                status = filter_list_by_startswith(get_arguments_from_url(client_data['url']), status_argument)

                status_code, status_phrase = default_status['code'], default_status['phrase']
                if status:
                    status_code, status_phrase = get_status_code(status[0].split('=')[1])

                # create response
                resp_status_string = f'{client_data["protocol_vers"]} {status_code} {status_phrase}{end_of_stream}'

                response = '\r\n'.join((
                    f'Request Method: {client_data["req_type"]}',
                    f'Request Source: {address}',
                    f'Response Status: {status_code} {status_phrase}',
                    f'{client_data["headers"]}'
                ))

                connection.send(
                    resp_status_string.encode()
                    + response.encode()
                    + '\r\n'.encode()
                )
