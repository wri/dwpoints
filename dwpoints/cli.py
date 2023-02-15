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
YEAR=config.get('year')
MONTH=config.get('month')
DAY=config.get('day')
DURATION=config.get('duration')
DURATION_TYPE=config.get('duration_type')
LON_COLUMN=config.get('lon')
LAT_COLUMN=config.get('lat')
MIN_CROP=config.get('min_crop')
MIN_CROPISH=config.get('min_cropish')
DEST_PREFIX=config.get('prefix')
ACCURACY_DEST_PREFIX=config.get('acc_prefix')
CONFUSION_DEST_PREFIX=config.get('cm_prefix')
NOISY=config.get('noisy')
NORMALIZE_CM=config.get('normalize')



#
# PUBLIC
#
@click.group()
@click.option('--noisy',default=NOISY,help='print info and warning messages',type=bool)
@click.pass_context
def cli(ctx,noisy):
    ctx.obj={}
    ctx.obj['noisy']=noisy



@click.command(name='annual',help='generate aggregate dwpoints file for 1 year')
@click.argument('src')
@click.argument('dest',default=False)
@click.option(
    '--year',
    default=YEAR,
    help='year to generate squashes',
    type=int)
@click.option(
    '--lon',
    default=LON_COLUMN,
    help='name of longitude column')
@click.option(
    '--lat',
    default=LAT_COLUMN,
    help='name of latitude column')
@click.option(
    '--min_crop',
    default=MIN_CROP,
    help='minimum number of crop months for crop-rule',
    type=int)
@click.option(
    '--min_cropish',
    default=MIN_CROPISH,
    help='minimum number of cropish months for crop-rule',
    type=int)
@click.option(
    '--prefix',
    default=DEST_PREFIX,
    help='if no dest given, name file `{prefix}.<year>.src-filename.csv`')
@click.option(
    '--noisy',
    default=NOISY,
    type=bool)
@click.option(
    '--squash',
    default=None,
    help='comma deliminated string of squash_keys (w/o spaces)')
@click.pass_context
def annual(ctx,src,dest,year,lon,lat,min_crop,min_cropish,prefix,noisy,squash):
    core.annual(
        src=src,
        dest=dest,
        year=year,
        lon=lon,
        lat=lat,
        min_crop=min_crop,
        min_cropish=min_cropish,
        prefix=prefix,
        noisy=noisy,
        squash=squash)



@click.command(name='aggregate',help='generate aggregate dwpoints file for start-date and duration')
@click.argument('src')
@click.argument('dest',default=False)
@click.option(
    '--year',
    default=YEAR,
    help='start year to generate squashes',
    type=int)
@click.option(
    '--month',
    default=MONTH,
    help='start month to generate squashes',
    type=int)
@click.option(
    '--day',
    default=DAY,
    help='start day to generate squashes',
    type=int)
@click.option(
    '--start_date',
    default=None,
    help='start-date: overides y/m/d above',
    type=str)
@click.option(
    '--duration',
    default=DURATION,
    help='number of "duration_type" units till end-date',
    type=int)
@click.option(
    '--duration_type',
    default=DURATION_TYPE,
    help='one of "year", "month", "day"',
    type=str)
@click.option(
    '--lon',
    default=LON_COLUMN,
    help='name of longitude column')
@click.option(
    '--lat',
    default=LAT_COLUMN,
    help='name of latitude column')
@click.option(
    '--prefix',
    default=DEST_PREFIX,
    help='if no dest given, name file `{prefix}.<start-date>.src-filename.csv`')
@click.option(
    '--noisy',
    default=NOISY,
    type=bool)
@click.option(
    '--squash',
    default=None,
    help='comma deliminated string of squash_keys (w/o spaces)')
@click.pass_context
def aggregate(ctx,src,dest,year,month,day,start_date,duration,duration_type,lon,lat,prefix,noisy,squash):
    core.aggregate(
        src=src,
        dest=dest,
        year=year,
        month=month,
        day=day,
        start_date=start_date,
        duration=duration,
        duration_type=duration_type,
        lon=lon,
        lat=lat,
        prefix=prefix,
        noisy=noisy,
        squash=squash)


@click.command(name='accuracy',help='generate accuracy results')
@click.argument('src')
@click.argument('label')
@click.option(
    '--prefix',
    default=ACCURACY_DEST_PREFIX,
    help='output file is `{prefix}.src-filename.csv`')
@click.option(
    '--noisy',
    default=NOISY,
    type=bool)
@click.option(
    '--squash',
    default=None,
    help='comma deliminated string of squash_keys (w/o spaces)')
@click.option(
    '--run_type',
    default=None,
    help='"aggregate" if not performing annual analysis')
def accuracy(src,label,prefix,noisy,squash,run_type):
    core.accuracy(src=src,label=label,prefix=prefix,noisy=noisy,squash=squash,run_type=run_type)


@click.command(name='confusion',help='generate confusion matrices for specific squashes')
@click.argument('src')
@click.argument('label')
@click.option(
    '--prefix',
    default=CONFUSION_DEST_PREFIX,
    help='output files are `{prefix}.{squash_col}.src-filename.csv`')
@click.option(
    '--noisy',
    default=NOISY,
    type=bool)
@click.option(
    '--squash',
    default=None,
    help='comma deliminated string of squash_keys (w/o spaces)')
@click.option(
    '--normalize',
    default=NORMALIZE_CM,
    type=bool,
    help='normalize confusion matrix')
@click.option(
    '--run_type',
    default=None,
    help='"aggregate" if not performing annual analysis')
def confusion(src,label,prefix,noisy,squash,normalize,run_type):
    core.confusion(
        src=src,
        label=label,
        prefix=prefix,
        noisy=noisy,
        squash=squash,
        normalize=normalize,
        run_type=run_type)


@click.command(name='config',help='generate config file')
@click.option(
    '--year',
    default=YEAR,
    help='year to generate squashes',
    type=int)
@click.option(
    '--lon',
    default=LON_COLUMN,
    help='name of longitude column')
@click.option(
    '--lat',
    default=LAT_COLUMN,
    help='name of latitude column')
@click.option(
    '--min_crop',
    default=MIN_CROP,
    help='minimum number of crop months for crop-rule',
    type=int)
@click.option(
    '--min_cropish',
    default=MIN_CROPISH,
    help='minimum number of cropish months for crop-rule',
    type=int)
@click.option(
    '--prefix',
    default=DEST_PREFIX,
    help='if not dest given, name file `{prefix}.src-filename.csv`')
@click.option(
    '--noisy',
    default=NOISY,
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
def generate_config(year,lon,lat,min_crop,min_cropish,prefix,noisy,squash,force):
    config.generate(year,lon,lat,min_crop,min_cropish,prefix,noisy,squash,force)


#
# MAIN
#
cli.add_command(annual)
cli.add_command(aggregate)
cli.add_command(accuracy)
cli.add_command(confusion)
cli.add_command(generate_config)



if __name__ == '__main__':
    cli()
