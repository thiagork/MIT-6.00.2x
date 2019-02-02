# MIT 6.00.2x
# Problem Set 3
# Simulating the Spread of Disease and Virus Population Dynamics

from ps3b_precompiled_36 import *
import random
import pylab

random.seed(0)  # Comment this line to see different results!


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce.
    """


class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        if random.random() <= self.getClearProb():
            return True
        else:
            return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        if random.random() <= (self.maxBirthProb * (1 - popDensity)):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException('NoChildException')


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population.
        returns: The total virus population (an integer)
        """
        return len(self.getViruses())

    def getPopDensity(self):
        """
        Returns the population density
        """
        return self.getTotalPop() / self.getMaxPop()

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step.

        returns: The total virus population at the end of the update (an
        integer)
        """
        copyViruses = self.getViruses()[:]
        for virus in copyViruses:
            if virus.doesClear():
                self.viruses.remove(virus)
        if self.getPopDensity() < 1:
            copyViruses = self.getViruses()[:]
            for virus in copyViruses:
                try:
                    self.viruses.append(virus.reproduce(self.getPopDensity()))
                except NoChildException:
                    pass
        return self.getTotalPop()


def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph when no drugs are used and
    viruses do not have any drug resistance.
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    numTimesteps = 300
    virusPopulationPerTrial = {x: () for x in range(numTimesteps)}
    for trial in range(numTrials):
        # Line bellow broken to comply with pep8
        viruses = [SimpleVirus(maxBirthProb, clearProb)
                   for x in range(numViruses)]
        patient = Patient(viruses, maxPop)
        for timestep in range(numTimesteps):
            patient.update()
            virusPopulationPerTrial[timestep] += (patient.getTotalPop(),)
    avgVirusPopulation = {}
    for timestep in virusPopulationPerTrial:
        # Line bellow broken to comply with pep8
        avgVirusPopulation[timestep] = (
                sum(virusPopulationPerTrial[timestep]) /
                len(virusPopulationPerTrial[timestep])
        )
    pylab.plot(list(avgVirusPopulation.values()), label="SimpleVirus")
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc="best")
    pylab.show()


class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as
        attributes of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each
        drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This
        is the probability of the offspring acquiring or losing resistance to
        a drug.
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb
        SimpleVirus.__init__(self, self.maxBirthProb, self.clearProb)

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This
        method is called by getResistPop() in TreatedPatient to determine
        how many virus particles have resistance to a drug.

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        try:
            if self.getResistances()[drug]:
                return True
            else:
                return False
        except KeyError:
            return False

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child has the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException('NoChildException')
        inheritance = dict(self.getResistances())
        for trait in inheritance:
            if random.random() <= self.getMutProb():
                inheritance[trait] = not self.getResistances()[trait]
        if random.random() <= (self.maxBirthProb * (1 - popDensity)):
            # Line bellow broken to comply with pep8
            return ResistantVirus(self.maxBirthProb, self.clearProb,
                                  inheritance, self.getMutProb())
        else:
            raise NoChildException('NoChildException')


class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.prescriptions = []
        Patient.__init__(self, self.viruses, self.maxPop)

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no
        effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is
        updated.
        """
        if newDrug not in self.getPrescriptions():
            self.prescriptions.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.prescriptions

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings.

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        virusesResistantToAllInDrugResist = 0
        for virus in self.getViruses():
            resistantToAll = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    resistantToAll = False
            if resistantToAll:
                virusesResistantToAllInDrugResist += 1
        return virusesResistantToAllInDrugResist

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step.

        returns: The total virus population at the end of the update (an
        integer)
        """
        copyViruses = self.getViruses()[:]
        for virus in copyViruses:
            if virus.doesClear():
                self.viruses.remove(virus)
        if self.getPopDensity() < 1:
            copyViruses = self.getViruses()[:]
            for virus in copyViruses:
                try:
                    # Line bellow broken to comply with pep8
                    self.viruses.append(
                        virus.reproduce(
                            self.getPopDensity(), self.getPrescriptions()
                        )
                    )
                except NoChildException:
                    pass
        return self.getTotalPop()


# Line bellow broken to comply with pep8
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb,
                       resistances, mutProb, numTrials):
    """
    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1).
    numTrials: number of simulation runs to execute (an integer)

    """
    numTimesteps = 300
    virusPopulationPerTrial = {x: () for x in range(numTimesteps)}
    resistantVirusPopulationPerTrial = dict(virusPopulationPerTrial)
    for trial in range(numTrials):
        # Line bellow broken to comply with pep8
        viruses = [ResistantVirus(maxBirthProb, clearProb, resistances,
                                  mutProb) for x in range(numViruses)]
        patient = TreatedPatient(viruses, maxPop)
        # Runs the first half of the simulation without drugs
        for timestep in range(numTimesteps//2):
            patient.update()
            virusPopulationPerTrial[timestep] += (patient.getTotalPop(),)
            # Line bellow broken to comply with pep8
            resistantVirusPopulationPerTrial[timestep] += (
                patient.getResistPop(['guttagonol']),
            )
        patient.addPrescription('guttagonol')
        # Runs the second half of the simulation after adding the drug
        for timestep in range(numTimesteps//2, numTimesteps):
            patient.update()
            virusPopulationPerTrial[timestep] += (patient.getTotalPop(),)
            # Line bellow broken to comply with pep8
            resistantVirusPopulationPerTrial[timestep] += (
                patient.getResistPop(['guttagonol']),
            )
    avgVirusPopulation = {}
    avgResistantVirusPopulation = {}
    # Runs the trials
    for timestep in virusPopulationPerTrial:
        # Line bellow broken to comply with pep8
        avgVirusPopulation[timestep] = (
            sum(virusPopulationPerTrial[timestep]) /
            len(virusPopulationPerTrial[timestep])
        )
        # Line bellow broken to comply with pep8
        avgResistantVirusPopulation[timestep] = (
            sum(resistantVirusPopulationPerTrial[timestep]) /
            len(resistantVirusPopulationPerTrial[timestep])
        )
    # Plots the results
    # Line bellow broken to comply with pep8
    pylab.plot(list(avgVirusPopulation.values()),
               label="Average total virus population")
    # Line bellow broken to comply with pep8
    pylab.plot(list(avgResistantVirusPopulation.values()),
               label="Average population of guttagonol-resistant virus")
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("time step")
    pylab.ylabel("# viruses")
    pylab.legend(loc="best")
    pylab.show()


# Uncomment one of these bellow to run the simulation
# simulationWithDrug(100, 20, 0.1, 0.05, 30)
simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 100)
# simulationWithDrug(100, 1000, 0.1, 0.05, {}, 0.005, 100)
# simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)
# simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)
