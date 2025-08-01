from utils.config import BASE_URL


class ProductAssociationEndpoints:

    BASE_PATH = f"{BASE_URL}/admin/product-association-types"

    @staticmethod
    def get_list(page=1, items_per_page=10, order="asc", translations_name="", code=""):
        
        url = (
            f"{ProductAssociationEndpoints.BASE_PATH}"
            f"?page={page}"
            f"&itemsPerPage={items_per_page}"
            f"&order[code]={order}"
        )

        if translations_name:
            url += f"&translations.name={translations_name}"
        if code:
            url += f"&code={code}"

        return url
