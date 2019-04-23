#!/bin/bash

baseurl="https://www.govinfo.gov/bulkdata/BILLS"
# wget --follow-ftp --header "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3" -U mozilla -H --page-requisites --directory-prefix=output --no-cookies -S -erobots=off -k --convert-links -r -l1  https://www.govinfo.gov/bulkdata/

flags=" --header \"accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3\" "
congress=(116 115 114 113)
session=(1 2)
houses=("hconres" "hjres" "hr" "hres" "s" "sconres" "sjres" "sres")

for con in "${congress[@]}"
do
	for ses in "${session[@]}"
	do
		for house in "${houses[@]}"
		do
			url="$baseurl/$con/$ses/$house/BILLS-$con-$ses-$house.zip"
			echo "$url"
			wget -nc $flags $url 
		done
	done
done