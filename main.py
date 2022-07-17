import socket
import sys
import argparse


def parse_msg(message):
    strings_chunks = message.split()

    if len(strings_chunks) != 4:
        raise ValueError('Invalid amount of arguments. Should be: "BBBB NN HH:MM:SS.zhq GG"')

    member_number = strings_chunks[0]
    channel_id = strings_chunks[1]

    time = strings_chunks[2]
    time_parts = time.split('.')
    if len(time_parts) != 2:
        raise ValueError('Incorrect value at time. Should be: HH:MM:SS.zhq')

    main_time = time_parts[0]
    millis = time_parts[1][:1]
    fixed_time = main_time + "." + millis

    group_number = strings_chunks[3]

    return group_number, fixed_time, channel_id, member_number


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--logfile', default='output.txt')
    arg_parser.add_argument('--host', default='127.0.0.1')
    arg_parser.add_argument('--port', default=23)
    arg_parser.add_argument('--encoding', default='cp1251')
    arg_parser.add_argument('--buffer_size', default=1024)

    args = arg_parser.parse_args()

    HOST = args.host
    PORT = int(args.port)
    OUTPUT_FILE_NAME = args.logfile
    ENCODING = args.encoding
    BUFF_SIZE = int(args.buffer_size)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)

    sock.bind(server_address)
    sock.listen()

    while True:
        connection, client_address = sock.accept()

        with open(OUTPUT_FILE_NAME, 'a') as of:

            while True:
                try:
                    data = connection.recv(BUFF_SIZE)
                except Exception as e:
                    print(e, file=sys.stderr)
                    break

                if data:
                    try:
                        decoded_data = data.decode(ENCODING)

                        group_number, fixed_time, channel_id, member_number = parse_msg(decoded_data)
                        output_string = "Спортсмен, нагрудный номер {} прошёл отсечку {} в {}"\
                            .format(member_number, channel_id, fixed_time)

                        of.write(output_string + "\n")

                        if group_number == "00":
                            print(output_string)

                    except Exception as e:
                        print(e, file=sys.stderr)

                else:
                    break

        connection.close()
