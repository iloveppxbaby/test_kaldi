pcm_dir=./pcm_data/

#wav_dir=./wav_data/new_data/
#wav_dir=./labeled/
#wav_dir=./test141/
wav_dir=./test300/
mkdir -p ${wav_dir}

while read line
do
    seg=`echo ${line} | cut -d"|" -f2`
    echo  $seg
   
    sox -t raw -e signed -b 16 -r 8000 ${pcm_dir}/$seg -t wav ${wav_dir}/${seg}.wav

done < test300.ndx
#done < test141.ndx
#done < split_pcm_ndx
#done < new.ndx

