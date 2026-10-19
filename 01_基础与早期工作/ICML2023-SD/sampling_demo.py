"""Dependency-free teaching reference for Algorithm 1; no Transformer timing claims."""
import random
import unittest
from collections import Counter


def sample(probs, rng):
    value = rng.random()
    cumulative = 0.0
    for token, probability in enumerate(probs):
        cumulative += probability
        if value < cumulative:
            return token
    return len(probs) - 1  # Roundoff at the last cumulative sum.


def residual(p, q):
    weights = [max(pi - qi, 0.0) for pi, qi in zip(p, q)]
    total = sum(weights)
    if total <= 0:
        raise ValueError('Residual is undefined when rejection has zero probability.')
    return [weight / total for weight in weights]


def speculative_step(prefix, draft_probs, target_batch_probs, gamma, rng):
    """Callbacks return normalized distributions over the SAME token IDs.

    target_batch_probs(contexts) supplies all gamma+1 distributions in one call.
    A toy callback may loop over contexts; this is not a GPU implementation.
    """
    guesses, qs = [], []
    for _ in range(gamma):
        q = draft_probs(prefix + guesses)
        guesses.append(sample(q, rng))
        qs.append(q)
    contexts = [prefix + guesses[:i] for i in range(gamma + 1)]
    ps = target_batch_probs(contexts)
    accepted = gamma
    for i, token in enumerate(guesses):
        # q_i(token)>0: this token was actually drawn from q_i.
        if rng.random() > min(1.0, ps[i][token] / qs[i][token]):
            accepted = i
            break
    next_probs = ps[gamma] if accepted == gamma else residual(ps[accepted], qs[accepted])
    correction_or_bonus = sample(next_probs, rng)
    return prefix + guesses[:accepted] + [correction_or_bonus], {
        'drafts': guesses, 'accepted': accepted, 'extra': correction_or_bonus,
        'extra_kind': 'bonus' if accepted == gamma else 'correction',
    }


class FixedRandom:
    def __init__(self, values):
        self.values = iter(values)

    def random(self):
        return next(self.values)


class SamplingChecks(unittest.TestCase):
    def test_exact_probability_mass_and_wrong_fallback(self):
        pairs = [([.5, .3, .2], [.2, .5, .3]),
                 ([1., 0.], [0., 1.]),
                 ([.25, .75], [.25, .75]),
                 ([.4, .6], [.6, .4])]
        for p, q in pairs:
            mass = [min(pi, qi) for pi, qi in zip(p, q)]
            rejection = 1 - sum(mass)
            result = mass if rejection < 1e-14 else [m + rejection * r for m, r in zip(mass, residual(p, q))]
            for actual, expected in zip(result, p):
                self.assertAlmostEqual(actual, expected, places=12)
        p, q = pairs[0]
        rejection = 1 - sum(min(pi, qi) for pi, qi in zip(p, q))
        wrong = [min(pi, qi) + rejection * pi for pi, qi in zip(p, q)]
        self.assertAlmostEqual(wrong[0], .35)

    def test_all_accept_and_first_rejection_and_gamma_zero(self):
        q = lambda _: [.2, .5, .3]
        target = lambda contexts: [[.5, .3, .2] for _ in contexts]
        # Draft B,C,A; accept B, reject C; residual correction A.
        out, trace = speculative_step([], q, target, 3, FixedRandom([.4, .9, .1, .5, .9, .2]))
        self.assertEqual(out, [1, 0])
        self.assertEqual(trace['accepted'], 1)
        same = lambda contexts: [[.2, .5, .3] for _ in contexts]
        out, trace = speculative_step([], q, same, 2, FixedRandom([.1, .4, .7, .8, .9]))
        self.assertEqual(out, [0, 1, 2])
        self.assertEqual(trace['extra_kind'], 'bonus')
        out, trace = speculative_step([], q, target, 1, FixedRandom([.4, .9, .2]))
        self.assertEqual(out, [0])
        self.assertEqual(trace['accepted'], 0)
        out, trace = speculative_step([], q, target, 0, FixedRandom([.1]))
        self.assertEqual(out, [0])

    def test_joint_distribution_with_prefix_dependent_models(self):
        def p(prefix):
            return [.7, .3] if not prefix or prefix[-1] == 0 else [.2, .8]

        def q(prefix):
            return [.4, .6] if not prefix or prefix[-1] == 0 else [.8, .2]

        rng = random.Random(20261012)
        trials = 30000
        counts = Counter()
        for _ in range(trials):
            prefix = []
            while len(prefix) < 2:
                prefix, _ = speculative_step(prefix, q, lambda contexts: [p(c) for c in contexts], 3, rng)
            counts[tuple(prefix[:2])] += 1
        expected = {(a, b): p([])[a] * p([a])[b] for a in range(2) for b in range(2)}
        for seq, probability in expected.items():
            self.assertLess(abs(counts[seq] / trials - probability), .015)
        print('Joint distribution:', {str(k): round(counts[k] / trials, 4) for k in expected})
        print('Expected:', expected)


if __name__ == '__main__':
    q = lambda _: [.2, .5, .3]
    p_batch = lambda contexts: [[.5, .3, .2] for _ in contexts]
    tokens, trace = speculative_step([], q, p_batch, 3, FixedRandom([.4, .9, .1, .5, .9, .2]))
    print('Worked example:', tokens, trace)
    unittest.main(verbosity=2)
