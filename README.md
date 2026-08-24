# Game History Analyzer

**API untuk menganalisis riwayat permainan dari berbagai platform gaming.**

## Fitur Phase 1

✅ **Database SQLite** untuk menyimpan riwayat permainan
✅ **API RESTful** dengan FastAPI
✅ **Import CSV/JSON** untuk data riwayat
✅ **Deteksi duplikat** menggunakan hash SHA256
✅ **Validasi data** komprehensif dengan Pydantic
✅ **Sanitasi keamanan** untuk data sensitif
✅ **Test suite lengkap** dengan pytest
✅ **UI dalam Bahasa Indonesia**

## Struktur Proyek

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py              # Konfigurasi
│   ├── models/
│   │   ├── __init__.py
│   │   └── database.py        # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── game.py
│   │   └── game_round.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py      # Database setup
│   ├── services/
│   │   ├── __init__.py
│   │   ├── sanitizer.py       # Redaksi data sensitif
│   │   ├── parser.py          # Parser CSV/JSON
│   │   ├── history_service.py # Operasi database
│   │   └── import_service.py  # Import data
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py          # Logging
│   │   └── validators.py      # Validasi data
│   └── api/
│       ├── __init__.py
│       └── routes/
│           ├── __init__.py
│           ├── health.py      # GET /api/health
│           ├── games.py       # GET/POST /api/games
│           ├── history.py     # GET/DELETE /api/history
│           └── import_data.py # POST /api/history/import
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # pytest config
│   ├── test_api_*.py          # API tests
│   ├── test_sanitizer.py      # Security tests
│   ├── test_parser.py         # Parser tests
│   ├── test_validators.py     # Validator tests
│   └── fixtures/
│       ├── sample_history.json
│       └── sample_history.csv
├── requirements.txt
└── run.py                      # Entry point

data/
├── .gitkeep
└── app.db                      # SQLite database (auto-created)
```

## Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/Alfaruqi10/game-history-analyzer.git
cd game-history-analyzer
```

### 2. Setup Virtual Environment (Windows)

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
# Copy template environment
copy ../.env.example ../.env
```

Edit `.env` sesuai kebutuhan (opsional, default sudah cukup).

### 5. Database Setup

Database akan otomatis dibuat saat aplikasi dijalankan pertama kali.

## Menjalankan Aplikasi

### Start Backend API (Windows)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API akan tersedia di: **http://127.0.0.1:8000**

Dokumentasi interaktif: **http://127.0.0.1:8000/docs**

## API Endpoints

### Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "Sehat",
  "message": "Backend Game History Analyzer berjalan normal"
}
```

---

### Daftar Permainan

```http
GET /api/games
```

**Response:**
```json
[
  {
    "id": 1,
    "game_name": "Book of Dead",
    "provider": "Play'n GO",
    "game_type": "slot",
    "created_at": "2026-08-24T08:00:00"
  }
]
```

---

### Buat Permainan

```http
POST /api/games
Content-Type: application/json

{
  "game_name": "Book of Dead",
  "provider": "Play'n GO",
  "game_type": "slot"
}
```

---

### Riwayat Permainan (Paginated)

```http
GET /api/history?skip=0&limit=50
```

**Response:**
```json
{
  "total": 100,
  "skip": 0,
  "limit": 50,
  "data": [
    {
      "id": 1,
      "external_round_id": "ROUND_001",
      "timestamp": "2026-08-24T08:00:00",
      "bet_amount": 10000,
      "win_amount": 5000,
      "multiplier": 0.5,
      "currency": "IDR",
      "result": "LOSE",
      "game": "Book of Dead",
      "provider": "Play'n GO"
    }
  ]
}
```

**Query Parameters:**
- `skip` (int, default=0): Berapa banyak record yang dilewati
- `limit` (int, default=50, max=100): Jumlah record per halaman

---

### Detail Riwayat

```http
GET /api/history/{id}
```

**Response:**
```json
{
  "id": 1,
  "external_round_id": "ROUND_001",
  "timestamp": "2026-08-24T08:00:00",
  "bet_amount": 10000,
  "win_amount": 5000,
  "multiplier": 0.5,
  "currency": "IDR",
  "result": "LOSE",
  "created_at": "2026-08-24T08:00:00"
}
```

---

### Import Riwayat (CSV/JSON)

```http
POST /api/history/import
Content-Type: multipart/form-data

file: <file.csv atau file.json>
user_id: "20512184" (optional)
```

**Response:**
```json
{
  "success": true,
  "total": 5,
  "saved": 5,
  "skipped": 0,
  "errors": [],
  "warnings": []
}
```

**Format CSV:**
```csv
user_id,game,provider,round_id,timestamp,bet_amount,win_amount,multiplier,currency,result
20512184,Book of Dead,Play'n GO,ROUND_001,2026-08-24T08:00:00Z,10000,5000,0.5,IDR,LOSE
```

**Format JSON:**
```json
[
  {
    "user_id": "20512184",
    "game": "Book of Dead",
    "provider": "Play'n GO",
    "round_id": "ROUND_001",
    "timestamp": "2026-08-24T08:00:00Z",
    "bet_amount": 10000,
    "win_amount": 5000,
    "multiplier": 0.5,
    "currency": "IDR",
    "result": "LOSE"
  }
]
```

---

### Hapus Semua Riwayat

```http
DELETE /api/history
```

**Response:**
```json
{
  "message": "5 record berhasil dihapus",
  "deleted_count": 5
}
```

## Menjalankan Tests

### Run All Tests

```bash
cd backend
pytest -v
```

### Run Specific Test File

```bash
pytest tests/test_api_health.py -v
```

### Run with Coverage

```bash
pytest --cov=app tests/
```

### Test Categories

- **test_api_*.py** - API endpoint tests
- **test_sanitizer.py** - Security/redaction tests
- **test_parser.py** - CSV/JSON parser tests
- **test_validators.py** - Data validation tests

## Keamanan

### Data Sensitif yang Tidak Disimpan

❌ Passwords
❌ Cookies
❌ Session tokens
❌ Authorization headers
❌ API keys

Semua data sensitif di-**redact** sebelum disimpan atau di-log.

### Sanitizer

Modul `app/services/sanitizer.py` secara otomatis:
- Menghapus header sensitif
- Menredact field password/token/secret
- Membersihkan string yang mengandung credentials

## Deteksi Duplikat

Setiap record memiliki hash SHA256 yang dihitung dari:
- Round ID
- Timestamp
- Bet Amount
- Win Amount

Duplikat otomatis terdeteksi dan dilewati saat import.

## Struktur Database

### users
```sql
id (Primary Key)
external_user_id (Unique)
username
created_at
updated_at
```

### games
```sql
id (Primary Key)
game_name (Indexed)
provider
game_type
created_at
```

### game_rounds
```sql
id (Primary Key)
user_id (Foreign Key)
game_id (Foreign Key)
external_round_id (Unique, Indexed)
timestamp (Indexed)
bet_amount
win_amount
multiplier
currency
result (Enum: WIN, LOSE, DRAW, UNKNOWN)
raw_data_hash (Unique)
created_at (Indexed)
```

### collection_runs
```sql
id (Primary Key)
started_at
finished_at
status (PENDING, RUNNING, COMPLETED, FAILED)
records_found
records_saved
records_skipped
error_message
```

## Troubleshooting

### "Module not found" error

```bash
# Pastikan virtual environment aktif
venv\Scripts\activate

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### Database error

```bash
# Hapus database dan buat ulang
rm data/app.db
python -m uvicorn app.main:app --reload
```

### Port 8000 sudah terpakai

```bash
# Gunakan port berbeda
python -m uvicorn app.main:app --reload --port 8001
```

## Limitations (Phase 1)

⚠️ **Single-user environment** - Tidak ada autentikasi multi-user
⚠️ **Local SQLite only** - Tidak mendukung database external
⚠️ **No UI frontend** - Hanya API backend (akses via /docs)
⚠️ **No real-time sync** - Import harus manual
⚠️ **No BC.Game integration** - Tidak terhubung ke BC.Game API

## Rencana Phase 2

- [ ] Web UI (React/Vue.js)
- [ ] Autentikasi & multi-user support
- [ ] Database PostgreSQL
- [ ] Real-time data sync
- [ ] Advanced analytics & reports
- [ ] User preferences & settings

## Kontribusi

Pull requests dipersilahkan! Untuk perubahan besar, silakan buka issue terlebih dahulu.

## Lisensi

MIT

## Kontak

GitHub: [@Alfaruqi10](https://github.com/Alfaruqi10)
