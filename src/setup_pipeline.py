from pathlib import Path
import subprocess
import sys
import time

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_step(step_name: str, command: list[str]) -> None:
    print(f"\n=== {step_name} ===")
    print("Running:", " ".join(command))

    result = subprocess.run(command, cwd=PROJECT_ROOT)

    if result.returncode != 0:
        print(f"\nStep failed: {step_name}")
        sys.exit(result.returncode)

    print(f"Completed: {step_name}")


def docker_compose_up() -> None:
    print("\n=== Starting MySQL with Docker ===")

    result = subprocess.run(
        ["docker", "compose", "up", "-d"],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        print("\nFailed to start Docker services.")
        sys.exit(result.returncode)

    print("Docker services started.")
    print("Waiting a few seconds for MySQL to initialize...")
    time.sleep(10)


def main() -> None:
    run_step("Download raw data", [sys.executable, "src/download_data.py"])
    run_step("Run ETL", [sys.executable, "src/etl.py"])

    docker_compose_up()

    run_step("Load cleaned data into MySQL", [sys.executable, "src/load_to_mysql.py"])

    print("\nPipeline setup complete.")


if __name__ == "__main__":
    main()