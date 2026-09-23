"""Which keeper registry the rain deploy registers its upkeep on.

The id was a hardcoded constant, which tied the script to one TestNet app
and made it wrong on every other chain. It now resolves the same way the
keeper bot's does, keeping TestNet's live keeper as that network's default.
"""

import argparse

import pytest

from scripts.rain_testnet_deploy import TESTNET_KEEPER_APP_ID, resolve_keeper_app_id


@pytest.fixture
def parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser()


def test_the_flag_wins(parser, monkeypatch) -> None:
    monkeypatch.setenv("KEEPER_APP_ID", "456")
    assert resolve_keeper_app_id(parser, 123, "localnet") == 123


def test_the_env_is_next(parser, monkeypatch) -> None:
    monkeypatch.setenv("KEEPER_APP_ID", "456")
    assert resolve_keeper_app_id(parser, None, "testnet") == 456


def test_testnet_defaults_to_the_live_keeper(parser, monkeypatch) -> None:
    monkeypatch.delenv("KEEPER_APP_ID", raising=False)
    assert resolve_keeper_app_id(parser, None, "testnet") == TESTNET_KEEPER_APP_ID


@pytest.mark.parametrize("network", ["localnet", "mainnet"])
def test_any_other_network_must_name_one(parser, monkeypatch, network) -> None:
    """A TestNet app id means nothing on another chain, so it is never a guess."""
    monkeypatch.delenv("KEEPER_APP_ID", raising=False)
    with pytest.raises(SystemExit):
        resolve_keeper_app_id(parser, None, network)
