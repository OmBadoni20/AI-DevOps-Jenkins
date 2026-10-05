import os
import sys
from google import genai


def analyze_log(log_file):
    # Read the Jenkins/test failure log
    with open(log_file, "r", encoding="utf-8") as f:
        log = f.read()

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = f"""
You are an AI-powered DevOps failure analysis assistant.

Analyze the following Jenkins CI/CD failure log.

Provide a concise and technically accurate report with exactly these sections:

1. Error
2. Root Cause
3. Affected Stage
4. Affected Test/File
5. Recommended Fix
6. Severity
7. Confidence

Important:
- Base your answer only on the provided log.
- Do not invent information.
- Clearly distinguish the actual error from the recommended solution.

Jenkins Failure Log:
--------------------
{log}
--------------------
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ai_log_analyzer.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]

    if not os.path.exists(log_file):
        print(f"Error: Log file not found: {log_file}")
        sys.exit(1)

    report = analyze_log(log_file)

    print("\n========== AI DEVOPS FAILURE ANALYSIS ==========\n")
    print(report)
    print("\n================================================\n")

    with open("ai_failure_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print("AI report saved to: ai_failure_report.txt")