# ============================================================
#  JoviLens — Assistente Inteligente de Câmera
#  Computational Thinking with Python — Sprint 2
#  FIAP x JOVI Challenge 2026
# ============================================================
#
#  Funcionalidades implementadas:
#   1. Detecção automática de modo por análise de cena
#   2. Histórico personalizado com sugestão por horário
#   3. Modo Aula — OCR + organização por disciplina em PDF
#
# ============================================================

import json
import os
from datetime import datetime

# ── Constantes e dados globais ────────────────────────────────

MODOS_DISPONIVEIS = [
    "Foto", "Retrato", "Doc", "Vídeo",
    "Noite", "Traduzir", "QR", "Pro",
    "Slow", "Cinema", "Pano", "Objeto"
]

ARQUIVO_HISTORICO = "jovilens_historico.json"
ARQUIVO_AULAS     = "jovilens_aulas.json"

# Regras de detecção de contexto por palavras-chave
REGRAS_CONTEXTO = {
    "Doc": [
        "caderno", "lousa", "papel", "documento", "texto",
        "folha", "livro", "apostila", "planilha", "prova",
        "gabarito", "anotação", "escanear", "scan"
    ],
    "Noite": [
        "escuro", "noite", "pouca luz", "penumbra",
        "sombra", "festa", "bar", "show", "concerto"
    ],
    "Retrato": [
        "pessoa", "rosto", "selfie", "retrato", "amigo",
        "colega", "professor", "grupo", "turma", "foto"
    ],
    "Traduzir": [
        "traduz", "inglês", "espanhol", "francês", "alemão",
        "japonês", "chinês", "coreano", "estrangeiro", "placa",
        "cardápio", "menu", "legenda", "idioma"
    ],
    "QR": [
        "qr", "código", "barcode", "código de barras",
        "link", "ler código", "pix", "cupom"
    ],
    "Vídeo": [
        "vídeo", "gravar", "filmagem", "gravação",
        "apresentação", "aula", "tutorial", "live"
    ],
    "Objeto": [
        "objeto", "planta", "flor", "inseto", "produto",
        "identificar", "reconhecer", "o que é", "que planta"
    ],
    "Pano":  ["panorama", "paisagem", "amplo", "cidade", "horizonte"],
    "Slow":  ["câmera lenta", "slow", "slowmo", "devagar", "detalhe"],
    "Cinema":["cinema", "cinemático", "filme", "widescreen"],
    "Pro":   ["manual", "iso", "exposição", "ev", "profissional", "raw"],
}

DISCIPLINAS_PADRAO = [
    "Matemática", "Português", "História", "Geografia",
    "Física", "Química", "Biologia", "Inglês",
    "Filosofia", "Sociologia", "Ed. Física", "Outra"
]


# ── Utilitários ───────────────────────────────────────────────

def linha(char="─", largura=50):
    """Imprime uma linha divisória."""
    print(char * largura)


def cabecalho(titulo: str):
    """Imprime um cabeçalho formatado."""
    print()
    linha("═")
    print(f"  {titulo}")
    linha("═")


def pausar():
    """Aguarda o usuário pressionar Enter."""
    input("\n  [ Enter para continuar ] ")


def timestamp() -> str:
    """Retorna timestamp formatado."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def hora_atual() -> str:
    """Retorna apenas a hora atual."""
    return datetime.now().strftime("%H:%M")


def periodo_do_dia() -> str:
    """Classifica o período do dia."""
    hora = datetime.now().hour
    if 5 <= hora < 12:
        return "manhã"
    elif 12 <= hora < 18:
        return "tarde"
    elif 18 <= hora < 23:
        return "noite"
    else:
        return "madrugada"


# ── Gerenciamento de Histórico ────────────────────────────────

def carregar_historico() -> list:
    """Carrega o histórico de capturas do arquivo JSON."""
    if not os.path.exists(ARQUIVO_HISTORICO):
        return []
    try:
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def salvar_historico(historico: list) -> None:
    """Salva o histórico de capturas no arquivo JSON."""
    try:
        with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"  ⚠️  Erro ao salvar histórico: {e}")


def registrar_captura(modo: str, descricao: str = "", historico: list = None) -> dict:
    """
    Registra uma nova captura no histórico.
    Retorna o dicionário da captura registrada.
    """
    periodo = periodo_do_dia()
    captura = {
        "id":        len(historico) + 1 if historico else 1,
        "modo":      modo,
        "descricao": descricao,
        "horario":   hora_atual(),
        "timestamp": timestamp(),
        "periodo":   periodo
    }
    if historico is not None:
        historico.append(captura)
        salvar_historico(historico)

    print(f"\n  ✅ Captura #{captura['id']} registrada!")
    print(f"     Modo    : {modo}")
    print(f"     Horário : {captura['horario']} ({periodo})")
    if descricao:
        print(f"     Cena    : {descricao}")
    return captura


# ── FUNCIONALIDADE 1: Detecção de Contexto ───────────────────

def detectar_modo_por_cena(descricao: str) -> tuple[str, float]:
    """
    Analisa a descrição da cena e retorna o modo mais adequado
    junto com o score de confiança (0.0 a 1.0).
    """
    descricao_lower = descricao.lower()
    scores = {}

    for modo, palavras in REGRAS_CONTEXTO.items():
        # Conta quantas palavras-chave aparecem na descrição
        matches = sum(1 for palavra in palavras if palavra in descricao_lower)
        if matches > 0:
            # Score proporcional ao número de matches e total de palavras
            scores[modo] = matches / len(palavras)

    if not scores:
        return "Foto", 0.0

    # Retorna o modo com maior score
    melhor_modo = max(scores, key=scores.get)
    confianca   = min(scores[melhor_modo] * 10, 1.0)  # normaliza para 0-1
    return melhor_modo, confianca


def funcionalidade_detectar_cena(historico: list) -> None:
    """Fluxo completo de detecção de modo por descrição de cena."""
    cabecalho("🔍 DETECÇÃO INTELIGENTE DE MODO")

    print("\n  Descreva o que você quer fotografar/filmar.")
    print("  A IA analisará o contexto e sugerirá o melhor modo.\n")

    descricao = input("  📝 Descreva a cena: ").strip()

    if not descricao:
        print("\n  ⚠️  Descrição vazia. Tente novamente.")
        pausar()
        return

    if len(descricao) < 3:
        print("\n  ⚠️  Descrição muito curta. Seja mais específico.")
        pausar()
        return

    # Análise
    print("\n  🤖 Analisando cena...")
    modo, confianca = detectar_modo_por_cena(descricao)

    # Exibe resultado
    print(f"\n  ┌{'─'*36}┐")
    print(f"  │  Modo sugerido : {modo:<18}│")
    print(f"  │  Confiança     : {f'{confianca*100:.0f}%':<18}│")
    print(f"  └{'─'*36}┘")

    # Exibe barra de confiança
    barras = int(confianca * 20)
    barra  = "█" * barras + "░" * (20 - barras)
    print(f"\n  Confiança: [{barra}] {confianca*100:.0f}%")

    # Motivo da sugestão
    palavras_encontradas = [
        p for p in REGRAS_CONTEXTO.get(modo, [])
        if p in descricao.lower()
    ]
    if palavras_encontradas:
        print(f"\n  🔑 Palavras detectadas: {', '.join(palavras_encontradas)}")

    # Confirma aplicação
    print()
    confirma = input("  Aplicar este modo e registrar captura? (s/n): ").strip().lower()

    if confirma == "s":
        registrar_captura(modo, descricao, historico)

        # Verifica se é modo Aula (Doc + horário de aula)
        if modo == "Doc" and periodo_do_dia() in ("manhã", "tarde"):
            print("\n  💡 Dica: Parece que você está em aula!")
            ir_aula = input("     Quer salvar como registro de aula? (s/n): ").strip().lower()
            if ir_aula == "s":
                funcionalidade_modo_aula(historico, modo_direto=True,
                                         descricao_externa=descricao)
                return
    else:
        # Permite escolher outro modo
        print("\n  Modos disponíveis:")
        for i, m in enumerate(MODOS_DISPONIVEIS, 1):
            print(f"    {i:>2}. {m}")
        escolha = input("\n  Escolha outro modo (número) ou Enter para cancelar: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(MODOS_DISPONIVEIS):
            modo_manual = MODOS_DISPONIVEIS[int(escolha) - 1]
            registrar_captura(modo_manual, descricao, historico)

    pausar()


# ── FUNCIONALIDADE 2: Histórico e Sugestão por Horário ───────

def analisar_padroes(historico: list) -> dict:
    """
    Analisa o histórico e retorna estatísticas de uso.
    Retorna dicionário com modos mais usados por período.
    """
    if not historico:
        return {}

    padroes = {"manhã": {}, "tarde": {}, "noite": {}, "madrugada": {}}

    for captura in historico:
        periodo = captura.get("periodo", "tarde")
        modo    = captura.get("modo", "Foto")
        if periodo in padroes:
            padroes[periodo][modo] = padroes[periodo].get(modo, 0) + 1

    return padroes


def sugerir_modo_por_horario(historico: list) -> str | None:
    """
    Sugere um modo baseado no histórico de uso no período atual.
    Retorna o modo sugerido ou None se não há histórico suficiente.
    """
    if len(historico) < 3:
        return None

    padroes = analisar_padroes(historico)
    periodo = periodo_do_dia()
    usos_periodo = padroes.get(periodo, {})

    if not usos_periodo:
        return None

    return max(usos_periodo, key=usos_periodo.get)


def funcionalidade_historico(historico: list) -> None:
    """Exibe histórico completo com análise de padrões e sugestão personalizada."""
    cabecalho("📊 HISTÓRICO E PERFIL DE USO")

    if not historico:
        print("\n  📭 Nenhuma captura registrada ainda.")
        print("     Use a opção 1 para começar a registrar!")
        pausar()
        return

    # ── Resumo geral ──────────────────────────────────────
    total = len(historico)
    print(f"\n  Total de capturas: {total}")
    print(f"  Período atual    : {periodo_do_dia().capitalize()}")

    # Contagem por modo
    contagem_modos = {}
    for c in historico:
        modo = c.get("modo", "Foto")
        contagem_modos[modo] = contagem_modos.get(modo, 0) + 1

    modo_favorito = max(contagem_modos, key=contagem_modos.get)

    print(f"\n  {'MODO':<14} {'USOS':>5}  {'PROPORÇÃO'}")
    linha()
    for modo, usos in sorted(contagem_modos.items(), key=lambda x: -x[1]):
        prop      = usos / total
        barras    = int(prop * 20)
        barra_str = "█" * barras + "░" * (20 - barras)
        estrela   = " ★" if modo == modo_favorito else ""
        print(f"  {modo:<14} {usos:>5}  [{barra_str}]{estrela}")

    # ── Padrões por período ───────────────────────────────
    padroes = analisar_padroes(historico)
    print(f"\n  {'PERÍODO':<12} {'MODO MAIS USADO':<14} {'USOS':>5}")
    linha()
    for periodo, modos in padroes.items():
        if modos:
            melhor = max(modos, key=modos.get)
            print(f"  {periodo.capitalize():<12} {melhor:<14} {modos[melhor]:>5}")
        else:
            print(f"  {periodo.capitalize():<12} {'(sem dados)':<14}")

    # ── Sugestão personalizada ────────────────────────────
    sugestao = sugerir_modo_por_horario(historico)
    if sugestao:
        print(f"\n  💡 Baseado no seu histórico, agora ({hora_atual()})")
        print(f"     você costuma usar: [{sugestao}]")
        usar = input(f"     Registrar captura em modo {sugestao} agora? (s/n): ").strip().lower()
        if usar == "s":
            registrar_captura(sugestao, f"Sugestão automática — {periodo_do_dia()}", historico)

    # ── Últimas 5 capturas ────────────────────────────────
    print(f"\n  Últimas {min(5, total)} capturas:")
    linha()
    for c in reversed(historico[-5:]):
        desc = f" — {c['descricao'][:28]}..." if c.get('descricao') else ""
        print(f"  #{c['id']:<4} {c['modo']:<10} {c['horario']}  {c['periodo']}{desc}")

    pausar()


# ── FUNCIONALIDADE 3: Modo Aula ───────────────────────────────

def carregar_aulas() -> list:
    """Carrega os registros de aulas do arquivo JSON."""
    if not os.path.exists(ARQUIVO_AULAS):
        return []
    try:
        with open(ARQUIVO_AULAS, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def salvar_aulas(aulas: list) -> None:
    """Salva os registros de aulas no arquivo JSON."""
    try:
        with open(ARQUIVO_AULAS, "w", encoding="utf-8") as f:
            json.dump(aulas, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"  ⚠️  Erro ao salvar aulas: {e}")


def exportar_aula_pdf_simulado(aula: dict) -> str:
    """
    Simula a exportação de uma aula para PDF.
    (Em produção, usaria bibliotecas como reportlab ou fpdf2)
    Retorna o nome do arquivo gerado.
    """
    nome_arquivo = (
        f"aula_{aula['disciplina'].replace(' ', '_')}_"
        f"{aula['data'].replace('/', '-')}_"
        f"{aula['horario'].replace(':', 'h')}.txt"
    )

    conteudo = f"""
╔══════════════════════════════════════════════════════════════╗
║                    JoviLens — Modo Aula                      ║
║              Registro OCR de Material de Estudo              ║
╚══════════════════════════════════════════════════════════════╝

Disciplina : {aula['disciplina']}
Professor  : {aula.get('professor', 'Não informado')}
Data       : {aula['data']}
Horário    : {aula['horario']}
Capturas   : {aula['total_capturas']} foto(s)

{'═'*62}
CONTEÚDO CAPTURADO (OCR Simulado)
{'═'*62}

{aula.get('conteudo_ocr', 'Conteúdo não disponível')}

{'═'*62}
Tags: {', '.join(aula.get('tags', []))}
Gerado em : {timestamp()}
{'═'*62}
"""

    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(conteudo)
        return nome_arquivo
    except IOError:
        return ""


def funcionalidade_modo_aula(historico: list,
                              modo_direto: bool = False,
                              descricao_externa: str = "") -> None:
    """
    Modo Aula: captura múltiplas fotos de conteúdo de aula,
    organiza por disciplina e gera registro exportável.
    """
    cabecalho("📚 MODO AULA — OCR + ORGANIZAÇÃO")

    aulas = carregar_aulas()

    print("\n  O Modo Aula permite registrar o conteúdo de uma aula")
    print("  inteira: lousa, caderno, apostila. Tudo organizado por")
    print("  disciplina e exportado como documento.\n")

    # ── Selecionar disciplina ─────────────────────────────
    print("  Disciplinas disponíveis:")
    for i, d in enumerate(DISCIPLINAS_PADRAO, 1):
        print(f"    {i:>2}. {d}")

    while True:
        escolha = input("\n  Número da disciplina (ou 0 para digitar outra): ").strip()
        if escolha == "0":
            disciplina = input("  Nome da disciplina: ").strip()
            if disciplina:
                break
            print("  ⚠️  Nome inválido.")
        elif escolha.isdigit() and 1 <= int(escolha) <= len(DISCIPLINAS_PADRAO):
            disciplina = DISCIPLINAS_PADRAO[int(escolha) - 1]
            break
        else:
            print("  ⚠️  Opção inválida.")

    # ── Informações da aula ───────────────────────────────
    professor = input(f"\n  Professor de {disciplina} (Enter para pular): ").strip()

    # ── Sessão de capturas ────────────────────────────────
    print(f"\n  {'─'*46}")
    print(f"  📸 SESSÃO DE CAPTURAS — {disciplina.upper()}")
    print(f"  {'─'*46}")
    print("  Digite o que está sendo fotografado em cada captura.")
    print("  A IA aplicará OCR e detectará o tipo de conteúdo.")
    print("  Digite 'fim' quando terminar a sessão.\n")

    capturas_aula   = []
    linhas_ocr      = []
    tags_detectadas = set()

    # Tipos de conteúdo e suas tags
    tipos_conteudo = {
        "lousa":     ["lousa", "quadro", "quadro negro", "lousa branca"],
        "caderno":   ["caderno", "anotação", "rascunho"],
        "apostila":  ["apostila", "folha", "impresso", "livro", "xerox"],
        "exercício": ["exercício", "questão", "problema", "tarefa", "lista"],
        "mapa":      ["mapa", "gráfico", "diagrama", "tabela", "esquema"],
    }

    numero_captura = 1
    if modo_direto and descricao_externa:
        # Já vem com uma captura pré-registrada
        capturas_aula.append({
            "numero": 1,
            "descricao": descricao_externa,
            "tipo": "lousa"
        })
        linhas_ocr.append(f"[Captura 1] {descricao_externa}")
        tags_detectadas.add("lousa")
        print(f"  ✅ Captura 1 registrada: {descricao_externa}")
        numero_captura = 2

    while True:
        entrada = input(f"  📷 Captura {numero_captura} (ou 'fim'): ").strip()

        if entrada.lower() in ("fim", "f", "sair", "q"):
            if not capturas_aula and numero_captura == 1:
                print("\n  ⚠️  Nenhuma captura registrada. Saindo do Modo Aula.")
                pausar()
                return
            break

        if not entrada:
            print("  ⚠️  Descrição vazia, tente novamente.")
            continue

        # Detecta tipo de conteúdo
        tipo_detectado = "geral"
        for tipo, palavras in tipos_conteudo.items():
            if any(p in entrada.lower() for p in palavras):
                tipo_detectado = tipo
                tags_detectadas.add(tipo)
                break

        # OCR simulado (em produção: Google Vision API)
        ocr_simulado = f"[OCR — {tipo_detectado.upper()}] {entrada}"
        linhas_ocr.append(f"[Captura {numero_captura}] {ocr_simulado}")

        captura_item = {
            "numero":    numero_captura,
            "descricao": entrada,
            "tipo":      tipo_detectado
        }
        capturas_aula.append(captura_item)

        # Registra no histórico geral
        registrar_captura("Doc", f"[Aula {disciplina}] {entrada}", historico)

        print(f"     ✓ Tipo detectado: {tipo_detectado.upper()}")
        numero_captura += 1

    if not capturas_aula:
        print("\n  ⚠️  Sessão encerrada sem capturas.")
        pausar()
        return

    # ── Monta o registro da aula ──────────────────────────
    agora  = datetime.now()
    data   = agora.strftime("%d/%m/%Y")
    horario = agora.strftime("%H:%M")

    # Adiciona tags automáticas
    tags_detectadas.add(disciplina.lower())
    tags_detectadas.add(periodo_do_dia())

    conteudo_ocr_final = "\n".join(linhas_ocr)

    aula_registro = {
        "id":             len(aulas) + 1,
        "disciplina":     disciplina,
        "professor":      professor if professor else "Não informado",
        "data":           data,
        "horario":        horario,
        "total_capturas": len(capturas_aula),
        "capturas":       capturas_aula,
        "conteudo_ocr":   conteudo_ocr_final,
        "tags":           sorted(list(tags_detectadas)),
        "timestamp":      timestamp()
    }

    aulas.append(aula_registro)
    salvar_aulas(aulas)

    # ── Resumo da sessão ──────────────────────────────────
    print(f"\n  {'═'*46}")
    print(f"  ✅ SESSÃO CONCLUÍDA — {disciplina.upper()}")
    print(f"  {'═'*46}")
    print(f"  Total de capturas : {len(capturas_aula)}")
    print(f"  Data              : {data} às {horario}")
    print(f"  Conteúdos         : {', '.join(tags_detectadas - {disciplina.lower(), periodo_do_dia()}) or 'geral'}")

    # ── Exportar ──────────────────────────────────────────
    exportar = input("\n  Exportar registro como documento? (s/n): ").strip().lower()
    if exportar == "s":
        nome_arquivo = exportar_aula_pdf_simulado(aula_registro)
        if nome_arquivo:
            print(f"\n  📄 Documento gerado: {nome_arquivo}")
            print(f"     (Em produção: PDF real com imagens OCR via Google Vision API)")
        else:
            print("\n  ⚠️  Erro ao gerar documento.")

    # ── Listar aulas salvas ───────────────────────────────
    if len(aulas) > 1:
        print(f"\n  📚 Você tem {len(aulas)} aulas registradas no total.")
        ver = input("  Ver todas as aulas? (s/n): ").strip().lower()
        if ver == "s":
            listar_aulas_salvas(aulas)

    pausar()


def listar_aulas_salvas(aulas: list) -> None:
    """Exibe tabela com todas as aulas registradas."""
    print(f"\n  {'#':<4} {'DISCIPLINA':<14} {'DATA':<12} {'HORA':<7} {'CAPTURAS':>8}")
    linha()
    for a in aulas:
        print(
            f"  {a['id']:<4} "
            f"{a['disciplina']:<14} "
            f"{a['data']:<12} "
            f"{a['horario']:<7} "
            f"{a['total_capturas']:>8}"
        )


# ── BÔNUS: Captura Manual ─────────────────────────────────────

def funcionalidade_captura_manual(historico: list) -> None:
    """Permite registrar uma captura manual escolhendo o modo."""
    cabecalho("📷 CAPTURA MANUAL")

    print("\n  Modos disponíveis:\n")
    for i, m in enumerate(MODOS_DISPONIVEIS, 1):
        print(f"    {i:>2}. {m}")

    print()
    while True:
        escolha = input("  Número do modo: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(MODOS_DISPONIVEIS):
            modo = MODOS_DISPONIVEIS[int(escolha) - 1]
            break
        print("  ⚠️  Opção inválida.")

    descricao = input(f"  Descrição da cena em modo {modo} (Enter para pular): ").strip()
    registrar_captura(modo, descricao, historico)
    pausar()


# ── MENU PRINCIPAL ────────────────────────────────────────────

def exibir_menu(historico: list) -> None:
    """Exibe o menu principal com informações contextuais."""
    sugestao = sugerir_modo_por_horario(historico)
    periodo  = periodo_do_dia()
    hora     = hora_atual()

    print("\n")
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║         🎯 JoviLens — IA de Câmera           ║")
    print("  ║           FIAP x JOVI Challenge 2026         ║")
    print("  ╠══════════════════════════════════════════════╣")
    print(f"  ║  🕐 {hora}  •  {periodo.capitalize():<38}║")
    if sugestao:
        print(f"  ║  💡 Sugestão para agora: {sugestao:<22}║")
    if historico:
        print(f"  ║  📸 Capturas hoje: {len(historico):<29}║")
    print("  ╠══════════════════════════════════════════════╣")
    print("  ║                                              ║")
    print("  ║   1  •  Detectar modo por descrição de cena  ║")
    print("  ║   2  •  Ver histórico e perfil de uso        ║")
    print("  ║   3  •  Modo Aula (OCR + organizar por disc.)║")
    print("  ║   4  •  Captura manual                       ║")
    print("  ║                                              ║")
    print("  ║   0  •  Sair                                 ║")
    print("  ║                                              ║")
    print("  ╚══════════════════════════════════════════════╝")


def main() -> None:
    """Função principal — inicializa e executa o menu."""
    os.system("cls" if os.name == "nt" else "clear")

    print("\n  Carregando JoviLens...")
    historico = carregar_historico()
    print(f"  ✓ Histórico carregado: {len(historico)} captura(s)")

    while True:
        exibir_menu(historico)

        opcao = input("\n  Escolha: ").strip()

        match opcao:
            case "1":
                funcionalidade_detectar_cena(historico)
            case "2":
                funcionalidade_historico(historico)
            case "3":
                funcionalidade_modo_aula(historico)
            case "4":
                funcionalidade_captura_manual(historico)
            case "0":
                print("\n  👋 Encerrando JoviLens.")
                print("     Seu histórico foi salvo automaticamente.")
                print(f"     Total de capturas: {len(historico)}\n")
                break
            case _:
                print("\n  ⚠️  Opção inválida. Escolha entre 0 e 4.")
                pausar()


# ── Entry point ───────────────────────────────────────────────

if __name__ == "__main__":
    main()