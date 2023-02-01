import os
import re
import json
import click
from shutil import copyfile, move
import dwpoints.core as core
import dwpoints.config as config
import dwpoints.constants as c
#
# CONFIG CONSTANTS
#
# PORT=config.get('port')
# REMOTE_PATH=config.get('remote_path')
# SSH_KEY=config.get('ssh_key')
# NOISY=config.get('noisy')
# AUTO_INIT=config.get('auto_init')

# #
# # PUBLIC
# #
# @click.group()
# @click.option('--noisy',default=NOISY,help='print info and warning messages',type=bool)
# @click.pass_context
# def cli(ctx,noisy):
#     ctx.obj={}
#     ctx.obj['noisy']=noisy


# @click.command(help='turn off dwpoints')
# @click.pass_context
# def off(ctx):
#     core.off(noisy=ctx.obj['noisy'])


# @click.command(help='remove sftp-config for ident')
# @click.argument('ident')
# @click.pass_context
# def remove(ctx,ident):
#     core.remove(ident,noisy=ctx.obj['noisy'])


# @click.command(help='initialize a new sftp-config')
# @click.argument('ident')
# @click.pass_context
# def init(ctx,ident):
#     core.init(ident,noisy=ctx.obj['noisy'])  


# @click.command(name='open',help='open current port for the current remote')
# @click.argument('port',default=PORT)
# @click.pass_context
# def open_port(ctx,port):
#     core.open_port(port,noisy=ctx.obj['noisy'])


# @click.command(help='print current remote ident')
# @click.pass_context
# def current(ctx):
#     core.current()


# @click.command(help='create and initialize new remote config')
# @click.argument('ident')
# @click.argument('ip')
# @click.argument('remote_path',default=REMOTE_PATH)
# @click.argument('ssh_key',default=SSH_KEY)
# @click.argument('auto_init',default=AUTO_INIT,type=bool)
# @click.option(
#     '--force',
#     default=False,
#     help='if true overwrite existing config',
#     type=bool)
# @click.pass_context
# def create(ctx,ident,ip,remote_path,ssh_key,auto_init,force):
#     core.create(
#         ident,
#         ip,
#         remote_path,
#         ssh_key,
#         auto_init,
#         noisy=ctx.obj['noisy'],
#         force=force)


# @click.command(name='list',help='list available remote configs')
# def list_remotes():
#     core.list_remotes()


# @click.command(name='config',help='generate config file')
# @click.argument('port',default=c.PORT)
# @click.argument('remote_path',default=c.REMOTE_PATH)
# @click.argument('ssh_key',default=c.SSH_KEY)
# @click.argument('noisy',default=c.NOISY)
# @click.argument('auto_init',default=c.AUTO_INIT,type=bool)
# @click.option(
#     '--force',
#     default=False,
#     help='if true overwrite existing config',
#     type=bool)
# def generate_config(port,remote_path,ssh_key,noisy,auto_init,force):
#     config.generate(port,remote_path,ssh_key,noisy,auto_init,force)


# #
# # MAIN
# #
# cli.add_command(init)
# cli.add_command(off)
# cli.add_command(create)
# cli.add_command(current)
# cli.add_command(open_port)
# cli.add_command(list_remotes)
# cli.add_command(generate_config)
# cli.add_command(remove)


# if __name__ == '__main__':
#     cli()
