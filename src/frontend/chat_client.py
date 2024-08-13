import json
import requests


class ChatClient:
    def __init__(self, server_url, timeout=600):
        self.server_url = server_url
        self.timeout = timeout

    def stream(self, message, session_id):
        headers = {"Content-Type": "application/json"}
        data = {"message": message, "session_id": session_id}
        special_char = None

        try:
            with requests.post(
                f"{self.server_url}/stream",
                headers=headers,
                data=json.dumps(data),
                timeout=self.timeout,
                stream=True,
            ) as chunked_response:
                for loop_chunk in chunked_response.iter_content(chunk_size=20):
                    chunk = loop_chunk

                    if special_char:
                        chunk = special_char + chunk
                        special_char = None

                    if chunk.endswith(b"\xc2") or chunk.endswith(b"\xc3"):
                        special_char = chunk[-1:]
                        yield chunk[:-1].decode("utf-8")
                    else:
                        yield chunk.decode("utf-8")

        except Exception as e:
            print(e)
            yield "I'm sorry, but I'm having trouble processing your request. Please try again."
