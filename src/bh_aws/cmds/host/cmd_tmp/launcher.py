#!/usr/bin/env python3
from pathlib import Path

from bh_aws import tmpname

USER_DATA_DIR=Path(__file__).parent/'user-data'

def template4version(version='2'):
    TEMPLATE_ID="lt-0379c2edd4f580d9b"
    return f"LaunchTemplateId={TEMPLATE_ID},Version={version}"

class Launcher:
    class EXC(BaseException): pass
    class EXC_userdata(EXC): pass
    def __init__(self
        , profile='showme'
        , dry=False
        , userdata = 'ubuntu'
        , template = '2'
        ):
        self._profile = profile
        self._dry = dry
        self._userdata = USER_DATA_DIR/userdata
        self._template = template
        if not self._userdata.exists():
            raise self.EXC_userdata
    def tag_specifications(self):
         tags="[{Key=Name,Value=%s}]" % tmpname()
         return f"ResourceType=instance,Tags={tags}"
    def launch_template(self):
        return template4version(self._template)
        #return LAUNCH_TEMPLATE
    def profile(self):
        return self._profile
    def user_data(self):
        return f"file://{self._userdata}"
    def DRY_RUN(self):
        return self._dry and "--dry-run" or ""
    def _cmdline(s):
        line= f"""
        aws ec2 run-instances
            --profile {s.profile()}
            --launch-template {s.launch_template()}
            --tag-specifications {s.tag_specifications()}
            --user-data {s.user_data()}
            {s.DRY_RUN()}
        """
        return line

