import requests


def notify_success(hash_id: str, password: str):
    """
    Envia notificação via HTTP para o ntfy.sh.
    """
    url = "https://ntfy.sh/localghost"

    mensagem = f"Hash quebrado!\n\nHash: {hash_id}\nSenha: {password}"

    try:
        response = requests.post(
            url,
            data=mensagem.encode("utf-8"),
            headers={
                "Title": "[CRACKED!]",
                "Priority": "urgent",
                "Tags": "skull"
            },
            timeout=10
        )

        if response.status_code == 200:
            print(f"\n[CRACKED!] Notificação enviada via ntfy! Senha: {password}\n")
        else:
            print(f"\n[ERRO] Falha ao enviar notificação HTTP. Status code: {response.status_code}\n")

    except requests.exceptions.RequestException as e:
        print(f"\n[ERRO] Exceção ao tentar conectar com ntfy.sh: {e}\n")