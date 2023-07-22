import json

class Page:
    def __init__(self, id, created_time, last_edited_time, created_by, last_edited_by, cover, icon, parent, archived, properties, url, public_url):
        self.id = id
        self.created_time = created_time
        self.last_edited_time = last_edited_time
        self.created_by = created_by
        self.last_edited_by = last_edited_by
        self.cover = cover
        self.icon = icon
        self.parent = parent
        self.archived = archived
        self.properties = properties
        self.url = url
        self.public_url = public_url

    @classmethod
    def from_json(cls, json_data):
        results = json_data.get("results", [])
        pages = []
        for result in results:
            id = result.get("id")
            created_time = result.get("created_time")
            last_edited_time = result.get("last_edited_time")
            created_by = result.get("created_by", {}).get("id")
            last_edited_by = result.get("last_edited_by", {}).get("id")
            cover = result.get("cover")
            icon = result.get("icon")
            parent = result.get("parent", {}).get("database_id")
            archived = result.get("archived", False)
            properties = result.get("properties", {})
            url = result.get("url")
            public_url = result.get("public_url")
            page = cls(id, created_time, last_edited_time, created_by, last_edited_by, cover, icon, parent, archived, properties, url, public_url)
            pages.append(page)
        return pages
