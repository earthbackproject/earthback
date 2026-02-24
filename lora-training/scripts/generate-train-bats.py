"""
Generate one flux-lora-train-[char].bat per character.
Run once to create all 12 bat files in lora-training/.

Usage: python generate-train-bats.py
"""

import shutil
from pathlib import Path

BASE  = Path(r"C:\users\adrxi\Earthback\lora-training")
KOHYA = Path(r"D:\AI\kohya_ss")   # ← adjust if Kohya SS installed elsewhere
VENV  = KOHYA / "venv" / "Scripts" / "python.exe"

CHARS = [
    "james-osei",
    "lena-hartmann",
    "tom-westhall",
    "rosa-mendez",
    "mei-lin",
    "elena-vasquez",
    "amara-diallo",
    "marcus-webb",
    "kenji-nakamura",
    "priya-sharma",
    "dara-okonkwo",
    "sam-torres",
]

TOML_TEMPLATE = BASE / "configs" / "flux-lora-base.toml"
OUT_DIR        = BASE / "configs"

for slug in CHARS:
    # Write per-character TOML
    toml_src  = TOML_TEMPLATE.read_text(encoding="utf-8")
    toml_out  = toml_src.replace("CHAR_SLUG", slug)
    toml_path = OUT_DIR / f"flux-lora-{slug}.toml"
    toml_path.write_text(toml_out, encoding="utf-8")

    # Write launcher bat
    bat_content = f"""@echo off
echo Training LoRA for: {slug}
echo Config: {toml_path}
echo Output: {BASE / "output"}
echo.
{VENV} "{KOHYA / 'flux_train_network.py'}" --config_file "{toml_path}"
echo.
echo Done! Check {BASE / "output" / (slug + "-v1.safetensors")}
pause
"""
    bat_path = BASE / f"train-{slug}.bat"
    bat_path.write_text(bat_content, encoding="utf-8")
    print(f"  Created: train-{slug}.bat + configs/flux-lora-{slug}.toml")

print(f"\nAll {len(CHARS)} character configs generated.")
print("Run train-james-osei.bat to start first character.")
