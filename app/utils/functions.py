import requests
import json
import configparser
import time
import logging

from functools import wraps
from aiogram import types

from openai import OpenAI

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='debug.log',  
    filemode='a'
) 

def search_posts(query: str, end_cursor: str, limit: int = 10) -> dict: 

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,es;q=0.5,de;q=0.4',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.threads.com',
        'priority': 'u=1, i',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.168", "Google Chrome";v="138.0.7204.168"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"15.5.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'x-asbd-id': '359341',
        'x-bloks-version-id': 'b12cfbcbf33dbc5967ca6292a74038c86c0f5679d254920a74764d33130237fa',
        'x-csrftoken': 'PICVi8Zr7koLgtn4eW7RRS3f0MhTIzUh',
        'x-fb-friendly-name': 'BarcelonaProfileCompletionQuery',
        'x-fb-lsd': '-WT3f1gsIjWvQXvTm1qz-E',
        'x-ig-app-id': '238260118697367',
        'x-root-field-name': 'xdt_api__v1__text_feed__search_results__connection_v2',
    }

    raw_data = {
        'after': end_cursor,
        'before': None,
        'first': limit,
        'has_serp_header': False,
        'last': None,
        'meta_place_id': None,
        'pinned_ids': None,
        'power_search_info': None,
        'query': query,
        'recent': 1,
        'search_surface': 'default',
        'tagID': None,
        'trend_fbid': None,
        '__relay_internal__pv__BarcelonaHasSERPHeaderrelayprovider': False,
        '__relay_internal__pv__BarcelonaIsLoggedInrelayprovider': True,
        '__relay_internal__pv__BarcelonaHasSelfReplyContextrelayprovider': False,
        '__relay_internal__pv__BarcelonaHasInlineReplyComposerrelayprovider': False,
        '__relay_internal__pv__BarcelonaIsSearchDiscoveryEnabledrelayprovider': False,
        '__relay_internal__pv__IsTagIndicatorEnabledrelayprovider': False,
        '__relay_internal__pv__BarcelonaOptionalCookiesEnabledrelayprovider': True,
        '__relay_internal__pv__BarcelonaHasSpoilerStylingInforelayprovider': False,
        '__relay_internal__pv__BarcelonaQuotedPostUFIEnabledrelayprovider': False,
        '__relay_internal__pv__BarcelonaIsCrawlerrelayprovider': False,
        '__relay_internal__pv__BarcelonaHasDisplayNamesrelayprovider': False,
        '__relay_internal__pv__BarcelonaCanSeeSponsoredContentrelayprovider': False,
        '__relay_internal__pv__BarcelonaShouldShowFediverseM075Featuresrelayprovider': False,
        '__relay_internal__pv__BarcelonaImplicitTrendsGKrelayprovider': False,
        '__relay_internal__pv__BarcelonaIsInternalUserrelayprovider': False
    }

    data = {
        'doc_id': '24204831102456745',
        'variables': json.dumps(raw_data),
    }

    try:
        cookies = load_cookies_from_ini('app/constants/config.ini')
  
        response = requests.post('https://www.threads.com/graphql/query',
                                cookies=cookies,
                                headers=headers,
                                data=data)
        
        if response.status_code != 200:
            logging.info(response.json())
            logging.error(f"Failed to search posts. Status code: {response.status_code}")
            return None
        
        return response.json()
    
    except Exception as e:
        logging.error(f"Error occurred while searching posts: {e}")
        return None


def comment_post(post_pk: str, text: str) -> None:

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,es;q=0.5,de;q=0.4',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.threads.com',
        'priority': 'u=1, i',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.168", "Google Chrome";v="138.0.7204.168"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"macOS"',
        'sec-ch-ua-platform-version': '"15.5.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'x-asbd-id': '359341',
        'x-bloks-version-id': 'b12cfbcbf33dbc5967ca6292a74038c86c0f5679d254920a74764d33130237fa',
        'x-csrftoken': 'PICVi8Zr7koLgtn4eW7RRS3f0MhTIzUh',
        'x-fb-friendly-name': 'BarcelonaProfileCompletionQuery',
        'x-fb-lsd': '-WT3f1gsIjWvQXvTm1qz-E',
        'x-ig-app-id': '238260118697367',
        'x-root-field-name': 'xdt_api__v1__text_feed__search_results__connection_v2',
    }

    # Prepare the data for the request
    variables = {"entry_point":"create_reply",
                 "excluded_inline_media_ids":[],
                 "fediverse_composer_enabled":True,
                 "is_spoiler_media":False,
                 "link_attachment_url":None,
                 "ranking_info_token":None,
                 "reply_control":0,
                 "reply_id":post_pk,
                 "special_effects_enabled_str":None,
                 "tag_header":None,
                 "text_with_entities":{"entities":[],"text":text}}
    
    # Payload
    data = {
        'audience': 'default',
        'barcelona_source_reply_id': post_pk,
        'caption': text,
        'creator_geo_gating_info': '{"whitelist_country_codes":[]}',
        'custom_accessibility_caption': '',
        'gen_ai_detection_method': '',
        'internal_features': '',
        'is_meta_only_post': '',
        'is_paid_partnership': '',
        'is_upload_type_override_allowed': '1',
        'publish_mode': 'text_post',
        'text_post_app_info': json.dumps(variables),
        'upload_id': str(time.time() * 1000), # store it as miliseconds to keep things real
        'jazoest': '22801',
    }
    
    # Make the request to publish the comment
    try:
        cookies = load_cookies_from_ini('app/constants/config.ini')

        response = requests.post(
            'https://www.threads.com/api/v1/media/configure_text_only_post/',
            cookies=cookies,
            headers=headers,
            data=data,
        )

        # Check the response 
        if response.status_code != 200:
            logging.error(f"Failed to post comment: {response.status_code}")
            
            if response.json()['message']:
                return response.json()
            
            return
        
    except Exception as e:
        logging.error(f"Error while posting comment: {e}")
        return
    

def load_cookies_from_ini(file_path='config.ini'):
    config = configparser.ConfigParser(interpolation=None)
    config.read(file_path)

    cookies = {}

    if 'Cookies' in config:
        cookies = dict(config['Cookies'])
    else:
        print(config.read(file_path))


    return cookies


def update_cookies_in_ini(new_cookies: dict, file_path='config.ini'):
    config = configparser.ConfigParser(interpolation=None)
    config.read(file_path)

    config['Cookies'] = {}

    for key, value in new_cookies.items():
        config['Cookies'][key] = value

    with open(file_path, 'w') as configfile:
        config.write(configfile)


def generate_comment(post_text: str) -> str:

    """
    Generate a comment for a post using OpenAI's chat completion API.
    :param post_text: The text of the post to generate a comment for.
    """

    config = configparser.ConfigParser(interpolation=None)
    config.read('app/constants/config.ini')

    # Initialize the OpenAI client with the API key
    client = OpenAI(api_key=config['Bot']['open_ai_token'])
    
    # Create a chat completion request to generate a comment
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": config['Bot']['system_comment_prompt'].strip('"')
            },
            {
                "role": "user",
                "content": f"Generate a comment for this post: {post_text}"
            }
        ],
        temperature=0.7,
        max_tokens=100, # specify the maximum number of tokens if needed
        n=1,
    )

    # Return the generated comment from the response
    return response.choices[0].message.content


def check_topic(text: str) -> str:

    config = configparser.ConfigParser(interpolation=None)
    config.read('app/constants/config.ini')

    # Init client with API key
    client = OpenAI(api_key=config['Bot']['open_ai_token'])

    # Wrap it with try/except.. just in case.
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                "role": "system",
                "content": config['Bot']['system_topic_prompt'].strip('"')
                },
                {
                    "role": "user",
                    "content": f"Post content to analyze: {text}"
                }
            ],
            temperature=0.7,
            max_tokens=50, # feel free to adjust token count here
            n=1,
        )
    except Exception as e:
        logging.error(e)
        return
    
    return response.choices[0].message.content



def admin_only():
    def decorator(handler):
        @wraps(handler)
        async def wrapper(msg: types.Message, *args, **kwargs):
            config = configparser.ConfigParser(interpolation=None)
            config.read('app/constants/config.ini')
            admin_id = config['Bot'].get('admin_id')

            if str(msg.chat.id) != str(admin_id):
                await msg.answer("🚫 You are not allowed to use this command.")
                return
            return await handler(msg, *args, **kwargs)
        return wrapper
    return decorator