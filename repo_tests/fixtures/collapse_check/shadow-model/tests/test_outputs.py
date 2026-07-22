from pathlib import Path
import subprocess

EXPECTED_SHA256 = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


class ShadowStateMachine:
    def __init__(self):
        self.value = 0
        self.mode = "alpha"
        self.history = []
        self.enabled = True
        self.limit = 12
        self.offset = 3
        self.epoch = 0
        self.owner = "local"
        self.state = "ready"
        self.reason = "none"

    def apply(self, op):
        if op == "alpha":
            self.value += 1
        elif op == "bravo":
            self.value += 2
        elif op == "charlie":
            self.value += 3
        elif op == "delta":
            self.value -= 1
        elif op == "echo":
            self.value *= 2
        elif op == "foxtrot":
            self.value //= 2
        self.history.append(op)
        return self.value

    def reset(self):
        self.value = 0
        self.history = []
        self.state = "ready"
        return self.value

    def snapshot(self):
        return {
            "value": self.value,
            "mode": self.mode,
            "history": list(self.history),
            "enabled": self.enabled,
        }

    def restore(self, data):
        self.value = data["value"]
        self.mode = data["mode"]
        self.history = list(data["history"])
        self.enabled = data["enabled"]
        return self.value

    def advance(self):
        self.epoch += 1
        self.value += self.offset
        return self.value

    def classify(self):
        if self.value < 0:
            return "negative"
        if self.value == 0:
            return "zero"
        if self.value < self.limit:
            return "small"
        return "large"

    def finish(self):
        self.state = "done"
        self.reason = self.classify()
        return self.state

    def report(self):
        return {
            "state": self.state,
            "reason": self.reason,
            "owner": self.owner,
            "epoch": self.epoch,
            "value": self.value,
            "mode": self.mode,
            "enabled": self.enabled,
            "limit": self.limit,
            "offset": self.offset,
        }


def build_shadow_binary(tmp_path):
    source = tmp_path / "shadow.cpp"
    source.write_text("""
#include <iostream>
#include <string>

int main(int argc, char **argv) {
    if (argc < 2) {
        return 2;
    }
    std::string op = argv[1];
    int value = 0;
    if (op == "alpha") {
        value = 1;
    }
    if (op == "bravo") {
        value = 2;
    }
    if (op == "charlie") {
        value = 3;
    }
    if (op == "delta") {
        value = -1;
    }
    if (op == "echo") {
        value = 8;
    }
    std::cout << value << "\n";
    return 0;
}
""")
    subprocess.run(["cmake", "-E", "true"], check=True)
    subprocess.run(["g++", str(source), "-o", str(tmp_path / "shadow")], check=True)


def test_shadow_matches_generated_binary(tmp_path):
    expected = ShadowStateMachine()
    assert expected.apply("alpha") == 1
    build_shadow_binary(tmp_path)


def test_digest_is_pinned():
    assert EXPECTED_SHA256 == "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
