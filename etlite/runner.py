# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Edward Lau <elau1004@netscape.net>
# Licensed under the MIT License.
#

import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group( context_settings=CONTEXT_SETTINGS )
@click.version_option(version='0.1.0')
def start():
    pass


@start.command()
@click.option('--debug' ,type=bool ,default=False ,help='Enable debug logging.')
@click.argument('job_code')  # add the name argument
@click.argument('job_desc')  # add the desc argument
def install(**kwargs):
    print( "Install:")
    print( f"Job_Code=  {kwargs['job_code']}")
    print( f"Job_Desc=  {kwargs['job_desc']}")
    print( f"Debugging= {kwargs['debug']}")
    pass

def _abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()

@start.command()
@click.option('--debug' ,default=False ,help='Enable debug logging.')
@click.confirmation_option(prompt='Are you sure you want to uninstall this job?')
@click.argument('job_code')  # add the name argument
def uninstall(**kwargs):
    print( "UnInstall:")
    print( f"Job_Code=  {kwargs['job_code']}")
    print( f"Debugging= {kwargs['debug']}")
    pass


@start.command()
@click.option('--debug' ,default=False ,help='Enable debug logging.')
@click.argument('job_dag')  # add the dag argument
def run(**kwargs):
    print( "Run:")
    print( f"Job_Dag=   {kwargs['job_dag']}")
    print( f"Debugging= {kwargs['debug']}")
    pass

if __name__ == '__main__':
    start()
