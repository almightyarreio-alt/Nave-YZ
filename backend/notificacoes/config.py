import json
from copy import deepcopy
from pathlib import Path


CAMINHO_CONFIG = Path(__file__).with_name("notificacoes.json")

CONFIG_PADRAO = {
    "notifications": {"enabled": True},
    "toast": {"enabled": True},
    "sound": {"enabled": True, "file": "alert.wav"},
    "webhook": {"enabled": True, "url": ""},
}


def _mesclar_configuracao(dados):
    config = deepcopy(CONFIG_PADRAO)
    if isinstance(dados, dict):
        for chave, valor in dados.items():
            if isinstance(valor, dict) and isinstance(config.get(chave), dict):
                config[chave].update(valor)
            else:
                config[chave] = valor
    return config


def carregar_configuracao():
    if not CAMINHO_CONFIG.exists():
        salvar_configuracao(CONFIG_PADRAO)
        return deepcopy(CONFIG_PADRAO)

    with CAMINHO_CONFIG.open("r", encoding="utf-8") as arquivo:
        return _mesclar_configuracao(json.load(arquivo))


def salvar_configuracao(configuracao):
    config = _mesclar_configuracao(configuracao)
    with CAMINHO_CONFIG.open("w", encoding="utf-8") as arquivo:
        json.dump(config, arquivo, ensure_ascii=False, indent=2)
        arquivo.write("\n")
    return config
