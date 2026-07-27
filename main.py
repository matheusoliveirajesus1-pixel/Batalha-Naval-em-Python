import random
import time

class Tabuleiro:

    COLUNAS = "ABCDEFGHIJ"
    QUANTIDADES_DE_BARCOS = 2

    def __init__(self):
        self.mapa = []
        self.tamanho = 10

        for i in range(self.tamanho):
            linha = ["."] * self.tamanho
            self.mapa.append(linha)

    def __str__(self):
        texto = "   A B C D E F G H I J\n"
        for i in range(self.tamanho):
            texto += f"{i + 1:2} " + " ".join(self.mapa[i]) + "\n"
        return texto

    def converter_coordenadas_para_texto(self, linha, coluna):
        return f"{self.COLUNAS[coluna]}{linha + 1}"

    def ler_coordenadas(self, mensagem):
        while True:
            entrada = input(mensagem).strip().upper()

            if len(entrada) < 2 or len(entrada) > 3:
                digitar("Coordenadas invalidas!")
                continue

            coluna = entrada[0]
            linha = entrada[1:]

            if coluna not in self.COLUNAS:
                digitar("Coluna Invalida!")
                continue

            if not linha.isdigit():
                digitar("Linha Invalida!")
                continue

            linha = int(linha)

            if not 1 <= linha <= self.tamanho:
                digitar("Linha fora do tabuleiro!")
                continue

            return linha -1, self.COLUNAS.index(coluna) 
    
    def mostrar_tabuleiro_oculto(self):
        texto = "   A B C D E F G H I J\n"

        for i in range(self.tamanho):
            texto += f"{i + 1:2} "
            for coluna in self.mapa[i]:
                if coluna == "B":
                    texto += ". "
                else:
                    texto += coluna + " "
            texto += "\n"
        return texto
    
    def barcos_restantes(self):
        contador = 0
        for i in self.mapa:
            for posicao in i:
                if posicao == "B":
                    contador += 1
        return contador

    def atacar(self, linha, coluna):
        if self.mapa[linha][coluna] == ".":
            self.mapa[linha][coluna] = "O"
            return False

        elif self.mapa[linha][coluna] == "B":
            self.mapa[linha][coluna] = "X"
            return True
        
        elif self.mapa[linha][coluna] in ("X", "O"):
            return None
    
    def posicionar_barco_bot(self):
        for _ in range(self.QUANTIDADES_DE_BARCOS): 
            while True:
                linha = random.randint(0, self.tamanho - 1)
                coluna = random.randint(0, self.tamanho - 1)
                if self.colocar_barco(linha, coluna):
                    break
            
    def colocar_barco(self, linha, coluna):
        if linha >= 0 and linha < self.tamanho and coluna >= 0 and coluna < self.tamanho: 
            if self.mapa[linha][coluna] == ".":
                self.mapa[linha][coluna] = "B"
                return True
            else:
                digitar("Já existe um barco nessa posição!")
                return False
        else:
            digitar("Posição Invalida!")
            return False
    
    def posicionar_barco_jogador(self):
        print(self)
        while True:
            linhas, colunas = self.ler_coordenadas("Digite a posição (EX: F7): ")

            if self.colocar_barco(linhas, colunas):
                print(self)
                break

class Jogador():
    def __init__(self, nome ="", vitorias =0, derrotas =0):
        self.nome = nome
        self.vitorias = vitorias
        self.derrotas = derrotas
    
    def __str__(self):
        return f"\n===== STATS =====\nJogador: {self.nome}\nVitorias: {self.vitorias}\nDerrotas: {self.derrotas}\n=================\n"
    
    def salvar_jogador(self):
            with open("dados_jogador.txt", "w") as arquivo:
                arquivo.write(self.nome + "\n")
                arquivo.write(str(self.vitorias) + "\n")
                arquivo.write(str(self.derrotas) + "\n")
        
    def carregar_jogador(self):
        with open("dados_jogador.txt", "r") as arquivo:
            self.nome = arquivo.readline().strip()
            self.vitorias = int(arquivo.readline().strip())
            self.derrotas = int(arquivo.readline().strip())



#FUNÇÕES DO SISTEMA
def ler_int(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            digitar("\nDigite apenas Numeros!\n")

def digitar(texto, velocidade=0.05):
    for letra in texto:
        print(letra, end="", flush=True)
        time.sleep(velocidade)
    print()

def turno_jogador(tabuleiro_bot):
    while True:
        print(tabuleiro_bot.mostrar_tabuleiro_oculto())

        linhas, colunas = tabuleiro_bot.ler_coordenadas("Digite a posição (EX: F7): ")
        resultado = tabuleiro_bot.atacar(linhas, colunas)

        if resultado is None:
            digitar("Você já atacou essa posição!")
            continue
    
        print("\nAnalisando...")
        time.sleep(1.5)

        if resultado is True:
            digitar("Você acertou um barco!")
        elif resultado is False:
            digitar("Água!")

        break

def turno_bot(tabuleiro_jogador):
    print("\nO Bot esta pensando..." )
    time.sleep(2)

    while True:
        linhas = random.randint(0, tabuleiro_jogador.tamanho - 1)
        coluna = random.randint(0, tabuleiro_jogador.tamanho - 1)

        resultado = tabuleiro_jogador.atacar(linhas, coluna)

        if resultado is None:
            continue

        digitar(f"O bot atacou {tabuleiro_jogador.converter_coordenadas_para_texto(linhas, coluna)}!")
       
        if resultado is True:
            digitar("O Bot acertou um dos seus barcos!")
        elif resultado is False:
            digitar("O Bot acertou a Água!")

        break

def partida(tabuleiro_bot, tabuleiro_jogador, jogador):
    while True:
        turno_jogador(tabuleiro_bot)
        print("===== TABULEIRO BOT =====")
        print(tabuleiro_bot.mostrar_tabuleiro_oculto())
        if tabuleiro_bot.barcos_restantes() == 0:
            digitar("Parabens você ganhou o jogo")
            jogador.vitorias += 1
            jogador.salvar_jogador()
            break

        turno_bot(tabuleiro_jogador)
        time.sleep(1.5)
        print("===== SEU TABULEIRO =====")
        print(tabuleiro_jogador)
        if tabuleiro_jogador.barcos_restantes() == 0:
            digitar("O Bot Ganhou a partida")
            digitar("tabela do bot")
            print(tabuleiro_bot)
            jogador.derrotas += 1
            jogador.salvar_jogador()
            break

#VARIAVEIS GLOBAIS
jogador1 = Jogador()
rodando = True

#SISTEMA

try:
    jogador1.carregar_jogador()
except FileNotFoundError:
    nick = input("Para Começar digite seu nome de jogador!: ")
    jogador1.nome = nick
    jogador1.salvar_jogador()

digitar(f"\nBem-Vindo {jogador1.nome} ao batalha Naval", 0.08)
while rodando:
    
    print("1 - Jogar")
    print("2 - Stats")
    print("3 - Regras")
    print("4 - Creditos")
    print("5 - Fechar Jogo\n")

    opcao = ler_int("Qual opção você deseja selecionar? ")
            
    match opcao:
        case 1:
            tabuleiro_jogador = Tabuleiro()
            tabuleiro_bot = Tabuleiro()

            tabuleiro_bot.posicionar_barco_bot()
            for _ in range(tabuleiro_jogador.QUANTIDADES_DE_BARCOS):
                tabuleiro_jogador.posicionar_barco_jogador()
            
            digitar("Jogo iniciado")
            time.sleep(1)
            partida(tabuleiro_bot, tabuleiro_jogador, jogador1)
        case 2:   
            print(jogador1)
        case 3:   
            digitar("Regras")
            #futuro codigo...
        case 4:   
            digitar("Desenvolvedor: Sizer")
        case 5:
            digitar("Fechando Jogo...")
            jogador1.salvar_jogador()
            time.sleep(0.5)
            rodando = False
        case _:        
            print("Opção invalida")

