from pathlib import Path

BIN = Path("/app/bin/netplay_matrix")
CONFIG = Path("/app/config/sim_defaults.yaml")
BUILD_CACHE = Path("/app/build/CMakeCache.txt")
TARGET_CACHE = Path("/app/target/cache.bin")


def test_contract_paths():
    assert BIN.is_absolute()
    assert CONFIG.is_absolute()
    assert BUILD_CACHE.is_absolute()
    assert TARGET_CACHE.is_absolute()
