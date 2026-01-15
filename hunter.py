import requests
import time
import os
import socket
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

# --- Configuration ---
MAX_THREADS = 4  
MAX_LENGTH = 6
OUTPUT_FILE = "rdap_available.txt"
CHECKPOINT_FILE = "checkpoint.txt"
RDAP_BASE_URL = "https://rdap.verisign.com/com/v1/domain/"
DICT_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"

def is_active_site(domain):
    """Checks DNS to see if the site is already live."""
    try:
        socket.gethostbyname(domain)
        return True
    except (socket.error, UnicodeError):
        return False

def check_domain(word):
    """The task each thread will perform."""
    domain = f"{word}.com"
    
    # Step 1: DNS Check (Ultra Fast, skips the queue)
    if is_active_site(domain):
        return None 

    # Step 2: RDAP Check (Only if DNS says it might be free)
    try:
        resp = requests.get(RDAP_BASE_URL + domain, timeout=3)
        if resp.status_code == 404:
            return domain
        elif resp.status_code == 429:
            return "RATE_LIMIT"
    except:
        pass
    return None

def run_turbo_search():
    # 1. Load words
    print("--- Loading Dictionary ---")
    r = requests.get(DICT_URL)
    all_words = [w.strip().lower() for w in r.text.splitlines() if len(w.strip()) <= MAX_LENGTH and w.strip().isalnum()]
    words = sorted(list(set(all_words)))
    total_count = len(words)
    
    # 2. Resume Logic
    start_idx = 0
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            last = f.read().strip()
            if last in words:
                start_idx = words.index(last) + 1

    print(f"Turbo Sprint Started | Threads: {MAX_THREADS} | Remaining: {total_count - start_idx}")
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        with open(OUTPUT_FILE, "a") as out:
            # Process in batches equal to thread count
            for i in range(start_idx, total_count, MAX_THREADS):
                batch = words[i : i + MAX_THREADS]
                
                # Run the batch through the threads
                results = list(executor.map(check_domain, batch))

                for result in results:
                    if result == "RATE_LIMIT":
                        print("\n[!] Rate Limit Hit! Cooling down for 60s...")
                        time.sleep(60)
                    elif result:
                        print(f"\n[!] MATCH FOUND: {result}")
                        out.write(result + "\n")
                        out.flush()

                # Update Checkpoint with the last word of the batch
                with open(CHECKPOINT_FILE, "w") as f:
                    f.write(batch[-1])

                # Progress Display
                current_count = i + len(batch)
                percent = (current_count / total_count) * 100
                
                # Calculate ETA
                elapsed = time.time() - start_time
                processed = current_count - start_idx
                if processed > 0:
                    avg_time = elapsed / processed
                    eta = (total_count - current_count) * avg_time
                    eta_str = str(timedelta(seconds=int(eta)))
                else:
                    eta_str = "Calculating..."

                sys.stdout.write(f"\rProgress: [{current_count}/{total_count}] {percent:.2f}% | ETA: {eta_str} | Current: {batch[-1]}.com    ")
                sys.stdout.flush()

                # Small sleep to keep the connection stable
                time.sleep(1.0)

if __name__ == "__main__":
    try:
        run_turbo_search()
    except KeyboardInterrupt:
        print("\n\nPaused. Progress saved to checkpoint.")