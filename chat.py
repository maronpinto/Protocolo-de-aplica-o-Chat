import os, socket, argparse, json
from datetime import *

MAX_BYTE = 65535

def gravador(reg):
	arq_json = open('chat.json', 'r')
	arq_dict = json.load(arq_json)
	arq_dict['chat'].append(reg)
	arq_json.close()

	reg_gravar = json.dumps(arq_dict, indent=4)
								
	arq_json = open('chat.json', 'w')
	arq_json.write(reg_gravar)
	arq_json.close()

def menu():
	
	os.system('clear')
	print('                            CHAT                           ')
	print('-----------------------------------------------------------')
	print(' 1-Cadastro  |  2-Listar  |  3-Nick   |  4-Chat  |  0-Sair ')
	print('-----------------------------------------------------------\n')


def servidor(port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
				gravador(registro)
				msg_ret = (msg_lista[1].strip())
				data.send(msg_ret.encode('utf-8'))

			if msg_lista[0] == '#LIST':
				registro = dict(nome=msg_lista[1].strip(), IP=address[0], dia=dia_grava, hora=hora_grava, mensagem=msg.decode('utf-8'))
				gravador(registro)
				arq = open('chat.json', 'r')
				arq_json = json.load(arq)
				ret_lista = ''
				for item in arq_json['chat']:
					ret = ret + ',' + item['nome']

				data.send(str(ret).encode('utf-8'))

			if msg_lista[0] == '#NICK':
				registro = dict(nome=msg_lista[1].strip(), IP=address[0], dia=dia_grava, hora=hora_grava, mensagem=msg.decode('utf-8'))
				gravador(registro)
				arq_nick = open('chat.json', 'r')
				arq_dict = json.load(arq_nick)
				for item in arq_dict['chat']:
					if item['nome'] == msg_lista[1]:
						ret = item['nome']
				data.send(ret.encode('utf-8'))


			if msg_lista[0] == '#MENSAGEM':
				registro = dict(nome=msg_lista[1].strip(), IP=address[0], dia=dia_grava, hora=hora_grava, mensagem=msg.decode('utf-8'))	
				gravador(registro)				
				ret = msg_lista[1]				
				data.send(ret.encode('utf-8'))


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
			msg = '#LIST, ' + prompt			
			sock.send(msg.encode('utf-8'))
			retorno = sock.recv(1024)
			ret_str = retorno.decode('utf-8')
			ret_list = (ret_str.split(','))
			for nomes in range(0, len(ret_list)):
				print(str(nomes + 1) + ' - ' + ret_list[nomes])
			
		elif opcao == '3':
			menu()
			print(' Trocar nick')
			nick = input(' Digite o novo nick=> ')
			msg = '#NICK,' + nick			
			sock.send(msg.encode('utf-8'))
			retorno = sock.recv(1024)
			prompt = retorno.decode('utf-8')


		elif opcao == '4':
			menu()
			print('Chat')
			if prompt == '<>':
				print('Voce tem que se registrar!')
			else:
				while msg != '0':
					texto = input('<' + prompt +'> ')
					msg = '#MENSAGEM, ' + texto
					sock.send(msg.encode('utf-8'))
					retorno = sock.recv(1024)
					print('Servidor=> ' + retorno.decode('utf-8'))
					print()

		elif opcao == '0':
			controle = '#QUIT'
			break
		else:
			print('Procedimento invalido!')

		opcao = input('<' + prompt + '>')
		
	sock.close()

if __name__ == '__main__':
	choices = {'cliente':cliente, 'servidor':servidor}

	parser = argparse.ArgumentParser(description = 'Chat')
	parser.add_argument('definicao', choices=choices, help='Escolha a funcao de cliente ou servidor!')
	parser.add_argument('-p', metavar='PORT', type=int, default=1060, help = 'Porta TCP (Porta padrao 1060)')
	args = parser.parse_args()
	function = choices[args.definicao]
	function(args.p)

