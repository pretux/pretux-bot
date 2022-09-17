from unittest import result
import requests
import json
import time

url_base = "https://api.notion.com/v1/databases/"
database_contemplated = "f78bbfdcff85446089f4a1900f6b555b"
database_general = "24ae3965567841808b9ac6349c7b6e33"
database_refused = "94271d3ea7404fc2a846cf741a737b9f"
notion_token = "secret_hYdSZcKGGln29FVZ9ZiH9kbZBPRi5yrLXWkiDMrPD4W"
notion_version = "2021-08-16"
user_info = {}


def check_user(email, database, check_pedency):
    url = url_base + database + "/query"
    if check_pedency:
        payload = json.dumps({"filter": {"and": [{"property": "Email", "email": {
                             "equals": email}}, {"property": "Pendente", "checkbox": {"equals": True}}]}})
    else:
        payload = json.dumps(
            {"filter": {"property": "Email", "email": {"equals": email}}})

    headers = {'Authorization': 'Bearer ' + notion_token,
               'Notion-Version': notion_version, 'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


def remove_user_after_confirm(user_notion_id):
    url = "https://api.notion.com/v1/blocks/" + user_notion_id
    payload = {}

    headers = {'Authorization': 'Bearer ' + notion_token,
               'Notion-Version': notion_version, 'Content-Type': 'application/json'}
    response = requests.request("DELETE", url, headers=headers, data=payload)
    return response.json()


def confirm_scholarship(name, email, course_name, course_title, end_time, activity, telegram_id):
    url = "https://api.notion.com/v1/pages/"
    payload = json.dumps({
    "parent": {
        "database_id": database_general
    },
    "properties": {
        "Link": {
            "id": "%3D%3BAL",
            "type": "url",
            "url": "none"
        },
        "Data do termino do curso": {
            "id": "%40%5CQB",
            "type": "date",
            "date": {
                "start": "2022-09-24",
                "end": end_time
            }
        },
        "Email": {
            "id": "Eoo%7C",
            "type": "email",
            "email": email
        },
        "Curso": {
            "id": "sHj%3D",
            "type": "select",
            "select": {
                "id": "EgE|",
                "name": course_name,
                "color": "red"
            }
        },
        "Done": {
            "id": "vZbr",
            "type": "select",
            "select": {
                "id": "UpUB",
                "name": "Não",
                "color": "orange"
            }
        },
        "Título": {
            "id": "%5BMu%3C",
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Mergo"
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                    "plain_text": course_title,
                    "href": "none"
                }
            ]
        },
        "Pendente": {
            "id": "nT%3A%5D",
            "type": "checkbox",
            "checkbox": True
        },
        "telegram_id": {
            "id": "PnFU",
            "type": "number",
            "number": telegram_id
        },
        "Tipo": {
            "id": "kIk_",
            "type": "select",
            "select": {
                "id": "ETjJ",
                "name": "Entregar um artigo",
                "color": "orange"
            }
        },
        "Observações": {
            "id": "w%3D%3FH",
            "type": "rich_text",
            "rich_text": []
        },
        "Pessoa": {
            "id": "title",
            "type": "title",
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": name
                    },
                    "plain_text": name,
                    "href": "none"
                }
            ]
        }
    }
})

    headers = {'Authorization': 'Bearer ' + notion_token,
               'Notion-Version': notion_version, 'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()

def refuse_scholarship(name, email, course_name, course_title, end_time, activity, telegram_id):
    url = "https://api.notion.com/v1/pages/"
    payload = json.dumps({
    "parent": {
        "database_id": database_refused
    },
    "properties": {
        "Link": {
            "id": "%3D%3BAL",
            "type": "url",
            "url": "none"
        },
        "Data do termino do curso": {
            "id": "%40%5CQB",
            "type": "date",
            "date": {
                "start": "2022-09-24",
                "end": end_time
            }
        },
        "Email": {
            "id": "Eoo%7C",
            "type": "email",
            "email": email
        },
        "Curso": {
            "id": "sHj%3D",
            "type": "select",
            "select": {
                "id": "EgE|",
                "name": course_name,
                "color": "red"
            }
        },
        "Done": {
            "id": "vZbr",
            "type": "select",
            "select": {
                "id": "UpUB",
                "name": "Não",
                "color": "orange"
            }
        },
        "Título": {
            "id": "%5BMu%3C",
            "type": "rich_text",
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "Mergo"
                    },
                    "annotations": {
                        "bold": False,
                        "italic": False,
                        "strikethrough": False,
                        "underline": False,
                        "code": False,
                        "color": "default"
                    },
                    "plain_text": course_title,
                    "href": "none"
                }
            ]
        },
        "Pendente": {
            "id": "nT%3A%5D",
            "type": "checkbox",
            "checkbox": False
        },
        "telegram_id": {
            "id": "PnFU",
            "type": "number",
            "number": telegram_id
        },
        "Tipo": {
            "id": "kIk_",
            "type": "select",
            "select": {
                "id": "ETjJ",
                "name": "Entregar um artigo",
                "color": "orange"
            }
        },
        "Observações": {
            "id": "w%3D%3FH",
            "type": "rich_text",
            "rich_text": []
        },
        "Pessoa": {
            "id": "title",
            "type": "title",
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": name
                    },
                    "plain_text": name,
                    "href": "none"
                }
            ]
        }
    }
})

    headers = {'Authorization': 'Bearer ' + notion_token,
               'Notion-Version': notion_version, 'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    return response.json()

def check_pendency(email):
    user = check_user(email, database_general, True)
    print(user)
    user_info = []
    if len(user["results"]) == 0:
        user_info.append({'status': "is_not_pending", })
        return user_info

    else:
        user_info.append(
            {
                'status': "is_pending",
                'name': user["results"][0]["properties"]["Pessoa"]["title"][0]["plain_text"],
                'course_name': user["results"][0]["properties"]["Título"]["rich_text"][0]["plain_text"],
                'email': user["results"][0]["properties"]["Email"]["email"],
                'pendecy':  user["results"][0]["properties"]["Pendente"]["checkbox"],
                'activity': user["results"][0]["properties"]["Tipo"]["select"]["name"]
            })
        return user_info




def main(email):
    user = check_user(email, database_general, True)
    user_info = []
    if len(user["results"]) == 0:
        user_info = []
        user = check_user(email, database_contemplated, False)
        if len(user["results"]) == 0:
            user_info.append({'status': "not_contemplated", })
            return user_info
        else:
            user_info.append(
                {
                    'status': "contemplated",
                    'user_id': user["results"][0]["id"],
                    'name': user["results"][0]["properties"]["Pessoa"]["title"][0]["plain_text"],
                    'email': user["results"][0]["properties"]["Email"]["email"],
                    'course_name': user["results"][0]["properties"]["Título"]["rich_text"][0]["plain_text"],
                    'course_title': user["results"][0]["properties"]["Curso"]["select"]["name"],
                    'activity':     user["results"][0]["properties"]["Tipo"]["select"]["name"],
                    'end_time': user["results"][0]["properties"]["Data do termino do curso"]["date"]["start"]
                })
            return user_info
    else:
        user_info.append(
            {
                'status': "is_pending",
                'name': user["results"][0]["properties"]["Pessoa"]["title"][0]["plain_text"],
                'course_name': user["results"][0]["properties"]["Título"]["rich_text"][0]["plain_text"],
                'email': user["results"][0]["properties"]["Email"]["email"],
                'pendecy':  user["results"][0]["properties"]["Pendente"]["checkbox"],
                'activity': user["results"][0]["properties"]["Tipo"]["select"]["name"]
            })
        return user_info


