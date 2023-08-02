with open('./photos_api/description.md', encoding='utf-8') as file:
    description = file.read()

application_metadata = {
    "title": "Patient API DIANA",
    "description": description,
    "version": "0.0.1.dev1",
}
