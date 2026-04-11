import os
import re
import json
import base64
import math
import argparse

class ForensicAuditor:
    def __init__(self):
        # Elite 2026 Detection Patterns
        self.secret_patterns = {
            "AWS_ACCESS_KEY": re.compile(r"AKIA[0-9A-Z]{16}"),
            "AWS_SECRET_KEY": re.compile(r"[a-zA-Z0-9+/]{40}"),
            "GITHUB_TOKEN": re.compile(r"ghp_[a-zA-Z0-9]{36}"),
            "PRIVATE_KEY": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
            "GENERIC_SECRET": re.compile(r"(?:key|secret|token|password|auth|api)[-_]?(?:key|secret|token|password|auth|api)?\s*[:=]\s*['\"]([a-zA-Z0-9]{16,})['\"]", re.IGNORECASE)
        }
        
        self.malware_heuristics = {
            "EXECUTION": re.compile(r"(?:eval|exec|os\.system|subprocess\.|Popen|os\.popen|shell_exec|base64_decode)\s*\("),
            "NETWORK_EXFIL": re.compile(r"(?:requests\.post|urllib\.request|http\.client|socket\.connect|curl|wget|axios\.post)\s*\("),
            "ENCODED_PAYLOAD": re.compile(r"(?:base64|hex|rot13|u\d+)\.(?:decode|b64decode|unhexlify)"),
            "SUSPICIOUS_DOMAINS": re.compile(r"(?:pastebin|discordapp\.com/api/webhooks|ngrok\.io|webhook\.site|temp-mail|anonfiles)"),
            "FILE_SYSTEM_MUTATION": re.compile(r"(?:os\.remove|shutil\.rmtree|os\.chmod|subprocess\.run\(['\"]rm\s+-rf)"),
        }

    def calculate_entropy(self, data):
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def analyze_file(self, file_path):
        results = {
            "file": os.path.basename(file_path),
            "status": "CLEAN",
            "risk_score": 0,
            "findings": {
                "secrets": [],
                "malicious_patterns": [],
                "suspicious_entropy": False
            }
        }

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # 1. Scan for Secrets
                for name, pattern in self.secret_patterns.items():
                    matches = pattern.findall(content)
                    if matches:
                        results["findings"]["secrets"].append({"type": name, "count": len(matches)})
                        results["risk_score"] += 10 * len(matches)

                # 2. Heuristics
                for name, pattern in self.malware_heuristics.items():
                    matches = pattern.findall(content)
                    if matches:
                        results["findings"]["malicious_patterns"].append({"type": name, "count": len(matches)})
                        results["risk_score"] += 20 * len(matches)

                # 3. Entropy Check
                entropy = self.calculate_entropy(content)
                if entropy > 5.5:  # Arbitrary threshold for high-entropy text
                    results["findings"]["suspicious_entropy"] = True
                    results["risk_score"] += 15

            # Final Verdict
            if results["risk_score"] >= 50:
                results["status"] = "DANGEROUS"
            elif results["risk_score"] > 0:
                results["status"] = "SUSPICIOUS"

        except Exception as e:
            results["status"] = "ERROR"
            results["error"] = str(e)

        return results

def main():
    parser = argparse.ArgumentParser(description="Elite 2026 Forensic File Auditor")
    parser.add_argument("target", help="Path to the file to audit")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    args = parser.parse_args()

    auditor = ForensicAuditor()
    report = auditor.analyze_file(args.target)

    if args.json:
        print(json.dumps(report, indent=4))
    else:
        print(f"--- Forensic Report: {report['file']} ---")
        print(f"Status: {report['status']}")
        print(f"Risk Score: {report['risk_score']}")
        if report["findings"]["secrets"]:
            print(f"Secrets Found: {report['findings']['secrets']}")
        if report["findings"]["malicious_patterns"]:
            print(f"Security Patterns: {report['findings']['malicious_patterns']}")
        if report["findings"]["suspicious_entropy"]:
            print("WARNING: High entropy detected (Potential encryption/packing)")

if __name__ == "__main__":
    main()
