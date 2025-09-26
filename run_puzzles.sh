
#!/bin/bash

# Script to run puzzleSolver.py on all puzzle files with customizable parameters
# Usage: ./run_all_puzzles.sh [input_directory] [output_directory] [algorithm] [heuristic]
# Example: ./run_all_puzzles.sh puzzles_8 results 1 1

# Default values
INPUT_DIR=${1:-"puzzles_8"}
OUTPUT_DIR=${2:-"results"}
ALGORITHM=${3:-1}  # 1 for A*, 2 for RBFS
HEURISTIC=${4:-1}  # 1 for h1, 2 for h2

# Function to display usage
show_usage() {
    echo "Usage: $0 [input_directory] [output_directory] [algorithm] [heuristic]"
    echo ""
    echo "Parameters:"
    echo "  input_directory  : Directory containing puzzle input files (default: puzzles_8)"
    echo "  output_directory : Directory to store output files (default: results)"
    echo "  algorithm        : 1 for A*, 2 for RBFS (default: 1)"
    echo "  heuristic        : 1 for h1 (Manhattan), 2 for h2 (Misplaced) (default: 1)"
    echo ""
    echo "Examples:"
    echo "  $0                           # Use all defaults"
    echo "  $0 puzzles_8 results 1 1     # A* with Manhattan distance"
    echo "  $0 puzzles_8 results 1 2     # A* with Misplaced tiles"
    echo "  $0 puzzles_8 results 2 1     # RBFS with Manhattan distance"
    echo "  $0 puzzles_15 results 2 2    # RBFS with Misplaced tiles on 15-puzzles"
}

# Check if help is requested
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_usage
    exit 0
fi

# Validate algorithm parameter
if [[ "$ALGORITHM" != "1" && "$ALGORITHM" != "2" ]]; then
    echo "Error: Algorithm must be 1 (A*) or 2 (RBFS)"
    show_usage
    exit 1
fi

# Validate heuristic parameter
if [[ "$HEURISTIC" != "1" && "$HEURISTIC" != "2" ]]; then
    echo "Error: Heuristic must be 1 (h1) or 2 (h2)"
    show_usage
    exit 1
fi

# Check if input directory exists
if [[ ! -d "$INPUT_DIR" ]]; then
    echo "Error: Input directory '$INPUT_DIR' does not exist"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Create a subdirectory for this specific run
ALG_NAME=$([ "$ALGORITHM" == "1" ] && echo "Astar" || echo "RBFS")
HEUR_NAME=$([ "$HEURISTIC" == "1" ] && echo "h1" || echo "h2")
RUN_DIR="${OUTPUT_DIR}/${ALG_NAME}_${HEUR_NAME}"
mkdir -p "$RUN_DIR"

# Create log file for this run
LOG_FILE="${RUN_DIR}/run_log.txt"
RESULTS_CSV="${RUN_DIR}/results.csv"

# Function to determine puzzle size from filename or content
get_puzzle_size() {
    local file="$1"
    
    # First try to determine from filename
    if [[ "$file" == *"puzzle_8"* || "$file" == *"8puzzle"* ]]; then
        echo "3"
        return
    elif [[ "$file" == *"puzzle_15"* || "$file" == *"15puzzle"* ]]; then
        echo "4"
        return
    fi
    
    # If filename doesn't indicate size, check file content
    local lines=$(wc -l < "$file")
    if [[ $lines -eq 3 ]]; then
        echo "3"
    elif [[ $lines -eq 4 ]]; then
        echo "4"
    else
        echo "3"  # Default to 3 if uncertain
    fi
}

# Initialize results CSV
echo "filename,algorithm,heuristic,puzzle_size,status,execution_time_ms,solution_depth,states_explored" > "$RESULTS_CSV"

# Display run configuration
echo "=========================================="
echo "Running puzzleSolver.py with configuration:"
echo "  Input Directory: $INPUT_DIR"
echo "  Output Directory: $RUN_DIR"
echo "  Algorithm: $ALG_NAME (A=$ALGORITHM)"
echo "  Heuristic: $HEUR_NAME (H=$HEURISTIC)"
echo "  Log file: $LOG_FILE"
echo "  Results CSV: $RESULTS_CSV"
echo "=========================================="

# Initialize counters
total_files=0
successful_runs=0
failed_runs=0

# Start timing
start_time=$(date +%s)

# Process all .txt files in input directory
for input_file in "$INPUT_DIR"/*.txt; do
    # Skip if no .txt files found
    [[ ! -f "$input_file" ]] && continue
    
    # Get just the filename without path
    filename=$(basename "$input_file")
    echo "Processing: $filename"
    
    # Determine puzzle size
    puzzle_size=$(get_puzzle_size "$input_file")
    
    # Create output filename
    output_file="${RUN_DIR}/${filename%.txt}_${ALG_NAME}_${HEUR_NAME}_output.txt"
    
    # Record start time for this puzzle (macOS compatible)
    puzzle_start=$(python -c "import time; print(int(time.time() * 1000))")
    
    # Run the solver
    echo "  Running: python puzzleSolver.py $ALGORITHM $puzzle_size $HEURISTIC \"$input_file\" \"$output_file\""
    
    # Run the solver and capture output
    # Run the solver and capture output
    solver_output=$(python puzzleSolver.py "$ALGORITHM" "$puzzle_size" "$HEURISTIC" "$input_file" "$output_file" 2>&1)
    exit_code=$?
    
    if [[ $exit_code -eq 0 ]]; then
        # Extract execution time from solver output (e.g., "Algorithm took 1.23 milliseconds")
        execution_time=$(echo "$solver_output" | grep "Algorithm took" | sed 's/Algorithm took \([0-9.]*\) milliseconds/\1/')
        [[ -z "$execution_time" ]] && execution_time="N/A"
        
        # Extract states explored from output
        states_explored=$(echo "$solver_output" | grep "Nodes Explored:" | sed 's/Nodes Explored: //')
        [[ -z "$states_explored" ]] && states_explored="N/A"
        
        # Count solution depth (number of moves) - count commas + 1 for moves
        if [[ -f "$output_file" ]] && [[ -s "$output_file" ]]; then
            content=$(head -n1 "$output_file" | tr -d '\n')
            if [[ -n "$content" && "$content" != "" ]]; then
                # Count moves by counting commas and adding 1
                solution_depth=$(echo "$content" | grep -o ',' | wc -l)
                solution_depth=$((solution_depth + 1))
            else
                solution_depth=0
            fi
        else
            solution_depth="N/A"
        fi
        
        echo "  ✓ Success - Time: ${execution_time}ms, Depth: $solution_depth, States: $states_explored"
        echo "$filename,$ALG_NAME,$HEUR_NAME,$puzzle_size,SUCCESS,$execution_time,$solution_depth,$states_explored" >> "$RESULTS_CSV"
        ((successful_runs++))
    else
        # For failed runs, we can't extract algorithm time, so use N/A
        echo "  ✗ Failed - Check $LOG_FILE for details"
        echo "$solver_output" >> "$LOG_FILE"
        echo "$filename,$ALG_NAME,$HEUR_NAME,$puzzle_size,FAILED,N/A,N/A,N/A" >> "$RESULTS_CSV"
        ((failed_runs++))
    fi
    
    ((total_files++))
    echo ""
done

# End timing
end_time=$(date +%s)
total_time=$((end_time - start_time))

# Display summary
echo "=========================================="
echo "Run Summary:"
echo "  Total files processed: $total_files"
echo "  Successful runs: $successful_runs"
echo "  Failed runs: $failed_runs"
echo "  Total execution time: ${total_time}s"
echo "  Results saved to: $RESULTS_CSV"
echo "  Log file: $LOG_FILE"
echo "=========================================="

# Display results preview if successful runs exist
if [[ $successful_runs -gt 0 ]]; then
    echo ""
    echo "Results preview:"
    head -n 6 "$RESULTS_CSV" | column -t -s ','
fi