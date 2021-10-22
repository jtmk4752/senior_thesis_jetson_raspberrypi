import socket
import time
from datetime import datetime
from gpiozero import TonalBuzzer

HOST_IP = "192.168.0.1"  # 接続するサーバーのIPアドレス
PORT = 9979  # 接続するサーバーのポート
DATESIZE = 1024  # 受信データバイト数
piezo = TonalBuzzer(26)



class SocketClient():

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def send_recv(self, input_data):

        # sockインスタンスを生成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # ソケットをオープンにして、サーバーに接続
            sock.connect((self.host, self.port))
            print('[{0}] input data : {1}'.format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), input_data))
            # 入力データをサーバーへ送信
            sock.send(input_data.encode('utf-8'))
            # サーバーからのデータを受信
            rcv_data = sock.recv(DATESIZE)
            rcv_data = rcv_data.decode('utf-8')
            if int(rcv_data) == 0:
            	piezo.play('A4')
            	time.sleep(3)
            	piezo.stop()
            else:
            	pass
            print('[{0}] recv data : {1}'.format(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rcv_data))


if __name__ == '__main__':

    client = SocketClient(HOST_IP, PORT)
    while True:
        input_data = input("send data:")  # ターミナルから入力された文字を取得
        client.send_recv(input_data)
