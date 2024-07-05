#!/usr/bin/env python

import os
from pathlib import Path
import sys
import time
from flask import Flask, flash, request, redirect, url_for, render_template
import subprocess

from jinja2 import Template
import codecs

# Not used but might be useful with modification
def cleanup():
    print('cleanup!')
    snakemake_clean_cmd = 'snakemake --cores all clean'
    snakemake_clean_cmd = snakemake_clean_cmd.split()
    subprocess.run(snakemake_clean_cmd, shell=False)

def kill():
    print('Killing PID!')
    snakemake_kill_cmd = 'snakemake --cores all kill'
    snakemake_kill_cmd = snakemake_kill_cmd.split()
    subprocess.run(snakemake_kill_cmd, shell=False)

def runner():
    print("running!")
    time.sleep(10)
    return 1


# Setting up Flask
script_path = os.path.abspath(os.path.dirname(__file__)) #os.path.realpath(__file__)
FASTQ_FOLDER = os.path.join(script_path, 'snakemake-qiime-edna2','fastq_data')
RUN_LOG_FILE = os.path.join(script_path, 'snakemake-qiime-edna2','logs', 'runlog.txt')
DATABASE_FOLDER = os.path.join(script_path, 'snakemake-qiime-edna2', 'database',
                               'qiime2-qza')

#STATIC_FOLDER = os.path.join(os.getcwd(), 'static')
STATIC_FOLDER = os.path.join(script_path, 'static')
#print(FASTQ_FOLDER)

app = Flask(__name__, static_url_path=STATIC_FOLDER, static_folder=STATIC_FOLDER)
app.secret_key = "secret_key"

# home page
@app.route('/')
def index():
    # kill any hanging processes and cleanup
    kill()
    cleanup()
    # Not used but might be useful with modification
    #setup(script_path)
    return render_template('index.html')

@app.route('/infer')
# upload_image
def upload():
    print("/infer")
    return redirect(url_for('edit_config'))

# config
@app.route('/config', methods=['GET', 'POST'])
def edit_config():
    if request.method == 'POST':
        data = {
                'prob':request.form['prob'],
                }
        print(data)
        config_path = script_path + '/config-template.yaml'
        with open(config_path) as rf:
            template = Template(rf.read(), trim_blocks=True)
        render_file = template.render(data)
        config_out_path = script_path + '/config.yaml'
        outfile = codecs.open(config_out_path, 'w', 'utf-8')
        outfile.write(render_file)
        outfile.close()
        # goto the pipeline running page
        return redirect(url_for('running'))
    print('called edit config')
    return render_template('config.html')

# done
@app.route('/done')
def done():
    # insert logic to check that megadetector work
    f_path = Path("/project/megadetector")

    if f_path.is_dir():
        return render_template('done.html')
    else:
        return render_template('done-fail.html')

@app.route('/running')
def running():
    return render_template('running.html')

@app.route('/pipeline')
def pipeline():
    snakemake_run_cmd = 'snakemake --cores all all'
    snakemake_run_cmd = snakemake_run_cmd.split()
    subprocess.run(snakemake_run_cmd, shell=False)
    #zip_cmd = 'zip -FSr %s/static/results.zip %s/snakemake-qiime-edna2'%(script_path,script_path)
    #zip_cmd = zip_cmd.split()
    #subprocess.run(zip_cmd, shell=False)
    return "done running"

if __name__ == "__main__":
	app.debug = True
	port = 5000 
	app.run(host="0.0.0.0", debug=True, port=port)
