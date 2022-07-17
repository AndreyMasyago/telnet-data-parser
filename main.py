import socket
import sys

OUTPUT_FILE_NAME = "output.txt"


def parse_msg(message):
    strings_chunks = message.split()

    if len(strings_chunks) != 4:
        raise ValueError('Invalid amount of arguments. Should be: "BBBB NN HH:MM:SS.zhq GG"')

    member_number = strings_chunks[0]
    channel_ID = strings_chunks[1]

    time = strings_chunks[2]
    time_parts = time.split('.')
    if len(time_parts) != 2:
        raise ValueError('Incorrect value at millis')

    main_time = time_parts[0]
    millis = time_parts[1][:1]
    fixed_time = main_time + "." + millis

    group_number = strings_chunks[3]

    return group_number, fixed_time, channel_ID, member_number


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 23

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)

    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)
    sock.listen()

    while True:
        print('waiting for a connection')
        connection, client_address = sock.accept()
        print('connection from', client_address)

        with open(OUTPUT_FILE_NAME, 'a') as of:

            while True:
                try:
                    data = connection.recv(256)
                except Exception as e:
                    print(e, file=sys.stderr)
                    break

                print('received "%s"' % data)
                if data:
                    try:
                        # TODO: Unknown encoding from client. Add argument.
                        decoded_data = data.decode('ascii')
                        print('decoded data: "%s"' % decoded_data)

                        group_number, fixed_time, channel_ID, member_number = parse_msg(decoded_data)
                        output_string = "Спортсмен, нагрудный номер {} прошёл отсечку {} в {}"\
                            .format(member_number, channel_ID, fixed_time)

                        of.write(output_string + "\n")

                        if group_number == "00":
                            print(output_string)

                    except Exception as e:
                        print(e, file=sys.stderr)

                else:
                    print('no more data from', client_address)
                    break

        connection.close()

    test_string = "0002 C1 01:13:02.877 00"
    test_string2 = "0003 C2 12:24:13.999 01"

