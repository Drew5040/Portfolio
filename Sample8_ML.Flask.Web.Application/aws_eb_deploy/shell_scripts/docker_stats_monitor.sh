#!/bin/bash

declare -A max_cpu
declare -A max_cpu
declare -A min_cpu
declare -A max_mem
declare -A min_mem

for container_id in $(docker ps -q); do
    max_cpu["$container_id"]=0
    min_cpu["$container_id"]=100
    max_mem["$container_id"]=0
    min_mem["$container_id"]=999999
done

while true; do
    for container_id in $(docker ps -q); do
        stats=$(docker stats --no-stream --format "{{.Container}} {{.Name}} {{.CPUPerc}} {{.MemUsage}}" "$container_id")
        container_name=$(echo "$stats" | awk '{print $2}')
        cpu=$(echo "$stats" | awk '{print $3}' | sed 's/%//')
        mem=$(echo "$stats" | awk '{print $4}' | sed 's/[^0-9.]//g')

        # Update max values
        if (( $(echo "$cpu > ${max_cpu[$container_id]}" | bc -l) )); then
            max_cpu["$container_id"]=$cpu
        fi
        if (( $(echo "$mem > ${max_mem[$container_id]}" | bc -l) )); then
            max_mem["$container_id"]=$mem
        fi

        # Update min values
        if (( $(echo "$cpu < ${min_cpu[$container_id]}" | bc -l) )); then
            min_cpu["$container_id"]=$cpu
        fi
        if (( $(echo "$mem < ${min_mem[$container_id]}" | bc -l) )); then
            min_mem["$container_id"]=$mem
        fi
    done

    # Print the header
    printf "%-15s %-20s %-10s %-10s %-15s %-15s\n" "Container ID" "Name" "Max CPU %" "Min CPU %" "Max MEM (MiB)" "Min MEM (MiB)"

    # Print the stats for each container
    for container_id in "${!max_cpu[@]}"; do
        container_name=$(docker inspect --format '{{.Name}}' "$container_id" | cut -c 2-)
        printf "%-15s %-20s %-10.2f %-10.2f %-15.2f %-15.2f\n" "$container_id" "$container_name" "${max_cpu["$container_id"]}" "${min_cpu["$container_id"]}" "${max_mem["$container_id"]}" "${min_mem["$container_id"]}"
    done

    sleep 5
done
