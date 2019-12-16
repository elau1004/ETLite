# -*- coding: utf-8 -*-
#MIT License
#
#Copyright (c) 2019 Edward Lau
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

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
