import subprocess
from wgconfig import WGConfig
from pyroute2 import IPRoute
import os

# Function to generate WireGuard key pairs
def generate_wireguard_keys():
    private_key = subprocess.check_output("wg genkey", shell=True).decode().strip()
    public_key = subprocess.check_output(f"echo {private_key} | wg pubkey", shell=True).decode().strip()
    return private_key, public_key

def generate_wireguard_config(profile_id):
    # Generate keys for the server and the peer
    server_private_key, server_public_key = generate_wireguard_keys()
    peer_private_key, peer_public_key = generate_wireguard_keys()

    # Server and Peer configuration details
    wg_interface_name = f'wg{profile_id}'
    vrf_name = f'vrf_wg{profile_id}'
    peer_allowed_ips = '10.89.64.0/24, 10.64.89.1/32'  # Example IP for the peer
    server_listen_port = str(20000+profile_id)
    server_interface_ip = '10.64.89.254/24'
    # Create server's WireGuard configuration

    wg_conf_path = f"/etc/wireguard/wg{profile_id}.conf"

    # Create and configure the WireGuard interface
    wg = WGConfig(wg_conf_path)
    wg.add_attr(None, 'PrivateKey', server_private_key)
    wg.add_attr(None, 'ListenPort', server_listen_port)
    wg.add_attr(None, 'Address', server_interface_ip)
    wg.add_peer(peer_public_key)
    wg.add_attr(peer_public_key, 'AllowedIPs', peer_allowed_ips)

    # Write the configuration to file
    wg.write_file()

    # Peer configuration (to be shared with the peer)
    peer_config = f"""
[Interface]
PrivateKey = {peer_private_key}
Address = 10.64.89.1/32
DNS = 8.8.8.8

[Peer]
PublicKey = {server_public_key}
Endpoint = 103.179.29.22:{server_listen_port}
AllowedIPs = 10.64.89.0/24"""



    # Create VRF and assign WireGuard interface to it using pyroute2
    ipr = IPRoute()

    # Create VRF
    ipr.link('add', ifname=vrf_name, kind='vrf', vrf_table=1000 + profile_id)
    # Bring VRF up
    vrf_index = ipr.link_lookup(ifname=vrf_name)[0]
    ipr.link('set', index=vrf_index, state='up')

    # Bring up the WireGuard interface
    subprocess.run(f"wg-quick up {wg_interface_name}", shell=True)

    # Get WireGuard interface index
    wg_index = ipr.link_lookup(ifname=wg_interface_name)[0]

    # Assign WireGuard interface to the VRF
    ipr.link('set', index=wg_index, master=vrf_index)
    print(vrf_name)
    ipr.close()

    return peer_config