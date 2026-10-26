import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from qiskit import transpile
from qiskit_aer import AerSimulator

from src.treasure_hunt import LOCATIONS, build_treasure_circuit, run_search


ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)


def main():
    shots = 1024
    rows = []
    experiment = {
        "experiment": "Grover Quantum Treasure Hunt",
        "shots_per_target": shots,
        "simulator": "Qiskit AerSimulator",
        "ideal_success_probability": 1.0,
        "classical_random_guess_probability": 0.25,
        "targets": {},
    }

    for target in LOCATIONS:
        counts = run_search(target, shots=shots)
        success = counts.get(target, 0) / shots

        experiment["targets"][target] = {
            "counts": counts,
            "success_count": counts.get(target, 0),
            "success_probability": success,
        }

        rows.append({
            "target": target,
            "shots": shots,
            "success_count": counts.get(target, 0),
            "success_probability": success,
            "classical_random_guess_probability": 0.25,
        })

        print(
            f"Target {target}: {counts} | "
            f"success={success:.3f} | classical baseline=0.250"
        )

    with (RESULTS / "experiment_results.json").open("w", encoding="utf-8") as f:
        json.dump(experiment, f, indent=2)

    with (RESULTS / "experiment_results.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    # Visualize the results for the target 11.
    target = "11"
    counts = run_search(target, shots=shots)
    labels = list(LOCATIONS)
    values = [counts.get(label, 0) for label in labels]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.xlabel("Measured location")
    plt.ylabel("Number of shots")
    plt.title("Grover Search: Target 11")
    plt.axhline(shots / 4, linestyle="--", label="Uniform baseline")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RESULTS / "grover_histogram.png", dpi=160)
    plt.close()

    # Export the circuit diagram.
    simulator = AerSimulator()
    circuit = transpile(
        build_treasure_circuit(target), simulator
    )
    circuit.draw(
        output="mpl",
        fold=-1,
        filename=str(RESULTS / "grover_circuit.png"),
    )

    print("\nExperiment complete. Saved files:")
    for path in sorted(RESULTS.iterdir()):
        print(f"  {path.name}")


if __name__ == "__main__":
    main()