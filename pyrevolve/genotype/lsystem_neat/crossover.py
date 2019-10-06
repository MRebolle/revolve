from pyrevolve.genotype.plasticoding.plasticoding import Plasticoding, Alphabet, PlasticodingConfig
from pyrevolve.genotype.lsystem_neat.lsystem_neat_genotype import LSystemCPGHyperNEATGenotype
from pyrevolve.genotype.neat_brain_genome.crossover import NEATCrossoverConf
from pyrevolve.genotype.neat_brain_genome.crossover import standard_crossover as NEATBrainCrossover

import random


class CrossoverConfig:
    def __init__(self,
                 crossover_prob):
        """
        Creates a Crossover object that sets the configuration for the crossover operator

        :param crossover_prob: crossover probability
        """
        self.crossover_prob = crossover_prob



def standard_crossover(parent_individuals, Lsystem_conf, cross_conf):
    """
    Creates an child (individual) through crossover with two parents

    :param parent_individuals: Parents type Individual2
    :param genotype_conf: LSystemCPGHyperNEATGenotypeConfig type
    :param cross_conf: Lsystem-CrossoverConfig type
    :return: brain and body crossover (Only body right now)
    """
    assert len(parent_individuals) == 2

    parents_body_genotype = [p.body_genotype for p in parent_individuals]
    parents_brain_genotype = [p.brain_genotype for p in parent_individuals]

    child_genotype = LSystemCPGHyperNEATGenotype()
    Neatconf = NEATCrossoverConf()

    new_body = new_child_body(parents_body_genotype, Lsystem_conf, cross_conf)
    new_brain = NEATBrainCrossover(parents_brain_genotype, Neatconf, cross_conf)

    child_genotype._body_genome = new_body
    child_genotype._brain_genome = new_brain

    return child_genotype


def new_child_body(parents, Lsystem_conf, cross_conf):

        grammar = {}
        crossover_attempt = random.uniform(0.0, 1.0)
        if crossover_attempt > cross_conf.crossover_prob:
            grammar = parents[0].grammar
        else:
            for letter in Alphabet.modules():
                sel_parent = random.randint(0, 1)
                grammar[letter[0]] = parents[sel_parent].grammar[letter[0]]

        new_genotype = Plasticoding(Lsystem_conf.plasticoding, 'tmp')
        new_genotype.grammar = grammar
        return new_genotype


    #mother_body = parent_individuals[0].genotype._body_genome
    #father_body = parent_individuals[1].genotype._body_genome
    #mother_brain = parent_individuals[0].genotype._brain_genome
    #father_brain = parent_individuals[1].genotype._brain_genome
    #child_genotype = LSystemCPGHyperNEATGenotype()
    #child_genotype._body_genome = standard_crossover_lsystem([mother_body, father_body])
    #child_genotype._brain_genome = standard_crossover_neat([mother_brain, father_brain])
    #return child_genotype