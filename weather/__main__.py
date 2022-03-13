import typer

from weather import cache, html_requests, parser
from weather.config import BASE_URL


@cache.timed_cache(['city'])
def check_weather(city: str) -> str:
    if not city:
        raise RuntimeError('City is not specified.')

    url = BASE_URL + city
    html = html_requests.get(url)
    return parser.parse_html(html)


def main(
    city: str = typer.Argument(
        None, help='The city where you need to check the weather.'
    )
):
    try:
        degree = check_weather(city=city)
        typer.echo(f'The weather is: {degree}')
    except RuntimeError as error:
        typer.echo(error)


if __name__ == '__main__':
    typer.run(main)
