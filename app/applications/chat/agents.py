from cent import Client, CentException

from django.conf import settings


class CentrifugoAgent:
    def __init__(self) -> None:
        ws_url = f'http://{settings.CENTRIFUGO_IP_ADDRESS}'
        api_key = f'{settings.CENTRIFUGO_API_KEY}'
        self.client = Client(ws_url, api_key=api_key, timeout=1)

    def publish(self, channel: str, message: dict) -> bool:
        try:
            self.client.publish(channel, message)
            success_result = True
        except CentException:
            success_result = False
        return success_result

    def publish_multiple(self, params_list):
        for params in params_list:
            self.client.add('publish', params)
        try:
            self.client.send()
            success = True,
        except CentException:
            success = False
        return success
