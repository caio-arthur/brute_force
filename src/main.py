import os
from hashcat_runner import run_mask_attack_with_monitoring, get_cracked_hashes
from notifier import notify_success


def main():
    combined_hash_path = "hashes/combined.hc22000"
    mask_file_path = "masks/attack.hcmask"

    already_notified = set(get_cracked_hashes(combined_hash_path).keys())

    print(f"[*] Iniciando ataque em lote com arquivo .hcmask")
    
    return_code = run_mask_attack_with_monitoring(
        hash_file_path=combined_hash_path,
        mask_args=mask_file_path,
        on_cracked_callback=notify_success,
        already_notified=already_notified
    )

    print(f"\n[*] Processo finalizado com código: {return_code}")

if __name__ == "__main__":
    main()