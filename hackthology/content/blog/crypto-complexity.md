Title: Cryptography and Complexity
Author: Tim Henderson
Date: 2013-11-11
Category: Blog

This is a conversion from a latex paper I wrote. If you want all formatting
correct or the bibliography you should read the
[pdf version]({static}/pdfs/crypto-complexity.pdf).

Cite as:

> Henderson, Tim A. D. **Cryptography and Complexity**. Unpublished. Case Western Reserve University. MATH 408.  Spring 2012.

<hr/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<p>Modern cryptographic systems are built on problems which are assumed to be computationally infeasible. Computational infeasibility means a computation which although computable would take far too many resources to actually compute. Ideally in cryptography one would like to ensure an infeasible computation&#8217;s cost is greater than the reward obtained by computing it. At first glance this seems to be an odd notion to base a cryptographic system on. Don&#8217;t we want our cryptographic systems to be totally secure? They should be unbreakable! &#8220;It may take a long time to break it,&#8221; seems like a poor guarantee of security.</p>
<p>However, it is the best guarantee which can exist in either an ideal world (from a mathematical perspective) or the physical world. As we shall see later in the survey, if several widely held assumptions turn out to be false we can not even make the guarantee of computational infeasibility.</p>
<h2>Classical Security</h2>
<p>In classical cryptographic systems, those known to the academic community prior to the publication of Diffie and Hellman&#8217;s paper <span class="citation"></span>, security assumptions were based on the results of information theory. This approach is sometimes referred to as <em>information-theoretic</em> and is concerned with whether there exists information in the <em>ciphertext</em> which originated in the <em>plaintext</em> or in the <em>key</em>. We say a system has <em>perfect-secrecy</em> if:</p>
<p><span class="math">\[\begin{aligned}
  \forall_{m \in \mathcal{M}} \forall_{c \in \mathcal{C}} \text{ : } 
  Pr[\mathcal{M} = m | \mathcal{C} = c] = Pr[\mathcal{M} = m]
  \label{perfect-secrecy}\end{aligned}\]</span></p>
<p>Intuitively this formula says an attacker gains no information about the contents of a message from the ciphertext of the message. Does this mean the attacker knows nothing about the message? Of course not! However, he doesn&#8217;t <em>learn</em> anything new about the message by closely examining the ciphertext. Therefore, the ciphertext of the message is essentially useless to an attacker. <span class="citation"></span><sup><a href="#fn1" class="footnoteRef" id="fnref1">1</a></sup></p>
<p>However, any system with <em>perfect-secrecy</em> requires the length of the key to be at least as large as the sum of the lengths of all messages encrypted with it. Since the key has to be at least as long as the messages sent such a system is of little value in practical modern situations.<span class="citation"></span><sup><a href="#fn2" class="footnoteRef" id="fnref2">2</a></sup></p>
<p>There are two practical problems with a system with <em>perfect-secrecy</em> the first is &#8220;Key Distribution.&#8221; Since the sender and receiver must use the same key they must some how <em>secretly</em> agree on a key beforehand. Therefore, there must exist some &#8220;second channel&#8221; by which the sender and receiver can communicate. The second problem has to do with the length of the key. Since it is as long as the message there seems to be only small utility in the system as the sender and receiver could conceivably securely exchange messages using their secure &#8220;second channel&#8221; they use for key distribution.</p>
<p>These to problems make the system an unrealistic system for securing (for instance) internet communications. Internet communications do not require the parties to know each other before hand and allow for no secondary secure communications channel to exist. Therefore, some other encryption methodology must be used if one wants to secure communication in this setting.</p>
<h2>Modern Security</h2>
<p>In modern system we no longer discuss security in terms of whether a system provides <em>perfect-secrecy</em>. Instead, we say if a ciphertext contains information leaked from the plaintext it should be computationally infeasible to extract that information. We can provide this property even in cases where the key is shorter than the message. This property can also be provided in cases where the attacker has access to the <em>encryption</em> key (but not of course to the <em>decryption</em> key).<span class="citation"></span><sup><a href="#fn3" class="footnoteRef" id="fnref3">3</a></sup></p>
<p>In following section [secure-encryption] we shall unpack and rigorously define (using <span class="citation"></span>&#8217;s definitions) the definition above. In particular we will look at the definition in the context of symmetric key systems. The difficulties of public key systems will also be briefly presented but without detailed exposition. However, before we get to the fun stuff we will first present complexity theory and one way functions.</p>
<h1>A Tour of Computational Complexity Theory</h1>
<p>In many ways Computability Theory, and its daughter field Complexity Theory, began with proof of the incompleteness of axiomatic systems in 1931.<span class="citation"></span> The proof is a tremendously important result in meta-mathematics stating: no recursively axiomatized mathematical system can be both complete and consistent. Thus, we cannot prove in a particular theory that the same particular theory is consistent. Indeed, if we did construct such a proof it would prove exactly the opposite. Thus, there are some mathematical sentences which are true for which no algorithm can decided on their truth value.</p>
<p>In a similar result, Alan Turing in 1937 proved that for general programs one could not decide whether the programs would halt for all inputs.<span class="citation"></span> During the previous year Alonzo Church proved the exact same thing for evaluations of <span class="math">\(\lambda\)</span>-Calculus expressions.<span class="citation"></span> Church and Turing later conjectured that the machine Turing defined (eg. Turing Machines) and Church&#8217;s lambda calculus were equivalent. All though this is an unprovable conjecture it is largely accepted today.</p>
<p>Once actual computational machines were produced (as opposed to the abstract machines of Turing and Church), programmers became interested in the notion of the <em>complexity</em> of an algorithm. The complexity of an algorithm is an expression of how much time or space or other resources the algorithm will use. The representation of time and space is abstract and placed in terms of the size of the parameters to the algorithm. Today, we use asymptotic notation to express complexity assertions. The notation was standardized by Don Knuth in 1976 but in wide (although inconsistent) use before then. It was invented by Bachmann in 1894 for use in a different context.<span class="citation"></span></p>
<p>The interest in the complexity of algorithms and work on linguistics (particularly formal language hierarchies) lead to work on classifying the &#8220;hardness&#8221; computational problems. For instance all of the language classes in the Chomsky hierarchy have hardness results. Type-0 Languages (all recursively enumerable languages) are recognizable but only non-deterministically. While, Type-3 languages (referred to as regular languages) can be recognized in linear time.<sup><a href="#fn4" class="footnoteRef" id="fnref4">4</a></sup><span class="citation"></span></p>
<p>This leads to defining complexity classes for problems (as opposed to algorithms). A complexity class typically refers to a bound on the amount time or space needed to solve the problem in the worst case. Thus, complexity classes describe how difficult a problem is to solve in general. The first general results in the theory were obtained in 1965 by Hartmanis and Stearns who defined the meaning computation complexity.</p>
<p>In particular Hartmanis and Stearns modeled their definition using the computational model of an N-Tape Turing Machine. Any computational model could have been used, and today others are used. In particular the authors prove facts about the computability of particular binary strings, <span class="math">\(\alpha\)</span> in the paper. They say <span class="math">\(\alpha\)</span> is in a complexity class <span class="math">\(S_T\)</span> if <span class="math">\(T: \mathbb{N} \rightarrow \mathbb{N}\)</span> is a monotone increasing function and there exists a Turing machine <span class="math">\(\mathcal{M}\)</span> such that <span class="math">\(\mathcal{M}\)</span> computes the <span class="math">\(n\)</span>th term in <span class="math">\(T(n)\)</span> steps.</p>
<p>What does this definition mean intuitively? Think of <span class="math">\(T\)</span> as a time function, where time is a function of the number bits generated. A string can belongs to those complexity classes which can compute the string according to the complexity class&#8217;s specified time function. Thus, by specifying some general time functions such as (<span class="math">\(1\)</span>, <span class="math">\(n\)</span>, <span class="math">\(n^2\)</span> &#8230;, <span class="math">\(2^n\)</span>) one can begin classifying bit-strings. The bit-strings correspond to problem solutions. For a simple example consider the bit-string which corresponds to all prime numbers. To compute it, one would need to actually compute exactly those numbers which are prime.<span class="citation"></span></p>
<p>The type of problem Hartmanis and Stearns classified belongs to the class of problems known as Decision Problems. Informally, decision problems are problems to which there is a &#8220;yes/no&#8221; answer. For instance, deciding whether the first <span class="math">\(n\)</span> bits of a string is in a language, <span class="math">\(\mathcal{L} \subseteq \{0,1\}^*\)</span>, is a decision problem. Complexity classes are more general than just decision problems however, one can construct complexity classes for any type of computational problem, optimizations problems for instance.</p>
<h2>The Class NP</h2>
<p>Of particular importance to mathematics, computer science and this paper in particular is the complexity class NP (Non-Deterministic Polynomial Time). The class of NP is defined (intuitively) as those problems which have easily verifiable solutions. What does it mean for a solution to be &#8220;easily verifiable.&#8221; It means given the problem instance and the solution one can check the validity of the solution in <span class="math">\(O(n^k)\)</span> where <span class="math">\(n\)</span> is parameterized by the problem and <span class="math">\(k\)</span> is a constant.</p>
<p>More formally, the class NP is defined in terms of formal languages. Let <span class="math">\(\Sigma\)</span> be an alphabet and <span class="math">\(\Sigma_{0}\)</span> be <span class="math">\(\Sigma - \{*\}\)</span> where <span class="math">\(*\)</span> is the empty symbol. Let <span class="math">\(\Sigma_{0}^{*}\)</span> be the closure of all finite strings made up of symbols in <span class="math">\(\Sigma_{0}\)</span>. We define a language, <span class="math">\(\mathcal{L}\)</span>, as <span class="math">\(\mathcal{L} \subseteq \Sigma_{0}^{*}\)</span>.</p>
<p>The Class NP<sup><a href="#fn5" class="footnoteRef" id="fnref5">5</a></sup></p>
<blockquote>
<p>A language, <span class="math">\(\mathcal{L}\)</span>, belongs to NP if there exists a Deterministic Turing Machine, <span class="math">\(\mathcal{M}\)</span>, a polynomial, <span class="math">\(p(n)\)</span> &#8211; such that <span class="math">\(p(n)\)</span> defines the complexity class of <span class="math">\(\mathcal{M}\)</span><sup><a href="#fn6" class="footnoteRef" id="fnref6">6</a></sup> &#8211; and on any input <span class="math">\(x
    \in \Sigma_{0}^{*}\)</span>:</p>
<ul>
<li><p>if <span class="math">\(x \in \mathcal{L}\)</span> then there exists a <em>certificate</em>, <span class="math">\(y
            \in \Sigma_{0}^{*} \text{ st. } |y| \leq p(|x|)\)</span>, and <span class="math">\(\mathcal{M}\)</span> accepts the input string <span class="math">\(xy\)</span>.</p></li>
<li><p>if <span class="math">\(x \notin \mathcal{L}\)</span> then for any string, <span class="math">\(y \in
            \Sigma_{0}^{*}\)</span>, <span class="math">\(\mathcal{M}\)</span> rejects the input string <span class="math">\(xy\)</span>.</p></li>
</ul>
</blockquote>
<p>The given definition does not discuss Non-Determinism. To see the role of Non-Determinism consider constructing solutions (certificates) to problem instances (the string x in the definition). If certificates can be chosen and examined non-deterministically then it will take only polynomial time to find a solution. However, if we are testing every possible certificate deterministically it will take <span class="math">\(\vert \Sigma_0\vert ^{p(\vert x\vert )}\)</span> examinations, a combinatorial explosion. Thus, problems in NP have solutions which are easy to verify but not necessarily easy to construct.</p>
<h2>The Class P</h2>
<p>The complexity class P (Polynomial Time) is exactly those problems solvable in deterministic polynomial time. More formally,</p>
<p>The Class P<sup><a href="#fn7" class="footnoteRef" id="fnref7">7</a></sup></p>
<blockquote>
<p>Let <span class="math">\(\Pi\)</span> be a decision problem. Let <span class="math">\(L_{\Pi} = \{ x \in \Sigma_0^* |
    \text{x is an encoding of an instance of } \Pi \}\)</span>, that is, <span class="math">\(L_{\Pi}\)</span> is the language of <span class="math">\(\Pi\)</span>. We can then define the class P as:</p>
<p><span class="math">\[\begin{aligned}
      P = \{ L \subseteq \Sigma_0^* |&amp; \text{ there is a Deterministic Turing} 
        \text{ Machine, } \mathcal{M} \text{, and a polynomial, } \\
        &amp;p(n) \text{, } \text{such that } T_{\mathcal{M}} \leq p(n) 
        \text{ for all } n \geq 1 \}
    \end{aligned}\]</span></p>
</blockquote>
<p>A language is in P if one can construct a Turing Machine which accepts it (and rejects all non-members) in time less than some polynomial (with respect to the size of the input).</p>
<p>All those problems which belong to P are considered easily solvable, or tractable. While, they are &#8220;easy&#8221; one should not make the mistake of assuming they are simple. Given a polynomial time algorithm which solves a problem one can easily solve it. However, even if you know a polynomial time algorithm exists for a problem constructing the algorithm may be difficult.</p>
<h2>P vs.&#160;NP</h2>
<p>What is the relationship between P and NP? It is known P is contained in NP (ie. <span class="math">\(P \subseteq NP\)</span>). However, whether <span class="math">\(NP \subseteq P\)</span> is true is one of the greatest open questions in applied mathematics. The class P containment inside of NP is obvious: if we can find a solution in polynomial time it is certainly verifiable in polynomial time. To show NP is contained within P one would need to show every problem in NP can be solved with a polynomial time algorithm.</p>
<p>The methodology for solving P vs NP with the greatest impact relies on the idea of <em>reduction</em>. We say problem, <span class="math">\(\Pi_1\)</span> is <em>reducible</em> to another problem, <span class="math">\(\Pi_2\)</span>, if one can find a mapping from every instance of <span class="math">\(\Pi_1\)</span> to equivalent instances of <span class="math">\(\Pi_2\)</span> such that the solutions to the constructed instances of <span class="math">\(\Pi_2\)</span> correspond to solutions of <span class="math">\(\Pi_1\)</span>. A reduction is a <em>polynomial reduction</em> if the mapping can be done in polynomial time. A problem, <span class="math">\(\Pi_1\)</span>, is as &#8220;hard&#8221; as another problem, <span class="math">\(\Pi_2\)</span>, if <span class="math">\(\Pi_2\)</span> can be <em>reduced</em> to <span class="math">\(\Pi_2\)</span>. Thus, hardness is a relational notion. Problems are not intrinsically hard, they are hard with respect to other problems.</p>
<p>To prove P contains NP one could prove the hardest problem in NP is also in P. By the definition of hardness above, if a problem, <span class="math">\(\Pi_h\)</span>, is the hardest problem in NP than every other problem in NP is reducible to <span class="math">\(\Pi_h\)</span>. Problems which are at least as hard as every problem in NP are know as NP-Hard problems. A problem does not need to be in NP to be NP-Hard. However, if a problem is NP-Hard and it is in NP then it is called an NP-Complete problem.</p>
<p>NP-Complete problems exist and their existence is one of the greatest results in complexity theory. It was proved by Stephen Cook in 1971 who found the first NP-Complete problem. The problem he found is known as SAT (for satisfiability of boolean formulas). He proved any problem solvable in polynomial time by a Nondeterministic Turing Machine can be reduced to finding whether or not a boolean formula is satisfiable.<span class="citation"></span> Cook&#8217;s result launched a wave of research. The very next year Richard Karp proved 21 other problems were also NP-Complete.<span class="citation"></span></p>
<p>While there have many hundreds of problems proven to be NP-Complete since Cook proved SAT, there have been only fruitless attempts to prove P does or does not contain NP. The leading consensus in the complexity community is P does not contain NP. Furthermore, since it appears work on proving P contains NP is permanently stalled one can safely assume NP-Hard problems are in some platonic sense actually difficult to solve.</p>
<h2>Infeasibility</h2>
<p>A sharper definition of computational infeasibility can now be given with definitions of Complexity Classes, P, and NP in hand. Recall the opening statement on infeasibility, where we defined an infeasible computation to be one requiring too many resources to actually compute. If one has encrypted a message one would ideally like the ciphertext to be unreadable. If the message is a solution to an NP-Complete problem then the ciphertext could be the problem instance and therefore can only be decrypted by solving the NP-Complete problem. However, assuming NP is not contained in P, the NP-Complete problem will take time proportional to <span class="math">\(\vert \Sigma_0^*\vert ^{\vert x\vert }\)</span> (where x is the ciphertext) to solve.</p>
<p>Therefore, a new working definition of an infeasible computation is a &#8220;hard&#8221; instance of an NP-Hard problem of sufficient size. What is sufficient size? Any size which leads to <span class="math">\(\vert \Sigma_0^*\vert ^{\vert x\vert }\)</span> to be so large as to be uncomputable. An example of such as size might be <span class="math">\(160\)</span> since trying <span class="math">\(2^{160}\)</span> possible solutions is not expected to ever be computable with classical computers in time less than the age of the universe. What is a &#8220;hard&#8221; instance? A hard instance is one in which there exists no better way to find a solution than trying all possible solutions. Not every instance of a hard problem is hard to solve. Specifying an infeasible computation requires a hard instance is a necessary restriction.</p>
<h2>Probabilistic Infeasibility</h2>
<p>In the previous section it was assumed all computations were exact. No computation <em>sometimes</em> gave the right answer and sometimes did not. However, with an algorithm which mostly gives right answers could be very useful to the cryptanalyst. Therefore, we briefly turn our attention to probabilistic computations.</p>
<h3>Probabilistic Turing Machines</h3>
<p>A Probabilistic Turing Machine (PTM) is a Deterministic Turing Machine (DTM) with an extra input tape. The tape is called the &#8220;coin flipping tape.&#8221; The PTM can read one bit of information at a time from the coin flipping tape. Each bit is assured to be a random bit.<sup><a href="#fn8" class="footnoteRef" id="fnref8">8</a></sup> Computation on the machine proceeds as before except at any time a random choice can be made. This allows us to construct algorithms which will &#8220;probably&#8221; but not necessarily produce the desired answer.</p>
<p>Analyzing the running time of a PTM is a bit different than a DTM. While a DTM&#8217;s running time only depends on its program and the initial configuration of the input tape, a PTM also depends on the random bits it reads during the computation. Therefore, the running time of a PTM is a random variable (we denote it as <span class="math">\(t_{\mathcal{M}}(x)\)</span>). Furthermore, whether a PTM halts or not on a fixed input is also a random variable. A <em>halting</em> PTM is one which halts after a finite number of steps for all inputs and all configurations of the coin tossing tape.</p>
<p>With the definition a <em>halting</em> PTM in hand we are now prepared to reason about its running time. Worst case running time of a PTM, <span class="math">\(T_{\mathcal{M}}(n)\)</span>, is:</p>
<p><span class="math">\[\begin{aligned}
  T_{\mathcal{M}}(n) = \text{max} \{ t \text{ } | \text{ there exists a } 
                       x \in \Sigma^{n}_{0} \text{ such that } 
                       \text{Pr}[t_{\mathcal{M}}(x) = t] &gt; 0 \}\end{aligned}\]</span></p>
<p>Informally, this definition states: the worst case running time of a PTM is the maximum running time, <span class="math">\(t_{\mathcal{M}}(x)\)</span>, for which the machine will run with some probability greater than zero. A polynomial PTM is one in which there exists some positive polynomial, <span class="math">\(p(\cdot)\)</span>, such that <span class="math">\(T_{\mathcal{M}}(n) \le p(n)\)</span> holds.<span class="citation"></span><sup><a href="#fn9" class="footnoteRef" id="fnref9">9</a></sup></p>
<p>BPP, Bounded Probability Polynomial Time</p>
<blockquote>
<p>A language <span class="math">\(\mathcal{L}\)</span> is recognized by a polynomial PTM, <span class="math">\(\mathcal{M}\)</span>, if:</p>
<ul>
<li><p><em>for every <span class="math">\(x \in \mathcal{L}\)</span> it holds that</em> Pr<span class="math">\([\mathcal{M} \text{ accepts } x] \ge \frac{2}{3}\)</span></p></li>
<li><p><em>for every <span class="math">\(x \notin \mathcal{L}\)</span> it holds that</em> Pr<span class="math">\([\mathcal{M} \text{ does not accept } x] \ge \frac{2}{3}\)</span></p></li>
</ul>
<p>BPP is the class of languages recognized by a polynomial PTM.<sup><a href="#fn10" class="footnoteRef" id="fnref10">10</a></sup><sup><a href="#fn11" class="footnoteRef" id="fnref11">11</a></sup></p>
</blockquote>
<p>The class Bounded Probability Polynomial Time, sometimes called Bounded-<em>Error</em> Probabilistic Polynomial Time, is somewhat analogous to the class P. Computations in BPP are considered feasible computations. The class P is contained within BPP, <span class="math">\(P \subseteq BPP\)</span>. However, the relationship between NP and BPP has not been established. In practice cryptographers assume <span class="math">\(NP \nsubseteq BPP\)</span> which implies <span class="math">\(NP \neq P\)</span>. All problems unsolvable by a polynomial PTM are considered infeasible, of which NP-Hard problems are a special case. As before, some instances of hard problems may in fact be easy to solve.</p>
<p>Infeasible computations as defined above are nice formalisms but do not seem too useful. To utilize the previous definition one has to answer the following question: Given and instance of a problem is it a <em>hard</em> instance? Unfortunately, we don&#8217;t know how to answer this question.<sup><a href="#fn12" class="footnoteRef" id="fnref12">12</a></sup> As we will see later, if we could easily find hard instances we could construct a simple and secure crypto-system by sampling hard instances. Therefore, cryptographers need better assurances than <em>worst-case</em> assurances; a cryptographer needs to know a typical instance of a problem is hard.<span class="citation"></span></p>
<h1>One Way Functions</h1>
<p>With a firm grounding in Complexity Theory, we turn our attention to cryptography. First, by capturing the notion of exploitable computational difficulty as epitomized in the one way function. A one way function is a function which is <em>easy</em> to compute but <em>hard</em> to invert. More specifically:</p>
<p>One Way Function [owf]</p>
<blockquote>
<ol>
<li><p><span class="math">\(\forall_x\)</span> computing <span class="math">\(f(x) = y\)</span> is <em>easy</em> to compute.</p></li>
<li><p><span class="math">\(\forall_y\)</span> computing <span class="math">\(f^{-1}(y)\)</span> such that <span class="math">\(f(x) \in f^{-1}(y)\)</span> is <em>hard</em> to compute.</p></li>
</ol>
</blockquote>
<p>The one way function in definition [owf] is more of a theoretical construct than an actual mathematical construct. Therefore, it uses the notion of <em>easy</em> and <em>hard</em> computations without grounding itself with exact definitions. One can think of this first definition as an abstract, or ideal, definition.</p>
<p>Ignoring for the moment the definitional problems, what use is a one way function to the cryptographer? It turns out one can define secure cryptosystems with one way functions. Such a cryptosystem will be discussed in detail in section [secure-encryption]. For now consider this simple example of the power of the idea:</p>
<blockquote>
<p>One day while toiling away, Ian had a flash of insight which would put his mechanical workings to right. A machine danced in his mind, one which would make widgets faster and better than before. So clever his insight he knew no one else would easily come up with the same idea. Thus, he decided not to patent it. Instead, he wrote down his idea and ran it through a one way function producing <span class="math">\(y\)</span> his certificate of his idea. He then published <span class="math">\(y\)</span> widely, placing it in all the libraries around the country.</p>
<p>Many years passed and Mallory stole Ian&#8217;s idea. Mallory being very clever sought to undue Ian and patented the idea. Then, he sued Ian for patent infringement. But, since Ian had a certificate of his invention, <span class="math">\(y\)</span>, he could prove to the court he had invented and known about the idea long before Mallory had filed for the patent. The court agreed with Ian and invalidated Mallory&#8217;s patent.</p>
</blockquote>
<p>The challenge in section [secure-encryption] will be transforming the one way function into a workable encryption device. For while a powerful concept, as demonstrated by the story above, it is non-obvious how a crypto-system can be constructed from it. But before crypto-systems, the definition must be tightened. Furthermore, one must be convinced one way functions can be reasonably expected to exist.</p>
<h2>Strong One Way Functions</h2>
<p>There are two vague terms used in definition [owf], <em>easy</em> and <em>hard</em> computations. Fortunately, we have already defined what an <em>easy</em> computation is: an easy computation is on which can be done in (probabilistic) polynomial time. But what about inversion? What does it mean for a function to be hard to invert? A function, <span class="math">\(f\)</span>, is hard to invert if every probabilistic polynomial time algorithms will only invert <span class="math">\(f\)</span> with <em>negligible</em> probability.</p>
<p>Negligible<sup><a href="#fn13" class="footnoteRef" id="fnref13">13</a></sup> [neg]</p>
<blockquote>
<p>A function, <span class="math">\(\mu : \mathbb{N} \rightarrow \mathbb{R}\)</span>, is negligible if for every positive polynomial, <span class="math">\(p(\cdot)\)</span>, there exists an <span class="math">\(N\)</span> such that for all <span class="math">\(n &gt; N\)</span>,</p>
<p><span class="math">\[\begin{aligned}
      \mu(n) &lt; \frac{1}{p(n)}
    \end{aligned}\]</span></p>
</blockquote>
<p>The definition of negligible is reminiscent of Asymptotic Notation used in the analysis of algorithms. It concerns itself with the behavior of the function, <span class="math">\(\mu(n)\)</span>, when <span class="math">\(n\)</span> grows large. An additional, and useful, feature of the definition is any negligible function remain negligible after multiplication with any polynomial <span class="math">\(q(\cdot)\)</span>. Therefore, any event which occurs with negligible probability will continue to occur with negligible probability even after polynomial repetitions. Thus, if <span class="math">\(f\)</span> is only invertible with polynomial time algorithm, <span class="math">\(A\)</span>, with negligible probability than no polynomial repetition of <span class="math">\(A\)</span> will be likely to invert <span class="math">\(f\)</span>.</p>
<p>Strong One Way Functions<sup><a href="#fn14" class="footnoteRef" id="fnref14">14</a></sup> [strong-owf]</p>
<blockquote>
<p>A function, <span class="math">\(f : \{0,1\}^* \rightarrow \{0,1\}^*\)</span>, is <strong>strongly</strong> one way if it is:</p>
<dl>
<dt>Easy to compute</dt>
<dd><p>There exists a (deterministic) polynomial time algorithm A such that on input x algorithm A outputs <span class="math">\(f(x)\)</span> (ie. <span class="math">\(A(x) =
      f(x)\)</span>).</p>
</dd>
<dt>Hard to invert</dt>
<dd><p>For <em>every</em> probabilistic polynomial time algorithm <span class="math">\(A&#39;\)</span>, every positive polynomial <span class="math">\(p(\cdot)\)</span>, and all sufficiently large <span class="math">\(n\)</span> the probability <span class="math">\(A&#39;\)</span> inverts <span class="math">\(f\)</span> is negligible. That is:</p>
<p><span class="math">\[\begin{aligned}
        \text{Pr}[A&#39;(f(x)) \in f^{-1}(f(x))] &lt; \frac{1}{p(n)}
      \end{aligned}\]</span></p>
</dd>
</dl>
</blockquote>
<p>In the above definition &#8220;input x&#8221; should be considered as a random variable drawn from a uniform distribution over <span class="math">\(\{0,1\}^n\)</span>. Thus, the second condition reads: for any random input of size <span class="math">\(n\)</span> the probability an arbitrary polynomial time algorithm will find a pre-image is negligible. If such a function could be found or constructed it would offer a strong assurance of computational difficulty.</p>
<h2>Weak One Way Functions</h2>
<p>While strong one way functions ensure any efficient inversion algorithm has only a negligible likelihood of succeeding; weak one way functions require efficient inversion algorithms will fail with a non-negligible probability.</p>
<p>Weak One Way Functions<sup><a href="#fn15" class="footnoteRef" id="fnref15">15</a></sup> [weak-owf]</p>
<blockquote>
<p>A function, <span class="math">\(f : \{0,1\}^* \rightarrow \{0,1\}^*\)</span>, is <strong>weakly</strong> one way if it is:</p>
<dl>
<dt>Easy to compute</dt>
<dd><p>There exists a (deterministic) polynomial time algorithm A such that on input x algorithm A outputs <span class="math">\(f(x)\)</span> (ie. <span class="math">\(A(x) =
      f(x)\)</span>).</p>
</dd>
<dt>Slightly hard to invert</dt>
<dd><p>There exists a polynomial <span class="math">\(p(\cdot)\)</span> such that for every probabilistic polynomial time algorithm, <span class="math">\(A&#39;\)</span>, and a sufficiently large <span class="math">\(n\)</span>&#8217;s,</p>
<p><span class="math">\[\begin{aligned}
        \text{Pr}[A&#39;(f(x)) \notin f^{-1}(f(x))] &gt; \frac{1}{p(n)}
      \end{aligned}\]</span></p>
</dd>
</dl>
</blockquote>
<p>In definition [strong-owf] the probability that <span class="math">\(A&#39;\)</span> could invert <span class="math">\(f\)</span> has an upper bound of <span class="math">\(p(\cdot)^{-1}\)</span> for <em>every</em> positive polynomial. In definition [weak-owf], there is a <em>single</em> positive polynomial, <span class="math">\(p(\cdot)\)</span>, such that <span class="math">\(p(\cdot)^{-1}\)</span> is a lower bound on the failure of any efficient inversion algorithm. Unlike strong one way functions, weak one way functions are not hard for typical instances. However, they are hard for some percentage of instances.</p>
<h3>Amplification of Weak One Way Functions</h3>
<p>Since weak functions are hard for a non-negligible percentage of inputs they can be used to construct strong functions. The proof for this bold assertion is given by Goldreich.<span class="citation"></span><sup><a href="#fn16" class="footnoteRef" id="fnref16">16</a></sup> Since one can convert a weak one way function into a strong one it suffices to find weak ones. While a strongly one way function may yield a more efficient cryptosystem a weak one will still allow a secure system (as discussed in section [secure-encryption]).</p>
<h2>Hard Core Predicates</h2>
<p>If Alice has a strong one way function <span class="math">\(f\)</span>, computes <span class="math">\(y = f(x)\)</span>, and sends <span class="math">\(y\)</span> to Bob while Eve eavesdrops what can Eve learn about <span class="math">\(x\)</span>? Depending on the function <span class="math">\(f\)</span> Eve may be able to learn a surprising amount. Since <span class="math">\(f\)</span> is hard to invert Eve cannot learn everything about <span class="math">\(x\)</span> but she may not need too. Is there some way to quantify which bits of <span class="math">\(x\)</span> Eve can learn about and which bits she can&#8217;t?</p>
<p>There is! The bits which are hard for a polynomial attacker (like Eve) to learn about are called the &#8220;Hard Core&#8221; of a one way function. A predicate is a yes/no question, for example: Does <span class="math">\(x\)</span> end with a 0? If a yes/no question is hard for Eve to answer it is called a Hard Core Predicate. Since a yes/no question only has 2 possible answers Eve can always guess the answer. Therefore, a predicate is only hard for her to answer if she can&#8217;t do better than get it right about half the time. To be precise:</p>
<p><span class="math">\[\begin{aligned}
  \text{Pr}[\text{EveGuess\_P}(y) = P(x)] \le \frac{1}{2} + neg(|x|)\end{aligned}\]</span></p>
<p>where <span class="math">\(neg(\vert x\vert )\)</span> is a negligible function (as defined in definition [neg]). This description of Eve trying to guess something about <span class="math">\(x\)</span>, like whether it starts with 0, leads nicely into a formal definition:</p>
<p>Hard-Core Predicates<sup><a href="#fn17" class="footnoteRef" id="fnref17">17</a></sup> [hardcore]</p>
<blockquote>
<p>A polynomial time computable predicate, <span class="math">\(b : \{0,1\}^* \rightarrow
    \{0,1\}\)</span>, is called a <strong>hard-core</strong> of a function, <span class="math">\(f\)</span>, if for every probabilistic polynomial time algorithm <span class="math">\(A&#39;\)</span>, every positive polynomial <span class="math">\(p(\cdot)\)</span>, and all sufficiently large <span class="math">\(|x|\)</span>&#8217;s,</p>
<p><span class="math">\[\begin{aligned}
      \text{Pr}[A&#39;(f(x)) = b(x)] &lt; \frac{1}{2} + \frac{1}{p(|x|)}
    \end{aligned}\]</span></p>
</blockquote>
<p>Given a hard to invert function, <span class="math">\(f\)</span>, one knows some of the bits in its input must be hard to predict from the output. How does one know which bits are the hard bits? In general deciding what bits are hard for a function is difficult but one can always construct a Hard-Core Predicate for any strong one way function. Since one can always construct a strong one way function from a weak function this poses no limitation to the framework.</p>
<h3>Constructing Hard-Core Predicates</h3>
<p>The following result was first proved in 1982 by Yao but we present a simplification due to Goldreich and Levin as presented by Talbot and Welsh.<span class="citation"></span><sup><a href="#fn18" class="footnoteRef" id="fnref18">18</a></sup> A detailed proof is available as usual in the Goldreich book.<span class="citation"></span><sup><a href="#fn19" class="footnoteRef" id="fnref19">19</a></sup></p>
<p>Hard-Core Predicates from Strong One Way Functions [con-hard]</p>
<blockquote>
<p>Let <span class="math">\(f\)</span> be an arbitrary strong one way function. Let <span class="math">\(g\)</span> be defined as <span class="math">\(g(x, r) = (f(x), r)\)</span>, where <span class="math">\(|x| = |r|\)</span>. Let <span class="math">\(r\)</span> be a random bit string. Then define <span class="math">\(B(x, r)\)</span> to be a Hard-Core Predicate of <span class="math">\(g\)</span> by:</p>
<p><span class="math">\[\begin{aligned}
      B(x,r) &amp;= \sum\limits^{|x|}_{i=1} x_i r_i \imod{2} \\
             &amp;= \bar{x} \cdot \bar{r} \imod{2} 
    \end{aligned}\]</span></p>
</blockquote>
<p>The theorem states, if <span class="math">\(f\)</span> is strongly one way then it will be hard to guess the result of taking an exclusive-or of a random subset of <span class="math">\(x\)</span> given <span class="math">\(f(x)\)</span> and the subset <span class="math">\(r\)</span>. If <span class="math">\(B(x,r)\)</span> is not a hard-core of <span class="math">\(g\)</span> then <span class="math">\(f\)</span> is easily invertible. The proof involves constructing an algorithm from the predictor for <span class="math">\(B\)</span>. For details on the construction once again see Goldreich.</p>
<p>With the result of theorem [con-hard] and the ability to construct strong one way functions from weak one way functions one will always be able to construct a function where at least one predicate on <span class="math">\(x\)</span> is hard to compute. If one bit is not enough it turns out <em>hard-core functions</em> are also constructable. However, their specific details are well out of the scope of this paper.</p>
<h2>Constructing One Way Functions</h2>
<p>It one is going to build a crypto-system based on hard computational problems (specifically strong one way functions) one should have some way of identifying such problems. From a practical perspective there are three number theoretic based problems which are assumed to be one way functions. The first is the discrete log problem: <span class="math">\(g^x \equiv y \imod{p}\)</span>, second finding square roots mod <span class="math">\(N = pq\)</span>, and third the &#8220;RSA&#8221; problem <span class="math">\(c \equiv x^e \imod{N}\)</span>. While these problems are likely to be used in practice none of them are suspected to be in the class NP-Hard. While, instances of problems in NP-Hard may be efficiently solvable there is good evidence they are not. In contrast these problems are potentially vulnerable to good approximation algorithms.</p>
<p>Thus, an open problem for the aspiring cryptographer to tackle is to suggest a novel one way function. However, serious care needs to be exercised when suggesting such a function. It is not good enough for the function to be difficult in the <em>worst-case</em> it must be difficult in the typical case. Average case complexity analysis relies heavily on the input distribution. Thus, the input distribution must be carefully characterized and uniform sampling techniques must be developed. Without exercising such care the aspiring cryptographer may fall into the trap of defining something which appears secure from a cursory theoretical glance but on close inspection is quite vulnerable.</p>
<h1>Secure Encryption</h1>
<p>[secure-encryption]</p>
<p>Secure encryption schemes are naturally built on top of strong one way functions with hard-core predicates. However, before the encryption schemes can be defined a formal definition of security must be stated. Until now, our definition has been colloquial: information in the ciphertext should be computationally infeasible to extract. The informal definition is too vague for use in defining an encryption system because the security definition is more important than the cryptographic system itself. A proper definition ensures systems conforming to the definition will be more difficult to attack.</p>
<h2>Security Definitions</h2>
<p>[sec-def]</p>
<p>Before rigorously defining a modern definition of security let us turn once again to classical security and <em>perfect-secrecy</em>. Recall perfect secrecy says an attackers <em>uncertainty</em> about a message should not be reduced when in possession of a corresponding ciphertext. As noted in the introduction, the obvious criticism of <em>perfect-secrecy</em> is the implied key length. In such a system, the length of the key must be at least as long as the message. Making the definition impractical for most modern uses of cryptography. Therefore, a new definition is indeed necessary.</p>
<h3>Polynomial Indistinguishability</h3>
<p>The first definition we will consider is <em>polynomial-indistinguishability</em>. Informally, if Alice has two messages, <span class="math">\(M_1\)</span> and <span class="math">\(M_2\)</span> and she sends Bob a ciphertext, <span class="math">\(C\)</span>, Eve who has been given both messages and the ciphertext will have no easy way to determine which message it corresponds to. Something is easy for Eve if she can do it in probabilistic polynomial time. Indeed, it is assumed none of our characters can do any computations except easy ones. Formally,</p>
<p>Polynomial Indistinguishability of Encryptions<sup><a href="#fn20" class="footnoteRef" id="fnref20">20</a></sup></p>
<blockquote>
<p>An encryption scheme, <span class="math">\((G, E, D)\)</span>, where <span class="math">\(G\)</span> generates keys, <span class="math">\(E\)</span> encrypts messages, and <span class="math">\(D\)</span> decrypts messages has <em>indistinguishable encryptions</em> if for every probabilistic polynomial time algorithm, <span class="math">\(A&#39;\)</span>, every polynomial <span class="math">\(p(\cdot)\)</span>, all sufficiently large <span class="math">\(n\)</span>, and every <span class="math">\(x,y \in
    \{0,1\}^{\text{poly}(n)}\)</span> with <span class="math">\(|x| = |y|\)</span>,</p>
<p><span class="math">\[\begin{aligned}
      | \text{Pr}[A&#39;(E_{G(1^n)}(x)) = 1] - 
        \text{Pr}[A&#39;(E_{G(1^n)}(y)) = 1] |  &lt;  \frac{1}{p(n)}
    \end{aligned}\]</span></p>
</blockquote>
<p>The above definition was written with a symmetric encryption and decryption keys. However, the public key version only has minor and unimportant complications. The importance of the definition is in the intuition. Eve, the attacker, knows both messages and she has a ciphertext. The only thing she does not know is the key used to create the ciphertext. If the system is polynomially indistinguishable then Eve can only guess which message the ciphertext corresponds to. Since there are two messages she will only get it right half the time. If she can get it right better than half the time then the system is <em>not</em> polynomially indistinguishable.</p>
<p>The <em>security</em> of the definition is perhaps non-obvious but consider the case were Eve can distinguish which message the ciphertext corresponds too. If the system was supposed to have <em>perfect-secrecy</em> then clearly the secrecy would have been violated. Some bit of information would be leaking from the message to the ciphertext. Therefore, what the definition is saying is no information is leaking from the message to the ciphertext which can be extracted in polynomial time.</p>
<h3>Semantic Security</h3>
<p>The intuitive explanation of polynomial indistinguishability is captured in an alternative definition: <em>semantic-security</em>. A crypto-system is semantically secure if any piece of information Eve can compute given a ciphertext she could just as easily compute without the ciphertext. That is, the ciphertext provides Eve with no advantage for computing any piece of information of interest to her. Formally,</p>
<p>Semantic Security<sup><a href="#fn21" class="footnoteRef" id="fnref21">21</a></sup></p>
<blockquote>
<p>An encryption scheme, <span class="math">\((G, E, D)\)</span>, where <span class="math">\(G\)</span> generates keys, <span class="math">\(E\)</span> encrypts messages, and <span class="math">\(D\)</span> decrypts messages is <em>semantically secure</em> if for every probabilistic polynomial time algorithm, <span class="math">\(A\)</span>, there exists another probabilistic polynomial time algorithm, <span class="math">\(A&#39;\)</span>, such that for every message <span class="math">\(\mathcal{M}\)</span> of length <span class="math">\(n\)</span>, every pair of functions with polynomially bounded output <span class="math">\(f,h : \{0,1\}^* \rightarrow \{0,1\}^*\)</span>, every polynomial <span class="math">\(p(\cdot)\)</span>, and all sufficiently large <span class="math">\(n\)</span>,</p>
<p><span class="math">\[\begin{aligned}
      \text{Pr}[A(1^n, E_{G_1(1^n)}(\mathcal{M}), h(1^n, \mathcal{M})] =
                                                        f(1^n,\mathcal{M})] \\
                                  &lt;
      \text{Pr}[A&#39;(1^n, h(1^n, \mathcal{M})] = f(1^n,\mathcal{M})] +
                                                        \frac{1}{p(n)}
    \end{aligned}\]</span></p>
</blockquote>
<p>In the above definition, <span class="math">\(f\)</span> represents the information Eve would like to compute. The information Eve wants, <span class="math">\(f\)</span>, is a function of the message and the length of the message (encoded for technical reasons in unary). The output of <span class="math">\(f\)</span> is polynomial however it is not necessary for <span class="math">\(f\)</span> to be a <em>computable</em> function. The algorithm <span class="math">\(A\)</span> guesses <span class="math">\(f\)</span> using the ciphertext, the length of the message, and <span class="math">\(h\)</span>. The algorithm <span class="math">\(A&#39;\)</span> guesses <span class="math">\(f\)</span> using only the length of the message and <span class="math">\(h\)</span>. The function <span class="math">\(h\)</span> represents a polynomial amount of <em>a-priori</em> knowledge about the output of <span class="math">\(f\)</span>.</p>
<p>The definition of semantic security intuitive says the probability Eve can guess <span class="math">\(f\)</span> utilizing the ciphertext is at most negligibly greater than guessing <span class="math">\(f\)</span> without the ciphertext. The definition places no restrictions on what Eve might be guessing (other than an upper bound on its size). Eve could be guessing whether the message is an order to move troops, or the message is a bank account number; it makes no difference to the definition.</p>
<p><em>Semantic-security</em> is therefore the complexity theory analog of <em>perfect-secrecy</em>. It provides assurance to the cryptographer that a polynomially bound cryptanalyst will be able to gain no information from the ciphertext. In practice, one only cares about polynomially bound adversaries since exponential adversaries do not exist.</p>
<h3>Equivalence of Definitions</h3>
<p>In a potentially surprising result it turns out it doesn&#8217;t matter which security definition one uses, they imply each other:</p>
<p>Equivalence of Definitions<sup><a href="#fn22" class="footnoteRef" id="fnref22">22</a></sup> [equiv-thm]</p>
<blockquote>
<p>An encryption scheme is semantically secure if and only if it has indistinguishable encryptions.</p>
</blockquote>
<p>In practice, it is usually far easier to prove a scheme has indistinguishable ciphertexts. However, from a security perspective the property one actually wants is <em>semantic-security</em>. Thus, theorem [equiv-thm] provides the cryptographer with an incredibly useful result.</p>
<h2>A Secure Symmetric Key Encryption Scheme</h2>
<p>To construct a perfectly secret symmetric key encryption scheme from an information theory perspective one first obtains a large amount of random information. One then takes a random bit for each bit of message and exclusive-ors them together. One now has the perfect cryptographic system. The construction of a semantically secure system is quite similar (in the case of stream ciphers). One takes a bit of random information, referred alternately as the seed of the key, stretches it to create a pseudo-random sequence the same length as the message. The message and the pseudo-random sequence are then xored together. This encryption scheme will clearly be semantically secure if no adversary can distinguish between the pseudo-random sequence and a truly random sequence.</p>
<h3>Pseudo-Random Sequence Generators</h3>
<p>A pseudo-random bit generator, <span class="math">\(G(x)\)</span> is defined as a deterministic polynomial time algorithm taking a bit-string, <span class="math">\(x \in \{0,1\}^k\)</span>, and outputting a longer string <span class="math">\(G(x)\)</span>. In other words, the generator stretches the input. For the generator to be pseudo-random in nature, the output must be unpredictable if the input is random. Luckily, we already know how to produce bits which are essentially unguessable by a polynomial adversary. Hard-core predicates by construction cannot be guessed correctly better than half the time.</p>
<p>A Pseudo-Random Generator can be Constructed from any One Way Permutation.<sup><a href="#fn23" class="footnoteRef" id="fnref23">23</a></sup><sup><a href="#fn24" class="footnoteRef" id="fnref24">24</a></sup> [onebitgen]</p>
<blockquote>
<p>Let <span class="math">\(f : \{0,1\}^* \rightarrow \{0,1\}^*\)</span> be a one-way function length preserving permutation with a hard core predicate <span class="math">\(B : \{0,1\}^*
    \rightarrow \{0,1\}\)</span> then,</p>
<p><span class="math">\[\begin{aligned}
      &amp;G : \{0,1\}^k \rightarrow \{0,1\}^{k+1} \\
      &amp;G(x) = (f(x), B(x))
    \end{aligned}\]</span></p>
<p>is a pseudo-random generator.</p>
</blockquote>
<p>If <span class="math">\(x\)</span> is a random string, and therefore drawn from a uniform distribution over <span class="math">\(\{0,1\}^k\)</span>, then <span class="math">\(f(x)\)</span> is also a random string. Therefore, if there is some test, <span class="math">\(T\)</span>, which can distinguish <span class="math">\(G(x)\)</span> from a random string of length <span class="math">\(k+1\)</span> it must be distinguishing the last bit, <span class="math">\(B(x)\)</span>. Since, it can distinguish <span class="math">\(B(x)\)</span> from a random bit then one must be able to guess it significantly better than half the time. However, this contradicts <span class="math">\(B(x)\)</span> being a hard-core predicate of <span class="math">\(f(x)\)</span>. Therefore, <span class="math">\(f\)</span> is either not a one-way function or <span class="math">\(G(x)\)</span> is a pseudo-random generator.</p>
<p>While, theorem [onebitgen] certainly constructs a pseudo-random number generator it is hardly a useful one. Recall, the issue with perfect secrecy was the key size. If one constructed a stream cipher from using theorem [onebitgen] one would only save 1 bit of key size over a one time pad. Luckily, the following extension also holds:</p>
<p>An <span class="math">\(l(k)\)</span> Pseudo-Random Generator<sup><a href="#fn25" class="footnoteRef" id="fnref25">25</a></sup> [gen]</p>
<blockquote>
<p>Let <span class="math">\(f : \{0,1\}^* \rightarrow \{0,1\}^*\)</span> be a one-way function length preserving permutation with a hard core predicate <span class="math">\(B : \{0,1\}^*
    \rightarrow \{0,1\}\)</span>. If <span class="math">\(l(\cdot)\)</span> is a positive polynomial then,</p>
<p><span class="math">\[\begin{aligned}
      &amp;G : \{0,1\}^k \rightarrow \{0,1\}^{l(k)} \\
      &amp;G(x) = (B(x), B(f(x)), B(f^2(x)), ..., B(f^{l(k)-1}(x)))
    \end{aligned}\]</span></p>
<p>is a pseudo-random generator.</p>
</blockquote>
<p>With the construction in theorem [gen] one can now generate a strong pseudo-random sequence. If <span class="math">\(f\)</span> is a strong one way function with a hard-core then no polynomial adversary can discern between the output of the generator above and a truly random string.</p>
<p>A Symmetric Key Stream Cipher<sup><a href="#fn26" class="footnoteRef" id="fnref26">26</a></sup></p>
<blockquote>
<dl>
<dt>Setup</dt>
<dd><p>Alice chooses a short random key <span class="math">\(x \in_{R} \{0,1\}^k\)</span></p>
</dd>
<dt>Key Distribution</dt>
<dd><p>Alice secretly shares <span class="math">\(x\)</span> with Bob.</p>
</dd>
<dt>Encryption</dt>
<dd><p>Alice encrypts an <span class="math">\(m\)</span>-bit message, <span class="math">\(M\)</span>, by generating a pseudo-random string:</p>
<p><span class="math">\[\begin{aligned}
                          G(x) = (B(f(x)), B(f^2(x)), ..., B(f^m(x)))
                        \end{aligned}\]</span></p>
<p>and forming the cryptogram <span class="math">\(C = G(x) \otimes M\)</span></p>
</dd>
<dt>Decryption</dt>
<dd><p>Bob creates the same string <span class="math">\(G(x)\)</span> an recovers the message via <span class="math">\(M = G(x) \otimes C\)</span>.</p>
</dd>
</dl>
</blockquote>
<p>The strength of the cipher relies on the strength of <span class="math">\(G(x)\)</span> and the strength of <span class="math">\(G(x)\)</span> relies on the underlying properties of the one way function, <span class="math">\(f\)</span>. The above stream cipher is clearly semantically secure since the ciphertexts are indistinguishable by Eve. If Eve could distinguish the ciphertexts than she could predict <span class="math">\(G(x)\)</span>. If Eve can predict <span class="math">\(G(x)\)</span> than <span class="math">\(f\)</span> must not be a one way function.</p>
<p>While the above stream cipher is semantically secure, it is not necessarily the construction one would use in practice. Often, one would instead want to use a block cipher. Luckily, one can also construct block based ciphers from pseudo-random generators. For these an many other complications I refer you to Oded Goldreich&#8217;s 2004 book.<span class="citation"></span></p>
<h2>Public Key Schemes</h2>
<p>I will not discuss the public key schemes in detail. The definitions for security setup in section [sec-def] are implicitly for symmetric key systems. While, the modifications are fairly trivial they should be given proper treatment. In addition the public key systems deserve a thorough explanation. I will settle for some brief remarks.</p>
<p>The RSA cryptographic system does not satisfy the property of polynomial indistinguishability. In particular, if Eve wants to tell whether <span class="math">\(C\)</span> corresponds to <span class="math">\(M_1\)</span> or to <span class="math">\(M_2\)</span> all she has to do is encrypt both messages can compare their ciphertexts. Eve and easily do this since the encryption algorithm in a public key system is public and therefore available to Eve.</p>
<p>The encryption algorithm being publicly available seems to be an insurmountable obstacle at first, but it turns out to be possible to overcome it. In the case of the RSA algorithm one needs to introduce randomness (and thus uncertainty) into the encryption process. One such suggestion <em>Randomized RSA</em> introduces random data into each encryption thus ensuring polynomial indistinguishability. However, Randomized RSA comes with a cost: one must believe a different strong assumption. One must assume RSA has a &#8220;large&#8221; hard-core of bits in the input. While, this may be a reasonable assumption it is a <em>different</em> assumption and not implied by the usual RSA assumption. For details I once again commend you to Goldreich&#8217;s 2004 book.<span class="citation"></span></p>
<h1>Concluding Remarks</h1>
<p>Basing cryptographic security on computation complexity is a sound practice. It yields systems with strong and extensible security guarantees. However, it also requires strong assumptions. In particular, we must believe in &#8220;one way functions.&#8221; While, there is good evidence they exist, and several candidate functions appear to work, we do not <em>know</em> they exist. But, until a better formalism comes along complexity theory is secure in its position as the basis of modern cryptography.</p>
<div class="footnotes">
<hr />
<ol>
<li id="fn1"><p>See section 4.6.1<a href="#fnref1">&#8617;</a></p></li>
<li id="fn2"><p>See pages 2,3<a href="#fnref2">&#8617;</a></p></li>
<li id="fn3"><p>See page 3<a href="#fnref3">&#8617;</a></p></li>
<li id="fn4"><p>ie. time proportional to the size of the input<a href="#fnref4">&#8617;</a></p></li>
<li id="fn5"><p>See <span class="citation"></span> page 41 at the bottom.<a href="#fnref5">&#8617;</a></p></li>
<li id="fn6"><p>That is <span class="math">\(\mathcal{M}\)</span> computes in the <span class="math">\(n\)</span>th bit of output in <span class="math">\(p(n)\)</span> time.<a href="#fnref6">&#8617;</a></p></li>
<li id="fn7"><p>See <span class="citation"></span> page 23.<a href="#fnref7">&#8617;</a></p></li>
<li id="fn8"><p>Since a PTM is a theoretical construction rather than a physical construction we can do away with the nasty realities of life and assume these random bits are actually random! A nice change of pace.<a href="#fnref8">&#8617;</a></p></li>
<li id="fn9"><p>See section 4.2<a href="#fnref9">&#8617;</a></p></li>
<li id="fn10"><p>Note, any constant greater than <span class="math">\(\frac{1}{2}\)</span> can be used here.<a href="#fnref10">&#8617;</a></p></li>
<li id="fn11"><p>Definition is a combination of Definition 1.3.4 from <span class="citation"></span> and the definition given in Section 4.5 of <span class="citation"></span>.<a href="#fnref11">&#8617;</a></p></li>
<li id="fn12"><p>From personal discussion with Prof. Harold Connamacher (harold.connamacher@cwru.edu)<a href="#fnref12">&#8617;</a></p></li>
<li id="fn13"><p>Definition due to <span class="citation"></span> see Def. 1.3.5<a href="#fnref13">&#8617;</a></p></li>
<li id="fn14"><p>Definition due to <span class="citation"></span> see Def. 2.2.1. Note, I simplified the definition slightly for clarity.<a href="#fnref14">&#8617;</a></p></li>
<li id="fn15"><p>Definition due to <span class="citation"></span> see Def. 2.2.2<a href="#fnref15">&#8617;</a></p></li>
<li id="fn16"><p>See Theorem 2.3.2 for an impractical but demonstrative conversion and Section 2.6 for an efficient conversion in the case of one-way permutations.<a href="#fnref16">&#8617;</a></p></li>
<li id="fn17"><p>Definition due to <span class="citation"></span> see Def. 2.5.1<a href="#fnref17">&#8617;</a></p></li>
<li id="fn18"><p>Theorem 10.8<a href="#fnref18">&#8617;</a></p></li>
<li id="fn19"><p>Section 2.5.2<a href="#fnref19">&#8617;</a></p></li>
<li id="fn20"><p>Definition due to <span class="citation"></span> see Def. 5.2.3, simplified.<a href="#fnref20">&#8617;</a></p></li>
<li id="fn21"><p>Definition due to <span class="citation"></span> see Def. 5.2.1, simplified.<a href="#fnref21">&#8617;</a></p></li>
<li id="fn22"><p>Theorem (and proof) due to <span class="citation"></span> Theorem 5.2.5.<a href="#fnref22">&#8617;</a></p></li>
<li id="fn23"><p>Theorem and proof due to <span class="citation"></span> see theorem 10.9. My proof is a summary of Talbot and Welsh&#8217;s main argument<a href="#fnref23">&#8617;</a></p></li>
<li id="fn24"><p>A one way permutation is simply a one way function which is a bijection from the domain to the range. The existence of one way functions implies the existence of one way permutations.<a href="#fnref24">&#8617;</a></p></li>
<li id="fn25"><p>Theorem due to <span class="citation"></span> see Theorem 10.10<a href="#fnref25">&#8617;</a></p></li>
<li id="fn26"><p>Definition due to <span class="citation"></span> see page 216.<a href="#fnref26">&#8617;</a></p></li>
</ol>
</div>

