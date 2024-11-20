import requests

# Fetch peer_list and machineInfo from the provided URL
def fetch_peer_list_and_machine_info(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if response.content:  # Check if the response has content
                try:
                    data = response.json()
                    peer_list = data.get('peerList', [])
                    machine_info = data.get('machineInfo', {})
                    return peer_list, machine_info
                except requests.exceptions.JSONDecodeError:
                    print(f"Error: Received a response that is not JSON from {url}")
            else:
                print(f"Error: Received an empty response from {url}")
        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return [], {}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return [], {}

# Fetch peer list from a specific peer (host:port)
def fetch_peer_list_from_peer(ip, port):
    try:
        peer_url = f"http://{ip}:{port}/wallet/getnodeinfo"
        response = requests.get(peer_url, timeout=3)
        if response.status_code == 200:
            if response.content:  # Check if the response has content
                try:
                    data = response.json()
                    peer_list = data.get('peerList', [])
                    machine_info = data.get('machineInfo', {})
                    return peer_list, machine_info
                except requests.exceptions.JSONDecodeError:
                    print(f"Error: Received a response from {peer_url} that is not JSON")
                    return [], {}
            else:
                print(f"Error: Received an empty response from {peer_url}")
                return [], {}
        else:
            print(f"Failed to fetch peer list from {peer_url}. Status code: {response.status_code}")
            return [], {}
    except requests.exceptions.Timeout:
        print(f"Request to {peer_url} timed out (over 1 second). Moving to next peer.")
        return [], {}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching peer list from {peer_url}: {e}")
        return [], {}

# Extract the relevant machineInfo fields for comparison
def extract_relevant_machine_info(machine_info):
    return {
        'cpuCount': machine_info.get('cpuCount'),
        'javaVersion': machine_info.get('javaVersion'),
        'osName': machine_info.get('osName'),
        'totalMemory': machine_info.get('totalMemory')
    }

# Find peers with matching cpuCount, javaVersion, osName, totalMemory in peer_list1
def find_peers_with_matching_machine_info(peer_list, target_machine_info):
    matching_peers = []
    for peer in peer_list:
        host = peer.get('host', '').lstrip('/')  # Remove leading '/' from the host
        port = peer.get('port', 18888)  # Default port if not specified
        # Fetch machine info from the peer
        _, peer_machine_info = fetch_peer_list_from_peer(host, 8090)
        peer_relevant_info = extract_relevant_machine_info(peer_machine_info)

        # Compare the relevant fields
        if peer_relevant_info == target_machine_info:
            matching_peers.append(f"{host}:{port}")
    return matching_peers

# Main function
def main():
    original_url = "https://api.trongrid.io/wallet/getnodeinfo"
    
    # Step 1: Fetch peer_list0 and machineInfo from the original link
    peer_list0, original_machine_info = fetch_peer_list_and_machine_info(original_url)
    
    if not peer_list0:
        print("No peers found in peer_list0.")
        return
    
    # Extract the relevant fields from original machineInfo for comparison
    target_machine_info = extract_relevant_machine_info(original_machine_info)
    
    # Step 2: Surf peers in peer_list0 until finding the first working peer
    working_peer_list1 = None
    first_peer_info = None

    for peer in peer_list0:
        host = peer.get('host', '').lstrip('/')  # Remove leading '/' from the host
        port = peer.get('port', 18888)  # Default port if not specified
        print(f"Trying to fetch peer_list1 from {host}:8090")
        peer_list1, peer_machine_info = fetch_peer_list_from_peer(host, 8090)
        
        if peer_list1:  # Stop at the first working link
            working_peer_list1 = peer_list1
            first_peer_info = peer_machine_info
            print(f"Successfully fetched from {host}:{port}. Stopping further requests.")
            break
    
    if not working_peer_list1:
        print("No working peers found in peer_list0.")
        return

    # Step 3: Find peers in peer_list1 with matching machineInfo (cpuCount, javaVersion, osName, totalMemory)
    matching_peers = find_peers_with_matching_machine_info(working_peer_list1, target_machine_info)
    
    # Output the result
    if matching_peers:
        print("Peers in peer_list1 with matching machineInfo:", matching_peers)
    else:
        print("No peers in peer_list1 have matching machineInfo.")

if __name__ == "__main__":
    main()
