import pytest

from src.treasure_hunt import (
    LOCATIONS,
    build_treasure_circuit,
    run_search,
)


@pytest.mark.parametrize("target", LOCATIONS)
def test_grover_finds_every_target(target):
    counts = run_search(target, shots=256)

    assert counts == {target: 256}


@pytest.mark.parametrize("target", LOCATIONS)
def test_circuit_has_two_qubits_and_two_classical_bits(target):
    circuit = build_treasure_circuit(target)

    assert circuit.num_qubits == 2
    assert circuit.num_clbits == 2


def test_invalid_target_is_rejected():
    with pytest.raises(ValueError):
        build_treasure_circuit("22")


def test_zero_shots_are_rejected():
    with pytest.raises(ValueError):
        run_search("11", shots=0)


def test_negative_shots_are_rejected():
    with pytest.raises(ValueError):
        run_search("11", shots=-1)