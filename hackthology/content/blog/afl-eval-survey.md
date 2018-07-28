Title: How to Evaluate Statistical Fault Localization
Author: Tim Henderson
Date: 2018-07-27
Category: Blog


<h4>Cite as:</h4>
> **Tim A. D. Henderson**. *How To Evaluate Statistical Fault Localization*.
> Blog. 2018.  <https://hackthology.com/how-to-evaluate-statistical-fault-localization.html>
> <br/>
> [PDF]({filename}/pdfs/how-to-eval-fault-localization.pdf).
> [WEB]({filename}/blog/afl-eval-survey.md).

<h4>Note</h4>
> This is a conversion from a latex paper I wrote. If you want all formatting
> correct you should read the
> [pdf version]({filename}/pdfs/how-to-eval-fault-localization.pdf).

<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/latest.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
<h1 id="introduction">Introduction</h1>
<p>Automatic fault localization is a software engineering technique to assist a programmer during the debugging process by suggesting suspicious locations that may be related to the root cause of the bug. The big idea behind behind automatic fault localization (or just fault localization) is by pointing the programmer towards the right area of the program the programmer will find the cause of the bug more quickly.</p>
<p>One approach to fault localization is <em>Spectrum Based Fault Localization</em> which is also known as <em>Coverage Based Statistical Fault Localization</em> (CBSFL) <span class="citation">[<a href="#ref-Jones2002">1</a>]-[<a href="#ref-Sun2016">3</a>]</span>. This approach uses test coverage information to rank the statements from most "suspicious" to least suspicious. To perform CBSFL, test cases are run through an instrumented program. The instrumentation collects coverage profiles which report each statement<a href="#fn1" class="footnoteRef" id="fnref1"><sup>1</sup></a> executed during the test run. A <em>test oracle</em> is used to label each execution profile with whether or not the test passed or failed. Such oracles can be either automatic or manual (i.e. a human). The labeled execution profiles are referred to as the <em>coverage spectra</em>.</p>
<p>CBSFL techniques score each program element (location in the program) by its "statistical suspiciousness" such that the most suspicious element has the highest score. The scores are computed by <em>suspiciousness metrics</em> which attempt to quantify the relationship between the execution each program element and the occurrence of program failure.</p>
<p>There have been a great many statistical fault localization suspiciousness metrics proposed <span class="citation">[<a href="#ref-Lucia2014">2</a>]</span> since the idea was first proposed by Jones, Harrold and Stasko in 2002 <span class="citation">[<a href="#ref-Jones2002">1</a>]</span>. The majority of the metrics are computed from just a few values: the number of tests <span class="math inline">\(n\)</span>, the number of passing tests <span class="math inline">\(p\)</span>, the number failing tests <span class="math inline">\(f\)</span>, the number of test runs an element <span class="math inline">\(e\)</span> was executed in <span class="math inline">\(n_e\)</span>, the number of passing test runs an element was executed in <span class="math inline">\(p_e\)</span>, and the number of failing test runs an element was executed in <span class="math inline">\(f_e\)</span>. For instance, using these simple statistics one can estimate the conditional probability of program failure <span class="math inline">\(F\)</span> given that a particular element <span class="math inline">\(e\)</span> was executed: <span class="math display">\[\begin{aligned}
  
  {\textrm{Pr}\left[{F|e}\right]} &amp;= \frac{{\textrm{Pr}\left[{F \cap e}\right]}}{{\textrm{Pr}\left[{e}\right]}}
                        \approx \frac{\frac{f_{e}}{n}}{\frac{n_{e}}{n}}
                        = \frac{f_e}{n_e}\end{aligned}\]</span> While many of the studies in statistical fault localization use more complex formulas <span class="citation">[<a href="#ref-Lucia2014">2</a>], [<a href="#ref-Sun2016">3</a>]</span> (with various technical motivations) most of the metrics are measures statistical association as in the equation above.</p>
<p>The runtime information used to compute the above statistics is commonly referred to as the <em>coverage spectra</em> of the program. Coverage spectra is a matrix <span class="math inline">\({\bf C}\)</span> where <span class="math inline">\({\bf C}_{i,j} &gt; 0\)</span> indicates that the program element <span class="math inline">\(\mathcal{E}_i\)</span> was executed at least once during test <span class="math inline">\(\mathcal{T}_j\)</span>. Additionally, there is an additional "test status" vector <span class="math inline">\({\bf S}\)</span> where <span class="math inline">\({\bf S}_{j} = \text{"F&#39;&#39;}\)</span> if test <span class="math inline">\(\mathcal{T}_j\)</span> failed and <span class="math inline">\({\bf S}_{j} =
\text{"P&#39;&#39;}\)</span> if test <span class="math inline">\(j\)</span> passed.</p>
<p>To collect the coverage spectra the program is instrumented to collect a runtime profile of the executed elements. This instrumentation can be done (in principle) at any granularity including: expression, statement, basic block<a href="#fn2" class="footnoteRef" id="fnref2"><sup>2</sup></a>, function, class, file, or package. The statistical methods which make use of spectra are agnostic to their granularity. While the granularity does not effect the statistical computation it changes how the localization results are perceived by the programmer. In the past, programmers have indicated a desire for finer grained results: at statement, basic block, or function level <span class="citation">[<a href="#ref-Kochhar2016">5</a>]</span> over very coarse grained results at the class, file, or package level.</p>
<p>Some statistical fault localization techniques use additional information to either improve accuracy or provide more explainable results. For instance, work on <em>Causal Fault Localization</em> uses additional static and dynamic information to control for statistical confounding <span class="citation">[<a href="#ref-Baah2010">6</a>]</span>. In contrast <em>Suspicious Behavior Based Fault Localization</em> (SBBFL) uses runtime control flow information (the behavior) to identify groups of collaborating suspicious elements <span class="citation">[<a href="#ref-Henderson2018">7</a>]</span>. These techniques leverage data mining techniques <span class="citation">[<a href="#ref-Aggarwal2014">8</a>]</span> such as frequent <span class="citation">[<a href="#ref-Agrawal1993">9</a>]-[<a href="#ref-Aggarwal2014a">11</a>]</span> or significant pattern mining <span class="citation">[<a href="#ref-Henderson2018">7</a>], [<a href="#ref-Yan2008">12</a>]</span>. When significant patterns are mined metrics (such as statistical fault localization suspiciousness metrics) are used to identify the most significant patterns <span class="citation">[<a href="#ref-Henderson2018">7</a>], [<a href="#ref-Cheng2009a">13</a>]</span>.</p>
<p>Finally, a variety of non-statistical (or mixed methods) techniques for fault localization have been explored <span class="citation">[<a href="#ref-Abreu2006">14</a>]-[<a href="#ref-Wong2016">17</a>]</span>. These range from delta debugging <span class="citation">[<a href="#ref-Zeller1999">18</a>]</span> to nearest neighbor queries <span class="citation">[<a href="#ref-Renieres2003">19</a>]</span> to program slicing <span class="citation">[<a href="#ref-Tip1995">20</a>], [<a href="#ref-Mao2014">21</a>]</span> to information retrieval <span class="citation">[<a href="#ref-Marcus2004">22</a>]-[<a href="#ref-Le2015">24</a>]</span> to test case generation <span class="citation">[<a href="#ref-Artzi2010">25</a>]-[<a href="#ref-Perez2014">27</a>]</span>. Despite differences in the technical and theoretical approach of these alternate methods they also suggest locations (or groups of locations) for the programmer to consider when debugging.</p>
<h1 id="evaluation-methods">Evaluation Methods</h1>
<p>Some of the earliest papers in fault localization do not provide a quantitative method for evaluating performance (as is seen in later papers <span class="citation">[<a href="#ref-Pearson2017">28</a>]</span>). For instance, in the earliest CBSFL paper <span class="citation">[<a href="#ref-Jones2002">1</a>]</span> (by Jones <em>et al.</em>'s) the technique is evaluated using a qualitative visualization. At the time, this was entirely appropriate as Jones was proposing a technique for visualizing test coverage for assisting the debugging process. The test coverage visualization was driven by what is now called a statistical fault localization metric (Tarantula). The evaluation visualization aggregated the visualizations all of the programs included in the study.</p>
<p>While, the evaluation method used in the Jones paper effectively communicated the potential of CBSFL (and got many researchers excited about the idea) it was not good way to compare multiple fault localization techniques. In 2005 Jones and Harrold <span class="citation">[<a href="#ref-Jones2005">29</a>]</span> conducted a study which compared their Tarantula technique to 3 other techniques: Set Union and Intersection <span class="citation">[<a href="#ref-Agrawal1995">30</a>]</span>, Nearest Neighbor <span class="citation">[<a href="#ref-Renieres2003">19</a>]</span>, and Cause-Transitions <span class="citation">[<a href="#ref-Cleve2005">31</a>]</span>. These techniques all took unique approaches toward the fault localization problem and were originally evaluated in different ways. Jones and Harrold re-evaluated all 5 methods under a new common evaluation framework.</p>
<p>In the 2005 paper, Jones and Harrold evaluate the effectiveness of each technique by using the technique to rank the statements in the subject programs. Each technique ranked the statements from most likely to be the cause of the fault to least likely. For Tarantula, the statements are ranked using the Tarantula suspiciousness score:<a href="#fn3" class="footnoteRef" id="fnref3"><sup>3</sup></a></p>
<h4 id="definition.-tarantula-rank-score"><strong>Definition</strong>. Tarantula Rank Score <span class="citation">[<a href="#ref-Jones2005">29</a>]</span></h4>
<blockquote>
<p>Given a set of locations <span class="math inline">\(L\)</span> with their suspiciousness scores <span class="math inline">\(s(l)\)</span> for <span class="math inline">\(l
  \in L\)</span> the Rank Score for a location <span class="math inline">\(l \in L\)</span> is: <span class="math display">\[\begin{aligned}
    {{\left|{ \left\{ x ~:~ x \in L \wedge s(x) &gt; s(l) \right\} }\right|}} +
    {{\left|{ \left\{ x ~:~ x \in L \wedge s(x) = s(l) \right\} }\right|}}
  \end{aligned}\]</span></p>
</blockquote>
<p>For Set Union and Intersection, Nearest Neighbor and Cause-Transitions the statements are ranked using a System Dependence Graph (SDG) <span class="citation">[<a href="#ref-Horwitz1990">32</a>]</span> technique from Renieres and Reiss <span class="citation">[<a href="#ref-Renieres2003">19</a>]</span> who first suggested the ranking idea. The ranks are then used to calculate the Tarantula Rank Score.</p>
<p>In the Jones and Harrold evaluation the authors do not use the Tarantula Rank Score directly but instead use a version normalized by program size:</p>
<h4 id="definition.-tarantula-effectiveness-score-expense"><strong>Definition</strong>. Tarantula Effectiveness Score (Expense) <span class="citation">[<a href="#ref-Jones2005">29</a>]</span></h4>
<blockquote>
<p>The percentage of program elements that do not need to be examined to find the fault when the elements are arranged according to their rank. Formally: let <span class="math inline">\(n\)</span> be the total number of program elements, and let <span class="math inline">\(r(f)\)</span> be the Tarantula Rank Score of the faulty element <span class="math inline">\(f\)</span> then the score is: <span class="math display">\[\begin{aligned}
    \frac{n-r(f)}{n}
  \end{aligned}\]</span></p>
</blockquote>
<p>Using the normalized effectiveness score Jones and Harrold directly compare the fault localization effectiveness of each of the considered methods. They did this in two ways. First, they presented a table (Table 2) which bucketed all the buggy versions form all the programs by the percentage given by the Tarantula Effectiveness Score. Second, they presented a figure (Figure 2) which showed the data in Table 2 as a cumulative curve.</p>
<p>The basic evaluation method presented by Jones and Harrold has become the standard evaluation method. Faulty statements are scored, ranked, rank-scored, normalized, and then aggregated over all versions and programs to provide an overall representation of the fault localization method's performance (a few examples: <span class="citation">[<a href="#ref-Lucia2014">2</a>], [<a href="#ref-Sun2016">3</a>], [<a href="#ref-Steimann2013">33</a>]-[<a href="#ref-Zheng2018">36</a>]</span>). While the basic method has stayed fairly consistent, there has been some innovation in the scoring (both the Rank Score and the Effectiveness Scores).</p>
<p>For instance, Wong <em>et al.</em> <span class="citation">[<a href="#ref-Wong2008">34</a>]</span> introduced the most commonly used Effectiveness Score the <span class="math inline">\(\mathcal{EXAM}\)</span> score. This score is essentially the same as the Expense score except it gives the percentage of elements which need to be examined rather than those avoided.</p>
<h4 id="definition.-mathcalexam-score"><strong>Definition</strong>. <span class="math inline">\(\mathcal{EXAM}\)</span> Score <span class="citation">[<a href="#ref-Wong2008">34</a>]</span></h4>
<blockquote>
<p>The percentage of program elements that need to be examined to find the fault when the elements are arranged according to their rank. Formally: let <span class="math inline">\(n\)</span> be the total number of program elements, and let <span class="math inline">\(r(f)\)</span> be the Tarantula Rank Score of the faulty element <span class="math inline">\(f\)</span> then the score is: <span class="math display">\[\begin{aligned}
    \frac{r(f)}{n}
  \end{aligned}\]</span></p>
</blockquote>
<p>Ali <em>et al.</em> <span class="citation">[<a href="#ref-Ali2009">37</a>]</span> identified an important problem with the Jones and Harrold evaluation: some fault localization metrics and algorithms rank statements equally. This is captured in the second term in the definition for the Tarantula Rank Score. However, Ali points out that this introduces bias towards algorithms that always assign unique scores (that are close together) rather than those that would score the same group of statement equally. The fix is to instead compute the expected number of statements the programmer would examine if they chose the next equally scored element at random.</p>
<h4 id="definition.-rank-score"><strong>Definition</strong>. Rank Score</h4>
<blockquote>
<p>Gives the expected number of locations a programmer would inspect before finding the bug. Formally, given a set of locations <span class="math inline">\(L\)</span> with their suspiciousness scores <span class="math inline">\(s(l)\)</span> for <span class="math inline">\(l \in L\)</span> the Rank Score for a location <span class="math inline">\(l
  \in L\)</span> is <span class="citation">[<a href="#ref-Ali2009">37</a>]</span>: <span class="math display">\[\begin{aligned}
    {{\left|{ \left\{ x ~:~ x \in L \wedge s(x) &gt; s(l) \right\} }\right|}} +
    \frac{
      {{\left|{ \left\{ x ~:~ x \in L \wedge s(x) = s(l) \right\} }\right|}}
    }{
      2
    }
  \end{aligned}\]</span></p>
</blockquote>
<p>Following Ali, we recommend utilizing the above definition for Rank Score over the Tarantula definition.</p>
<p>Parin and Orso <span class="citation">[<a href="#ref-Parnin2011">38</a>]</span> conducted a user study which looked at the programmer experience of using a statistical fault localization tool (Tarantula <span class="citation">[<a href="#ref-Jones2002">1</a>]</span>). Among their findings they found that programmers would not look deeply through the list of locations and would instead only consider the first few items. As a result they encouraged studies to no longer report scores as percentages. While some studies still report the percentages most studies are now reporting the absolute (non-percentage) rank scores. Reporting as absolute scores is important for another reason, if percentage ranks are reported larger programs can have much larger absolute ranks for the same percentage rank. This biases the evaluation toward large programs even when the actual localization result is poor.</p>
<p>Steimann <em>et al.</em> <span class="citation">[<a href="#ref-Steimann2013">33</a>]</span> identified a number of threats to validity in CBSFL studies including: heterogeneous subject programs, poor test suites, small sample sizes, unclear sample spaces, flaky tests, total number of faults, and masked faults. For evaluation they used the Rank Score modified to deal with <span class="math inline">\(k\)</span> faults tied at the same rank.</p>
<h4 id="definition.-steimann-rank-score"><strong>Definition</strong>. Steimann Rank Score</h4>
<blockquote>
<p>Gives the expected number of locations a programmer would inspect before finding the bug when multiple faulty statements have the same rank. Formally, given a set of locations <span class="math inline">\(L\)</span> with their suspiciousness scores <span class="math inline">\(s(l)\)</span> for <span class="math inline">\(l
  \in L\)</span> the Rank Score for a location <span class="math inline">\(l \in L\)</span> is <span class="citation">[<a href="#ref-Steimann2013">33</a>]</span>: <span class="math display">\[\begin{aligned}
    &amp; {{\left|{ \left\{ x ~:~ x \in L \wedge s(x) &gt; s(l) \right\} }\right|}}\\
    &amp; + \frac{
          {{\left|{ \left\{ x ~:~ x \in L \wedge s(x) = s(l) \right\} }\right|}} + 1
        }{
          {{\left|{ \left\{ x ~:~ x \in L \wedge s(x) = s(l) \wedge x \text{ is a
          faulty location} \right\}}\right|}} + 1
        }
  \end{aligned}\]</span></p>
</blockquote>
<p>Moon <em>et al.</em> <span class="citation">[<a href="#ref-Moon2014">39</a>]</span> proposed Locality Information Loss (LIL) as an alternative evaluation framework. LIL models the localization result as a probability distribution constructed from the suspiciousness scores:</p>
<h4 id="definition.-lil-probability-distribution"><strong>Definition</strong>. LIL Probability Distribution</h4>
<blockquote>
<p>Let <span class="math inline">\(\tau\)</span> be a suspicious metric normalized to the <span class="math inline">\([0,1]\)</span> range of reals. Let <span class="math inline">\(n\)</span> be the number statements in the program. Let <span class="math inline">\(S\)</span> be the set of statements. For all <span class="math inline">\(1 \le i \le n\)</span> let <span class="math inline">\(s_i \in S\)</span>. The constructed probability distribution is: <span class="math display">\[\begin{aligned}
    P_{\tau}(s_i) = \frac{\tau(s_i)}{\sum^{n}_{j=1} \tau(s_j)}
  \end{aligned}\]</span></p>
</blockquote>
<p>LIL uses a measure of distribution divergence (Kullback-Leibler) to compute a score of how different the constructed distribution is from the "perfect" expected distribution. The advantage of the LIL framework is it does not depend on a list of ranked statements and can be applied to non-statistical methods (using a synthetic <span class="math inline">\(\tau\)</span>). The disadvantage of LIL is it does not indicate programmer effort (as indicated by the Rank Score). However, it may be a better metric to use when evaluating fault localization systems as a component for automated bug repair systems.</p>
<p>Pearson <em>et al.</em> <span class="citation">[<a href="#ref-Pearson2017">28</a>]</span> re-evaluated a number of previous results using new real world subject programs with real defects and test suites. In contrast to previous work they made use of statistical hypothesis testing and confidence intervals to test the significance of the results. To evaluate the performance of each technique under study they used the <span class="math inline">\(\mathcal{EXAM}\)</span> score reporting best, average, and worst case results for multi-statement faults.</p>
<p><em>T-Score</em> <span class="citation">[<a href="#ref-Liu2006">40</a>]</span> is designed for non-statistical fault localization methods which produce a small set of suspicious statements in the program. To evaluate how helpful these reports are <em>T-Score</em> uses the Program Dependence Graph (PDG) <span class="citation">[<a href="#ref-Horwitz1990">32</a>], [<a href="#ref-Ferrante1987">41</a>]</span> to compute a set of vertices in the graph that must be examined in order to reach any faulty vertex. This set is computed via a breadth first search from the set of vertices in the report. Finally, the score is computed as the percentage of examined vertices out of the total number of vertices in the graph.</p>
<h1 id="multiple-fault-evaluations">Multiple Fault Evaluations</h1>
<p>With the exception of LIL, the evaluation methods discussed so far are generally defined to operate with a single faulty location. However, there may be multiple faults or multiple locations associated with a single fault or both. Multiple faults can interact <span class="citation">[<a href="#ref-DiGiuseppe2011">42</a>]</span> and interfere with the performance of the fault localizer. For evaluation purposes one of the most popular methods is to take either best result <span class="citation">[<a href="#ref-Wong2007">43</a>]</span>, the average result <span class="citation">[<a href="#ref-Abreu2006">14</a>], [<a href="#ref-Naish2011">44</a>]</span>, or the worst result <span class="citation">[<a href="#ref-Wong2007">43</a>]</span>.</p>
<h1 id="evaluating-other-techniques">Evaluating Other Techniques</h1>
<p>One of the challenges with the methods presented so far is they may not work well for evaluating alternate fault localization methods. For instance, information retrieval based localization methods do not necessarily score and rank every program location. Instead they produce a report of associated regions. Jones and Harrold <span class="citation">[<a href="#ref-Jones2005">29</a>]</span> used a synthetic ranking system <span class="citation">[<a href="#ref-Renieres2003">19</a>]</span> based on the SDG <span class="citation">[<a href="#ref-Horwitz1990">32</a>]</span> which in principle could be used in such situation. However, like the <em>T-Score</em> it uses an arbitrary method (minimal dependence spheres) to compute the number of SDG nodes which must be examined.</p>
<p>The LIL method could also potentially be used to evaluate alternative methods. It does not rely on ranking but instead on the suspiciousness scores which it converts into a probability distribution. To support evaluating report based localization the reports are converted to a probability distribution with all locations in the report set to a equal high probability and all locations not in the report set to a tiny probability.</p>
<p><em>Suspicious Behavior Based Fault Localization</em> <span class="citation">[<a href="#ref-Henderson2018">7</a>]</span> requires particular care. These methods are produce a ranked set of "behaviors" which are structured groups of interacting program locations. The structure could be a call invocation structure <span class="citation">[<a href="#ref-Liu2005">45</a>]-[<a href="#ref-Diamantopoulos2014">49</a>]</span>, a general control flow structure <span class="citation">[<a href="#ref-Henderson2018">7</a>], [<a href="#ref-Cheng2009a">13</a>], [<a href="#ref-Mousavian2011">50</a>]</span>, or even an information flow structure <span class="citation">[<a href="#ref-Eichinger2010">51</a>]</span>. The structures are scored and ranked similar to CBSFL. However, unlike in CBSFL all program locations are not necessarily included. In the past, studies have used a variety of techniques to evaluated the effectiveness including precision and recall <span class="citation">[<a href="#ref-Cheng2009a">13</a>]</span> and scores based off of the <span class="math inline">\(\mathcal{EXAM}\)</span> score <span class="citation">[<a href="#ref-Henderson2018">7</a>]</span>.</p>
<p>Another subtle special case involves comparing statistical techniques which operate on different granularity levels. As mentioned previously, coverage can be collected at any granularity level: expression, statement, basic block, method or function, class, file, and even non-structural elements such as paths. Any of the CBSFL metrics can be used with any of these granularities. However, a single study using any of the previous evaluation methods must keep the granularity consistent. This makes it impossible to compare across granularity levels. This is makes it particularly difficult to accurately compare method level behavioral approaches <span class="citation">[<a href="#ref-Liu2005">45</a>]</span> to CBSFL.</p>
<h1 id="assumptions">Assumptions</h1>
<p>The biggest assumption that all evaluation models make is so-called <em>perfect bug understanding</em> which assumes programmers will recognize a bug as soon as they "examine" the faulty location. This assumption is obviously false <span class="citation">[<a href="#ref-Parnin2011">38</a>]</span>. However, it continues to be a useful simplifying assumption for evaluation purposes of the localization algorithms. From the standpoint of automated fault localization there are really two tasks: 1) finding the fault and 2) explaining the fault. Assuming perfect bug understanding is reasonable for evaluating a tools performance on task 1. However, their is the important caveat that programmers need more assistance at task 2. As a research community we do not currently have a standard method for evaluating our algorithmic performance on task 2.</p>
<p>The second assumption is that programmers will follow the rank list or suspiciousness scores when debugging a program using a fault localization tool. This assumption is obviously false as well <span class="citation">[<a href="#ref-Parnin2011">38</a>]</span>. A programmer may follow the list for the very first item and even the second but where they go from there is likely only partially influenced by the list. The bigger influence will be from the conclusions they are drawing from what they learn upon inspecting each location. Our new model does not require this assumption.</p>
<div id="refs" class="references">
<h1>References</h1>
<div id="ref-Jones2002">
<p>[1] J. Jones, M. Harrold, and J. Stasko, "Visualization of test information to assist fault localization," <em>Proceedings of the 24th International Conference on Software Engineering. ICSE 2002</em>, 2002, doi:<a href="https://doi.org/10.1145/581339.581397">10.1145/581339.581397</a>.</p>
</div>
<div id="ref-Lucia2014">
<p>[2] Lucia, D. Lo, L. Jiang, F. Thung, and A. Budi, "Extended comprehensive study of association measures for fault localization," <em>Journal of Software: Evolution and Process</em>, vol. 26, no. 2, pp. 172-219, Feb. 2014, doi:<a href="https://doi.org/10.1002/smr.1616">10.1002/smr.1616</a>.</p>
</div>
<div id="ref-Sun2016">
<p>[3] S.-F. Sun and A. Podgurski, "Properties of Effective Metrics for Coverage-Based Statistical Fault Localization," in <em>2016 ieee international conference on software testing, verification and validation (icst)</em>, 2016, pp. 124-134, doi:<a href="https://doi.org/10.1109/ICST.2016.31">10.1109/ICST.2016.31</a>.</p>
</div>
<div id="ref-Aho2007">
<p>[4] A. Aho, R. Sethi, M. S. Lam, and J. D. Ullman, <em>Compilers: principles, techniques, and tools</em>. 2007.</p>
</div>
<div id="ref-Kochhar2016">
<p>[5] P. S. Kochhar, X. Xia, D. Lo, and S. Li, "Practitioners' expectations on automated fault localization," in <em>Proceedings of the 25th international symposium on software testing and analysis - issta 2016</em>, 2016, pp. 165-176, doi:<a href="https://doi.org/10.1145/2931037.2931051">10.1145/2931037.2931051</a>.</p>
</div>
<div id="ref-Baah2010">
<p>[6] G. G. K. Baah, A. Podgurski, and M. J. M. Harrold, "Causal inference for statistical fault localization," in <em>Proceedings of the 19th international symposium on software testing and analysis</em>, 2010, pp. 73-84, doi:<a href="https://doi.org/10.1145/1831708.1831717">10.1145/1831708.1831717</a>.</p>
</div>
<div id="ref-Henderson2018">
<p>[7] T. A. D. Henderson and A. Podgurski, "Behavioral Fault Localization by Sampling Suspicious Dynamic Control Flow Subgraphs," in <em>IEEE conference on software testing, validation and verification</em>, 2018.</p>
</div>
<div id="ref-Aggarwal2014">
<p>[8] C. C. Aggarwal and J. Han, Eds., <em>Frequent Pattern Mining</em>. Cham: Springer International Publishing, 2014.</p>
</div>
<div id="ref-Agrawal1993">
<p>[9] R. Agrawal, T. Imieliński, and A. Swami, "Mining association rules between sets of items in large databases," <em>ACM SIGMOD Record</em>, vol. 22, no. 2, pp. 207-216, Jun. 1993, doi:<a href="https://doi.org/10.1145/170036.170072">10.1145/170036.170072</a>.</p>
</div>
<div id="ref-Yan2002">
<p>[10] X. Yan and J. Han, "gSpan: graph-based substructure pattern mining," in <em>2002 ieee international conference on data mining, 2002. proceedings.</em>, 2002, pp. 721-724, doi:<a href="https://doi.org/10.1109/ICDM.2002.1184038">10.1109/ICDM.2002.1184038</a>.</p>
</div>
<div id="ref-Aggarwal2014a">
<p>[11] C. C. Aggarwal, M. A. Bhuiyan, and M. A. Hasan, "Frequent Pattern Mining Algorithms: A Survey," in <em>Frequent pattern mining</em>, Cham: Springer International Publishing, 2014, pp. 19-64.</p>
</div>
<div id="ref-Yan2008">
<p>[12] X. Yan, H. Cheng, J. Han, and P. S. Yu, "Mining Significant Graph Patterns by Leap Search," in <em>Proceedings of the 2008 acm sigmod international conference on management of data</em>, 2008, pp. 433-444, doi:<a href="https://doi.org/10.1145/1376616.1376662">10.1145/1376616.1376662</a>.</p>
</div>
<div id="ref-Cheng2009a">
<p>[13] H. Cheng, D. Lo, Y. Zhou, X. Wang, and X. Yan, "Identifying Bug Signatures Using Discriminative Graph Mining," in <em>Proceedings of the eighteenth international symposium on software testing and analysis</em>, 2009, pp. 141-152, doi:<a href="https://doi.org/10.1145/1572272.1572290">10.1145/1572272.1572290</a>.</p>
</div>
<div id="ref-Abreu2006">
<p>[14] R. Abreu, P. Zoeteweij, and A. Van Gemund, "An Evaluation of Similarity Coefficients for Software Fault Localization," in <em>2006 12th pacific rim international symposium on dependable computing (prdc'06)</em>, 2006, pp. 39-46, doi:<a href="https://doi.org/10.1109/PRDC.2006.18">10.1109/PRDC.2006.18</a>.</p>
</div>
<div id="ref-Abreu2009">
<p>[15] R. Abreu, P. Zoeteweij, R. Golsteijn, and A. J. C. van Gemund, "A practical evaluation of spectrum-based fault localization," <em>Journal of Systems and Software</em>, vol. 82, no. 11, pp. 1780-1792, 2009, doi:<a href="https://doi.org/10.1016/j.jss.2009.06.035">10.1016/j.jss.2009.06.035</a>.</p>
</div>
<div id="ref-Agarwal2014">
<p>[16] P. Agarwal and A. P. Agrawal, "Fault-localization Techniques for Software Systems: A Literature Review," <em>SIGSOFT Softw. Eng. Notes</em>, vol. 39, no. 5, pp. 1-8, Sep. 2014, doi:<a href="https://doi.org/10.1145/2659118.2659125">10.1145/2659118.2659125</a>.</p>
</div>
<div id="ref-Wong2016">
<p>[17] W. E. Wong, R. Gao, Y. Li, R. Abreu, and F. Wotawa, "A Survey on Software Fault Localization," <em>IEEE Transactions on Software Engineering</em>, vol. 42, no. 8, pp. 707-740, Aug. 2016, doi:<a href="https://doi.org/10.1109/TSE.2016.2521368">10.1109/TSE.2016.2521368</a>.</p>
</div>
<div id="ref-Zeller1999">
<p>[18] A. Zeller, "Yesterday, My Program Worked. Today, It Does Not. Why?" <em>SIGSOFT Softw. Eng. Notes</em>, vol. 24, no. 6, pp. 253-267, Oct. 1999, doi:<a href="https://doi.org/10.1145/318774.318946">10.1145/318774.318946</a>.</p>
</div>
<div id="ref-Renieres2003">
<p>[19] M. Renieres and S. Reiss, "Fault localization with nearest neighbor queries," in <em>18th ieee international conference on automated software engineering, 2003. proceedings.</em>, 2003, pp. 30-39, doi:<a href="https://doi.org/10.1109/ASE.2003.1240292">10.1109/ASE.2003.1240292</a>.</p>
</div>
<div id="ref-Tip1995">
<p>[20] F. Tip, "A survey of program slicing techniques," <em>Journal of programming languages</em>, vol. 3, no. 3, pp. 121-189, 1995.</p>
</div>
<div id="ref-Mao2014">
<p>[21] X. Mao, Y. Lei, Z. Dai, Y. Qi, and C. Wang, "Slice-based statistical fault localization," <em>Journal of Systems and Software</em>, vol. 89, no. 1, pp. 51-62, 2014, doi:<a href="https://doi.org/10.1016/j.jss.2013.08.031">10.1016/j.jss.2013.08.031</a>.</p>
</div>
<div id="ref-Marcus2004">
<p>[22] A. Marcus, A. Sergeyev, V. Rajlieh, and J. I. Maletic, "An information retrieval approach to concept location in source code," <em>Proceedings - Working Conference on Reverse Engineering, WCRE</em>, pp. 214-223, 2004, doi:<a href="https://doi.org/10.1109/WCRE.2004.10">10.1109/WCRE.2004.10</a>.</p>
</div>
<div id="ref-Zhou2012">
<p>[23] J. Zhou, H. Zhang, and D. Lo, "Where should the bugs be fixed? More accurate information retrieval-based bug localization based on bug reports," <em>Proceedings - International Conference on Software Engineering</em>, pp. 14-24, 2012, doi:<a href="https://doi.org/10.1109/ICSE.2012.6227210">10.1109/ICSE.2012.6227210</a>.</p>
</div>
<div id="ref-Le2015">
<p>[24] T.-D. B. Le, R. J. Oentaryo, and D. Lo, "Information retrieval and spectrum based bug localization: better together," in <em>Proceedings of the 2015 10th joint meeting on foundations of software engineering - esec/fse 2015</em>, 2015, pp. 579-590, doi:<a href="https://doi.org/10.1145/2786805.2786880">10.1145/2786805.2786880</a>.</p>
</div>
<div id="ref-Artzi2010">
<p>[25] S. Artzi, J. Dolby, F. Tip, and M. Pistoia, "Directed Test Generation for Effective Fault Localization," in <em>Proceedings of the 19th international symposium on software testing and analysis</em>, 2010, pp. 49-60, doi:<a href="https://doi.org/10.1145/1831708.1831715">10.1145/1831708.1831715</a>.</p>
</div>
<div id="ref-Sahoo2013">
<p>[26] S. K. Sahoo, J. Criswell, C. Geigle, and V. Adve, "Using likely invariants for automated software fault localization," in <em>Proceedings of the eighteenth international conference on architectural support for programming languages and operating systems</em>, 2013, vol. 41, p. 139, doi:<a href="https://doi.org/10.1145/2451116.2451131">10.1145/2451116.2451131</a>.</p>
</div>
<div id="ref-Perez2014">
<p>[27] A. Perez, R. Abreu, and A. Riboira, "A Dynamic Code Coverage Approach to Maximize Fault Localization Efficiency," <em>J. Syst. Softw.</em>, vol. 90, pp. 18-28, Apr. 2014, doi:<a href="https://doi.org/10.1016/j.jss.2013.12.036">10.1016/j.jss.2013.12.036</a>.</p>
</div>
<div id="ref-Pearson2017">
<p>[28] S. Pearson, J. Campos, R. Just, G. Fraser, R. Abreu, M. D. Ernst, D. Pang, and B. Keller, "Evaluating and Improving Fault Localization," in <em>Proceedings of the 39th international conference on software engineering</em>, 2017, pp. 609-620, doi:<a href="https://doi.org/10.1109/ICSE.2017.62">10.1109/ICSE.2017.62</a>.</p>
</div>
<div id="ref-Jones2005">
<p>[29] J. A. Jones and M. J. Harrold, "Empirical Evaluation of the Tarantula Automatic Fault-localization Technique," in <em>Proceedings of the 20th ieee/acm international conference on automated software engineering</em>, 2005, pp. 273-282, doi:<a href="https://doi.org/10.1145/1101908.1101949">10.1145/1101908.1101949</a>.</p>
</div>
<div id="ref-Agrawal1995">
<p>[30] H. Agrawal, J. Horgan, S. London, and W. Wong, "Fault localization using execution slices and dataflow tests," in <em>Proceedings of sixth international symposium on software reliability engineering. issre'95</em>, 1995, pp. 143-151, doi:<a href="https://doi.org/10.1109/ISSRE.1995.497652">10.1109/ISSRE.1995.497652</a>.</p>
</div>
<div id="ref-Cleve2005">
<p>[31] H. Cleve and A. Zeller, "Locating causes of program failures," <em>Proceedings of the 27th international conference on Software engineering - ICSE '05</em>, p. 342, 2005, doi:<a href="https://doi.org/10.1145/1062455.1062522">10.1145/1062455.1062522</a>.</p>
</div>
<div id="ref-Horwitz1990">
<p>[32] S. Horwitz, "Identifying the Semantic and Textual Differences Between Two Versions of a Program," <em>SIGPLAN Not.</em>, vol. 25, no. 6, pp. 234-245, Jun. 1990, doi:<a href="https://doi.org/10.1145/93548.93574">10.1145/93548.93574</a>.</p>
</div>
<div id="ref-Steimann2013">
<p>[33] F. Steimann, M. Frenkel, and R. Abreu, "Threats to the validity and value of empirical assessments of the accuracy of coverage-based fault locators," <em>Proceedings of the 2013 International Symposium on Software Testing and Analysis - ISSTA 2013</em>, p. 314, 2013, doi:<a href="https://doi.org/10.1145/2483760.2483767">10.1145/2483760.2483767</a>.</p>
</div>
<div id="ref-Wong2008">
<p>[34] E. Wong, T. Wei, Y. Qi, and L. Zhao, "A Crosstab-based Statistical Method for Effective Fault Localization," in <em>2008 international conference on software testing, verification, and validation</em>, 2008, pp. 42-51, doi:<a href="https://doi.org/10.1109/ICST.2008.65">10.1109/ICST.2008.65</a>.</p>
</div>
<div id="ref-Landsberg2015">
<p>[35] D. Landsberg, H. Chockler, D. Kroening, and M. Lewis, "Evaluation of Measures for Statistical Fault Localisation and an Optimising Scheme," in <em>International conference on fundamental approaches to software engineering</em>, 2015, vol. 9033, pp. 115-129, doi:<a href="https://doi.org/10.1007/978-3-662-46675-9">10.1007/978-3-662-46675-9</a>.</p>
</div>
<div id="ref-Zheng2018">
<p>[36] Y. Zheng, Z. Wang, X. Fan, X. Chen, and Z. Yang, "Localizing multiple software faults based on evolution algorithm," <em>Journal of Systems and Software</em>, vol. 139, pp. 107-123, 2018, doi:<a href="https://doi.org/10.1016/j.jss.2018.02.001">10.1016/j.jss.2018.02.001</a>.</p>
</div>
<div id="ref-Ali2009">
<p>[37] S. Ali, J. H. Andrews, T. Dhandapani, and W. Wang, "Evaluating the Accuracy of Fault Localization Techniques," <em>2009 IEEE/ACM International Conference on Automated Software Engineering</em>, pp. 76-87, 2009, doi:<a href="https://doi.org/10.1109/ASE.2009.89">10.1109/ASE.2009.89</a>.</p>
</div>
<div id="ref-Parnin2011">
<p>[38] C. Parnin and A. Orso, "Are Automated Debugging Techniques Actually Helping Programmers?" in <em>ISSTA</em>, 2011, pp. 199-209.</p>
</div>
<div id="ref-Moon2014">
<p>[39] S. Moon, Y. Kim, M. Kim, and S. Yoo, "Ask the Mutants: Mutating faulty programs for fault localization," <em>Proceedings - IEEE 7th International Conference on Software Testing, Verification and Validation, ICST 2014</em>, pp. 153-162, 2014, doi:<a href="https://doi.org/10.1109/ICST.2014.28">10.1109/ICST.2014.28</a>.</p>
</div>
<div id="ref-Liu2006">
<p>[40] C. Liu, C. Chen, J. Han, and P. S. Yu, "GPLAG: Detection of Software Plagiarism by Program Dependence Graph Analysis," in <em>Proceedings of the 12th acm sigkdd international conference on knowledge discovery and data mining</em>, 2006, pp. 872-881, doi:<a href="https://doi.org/10.1145/1150402.1150522">10.1145/1150402.1150522</a>.</p>
</div>
<div id="ref-Ferrante1987">
<p>[41] J. Ferrante, K. J. Ottenstein, and J. D. Warren, "The program dependence graph and its use in optimization," vol. 9. pp. 319-349, Jul-1987.</p>
</div>
<div id="ref-DiGiuseppe2011">
<p>[42] N. DiGiuseppe and J. A. Jones, "On the influence of multiple faults on coverage-based fault localization," in <em>Proceedings of the 2011 international symposium on software testing and analysis - issta '11</em>, 2011, p. 210, doi:<a href="https://doi.org/10.1145/2001420.2001446">10.1145/2001420.2001446</a>.</p>
</div>
<div id="ref-Wong2007">
<p>[43] W. E. Wong, Y. Qi, L. Zhao, and K. Y. Cai, "Effective fault localization using code coverage," <em>Proceedings - International Computer Software and Applications Conference</em>, vol. 1, no. Compsac, pp. 449-456, 2007, doi:<a href="https://doi.org/10.1109/COMPSAC.2007.109">10.1109/COMPSAC.2007.109</a>.</p>
</div>
<div id="ref-Naish2011">
<p>[44] L. Naish, H. J. Lee, and K. Ramamohanarao, "A model for spectra-based software diagnosis," <em>ACM Transactions on Software Engineering and Methodology</em>, vol. 20, no. 3, pp. 1-32, 2011, doi:<a href="https://doi.org/10.1145/2000791.2000795">10.1145/2000791.2000795</a>.</p>
</div>
<div id="ref-Liu2005">
<p>[45] C. Liu, H. Yu, P. S. Yu, X. Yan, H. Yu, J. Han, and P. S. Yu, "Mining Behavior Graphs for ‘Backtrace' of Noncrashing Bugs," in <em>Proceedings of the 2005 siam international conference on data mining</em>, 2005, pp. 286-297, doi:<a href="https://doi.org/10.1137/1.9781611972757.26">10.1137/1.9781611972757.26</a>.</p>
</div>
<div id="ref-Eichinger2008">
<p>[46] F. Eichinger, K. Böhm, and M. Huber, "Mining Edge-Weighted Call Graphs to Localise Software Bugs," in <em>European conference machine learning and knowledge discovery in databases</em>, 2008, pp. 333-348, doi:<a href="https://doi.org/10.1007/978-3-540-87479-9_40">10.1007/978-3-540-87479-9_40</a>.</p>
</div>
<div id="ref-Chilimbi2009">
<p>[47] T. M. Chilimbi, B. Liblit, K. Mehra, A. V. Nori, and K. Vaswani, "HOLMES: Effective Statistical Debugging via Efficient Path Profiling," in <em>Proceedings of the 31st international conference on software engineering</em>, 2009, pp. 34-44, doi:<a href="https://doi.org/10.1109/ICSE.2009.5070506">10.1109/ICSE.2009.5070506</a>.</p>
</div>
<div id="ref-Yousefi2013">
<p>[48] A. Yousefi and A. Wassyng, "A Call Graph Mining and Matching Based Defect Localization Technique," in <em>2013 ieee sixth international conference on software testing, verification and validation workshops</em>, 2013, pp. 86-95, doi:<a href="https://doi.org/10.1109/ICSTW.2013.17">10.1109/ICSTW.2013.17</a>.</p>
</div>
<div id="ref-Diamantopoulos2014">
<p>[49] T. Diamantopoulos and A. Symeonidis, "Localizing Software Bugs using the Edit Distance of Call Traces," <em>International Journal on Advances in Software</em>, vol. 7, no. 1 &amp; 2, pp. 277-288, 2014.</p>
</div>
<div id="ref-Mousavian2011">
<p>[50] Z. Mousavian, M. Vahidi-Asl, and S. Parsa, "Scalable Graph Analyzing Approach for Software Fault-localization," in <em>Proceedings of the 6th international workshop on automation of software test</em>, 2011, pp. 15-21, doi:<a href="https://doi.org/10.1145/1982595.1982599">10.1145/1982595.1982599</a>.</p>
</div>
<div id="ref-Eichinger2010">
<p>[51] F. Eichinger, K. Krogmann, R. Klug, and K. Böhm, "Software-defect Localisation by Mining Dataflow-enabled Call Graphs," in <em>Proceedings of the 2010 european conference on machine learning and knowledge discovery in databases: Part i</em>, 2010, pp. 425-441.</p>
</div>
</div>
<div class="footnotes">
<hr />
<ol>
<li id="fn1"><p>The coverage can be collected at other levels as well. For instance there has been work which collects it at the class, method, and basic block levels.<a href="#fnref1">↩</a></p></li>
<li id="fn2"><p>A basic block is a sequence of sequential instructions, always entered from the first instruction and exited from the last <span class="citation">[<a href="#ref-Aho2007">4</a>]</span>.<a href="#fnref2">↩</a></p></li>
<li id="fn3"><p>It is ahistorical to call Tarantula metric a suspiciousness score when referring to the 2002 paper <span class="citation">[<a href="#ref-Jones2002">1</a>]</span>. Jones introduced the term suspiciousness score in the 2005 paper <span class="citation">[<a href="#ref-Jones2005">29</a>]</span> for the purpose of ranking the statements. However, the term is now in common use and it was explained above.<a href="#fnref3">↩</a></p></li>
</ol>
</div>
