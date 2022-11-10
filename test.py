import numpy as np
from qiskit import Aer
from qiskit.visualization import plot_histogram
from qiskit.utils import QuantumInstance
from qiskit.algorithms import Grover, AmplificationProblem
from qiskit.circuit.library import PhaseOracle
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute,IBMQ
import math
import time
from qiskit.tools.monitor import job_monitor

with open('3sat.dimacs', 'r') as f:
    dimacs = f.read()
print(dimacs)
oracle = PhaseOracle.from_dimacs_file('3sat.dimacs')
print(oracle.draw())

def gateCreation():
        time.sleep(10)
        pi = math.pi
        q = QuantumRegister(20,'q')
        c = ClassicalRegister(20,'c')
        qc = QuantumCircuit(q,c)

        print('\nInitialising Circuit...\n')

        ### Initialisation ###

        qc.h(q[0])
        qc.h(q[1])
        qc.h(q[2])
        qc.h(q[3])
        for i in range (4,20):
            qc.h(q[i])
            qc.cp(pi/4, q[i-1], q[i])
            qc.cx(q[i-1], q[i])
            qc.cp(-pi/4, q[i-1], q[i])
            qc.cx(q[i-1], q[i])
            qc.cp(pi/4, q[i-1], q[i])
            qc.cx(q[i-1], q[i])
            qc.cp(-pi/4, q[i-1], q[i])
            qc.cx(q[i-1], q[i])
            qc.cp(pi/4, q[i-1], q[i])
            qc.cx(q[i], q[i-1])
            qc.cp(-pi/4, q[i-1], q[i])
            qc.cx(q[i-1], q[i])
            qc.cp(pi/4, q[i-1], q[i])
            
        print('\nPreparing Oracle circuit.... for 0000\n')

        ### 0000 Oracle ###

        ### 0001 Oracle ###

        qc.x(q[1])
        qc.x(q[2])
        qc.x(q[3])

        qc.cp(pi/4, q[0], q[3])
        qc.cx(q[0], q[1])
        qc.cp(-pi/4, q[1], q[3])
        qc.cx(q[0], q[1])
        qc.cp(pi/4, q[1], q[3])
        qc.cx(q[1], q[2])
        qc.cp(-pi/4, q[2], q[3])
        qc.cx(q[0], q[2])
        qc.cp(pi/4, q[2], q[3])
        qc.cx(q[1], q[2])
        qc.cp(-pi/4, q[2], q[3])
        qc.cx(q[0], q[2])
        qc.cp(pi/4, q[2], q[3])

        qc.x(q[1])
        qc.x(q[2])
        qc.x(q[3])

        print(qc.draw())

        time.sleep(100000)

class Verifier():
    """Create an object that can be used to check whether
    an assignment satisfies a DIMACS file.
        Args:
            dimacs_file (str): path to the DIMACS file
    """
    def __init__(self, dimacs_file):
        with open(dimacs_file, 'r') as f:
            self.dimacs = f.read()

    def is_correct(self, guess):
        """Verifies a SAT solution against this object's
        DIMACS file.
            Args:
                guess (str): Assignment to be verified.
                             Must be string of 1s and 0s.
            Returns:
                bool: True if `guess` satisfies the
                           problem. False otherwise.
        """
        # Convert characters to bools & reverse
        guess = [bool(int(x)) for x in guess][::-1]
        for line in self.dimacs.split('\n'):
            line = line.strip(' 0')
            clause_eval = False
            for literal in line.split(' '):
                if literal in ['p', 'c']:
                    # line is not a clause
                    clause_eval = True
                    break
                if '-' in literal:
                    literal = literal.strip('-')
                    lit_eval = not guess[int(literal)-1]
                else:
                    lit_eval = guess[int(literal)-1]
                clause_eval |= lit_eval
            if clause_eval is False:
                return False
        return True
gateCreation()
v = Verifier('3sat.dimacs')   
v.is_correct('001')
# Configure backend
backend = Aer.get_backend('aer_simulator')
quantum_instance = QuantumInstance(backend, shots=1024)

# Create a new problem from the phase oracle and the
# verification function
problem = AmplificationProblem(oracle=oracle, is_good_state=v.is_correct)

# Use Grover's algorithm to solve the problem
grover = Grover(quantum_instance=quantum_instance)
result = grover.amplify(problem)
result.top_measurement
plot_histogram(result.circuit_results).savefig('histogram.png')