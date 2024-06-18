configfile: "config.yaml"

rule megadetector:
    input:
    output:
    params:
        thresh=params['md-threshold']
    shell:
        'python {params.thresh}'    
