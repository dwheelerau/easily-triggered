configfile: "config.yaml"

rule all:
    input:    
        "/project/megadetector-summary.txt"

rule megadetector:
    output:
        "/project/project.json"
    params:
        thresh=config["md-threshold"],
        model=config["md-model"]
    shell:
        "python -m megadetector.detection.run_detector_batch {params.model} /project/ {output} --recursive --threshold {params.thresh} --checkpoint_frequency 1000"

rule json_to_csv:
    input:
        "/project/project.json"
    output:
        "/project/project.csv"
    params:
        thresh=config["md-threshold"]
    shell:
        "python scripts/json_to_csv.py -i {input} -t {params.thresh}"

rule sort_md:
    input:
        "/project/project.csv"
    output:
        "/project/megadetector-summary.txt"
    params:
        outdir="/project/megadetector/"
    shell:
        "mkdir -p {params.outdir} && python scripts/collect_image_files.py -b /project/ -i {input} -o {params.outdir} | tee {output}"

rule clean:
    shell:
        "rm -f /project/project.* && rm -rf /project/megadetector && rm -f /project/megadetector-summary.txt"

rule kill:
    shell:
        "for pid in $(ps -ef | grep 'megadetector' | awk '{{print $2}}'); do kill -9 $pid; done"

