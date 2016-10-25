# Praktikumsauswertung P1
## Messen.py
This is the program that should be run when the Experiment is conducted it also collects Metadata to the experiment.
it writes the following Variables into dict in a JSON-File:
* messungen
* messgroessen
* metadaten 
The Structure of the Metaata is the following:
messungen is an list of lists where every containd list is one messung.
messgroessen is a list of lists where every contained list is a messgroese with acompaning data to describe the characteristics of the measured Value.
metadata[i] corresponds to messgroessen[i] corresponds to messung[i] of messungen.
