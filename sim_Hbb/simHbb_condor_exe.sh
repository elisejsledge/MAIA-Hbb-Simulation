#!/bin/bash
echo $HOSTNAME
echo $APPTAINER_NAME
echo $PWD
echo

echo "Sourcing setup scripts"
source /setup.sh
which ddsim
which Marlin
which k4run
type whizard

echo

echo "Simulating H->bb files in MAIA"
#export STASHCP=/cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/23/current/el8-x86_64/usr/bin/stashcp
#$STASHCP -d osdf:///scratch/ejsledge/detector-simulation/geometries/MuColl_10TeV_v0A/

ddsim --steeringFile sim_steer_GEN_CONDOR_Hbb.py


#ls
#echo "moving to scratch director"
#cd /scratch
#ls
echo

echo "Job complete"