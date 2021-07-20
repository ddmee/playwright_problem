# stdlib
import os
from urllib.parse import urljoin


FIELD_REQUIRED = "text='[This field is required.]'"
SUBMIT_INPUT = "text=Submit"
CANCEL_INPUT = "text=Cancel"


def server_url(sub_path:str='') -> str:
    base = f"{os.environ['PROTOCOL']}://{os.environ['HOST']}:{os.environ['PORT']}/"
    return urljoin(base, sub_path)
