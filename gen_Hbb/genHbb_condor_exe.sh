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

echo "Simulating H->bb files"
export STASHCP=/cvmfs/oasis.opensciencegrid.org/osg-software/osg-wn-client/23/current/el8-x86_64/usr/bin/stashcp
$STASHCP -d osdf:///scratch/ejsledge/detector-simulation/geometries/MuColl_10TeV_v0A/MuColl_10TeV_v0A.xml

whizard mumu_H_bb_10TeV.sin


ls
echo

echo "Job complete"