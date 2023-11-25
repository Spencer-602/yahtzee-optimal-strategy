from itertools import combinations_with_replacement, combinations, product, chain
from scoring import Roll, Category

def reverse_dict(d): 
    rd = {}
    for k in d:
        for roll in d[k]:
            rd.setdefault(roll, set())
            rd[roll].add(k)
    return rd

""" dice throw experiment"""
def throw_dice(kept): # calculates probability of each dice roll
    n_dice_to_roll = 5-len(kept)
    # dice = (1,2,3,4,5,6)
    outcomes  = set(product(dice, repeat=n_dice_to_roll)) # set with all possible outcomes of rolling n dice - with repetition
    hist = {}
    for trial in outcomes:
        # chain combines two iterables together
        sorted_trial = tuple(sorted(chain(kept, trial))) # combines kept dice with currently rolled "trial" dice - sorted numerically
        hist.setdefault(sorted_trial, 0) # adds the dice to the dictionary with value 0 if it is not already there
        hist[sorted_trial] += 1 # adds 1 occurrence to the dice combination.
    normalizer = float(sum(hist.values())) # number of possibilities
    for k in hist:
        hist[k] /= normalizer # for each dice roll - divides number of occurrences by total number of dice rolls
    return hist

""" g3: the edges from g2 to g3"""
def get_edges_and_prob():
    dice = range(1,7)
    # combinations with replacement(iterator, length of subset): unordered, allows same item to be used multiple times in the same group Ex. ((1,2,3,4), 3) -> (1,1,2), (1,3,3), (1,4,3)
    # combinations(iterator, length of subset): unordered, each item can only be used once per group Ex. ((1,2,3,4), 3) -> (1,2,3), (1,2,4)

    # fills distinct_keeper with every possible keep of every roll
    for t in combinations_with_replacement(dice,5): # every possible roll with 5 dice without repetition - length 252 - page 8
        for n_keep in range(0,6): # every possible number of keep
            for keep in combinations(t,n_keep): # every n_keep size group in the current roll
                if keep not in distinct_keeper:
                    distinct_keeper.add(keep) 
                    kept_to_id[keep] = len(distinct_keeper)-1 # converts keep to a number for easier use
                    id_to_kept[len(distinct_keeper)-1] = keep # converts number back to keep

    reroller = {} # Dictionary
    for case in distinct_keeper:
        n_dice_to_reroll = 5 - len(case) # if you kept 0, reroll 5
        for reroll in combinations_with_replacement(dice, n_dice_to_reroll): # possible rerolls 
            reroll_result = tuple(sorted(chain(case, reroll))) # combines keep and reroll and sorts numerically to prevent duplicates
            reroller.setdefault(case, {}) # if the current keep (case) doesn't exist yet, add it to reroller with a value of an empty dictionary - used to hold all possible reroll results
            reroller[case].setdefault(reroll_result,0) # if the reroll result is new, add it to the keep's possible results with value 0
            reroller[case][reroll_result] = 1 # why isn't this += 1 like line 22?
                
    for case in reroller:
        hist = throw_dice(case)
        for key in reroller[case]:
            reroller[case][key] = hist[key]
    return reroller

""" global shared data """
dice = range(1,7)
dice_to_id = {}
id_to_dice = {}
kept_to_id = {}    
id_to_kept = {}

distinct_keeper = set()
for i,t in enumerate(combinations_with_replacement(dice,5)):
    dice_to_id[t] = i
    id_to_dice[i] = t

edge_prob = get_edges_and_prob()
reverse_edge = reverse_dict(edge_prob)


#retro_back = get_retro_back()
single_throw = throw_dice(tuple())

all_5_dice_outcomes = [t for t in combinations_with_replacement(dice,5)]

eval_points = {}
for cat_name in Category.CATEGORY_ID_TO_NAME:
    for r in all_5_dice_outcomes:
        eval_points.setdefault(cat_name, {})
        eval_points[cat_name][r] = Roll(r).eval_point(cat_name)
        #print cat_name, r, eval_points[cat_name][r] 

print 'length of dice_to_id', len(dice_to_id)
print 'length of kept_to_id', len(kept_to_id)

for key in id_to_dice:
    #print key, dice_to_id[id_to_dice[key]]
    assert key == dice_to_id[id_to_dice[key]]

for key in id_to_kept:
    #print key, kept_to_id[id_to_kept[key]]
    assert key == kept_to_id[id_to_kept[key]]

#from pprint import pprint
#pprint(eval_points)
