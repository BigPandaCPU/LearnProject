import synapseclient
import synapseutils

syn = synapseclient.Synapse()
syn.login('synapse_username', 'password')
files = synapseutils.syncFromSynapse(syn, 'syn10285054')
