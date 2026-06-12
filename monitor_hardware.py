"""
Monitor de Hardware - CPU, RAM, Temperatura e Disco
Autor: Seu Nome
Descrição: Monitora recursos do sistema em tempo real e envia alertas
           quando algum componente ultrapassa o limite configurado.

Dependências:
    pip install psutil plyer

Como usar:
    python monitor_hardware.py

    O monitor roda em segundo plano e avisa quando:
    - CPU passar de 80%
    - RAM passar de 85%
    - Temperatura da CPU passar de 80°C
    - Disco passar de 90% de uso
"""

import psutil
import time
import datetime
import os

# ─────────────────────────────────────────────
#  Tenta importar a biblioteca de notificações
# ─────────────────────────────────────────────
try:
    from plyer import notification
    NOTIFICACOES_ATIVAS = True
except ImportError:
    NOTIFICACOES_ATIVAS = False
    print("[AVISO] 'plyer' não instalado. Notificações desativadas.")
    print("        Para ativar, rode: pip install plyer\n")


# ─────────────────────────────────────────────
#  Configurações de alerta (edite à vontade!)
# ─────────────────────────────────────────────
LIMITE_CPU_PERCENT    = 80    # % de uso da CPU
LIMITE_RAM_PERCENT    = 85    # % de uso da RAM
LIMITE_TEMP_CPU       = 80    # °C
LIMITE_DISCO_PERCENT  = 90    # % de uso do disco
INTERVALO_SEGUNDOS    = 5     # Frequência de verificação
ARQUIVO_LOG           = "hardware_log.txt"


# ─────────────────────────────────────────────
#  Funções auxiliares
# ─────────────────────────────────────────────

def hora_atual():
    """Retorna a data e hora formatadas."""
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def salvar_log(mensagem):
    """Salva uma linha no arquivo de log."""
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{hora_atual()}] {mensagem}\n")


def enviar_notificacao(titulo, mensagem):
    """Envia notificação no desktop (se disponível)."""
    print(f"  🔔 ALERTA: {titulo} — {mensagem}")
    salvar_log(f"ALERTA | {titulo}: {mensagem}")
    if NOTIFICACOES_ATIVAS:
        try:
            notification.notify(
                title=titulo,
                message=mensagem,
                app_name="Monitor de Hardware",
                timeout=8,
            )
        except Exception as e:
            print(f"  [Erro na notificação: {e}]")


def obter_temperatura_cpu():
    """
    Tenta ler a temperatura da CPU.
    Funciona melhor no Linux. No Windows pode exigir
    ferramentas extras como o OpenHardwareMonitor.
    """
    try:
        temps = psutil.sensors_temperatures()
        if not temps:
            return None

        # Procura por chaves comuns de temperatura da CPU
        for chave in ("coretemp", "cpu_thermal", "k10temp", "acpitz"):
            if chave in temps:
                leituras = temps[chave]
                if leituras:
                    return leituras[0].current
    except (AttributeError, NotImplementedError):
        pass
    return None


def limpar_tela():
    """Limpa o terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def barra_progresso(valor, maximo=100, largura=25):
    """Gera uma barra de progresso visual em texto."""
    preenchimento = int((valor / maximo) * largura)
    barra = "█" * preenchimento + "░" * (largura - preenchimento)
    return f"[{barra}]"


# ─────────────────────────────────────────────
#  Função principal de monitoramento
# ─────────────────────────────────────────────

def monitorar():
    print("=" * 60)
    print("   🖥️  MONITOR DE HARDWARE  —  iniciando...")
    print(f"   Verificando a cada {INTERVALO_SEGUNDOS}s | Log: {ARQUIVO_LOG}")
    print("   Pressione Ctrl+C para encerrar.")
    print("=" * 60)
    salvar_log("Monitor iniciado.")
    time.sleep(1)

    while True:
        try:
            # ── Coleta de dados ──────────────────────────────
            cpu_percent = psutil.cpu_percent(interval=1)
            ram         = psutil.virtual_memory()
            disco       = psutil.disk_usage("/")
            temperatura = obter_temperatura_cpu()

            ram_percent   = ram.percent
            disco_percent = disco.percent

            # ── Exibição no terminal ─────────────────────────
            limpar_tela()
            print("=" * 60)
            print(f"  🖥️  MONITOR DE HARDWARE  |  {hora_atual()}")
            print("=" * 60)

            # CPU
            status_cpu = "⚠️ ALTO" if cpu_percent >= LIMITE_CPU_PERCENT else "✅ OK"
            print(f"\n  CPU")
            print(f"    Uso:  {barra_progresso(cpu_percent)} {cpu_percent:.1f}%  {status_cpu}")

            # Temperatura
            if temperatura is not None:
                status_temp = "⚠️ ALTA" if temperatura >= LIMITE_TEMP_CPU else "✅ OK"
                print(f"    Temp: {temperatura:.1f}°C  {status_temp}  (limite: {LIMITE_TEMP_CPU}°C)")
            else:
                print(f"    Temp: Não disponível neste sistema")

            # RAM
            ram_usada_gb = ram.used  / (1024 ** 3)
            ram_total_gb = ram.total / (1024 ** 3)
            status_ram = "⚠️ ALTA" if ram_percent >= LIMITE_RAM_PERCENT else "✅ OK"
            print(f"\n  RAM")
            print(f"    Uso:  {barra_progresso(ram_percent)} {ram_percent:.1f}%  {status_ram}")
            print(f"          {ram_usada_gb:.1f} GB usados de {ram_total_gb:.1f} GB")

            # Disco
            disco_usado_gb = disco.used  / (1024 ** 3)
            disco_total_gb = disco.total / (1024 ** 3)
            status_disco = "⚠️ CHEIO" if disco_percent >= LIMITE_DISCO_PERCENT else "✅ OK"
            print(f"\n  DISCO")
            print(f"    Uso:  {barra_progresso(disco_percent)} {disco_percent:.1f}%  {status_disco}")
            print(f"          {disco_usado_gb:.1f} GB usados de {disco_total_gb:.1f} GB")

            print(f"\n  Próxima verificação em {INTERVALO_SEGUNDOS}s... (Ctrl+C para sair)")
            print("=" * 60)

            # ── Verificação de alertas ───────────────────────
            if cpu_percent >= LIMITE_CPU_PERCENT:
                enviar_notificacao(
                    "CPU sobrecarregada!",
                    f"Uso em {cpu_percent:.1f}% (limite: {LIMITE_CPU_PERCENT}%)"
                )

            if temperatura is not None and temperatura >= LIMITE_TEMP_CPU:
                enviar_notificacao(
                    "Temperatura da CPU alta!",
                    f"{temperatura:.1f}°C (limite: {LIMITE_TEMP_CPU}°C)"
                )

            if ram_percent >= LIMITE_RAM_PERCENT:
                enviar_notificacao(
                    "Memória RAM alta!",
                    f"Uso em {ram_percent:.1f}% (limite: {LIMITE_RAM_PERCENT}%)"
                )

            if disco_percent >= LIMITE_DISCO_PERCENT:
                enviar_notificacao(
                    "Disco quase cheio!",
                    f"Uso em {disco_percent:.1f}% (limite: {LIMITE_DISCO_PERCENT}%)"
                )

            time.sleep(INTERVALO_SEGUNDOS)

        except KeyboardInterrupt:
            print("\n\n  Monitor encerrado pelo usuário.")
            salvar_log("Monitor encerrado.")
            break
        except Exception as e:
            print(f"\n  [ERRO] {e}")
            salvar_log(f"ERRO: {e}")
            time.sleep(INTERVALO_SEGUNDOS)


# ─────────────────────────────────────────────
#  Ponto de entrada
# ─────────────────────────────────────────────
if __name__ == "__main__":
    monitorar()
