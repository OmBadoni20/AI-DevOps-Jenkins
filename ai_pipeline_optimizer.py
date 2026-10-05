import os
import sys
from google import genai


def analyze_pipeline(jenkinsfile):
    with open(jenkinsfile, "r", encoding="utf-8") as f:
        pipeline = f.read()

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = f"""
You are an AI DevOps CI/CD optimization assistant.

Analyze the following Jenkinsfile.

Identify practical opportunities to improve:

1. Pipeline execution efficiency
2. Redundant operations
3. Dependency installation
4. Docker build efficiency
5. Pipeline reliability
6. Security
7. Opportunities for caching
8. Opportunities for parallel execution, if appropriate

For every recommendation:
- Explain the current issue.
- Explain the proposed improvement.
- Explain the expected DevOps benefit.
- Do not invent timing improvements.
- If a recommendation cannot be justified from the Jenkinsfile, say so.

Jenkinsfile:
----------------
{pipeline}
----------------
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python ai_pipeline_optimizer.py Jenkinsfile")
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print("Jenkinsfile not found.")
        sys.exit(1)

    report = analyze_pipeline(sys.argv[1])

    print("\n========== AI JENKINS OPTIMIZATION ==========\n")
    print(report)
    print("\n==============================================\n")

    with open("ai_pipeline_optimization_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print("Optimization report saved to ai_pipeline_optimization_report.txt")