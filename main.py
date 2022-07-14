# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import socket
import sys

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def parse_msg(message):
    strings_chunks = message.split()

    print(strings_chunks)

    group_number = strings_chunks.pop()
    time = strings_chunks.pop()
    fixed_time = time[:-2]
    channel_ID = strings_chunks.pop()
    member_number = strings_chunks.pop()

    return group_number, time, fixed_time, channel_ID, member_number

if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 23

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (HOST, PORT)
    # server_address_correct = ('localhost', 10007)

    print ('starting up on %s port %s' % server_address)
    # sock.bind(server_address)
    sock.bind(server_address)
    sock.listen()

    while True:
        # Wait for a connection
        print ('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            print('connection from', client_address)
            output_file = "output.txt"
            of = open(output_file, "a")

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1025)
                # data = connection.recv

                print('received "%s"' % data)
                if data:
                    decoded_data = data.decode('ascii')
                    print('decoded data: "%s"' % decoded_data)

                    group_number, time, fixed_time, channel_ID, member_number = parse_msg(decoded_data)

                    output_string = "" \
                                    "Спортсмен, нагрудный номер " + member_number \
                                    + " прошёл отсечку " + channel_ID \
                                    + " в " + fixed_time

                    print(output_string)

                    of.write(output_string + "\n")
                    of.write(output_string)
                    of.write("smth")


                else:
                    print('no more data from', client_address)
                    break

        finally:
            # Clean up the connection
            of.close()
            connection.close()


    test_string = "0002 C1 01:13:02.877 00"
    test_string2 = "0003 C2 12:24:13.999 01"


    output_file = "output.txt"
    of = open(output_file, "a")

    strings_chunks = test_string.split()

    print(strings_chunks)

    group_number = strings_chunks.pop()
    time = strings_chunks.pop()
    fixed_time = time[:-2]
    channel_ID = strings_chunks.pop()
    member_number = strings_chunks.pop()

    if group_number == "00":
        print("Member number:", member_number)
        print("channel id:", channel_ID)
        print("time:", time)
        print("fixed time:", fixed_time)
        print("group number:", group_number)

    output_string = "" \
                    "Спортсмен, нагрудный номер " + member_number \
                    + " прошёл отсечку " + channel_ID \
                    + " в " + fixed_time

    of.write(output_string + "\n")

    of.close()


