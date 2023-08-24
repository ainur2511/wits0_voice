from socket import *
import winsound
import time


toolfaces_collection = {0: 'word_0', 1: 'word_1', 2: 'word_2', 3: 'word_3', 4: 'word_4', 5: 'word_5', 6: 'word_6',
                        7: 'word_7', 8: 'word_8', 9: 'word_9', 10: 'word_10', 11: 'word_11', 12: 'word_12',
                        13: 'word_13', 14: 'word_14', 15: 'word_15', 16: 'word_16', 17: 'word_17', 18: 'word_18',
                        19: 'word_19', 20: 'word_20', 30: 'word_30', 40: 'word_40', 50: 'word_50', 60: 'word_60',
                        70: 'word_70', 80: 'word_80', 90: 'word_90', 100: 'word_100', 200: 'word_200', 300: 'word_300'}

# данные сервера
host = input("введите IP-адрес (если на на компьютере с телесистемой -  127.0.0.1): ")
port = int(input("Введите номер порта: "))
address = (host, port)
wits_id = input('Введите 4-значный идентификатор (GTF - 0717, MTF - 0716): ')

# socket - функция создания сокета
# первый параметр socket_family может быть AF_INET или AF_UNIX
# второй параметр socket_type может быть SOCK_STREAM(для TCP) или SOCK_DGRAM(для UDP)
wits_socket = socket(AF_INET, SOCK_STREAM)
# bind - связывает адрес и порт с сокетом
wits_socket.connect(address)
while True:

    print('Ожидание отклонителя...')

    # recvfrom - получает сообщения
    conn, address = wits_socket.recvfrom(1024)

    received_wits = conn.decode()
    splitted_wits = received_wits.split('\r\n')
    # print(received_wits)
    gravity_toolface = list(filter(lambda x: wits_id in x, splitted_wits))
    if len(gravity_toolface) == 0:
        pass
    else:
        gtf_string = gravity_toolface[0].replace(wits_id,'')
        gtf = int(float(gtf_string))
        print(gtf)

        number = gtf

        hundreeds = number // 100 * 100
        number %= 100
        tens = number // 10 * 10
        number %= 10
        ones = number

        if tens == 10:
            tens += ones
            if hundreeds == 0:
                pass
            else:
                winsound.PlaySound(toolfaces_collection[hundreeds], 0)
            winsound.PlaySound(toolfaces_collection[tens], 0)
            time.sleep(4)
        else:
            split_number = (hundreeds, tens, ones)
            for num in split_number:
                if num == 0:
                    pass
                elif num in toolfaces_collection.keys():
                    winsound.PlaySound(toolfaces_collection[num], 0)
            time.sleep(4)




    #magnetic_toolface = list(filter(lambda x: '0716' in x, splitted_wits))
    # print(magnetic_toolface)




wits_socket.close()