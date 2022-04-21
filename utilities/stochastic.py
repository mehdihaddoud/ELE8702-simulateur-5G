from math import ceil
from scipy.stats import expon, uniform
"""Stochastic based functions

Module used to regroup stochastic functions such as 
packet generation.
"""

def gen_packets(time: int, gen_distribution: dict, 
                len_distribution: dict) -> list:
    """Generates packet info

    Note that genrerations are in batch for performance 
    enhancement.

    Args: 
        time (int): time interval to generate packets (ms)
        gen_distribution (dict): Parameters of the 
            packet generation time in the same format 
            as the input.
        len_distribution (dict): Parameters of the packet generation 
            length (in bits) in the same format as the input.

    """
    gen_sample_lists = []
    for i, distribution_dict in enumerate([gen_distribution, len_distribution]):
        if distribution_dict['type'] == 'uniform':
            distribution = uniform
            parameters = (distribution_dict['a'],
                          distribution_dict['b'])
            parameters = {'scale' :distribution_dict['b'] \
                                   - distribution_dict['a'],
                          'loc': distribution_dict['a']}
        elif distribution_dict['type'] == 'exponential':
            distribution = expon
            parameters = {'scale' :distribution_dict['scale'],
                          'loc': 0}
        else:
            raise NotImplementedError('Distribution type not implemented')

        if i == 0: #case defining the number of total packets
            samples = []
            last_sample =-3*parameters['scale'] #Negative for buffer
            pregen_samples = []
            i = 0
            while last_sample < time:
                if i == len(pregen_samples): 
                    i=0
                    pregen_samples = distribution.rvs(
                        size = int(1.5*time/parameters['scale']), 
                        scale = parameters['scale'],
                        loc = parameters['loc'])
                last_sample += pregen_samples[i]
                if last_sample >= 0: #Discarding buffer
                    samples.append(ceil(last_sample))
                i += 1
            samples.pop()
            gen_sample_lists.append(samples)

        else: #Simpler case with fixed number of generations
            gen_sample_lists.append(map(
                ceil,
                list( distribution.rvs(size = len(gen_sample_lists[0]),
                                       scale = parameters['scale'],
                                       loc = parameters['loc'])),
                ))
    return list(zip(*gen_sample_lists))
