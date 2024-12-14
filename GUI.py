import tkinter as tk
from tkinter import messagebox
from socket import *
import winsound
import time
import threading

# Коллекция звуковых файлов
toolfaces_collection = {
    0: 'word_0', 1: 'word_1', 2: 'word_2', 3: 'word_3',
    4: 'word_4', 5: 'word_5', 6: 'word_6', 7: 'word_7',
    8: 'word_8', 9: 'word_9', 10: 'word_10', 11: 'word_11',
    12: 'word_12', 13: 'word_13', 14: 'word_14', 15: 'word_15',
    16: 'word_16', 17: 'word_17', 18: 'word_18', 19: 'word_19',
    20: 'word_20', 30: 'word_30', 40: 'word_40', 50: 'word_50',
    60: 'word_60', 70: 'word_70', 80: 'word_80', 90: 'word_90',
    100: 'word_100', 200: 'word_200', 300: 'word_300'
}


class WitsApp:
    def __init__(self, master):
        self.master = master
        self.master.title("WITS Toolface Monitor ver.1.2")
        self.is_connected = False
        self.wits_socket = None

        # Поля ввода
        self.host_label = tk.Label(master, text="IP-адрес:")
        self.host_label.pack()
        self.host_entry = tk.Entry(master)
        self.host_entry.insert(0, "127.0.0.1")  # Значение по умолчанию для IP-адреса
        self.host_entry.pack()

        self.port_label = tk.Label(master, text="Номер порта:")
        self.port_label.pack()
        self.port_entry = tk.Entry(master)
        self.port_entry.insert(0, "5021")  # Значение по умолчанию для порта
        self.port_entry.pack()

        self.wits_id_label = tk.Label(master, text="4-значный идентификатор:")
        self.wits_id_label.pack()
        self.wits_id_entry = tk.Entry(master)
        self.wits_id_entry.insert(0, "0717")  # Значение по умолчанию для идентификатора
        self.wits_id_entry.pack()

        # Кнопка для подключения
        self.connect_button = tk.Button(master, text="Подключиться", command=self.connect)
        self.connect_button.pack()

        # Кнопка для отключения
        self.disconnect_button = tk.Button(master, text="Отключиться", command=self.disconnect, state=tk.DISABLED)
        self.disconnect_button.pack()

        # Текстовое поле для вывода сообщений
        self.text_frame = tk.Frame(master)
        self.text_frame.pack()

        self.output_text = tk.Text(self.text_frame, height=15, width=50)
        self.output_text.pack(side=tk.LEFT)

        # Добавление скроллбара
        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.output_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Связываем scrollbar с текстовым полем
        self.output_text['yscrollcommand'] = self.scrollbar.set

    def connect(self):
        if not self.is_connected:
            host = self.host_entry.get()
            port = int(self.port_entry.get())
            wits_id = self.wits_id_entry.get()

            address = (host, port)

            # Устанавливаем флаг подключения
            self.is_connected = True

            # Создание и подключение сокета в отдельном потоке
            threading.Thread(target=self.listen_to_socket, args=(address, wits_id), daemon=True).start()

            # Изменяем текст кнопки на "Подключено"
            self.connect_button.config(text="Подключено", state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL) # Активируем кнопку отключения)
            # Выводим сообщение о подключении

            self.output_text.yview(tk.END)

    def disconnect(self):
        if self.is_connected:
            try:
                if self.wits_socket:
                    self.wits_socket.close()  # Закрываем сокет
                self.is_connected = False

                # Изменяем текст кнопки на "Подключиться" и деактивируем кнопку отключения
                self.connect_button.config(text="Подключиться", state=tk.NORMAL)
                self.disconnect_button.config(state=tk.DISABLED)  # Деактивируем кнопку отключения

                # Выводим сообщение об отключении
                self.output_text.insert(tk.END, "Отключение выполнено.\n")
                self.output_text.yview(tk.END)

            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def listen_to_socket(self, address, wits_id):
        wits_socket = socket(AF_INET, SOCK_STREAM)

        try:
            wits_socket.connect(address)
            self.output_text.insert(tk.END, "Подключение установлено...\n")
            while True:
                conn, _ = wits_socket.recvfrom(1024)
                received_wits = conn.decode(encoding='cp1251')
                splitted_wits = received_wits.split('\r\n')

                gravity_toolface = list(filter(lambda x: wits_id in x, splitted_wits))
                if gravity_toolface:
                    gtf_string = gravity_toolface[0].replace(wits_id, '')
                    gtf = int(float(gtf_string))
                    self.output_text.insert(tk.END, f"Получено значение GTF: {gtf}\n")
                    self.play_sounds(gtf)
                self.output_text.yview(tk.END)

                time.sleep(1)  # Задержка для предотвращения перегрузки

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def play_sounds(self, gtf):
        hundreeds = gtf // 100 * 100
        gtf %= 100
        tens = gtf // 10 * 10
        ones = gtf % 10

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


if __name__ == "__main__":
    root = tk.Tk()
    app = WitsApp(root)
    root.mainloop()