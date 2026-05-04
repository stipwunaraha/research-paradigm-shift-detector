"""
Example usage of the ParadigmShiftDetector.
"""

from stip import ParadigmShiftDetector

def main():
    """
    Example: Analyze semantic shifts for the term "attention" in AI research.
    """
    # Initialize detector
    detector = ParadigmShiftDetector(
        corpus_path="./data/sample_corpus.jsonl",
        term="attention",
        time_slice_years=5,
        threshold=0.3
    )
    
    try:
        # Load and process corpus
        detector.load_corpus()
        
        # Build embeddings
        detector.build_embeddings()
        
        # Detect paradigm shifts
        shifts = detector.detect_shifts()
        
        # Print results
        if shifts:
            print("\n=== DETECTED PARADIGM SHIFTS ===")
            for shift in shifts:
                print(f"\nYear {shift.year}:")
                print(f"  Term: {shift.term}")
                print(f"  Similarity Score: {shift.similarity:.3f}")
                print(f"  Significance: {shift.significance_score:.3f}")
                print(f"  Context Before: {shift.context_before}")
                print(f"  Context After: {shift.context_after}")
        else:
            print("\nNo significant paradigm shifts detected.")
        
        # Export results
        detector.export_results("./results/shift_analysis.json", shifts)
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nTo run this example, create a sample corpus file at ./data/sample_corpus.jsonl")
        print("Format: {\"year\": 1995, \"title\": \"...\", \"abstract\": \"...\"}")


if __name__ == "__main__":
    main()
