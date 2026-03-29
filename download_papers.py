import arxiv
import os
import ssl
import certifi

# ✅ Fix SSL
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

download_dir = "data/papers"
os.makedirs(download_dir, exist_ok=True)

search = arxiv.Search(
    query="cat:cs.AI",
    max_results=10,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

print("Downloading papers...\n")

for i, result in enumerate(search.results()):
    
    # ✅ Use UNIQUE arXiv paper ID (BEST APPROACH)
    paper_id = result.entry_id.split("/")[-1]
    filename = f"{paper_id}.pdf"
    file_path = os.path.join(download_dir, filename)

    print(f"{i+1}. {result.title}")

    # ✅ Skip if already downloaded and valid
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > 0:
            print("⏭ Skipped (already exists)")
            continue
        else:
            print("⚠ Found corrupted file, re-downloading...")
            os.remove(file_path)

    try:
        result.download_pdf(dirpath=download_dir, filename=filename)

        # ✅ Validate download
        if os.path.exists(file_path) and os.path.getsize(file_path) == 0:
            print("❌ Download failed (0 KB), deleting...")
            os.remove(file_path)

    except Exception as e:
        print("❌ Error downloading:", e)

print("\n✅ Download complete")