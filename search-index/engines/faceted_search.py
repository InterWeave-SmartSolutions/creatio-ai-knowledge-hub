import json
from typing import List, Dict

class FacetedSearchEngine:
    def __init__(self, core):
        self.core = core

    def apply_faceted_search(self, query: str, filters: Dict[str, str]) -> List[Dict]:
        # Conduct the base search
        base_results = self.core.search(query)
        
        # Apply filters
        filtered_results = []
        for result in base_results:
            matches_filters = all(
                result.get(key) == value for key, value in filters.items()
            )
            if matches_filters:
                filtered_results.append(result)
        return filtered_results

# Example usage:
# search_engine = SearchEngineCore()
# faceted_search = FacetedSearchEngine(search_engine)
# results = faceted_search.apply_faceted_search("search query", {"content_type": "video"})
