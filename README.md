# Quantum Mediated Semi-Quantum Key Distribution Protocol Simulator using python

This Python program simulates a mediated semi-quantum key distribution protocol. In this protocol, Alice and Bob use quantum operations to establish a secure communication channel with the help of a  third party (TP).

## Overview

The protocol consists of the following steps:
1. Initialization
2. Random Operations
3. Checking the Ratio of Operations
4. SIFT Operations
5. Discarding and Replacing Qubits
6. Sending Updated Sequences
7. Bell Measurements
8. Checking for Eavesdropping and TP's Honesty
9. Error Rate Threshold
10. Revealing SIFT Operations
11. Creating Raw Key
12. Obtaining Bob's Key

## Usage

To use the program, follow these steps:
1. Install Python on your system if not already installed.
2. Download or clone the repository containing the code.
3. Run the `QuantumProtocol` class with the desired number of qubits.

Example usage:
```python
# Instantiate the QuantumProtocol class
num_qubits = 10  # Adjust the number of qubits as needed
protocol = QuantumProtocol(num_qubits)
```

### Parameters
num_qubits: The number of qubits to be used in the protocol.

### Requirements
Python 3.x

### Disclaimer
This code is a simulation and should not be used for actual secure communication purposes without proper validation and security considerations.



