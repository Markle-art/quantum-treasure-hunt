from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

LOCATIONS = ("00", "01", "10", "11")


def build_treasure_circuit(target: str) -> QuantumCircuit:
    """Build a two-qubit Grover search circuit."""
    if target not in LOCATIONS:
        raise ValueError(f"Target must be one of {LOCATIONS}")

    circuit = QuantumCircuit(2, 2)

    # Step 1: Put both qubits into equal superposition.
    circuit.h([0, 1])

    # Step 2: Oracle marks the selected target.
    zero_bits = [i for i, bit in enumerate(target[::-1]) if bit == "0"]
    for qubit in zero_bits:
        circuit.x(qubit)

    circuit.cz(0, 1)

    for qubit in zero_bits:
        circuit.x(qubit)

    # Step 3: Grover diffusion operator.
    circuit.h([0, 1])
    circuit.x([0, 1])
    circuit.cz(0, 1)
    circuit.x([0, 1])
    circuit.h([0, 1])

    # Step 4: Measure both qubits.
    circuit.measure([0, 1], [0, 1])

    return circuit


def run_search(target: str, shots: int = 1024) -> dict[str, int]:
    if shots < 1:
        raise ValueError("shots must be at least 1")

    simulator = AerSimulator()
    compiled = transpile(build_treasure_circuit(target), simulator)
    result = simulator.run(compiled, shots=shots, seed_simulator=42).result()

    return result.get_counts()


if __name__ == "__main__":
    print("===================================")
    print("      QUANTUM TREASURE HUNT")
    print("===================================")
    print("Choose a hidden treasure location:")
    for index, location in enumerate(LOCATIONS, start=1):
        print(f"  {index}. {location}")

    choice = input("\nEnter location (00, 01, 10, or 11): ").strip()

    if choice not in LOCATIONS:
        print("Invalid location. Please choose 00, 01, 10, or 11.")
        raise SystemExit(1)

    shots_input = input("Number of shots [1024]: ").strip()
    shots = int(shots_input) if shots_input else 1024

    if shots < 1:
        print("Shots must be at least 1.")
        raise SystemExit(1)

    counts = run_search(choice, shots)

    print(f"\nHidden treasure: {choice}")
    print("Measurement counts:")
    for location, count in sorted(counts.items()):
        print(f"  {location}: {count}")

    successes = counts.get(choice, 0)
    print(f"\nTarget detections: {successes}/{shots}")
    print(f"Observed success rate: {successes / shots:.2%}")

    print("\nSEARCH COMPARISON")
    print("Classical random-order search:")
    print("  Average inspections for 4 locations: 2.5")
    print("  Worst case: 4 inspections")
    print("Grover search:")
    print("  Oracle queries in this circuit: 1")
    print("  Ideal target probability: 100%")
    print("\nNote: oracle queries are not directly equivalent")
    print("to total classical operations or circuit gate counts.")