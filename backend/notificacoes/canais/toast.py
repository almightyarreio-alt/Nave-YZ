import subprocess
import sys


CANAL = "toast"


class Toast:
    def __init__(self, config):
        self.config = config

    def enviar(self, evento):
        if sys.platform != "win32":
            return {"mensagem": "Toast Windows indisponivel fora do Windows"}

        titulo = evento.titulo.replace("'", "''")
        mensagem = evento.mensagem.replace("'", "''")
        script = (
            "[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null;"
            "$template = [Windows.UI.Notifications.ToastTemplateType]::ToastText02;"
            "$xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($template);"
            "$textNodes = $xml.GetElementsByTagName('text');"
            f"$textNodes.Item(0).AppendChild($xml.CreateTextNode('{titulo}')) | Out-Null;"
            f"$textNodes.Item(1).AppendChild($xml.CreateTextNode('{mensagem}')) | Out-Null;"
            "$toast = [Windows.UI.Notifications.ToastNotification]::new($xml);"
            "[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier('Nave YZ').Show($toast);"
        )
        subprocess.Popen(["powershell", "-NoProfile", "-Command", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"mensagem": "Toast solicitado"}


def criar_canal(config):
    return Toast(config)
