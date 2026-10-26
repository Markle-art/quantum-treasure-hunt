# Quantum Treasure Hunt

**A Qiskit implementation of Grover's quantum search algorithm.**

Quantum Treasure Hunt demonstrates how Grover's algorithm amplifies the probability of finding a marked item in an unstructured search space.

The project uses a two-qubit quantum circuit to search four possible locations: `00`, `01`, `10`, and `11`.

## The problem

Imagine four possible treasure locations, with exactly one containing the treasure. A uniform random guess has a 25% chance of finding the target in one attempt. Grover's algorithm uses quantum superposition, a phase-marking oracle, and amplitude amplification to increase the probability of measuring the target.

## How it works

1. **Superposition:** Hadamard gates prepare an equal superposition of four locations.
2. **Oracle:** A phase operation marks the chosen target without directly measuring it.
3. **Diffusion:** The Grover diffusion operator amplifies the target state's amplitude.
4. **Measurement:** Both qubits are measured to identify the selected location.

For four states with one marked target, one Grover iteration gives a 100% target probability in the ideal mathematical model.

## Features

- Configurable target location.
- Two-qubit Grover search circuit.
- Local simulation using Qiskit Aer.
- Automated tests for all four target locations.
- JSON and CSV experiment results.
- Measurement histogram and circuit diagram.
- Depolarizing-noise experiment.
- Input validation for invalid targets and shot counts.

## Technology

- Python
- Qiskit
- Qiskit Aer
- Matplotlib
- pytest

## Installation

Use Python 3.11 or newer, provided it is compatible with the installed dependencies.

Clone the repository:

```bash
git clone https://github.com/Markle-art/quantum-treasure-hunt.git
cd quantum-treasure-hunt
```

Create a virtual environment and install dependencies.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the interactive treasure hunt:

```powershell
python -m src.treasure_hunt
```

Run the automated tests:

```powershell
python -m pytest -v
```

Run the ideal-simulator experiments:

```powershell
python -m src.run_experiments
```

Run the noisy-simulator experiment:

```powershell
python -m src.noise_experiment
```

## Experiment 1: Ideal simulator

Each target was tested with 1,024 measurement shots.

| Target | Successful measurements | Observed success rate |
|---|---:|---:|
| `00` | 1,024 / 1,024 | 100% |
| `01` | 1,024 / 1,024 | 100% |
| `10` | 1,024 / 1,024 | 100% |
| `11` | 1,024 / 1,024 | 100% |

The results match the expected ideal behaviour of Grover's algorithm for four states and one marked target.

## Experiment 2: Simulated gate noise

The target `11` was tested with 4,096 shots per run.

The depolarizing noise model used a 1% error probability for single-qubit gates (`h` and `x`) and a 2% error probability for the two-qubit gate (`cz`).

| Measurement | Ideal simulator | Noisy simulator |
|---|---:|---:|
| Target detections (`11`) | 4,096 | 3,775 |
| Target success rate | 100.00% | 92.16% |
| Incorrect measurements | 0 | 321 |

The noisy run's observed target success rate was 92.16%, approximately 7.84 percentage points below the ideal result.

This illustrates how simulated gate errors can reduce the reliability of a quantum algorithm. This result is specific to the circuit, noise model, simulator configuration, and random seed. It is not a measurement from physical quantum hardware.

## Classical comparison

A single uniform random guess has a 25% chance of finding the target. A classical search that checks locations in random order takes 2.5 inspections on average and at most four inspections.

This small simulation demonstrates Grover's amplitude amplification, but it does not establish a practical speed advantage over classical computing. Oracle queries are not directly equivalent to total classical operations or circuit gate counts.

## Project structure

- `src/`
  - `__init__.py`
  - `treasure_hunt.py`
  - `run_experiments.py`
  - `noise_experiment.py`
- `tests/test_treasure_hunt.py`
- `results/`
  - `experiment_results.csv`
  - `experiment_results.json`
  - `grover_circuit.png`
  - `grover_histogram.png`
  - `noise_experiment.json`
- `.gitignore`
- `requirements.txt`
- `README.md`

## Limitations and future work

- The results come from local simulation, not physical quantum hardware.
- The search space contains only four states.
- The noisy experiment uses a simplified simulated noise model.
- Future work could explore larger search spaces, multiple marked states, different noise models, and real quantum backends.

## Responsible AI disclosure

AI assistance was used during development to help implement, debug, test, and document the project. The author should verify the implementation, understand the quantum concepts, and accurately disclose the tools and assistance used in the final submission.

## Acknowledgements

Built for the Qiskit Fall Fest Nairobi 2026 Hackathon.

