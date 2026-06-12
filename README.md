# 📊 Monitor de Hardware em Python

Este é um script em Python desenvolvido para monitorar o uso dos componentes de hardware do computador em tempo real. O objetivo é fornecer uma visão clara do consumo de recursos do sistema de forma leve e rápida diretamente pelo terminal ou interface gerada.

---

## 🚀 Funcionalidades

* **Monitoramento de CPU:** Exibe a porcentagem de uso atual de todos os núcleos.
* **Memória RAM:** Mostra o consumo atual, memória disponível e a porcentagem de uso.
* **Armazenamento (Disco):** Verifica o espaço total, utilizado e livre nos discos/SSD.
* **Status do Sistema:** Atualizações contínuas dos dados em tempo real.

---

## 🛠️ Pré-requisitos

Antes de rodar o projeto, você precisará ter o **Python 3.x** instalado na sua máquina. 

Além disso, o projeto utiliza a biblioteca `psutil` para coletar as métricas do sistema. Para instalá-la, abra o terminal e execute o comando abaixo:

```bash
pip install psutil
