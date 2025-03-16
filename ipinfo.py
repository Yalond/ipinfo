#!user/bin/env python3
title = """
██╗██████╗ ██╗███╗   ██╗███████╗ ██████╗ 
██║██╔══██╗██║████╗  ██║██╔════╝██╔═══██╗
██║██████╔╝██║██╔██╗ ██║█████╗  ██║   ██║
██║██╔═══╝ ██║██║╚██╗██║██╔══╝  ██║   ██║
██║██║     ██║██║ ╚████║██║     ╚██████╔╝
╚═╝╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝
"""

import argparse
import random

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#print(f"{bcolors.HEADER}Warning: No active frommets remain. Continue?{bcolors.ENDC}")

def convert_bin_to_cidr(bin_value):
    return str(list(filter(lambda x: x != " ", list(bin_value))).index("0"))

def convert_mask_to_cidr(mask):
    return convert_bin_to_cidr(' '.join([bin(int(x))[2:] for x in mask.split('.')]))

def convert_cidr_to_bin(cidr):
    out = ''
    counter = 0
    for i, v in enumerate(list('1' * int(cidr) + '0' * (32 - int(cidr)))):
        if (i != 0 and i % 8 == 0):
            out += ' '
        out += v
        counter += 1
    return out

def convert_cidr_to_mask(cidr):
    return '.'.join([str(int(x, 2)) for x in convert_cidr_to_bin(cidr).split(' ')])

def get_mask_info(inp):
    cidr = inp 

    if len(inp) == 35:
        cidr = convert_bin_to_cidr(inp)
    elif len(inp.split('.')) == 4:
        cidr = convert_mask_to_cidr(inp)
        res = convert_cidr_to_mask(cidr)
        if inp != res: raise Exception('Not a valid subnet mask.')
    elif not inp.isdigit():
        raise Exception("Mask value must be in either DDT, CIDR, or Binary")

    return {
        'BIN': convert_cidr_to_bin(cidr),
        'DDN': convert_cidr_to_mask(cidr),
        'CIDR': cidr
    }

def generate_random_cidr():
    return str(8 + int(random.random() * 32-8))

def mask_game(round_count, current_score=0, rounds_played=0):

    print(' ')
    if round_count == 0:
        print(f'You scored {current_score}/{rounds_played}, which is {int(float(current_score)/rounds_played * 100)}%!')
        return
    else: 
        print(f'Round {rounds_played + 1} of {round_count + rounds_played}')

    mask_info = get_mask_info(generate_random_cidr())

    target = 'CIDR'
    value = 'DDN'
    if random.random() > 0.5:
        target = 'DDN'
        value = 'CIDR'
    
    print(f'Convert {value} {mask_info[value]} to {target}\n')
    inp = input('Answer >>> ')
    if inp == mask_info[target]: 
        current_score += 1
        print("Correct!")
    else:
        print(f'Wrong! The correct answer is {mask_info[target]}')
    mask_game(round_count - 1, current_score, rounds_played + 1)

ip_class_info = {
    'A': {
        'from': '1.0.0.0',
        'to': '126.0.0.0',
        'default_mask': '255.0.0.0',
        'detail': 'For large networks',
        'Total networks': '126 (2^7)',
        'Hosts per network': '2^24 - 2',
        'Network Bits': '8'
        
    },
    'B': {
        'from': '128.0.0.0',
        'to': '191.255.0.0',
        'default_mask': '255.255.0.0',
        'detail': 'For medium networks',
        'Total networks': '16384 (2^14)',
        'Hosts per network': '2^16 - 2',
        'Network Bits': '16'
    },
    'C': {
        'from': '192.0.0.0',
        'to': '223.255.255.0',
        'default_mask': '255.255.255.0',
        'detail': 'For small networks',
        'Total networks': '2097152 (2^21)',
        'Hosts per network': '2^8 - 2',
        'Network Bits': '24'
    },
    'D': {
        'from': '224.0.0.0',
        'to': '239.255.255.255',
        'default_mask': '',
        'detail': 'Multicast'
    },
    'E': {
        'from': '240.0.0.0',
        'to': '255.255.255.255',
        'default_mask': '',
        'detail': 'Reserved for future use'
    }
}

def ip_to_array(ip):
    return [int(x) for x in ip.split('.')]

def generate_ip_address():
    start = random.randrange(1, 223)
    if (start == 127): return generate_ip_address()
    end = random.randrange(1, 255)
    m1 = random.randrange(0, 256)
    m2 = random.randrange(0, 256)
    return '.'.join([start, m1, m2, end])

def range_contains_ip(start, end, ip):
    start_array = ip_to_array(start)
    end_array = ip_to_array(end)
    ip_array = ip_to_array(ip)

    return start_array[0] >= ip_array[0] and ip_array[0] <= end_array[0]

def get_ip_class(ip):
    for ip_class, ip_range in ip_class_info.items():
        if range_contains_ip(ip_range['from'], ip_range['to'], ip):
            ip_range['class'] = ip_class
            return ip_class
    return 'Unknown IP class'
    
def get_ip_info(ip):
    ip_class = get_ip_class(ip)
    if ip_class in ip_class_info:
        return ip_class_info[ip_class]
    else: return {'Invlaid IP Address': ''}

def join_ip(start, mid, end):
    return '.'.join(list(map(str, start)) + list(map(str, mid)) + list(map(str, end)))

def get_first_usable(ip):
    parts = ip.split('.')
    return '.'.join(parts[:3] + [str(int(parts[-1]) + 1)])

def get_last_useable(ip):
    parts = ip.split('.')
    return '.'.join(parts[:3] + [str(int(parts[-1]) - 1)])

def get_info(ip, mask):
    ip_info = get_ip_info(ip)
    mask_info = get_mask_info(mask)

    prefix = int(mask_info['CIDR'])
    network_bits = int(ip_info['Network Bits'])

    subnet_bits = prefix - network_bits
    host_bits = 32 - prefix 
    subnet_count = 2 ** subnet_bits
    hosts_per_subnet = 2 ** host_bits - 2

    octet_count = prefix//8
    octet_host_count = 2 ** (8 - prefix% 8)

    parts = [int(x) for x in ip.split('.')]
    start = parts[:octet_count]
    end_subnet = [0 for x in parts[octet_count + 1:]]
    end_broadcast = [255 for x in end_subnet]

    host_list = []
    host_part_counter = 0
    while host_part_counter < 255:
        subnetID = join_ip(start, [host_part_counter], end_subnet)
        broadcast = join_ip(start, [host_part_counter + octet_host_count-1], end_broadcast)
        host_list.append({
            'subnetID': subnetID,
            'broadcast': broadcast,
            'first': get_first_usable(subnetID),
            'last': get_last_useable(broadcast)
        })
        host_part_counter += octet_host_count

    return {
        'Network Bits': network_bits,
        'Subnet Bits': subnet_bits,
        'Host Bits': host_bits,
        'Subnets': subnet_count,
        'Hosts Per Subnet': hosts_per_subnet,
        'HostList': host_list
    }

def main():
    parser = argparse.ArgumentParser(
        prog='IP Info',
        description='Provides information about IP addresses and subnet masks'
    )
    parser.add_argument('-m', '--mask', help='Provides information on the subnet mask.')
    parser.add_argument('-g', '--maskgame', help='Play the subnet mask game, specify the number of rounds you want to play.')
    parser.add_argument('-i', '--ipinfo', help='Print information relating to the IP class.')
    args = vars(parser.parse_args())

    if args['mask'] and args['ipinfo']:
        print(f'\nIP info for: {args["ipinfo"]} {args["mask"]} \n' )
        info = get_info(args['ipinfo'], args['mask'])
        for key, value in info.items():
            if (key != 'HostList'): print(f'{key}: {value}')
        print('--------------------------') 
        for hosts in info['HostList']:
            print(', '.join([f"{k}: {v}" for k, v in hosts.items()]))

    elif args['mask']:
        for key, value in get_mask_info(args['mask']).items():
            print(f'{key}: {value}')

    elif args['maskgame']:
        mask_game(int(args['maskgame']))

    elif args['ipinfo']:
        print(f'\nIP info for: {args["ipinfo"]}\n' )
        for key, value in get_ip_info(args['ipinfo']).items():
            print(f'{key}: {value}')
        print(' ')
    else:
        print(title)    
        print(parser.format_help())

if __name__ == '__main__':
    main()