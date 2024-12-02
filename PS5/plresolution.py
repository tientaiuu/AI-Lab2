import os
from typing import List, Tuple, Set

class Literal:
    def __init__(self, value: str):
        self.value = value.replace(' ', '')
    
    def __eq__(self, other):
        return self.value == other.value
    
    def __hash__(self):
        return hash(self.value)
    
    def __str__(self):
        return self.value
    
    def get_negation(self) -> 'Literal':
        if self.value.startswith('-'):
            return Literal(self.value[1:])
        return Literal(f'-{self.value}')
    
class Clause:
    def __init__(self, literals: List[Literal]):
        self.literals: Set[Literal] = set(literals)
        self.sort_literals()
    
    def sort_literals(self):
        self.literals = set(sorted(self.literals, key=lambda x: x.value))
    
    @staticmethod
    def myKey(literal: Literal):
        return literal.value[-1]
    
    def __eq__(self, other):
        return self.literals == other.literals
    
    def __hash__(self):
        return hash(frozenset(self.literals))
    
    def __str__(self):
        sorted_literals = sorted(self.literals, key=lambda x: x.value)
        return " OR ".join(str(lit) for lit in sorted_literals)
    
    def is_tautology(self) -> bool:
        for literal in self.literals:
            if literal.get_negation() in self.literals:
                return True
        return False
    
    def resolve_with(self, other: 'Clause') -> List['Clause']:
        resolvents = []
        for lit1 in self.literals:
            for lit2 in other.literals:
                if lit1 == lit2.get_negation():
                    
                    new_literals = list(self.literals - {lit1}) + list(other.literals - {lit2})
                    new_clause = Clause(new_literals)
                    if not new_clause.is_tautology():
                        resolvents.append(new_clause)
        return resolvents


class PLResolutionSolver:
    @staticmethod
    def read_input(file_path: str) -> Tuple[List[Literal], List[Literal], List[Clause]]:
        with open(file_path, 'r') as f:
            lines = [line.strip().replace(' ', '') for line in f.readlines()]
        
        alpha = [Literal(lit) for lit in lines[0].split('OR')]
        n = [Literal(num) for num in lines[1].split('OR')]
        
        KB = [
            Clause([Literal(lit) for lit in line.split('OR')])
            for line in lines[2:]
        ]
        
        return alpha, KB
    
    @staticmethod
    def write_output(data: List[List[Clause]], result: bool, file_name: str):
        with open(file_name, 'w') as f:
            for iteration in data:
                f.write(f"{len(iteration)}\n")
                for clause in iteration:
                    if clause.literals: 
                        f.write(str(clause) + "\n")
            
            if any(not clause.literals for clause_list in data for clause in clause_list):
                f.write("{}\n")
            
            f.write("YES" if result else "NO")
    
    def solve(self, KB: List[Clause], alpha: List[Literal]) -> Tuple[bool, List[List[Clause]]]:
        negated_alpha = [lit.get_negation() for lit in alpha]
        clauses = KB + [Clause([lit]) for lit in negated_alpha]
        
        output = []
        new_clauses = []
        
        while True:
            current_iteration = []
            
            for i, clause1 in enumerate(clauses):
                for clause2 in clauses[i+1:]:
                    resolvents = clause1.resolve_with(clause2)
                    
                    for resolvent in resolvents:
                        if resolvent not in clauses and resolvent not in new_clauses:
                            current_iteration.append(resolvent)
                            new_clauses.append(resolvent)
            
            output.append(current_iteration)
            
            if any(not clause.literals for clause in new_clauses):
                return True, output
            
            if all(resolvent in clauses for resolvent in new_clauses):
                return False, output
            
            clauses.extend(new_clauses)
            new_clauses = []

def main():
    base_folder = 'PS5'
    input_folder = os.path.join(base_folder, 'input')
    output_folder = os.path.join(base_folder, 'output')
    
    os.makedirs(output_folder, exist_ok=True)
    
    solver = PLResolutionSolver()
    
    for i in range(1, 6):
        input_file = os.path.join(input_folder, f'input{i}.txt')
        output_file = os.path.join(output_folder, f'output{i}.txt')
        
        alpha, KB = solver.read_input(input_file)
        result, output = solver.solve(KB, alpha)
        
        solver.write_output(output, result, output_file)
        print(f"Processed input{i}.txt and generated output{i}.txt")

if __name__ == '__main__':
    main()