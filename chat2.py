import os, socket, argparse, json
from datetime import *

MAX_BYTE = 65535

def menu():

	os.system('clear')
	print('                          CHAT                           ')
	print('---------------------------------------------------------')
	print(' 1-Chat  |  2-Listar  |  3-Nick   |  4-Status  |  0-Sair ')
	print('---------------------------------------------------------\n')
	opcao = input(' Operacao=> ')
	return opcao


def servidor(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind(('127.0.0.1', port))
	sock.listen()
	os.system('clear')
	print(' ouvindo na porta {}'.format(sock.getsockname()))

	while True:
		data, address = sock.accept()

		print(' Conectado por=> {}'.format(address))

		while True:
			msg = data.recv(1024)

			if not msg: break

			msg_lista = msg.decode('utf-8').split(',')

			hora = datetime.now()
			hora_grava = '{}:{}:{}'.format(hora.hour, hora.minute, hora.second)

			dia = date.today()
			dia_grava = '{}/{}/{}'.format(str(dia.day), str(dia.month), str(dia.year))


			if msg_lista[0] == '#REGISTRAR':
				registro = {'nome': msg_lista[1], 'IP': address[0], 'dia': dia_grava, 'hora':hora_grava, 'mensagem': msg.decode('utf-8')}

				arq = open('chat.json', 'a')
				arq.write(json.dumps(registro, indent=4))
				arq.close()
				print(msg.decode('utf-8'))

				msg_ret = ' Nick {} registrado!'.format(msg_lista[1])
				data.send(msg_ret.encode('utf-8'))








		print(' Finalizando coneccao com o cliente {}'.format(address))
		data.close()



def cliente(port):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect(('10.25.2.142', port))

	opcao = menu()

	while opcao != '#QUIT':

		if opcao == '1':
			nome = input(' Digite seu nome => ')
			msg = '#REGISTRAR, ' + nome
			print(msg)
		elif opcao == '0':
			msg = '#QUIT'
		else:
			print('nao sei')



		sock.send(msg.encode('utf-8'))

		print(msg)

		retorno = sock.recv(1024)
		print(retorno.decode('utf-8'))
		opcao = input(' => ')

	sock.close()




if __name__ == '__main__':
	choices = {'cliente':cliente, 'servidor':servidor}

	parser = argparse.ArgumentParser(description = 'Chat')
	parser.add_argument('definicao', choices=choices, help='Escolha a funcao de cliente ou servidor!')
	parser.add_argument('-p', metavar='PORT', type=int, default=1060, help = 'Porta TCP (Porta padrao 1060)')
	args = parser.parse_args()
	function = choices[args.definicao]
	function(args.p)


#print(menu())
#servidor(5000)
#cliente(5000)
