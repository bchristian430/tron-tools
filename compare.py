import requests

# Fetch peer_list0 from the provided URL
def fetch_peer_list0(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            if response.content:  # Check if the response has content
                try:
                    data = response.json()
                    return data.get('peerList', [])
                except requests.exceptions.JSONDecodeError:
                    print("Error: Received a response that is not JSON")
            else:
                print("Error: Received an empty response")
        else:
            print(f"Failed to fetch peer_list0. Status code: {response.status_code}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching peer_list0: {e}")
        return []

# Fetch peer list from a specific peer (host:port)
def fetch_peer_list_from_peer(ip, port):
    try:
        peer_url = f"http://{ip}:{port}/wallet/getnodeinfo"
        response = requests.get(peer_url, timeout=1)
        if response.status_code == 200:
            if response.content:  # Check if the response has content
                try:
                    data = response.json()
                    return data.get('peerList', [])
                except requests.exceptions.JSONDecodeError:
                    print(f"Error: Received a response from {peer_url} that is not JSON")
                    return []
            else:
                print(f"Error: Received an empty response from {peer_url}")
                return []
        else:
            print(f"Failed to fetch peer list from {peer_url}. Status code: {response.status_code}")
            return []
    except requests.exceptions.Timeout:
        print(f"Request to {peer_url} timed out (over 1 second). Moving to next peer.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching peer list from {peer_url}: {e}")
        return []

# Compare peers and find common ones across all peer lists
def find_common_peers(peer_lists):
    if not peer_lists:
        return []

    # Start with the first peer list
    common_peers = set(peer['host'] for peer in peer_lists[0])

    # Compare with other peer lists
    for peer_list in peer_lists[1:]:
        peer_hosts = set(peer['host'] for peer in peer_list)
        common_peers.intersection_update(peer_hosts)

    return list(common_peers)

# Find uncommon peers between two lists
def find_uncommon_peers(peer_list0, common_peers):
    peer_list0_hosts = set(peer['host'] for peer in peer_list0)
    common_peers_set = set(common_peers)

    # Uncommon peers from peer_list0 not in common peers
    uncommon_in_peer_list0 = peer_list0_hosts.difference(common_peers_set)

    # Uncommon peers in common peers not in peer_list0
    uncommon_in_common_peers = common_peers_set.difference(peer_list0_hosts)

    return {
        "uncommon_in_peer_list0": list(uncommon_in_peer_list0),
        "uncommon_in_common_peers": list(uncommon_in_common_peers)
    }

# Main function to orchestrate fetching and comparison
def main():
    base_url = "https://api.trongrid.io/wallet/getnodeinfo"
    
    # Step 1: Fetch peer_list0 from the base URL
    peer_list0 = fetch_peer_list0(base_url)

    print(peer_list0)
    return
    
    # Step 2: Fetch all peer lists from peers in peer_list0
    all_peer_lists = []
    valid_peer_list0 = []  # This will hold only valid peers
    for peer in peer_list0:
        host = peer.get('host', '').lstrip('/')  # Remove leading '/' from the host
        port = peer.get('port', 18888)  # Use the default port 18888 if not specified
        port = 8090
        if host and port:
            print(f"Fetching peer list from {host}:{port}")
            peer_list = fetch_peer_list_from_peer(host, port)
            if peer_list:  # Only include if peer list was fetched successfully
                all_peer_lists.append(peer_list)
                valid_peer_list0.append(peer)  # Only keep valid peers

    # Step 3: Find the common peers from the fetched peer lists (excluding peer_list0)
    common_peers = find_common_peers(all_peer_lists)
    
    # Step 4: Find the uncommon peers between peer_list0 and common peers
    uncommon_peers = find_uncommon_peers(valid_peer_list0, common_peers)
    
    # Output the results
    print("Valid peers in peer_list0:", valid_peer_list0)
    print("Common peers found from all peer lists (excluding peer_list0):", common_peers)
    print("Uncommon peers:", uncommon_peers)

if __name__ == "__main__":
    main()
