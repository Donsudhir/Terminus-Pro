.PHONY: build clean reset check

build:
	mkdir -p /app/bin
	go build -buildvcs=false -trimpath -o /app/bin/vaultctl ./cmd/vaultctl
	go build -buildvcs=false -trimpath -o /app/bin/inspect ./cmd/inspect

clean:
	rm -f /app/bin/vaultctl /app/bin/inspect

reset:
	/app/scripts/reset-fixture.sh

check:
	go test ./...
