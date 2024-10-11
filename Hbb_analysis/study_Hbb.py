from pyLCIO import IOIMPL
from pyLCIO import EVENT, UTIL
from ROOT import TH1D, TH2D, TFile, TLorentzVector, TMath, TTree, TVector3
import math
from optparse import OptionParser
from array import array
import os
import fnmatch

def collection_is_not_empty(event, collection_name):
    collection = event.getCollection(collection_name)
    count = 0
    for ihit, hit in enumerate(collection):
        count += 1
        break
    if count == 1:
        return True
    else:
        return False

print("Imports Successful!")
#Adapted from Federico Meloni and Junjia Zhang
#########################
# parameters
parser = OptionParser()
parser.add_option('-i', '--inFileDir', help='--inFileDir /data/fmeloni/DataMuC_MuColl_v1/reco/',
                  type=str, default='/scratch/ejsledge/jetStudies/reco_Hbb/output/Hbb_reco_sim_mumu_H_bb_10TeV_0')
parser.add_option('-p', '--inFilePrefix', help = '--inFilePrefix Hbb_reco_sim_mumu_H_bb_10TeV_0', 
                  type=str, default='neutronGun_E_0_50')
parser.add_option('-o', '--outFile', help='--output file name', 
                  type=str, default = 'Hbb_study')
parser.add_option('-v', action="store_true", help="-v if verbose", default=False)

(options, args) = parser.parse_args()



higgs_tree = TTree("higgs_tree", "neutron_tree")
E_truth = array('d', [0]) #true Higgs energy
pT_truth = array('d', [0]) #true Higgs pT
phi_truth = array('d', [0]) #true Higgs phi
theta_truth = array('d', [0]) #true Higgs theta
eta_truth = array('d', [0]) #true Higgs eta
jet_num = array('d', [0]) #number of Jets
bbbar_inv_mass = array('d', [0]) #Invariant mass of bbbar particles

b_E_truth = array('d', [0]) #true b energy
b_pT_truth = array('d', [0]) #true b pT
b_phi_truth = array('d', [0]) #true b phi
b_theta_truth = array('d', [0]) #true b theta
b_eta_truth = array('d', [0]) #true b eta

bbar_E_truth = array('d', [0]) #true bbar energy
bbar_pT_truth = array('d', [0]) #true bbar pT
bbar_phi_truth = array('d', [0]) #true bbar phi
bbar_theta_truth = array('d', [0]) #true bbar theta
bbar_eta_truth = array('d', [0]) #true bbar eta

mcparticle_num = array('d', [0]) #number of MCParticles
jet_energy = array('d', [0]) #total jet energy
dijet_invariant_mass = array('d', [0]) #top 2 jet invariant mass

higgs_tree.Branch("E_truth",  E_truth,  'var/D')
higgs_tree.Branch("pT_truth",  pT_truth,  'var/D')
higgs_tree.Branch("phi_truth", phi_truth, 'var/D')
higgs_tree.Branch("theta_truth", theta_truth, 'var/D')
higgs_tree.Branch("eta_truth", eta_truth, 'var/D')
higgs_tree.Branch("jet_num", jet_num, 'var/D')
higgs_tree.Branch("bbbar_inv_mass", bbbar_inv_mass, 'var/D')

higgs_tree.Branch("b_E_truth",  b_E_truth,  'var/D')
higgs_tree.Branch("b_pT_truth",  b_pT_truth,  'var/D')
higgs_tree.Branch("b_phi_truth", b_phi_truth, 'var/D')
higgs_tree.Branch("b_theta_truth", b_theta_truth, 'var/D')
higgs_tree.Branch("b_eta_truth", b_eta_truth, 'var/D')

higgs_tree.Branch("bbar_E_truth",  bbar_E_truth,  'var/D')
higgs_tree.Branch("bbar_pT_truth",  bbar_pT_truth,  'var/D')
higgs_tree.Branch("bbar_phi_truth", bbar_phi_truth, 'var/D')
higgs_tree.Branch("bbar_theta_truth", bbar_theta_truth, 'var/D')
higgs_tree.Branch("bbar_eta_truth", bbar_eta_truth, 'var/D')


higgs_tree.Branch("mcparticle_num", mcparticle_num, 'var/D')
higgs_tree.Branch("jet_energy", jet_energy, 'var/D')
higgs_tree.Branch("dijet_invariant_mass", dijet_invariant_mass, 'var/D')


jet_tree = TTree("jet_tree", "jet_tree")
higgs_E = array('d', [0]) #initial Higgs energy
higgs_pT = array('d', [0]) #initial Higgs pT
higgs_phi = array('d', [0]) #initial Higgs phi
higgs_theta = array('d', [0]) #initial Higgs theta
higgs_eta = array('d', [0]) #initial Higgs eta

jet_energy = array('d', [0]) #reconstructed jet energy
jet_pT = array('d', [0]) #reconstructed jet pT
jet_phi = array('d', [0]) #reconstructed jet phi
jet_theta = array('d', [0]) #reconstructed jet theta
jet_eta = array('d', [0]) #reconstructed jet eta

dijet_dR = array('d', [0]) #angular distance between dijets

jet_tree.Branch("higgs_E", higgs_E, 'var/D')
jet_tree.Branch("higgs_pT", higgs_pT, 'var/D')
jet_tree.Branch("higgs_phi", higgs_phi, 'var/D')
jet_tree.Branch("higgs_theta", higgs_theta, 'var/D')
jet_tree.Branch("higgs_eta", higgs_eta, 'var/D')

jet_tree.Branch("jet_energy", jet_energy, 'var/D')
jet_tree.Branch("jet_pT", jet_pT, 'var/D')
jet_tree.Branch("jet_phi", jet_phi, 'var/D')
jet_tree.Branch("jet_theta", jet_theta, 'var/D')
jet_tree.Branch("jet_eta", jet_theta, 'var/D')
jet_tree.Branch("dijetjet_dR", dijet_dR, 'var/D')


#open file
#file_dir = options.inFileDir + options.inFilePrefix
#iFile = file_dir + "/" + file_name
iFile = "/scratch/ejsledge/jetStudies/reco_Hbb/output/Hbb_reco_sim_mumu_H_bb_10TeV_0.slcio"


reader = IOIMPL.LCFactory.getInstance().createLCReader()
reader.open(iFile)

PDG_list = []

for ievt, event in enumerate(reader):
    mcpCollection = event.getCollection('MCParticle')
    if (options.v and ievt%10==0 and ievt>0):
            print("Processing event " + str(ievt))
            #break

    has_b = False
    has_bbar = False
    mcparticle_num[0] = len(mcpCollection)
    for mcp in mcpCollection:
        mcpPDG = mcp.getPDG()
        if mcpPDG not in PDG_list:
            PDG_list.append(mcpPDG)
        if mcpPDG == 25:
            E_truth[0] = mcp.getEnergy()
            dp3 = mcp.getMomentum()
            tlv = TLorentzVector()
            tlv.SetPxPyPzE(dp3[0], dp3[1], dp3[2], mcp.getEnergy())
            pT_truth[0] = tlv.Perp()
            phi_truth[0] = tlv.Phi()
            theta_truth[0] = tlv.Theta()
            eta_truth[0] = tlv.Eta()
        if mcpPDG == 5:
            has_b = True
            b_E_truth[0] = mcp.getEnergy()
            dp3 = mcp.getMomentum()
            btlv = TLorentzVector()
            btlv.SetPxPyPzE(dp3[0], dp3[1], dp3[2], mcp.getEnergy())
            b_pT_truth[0] = btlv.Perp()
            b_phi_truth[0] = btlv.Phi()
            b_theta_truth[0] = btlv.Theta()
            b_eta_truth[0] = btlv.Eta()
        if mcpPDG == -5:
            has_bbar = True
            bbar_E_truth[0] = mcp.getEnergy()
            dp3 = mcp.getMomentum()
            bbartlv = TLorentzVector()
            bbartlv.SetPxPyPzE(dp3[0], dp3[1], dp3[2], mcp.getEnergy())
            bbar_pT_truth[0] = bbartlv.Perp()
            bbar_phi_truth[0] = bbartlv.Phi()
            bbar_theta_truth[0] = bbartlv.Theta()
            bbar_eta_truth[0] = bbartlv.Eta()
    if(has_b and has_bbar):
        mb = 4.18 #GeV
        invMassPerf = math.sqrt(2*mb**2 + 2*(b_E_truth[0]*bbar_E_truth[0]) -(btlv.Px()*bbartlv.Px() + btlv.Py()*bbartlv.Py() + btlv.Pz()*bbartlv.Pz()))
        #s = btlv.Dot(bbartlv)
        #invMassRel = math.sqrt(2*b_pT_truth[0]*bbar_pT_truth[0]*(math.cosh(b_eta_truth[0]-bbar_eta_truth[0]) - math.cos(b_phi_truth[0]-bbar_phi_truth[0])))
        #print("perf = {} GeV | s = {} GeV | rel = {} GeV", invMassPerf, math.sqrt(s), invMassRel)
        bbbar_inv_mass[0] = invMassPerf
        

    higgs_tree.Fill()


    '''
    higgs_E[0] = mcp.getEnergy()
            higgs_pT[0] = tlv.Perp()
            higgs_phi[0] = tlv.Phi()
            higgs_theta[0] = tlv.Theta()
            higgs_eta[0] = tlv.Eta()
            '''

print(PDG_list)

output_file = TFile("Hbb_analysis_0.root", 'RECREATE')

higgs_tree.Write()
#jet_tree.Write()
output_file.Close()
