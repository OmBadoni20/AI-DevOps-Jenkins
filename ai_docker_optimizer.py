import os
import sys
from google import genai


def analyze_docker_files(dockerfile, requirements):
    with open(dockerfile, "r", encoding="utf-8") as f:
        docker_content = f.read()

    with open(requirements, "r", encoding="utf-8") as f:
        requirements_content = f.read()

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    prompt = f"""
You are an AI DevOps optimization assistant.

Analyze the following Dockerfile and Python dependency file.

Identify practical opportunities to improve:

1. Docker image size
2. Runtime dependency footprint
3. Build efficiency
4. Docker layer caching
5. Security
6. Separation of CI/development dependencies from runtime dependencies

Important:
- Base your recommendations only on the provided files.
- Do not invent dependencies or measurements.
- Explain why each recommendation would improve the DevOps workflow.
- Prioritize safe and practical changes for a small Flask application.

Dockerfile:
----------------
{docker_content}
----------------

Requirements:
----------------
{requirements_content}
----------------
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python ai_docker_optimizer.py <Dockerfile> <requirements.txt>")
        sys.exit(1)

    dockerfile = sys.argv[1]
    requirements = sys.argv[2]

    if not os.path.exists(dockerfile):
        print("Dockerfile not found.")
        sys.exit(1)

    if not os.path.exists(requirements):
        print("Requirements file not found.")
        sys.exit(1)

    report = analyze_docker_files(dockerfile, requirements)

    print("\n========== AI DOCKER OPTIMIZATION ==========\n")
    print(report)
    print("\n============================================\n")

    with open("ai_docker_optimization_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print("Optimization report saved to ai_docker_optimization_report.txt")