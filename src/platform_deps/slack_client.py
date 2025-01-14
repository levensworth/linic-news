import httpx


class SlackClient:
    def __init__(self, url: str) -> None:
        self._url = url
        self.__transport = httpx.AsyncHTTPTransport(retries=3)

    async def send_alert(self, payload: str) -> None:
        async with httpx.AsyncClient(transport=self.__transport) as client:
            result = await client.post(
                self._url,
                json={"text": payload},
            )
            if result.is_error:
                raise Exception(f"Got error from api => {result.text}")
