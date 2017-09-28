import re
from geoip import geolite2
import argparse

IP_PATTERN = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'


def search_dict_in_list(ip, arr):
    for item in arr:
        if item['ip'] == ip:
            return item


def is_log_file(log_file):
    if log_file:
        return log_file.split('.')[1] == 'log'


def is_valid_ip(ip):
    if ip:
        return re.match(IP_PATTERN, ip)


def get_log_ips(log):
    ips = []
    if log:
        arr = log.split(' ')
        for item in arr:
            if is_valid_ip(item):
                ips.append(item)
    return ips


def activities_per_ip(log_file):
    pass


def get_unique_ips(log_file):
    """
    Read a log file and return all unique ip with number of hits and
    country of origin.
    Save all unique ips and its info to a file named unique_ips.log
    """
    unique_ips = []
    with open(log_file) as logs:
        for line in logs:
            ips = get_log_ips(line)
            for ip in ips:
                # unique ip details
                ip_info = {'ip': ip, 'hits': 1, 'country': None}

                # get Ip country origin
                match = geolite2.lookup(ip_info.get('ip'))
                if match is not None:
                    ip_info['country'] = match.country

                # Add number of hits if ip already exist in unique ip list
                # else add it to the unique ip list
                ip_exist = search_dict_in_list(ip, unique_ips)
                if not ip_exist:
                    unique_ips.append(ip_info)
                else:
                    ip_exist['hits'] += 1

            # for the sake of faster testing
            # comment out this block of code to
            # get all the unique ips inside the sample log file.
            if len(unique_ips) == 20:
                break

        # write all unique ips with number of hits and country in a file
        # named unique_ips.
        file = open('unique_ips.log', 'w')
        file.write(str(unique_ips))
        print unique_ips

        # close file after writing the list of ips.
        file.close()


COMMANDS = {
            'get_unique_ips': get_unique_ips
           }

cmd_parser = argparse.ArgumentParser(description="Parse Apache Log")
cmd_parser.add_argument('-c', '--command', required=True, choices=list(COMMANDS.keys()))
cmd_parser.add_argument('-F', '--file', required=True)
args = cmd_parser.parse_args()

if __name__ == "__main__":
    if not is_log_file(args.file):
        print "file must be a log file"
    function = COMMANDS[args.command]
    function(args.file)