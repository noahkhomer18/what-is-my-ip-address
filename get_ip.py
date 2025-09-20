#!/usr/bin/env python3
"""
What is My IP Address - Python Tool
A simple command-line tool to display your public IP address.
"""

import requests
import sys
import json
from typing import Optional


def get_public_ip() -> Optional[str]:
    """
    Fetch the public IP address using multiple services for reliability.
    
    Returns:
        str: The public IP address, or None if unable to fetch
    """
    # List of IP services to try (in order of preference)
    ip_services = [
        'https://api.ipify.org',
        'https://ipinfo.io/ip',
        'https://icanhazip.com',
        'https://ident.me',
        'https://checkip.amazonaws.com'
    ]
    
    for service in ip_services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                ip = response.text.strip()
                # Basic validation - check if it looks like an IP address
                if '.' in ip and len(ip.split('.')) == 4:
                    return ip
        except (requests.RequestException, requests.Timeout):
            continue
    
    return None


def get_ip_details(ip: str) -> dict:
    """
    Get additional details about the IP address.
    
    Args:
        ip (str): The IP address
        
    Returns:
        dict: Dictionary containing IP details
    """
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json', timeout=5)
        if response.status_code == 200:
            return response.json()
    except (requests.RequestException, requests.Timeout):
        pass
    
    return {}


def main():
    """Main function to display IP address information."""
    print("🌐 What is My IP Address")
    print("=" * 30)
    
    # Get public IP
    print("Fetching your public IP address...")
    ip = get_public_ip()
    
    if not ip:
        print("❌ Error: Unable to fetch your IP address.")
        print("Please check your internet connection and try again.")
        sys.exit(1)
    
    print(f"📍 Your public IP address: {ip}")
    
    # Get additional details
    print("\nFetching additional details...")
    details = get_ip_details(ip)
    
    if details:
        print("\n📋 IP Details:")
        print("-" * 20)
        
        if 'city' in details and 'region' in details and 'country' in details:
            location = f"{details['city']}, {details['region']}, {details['country']}"
            print(f"📍 Location: {location}")
        
        if 'org' in details:
            print(f"🏢 ISP/Organization: {details['org']}")
        
        if 'timezone' in details:
            print(f"🕐 Timezone: {details['timezone']}")
        
        if 'hostname' in details:
            print(f"🌐 Hostname: {details['hostname']}")
    
    print(f"\n✅ IP address successfully retrieved: {ip}")


if __name__ == "__main__":
    main()
