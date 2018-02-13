train_ndx=train_ndx
key_ndx=key_ndx
trial_ndx=trial_ndx
>${trial_ndx}

cut -d" "  -f1 ${train_ndx} | sort | uniq > tmpa
cut -d" "  -f2 ${key_ndx} | sort | uniq > tmpb

while read mdl
do
    while read seg
    do
       spkr=`echo ${seg} | awk -F"[-_]" '{print $5}'`
       echo ${spkr}
       if [ "$spkr" == "$mdl" ] ; then      
           echo ${mdl} ${seg} target >>  ${trial_ndx}
       else
           echo ${mdl} ${seg} nontarget >>  ${trial_ndx}
       fi
    done < tmpb
done < tmpa
