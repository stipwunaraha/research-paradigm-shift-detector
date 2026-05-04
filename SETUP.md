# STIP Development Environment Setup

## 🚀 Quick Start

Untuk mengatur environment development di localhost, jalankan:

```bash
# Install semua dependencies
pip install -r requirements.txt

# Jalankan setup script (opsional, untuk download model spaCy)
python setup_env.py
```

Atau gunakan setup script otomatis:

```bash
python setup_env.py
```

## 📦 Dependencies

Semua dependensi sudah terdaftar di `requirements.txt`:

### Core Libraries
- **spacy** (>=3.0,<4.0) - NLP processing
- **scispacy** (>=0.4.0,<0.5.0) - Biomedical NLP
- **sentence-transformers** (>=2.0.0,<3.0.0) - Semantic embeddings
- **numpy** (>=1.20.0,<2.0.0) - Numerical computing
- **pandas** (>=1.3.0,<3.0.0) - Data manipulation
- **scikit-learn** (>=0.24.0,<2.0.0) - Machine learning utilities

### Data & Visualization
- **jsonlines** - JSON Lines format support
- **requests** - HTTP library
- **matplotlib** - Plotting library
- **seaborn** - Statistical visualization

### Testing & Development
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **black** - Code formatter
- **flake8** - Linting
- **mypy** - Type checking

## 🔧 Setup Options

### Option 1: Using venv (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt

# Optional: Download spaCy models
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
```

### Option 2: Using conda

```bash
# Create conda environment
conda create -n stip python=3.9

# Activate environment
conda activate stip

# Install dependencies
pip install -r requirements.txt

# Download spaCy models
python -m spacy download en_core_web_sm
```

### Option 3: Automated Setup

Jalankan script setup otomatis:

```bash
# Full setup (includes spaCy models)
python setup_env.py

# Skip model downloads (faster)
python setup_env.py --skip-models
```

## ✅ Verifikasi Instalasi

Setelah instalasi, verifikasi dengan:

```bash
# Run tests
pytest tests/ -v

# Run example
python examples/analyze_attention.py

# Check package versions
python -c "import spacy; print(spacy.__version__)"
```

## 🛠️ Development Tools

### Code Formatting
```bash
black stip/ tests/ examples/
```

### Linting
```bash
flake8 stip/ tests/
```

### Type Checking
```bash
mypy stip/
```

### Test Coverage
```bash
pytest tests/ --cov=stip --cov-report=html
```

## 📝 Pre-commit Hooks (Optional)

Untuk setup pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

## 🐛 Troubleshooting

### Issue: spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

### Issue: Permission denied
```bash
# Use user installation
pip install --user -r requirements.txt
```

### Issue: Conflicting versions
```bash
# Create fresh virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📚 Next Steps

Setelah setup selesai:

1. **Run tests**: `pytest tests/ -v`
2. **Try example**: `python examples/analyze_attention.py`
3. **Start developing**: Edit files in `stip/` directory
4. **Generate sample data**: `python data/generate_sample.py`

## 🔗 Resources

- [spaCy Documentation](https://spacy.io/)
- [Sentence Transformers](https://www.sbert.net/)
- [pytest Documentation](https://docs.pytest.org/)
- [Black Formatter](https://black.readthedocs.io/)

---

**Happy Coding! 🚀**
