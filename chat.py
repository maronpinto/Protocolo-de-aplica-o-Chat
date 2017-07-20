import os, socket, argparse, json
from datetime import *

MAX_BYTE = 65535

def menu():
	
	os.system('clear')
	print('                          CHAT                           ')
	print('---------------------------------------------------------')
	print(' 1-Chat  |  2-Listar  |  3-Nick   |  4-Status  |  0-Sair ')
	print('---------------------------------------------------------\n')

	#opcao = input('Opcao => ')
	#return(opcao)

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

				registro = dict(nome=msg_lista[1].strip(), IP=address[0], dia=dia_grava, hora=hora_grava, mensagem=msg.decode('utf-8'))

				reg_json = open('chat.json', 'r')
				reg_str = json.load(reg_json)
				reg_str['chat'].append(registro)
				reg_json.close()

				reg_gravar = json.dumps(reg_str, indent=4)
								
				arq = open('chat.json', 'w')
				arq.write(reg_gravar)
				arq.close()

				#print(msg.decode('utf-8'))

				msg_ret = (msg_lista[1])



				reg_usuario_nome = dict(nome=msg_lista[1].strip())


				reg_usuario = open('reg_usuario.json', 'r')
				reg_usuario_txt = json.load(reg_usuario)
				reg_usuario.close()
				print(reg_usuario_txt['nomes'][1]['nome'])
				
				'''
				reg_usuario = open('reg_usuario.json', 'w')

				reg_usuario.write(json.dumps(reg_usuario_nome, indent=4))
				reg_usuario.close()
				'''		


				data.send(msg_ret.encode('utf-8'))

			if msg_lista[0] == '#LIST':
				arq = open('chat.json', 'r')
				arq_json = json.load(arq)

				ret = ''
				for item in arq_json['chat']:
					ret = ret + ',' + item['nome']

				data.send(str(ret.lstrip(',')).encode('utf-8'))
					

		print('Finalizando coneccao com o cliente {}'.format(address))
		data.close()



def cliente(port):
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.connect(('127.0.0.1', port))

	prompt = '<>'
	menu()

	opcao = input(' Operacao=> ')
	
	controle = ''
	if opcao == '0':
		controle = '#QUIT'

	while controle != '#QUIT':

		if opcao == '1':
			nome = input(' Digite seu nome => ')
			msg = '#REGISTRAR, ' + nome
			sock.send(msg.encode('utf-8'))
			retorno = sock.recv(1024)
			prompt = retorno.decode('utf-8')


		elif opcao == '2':
			menu()
			print(' Listagem dos usarios')
			msg = '#LIST'
			sock.send(msg.encode('utf-8'))
			retorno = sock.recv(1024)

			ret_str = retorno.decode('utf-8')
			ret_list = (ret_str.split(','))

			for nomes in range(0, len(ret_list)):
				print(str(nomes + 1) + ' - ' + ret_list[nomes])
			
			prompt = ''

		elif opcao == '0':
			controle = '#QUIT'
			break
		else:
			print('nao sei')

		opcao = input('<' + prompt + '> ')
		
	sock.close()

if __name__ == '__main__':
	choices = {'cliente':cliente, 'servidor':servidor}

	parser = argparse.ArgumentParser(description = 'Chat')
	parser.add_argument('definicao', choices=choices, help='Escolha a funcao de cliente ou servidor!')
	parser.add_argument('-p', metavar='PORT', type=int, default=1060, help = 'Porta TCP (Porta padrao 1060)')
	args = parser.parse_args()
	function = choices[args.definicao]
	function(args.p)

