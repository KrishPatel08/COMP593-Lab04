from log_analysis import get_log_file_path_from_cmd_line, filter_log_by_regex
import pandas as pd

def main():
    


    log_file = get_log_file_path_from_cmd_line(1)
    
    dpt_tally = tally_port_traffic(log_file)

    generate_invalid_user_report(log_file)

    for dpt, count in dpt_tally.items():
        if count > 100:
            generate_port_traffic_report(log_file, dpt)

    pass


def tally_port_traffic(log_file):
    destination_port_logs = filter_log_by_regex(log_file, 'DPT=(.+?) ')[1]

    dpt_tally = {}
    for dpt_tuple in destination_port_logs:
        dpt_num = dpt_tuple[0]
        dpt_tally[dpt_num] = dpt_tally.get(dpt_num, 0) + 1

    return dpt_tally


def generate_port_traffic_report(log_file, port_number):
    regex = r"^(.{6}) (.{8}).*SRC=(.+?) DST=(.+?) .*SPT=(.+?) " + f"DPT=({port_number})"
    captured_data = filter_log_by_regex(log_file, regex)[1]

    report_df = pd.DataFrame(captured_data)
    report_header = ('Date', 'Time', 'Source IP Address', 'Destination IP Address', 'Source Port', 'Destination Port')
    report_df.to_csv(f'destination_port_{port_number}_report.csv', index=False, header=report_header)


def generate_invalid_user_report(log_file):
    regex = r"^(.{6}) (.{8}) .*Invalid user(.+) .*from(.+)"
    captured_data = filter_log_by_regex(log_file, regex)[1]

    report_df = pd.DataFrame(captured_data)
    report_header = ('Date', 'Time', 'Username', 'IP Address')
    report_df.to_csv(f'invalid_users.csv', index=False, header=report_header)
    


def generate_source_ip_log(log_file, ip_address):
    return

if __name__ == '__main__':
    main()