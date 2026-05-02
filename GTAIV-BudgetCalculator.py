#!/usr/bin/env python3

# Standard library imports
import os          # used for file path handling and file size checks
import argparse    # used for command-line arguments (flexible tuning of budgets)

# --------------------------------------------
# Default GTA IV directory structure paths
# --------------------------------------------
# These assume the script is run from the GTA IV root folder

CDIMAGE_PATH = os.path.join("pc", "models", "cdimages")  # base game archives
UPDATE_PATH = os.path.join("update", "pc", "models", "cdimages")  # mod/update overrides


# --------------------------------------------
# Get file size in bytes
# --------------------------------------------
def get_size_bytes(path):
    # os.path.getsize returns file size in bytes
    return os.path.getsize(path)


# --------------------------------------------
# Safely check if a file exists
# --------------------------------------------
def safe_path(path):
    # Returns path if it exists, otherwise returns None
    # This prevents crashes when mods/archives are missing
    return path if os.path.isfile(path) else None


# --------------------------------------------
# Resolve archive location (base + update)
# --------------------------------------------
def resolve_img(filename):

    base = safe_path(os.path.join(CDIMAGE_PATH, filename))
    update = safe_path(os.path.join(UPDATE_PATH, filename))

    return base, update


# --------------------------------------------
# Apply safety margin to budget values
# --------------------------------------------
def calc_budget(size_bytes, margin):
    return int(size_bytes * (1 + margin / 100))


# --------------------------------------------
# Convert bytes → MB (for readable output only)
# --------------------------------------------
def bytes_to_mb(b):
    return b / (1024 * 1024)


# --------------------------------------------
# Main execution logic
# --------------------------------------------
def main():

    # Command-line arguments allow users to tune safety margins
    parser = argparse.ArgumentParser()

    # Vehicle memory safety buffer (lower because vehicles are simpler)
    parser.add_argument("--veh-margin", type=float, default=20)

    # Ped memory safety buffer (higher due to variations, clothing, AI, etc.)
    parser.add_argument("--ped-margin", type=float, default=120)

    args = parser.parse_args()

    # --------------------------------------------
    # Locate required GTA IV archive files
    # --------------------------------------------
    veh_base, veh_update = resolve_img("vehicles.img")
    ped_base, ped_update = resolve_img("componentpeds.img")

    # --------------------------------------------
    # Sum file sizes (base + update if present)
    # --------------------------------------------
    veh_total = sum(get_size_bytes(p) for p in [veh_base, veh_update] if p)
    ped_total = sum(get_size_bytes(p) for p in [ped_base, ped_update] if p)

    # --------------------------------------------
    # Calculate recommended budgets (in bytes)
    # --------------------------------------------
    veh_budget = calc_budget(veh_total, args.veh_margin)
    ped_budget = calc_budget(ped_total, args.ped_margin)

    # --------------------------------------------
    # Output results
    # --------------------------------------------
    print("\n===== GTA IV Budget Calculator =====\n")

    # Show both human-readable MB and raw byte values
    print(f"Vehicles: {bytes_to_mb(veh_total):.2f} MB ({veh_total} bytes)")
    print(f"Peds    : {bytes_to_mb(ped_total):.2f} MB ({ped_total} bytes)\n")

    # These values are intended for RIL.Budgeted / Fusion Fix configs
    print("RECOMMENDED (for Fusion Fix/RIL.Budgeted):")
    print(f"VehicleBudget = {veh_budget}")
    print(f"PedBudget     = {ped_budget}")


# --------------------------------------------
# Entry point (prevents auto-run on import)
# --------------------------------------------
if __name__ == "__main__":
    main()