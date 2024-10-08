import netaddr
import mmdbencoder
import csv
from collections import namedtuple
import os
import subprocess


Row = namedtuple("Row", ["start", "end", "as_num", "iso_code", "as_description"])

subprocess.call(["curl", "-O", "https://iptoasn.com/data/ip2asn-combined.tsv.gz"])
subprocess.call(["gunzip", "-f", "ip2asn-combined.tsv.gz"])


enc = mmdbencoder.Encoder(
    6,  # IP version
    32,  # Size of the pointers
    "Geoacumen-Country",  # Name of the table
    ["en"],  # Languages
    {
        "en": "Geoacumen - Open Source IP to country mapping database by Kevin Chung"
    },  # Description
    compat=True,
)

print("Building data")
iso_codes = {}
with open("ip2asn-combined.tsv", newline="") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter="\t")
    for row in csv_reader:
        row = Row(*row)

        # Insert country data only once
        if row.iso_code in iso_codes:
            data_offset = iso_codes[row.iso_code]
        else:
            data_offset = enc.insert_data({"country": {"iso_code": row.iso_code}})
            iso_codes[row.iso_code] = data_offset

        cidrs = netaddr.iprange_to_cidrs(row.start, row.end)
        for cidr in cidrs:
            enc.insert_network(cidr, data_offset, strict=False)


print("Writing database")
with open("ip2asn-combined.mmdb", "wb") as f:
    enc.write(f)
os.remove("ip2asn-combined.tsv")
