import random


class QuantumProtocol:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.tp_honest = True
        self.ctrl_ratio = 0.4
        self.sift_ratio = 0.6
        self.ctrl_count_Alice = 0
        self.sift_count_Alice = 0
        self.ctrl_count_Bob = 0
        self.sift_count_Bob = 0
        self.run_protocol()

    def run_protocol(self):
        while True:
            # Step 1: Initialization
            self.qubits_Alice = [random.choice([0, 1]) for _ in range(self.num_qubits)]
            self.qubits_Bob = [random.choice([0, 1]) for _ in range(self.num_qubits)]

            # Step 2: Random Operations
            self.operations_Alice, self.operations_Bob = self.random_operations()
            print("\nStep 2: Random Operations")
            print("Operations Alice:", self.operations_Alice)
            print("Operations Bob:", self.operations_Bob)

            # Step 3: Checking the Ratio of Operations
            ctrl_count_Alice, sift_count_Alice, ctrl_count_Bob, sift_count_Bob = self.check_ratio()
            print("\nStep 3: Checking the Ratio of Operations")
            print("CTRL Count Alice:", ctrl_count_Alice)
            print("SIFT Count Alice:", sift_count_Alice)
            print("CTRL Count Bob:", ctrl_count_Bob)
            print("SIFT Count Bob:", sift_count_Bob)

            # Check if the ctrl and sift ratios are satisfied
            if ctrl_count_Alice == int(self.ctrl_ratio * self.num_qubits) and \
                    sift_count_Alice == int(self.sift_ratio * self.num_qubits) and \
                    ctrl_count_Bob == int(self.ctrl_ratio * self.num_qubits) and \
                    sift_count_Bob == int(self.sift_ratio * self.num_qubits):
                print("\nCTRL and SIFT ratios are satisfied. Proceeding with the protocol.")
                break  # Exit the loop if the ratios are satisfied
            else:
                print("CTRL and SIFT ratios not satisfied. Re-initializing...")

        # Step 4: SIFT Operations
        if self.sift_operations():
            print("\nStep 4: SIFT Operations")
            print("Alice Qubits before Replacing:", self.qubits_Alice)
            print("Bob Qubits before Replacing  :", self.qubits_Bob)

            # Step 5: Discarding and Replacing Qubits
            self.discard_replace_qubits()
            print("\nStep 5: Discarding and Replacing Qubits")
            print("Updated Qubits Alice:", self.qubits_Alice)
            print("Updated Qubits Bob:  ", self.qubits_Bob)

            # Step 6: Sending Updated Sequences
            updated_sequences_Alice, updated_sequences_Bob = self.send_updated_sequences()
            print("\nStep 6: Sending Updated Sequences")
            print("Updated Sequences Alice:", updated_sequences_Alice)
            print("Updated Sequences Bob:  ", updated_sequences_Bob)

            # Step 7: Bell Measurements
            tp_results = self.bell_measurements()
            print("\nStep 7: Bell Measurements")
            print("Bell Measurement Results:", tp_results)

            # Step 8: Checking for Eavesdropping and TP's Honesty
            selected_indices = random.sample(range(self.num_qubits), self.num_qubits // 2)
            honest_tp = self.check_eavesdropping(selected_indices)
            print("\nStep 8: Checking for Eavesdropping and TP's Honesty")

            # Step 9: Error Rate Threshold
            error_rate = sum([1 for a, b in zip(tp_results, self.operations_Alice) if a != b]) / self.num_qubits
            print("Error Rate:", error_rate)

            # Step 10: Revealing SIFT Operations
            sift_positions = self.reveal_sift_operations()
            print("\nStep 10: Revealing SIFT Operations")
            print("SIFT Positions:", sift_positions)

            # Step 11: Creating Raw Key
            raw_key = self.create_raw_key(sift_positions)
            print("\nStep 11: Creating Raw Key")
            print("Raw Key:", raw_key)

            # Step 13: Obtaining Bob's Key
            bob_key = self.obtain_bob_key(tp_results, sift_positions)
            print("\nStep 13: Obtaining Bob's Key")
            print("Bob's Key:", bob_key)

            if honest_tp and error_rate < 0.1:  # Adjust the error rate threshold as needed
                print("\nProtocol Successful")
            else:
                print("\nProtocol Aborted")
        else:
            print("Protocol Aborted: SIFT ratio not satisfied")

    def random_operations(self):
        return [random.choice(['CTRL', 'SIFT']) for _ in range(self.num_qubits)], [random.choice(['CTRL', 'SIFT']) for _
                                                                                   in range(self.num_qubits)]

    def check_ratio(self):
        ctrl_count_Alice = self.operations_Alice.count('CTRL')
        sift_count_Alice = self.operations_Alice.count('SIFT')
        ctrl_count_Bob = self.operations_Bob.count('CTRL')
        sift_count_Bob = self.operations_Bob.count('SIFT')
        return ctrl_count_Alice, sift_count_Alice, ctrl_count_Bob, sift_count_Bob

    def sift_operations(self):
        ctrl_count_Alice, sift_count_Alice, ctrl_count_Bob, sift_count_Bob = self.check_ratio()
        if (
                ctrl_count_Alice == ctrl_count_Bob == int(self.ctrl_ratio * self.num_qubits)
                and sift_count_Alice == sift_count_Bob == int(self.sift_ratio * self.num_qubits)
        ):
            return True
        return False

    def discard_replace_qubits(self):
        ctrl_count_Alice, _, ctrl_count_Bob, _ = self.check_ratio()  # Use _ for unused values
        indices_to_replace_Alice = random.sample(range(self.num_qubits), ctrl_count_Alice)
        indices_to_replace_Bob = random.sample(range(self.num_qubits), ctrl_count_Bob)
        for idx in indices_to_replace_Alice:
            self.qubits_Alice[idx] = random.choice([0, 1])
        for idx in indices_to_replace_Bob:
            self.qubits_Bob[idx] = random.choice([0, 1])

    def send_updated_sequences(self):
        return self.qubits_Alice, self.qubits_Bob

    def bell_measurements(self):
        results = []
        for i in range(self.num_qubits):
            alice_qubit = self.qubits_Alice[i]
            bob_qubit = self.qubits_Bob[i]
            result = alice_qubit ^ bob_qubit  # XOR operation
            results.append(result)
        return results

    def check_eavesdropping(self, selected_indices):
        selected_results_TP = [self.bell_measurements()[i] for i in selected_indices]
        selected_operations_Alice = [self.operations_Alice[i] for i in selected_indices]
        selected_operations_Bob = [self.operations_Bob[i] for i in selected_indices]

        # Compare results and operations
        if selected_results_TP == selected_operations_Alice and selected_results_TP == selected_operations_Bob:
            return True  # No eavesdropping or dishonest TP
        else:
            return False  # Possible eavesdropping or dishonest TP

    def reveal_sift_operations(self):
        sift_positions = [i for i, op in enumerate(self.operations_Alice) if op == 'SIFT']
        return sift_positions

    # Alice discloses her positions for SIFT operations , and that is used for the raw key bits
    def create_raw_key(self, sift_positions):
        raw_key = [self.qubits_Alice[i] for i in sift_positions]
        return raw_key

    def obtain_bob_key(self, tp_results, sift_positions):
        bob_key = [tp_results[i] if self.qubits_Bob[i] == 0 else 1 - tp_results[i] for i in sift_positions]
        return bob_key


# Instantiate the QuantumProtocol class
num_qubits = 10  # Adjust the number of qubits as needed
protocol = QuantumProtocol(num_qubits)
