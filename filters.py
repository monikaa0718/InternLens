def filter_relevant(results, company_name):
    filtered = []
    company = company_name.lower()

    for item in results:
        text = (item.get("title", "") + " " + item.get("body", "")).lower()

        if company in text and "internship" in text:
            filtered.append(item)

    return filtered