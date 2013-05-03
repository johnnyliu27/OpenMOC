import numpy
from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize


###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

num_threads = 4
track_spacing = 0.1
num_azim = 16
tolerance = 1E-3
max_iters = 1000
gridsize = 500

log.setLogLevel('NORMAL')


###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = materialize.materialize('../c5g7-materials.hdf5')

uo2_id = materials['UO2'].getId()
water_id = materials['Water'].getId()


###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating surfaces...')

circles = []
planes = []
radii = [0.15, 0.2, 0.25, 0.3, 0.35, 0.4]
planes.append(XPlane(x=-34.0))
planes.append(XPlane(x=34.0))
planes.append(YPlane(y=-34.0))
planes.append(YPlane(y=34.0))
for plane in planes: plane.setBoundaryType(REFLECTIVE)
for r in radii: circles.append(Circle(x=0.0, y=0.0, radius=r))


###############################################################################
#############################   Creating Cells   ##############################
###############################################################################

log.py_printf('NORMAL', 'Creating cells...')

cells = []
cells.append(CellBasic(universe=1, material=uo2_id))
cells.append(CellBasic(universe=1, material=water_id))
cells.append(CellBasic(universe=2, material=uo2_id))
cells.append(CellBasic(universe=2, material=water_id))
cells.append(CellBasic(universe=3, material=uo2_id))
cells.append(CellBasic(universe=3, material=water_id))
cells.append(CellBasic(universe=4, material=uo2_id))
cells.append(CellBasic(universe=4, material=water_id))
cells.append(CellBasic(universe=5, material=uo2_id))
cells.append(CellBasic(universe=5, material=water_id))
cells.append(CellBasic(universe=6, material=uo2_id))
cells.append(CellBasic(universe=6, material=water_id))

cells.append(CellFill(universe=9, universe_fill=7))
cells.append(CellFill(universe=11, universe_fill=8))
cells.append(CellFill(universe=0, universe_fill=10))

cells[0].addSurface(halfspace=-1, surface=circles[0])
cells[1].addSurface(halfspace=+1, surface=circles[0])
cells[2].addSurface(halfspace=-1, surface=circles[1])
cells[3].addSurface(halfspace=+1, surface=circles[1])
cells[4].addSurface(halfspace=-1, surface=circles[2])
cells[5].addSurface(halfspace=+1, surface=circles[2])
cells[6].addSurface(halfspace=-1, surface=circles[3])
cells[7].addSurface(halfspace=+1, surface=circles[3])
cells[8].addSurface(halfspace=-1, surface=circles[4])
cells[9].addSurface(halfspace=+1, surface=circles[4])
cells[10].addSurface(halfspace=-1, surface=circles[5])
cells[11].addSurface(halfspace=+1, surface=circles[5])

cells[14].addSurface(halfspace=+1, surface=planes[0])
cells[14].addSurface(halfspace=-1, surface=planes[1])
cells[14].addSurface(halfspace=+1, surface=planes[2])
cells[14].addSurface(halfspace=-1, surface=planes[3])


###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating 5 x 5 core of 17 x 17 assemblies...')

# 1st 17x17 assembly
assembly1 = Lattice(id=7, width_x=1.0, width_y=1.0)
assembly1.setLatticeCells([[1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
                          [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                          [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
                          [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                          [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
                          [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                          [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
                          [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                          [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
                          [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                          [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
                          [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                          [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
                          [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                          [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
                          [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                          [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]])

# 2nd 17x17 assembly
assembly2 = Lattice(id=8, width_x=1.0, width_y=1.0)
assembly2.setLatticeCells([[4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4],
                          [5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5],
                          [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4],
                          [5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5],
                          [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4],
                          [5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5],
                          [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4],
                          [5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5],
                          [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4],
                          [5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5],
                          [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4],
                          [5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5],
                          [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4],
                          [5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5],
                          [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4],
                          [5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5],
                          [4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4, 5, 4]])

# 4x4 core
core = Lattice(id=10, width_x=17.0, width_y=17.0)
core.setLatticeCells([[9, 11, 9, 11],
                      [11, 9, 11, 9],
                      [9, 11, 9, 11],
                      [11, 9, 11, 9]])


###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry()
for material in materials.values(): geometry.addMaterial(material)
for cell in cells: geometry.addCell(cell)
geometry.addLattice(core)
geometry.addLattice(assembly1)
geometry.addLattice(assembly2)

geometry.initializeFlatSourceRegions()


###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

log.py_printf('NORMAL', 'Initializing the track generator...')

track_generator = TrackGenerator(geometry, num_azim, track_spacing)
track_generator.generateTracks()


###############################################################################
###########################   Running a Simulation   ##########################
###############################################################################

solver = Solver(geometry, track_generator)
solver.setNumThreads(num_threads)
solver.setSourceConvergenceThreshold(tolerance)

Timer.startTimer()
solver.convergeSource(max_iters)
Timer.stopTimer()
Timer.recordSplit('Fixed source iteration on host')
Timer.printSplits()


###############################################################################
############################   Generating Plots   #############################
###############################################################################

log.py_printf('NORMAL', 'Plotting data...')

plotter.plotTracks(track_generator)
plotter.plotMaterials(geometry, gridsize)
plotter.plotCells(geometry, gridsize)
plotter.plotFlatSourceRegions(geometry, gridsize)
plotter.plotFluxes(geometry, solver, energy_groups=[1,2,3,4,5,6,7])

log.py_printf('TITLE', 'Finished')
