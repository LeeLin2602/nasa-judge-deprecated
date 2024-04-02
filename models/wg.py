import subprocess
from pyroute2 import IPRoute
from wgconfig import WGConfig

def run_subprocess(command):
    """Utility function to run subprocess commands with error checking."""
    return subprocess.run(command,
                          shell=True,
                          check=True,
                          stdout=subprocess.PIPE
                          ).stdout.decode().strip()

def generate_wireguard_keys():
    """Generates a WireGuard private and public key pair."""
    private_key = run_subprocess("wg genkey")
    public_key = run_subprocess(f"echo {private_key} | wg pubkey")
    return private_key, public_key

def configure_vrf(ipr, profile_id, wg_interface_name):
    """Configures a VRF for the WireGuard interface."""
    vrf_name = f'vrf_wg{profile_id}'
    ipr.link('add', ifname=vrf_name, kind='vrf', vrf_table=1000 + profile_id)
    vrf_index = ipr.link_lookup(ifname=vrf_name)[0]
    ipr.link('set', index=vrf_index, state='up')

    wg_index = ipr.link_lookup(ifname=wg_interface_name)[0]
    ipr.link('set', index=wg_index, master=vrf_index)

    return vrf_name

def generate_wireguard_config(profile_id):
    """Generates WireGuard configuration for both server and peer."""
    server_private_key, server_public_key = generate_wireguard_keys()
    peer_private_key, peer_public_key = generate_wireguard_keys()

    wg_interface_name = f'wg{profile_id}'
    server_listen_port = str(20000 + profile_id)
    server_interface_ip = '10.64.89.254/24'
    peer_allowed_ips = '10.89.64.0/24, 10.64.89.1/32'

    wg_conf_path = f"/etc/wireguard/{wg_interface_name}.conf"
    wg = WGConfig(wg_conf_path)
    wg.add_attr(None, 'PrivateKey', server_private_key)
    wg.add_attr(None, 'ListenPort', server_listen_port)
    wg.add_attr(None, 'Address', server_interface_ip)
    wg.add_peer(peer_public_key)
    wg.add_attr(peer_public_key, 'AllowedIPs', peer_allowed_ips)
    wg.write_file()

    peer_config = f"""
[Interface]
PrivateKey = {peer_private_key}
Address = 10.64.89.1/32
DNS = 8.8.8.8

[Peer]
PublicKey = {server_public_key}
Endpoint = YOUR_SERVER_IP:{server_listen_port}
AllowedIPs = 10.64.89.0/24
"""

    ipr = IPRoute()
    vrf_name = configure_vrf(ipr, profile_id, wg_interface_name)
    run_subprocess(f"wg-quick up {wg_interface_name}")

    print(vrf_name)
    ipr.close()

    return peer_config
