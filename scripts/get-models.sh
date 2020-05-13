#!/bin/sh
# uses sed to strip leading whitespace and blank lines
# and awk to filer out only lines with relevant data
# why not python? this is faster and more efficient
# sed 's/\s\{2,\}//g; /^[[:space:]]*$/d' $1 | awk '/models/'
awk '
BEGIN { FS = "="
        OFS = "#"
}
{
        if ($1 ~ "models.Model"){
                match($0, "[A-Z][a-z]+[[:punct:]]");
                model = substr($0,RSTART,RLENGTH - 1)
                if (prev_model != model) {
                        print "Model", model;
                        prev_mode = model
                }
        } else if (match($0, "models.[a-zA-Z]+[[:punct:]]") && !begin) {
                begin = 1
                field = substr($1, 0, length($1) - 1)
                split($2, tmp, ".")
                type = tmp[2]
                if (match($0, /models\.[A-Za-z]+\(.*\)/)) {
                        typespec = substr($0, RSTART+7, RLENGTH-2)
                        split(typespec, tmp, /\(/)
                        spec = substr(tmp[2], 0, length(tmp[2]) -1)
                        gsub(/,\s/, ",", spec)
                        if (spec)
                                print field, tmp[1], spec
                        else
                                print field, tmp[1]
                        begin = 0
                }
        } else if (begin) {
                type = type $0
                if ($0 ~ /.*\)$/) {
                        begin = 0
                        gsub(/\s{2,}/, "", type)
                        gsub(/,\s/, ",", type)
                        print field, type
                        type = ""
                } 
        }
}' $1 | tr -d '(' | tr -d ')' | sed 's/^\s*//'

