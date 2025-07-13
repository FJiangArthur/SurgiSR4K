import synapseclient 
import synapseutils 

syn = synapseclient.Synapse() 
syn.login(authToken="YOUR_TOKEN_HERE") 
files = synapseutils.syncFromSynapse(syn, 'syn68656645') 
