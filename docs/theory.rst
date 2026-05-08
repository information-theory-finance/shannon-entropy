.. _theory:

Theory
======

Shannon entropy is the central object of classical information theory.  This
page develops the concept from intuition through formal definition to
implementation, covering all properties relevant to the financial application.

----

Intuition
---------

Suppose you receive a message telling you the outcome of an experiment.
How much *information* does that message carry?  If the outcome was certain
beforehand (e.g. a biased coin that always lands heads), the message carries
zero information.  If all outcomes were equally likely, the message carries
the maximum possible information.  Shannon entropy formalises this intuition
as a single number attached to the probability distribution, not the outcome.

----

Formal Definition
-----------------

Let :math:`X` be a discrete random variable taking values in a finite
alphabet :math:`\mathcal{X}` with probability mass function
:math:`p : \mathcal{X} \to [0,1]`.

.. math::

   H(X) \;=\; -\sum_{x \in \mathcal{X}} p(x)\,\log_b\,p(x)

The base :math:`b` fixes the unit of measurement.

.. list-table::
   :header-rows: 1
   :widths: 15 20 65

   * - Base
     - Unit
     - Interpretation
   * - 2
     - bits
     - Minimum number of binary questions needed on average
   * - :math:`e`
     - nats
     - Natural unit; preferred in continuous information theory
   * - 10
     - hartleys
     - Digits of base-10 surprise

----

Properties
----------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Property
     - Statement
   * - Non-negativity
     - :math:`H(X) \geq 0`, with equality iff :math:`X` is deterministic.
   * - Maximum
     - :math:`H(X) \leq \log_b |\mathcal{X}|`, achieved by the uniform PMF.
   * - Concavity
     - :math:`H` is a strictly concave function of the PMF vector :math:`p`.
   * - Chain rule
     - :math:`H(X,Y) = H(X) + H(Y \mid X)`.
   * - Data processing
     - :math:`H(f(X)) \leq H(X)` for any deterministic function :math:`f`.
   * - Continuity
     - :math:`H` is continuous in :math:`p`.
   * - Symmetry
     - :math:`H` is invariant to permutations of the alphabet.

----

Worked Example
--------------

Consider a fair four-sided die: :math:`p(x) = 0.25` for
:math:`x \in \{1,2,3,4\}`.

.. math::

   H(X) \;=\; -4 \times 0.25 \log_2 0.25
           \;=\; -4 \times 0.25 \times (-2)
           \;=\; 2 \;\text{bits}

This means, on average, you need exactly two yes/no questions to identify the
outcome (e.g. "Is it ≥ 3?" then "Is it 1 or 3?").

Now consider a biased die: :math:`p = [0.7, 0.1, 0.1, 0.1]`.

.. math::

   H(X) = -0.7\log_2 0.7 - 3 \times 0.1\log_2 0.1 \approx 1.357 \;\text{bits}

Less entropy — the die is more predictable.

----

Implementation Notes
--------------------

The reference implementation in ``utils/math_core.py`` handles two edge cases:

.. code-block:: python

   def shannon_entropy(probs, base=2.0):
       probs = np.asarray(probs, dtype=float)
       probs = probs[probs > 0]   # 0·log(0) := 0 — drop zeros
       probs /= probs.sum()       # normalise; accepts unnormalised input
       return -np.sum(probs * np.log(probs) / np.log(base))

.. note::

   The function accepts unnormalised weights, making it convenient for
   passing raw histogram counts directly without a separate normalisation step.

.. warning::

   Numerical precision: for very small probabilities (:math:`p < 10^{-300}`),
   ``np.log`` may return ``-inf``.  The zero-filtering step above prevents
   this, but extreme distributions should be handled with care.
