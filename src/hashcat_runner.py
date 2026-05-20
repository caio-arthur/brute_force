import subprocess
import os
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

HASHCAT_DIR = os.path.join(BASE_DIR, "hashcat-7.1.2")
HASHCAT_BIN = os.path.join(HASHCAT_DIR, "hashcat.exe")

POTFILE_PATH = os.path.join(BASE_DIR, "potfile", "hashcat.potfile")


def build_hashcat_command(hash_file_path: str, mask_file_path: str) -> list:
    return [
        HASHCAT_BIN,
        "-a", "6",
        "-d", "1",
        "-m", "22000",
        "-w", "3",
        "-O",
        "--potfile-path", POTFILE_PATH,
        hash_file_path,
        mask_file_path      
    ]


def run_mask_attack_with_monitoring(
    hash_file_path: str,
    mask_args: list,
    on_cracked_callback,
    already_notified: set,
    check_interval_seconds: int = 15
) -> int:
    cmd = build_hashcat_command(hash_file_path, mask_args)

    print(f"\n[*] Executando em: {HASHCAT_DIR}")
    print(f"[*] Comando: {' '.join(cmd)}")

    process = subprocess.Popen(
        cmd,
        cwd=HASHCAT_DIR
    )

    while process.poll() is None:
        cracked_dict = get_cracked_hashes(hash_file_path)

        for hash_id, password in cracked_dict.items():
            if hash_id not in already_notified:
                on_cracked_callback(hash_id, password)
                already_notified.add(hash_id)

        time.sleep(check_interval_seconds)

    # Verificação final depois que o Hashcat termina
    cracked_dict = get_cracked_hashes(hash_file_path)

    for hash_id, password in cracked_dict.items():
        if hash_id not in already_notified:
            on_cracked_callback(hash_id, password)
            already_notified.add(hash_id)

    return process.returncode


def get_cracked_hashes(hash_file_path: str) -> dict:
    cmd = [
        HASHCAT_BIN,
        "-m", "22000",
        "--potfile-path", POTFILE_PATH,
        "--show",
        hash_file_path
    ]

    result = subprocess.run(
        cmd,
        cwd=HASHCAT_DIR,
        capture_output=True,
        text=True
    )

    cracked = {}

    for line in result.stdout.strip().splitlines():
        if line:
            parts = line.rsplit(":", 1)

            if len(parts) == 2:
                hash_original, password = parts
                cracked[hash_original] = password

    return cracked