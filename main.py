import argparse
from youtube_module import search_youtube
from filters import filter_relevant
from database import init_db, save_to_db

def main():
    parser = argparse.ArgumentParser(description="InternLens Phase 1 - YouTube Pipeline")
    parser.add_argument("company_name", help="Company or internship name")

    args = parser.parse_args()
    company_name = args.company_name

    print(f"Searching YouTube for: {company_name}")

    init_db()

    youtube_results = search_youtube(company_name)
    youtube_filtered = filter_relevant(youtube_results, company_name)

    inserted = save_to_db(youtube_filtered, company_name)

    print("\nPipeline completed")
    print(f"Found {len(youtube_filtered)} relevant YouTube results")
    print(f"Inserted {inserted} records into internlens.db")

if __name__ == "__main__":
    main()