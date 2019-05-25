#!/bin/bash
# File              : make_tags.sh
# Author            : zcy
# Date              : 2019-03-16 12:16:44
# Last Modified Date: 2019-05-21 11:11:25

#20181111 by chew

CUR_PATH=$(cd "$(dirname "$0")"; pwd)

TAGS_DIR="'${CUR_PATH}/' \
"

SEARCH="'*.h' \
'*.c' \
'*.cc' \
'*.cpp' \
'*.go' \
'*.py' \
"

FILES_CNT=0
TAGS_FILES="${CUR_PATH}/tags.files"

CTAGS_CMD="ctags --c++-kinds=+p+l+x+c+d+e+f+g+m+n+s+t+u+v --fields=+liazKS --extra=+q -L" 
CSCOPE_CMD="cscope -bkq -i"
CLEAN_CMD="rm -f cscope.* && rm -f tags && rm -f ${TAGS_FILES}"


GO_OK=true

## go project must under '${GOPATH}/src'
GO_SRC="${CUR_PATH##*/}"
GO_PATH="${CUR_PATH%/*}"
while [[ ${GO_SRC} != "" ]]
do
    if [[ ${GO_SRC} == "src" ]]; then
        break
    fi

    GO_SRC="${GO_PATH##*/}"
    GO_PATH="${GO_PATH%/*}"
done

## whether GO_PATH already set to GO ENV
GO_ENV_PATH=false
GO_ENV_PATHS=(${GOPATH//:/ })
for gopath in ${GO_ENV_PATHS[@]}
do
    if [[ ${gopath} == ${GO_PATH} ]]; then
        GO_ENV_PATH=true
        break
    fi
done


echo "Updating tags ..."
 if [[ $# == 1 && $1 == "clean" ]]; then
    echo "=== ${CLEAN_CMD} ==="
    time ${CLEAN_CMD}
 else 
    if [[ $# == 1 && $1 == "go" ]]; then
        if [[ ${GO_SRC} != "src" ]]; then
            GO_OK=false
            echo " '${CUR_PATH}' is not under a 'src' dir"
        else
            if [[ ${GO_ENV_PATH} == false ]]; then
                GO_OK=false
                echo " '${GO_PATH}' not in 'GOPATH:${GOPATH}'"
                echo " try 'export GOPATH=${GOPATH}:${GO_PATH}'"
            fi 
        fi
    fi


    if [[ ${GO_OK} == true ]]; then
        rm -f ${TAGS_FILES}
        echo "${SEARCH}" 
        for tpath in ${TAGS_DIR[@]}
        do
            echo "Find files from ${tpath}" 
            for tfile in ${SEARCH[@]}
            do
                eval find ${tpath} -name ${tfile} -print >> ${TAGS_FILES}
            done
        done
       
        echo "== ${CSCOPE_CMD} ${TAGS_FILES} =="
        time ${CSCOPE_CMD} ${TAGS_FILES}

        echo "== ${CTAGS_CMD} ${TAGS_FILES} =="
        time ${CTAGS_CMD} ${TAGS_FILES}

        FILES_CNT=`awk 'END{print NR}' ${TAGS_FILES}`
    fi
 fi
echo "${FILES_CNT} Update complete."

