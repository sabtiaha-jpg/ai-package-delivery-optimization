---
# Package Delivery Optimization 🚚

**Birzeit University — ENCS3340 Artificial Intelligence, Project #1**
Prepared by: Sabtiah Asad (1221960) & Waed Asad (1220882)
Supervisor: Dr. Samah Alaydi
---

## Overview

This project solves a Vehicle Routing Problem (VRP) for a small delivery shop. Given a set of packages (each with a location, weight, and priority) and a fleet of vehicles (each with a weight capacity), the program finds the most efficient way to assign packages to vehicles and plan routes to minimize total distance traveled.

Two optimization algorithms are implemented:

- **Genetic Algorithm (GA)** — evolves a population of candidate solutions over many generations via crossover and mutation.
- **Simulated Annealing (SA)** — probabilistically accepts worse solutions early on to escape local minima, gradually cooling to refine the result.

---

## Project Structure

```
AI-PROJECT/
├── code.py        # Main program
└── input.txt      # Packages dataset
```

---

## How to Run

**Install dependency:**
```bash
pip install matplotlib
```

**Run:**
```bash
python code.py
```

You'll be prompted to enter the number of vehicles, their capacities, and choose an algorithm (G / S). Enter q to quit.

---

## Input Format

```
# id   x   y   weight   priority
1      4   5   3        1
2      9   8   7        2
```

The shop is always at (0, 0) and is the start/end point for all routes.

---

## Algorithms

| Algorithm           | Key Parameters                              |
|---------------------|---------------------------------------------|
| Genetic Algorithm   | Population: 50, Generations: 300, Mutation: 5% |
| Simulated Annealing | Initial temp: 1000, Cooling: 0.95, Stop: 1  |

---
