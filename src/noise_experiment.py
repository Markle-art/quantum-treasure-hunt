import json
from pathlib import Path

from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

from src.treasure_hunt import build_treasure_circuit


ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def main():
    target = "11"
    shots = 4096

    circuit = build_treasure_circuit(target)

    ideal_simulator = AerSimulator()
    ideal_circuit = transpile(circuit, ideal_simulator, seed_transpiler=42)
    ideal_counts = ideal_simulator.run(
        ideal_circuit, shots=shots, seed_simulator=42
    ).result().get_counts()

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(0.01, 1), ["h", "x"]
    )
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(0.02, 2), ["cz"]
    )

    noisy_simulator = AerSimulator(noise_model=noise_model)
    noisy_circuit = transpile(circuit, noisy_simulator, seed_transpiler=42)
    noisy_counts = noisy_simulator.run(
        noisy_circuit, shots=shots, seed_simulator=42
    ).result().get_counts()

    report = {
        "target": target,
        "shots": shots,
        "noise_model": {
            "type": "depolarizing",
            "single_qubit_error_probability": 0.01,
            "two_qubit_error_probability": 0.02,
            "applies_to": ["h", "x", "cz"],
        },
        "ideal": {
            "counts": ideal_counts,
            "success_probability": ideal_counts.get(target, 0) / shots,
        },
        "noisy": {
            "counts": noisy_counts,
            "success_probability": noisy_counts.get(target, 0) / shots,
        },
    }

    output = RESULTS / "noise_experiment.json"
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Target: {target}")
    print(f"Shots per run: {shots}")
    print(f"Ideal counts: {ideal_counts}")
    print(f"Noisy counts: {noisy_counts}")
    print(
        "Ideal success: "
        f"{report['ideal']['success_probability']:.2%}"
    )
    print(
        "Noisy success: "
        f"{report['noisy']['success_probability']:.2%}"
    )
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()