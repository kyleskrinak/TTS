#!/bin/zsh

## Determine Python interpreter explicitly (prefer local venv installation)
if [ -x "./venv/bin/python" ]; then
  PYTHON="./venv/bin/python"
elif [ -x "./bin/python" ]; then
  PYTHON="./bin/python"
elif [ -n "$VIRTUAL_ENV" ]; then
  # venv is already activated, use the python from the activated env
  PYTHON="python3"
else
  echo "❌ Python virtual environment not activated and no local venv found."
  echo "👉 Either activate the venv: source venv/bin/activate"
  echo "👉 Or run with explicit interpreter: ./venv/bin/python mac-tts.py"
  exit 1
fi

echo "Running in $0 using shell $SHELL"

max_jobs=3
array=( *.txt(N) )

# Filter out non-content text files (README, requirements, .done files)
filtered=()
for f in "${array[@]}"; do
  case "$f" in
    requirements.txt|README*|*.done) continue;;
    *) filtered+=("$f") ;;
  esac
done
array=("${filtered[@]}")

if [ ${#array[@]} -eq 0 ]; then
  echo "No .txt files to process. (Filtered out README, requirements.txt, and .done files)"
  exit 0
fi
pids=()

for i in "${array[@]}"; do
  echo "Processing $i"
  "$PYTHON" mac-tts.py "$i" &  # Run the job in the background using explicit interpreter
  pids+=($!)  # Store the PID of the background job

  # Check if we have reached the max_jobs limit
  while (( ${#pids[@]} >= max_jobs )); do
    # Check the status of each PID
    for pid in "${pids[@]}"; do
      if ! kill -0 "$pid" 2>/dev/null; then
        # Remove completed PIDs
        pids=(${pids[@]/$pid})
      fi
    done
    sleep 1  # Prevent tight polling
  done
done

# Wait for any remaining background jobs to complete
for pid in "${pids[@]}"; do
  wait "$pid"
done
