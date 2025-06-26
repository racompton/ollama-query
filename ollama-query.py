import argparse
import requests
import json
import random

DEFAULT_TIMEOUT = 10  # seconds

def debug_print(enabled, message):
    if enabled:
        print(f"[DEBUG] {message}")

def get_models(ip, debug=False):
    try:
        url = f"http://{ip}:11434/api/tags"
        debug_print(debug, f"Fetching models from {url}")
        resp = requests.get(url, timeout=DEFAULT_TIMEOUT)
        resp.raise_for_status()
        debug_print(debug, f"Model list from {ip}: {resp.text}")
        return resp.json()
    except Exception as e:
        print(f"[{ip}] Failed to fetch models: {e}")
        return None

def query_model(ip, model_name, prompt, debug=False):
    try:
        url = f"http://{ip}:11434/api/generate"
        payload = {"model": model_name, "prompt": prompt, "stream": False}
        debug_print(debug, f"Querying {url} with payload: {payload}")
        response = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        debug_print(debug, f"Response from {ip}: {data}")
        return data.get("response") or data.get("content", "")
    except Exception as e:
        print(f"[{ip}] Failed to query model: {e}")
        return ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='File containing IP addresses')
    parser.add_argument('--query', required=True, help='File containing prompt query')
    parser.add_argument('--output', required=True, help='Output file for results')
    parser.add_argument('--model', help='Optional: Specify model name to use')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        ips = [line.strip() for line in f if line.strip()]

    random.shuffle(ips)  # 👈 Shuffle the list for randomness

    with open(args.query, 'r') as f:
        prompt = f.read().strip()

    with open(args.output, 'w') as outfile:
        for ip in ips:
            debug_print(args.debug, f"Processing IP: {ip}")
            models = get_models(ip, debug=args.debug)
            if not models or not models.get('models'):
                continue
            model_name = args.model or models['models'][0]['name']
            if not model_name:
                print(f"[{ip}] No models found")
                continue
            result = query_model(ip, model_name, prompt, debug=args.debug)
            clean_result = result.replace('\n', ' ').strip()
            print(f"Model is: {model_name}, Output is: {clean_result} \n")
            outfile.write(f"Model is: {model_name}, Output is: {clean_result} \n")
            outfile.flush()

if __name__ == '__main__':
    main()
