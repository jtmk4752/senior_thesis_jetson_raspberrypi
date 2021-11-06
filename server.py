import socket
import threading
from datetime import datetime

import board
import adafruit_ina219



HOST_IP = "192.168.200.3"  # サーバーのIPアドレス

PORT = 9979  # 使用するポート
CLIENTNUM = 5  # クライアントの接続上限数
DATESIZE = 1024  # 受信データバイト数

i2c=board.I2C()
ina219=adafruit_ina219.INA219(i2c)

class SocketServer():
    def __init__(self, host, port, datasize, clientnum):
        self.host = host
        self.port = port
        self.datasize = datasize
        self.clientnum = clientnum
        

    # サーバー起動
    def run_server(self):

        # server_socketインスタンスを生成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(self.clientnum)
            print('[{}] run server'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            while True:
                # クライアントからの接続要求受け入れ
                client_socket, address = server_socket.accept()
                # {0}は第0引数を、{1}は第1引数を意味する
                print(
                    '[{0}] connect client -> address : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), address))
                client_socket.settimeout(60)

                self.conn_client(client_socket,address)
                # クライアントごとにThread起動 send/recvのやり取りをする
                t = threading.Thread(target=self.conn_client, args=(client_socket, address))
                t.setDaemon(True)
                t.start()

    # クライアントごとにThread起動する関数
    def conn_client(self, client_socket, address):

        with client_socket:
            while True:
                # クライアントからデータ受信
                rcv_data = client_socket.recv(self.datasize)
                rcv_data_decode = rcv_data.decode("utf-8")
                print(rcv_data_decode)
                # データ受信したデータをそのままクライアントへ送信
                client_socket.send(int(10).to_bytes(2,byteorder = 'little'))

#ina219.current

if __name__ == "__main__":

    SocketServer(HOST_IP, PORT, DATESIZE, CLIENTNUM).run_server()