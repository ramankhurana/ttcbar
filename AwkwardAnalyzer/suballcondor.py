import os 

eospath="/eos/cms/store/group/phys_top/ExtraYukawa/2018/"
tosubmit="condor_test"
inputtextfile="tuples.txt"

os.system("ls -1 "+eospath+ " > "+inputtextfile)
#inputtextfile="skimfileslist/samplespplit/"

os.system("tar -cf python.tar python")
os.system("tar -cf pyfiles.tar *.py")
os.system("cp pyfiles.tar "+tosubmit)
os.system("cp python.tar "+tosubmit)
os.system("cp runanalysis.sh "+tosubmit)
os.system("cp requirements.txt "+tosubmit)



def filetolist(textfile):
    flist=[]
    for iline in open(textfile,'r'):
        flist.append(iline.rstrip())
    return flist

def createsubmitfile(filename):
    TEMP_SUB_FILE="""
    universe = vanilla
    request_memory = 8192
    Proxy_filename = x509up
    Proxy_path = /afs/cern.ch/user/k/khurana/private/$(Proxy_filename)
    request_cpus = 4
    +JobFlavour = "nextweek"
    executable = runanalysis.sh
    should_transfer_files = YES
    output = output_c/condor.$(Cluster).$(Process).out
    error = error_c/condor.$(Cluster).$(Process).err
    log = log_c/condor.$(Cluster).$(Process).log
    transfer_input_files = ./pyfiles.tar, python.tar, requirements.txt, runanalysis.sh
    on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)
    on_exit_hold = ( (ExitBySignal == True) || (ExitCode != 0) )
    on_exit_hold_reason = strcat("Job held by ON_EXIT_HOLD due to ",ifThenElse((ExitBySignal == True), "exit by signal",strcat("exit code ",ExitCode)), ".")
    periodic_release =  (NumJobStarts < 5) && ((CurrentTime - EnteredCurrentStatus) > (60*60))
    arguments =  """+eospath+"""/$(jobid) 2017 $(jobid) $(Proxy_path)
    queue jobid from """+filename +"""
    """
    
    fsub_out =  tosubmit+"/"+filename.split("/")[-1].replace(".root",".sub") 
    fsub=open(fsub_out,'w')
    fsub.write(TEMP_SUB_FILE)
    fsub.close()
    
    print ("condor_submit "+fsub_out)

    return 0 



#os.system("ls -1 "+inputtextfile+" >tmp.txt")
#sampleliist=filetolist("tmp.txt")
samplelist = filetolist(inputtextfile)
samplelist_fullpath = [eospath+"/"+i for i in samplelist]

for isample  in  samplelist_fullpath:
    print ("submitting jobs for: ",isample)
    createsubmitfile(isample)

