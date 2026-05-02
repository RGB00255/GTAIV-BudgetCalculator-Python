#!/usr/bin/env python3
import os
import argparse

CDIMAGE_PATH = os.path.join("pc", "models", "cdimages")
UPDATE_PATH = os.path.join("update", "pc", "models", "cdimages")


def get_size_bytes(path):
    return os.path.getsize(path)


def safe_path(path):
    return path if os.path.isfile(path) else None


def resolve_img(filename):
    base = safe_path(os.path.join(CDIMAGE_PATH, filename))
    update = safe_path(os.path.join(UPDATE_PATH, filename))
    return base, update


def calc_budget(size_bytes, margin):
    return int(size_bytes * (1 + margin / 100))


def bytes_to_mb(b):
    return b / (1024 * 1024)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--veh-margin", type=float, default=20)
    parser.add_argument("--ped-margin", type=float, default=120)  # higher default is more realistic
    args = parser.parse_args()

    veh_base, veh_update = resolve_img("vehicles.img")
    ped_base, ped_update = resolve_img("componentpeds.img")

    veh_total = sum(get_size_bytes(p) for p in [veh_base, veh_update] if p)
    ped_total = sum(get_size_bytes(p) for p in [ped_base, ped_update] if p)

    veh_budget = calc_budget(veh_total, args.veh_margin)
    ped_budget = calc_budget(ped_total, args.ped_margin)

    print("\n===== GTA IV Budget Calculator (BYTE MODE) =====\n")

    print(f"Vehicles: {bytes_to_mb(veh_total):.2f} MB ({veh_total} bytes)")
    print(f"Peds    : {bytes_to_mb(ped_total):.2f} MB ({ped_total} bytes)\n")

    print("RECOMMENDED (for Fusion Fix/RIL.Budgeted):")
    print(f"VehicleBudget = {veh_budget}")
    print(f"PedBudget     = {ped_budget}")


if __name__ == "__main__":
    main()
