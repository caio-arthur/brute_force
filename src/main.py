import os
from hashcat_runner import run_mask_attack_with_monitoring, get_cracked_hashes
from notifier import notify_success


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

COMBINED_HASH_PATH = os.path.join(BASE_DIR, "hashes", "combined.hc22000")
MASK_FILE_PATH = os.path.join(BASE_DIR, "masks", "attack.hcmask")


def main():
    if not os.path.exists(COMBINED_HASH_PATH):
        print(f"Arquivo de hashes não encontrado: {COMBINED_HASH_PATH}")
        return

    if not os.path.exists(MASK_FILE_PATH):
        print(f"Arquivo de máscaras não encontrado: {MASK_FILE_PATH}")
        return

    already_notified = set(get_cracked_hashes(COMBINED_HASH_PATH).keys())

    print("[*] Iniciando ataque em lote com arquivo .hcmask")
    print(f"[*] Hashes: {COMBINED_HASH_PATH}")
    print(f"[*] Máscaras: {MASK_FILE_PATH}")

    return_code = run_mask_attack_with_monitoring(
        hash_file_path=COMBINED_HASH_PATH,
        mask_file_path=MASK_FILE_PATH,
        on_cracked_callback=notify_success,
        already_notified=already_notified
    )

    print(f"\n[*] Processo finalizado com código: {return_code}")


if __name__ == "__main__":
    main()