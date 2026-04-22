<!-- research-paradigm-shift-detector/README.md -->

# ⏳ STIP: Structural Timeline of Intellectual Progression

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![spaCy](https://img.shields.io/badge/spaCy-3.0+-09a3d5.svg)](https://spacy.io/)

> *"Mendeteksi momen ketika komunitas riset secara kolektif berganti definisi terhadap konsep kunci."*

**STIP** adalah pipeline data yang memindai jutaan abstrak arXiv/PubMed untuk mendeteksi **Pergeseran Paradigma Semantik (Semantic Paradigm Shift)**. Alat ini memungkinkan kita untuk menentukan titik waktu historis ketika definisi suatu istilah ilmiah berubah secara fundamental.

### 📖 Contoh Kasus Nyata
- Kapan definisi "Signifikansi Statistik" bergeser dari sekadar p-value ke pendekatan Bayesian?
- Kapan istilah "Deep Learning" mulai menggeser istilah "Neural Networks" dalam judul makalah?
- Kapan fokus riset "AI" bergeser dari sistem pakar ke pembelajaran mesin?

### 🧪 Metodologi

1.  **Ekstraksi Frasa Kunci**: Menggunakan **spaCy** dan **SciSpacy** untuk mengekstrak *keyphrase* dari jutaan abstrak yang dikelompokkan per tahun.
2.  **Pelacakan Semantik Temporal**:
    - Membangun **Word2Vec** atau **BERT Embedding** untuk setiap *time slice* (misal: 1990-1995, 1996-2000).
    - Menghitung **cosine similarity** antara vektor istilah yang sama di periode waktu berbeda.
    - Penurunan drastis dalam *similarity* menandakan perubahan makna (mirip dengan deteksi *semantic shift*).
3.  **Deteksi Anomali**: Menggunakan metode statistik seperti *permutation tests* untuk memastikan perubahan signifikan, bukan kebetulan.

### 📦 Instalasi & Penggunaan

```bash
git clone https://github.com/stipwunaraha/research-paradigm-shift-detector.git
cd research-paradigm-shift-detector
pip install -r requirements.txt
python -m spacy download en_core_sci_lg  # Model SciSpacy
```

**Contoh: Menganalisis Pergeseran Makna "Attention" dalam AI:**
```python
from stip import ParadigmShiftDetector

detector = ParadigmShiftDetector(
    corpus_path="./data/arxiv_ai_abstracts.jsonl",
    term="attention"
)

# Jalankan analisis
shifts = detector.detect_shifts()

for shift in shifts:
    print(f"Tahun {shift.year}: Pergeseran signifikan terdeteksi!")
    print(f"  - Sebelum: {shift.context_before[:100]}...")
    print(f"  - Sesudah: {shift.context_after[:100]}...")
    print(f"  - Similarity Score: {shift.similarity:.3f}")
```

### 🚧 Roadmap
- [ ] Skrip untuk mengunduh metadata arXiv (via S3 bulk).
- [ ] Implementasi *sliding window* embedding dengan **Sentence-BERT**.
- [ ] Algoritma *permutation test* untuk signifikansi.
- [ ] Visualisasi *streamgraph* evolusi istilah.

### 📚 Referensi
- *Statistically Significant Detection of Semantic Shifts using Contextual Word Embeddings*.
- *TX-Ray: Quantifying and Explaining Model-Knowledge Transfer in (Un-)Supervised NLP*.

### 🤝 Kontribusi
Kami membutuhkan bantuan dalam *data engineering* (menangani dataset besar) dan visualisasi data.

### 📄 Lisensi
MIT License.
