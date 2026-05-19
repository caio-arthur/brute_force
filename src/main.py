import os
from hashcat_runner import run_mask_attack_with_monitoring, get_cracked_hashes
from notifier import notify_success


def main():
    combined_hash_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "hashes",
            "combined.hc22000"
        )
    )

    if not os.path.exists(combined_hash_path):
        print("Arquivo combined.hc22000 não encontrado. Agrupe seus hashes antes de rodar.")
        return

    with open(combined_hash_path, "r", encoding="utf-8", errors="ignore") as f:
        total_lines = sum(1 for line in f if line.strip())

    print(f"[*] Arquivo carregado: {combined_hash_path}")
    print(f"[*] Linhas encontradas no arquivo: {total_lines}")

    masks_to_run = [
        ["--increment", "--increment-min=8", "--increment-max=10", "?d?d?d?d?d?d?d?d?d?d"],
        ["?h?h?h?h?h?h?h?h"]
    ]

    # Evita notificar hashes que já estavam quebrados antes do script iniciar
    already_notified = set(get_cracked_hashes(combined_hash_path).keys())

    print(f"[*] Hashes já quebrados antes desta execução: {len(already_notified)}")

    for mask in masks_to_run:
        cracked_before = get_cracked_hashes(combined_hash_path)

        if len(cracked_before) >= total_lines:
            print("\n[!] Todos os hashes parecem já estar quebrados. Encerrando algoritmo.")
            break

        return_code = run_mask_attack_with_monitoring(
            hash_file_path=combined_hash_path,
            mask_args=mask,
            on_cracked_callback=notify_success,
            already_notified=already_notified,
            check_interval_seconds=15
        )

        print(f"\n[*] Hashcat finalizou a máscara com código: {return_code}")

    cracked_after = get_cracked_hashes(combined_hash_path)

    print("\n[*] Execução finalizada.")
    print(f"[*] Total de credenciais encontradas: {len(cracked_after)}")


if __name__ == "__main__":
    main()