import argparse
import logging
import sys

from service_api.app import app


logger = logging.getLogger(__name__)


def parse_args(args):

    parser = argparse.ArgumentParser(description="Movie list api", add_help=False)
    parser.add_argument("--help", action="help", help="movie list api help message")

    subparsers = parser.add_subparsers(dest="command")

    sparser = subparsers.add_parser("runserver", add_help=False, help="run server")
    sparser.add_argument("-h", "--host", dest="host", default="0.0.0.0", type=str, help="Host address")
    sparser.add_argument("-p", "--port", dest="port", default=8000, type=int, help="Host port")

    return parser.parse_args(args=args)


def runserver(host, port):
    """Setups params and run server.

    Args:
        host (str): Host where server will be running.
        port (str): Port where server will be running.

    """
    app.run(host=host, port=port)


def main(args=None):

    parsed_args = parse_args(args or sys.argv[1:])

    if parsed_args.command == "runserver":
        runserver(parsed_args.host, parsed_args.port)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(
            "Unexpected exception occurred. Service is going to shutdown. Error message: {}".format(e),
            extra={"error_message": e},
        )
        exit(1)
    finally:
        logger.info("Service stopped.")
