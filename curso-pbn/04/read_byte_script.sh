#
bin=/usr/bin/cat         # binario a ser lido byte a byte
size=$(stat -c %s $bin)  # tamanho em bytes do arquivo
> minimo                 # cria novo arquivo
for ((n = 0; n <= size; n++)); do
    dd if=$bin of=minimo bs=1 count=1 skip=$n oflag=append conv=notrunc status=none 2>/dev/null
    min=$(file minimo)
    [[ $min != $prev ]] && echo "$n bytes: $min"
    prev=$min
done

