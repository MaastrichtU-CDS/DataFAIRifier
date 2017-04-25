cwlVersion: v1.0
class: CommandLineTool
baseCommand: /Users/johan/localApps/d2rq-0.8.3-dev/dump-rdf
arguments:
    - prefix: "--verbose"
inputs:
    d2r_base_uri:
        type: string
        inputBinding:
            position: 1
            prefix: -b
    d2r_output_file:
        type: ["null", File]
        inputBinding:
            position: 2
            prefix: -o
    d2r_mapping_file:
        type: ["null", File]
        inputBinding:
            position: 3
outputs:
    message_out:
        type: stdout
