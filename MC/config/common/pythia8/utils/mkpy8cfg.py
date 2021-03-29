#! /usr/bin/env python3

### @author: Roberto Preghenella
### @email: preghenella@bo.infn.it

import argparse

parser = argparse.ArgumentParser(description='Make Pythia8 configuration',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--seed', type=int, default=None,
                   help='The random seed')

parser.add_argument('--idA', type=int, default='2212',
                   help='PDG code of projectile beam')

parser.add_argument('--idB', type=int, default='2212',
                   help='PDG code of target beam')

parser.add_argument('--eCM', type=float, default='13000.',
                    help='Centre-of-mass energy')

parser.add_argument('--process', default='inel', choices=['none', 'inel', 'ccbar', 'bbbar', 'heavy', 'jets', 'dirgamma'],
                    help='Process to switch on')

parser.add_argument('--ptHatMin', type=float,
                    help='The minimum invariant pT')

parser.add_argument('--ptHatMax', type=float,
                    help='The maximum invariant pT')

parser.add_argument('--weightPower', type=float,
                    help='Weight power to pT hard spectrum')

parser.add_argument('--output', default='pythia8.cfg',
                    help='Where to write the configuration')

parser.add_argument('--include', action='append', default=None,
                    help='Include files at the top of the configuration')

parser.add_argument('--append', action='append', default=None,
                    help='Include files at the bottom of the configuration')

parser.add_argument('--command', action='append', default=None,
                    help='User specified commands at the end of the configuration')

args = parser.parse_args()

### open output file
fout = open(args.output, 'w')

### included files
if args.include is not None :
    for i in args.include :
        fout.write('### --> included from %s \n' % (i))
        fin = open(i, 'r')
        data = fin.read()
        fin.close()
        fout.write('\n')
        fout.write(data)
        fout.write('\n')
        fout.write('### <-- included from %s \n' % (i))
    fout.write('\n')

fout.write('### --> generated by mkpy8cfg.py \n')
fout.write('\n')

### random
if args.seed is not None:
    fout.write('### random \n')
    fout.write('Random:setSeed = on \n')
    fout.write('Random:seed = %d \n' % (args.seed))
    fout.write('\n')

### beams
fout.write('### beams \n')
fout.write('Beams:idA = %d \n' % (args.idA))
fout.write('Beams:idB = %d \n' % (args.idB))
fout.write('Beams:eCM = %f \n' % (args.eCM))
fout.write('\n')

### processes
fout.write('### processes \n')
fout.write('SoftQCD:inelastic = off \n') ### we switch this off because it might be on by default
if args.process == 'inel':
    fout.write('SoftQCD:inelastic = on \n')
if args.process == 'ccbar' or args.process == 'heavy':
    fout.write('HardQCD:hardccbar = on \n')
if args.process == 'bbbar' or args.process == 'heavy':
    fout.write('HardQCD:hardbbbar = on \n')
if args.process == 'jets':
    fout.write('HardQCD:all = on \n')
if args.process == 'dirgamma':
    fout.write('PromptPhoton:all = on \n')
fout.write('\n')

### heavy ion  settings (valid for Pb-Pb 5520 only)
if args.idA==1000822080 and args.idB==1000822080:
    fout.write('### heavy-ion settings (valid for Pb-Pb 5520 only) \n')
    fout.write('HeavyIon:SigFitNGen = 0 \n')
    fout.write('HeavyIon:SigFitDefPar = 13.88,1.84,0.22,0.0,0.0,0.0,0.0,0.0 \n')
    fout.write('HeavyIon:bWidth = 14.48 \n')
fout.write('\n')

### decays
fout.write('### decays \n')
fout.write('ParticleDecays:limitTau0 = on \n') ### we will need to put some parameters for these settings
fout.write('ParticleDecays:tau0Max = 10. \n')
fout.write('\n')

### phase space cuts
fout.write('### phase space cuts \n')
if args.ptHatMin is not None :
    fout.write('PhaseSpace:pTHatMin = %f \n' % (args.ptHatMin))
if args.ptHatMax is not None :
    fout.write('PhaseSpace:pTHatMax = %f \n' % (args.ptHatMax))
if args.weightPower is not None :
    fout.write('PhaseSpace:bias2Selection = on \n')
    fout.write('PhaseSpace:bias2SelectionPow = %f" \n' % (args.weightPower))

fout.write('\n')

fout.write('### <-- generated by mkpy8cfg.py \n')
fout.write('\n')
    
### appended files
if args.append is not None :
    for i in args.append :
        fout.write('### --> included from %s \n' % (i))
        fin = open(i, 'r')
        data = fin.read()
        fin.close()
        fout.write('\n')
        fout.write(data)
        fout.write('\n')
        fout.write('### <-- included from %s \n' % (i))
    fout.write('\n')
    
### user commands
if args.command is not None :
    fout.write('### --> user commands \n')
    fout.write('\n')
    for i in args.command :
        fout.write(i)
        fout.write('\n')
        fout.write('\n')
    fout.write('### <-- user commands \n')

### close outout file
fout.close()
