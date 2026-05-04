<!-- research-paradigm-shift-detector/README.md -->

# ⏳ STIP: Structural Timeline of Intellectual Progression

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://github.com/stipwunaraha/research-paradigm-shift-detector/workflows/Tests/badge.svg)](https://github.com/stipwunaraha/research-paradigm-shift-detector/actions)
[![spaCy](https://img.shields.io/badge/spaCy-3.0+-09a3d5.svg)](https://spacy.io/)

**Detect semantic paradigm shifts in research literature through temporal embedding analysis.**

STIP (Structural Timeline of Intellectual Progression) adalah library Python yang dirancang untuk mengidentifikasi dan mengukur perubahan signifikan dalam makna dan penggunaan istilah ilmiah seiring waktu. Dengan menganalisis korpus besar abstrak penelitian, STIP membantu peneliti, bibliometrisian, dan analis kebijakan sains memahami bagaimana konsep berevolusi, bergabung, atau divergen sepanjang dekade kemajuan ilmiah.

---

## 🎯 Fitur Utama

- **Temporal Embedding**: Membangun word embeddings untuk setiap slice waktu (misal: per tahun) menggunakan SVD pada matriks ko-okurensi
- **Shift Detection**: Mengidentifikasi perubahan semantik yang signifikan secara statistik menggunakan permutation tests
- **Paradigm Analysis**: Menentukan tahun exact ketika istilah mengalami transformasi konseptual bermakna
- **Scalable Pipeline**: Memproses ribuan dokumen secara efisien dengan arsitektur modular
- **Export Ready**: Mengoutputkan hasil dalam format JSON untuk visualisasi dan analisis lanjutan

---

## 🚀 Quick Start

### Instalasi

```bash
# Clone repository
git clone https://github.com/stipwunaraha/research-paradigm-shift-detector.git
cd research-paradigm-shift-detector

# Install dependencies
pip install -r requirements.txt

# Download model spaCy
python -m spacy download en_core_web_sm

# Install dalam development mode
pip install -e .
```

### Penggunaan Dasar

```python
from stip import ParadigmShiftDetector

# Inisialisasi detector
detector = ParadigmShiftDetector(
    time_slices=5,  # Jumlah periode waktu
    min_freq=10,    # Minimum frekuensi istilah
    significance_threshold=0.95
)

# Load korpus Anda (format JSONL dengan field 'year' dan 'text')
corpus_path = "data/sample_corpus.jsonl"
results = detector.analyze(corpus_path)

# Dapatkan top paradigm shifts
for shift in results.get_top_shifts(n=10):
    print(f"{shift['term']}: {shift['year']} (score: {shift['similarity']:.3f}, p={shift['significance']:.3f})")
```

### Contoh Output

```
Term: "learning"
  Year 1999: similarity=-0.240, significance=0.981 ⚠️
  Year 2010: similarity=-0.185, significance=0.923

Term: "network"
  Year 2005: similarity=-0.312, significance=0.995 ⚠️
```

---

## 📊 Bagaimana Cara Kerjanya?

1. **Corpus Preprocessing**: Dokumen dikelompokkan per tahun dan ditokenisasi menggunakan spaCy
2. **Co-occurrence Matrix**: Membangun matriks term-context untuk setiap slice waktu
3. **Dimensionality Reduction**: Menerapkan SVD untuk membuat embeddings berdimensi rendah
4. **Alignment**: Menyelaraskan embeddings antar slice waktu menggunakan orthogonal Procrustes
5. **Shift Detection**: Menghitung jarak cosine dan menguji signifikansi via permutation test
6. **Visualization Ready**: Mengekspor hasil untuk plot timeline dan heatmap

---

## 📁 Struktur Proyek

```
research-paradigm-shift-detector/
├── stip/
│   ├── __init__.py          # Package exports
│   ├── embedding.py         # Kelas TemporalEmbedding
│   ├── shift_analyzer.py    # ShiftAnalyzer dengan permutation tests
│   └── detector.py          # Orchestrator ParadigmShiftDetector
├── data/
│   ├── sample_corpus.jsonl  # Dataset contoh (727 docs, 1990-2020)
│   └── generate_sample.py   # Generator korpus sintetis
├── examples/
│   └── analyze_attention.py # Contoh penggunaan
├── tests/
│   └── test_stip.py         # Unit dan integration tests
├── requirements.txt         # Dependencies Python
├── pyproject.toml          # Metadata package
├── setup.cfg               # Konfigurasi tambahan
├── SETUP.md                # Panduan setup lengkap
└── README.md               # File ini
```

---

## 🔬 Studi Kasus Nyata

STIP dapat menjawab pertanyaan seperti:

- **Bibliometrics**: Kapan definisi "Signifikansi Statistik" bergeser dari sekadar p-value ke pendekatan Bayesian?
- **AI History**: Kapan istilah "Deep Learning" mulai menggeser "Neural Networks" dalam judul makalah?
- **Science Policy**: Kapan fokus riset "AI" bergeser dari sistem pakar ke pembelajaran mesin?
- **Historical Analysis**: Bagaimana konsep "gene", "climate", atau "intelligence" berubah makna selama 50 tahun?
- **Literature Review**: Otomatis menemukan paper pivotal selama pergeseran paradigma

---

## 🧪 Menjalankan Tests

```bash
# Jalankan semua tests
pytest tests/ -v

# Jalankan dengan coverage
pytest tests/ --cov=stip --cov-report=html
```

Semua tests harus passing ✅ sebelum kontribusi diterima.

---

## 📝 Format Data

STIP mengharapkan data input dalam format JSONL (satu objek JSON per baris):

```json
{"year": 1995, "text": "This study explores neural networks for pattern recognition..."}
{"year": 1996, "text": "We propose a novel algorithm for machine learning tasks..."}
```

**Field wajib:**
- `year`: Integer (tahun publikasi)
- `text`: String (abstrak atau teks lengkap)

**Field opsional:**
- `id`: Identifier dokumen unik
- `title`: Judul paper
- Metadata tambahan apapun

---

## 🤝 Berkontribusi

Kontribusi sangat welcome! Ikuti langkah berikut:

1. Fork repository
2. Buat branch fitur (`git checkout -b feature/amazing-feature`)
3. Lakukan perubahan Anda
4. Jalankan tests (`pytest tests/ -v`)
5. Commit perubahan (`git commit -m 'Add amazing feature'`)
6. Push ke branch (`git push origin feature/amazing-feature`)
7. Buka Pull Request

Silakan baca [CONTRIBUTING.md](CONTRIBUTING.md) untuk detail code of conduct dan proses development.

**Kami khususnya membutuhkan bantuan dalam:**
- Data engineering (menangani dataset besar)
- Visualisasi data (streamgraph evolusi istilah)
- Integrasi dengan sumber data arXiv/PubMed

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

---

## 🙏 Acknowledgments

- Terinspirasi oleh pekerjaan dalam computational linguistics dan scientometrics
- Dibangun di atas fondasi dari [Hamilton et al. (2016)](https://doi.org/10.18653/v1/P16-1028) tentang diachronic word embeddings
- Menggunakan [spaCy](https://spacy.io/) untuk preprocessing NLP yang efisien
- Memanfaatkan [scikit-learn](https://scikit-learn.org/) untuk SVD dan statistical tests

---

## 📬 Kontak

- **Issues**: Laporkan bug atau request fitur via [GitHub Issues](https://github.com/stipwunaraha/research-paradigm-shift-detector/issues)
- **Discussions**: Bergabung dalam diskusi tentang metodologi dan aplikasi di [GitHub Discussions](https://github.com/stipwunaraha/research-paradigm-shift-detector/discussions)

---

> *"Science advances one funeral at a time."* — Max Planck

**STIP membantu Anda melihat kemajuan tersebut sebelum funerals terjadi.** 🔍📈
