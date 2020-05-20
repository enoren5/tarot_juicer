#!/usr/bin/awk -f
BEGIN {
        FS = " = "
        OFS = "#"
}
{
        # check if we are dealing with a model name i.e. models.Model
        if ($1 ~ "Model"){
                match($1, /[A-Za-z]+\(/);
                model = substr($1, RSTART, RLENGTH - 1)
                if (prev_model != model) {
                        # discovered new model
                        print "Model", model;
                        prev_model = model
                }
        } else {
                if (NF == 2 && index($0, "models") > 0){
                        #dealing with field definition
                        begin = 1
                        field_name = $1
                        split($2, tmp, /\./)
                        match(tmp[2], /[A-Za-z]+\(/)
                        field_type = substr(tmp[2], RSTART, RLENGTH - 1)
                        match(tmp[2], /\(.+\)/)
                        # minute the two parens, inside is single option
                        optn = substr(tmp[2], RSTART + 1, RLENGTH - 2)
                        if (length(optn) > 0){
                                sub(/^\s+/, "", field_name)
                                print field_name, field_type, optn 
                                begin = 0
                        } else if (index(tmp[2], ")") > 0){
                                # closing paren but no options
                                sub(/^\s+/, "", field_name)
                                print field_name, field_type, ""
                                begin = 0 # done, rdy for next
                        } else {
                                # not only option, more to come
                                match(tmp[2], /\(.+$/)
                                optns = substr(tmp[2], RSTART + 1, RLENGTH - 1)
                                sub(/^\s+/, "", optns)                
                                gsub(/\s{2,}/, "", optns)
                                sub(/,\s/, ",", optns)
                                # print $1, field_type, "more to come", optns
                        }
                        
                } else {
                        # dealing with more options
                        if (index($0, ")") > 0 && begin != 0){
                                # end of additional options
                                match($0, /[^\)]*/)
                                aditional = substr($0, RSTART, RLENGTH)
                                optns = optns aditional 
                                sub(/^\s+/, "", optns)
                                gsub(/\s{2,}/, "", optns)
                                sub(/^\s+/, "", field_name)
                                sub(/,\s/, ",", optns)
                                print field_name, field_type, optns
                                begin = 0 # done, next
                        } else {
                                optns = optns $0
                                sub(/^\s+/, "", optns)                
                                gsub(/\s{2,}/, "", optns)
                                sub(/,\s/, ",", optns)
                        }
                }
                        
        }
}
