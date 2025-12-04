import sys
import math
import argparse

class SATBuilder:
    """Helper class to build SAT formulas using Tseitin transformation."""
    
    def __init__(self):
        self.num_vars = 0
        self.clauses = []  
        self.var_names = {} 
    
    def new_var(self, name=None):
        """Allocates a new boolean variable."""
        self.num_vars += 1
        if name:
            self.var_names[self.num_vars] = name
        return self.num_vars
    
    def add_clause(self, literals):
        """Adds a clause to the formula. Ignores tautologies/false literals."""
        clean = []
        for lit in literals:
            if lit is True:
                return 
            if lit is False:
                continue
            clean.append(lit)
        
        if not clean:
            # Empty clause implies contradiction (False)
            if self.num_vars == 0:
                self.new_var("contradiction")
            self.clauses.append([1])
            self.clauses.append([-1])
            return
        self.clauses.append(clean)
    
    def const_true(self):
        return True
    
    def const_false(self):
        return False
    
    # === Logic Gates (Tseitin Transformation) ===
    
    def gate_not(self, a):
        """Returns variable equivalent to NOT a."""
        if a is True: return False
        if a is False: return True
        out = self.new_var()
        # CNF: (out v a) ^ (-out v -a)
        self.add_clause([out, a])
        self.add_clause([-out, -a])
        return out
    
    def gate_and(self, a, b):
        """Returns variable equivalent to (a AND b)."""
        if a is False or b is False: return False
        if a is True: return b
        if b is True: return a
        out = self.new_var()
        # CNF: (-out v a) ^ (-out v b) ^ (out v -a v -b)
        self.add_clause([-out, a])
        self.add_clause([-out, b])
        self.add_clause([out, -a, -b])
        return out
    
    def gate_or(self, a, b):
        """Returns variable equivalent to (a OR b)."""
        if a is True or b is True: return True
        if a is False: return b
        if b is False: return a
        out = self.new_var()
        # CNF: (out v -a) ^ (out v -b) ^ (-out v a v b)
        self.add_clause([out, -a])
        self.add_clause([out, -b])
        self.add_clause([-out, a, b])
        return out
    
    def gate_xor(self, a, b):
        """Returns variable equivalent to (a XOR b)."""
        if a is False: return b
        if b is False: return a
        if a is True: return self.gate_not(b)
        if b is True: return self.gate_not(a)
        out = self.new_var()
        # CNF: (-out v -a v -b) ^ (-out v a v b) ^ (out v -a v b) ^ (out v a v -b)
        self.add_clause([-out, -a, -b])
        self.add_clause([-out, a, b])
        self.add_clause([out, -a, b])
        self.add_clause([out, a, -b])
        return out
    
    # === Arithmetic Circuits ===
    
    def half_adder(self, a, b):
        """Computes sum and carry for 2 bits."""
        s = self.gate_xor(a, b)
        c = self.gate_and(a, b)
        return s, c
    
    def full_adder(self, a, b, cin):
        """Computes sum and carry for 3 bits (a, b, carry_in)."""
        # Sum = a XOR b XOR cin
        # Cout = (a AND b) OR (cin AND (a XOR b))
        axb = self.gate_xor(a, b)
        s = self.gate_xor(axb, cin)
        cout = self.gate_or(self.gate_and(a, b), self.gate_and(cin, axb))
        return s, cout
    
    def add_binary_numbers(self, bits_a, bits_b, num_bits):
        """Adds two L-bit binary numbers (LSB first). Returns L-bit sum and final carry."""
        # Pad inputs
        while len(bits_a) < num_bits: bits_a.append(False)
        while len(bits_b) < num_bits: bits_b.append(False)
        
        result = []
        carry = False
        for i in range(num_bits):
            s, carry = self.full_adder(bits_a[i], bits_b[i], carry)
            result.append(s)
        return result, carry
    
    def multiply_by_constant(self, x_var, constant, num_bits):
        """Returns binary representation of (x_var * constant)."""
        result = []
        for bit_pos in range(num_bits):
            bit_val = (constant >> bit_pos) & 1
            # If bit is 1, result depends on x_var. If 0, it's always 0.
            result.append(x_var if bit_val == 1 else False)
        return result
    
    def sum_weighted_vars(self, weights, x_vars, num_bits):
        """
        Sums a list of weighted boolean variables: sum(weights[i] * x_vars[i]).
        Uses a tree reduction of binary adders.
        """
        n = len(weights)
        if n == 0:
            return [False] * num_bits, False
        
        # Leaf nodes: multiply each x variable by its weight
        addends = []
        for i in range(n):
            bits = self.multiply_by_constant(x_vars[i], weights[i], num_bits)
            addends.append(bits)
        
        # Reduction tree: pair up addends and sum them
        while len(addends) > 1:
            new_addends = []
            for i in range(0, len(addends), 2):
                if i + 1 < len(addends):
                    sum_bits, _ = self.add_binary_numbers(addends[i], addends[i+1], num_bits)
                    new_addends.append(sum_bits)
                else:
                    new_addends.append(addends[i])
            addends = new_addends
        
        return addends[0], False 
    
    def compare_le(self, bits_a, const_b, num_bits):
        """
        Returns variable True if bits_a <= const_b.
        Implements recursive digital comparator from MSB to LSB.
        """
        le = True  # Base case: empty prefix is equal
        for i in range(num_bits - 1, -1, -1):
            a_bit = bits_a[i]
            b_bit = (const_b >> i) & 1
            
            if b_bit == 1:
                # If b=1, a <= b is True if a=0, else checks lower bits
                # le_new = (NOT a) OR (a AND le_prev)
                if a_bit is False:
                    le = True
                elif a_bit is True:
                    # le remains same
                    pass
                else:
                    # Logic simplification: (NOT a) OR le
                    if le is True: 
                        pass # le remains True
                    elif le is False:
                        le = self.gate_not(a_bit)
                    else:
                        le = self.gate_or(self.gate_not(a_bit), le)
            else:
                # If b=0, a <= b is only possible if a=0 AND check lower bits
                # le_new = (NOT a) AND le_prev
                if a_bit is False:
                    # le remains same
                    pass
                elif a_bit is True:
                    le = False
                else:
                    if le is True:
                        le = self.gate_not(a_bit)
                    elif le is False:
                        pass # le remains False
                    else:
                        le = self.gate_and(self.gate_not(a_bit), le)
        return le
    
    def assert_true(self, var):
        """Adds a unit clause forcing var to be True."""
        if var is True: return
        if var is False:
            if self.num_vars == 0: self.new_var()
            self.add_clause([1]); self.add_clause([-1]) # Contradiction
            return
        self.add_clause([var])
    
    def to_3sat(self):
        """Converts arbitrary clauses to 3-CNF (max 3 literals per clause)."""
        final_clauses = []
        for clause in self.clauses:
            if len(clause) <= 3:
                # Pad small clauses: (A v B) -> (A v B v B)
                c = list(clause)
                while len(c) < 3: c.append(c[-1])
                final_clauses.append(c)
            else:
                # Break large clauses using auxiliary variables
                # (L1 v L2 v L3 v ... v Ln) -> (L1 v L2 v z1) ^ (-z1 v L3 v z2) ...
                curr = clause
                while len(curr) > 3:
                    self.num_vars += 1
                    z = self.num_vars
                    final_clauses.append([curr[0], curr[1], z])
                    curr = [-z] + curr[2:]
                while len(curr) < 3: curr.append(curr[-1])
                final_clauses.append(curr)
        return final_clauses

def solve():
    parser = argparse.ArgumentParser(description='Bin Packing to MAX-3-SAT Reduction')
    parser.add_argument('input_file')
    parser.add_argument('capacity', type=int)
    parser.add_argument('num_bins', nargs='?', type=int)
    
    args = parser.parse_args()
    
    try:
        with open(args.input_file, 'r') as f:
            content = f.read()
            sizes = [int(x) for x in content.split()]
    except FileNotFoundError:
        print(f"Error: File {args.input_file} not found.")
        sys.exit(1)
    except ValueError:
        print("Error: Input file must contain only integers.")
        sys.exit(1)

    if not sizes:
        return

    n_items = len(sizes)
    C = args.capacity
    
    # Determine number of bins to solve for
    if args.num_bins is not None:
        m_bins = args.num_bins
        print(f"Using specified number of bins: {m_bins}")
    else:
        # Calculate Lower Bound (Initial Guess)
        if C > 0:
            m_bins = math.ceil(sum(sizes) / C)
        else:
            m_bins = n_items
        print(f"Using calculated lower bound bins: {m_bins}")
        
    # Calculate bits needed for capacity representation
    L = max(1, math.ceil(math.log2(C + 1))) if C > 0 else 1
    max_sum = sum(sizes)
    L = max(L, math.ceil(math.log2(max_sum + 1)) if max_sum > 0 else 1)

    sat = SATBuilder()
    
    # 1. Assignment Variables: x[i][j]
    x_vars = {}
    for i in range(n_items):
        for j in range(m_bins):
            x_vars[(i, j)] = sat.new_var(f"x_{i}_{j}")
    
    # 2. Constraint: Each item must be in at least one bin
    for i in range(n_items):
        sat.add_clause([x_vars[(i, j)] for j in range(m_bins)])
    
    # 3. Constraint: Each item must be in at most one bin
    for i in range(n_items):
        for j1 in range(m_bins):
            for j2 in range(j1 + 1, m_bins):
                sat.add_clause([-x_vars[(i, j1)], -x_vars[(i, j2)]])

    # 4. Constraint: Bin Capacity (Adder Circuit + Comparator)
    for j in range(m_bins):
        # Variables for items currently considered for this bin
        bin_x_vars = [x_vars[(i, j)] for i in range(n_items)]
        
        # Adder Tree: Calculate sum of sizes for items in this bin
        sum_bits, _ = sat.sum_weighted_vars(sizes, bin_x_vars, L)
        
        # Comparator: Assert sum <= Capacity
        le_var = sat.compare_le(sum_bits, C, L)
        sat.assert_true(le_var)
    
    # 5. Output 3-SAT Instance
    final_clauses = sat.to_3sat()
    
    output_file = "sat_output.txt"
    with open(output_file, 'w') as f:
        f.write(f"{sat.num_vars} {len(final_clauses)}\n")
        for c in final_clauses:
            f.write(f"{c[0]} {c[1]} {c[2]}\n")

if __name__ == "__main__":
    solve()