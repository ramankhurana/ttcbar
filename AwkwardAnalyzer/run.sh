for ifile in `less rootfiles.txt`
do 
python ttc_analyzer.py /eos/cms/store/group/phys_top/ExtraYukawa/2018/ $ifile
done
