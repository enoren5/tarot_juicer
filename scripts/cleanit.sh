#!/bin/sh
# uses sed to strip leading whitespace and blank lines
# and awk to filer out only lines with relevant data
# why not python? this is faster and more efficient
# sed 's/\s\{2,\}//g; /^[[:space:]]*$/d' $1 | awk '/models/'
awk '
BEGIN { FS = "=" }
{
        if ($1 ~ "models.Model"){
                print $0;
                match($0, "[A-Z][a-z]+[[:punct:]]");
                model = substr($0,RSTART,RLENGTH - 1)
                if (prev_model != model) {
                        print "Model", model;
                        prev_mode = model
                }
        } else if (match($0, "models.[a-zA-Z]+[[:punct:]]") && !begin) {
                begin = 1
                field = $1
                split($2, tmp, ".")
                type = tmp[2]
                if (match($0, /models\.[A-Za-z]+\(.*\)/)) {
                        print field, substr($0, RSTART+7, RLENGTH-2)
                        begin = 0
                }
        } else if (begin) {
                type = type $0
                if ($0 ~ /.*\)$/) {
                        begin = 0
                        gsub(/\s{2,}/, " ", type)
                        print field, type
                        type = ""
                } 
        }
}' generators/models.py

