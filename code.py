import math
import random
from typing import List

# === Package and Vehicle Classes ===
class Package:
    def __init__(self, id, x, y, weight, priority):
        self.id = id
        self.x = x
        self.y = y
        self.weight = weight
        self.priority = priority

class Vehicle:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity

# === Distance Calculation Functions ===
def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def get_route_length(route: List[Package], shop_location=(0, 0)):
    distance = 0
    x, y = shop_location
    for pkg in route:
        distance += get_distance(x, y, pkg.x, pkg.y)
        x, y = pkg.x, pkg.y
    distance += get_distance(x, y, shop_location[0], shop_location[1])
    return distance

def get_total_distance(individual, shop_location=(0, 0)):
    return sum(get_route_length(route, shop_location) for route in individual)

# === Load Packages from File ===
def load_packages(filename):
    packages = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                if line.strip() == "" or line.startswith("#"):
                    continue
                parts = line.strip().split()
                if len(parts) == 5:
                    id = int(parts[0])
                    x = float(parts[1])
                    y = float(parts[2])
                    weight = float(parts[3])
                    priority = int(parts[4])
                    packages.append(Package(id, x, y, weight, priority))
    except FileNotFoundError:
        print(f"\n[ERROR] File not found: {filename}")
        exit()
    return packages

# === Ask User for Vehicle Info ===
def get_user_vehicles():
    vehicles = []
    try:
        count = int(input("How many vehicles do you want to use? "))
        for i in range(count):
            cap = float(input(f"Enter capacity for vehicle {i+1}: "))
            vehicles.append(Vehicle(i+1, cap))
    except ValueError:
        print("Invalid input. Please enter numbers.")
        exit()
    return vehicles

# === Genetic Algorithm Functions ===
def make_random_solutions(pop_size, packages, vehicles):
    population = []
    for _ in range(pop_size):
        individual = [[] for _ in vehicles]
        pkgs = sorted(packages, key=lambda p: p.priority)
        for pkg in pkgs:
            for i in range(len(vehicles)):
                if sum(p.weight for p in individual[i]) + pkg.weight <= vehicles[i].capacity:
                    individual[i].append(pkg)
                    break
        population.append(individual)
    return population

def pick_best_two(population, shop_location):
    return sorted(population, key=lambda x: get_total_distance(x, shop_location))[:2]

def mix_parents(p1, p2):
    child = [[] for _ in p1]
    used = set()
    for i in range(len(p1)):
        for pkg in p1[i]:
            if pkg.id not in used:
                child[i].append(pkg)
                used.add(pkg.id)
    for i in range(len(p2)):
        for pkg in p2[i]:
            if pkg.id not in used:
                child[i].append(pkg)
                used.add(pkg.id)
    return child

def random_swap(individual, mutation_rate):
    if random.random() < mutation_rate:
        a, b = random.sample(range(len(individual)), 2)
        if individual[a] and individual[b]:
            pa = random.choice(individual[a])
            pb = random.choice(individual[b])
            individual[a].remove(pa)
            individual[b].remove(pb)
            individual[a].append(pb)
            individual[b].append(pa)

def solve_with_genetic(packages, vehicles, generations=300, pop_size=50, mutation_rate=0.05, shop_location=(0, 0)):
    population = make_random_solutions(pop_size, packages, vehicles)
    best = None
    best_cost = float('inf')
    for _ in range(generations):
        p1, p2 = pick_best_two(population, shop_location)
        child = mix_parents(p1, p2)
        random_swap(child, mutation_rate)
        population.append(child)
        cost = get_total_distance(child, shop_location)
        if cost < best_cost:
            best_cost = cost
            best = child
    return best, best_cost

# === Simulated Annealing Algorithm ===
def solve_with_annealing(packages, vehicles, shop_location=(0, 0), temp=1000, cooling_rate=0.95, stop_temp=1):
    def make_solution():
        solution = [[] for _ in vehicles]
        caps = [v.capacity for v in vehicles]
        pkgs = sorted(packages, key=lambda p: p.priority)
        for pkg in pkgs:
            for i in range(len(vehicles)):
                if caps[i] >= pkg.weight:
                    solution[i].append(pkg)
                    caps[i] -= pkg.weight
                    break
        return solution

    current = make_solution()
    best = current
    current_cost = get_total_distance(current, shop_location)
    best_cost = current_cost

    while temp > stop_temp:
        new = [r[:] for r in current]
        v1, v2 = random.sample(range(len(vehicles)), 2)
        if new[v1] and new[v2]:
            p1 = random.choice(new[v1])
            p2 = random.choice(new[v2])
            new[v1].remove(p1)
            new[v2].remove(p2)
            new[v1].append(p2)
            new[v2].append(p1)

            new_cost = get_total_distance(new, shop_location)
            delta = new_cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / temp):
                current = new
                current_cost = new_cost
                if new_cost < best_cost:
                    best = new
                    best_cost = new_cost
        temp *= cooling_rate
    return best, best_cost

# === Show Output ===
def show_output(vehicles, routes, total, algorithm_name):
    print("\nSuccess! Algorithm details are below:")
    print(f"Algorithm used: {algorithm_name}")
    print("\n----------------------------")
    for i, route in enumerate(routes):
        ids = [pkg.id for pkg in route]
        print(f"Vehicle {vehicles[i].id} delivers packages: {ids}")
        print(f"Route Distance: {round(get_route_length(route), 2)} units")
        print("----------------------------")
    print(f"Total Distance: {round(total, 2)} units\n")

# === Main Program with Loop to Stay Until Exit ===
if __name__ == "__main__":
    shop_location = (0, 0)
    filename = "input.txt"

    packages = load_packages(filename)
    vehicles = get_user_vehicles()

    while True:
        print("\nPackage Delivery Optimization")
        print("Choose algorithm to use:")
        print("G) Genetic Algorithm")
        print("S) Simulated Annealing")
        print("q) Quit")
        print("----------------------------")
        choice = input("Enter G, S or q to quit: ")

        if choice.lower() == "g":
            best_routes, total = solve_with_genetic(packages, vehicles)
            show_output(vehicles, best_routes, total, "Genetic Algorithm")
        elif choice.lower() == "s":
            best_routes, total = solve_with_annealing(packages, vehicles)
            show_output(vehicles, best_routes, total, "Simulated Annealing")
        elif choice.lower() == "q":
            print("Exiting program. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please enter G, S, or q.")
            print("----------------------------")
