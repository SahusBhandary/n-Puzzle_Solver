#!/bin/bash

# Script to generate 15 8-puzzles (N=3) with varying D values
# D values: 5, 10, 15, 20, 25 (3 puzzles each)

# Create output directory if it doesn't exist
mkdir -p puzzles_15

# Counter for puzzle numbering
counter=1

# D values to use
d_values=(10 20 30 40 50)

echo "Generating 15 8-puzzles with varying D values..."

# Generate 3 puzzles for each D value
for d in "${d_values[@]}"; do
    echo "Generating puzzles with D=$d..."
    
    for i in {1..3}; do
        output_file="puzzles_15/puzzle_15_D${d}_${i}.txt"
        
        echo "  Creating puzzle $counter: $output_file"
        python puzzleGenerator.py 4 $d "$output_file"
        
        if [ $? -eq 0 ]; then
            echo "    ✓ Successfully created $output_file"
        else
            echo "    ✗ Failed to create $output_file"
        fi
        
        ((counter++))
    done
    echo ""
done

echo "Puzzle generation complete!"
echo "Generated files:"
ls -la puzzles_15/

echo ""
echo "Summary:"
echo "- Total puzzles: 15"
echo "- Puzzle size: 15-puzzle (N=4)"
echo "- D values used: 5, 10, 15, 20, 25"
echo "- Puzzles per D value: 3"
echo "- Output directory: puzzles_15/"