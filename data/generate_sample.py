"""
Sample corpus generator for testing purposes.
Creates a small JSONL file with synthetic abstracts demonstrating semantic shift.
"""

import json
import random

def generate_sample_corpus(output_path: str, n_documents: int = 500):
    """
    Generate a sample corpus with synthetic abstracts showing semantic shift.
    
    The term "attention" will have different contexts before and after year 2000
    to simulate a paradigm shift (from cognitive science to deep learning).
    """
    
    # Pre-2000: "attention" in cognitive science context
    pre_2000_templates = [
        "We study human attention mechanisms in visual perception tasks.",
        "Attention allocation was measured using reaction time experiments.",
        "The role of selective attention in memory encoding was investigated.",
        "Participants performed attention-demanding tasks while monitoring stimuli.",
        "Our findings suggest attention modulates early sensory processing.",
        "Cognitive load affects attention span in multitasking scenarios.",
        "Attention deficits were observed in clinical populations.",
        "The neuroscience of attention reveals distinct neural networks.",
        "Spatial attention enhances perception at attended locations.",
        "Divided attention impairs performance on complex tasks."
    ]
    
    # Post-2000: "attention" in machine learning/deep learning context
    post_2000_templates = [
        "We propose a novel attention mechanism for sequence modeling.",
        "The attention layer computes weighted sums over encoder states.",
        "Self-attention enables the model to capture long-range dependencies.",
        "Multi-head attention improves representation learning in transformers.",
        "Attention weights visualize which tokens the model focuses on.",
        "The transformer architecture relies entirely on attention mechanisms.",
        "Scaled dot-product attention is computationally efficient.",
        "Cross-attention connects encoder and decoder in sequence-to-sequence models.",
        "Attention-based models outperform RNNs on translation tasks.",
        "Global attention mechanisms aggregate information across the input."
    ]
    
    documents = []
    
    # Generate documents from 1990 to 2020
    for year in range(1990, 2021):
        # Number of documents per year increases over time
        n_docs_this_year = max(10, int(n_documents / 31 * (1 + (year - 1990) / 31)))
        
        for _ in range(n_docs_this_year):
            if year < 2000:
                # Pre-shift: cognitive science context
                template = random.choice(pre_2000_templates)
                # Add some variation
                abstract = f"{template} This paper presents experimental results from {random.randint(20, 100)} participants."
            else:
                # Post-shift: ML/deep learning context
                template = random.choice(post_2000_templates)
                # Add some variation
                abstract = f"{template} We evaluate our approach on {random.choice(['WMT', 'ImageNet', 'SQuAD', 'COCO'])} dataset."
            
            doc = {
                "year": year,
                "title": f"Research on attention mechanisms ({year})",
                "abstract": abstract
            }
            documents.append(doc)
    
    # Write to JSONL file
    with open(output_path, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc) + '\n')
    
    print(f"Generated {len(documents)} sample documents to {output_path}")
    print(f"Time range: 1990-2020")
    print(f"Simulated paradigm shift around year 2000")


if __name__ == "__main__":
    generate_sample_corpus("./data/sample_corpus.jsonl", n_documents=500)
