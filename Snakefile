configfile: "config.yaml"

rule all:
    input:    
        "/project/yolov10-sort.log"

rule megadetector:
    output:
        "/project/project.json"
    params:
        thresh=config["md-threshold"],
        model=config["md-model"]
    shell:
        "python -m megadetector.detection.run_detector_batch {params.model} /project/ {output} --recursive --threshold {params.thresh}"

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

rule run_yolov10:
    input:
        "/project/megadetector-summary.txt"
    output:
        "/project/yolov10-summary.txt"
    params:
        save_images=config["create_images"],
        yolo_model=config["yolo-model"],
        yolo_conf=config["conf"],
        yolo_classes=config["classes"]
    shell:
        "for dir in /project/megadetector/animal/*; do outdir=$(basename $dir); "
        "yolo predict model={params.yolo_model} source=$dir project=/project/yolov10/$outdir "
        "save={params.save_images} save_txt=True save_conf=True classes={params.yolo_classes} "
        "conf={params.yolo_conf} | tee -a {output};done"

rule sort_yolov10:
    input:
        "/project/yolov10-summary.txt"
    output:
        "/project/yolov10-sort.log"
    params:
        all=config["collect_all_images"],
        sort_classes=config["sort_classes"],
        sort_thresh=config["sort_threshold"]
    shell:
        "python scripts/yolo_sort.py -t {params.sort_thresh} -b /project/yolov10/ "
        "-i /project/megadetector/animal -c {params.sort_classes} "
        "-o /project/yolo_sorted/ {params.all} | tee {output}"

rule clean:
    shell:
        "rm /project/project.* && rm -rf /project/megadetector && rm /project/megadetector-summary.txt "
        "rm -rf /project/yolov10 rm /project/yolov10-summary.txt"

