#!/usr/bin/env python3
import dns.resolver
import sys

domain = sys.argv[1]

# Resolve MX records for the domain
resolver = dns.resolver.Resolver()
try:
  nameserver = resolver.resolve(domain, "NS")[0].to_text()
  resolver.nameservers = [resolver.resolve(nameserver, "a")[0].to_text()]
except:
  print("Fail: Cannot find nameservers for domain")
  sys.exit(1)

try:
  mx_records = resolver.resolve(domain, "MX")
except:
  print("Fail: Cannot find mx record for domain")
  sys.exit(1)
# Flag to track if all MX records have A records
all_mx_have_a_records = True

# Loop through each MX record
for mx_record in mx_records:
    # Get the hostname from the MX record
    hostname = str(mx_record.exchange)
    # Resolve A records for the hostname
    try:
      a_records = dns.resolver.resolve(hostname, "A")
    except:
      all_mx_have_a_records = False
      break
    # Check if there are any A records
    if not a_records:
        all_mx_have_a_records = False
        break

if all_mx_have_a_records:
    print("Pass: All MX records have A records.")
else:
    print("Fail: Not all MX records have A records.")
