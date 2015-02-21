#! /usr/bin/env python
#Â encoding: utf-8
#
# Res andy
import xml.etree.ElementTree as ET,sys

###########################################################
#  • Always backup your map before launching this script  #
#  • Do that even so this script does its backup as well  # 
#  • Place this file directly into the map folder         # 
#  • Please report any errors to andys@deltaflyer.cz      #
#  • You can contact me on unofficial IRC SE channel too  #
#  • join #space-engineers on irc.esper.net               #
###########################################################

#too lazy to study namespaces in python, lets load the namespace line into string and place it into newly created file later
origfile = open('Sandbox.sbc').read()
backupfile = open('Sandbox.orig',"w")
backupfile.write(origfile)
backupfile.close
windows = 0
if len(origfile.split("\r\n")) == 1: #fix if this script is run in windows and set the flag
	windows = 1
	header = origfile.split("\n")[1]
else:
	header = origfile.split("\r\n")[1]


tree = ET.parse('Sandbox.sbc') #creates XML tree from sandbox.sbc file
root = tree.getroot() #creates XML root from the tree

checker = open('SANDBOX_0_0_0_.sbs').read() #opens worldfile for second checking if we have any items belonging to the IdentityID

a = 0 #helper to backnotate to root in XML remove function (it does not automatically)
deleted = 0 #definition of deleted NPC's, just for our info
Idents = [] #list of npcs to remove
Players = []

for child in root: #Let's list all subelements in root
	if child.tag == "Identities": #if the element is Itentity list
		Identities = a #save its position in root to this integer
		for identid in child: #iterate every Identity
			Idents.append(identid.find("IdentityId").text) #Add ID to Ident list

	if child.tag == "AllPlayersData": #if the element is PlayersData list, lets compile first checking list
		for item in child[0]: #iterate every playerdata
			for identid in item.findall("Value/IdentityId"): #in that look for IdentityId tag
				Players.append(identid.text) #and add it to Players list

	a += 1


if len(Idents) > 500:
	print "Please be patient. This script will run for long time as you have %s Identities for removal (some may be duplicates)." %len(Idents)

for Ident in Idents: #for every npcID in our NPC list
	if Ident in Players: #Verify, if this ID is amongst the Players
		print "%s not removed, is a player" %Ident #and gloat about it
		continue #and skip second check (no needed, we will not remove actual players)
	if Ident in checker: #Also verify, if this npc owns ANY blocks in the world
		print "%s not removed, some blocks owned by this ID" %Ident #and gloat about it
		continue #and skip removal, we cannot remove idents if they own any structure 

	for child in root.findall("Identities/MyObjectBuilder_Identity"): #for every Ident list all identities
		PlayerID = child.find("IdentityId").text #Extract the value from PlayerID subnode
		if PlayerID == Ident: # If they match
			root[Identities].remove(child) #remove node
			deleted += 1 #and increase counter
		

print "deleted %s entities" %deleted #gloat about how we're good
tree = ET.ElementTree(root)
tree.write('Sandbox.sbc', encoding='utf-8', xml_declaration=True) #save the file

filethelper = "" #helping string
worldR = open('Sandbox.sbc',"r") #open world file for reading
filet = worldR.read().split("\n") #read its content and split it by line (without newline character)
worldR.close() #close the file so we can write into it
filet[1] = header #replace the namespace line with the backup from the begining of the file
for line in filet: #iterate through every line in file
	if windows == 1:
		filethelper += line+"\n" #mangle it together with DOS newline
	else:
		filethelper += line+"\r\n" #mangle it together with FORCED DOS newline
worldW = open('Sandbox.sbc',"w") #open worldfile for write
worldW.write(filethelper) #write it                                 
worldW.close() #close it
#quit