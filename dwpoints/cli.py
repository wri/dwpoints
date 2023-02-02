import os
import re
import json
import click
from shutil import copyfile, move
import dwpoints.config as config
import dwpoints.constants as c
import dwpoints.core as core
#
# CONFIG CONSTANTS
#
NOISY=config.get('noisy')

#
# PUBLIC
#
@click.group()
@click.option('--noisy',default=NOISY,help='print info and warning messages',type=bool)
@click.pass_context
def cli(ctx,noisy):
    ctx.obj={}
    ctx.obj['noisy']=noisy



@click.command(name='run',help='generate dwpoints file')
@click.argument('src')
@click.argument('dest',default=False)
@click.option(
    '--year',
    default=c.YEAR,
    help='year to generate squashes',
    type=int)
@click.option(
    '--lon',
    default=c.LON_COLUMN,
    help='name of longitude column')
@click.option(
    '--lat',
    default=c.LAT_COLUMN,
    help='name of latitude column')
@click.option(
    '--min_crop',
    default=c.MIN_CROP,
    help='minimum number of crop months for crop-rule',
    type=int)
@click.option(
    '--min_cropish',
    default=c.MIN_CROPISH,
    help='minimum number of cropish months for crop-rule',
    type=int)
@click.option(
    '--noisy',
    default=c.NOISY,
    type=bool)
@click.option(
    '--squash',
    default=None,
    help='comma deliminated string of squash_keys (w/o spaces)')
@click.pass_context
def run(ctx,src,dest,year,lon,lat,min_crop,min_cropish,noisy,squash):
    core.run(src,dest,year,lon,lat,min_crop,min_cropish,noisy,squash)



@click.command(name='config',help='generate config file')
@click.option(
    '--year',
    default=c.YEAR,
    help='year to generate squashes',
    type=int)
@click.option(
    '--lon',
    default=c.LON_COLUMN,
    help='name of longitude column')
@click.option(
    '--lat',
    default=c.LAT_COLUMN,
    help='name of latitude column')
@click.option(
    '--min_crop',
    default=c.MIN_CROP,
    help='minimum number of crop months for crop-rule',
    type=int)
@click.option(
    '--min_cropish',
    default=c.MIN_CROPISH,
    help='minimum number of cropish months for crop-rule',
    type=int)
@click.option(
    '--noisy',
    default=c.NOISY,
    type=bool)
@click.option(
    '--squash',
    default=None,
    help='comma deliminated string of squash_keys (w/o spaces)')
@click.option(
    '--force',
    default=False,
    help='if true overwrite existing config',
    type=bool)
def generate_config(year,lon,lat,min_crop,min_cropish,noisy,squash,force):
    config.generate(year,lon,lat,min_crop,min_cropish,noisy,squash,force)


#
# MAIN
#
cli.add_command(run)
cli.add_command(generate_config)


if __name__ == '__main__':
    cli()
