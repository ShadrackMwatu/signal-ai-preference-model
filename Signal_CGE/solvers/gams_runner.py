import subprocess
from pathlib import Path


# Path to GAMS executable
GAMS_EXECUTABLE = r"C:\Users\smwatu\OneDrive - Kenya Institute for Public Policy Research and Analysis\Documents\Signal\Signal_CGE\solvers\gams.exe"


def run_gams_model():

    """
    Run the full Signal CGE GAMS model from Python.
    """

    # Main model directory
    model_dir = Path("Signal_CGE/models/gams")

    # Main GAMS file
    model_file = "model.gms"

    # Full model path
    model_path = model_dir / model_file

    # Confirm model exists
    if not model_path.exists():
        raise FileNotFoundError(
            f"GAMS model not found: {model_path}"
        )

    print("\n===================================")
    print("Starting Signal CGE GAMS Model")
    print("===================================\n")

    print(f"Working directory: {model_dir.resolve()}")
    print(f"Model file: {model_file}\n")

    # IMPORTANT:
    # Run GAMS INSIDE the model folder so all
    # include files and folders resolve correctly.
    command = [
        GAMS_EXECUTABLE,
        model_file,
    ]

    result = subprocess.run(
        command,
        cwd=model_dir,
        capture_output=True,
        text=True,
    )

    print("\n========== GAMS STDOUT ==========\n")
    print(result.stdout)

    print("\n========== GAMS STDERR ==========\n")
    print(result.stderr)

    print("\n========== RETURN CODE ==========\n")
    print(result.returncode)

    if result.returncode == 0:
        print("\nSignal CGE solved successfully.\n")
    else:
        print("\nSignal CGE failed.\n")

    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


if __name__ == "__main__":

    output = run_gams_model()