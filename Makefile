.PHONY: gendb
gendb: ip2asn-combined.mmdb

ip2asn-combined.mmdb:
	source .venv/bin/activate && python ./create.py

clean:
	rm -f ip2asn-combined.mmdb
