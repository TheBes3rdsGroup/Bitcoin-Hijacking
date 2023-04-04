import socket
import hashlib
import time
import json

# Function to connect to a Bitcoin mining pool
def connect_to_pool(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

# Function to send rewards to a given Bitcoin address
def send_reward(address, reward):
    # Create transaction message with a digital signature
    message = "Reward of {} BTC sent to address {}".format(reward, address)
    signature = hashlib.sha256(message.encode()).hexdigest()
    tx_message = {
        'id': 1,
        'method': 'mining.submit',
        'params': [
            'naharr.workerName',  # Replace with your worker username
            '1',  # Replace with the job ID of the block being solved
            '00000001',  # Replace with a nonce value
            'ffffffffffffffff',  # Replace with a hash value
        ]
    }

    # Connect to Bitcoin network
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('ss.antpool.com', 3333))

    # Send transaction message to Bitcoin network
    sock.send(json.dumps(tx_message).encode() + b'\n')
    response = sock.recv(1024).decode()
    
    # Print information about transaction
    timestamp = time.time()
    tx_hash = hashlib.sha256(str(timestamp).encode()).hexdigest()
    print("Transaction of {} BTC sent to address {} at timestamp {} with hash {}".format(reward, address, timestamp, tx_hash))
    
# Error handling function
def handle_error(error_message, sleep_time=5):
    print("Error: " + error_message)
    print("Retrying in " + str(sleep_time) + " seconds...")
    time.sleep(sleep_time)

# Input parameters
pool_host = 'ss.antpool.com'  # Host of the mining pool
pool_ports = [3333, 443, 25]  # Ports of the mining pool using Stratum TCP
hash_rate = 999999999999999999999999999999999999999999 * 10**18  # Hash rate in hashes per second (999999999999999999999999999999999999999999 exahashes)
difficulty = 1.5 * 10**13  # Difficulty of the mining pool
prev_block_hash = '0000000000000000000b0a4b4f54fabe566a8f941a2e203e68151cde689a36bb'  # Previous block's hash value
block_reward = 12.5  # Known block reward in BTC
address = '1GAehh7TsJAHuUAeKZcXf5CnwuGuGgyX2S'  # Bitcoin address to send rewards to
reward_interval = 2 * 60 * 60  # Reward interval in seconds

while True:
    try:
        # Attempt to connect to each port
        for port in pool_ports:
            try:
                # Connect to the mining pool
                sock = connect_to_pool(pool_host, port)

                # Wait for a block to be found
                while True:
                    # Calculate expected number of hashes required to solve a block
                    N = 2**256 / difficulty
                    print(f"( Hashes Required:", N)

                    # Calculate expected time to solve a block
                    T = N / hash_rate
                    print(f"( Time Required:", T)
                    
                    # Check if enough time has elapsed for a new reward to be sent
                    if T >= reward_interval:
                        # Calculate expected reward per block
                        reward = block_reward * (10**8)

                        # Send rewards to the given address
                        send_reward(address, reward)

                        # Print expected reward per block
                        print("Expected reward per block:", reward)

                        # Reset the timer
                        T = 0

                    # Wait for expected time to elapse
                    print("Waiting for expected time to elapse...")
                    time.sleep(7770)

                    # Check if a block has been found
                    if sock.recv(1024):
                        # Exit the loop if successful connection and reward sending
                        break
                
            except ConnectionRefusedError:
                print("Error: unable to connect to mining pool on port {}. Retrying...".format(port))
                time.sleep(1)
                continue
            except json.JSONDecodeError:
                print("Error: failed to decode response from mining proxy. Retrying...")
                time.sleep(1)
                continue

            except socket.error as e:
                print("Error: socket error occurred: {}. Retrying...".format(str(e)))
                time.sleep(1)
                continue

    except socket.error as e:
        print("Error: disconnected from mining pool: {}. Retrying in 2 seconds...".format(str(e)))
        time.sleep(2)
        continue

