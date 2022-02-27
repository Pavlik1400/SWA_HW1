import os
import yaml

from argparse import ArgumentParser, Namespace
from typing import Dict, Optional

from src import FACADE, LOGGING, MESSAGES, SERVICES_FILES, SERVICES_NAMES

SERVICES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")

def main(args: Namespace, config: Dict[str, int]):
    selected_service: Optional[str] = None
    if args.facade:
        if args.logging or args.messages:
            raise ValueError("Specify only one of --facade, --logging, --messages service to start")
        selected_service = FACADE
    elif args.logging:
        if args.messages:
            raise ValueError("Specify only one of --facade, --logging, --messages service to start")
        selected_service = LOGGING
    elif args.messages:
        selected_service = MESSAGES
    else:
        raise ValueError("Specify one of --facade, --logging, --messages service to start")

    start_cmd = f"uvicorn \
        {SERVICES_FILES[selected_service]}:{SERVICES_NAMES[selected_service]} \
        --host {config[selected_service]['host']} \
        --port {config[selected_service]['port']}"
    os.system(start_cmd)
    
if __name__ == "__main__":
    parser = ArgumentParser()
    
    parser.add_argument("--config", "-c", type=str, required=False, help="config with ports", default="services_config.yml")
    parser.add_argument("--facade", action="store_const", const=True, help="start facade service")
    parser.add_argument("--logging", action="store_const", const=True, help="start logging service")
    parser.add_argument("--messages", action="store_const", const=True, help="start messages service")
    args = parser.parse_args()
    
    ports: Dict[str, int] = yaml.load(open(args.config, 'r'), Loader=yaml.FullLoader)
    
    try:
        os.chdir(SERVICES_PATH)
    except Exception as exc:
        print(f"Is main.py in right directory? \n{exc}")

    main(args, ports)
