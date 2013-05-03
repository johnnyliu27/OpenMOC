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
planes.append(XPlane(x=-2.0))
planes.append(XPlane(x=2.0))
planes.append(YPlane(y=-2.0))
planes.append(YPlane(y=2.0))
circles.append(Circle(x=0.0, y=0.0, radius=0.4))
circles.append(Circle(x=0.0, y=0.0, radius=0.3))
circles.append(Circle(x=0.0, y=0.0, radius=0.2))
for plane in planes: plane.setBoundaryType(REFLECTIVE)


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
cells.append(CellFill(universe=5, universe_fill=4))
cells.append(CellFill(universe=0, universe_fill=6))

cells[0].addSurface(halfspace=-1, surface=circles[0])
cells[1].addSurface(halfspace=+1, surface=circles[0])
cells[2].addSurface(halfspace=-1, surface=circles[1])
cells[3].addSurface(halfspace=+1, surface=circles[1])
cells[4].addSurface(halfspace=-1, surface=circles[2])
cells[5].addSurface(halfspace=+1, surface=circles[2])

cells[7].addSurface(halfspace=+1, surface=planes[0])
cells[7].addSurface(halfspace=-1, surface=planes[1])
cells[7].addSurface(halfspace=+1, surface=planes[2])
cells[7].addSurface(halfspace=-1, surface=planes[3])


###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating 16 x 16 lattice...')

# 2x2 assembly
assembly = Lattice(id=4, width_x=1.0, width_y=1.0)
assembly.setLatticeCells([[1, 2], [1, 3]])

# 2x2 core
core = Lattice(id=6, width_x=2.0, width_y=2.0)
core.setLatticeCells([[5, 5], [5, 5]])


###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry()
for material in materials.values(): geometry.addMaterial(material)
for cell in cells: geometry.addCell(cell)
geometry.addLattice(assembly)
geometry.addLattice(core)

geometry.initializeFlatSourceRegions()


###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

log.py_printf('NORMAL', 'Initializing the track generator...')

track_generator = TrackGenerator(geometry, num_azim, track_spacing)
track_generator.setNumAzim(num_azim)
track_generator.setTrackSpacing(track_spacing)
track_generator.setGeometry(geometry)
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

#log.py_printf('NORMAL', 'Plotting data...')

#plotter.plotTracks(track_generator)
#plotter.plotMaterials(geometry, gridsize)
#plotter.plotCells(geometry, gridsize)
#plotter.plotFlatSourceRegions(geometry, gridsize)
#plotter.plotFluxes(geometry, solver, energy_groups=[1,2,3,4,5,6,7])

log.py_printf('TITLE', 'Finished')
