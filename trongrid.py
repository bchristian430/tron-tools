import requests

def get_tron_node_info():
    url = "https://api.trongrid.io/wallet/getnodeinfo"
    
    try:
        # Send a GET request to the API
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Extracting the node list (ip and port)
            if 'peerList' in data:
                nodes = data['peerList']
                ip_port_list = []
                
                # Loop through the nodes and extract IP and Port
                for node in nodes:
                    ip = node.get('host', '')
                    port = node.get('port', '')
                    ip_port_list.append(f"{ip}:{port}")
                
                return ip_port_list
            else:
                print("No nodes found in the response.")
                return []
        else:
            print(f"Failed to fetch node info. Status code: {response.status_code}")
            return []
    
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
        return []

# Call the function and print the list of IP:Port
ip_port_list = get_tron_node_info()
for ip_port in ip_port_list:
    print(ip_port)
