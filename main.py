import random

class Tabuleiro:

    COLUNAS = "ABCDEFGHIJ"

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

        for _ in range(2): 
            while True:
                letra = random.choice(self.COLUNAS)
                linha_bot = random.randint(0, self.tamanho - 1)
                if self.colocar_barco(linha_bot, self.transformar_coluna(letra)):
                    break
            
    def colocar_barco(self, linha, coluna):
        if linha >= 0 and linha < self.tamanho and coluna >= 0 and coluna < self.tamanho: 
            if self.mapa[linha][coluna] == ".":
                self.mapa[linha][coluna] = "B"
                return True
            else:
                print("Já existe um barco nessa posição!")
                return False
        else:
            print("Posição Invalida!")
            return False
    
    def transformar_coluna(self, coluna):
        while True:
            coluna = coluna.upper()

            if coluna in self.COLUNAS:
                return self.COLUNAS.index(coluna)
            else:
                print("Coluna Invalida!")
                coluna = input("Digite a Coluna: ")
    
    def posicionar_barco_jogador(self):
        print(self)
        while True:
            colunas = input("Digite a coluna onde o barco vai ficar: ")
            linhas = self.ler_linha_tabuleiro("Digite a linha onde o barco vai ficar: ")
            if self.colocar_barco(linhas, self.transformar_coluna(colunas)):
                print(self)
                break
    
    def ler_linha_tabuleiro(self, mensagem):
        while True:
            try:
                valor = int(input(mensagem))
                if valor > 0 and valor <= self.tamanho:
                    return valor - 1
                else:
                    print("Valor fora dos parametros!")
            except ValueError:
                print("Digite apenas numeros!")

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
            print("\nDigite apenas Numeros!\n")

def turno_jogador(tabuleiro_bot):
    while True:
        print(tabuleiro_bot.mostrar_tabuleiro_oculto())

        colunas = tabuleiro_bot.transformar_coluna(input("Digite a Coluna: ")) 
        linhas = tabuleiro_bot.ler_linha_tabuleiro("Digite a Linha: ")
        resultado = tabuleiro_bot.atacar(linhas, colunas)
        
        if resultado is True:
            print("Você acertou um barco!")
        elif resultado is False:
             print("Água!")

        elif resultado is None:
            print("Você já atacou essa posição!")
            continue
        break

def turno_bot(tabuleiro_jogador):
    while True:
        linhas = random.randint(0, tabuleiro_jogador.tamanho - 1)
        letra = tabuleiro_jogador.transformar_coluna(random.choice(tabuleiro_jogador.COLUNAS))
        
        resultado = tabuleiro_jogador.atacar(linhas, letra)
       
        if resultado is True:
            print("O Bot acertou um dos seus barcos!")
        elif resultado is False:
            print("O Bot acertou a Água!")
       
        elif resultado is None:
            continue
        break

def partida(tabuleiro_bot, tabuleiro_jogador, jogador):
    while True:
        turno_jogador(tabuleiro_bot)
        print(tabuleiro_bot.mostrar_tabuleiro_oculto())
        if tabuleiro_bot.barcos_restantes() == 0:
            print("Parabens você ganhou o jogo")
            jogador.vitorias += 1
            jogador.salvar_jogador()
            break

        turno_bot(tabuleiro_jogador)
        print("===== SEU TABULEIRO =====")
        print(tabuleiro_jogador)
        if tabuleiro_jogador.barcos_restantes() == 0:
            print("O Bot Ganhou a partida")
            print("tabela dpo bot")
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

print(f"\nBem-Vindo {jogador1.nome} ao batalha Naval")
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
            for _ in range(2):
                tabuleiro_jogador.posicionar_barco_jogador()
            
            print("Jogo iniciado")
            partida(tabuleiro_bot, tabuleiro_jogador, jogador1)
        case 2:   
            print(jogador1)
        case 3:   
            print("Regras")
            #futuro codigo...
        case 4:   
            print("Desenvolvedor: Sizer")
        case 5:
            print("Fechando Jogo...")
            jogador1.salvar_jogador()
            rodando = False
        case _:        
            print("Opção invalida")

