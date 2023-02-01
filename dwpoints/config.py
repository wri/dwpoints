import os.path
import yaml
import dwpoints.utils as utils
import dwpoints.constants as c
#
# DEFALUTS 
#
_DEFAULTS={
    'port':c.PORT,
    'remote_path':c.REMOTE_PATH,
    'ssh_key':c.SSH_KEY,
    'noisy':c.NOISY,
    'auto_init':c.AUTO_INIT
}


#
# LOAD CONFIG
#
if os.path.exists(c.SUBLR_CONFIG_PATH):
    _CONFIG=yaml.safe_load(open(c.SUBLR_CONFIG_PATH))
else:
    _CONFIG={}


def get(key):
    """ get value
    """
    return _CONFIG.get(key,_DEFAULTS.get(key))


def generate(
        port=c.PORT,
        remote_path=c.REMOTE_PATH,
        ssh_key=c.SSH_KEY,
        noisy=c.NOISY,
        auto_init=c.AUTO_INIT,
        force=False):
    """ generate config file
    """
    config={
        'port':port,
        'remote_path':remote_path,
        'ssh_key':ssh_key,
        'noisy':noisy,
        'auto_init':auto_init }
    if not force and os.path.exists(c.SUBLR_CONFIG_PATH):
        utils.log(c.SUBLR_CONFIG_EXISTS,True,level="ERROR")
    else:
        with open(c.SUBLR_CONFIG_PATH,'w+') as file:
            file.write("# {}\n".format(c.SUBLR_CONFIG_COMMENT))
            file.write(yaml.safe_dump(config, default_flow_style=False))
        utils.log(c.SUBLR_CONFIG_CREATED,noisy)


