# ============================================================
#  JoviLens -- Assistente Inteligente de Camera
#  Computational Thinking with Python -- Sprint 2
#  FIAP x JOVI Challenge 2026
# ============================================================

# -- Dados globais --------------------------------------------

MODOS = [
    "Foto", "Retrato", "Doc", "Video",
    "Noite", "Traduzir", "QR", "Pro",
    "Slow", "Cinema", "Pano", "Objeto"
]

DISCIPLINAS = [
    "Matematica", "Portugues", "Historia", "Geografia",
    "Fisica", "Quimica", "Biologia", "Ingles",
    "Filosofia", "Sociologia", "Ed. Fisica", "Outra"
]

# Palavras-chave por modo para deteccao de contexto
REGRAS = {
    "Doc":      ["caderno", "lousa", "papel", "documento", "texto",
                 "folha", "livro", "apostila", "prova", "scan"],
    "Noite":    ["escuro", "noite", "pouca luz", "sombra", "festa"],
    "Retrato":  ["pessoa", "rosto", "selfie", "retrato", "amigo", "turma"],
    "Traduzir": ["traduz", "ingles", "espanhol", "frances", "estrangeiro",
                 "placa", "cardapio", "idioma"],
    "QR":       ["qr", "codigo", "barcode", "link", "pix"],
    "Video":    ["video", "gravar", "filmagem", "apresentacao", "live"],
    "Objeto":   ["objeto", "planta", "flor", "produto", "identificar"],
    "Pano":     ["panorama", "paisagem", "amplo", "horizonte"],
    "Slow":     ["lento", "slow", "slowmo", "detalhe"],
    "Cinema":   ["cinema", "cinematico", "filme", "widescreen"],
    "Pro":      ["manual", "iso", "exposicao", "profissional"],
}

# Dicionario de traducao simulada: palavra em ingles -> portugues
# Em producao: substituir pelo retorno da Google Translate API
TRADUCOES = {
    "hello":        "ola",
    "world":        "mundo",
    "camera":       "camera",
    "photo":        "foto",
    "picture":      "imagem",
    "night":        "noite",
    "portrait":     "retrato",
    "document":     "documento",
    "translate":    "traduzir",
    "settings":     "configuracoes",
    "flash":        "flash",
    "zoom":         "zoom",
    "capture":      "capturar",
    "mode":         "modo",
    "filter":       "filtro",
    "brightness":   "brilho",
    "contrast":     "contraste",
    "focus":        "foco",
    "video":        "video",
    "record":       "gravar",
    "play":         "reproduzir",
    "stop":         "parar",
    "save":         "salvar",
    "delete":       "deletar",
    "share":        "compartilhar",
    "gallery":      "galeria",
    "album":        "album",
    "smile":        "sorria",
    "ready":        "pronto",
    "slow":         "lento",
    "fast":         "rapido",
    "wide":         "amplo",
    "close":        "perto",
    "open":         "aberto",
    "menu":         "menu",
    "back":         "voltar",
    "next":         "proximo",
    "done":         "concluido",
    "cancel":       "cancelar",
    "confirm":      "confirmar",
    "error":        "erro",
    "success":      "sucesso",
    "loading":      "carregando",
    "processing":   "processando",
}

# Idiomas disponiveis para o modo traducao
IDIOMAS = [
    "Ingles  -> Portugues",
    "Espanhol -> Portugues (simulado)",
    "Frances -> Portugues (simulado)",
]

# Historico de capturas (lista de dicionarios)
historico = []

# Historico de traducoes realizadas (lista de dicionarios)
traducoes_historico = []

# Aulas registradas (lista de dicionarios)
aulas = []


# -- Utilitarios ----------------------------------------------

def linha(char="-", tamanho=50):
    print(char * tamanho)


def cabecalho(titulo):
    print()
    linha("=")
    print("  " + titulo)
    linha("=")


def pausar():
    input("\n  [ Enter para continuar ] ")


def barra_progresso(valor, maximo, largura=20):
    # Gera barra ASCII. Ex: [####........] 40%
    if maximo == 0:
        preenchido  = 0
        porcentagem = 0
    else:
        preenchido  = int((valor / maximo) * largura)
        porcentagem = int((valor / maximo) * 100)

    vazio = largura - preenchido
    return "[" + "#" * preenchido + "." * vazio + "] " + str(porcentagem) + "%"


# -- FUNCIONALIDADE 1: Deteccao de modo por cena --------------

def detectar_modo(descricao):
    # Analisa descricao e retorna lista [modo, pontuacao]
    descricao_lower = descricao.lower()
    melhor_modo     = "Foto"
    melhor_pontos   = 0

    for modo in REGRAS:
        pontos = 0
        for palavra in REGRAS[modo]:
            if palavra in descricao_lower:
                pontos = pontos + 1

        if pontos > melhor_pontos:
            melhor_pontos = pontos
            melhor_modo   = modo

    return [melhor_modo, melhor_pontos]


def palavras_encontradas(descricao, modo):
    # Retorna lista das palavras-chave que ativaram a sugestao
    descricao_lower = descricao.lower()
    encontradas     = []

    if modo in REGRAS:
        for palavra in REGRAS[modo]:
            if palavra in descricao_lower:
                encontradas.append(palavra)

    return encontradas


def registrar_captura(modo, descricao):
    # Cria dicionario da captura e adiciona no historico
    captura = {
        "id":        len(historico) + 1,
        "modo":      modo,
        "descricao": descricao,
    }
    historico.append(captura)

    print()
    print("  >>> Captura #" + str(captura["id"]) + " registrada!")
    print("      Modo : " + modo)
    if descricao != "":
        print("      Cena : " + descricao)


def funcionalidade_detectar_cena():
    cabecalho("FUNC 1 -- Deteccao Inteligente de Modo por Cena")

    print()
    print("  Descreva o que voce quer fotografar.")
    print("  A IA analisa o contexto e sugere o modo ideal.")
    print()

    descricao = input("  Descreva a cena: ").strip()

    # Validacao da entrada
    if descricao == "":
        print("\n  AVISO: Descricao vazia. Tente novamente.")
        pausar()
        return

    if len(descricao) < 3:
        print("\n  AVISO: Descricao muito curta. Seja mais especifico.")
        pausar()
        return

    # Analise da cena
    print("\n  Analisando...")
    resultado = detectar_modo(descricao)
    modo      = resultado[0]
    pontos    = resultado[1]

    # Calcula confianca em porcentagem (maximo 100)
    confianca = pontos * 20
    if confianca > 100:
        confianca = 100

    # Exibe resultado
    print()
    linha("-", 40)
    print("  Modo sugerido : " + modo)
    print("  Indicador     : " + barra_progresso(confianca, 100))
    linha("-", 40)

    # Palavras que ativaram a sugestao
    encontradas = palavras_encontradas(descricao, modo)
    if len(encontradas) > 0:
        print("  Palavras-chave: " + ", ".join(encontradas))

    print()
    confirma = input("  Aplicar modo e registrar captura? (s/n): ").strip().lower()

    if confirma == "s":
        registrar_captura(modo, descricao)
    else:
        # Permite escolher outro modo manualmente
        print()
        print("  Modos disponiveis:")
        for i in range(len(MODOS)):
            print("    " + str(i + 1) + ". " + MODOS[i])

        print()
        escolha = input("  Numero do modo (ou Enter para cancelar): ").strip()

        if escolha.isdigit():
            numero = int(escolha)
            if 1 <= numero <= len(MODOS):
                registrar_captura(MODOS[numero - 1], descricao)
            else:
                print("\n  AVISO: Numero fora do intervalo.")
        else:
            print("\n  Captura cancelada.")

    pausar()


# -- FUNCIONALIDADE 2: Traducao de texto ----------------------

def traduzir_texto(texto):
    # Traduz palavra por palavra usando o dicionario TRADUCOES
    # Palavras nao encontradas sao mantidas no original com marcacao
    palavras        = texto.lower().split()
    palavras_traduz = []
    nao_encontradas = []

    for palavra in palavras:
        # Remove pontuacao basica para buscar no dicionario
        palavra_limpa = palavra.replace(",", "").replace(".", "").replace("!", "").replace("?", "")

        if palavra_limpa in TRADUCOES:
            palavras_traduz.append(TRADUCOES[palavra_limpa])
        else:
            palavras_traduz.append("[" + palavra_limpa + "?]")
            nao_encontradas.append(palavra_limpa)

    resultado = " ".join(palavras_traduz)
    return [resultado, nao_encontradas]


def funcionalidade_traducao():
    cabecalho("FUNC 2 -- Traducao de Texto (Modo Camera)")

    print()
    print("  Simula o modo de traducao da camera JoviLens.")
    print("  Voce digita o texto capturado (em ingles),")
    print("  e o sistema retorna a traducao para portugues.")
    print()

    # Escolha do idioma de origem
    print("  Idiomas disponiveis:")
    for i in range(len(IDIOMAS)):
        print("    " + str(i + 1) + ". " + IDIOMAS[i])

    idioma_escolhido = ""
    while idioma_escolhido == "":
        print()
        escolha = input("  Numero do idioma: ").strip()
        if escolha.isdigit():
            numero = int(escolha)
            if 1 <= numero <= len(IDIOMAS):
                idioma_escolhido = IDIOMAS[numero - 1]
            else:
                print("  AVISO: Numero fora do intervalo.")
        else:
            print("  AVISO: Digite um numero valido.")

    print()
    print("  Idioma selecionado: " + idioma_escolhido)

    # Loop de traducao -- usuario pode traduzir varias frases
    contador = 1
    while True:
        print()
        linha("-", 46)
        texto = input("  Texto " + str(contador) + " (ou 'sair'): ").strip()

        if texto.lower() == "sair" or texto.lower() == "s":
            break

        if texto == "":
            print("  AVISO: Texto vazio. Tente novamente.")
            continue

        if len(texto) < 2:
            print("  AVISO: Texto muito curto.")
            continue

        # Realiza a traducao
        resultado     = traduzir_texto(texto)
        traducao      = resultado[0]
        nao_traduzidas = resultado[1]

        # Calcula taxa de sucesso da traducao
        total_palavras    = len(texto.split())
        palavras_ok       = total_palavras - len(nao_traduzidas)
        barra             = barra_progresso(palavras_ok, total_palavras)

        print()
        print("  Original  : " + texto)
        print("  Traducao  : " + traducao)
        print("  Precisao  : " + barra)

        if len(nao_traduzidas) > 0:
            print("  Sem match : " + ", ".join(nao_traduzidas))

        # Salva no historico de traducoes
        registro = {
            "id":      len(traducoes_historico) + 1,
            "idioma":  idioma_escolhido,
            "original": texto,
            "traducao": traducao,
        }
        traducoes_historico.append(registro)
        print()
        print("  >>> Traducao #" + str(registro["id"]) + " salva no historico.")

        contador = contador + 1

    # Exibe resumo das traducoes realizadas na sessao
    realizadas = contador - 1
    if realizadas > 0:
        print()
        linha("=", 46)
        print("  SESSAO CONCLUIDA")
        linha("=", 46)
        print("  Traducoes realizadas : " + str(realizadas))
        print("  Total no historico   : " + str(len(traducoes_historico)))

        print()
        ver = input("  Ver historico completo de traducoes? (s/n): ").strip().lower()
        if ver == "s":
            print()
            print("  ID   ORIGINAL                  TRADUCAO")
            linha("-", 60)
            for t in traducoes_historico:
                orig  = t["original"]
                trad  = t["traducao"]
                if len(orig) > 22:
                    orig = orig[:22] + "..."
                if len(trad) > 22:
                    trad = trad[:22] + "..."
                print("  " + str(t["id"]).ljust(4) +
                      orig.ljust(26) +
                      trad)

    pausar()


# -- FUNCIONALIDADE 3: Modo Aula ------------------------------

def detectar_tipo_conteudo(descricao):
    # Detecta o tipo de conteudo da captura
    descricao_lower = descricao.lower()

    tipos = {
        "lousa":     ["lousa", "quadro", "quadro negro"],
        "caderno":   ["caderno", "anotacao", "rascunho"],
        "apostila":  ["apostila", "folha", "impresso", "livro", "xerox"],
        "exercicio": ["exercicio", "questao", "problema", "tarefa", "lista"],
        "diagrama":  ["mapa", "grafico", "diagrama", "tabela", "esquema"],
    }

    for tipo in tipos:
        for palavra in tipos[tipo]:
            if palavra in descricao_lower:
                return tipo

    return "geral"


def funcionalidade_modo_aula():
    cabecalho("FUNC 3 -- Modo Aula")

    print()
    print("  Registre o conteudo de uma aula inteira,")
    print("  organizado por disciplina.")
    print()

    # Selecionar disciplina
    print("  Disciplinas:")
    for i in range(len(DISCIPLINAS)):
        print("    " + str(i + 1) + ". " + DISCIPLINAS[i])

    disciplina = ""
    while disciplina == "":
        print()
        escolha = input("  Numero da disciplina (0 = digitar outra): ").strip()

        if escolha == "0":
            disciplina = input("  Nome: ").strip()
            if disciplina == "":
                print("  AVISO: Nome invalido.")

        elif escolha.isdigit():
            numero = int(escolha)
            if 1 <= numero <= len(DISCIPLINAS):
                disciplina = DISCIPLINAS[numero - 1]
            else:
                print("  AVISO: Numero fora do intervalo.")
        else:
            print("  AVISO: Digite um numero.")

    professor = input("\n  Professor (Enter para pular): ").strip()
    if professor == "":
        professor = "Nao informado"

    # Sessao de capturas
    print()
    linha("-", 46)
    print("  SESSAO -- " + disciplina.upper())
    linha("-", 46)
    print("  Descreva cada foto. Digite 'fim' para encerrar.")
    print()

    capturas_aula  = []
    numero_captura = 1

    while True:
        entrada = input("  Captura " + str(numero_captura) + " (ou 'fim'): ").strip()

        if entrada.lower() == "fim" or entrada.lower() == "f":
            if len(capturas_aula) == 0:
                print("\n  Nenhuma captura. Saindo do Modo Aula.")
                pausar()
                return
            break

        if entrada == "":
            print("  AVISO: Descricao vazia.")
            continue

        tipo = detectar_tipo_conteudo(entrada)

        item = {
            "numero":    numero_captura,
            "descricao": entrada,
            "tipo":      tipo
        }
        capturas_aula.append(item)

        # Registra no historico geral tambem
        registrar_captura("Doc", "[Aula " + disciplina + "] " + entrada)
        print("      Tipo: " + tipo.upper())

        numero_captura = numero_captura + 1

    # Salva aula na lista de aulas
    aula = {
        "id":         len(aulas) + 1,
        "disciplina": disciplina,
        "professor":  professor,
        "capturas":   capturas_aula,
        "total":      len(capturas_aula)
    }
    aulas.append(aula)

    # Lista tipos encontrados para o resumo
    tipos_encontrados = []
    for c in capturas_aula:
        if c["tipo"] not in tipos_encontrados:
            tipos_encontrados.append(c["tipo"])

    print()
    linha("=", 46)
    print("  SESSAO CONCLUIDA -- " + disciplina.upper())
    linha("=", 46)
    print("  Capturas  : " + str(len(capturas_aula)))
    print("  Professor : " + professor)
    print("  Conteudos : " + ", ".join(tipos_encontrados))

    # Exportar como arquivo de texto
    print()
    exportar = input("  Exportar registro? (s/n): ").strip().lower()

    if exportar == "s":
        nome = "aula_" + disciplina.replace(" ", "_") + "_" + str(aula["id"]) + ".txt"

        conteudo  = "=" * 50 + "\n"
        conteudo += "JoviLens -- Modo Aula\n"
        conteudo += "=" * 50 + "\n"
        conteudo += "Disciplina : " + disciplina + "\n"
        conteudo += "Professor  : " + professor + "\n"
        conteudo += "Capturas   : " + str(len(capturas_aula)) + "\n"
        conteudo += "-" * 50 + "\n"

        for c in capturas_aula:
            conteudo += str(c["numero"]) + ". [" + c["tipo"].upper() + "] " + c["descricao"] + "\n"

        conteudo += "=" * 50 + "\n"

        arquivo = open(nome, "w")
        arquivo.write(conteudo)
        arquivo.close()

        print("  Arquivo gerado: " + nome)

    # Mostra lista de aulas registradas
    if len(aulas) > 1:
        print()
        ver = input("  Ver todas as aulas? (s/n): ").strip().lower()
        if ver == "s":
            print()
            print("  ID   DISCIPLINA       CAPTURAS")
            linha("-", 36)
            for a in aulas:
                print("  " + str(a["id"]).ljust(4) +
                      a["disciplina"].ljust(16) +
                      str(a["total"]).rjust(6))

    pausar()


# -- MENU PRINCIPAL -------------------------------------------

def exibir_menu():
    print()
    print("  +--------------------------------------------+")
    print("  |      JoviLens -- IA de Camera              |")
    print("  |      FIAP x JOVI Challenge 2026            |")
    print("  +--------------------------------------------+")

    if len(historico) > 0:
        texto = "Capturas: " + str(len(historico))
        print("  |  " + texto.ljust(43) + "|")

    if len(traducoes_historico) > 0:
        texto = "Traducoes: " + str(len(traducoes_historico))
        print("  |  " + texto.ljust(43) + "|")

    print("  +--------------------------------------------+")
    print("  |                                            |")
    print("  |   1 - Detectar modo por cena               |")
    print("  |   2 - Traducao de texto                    |")
    print("  |   3 - Modo Aula                            |")
    print("  |                                            |")
    print("  |   0 - Sair                                 |")
    print("  |                                            |")
    print("  +--------------------------------------------+")


def main():
    while True:
        exibir_menu()

        opcao = input("\n  Escolha: ").strip()

        if opcao == "1":
            funcionalidade_detectar_cena()
        elif opcao == "2":
            funcionalidade_traducao()
        elif opcao == "3":
            funcionalidade_modo_aula()
        elif opcao == "0":
            print()
            print("  Encerrando JoviLens.")
            print("  Capturas realizadas  : " + str(len(historico)))
            print("  Traducoes realizadas : " + str(len(traducoes_historico)))
            print()
            break
        else:
            print("\n  AVISO: Opcao invalida. Escolha entre 0 e 3.")
            pausar()


# -- Inicio ---------------------------------------------------

main()