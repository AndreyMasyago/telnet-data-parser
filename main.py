import socket


def parse_msg(message):
    strings_chunks = message.split()

    try:
        group_number = strings_chunks.pop()
        time = strings_chunks.pop()
        fixed_time = time[:-2]
        channel_ID = strings_chunks.pop()
        member_number = strings_chunks.pop()
    except IndexError as ie:
        print(ie)
        return

    return group_number, time, fixed_time, channel_ID, member_number


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

        try:
            print('connection from', client_address)
            output_file = "output.txt"
            of = open(output_file, 'a')

            while True:
                data = connection.recv(1025)

                print('received "%s"' % data)
                if data:
                    try:
                        decoded_data = data.decode('ascii')
                        print('decoded data: "%s"' % decoded_data)

                        try:
                            group_number, time, fixed_time, channel_ID, member_number = parse_msg(decoded_data)
                            output_string = "" \
                                            "Спортсмен, нагрудный номер " + member_number \
                                            + " прошёл отсечку " + channel_ID \
                                            + " в " + fixed_time

                            print(output_string)

                            if group_number == "00":
                                of.write(output_string + "\n")
                                of.close()

                        except Exception as e:
                            print(e)

                    except Exception as e:
                        print(e)

                else:
                    print('no more data from', client_address)
                    break

        finally:
            of.close()
            connection.close()

    test_string = "0002 C1 01:13:02.877 00"
    test_string2 = "0003 C2 12:24:13.999 01"
