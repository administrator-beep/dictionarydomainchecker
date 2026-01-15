# 🚀 DictionaryDomainChecker

A high-performance Python tool for discovering available `.com` domains using English dictionary words. This script uses a multi-tiered approach—combining **Multi-threading**, **DNS Pre-screening**, and **RDAP lookups**—to find brandable gems while staying under the radar of registry rate limits.

---

## ✨ Features

* **Turbo Speed:** Multi-threaded architecture (`ThreadPoolExecutor`) processes multiple domains simultaneously.
* **Smart Filtering:** Uses **DNS Pre-screening** to instantly skip active websites (like apple.com) without wasting your RDAP quota.
* **Modern Protocol:** Replaces outdated WHOIS scraping with **RDAP** (Registration Data Access Protocol) for cleaner, JSON-based results.
* **Auto-Resume:** Tracks progress via `checkpoint.txt`. If the script stops, it picks up exactly where it left off.
* **Real-time Dashboard:** Live progress bar showing `[X/Y]`, percentage completion, and a dynamic **ETA**.
* **Completion Alert:** Visual summary and system beep once 100% of the dictionary is checked.

---

## 🛠️ Installation

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/dictionarydomainchecker.git](https://github.com/YOUR_USERNAME/dictionarydomainchecker.git)
    cd dictionarydomainchecker
    ```

2.  **Install Requirements:**
    ```bash
    pip install requests
    ```

---

## 🚀 How to Use

1.  **Configuration:**
    Open `hunter.py` and edit the **USER SETUP** section:
    ```python
    MAX_LENGTH = 6     # Target word length
    MAX_THREADS = 4    # Recommended: 4-6
    ```

2.  **Run the Script:**
    ```bash
    python hunter.py
    ```

---

## 🔍 How It Works



1.  **DNS Check (Fast Path):** The script attempts to resolve the domain's IP. If a site exists, it's marked "Taken" and skipped in milliseconds.
2.  **RDAP Lookup (Deep Check):** If no DNS record is found, the script queries the official RDAP server to confirm availability.
3.  **Auto-Throttle:** If the registry sends a `429 Too Many Requests` signal, the script automatically pauses for 60 seconds.

---

## 📜 License

[MIT](https://choosealicense.com/licenses/mit/)