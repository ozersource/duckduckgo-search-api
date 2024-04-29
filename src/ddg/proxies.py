import random


def load_proxies(input):
    if isinstance(input, str):
        with open(input, 'r') as file:
            proxies = file.readlines()
        proxy_list = [proxy.strip() for proxy in proxies]
    elif isinstance(input, list):
        proxy_list = input
    else:
        raise ValueError("Error format input")

    formatted_proxies = __format_proxies(proxy_list)
    if len(formatted_proxies) == 0:
        raise ValueError("Error format proxies input")
    return formatted_proxies


def __format_proxies(proxies):
    formatted_proxy_list = []
    for proxy in proxies:
        try:
            ip_port, user_pass = proxy.split('@')
            formatted_proxy = f"{user_pass}@{ip_port}"
            formatted_proxy_list.append(formatted_proxy)
        except ValueError:
            continue
    return formatted_proxy_list


def get_random_proxy(proxy_list):

    if not proxy_list:
        raise ValueError("Empty list")

    random_proxy = random.choice(proxy_list)
    proxy_dict = {
        'http': f"http://{random_proxy}",
        'https': f"http://{random_proxy}"
    }
    return proxy_dict

