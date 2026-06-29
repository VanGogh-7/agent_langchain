from typing import List

from langchain_community.utilities import DuckDuckGoSearchAPIWrapper


def web_search(web_query: str, num_results: int) -> List[str]:
    search = DuckDuckGoSearchAPIWrapper()

    return [
        result["link"]
        for result in search.results(web_query, num_results)
    ]

