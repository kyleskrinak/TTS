#!/bin/zsh

if [ -z "$VIRTUAL_ENV" ]; then
  echo "❌ Python virtual environment not activated."
  echo "👉 Run: source bin/activate"
  exit 1
fi

echo "Running in $0 using shell $SHELL"

max_jobs=3
array=(*.txt)
pids=()

for i in "${array[@]}"; do
  echo "Processing $i"
  python3 mac-tts.py "$i" &  # Run the job in the background
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
