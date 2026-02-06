import click

from infograph.svc.api_service import APIService


@click.command()
@click.option("--host", default="0.0.0.0", show_default=True)
@click.option("--port", default=8000, show_default=True, type=int)
def main(host: str, port: int) -> None:
    """Start the Infograph API service."""
    service = APIService()
    service.run(host=host, port=port)


if __name__ == "__main__":
    main()
