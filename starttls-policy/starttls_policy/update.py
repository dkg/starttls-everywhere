""" Util for updating local version of the policy file. """

try:
    import StringIO
except ImportError:
    from io import StringIO
import json
import pycurl

from starttls_policy import constants
from starttls_policy import policy

def _should_replace(old_config, new_config):
    return new_config.timestamp > old_config.timestamp

def _get_remote_data(url):
    buf = StringIO.StringIO()
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.WRITEFUNCTION, buf.write)
    curl.perform()
    curl.close()
    return buf.getvalue()

def update(remote_url=constants.POLICY_REMOTE_URL, filename=constants.POLICY_LOCAL_FILE):
    """ Fetches and updates local copy of the policy file with the remote file,
    if local copy is outdated. """
    data = _get_remote_data(remote_url)
    remote_config = policy.Config()
    remote_config.load_from_dict(json.loads(data))
    local_config = policy.Config(constants.POLICY_LOCAL_FILE)
    local_config.load()
    if _should_replace(local_config, remote_config):
        with open(filename, 'w+') as handle:
            handle.write(data)

if __name__ == "__main__":
    update()
