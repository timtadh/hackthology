Title: The Impact of Rare Failures on Statistical Fault Localization: the Case of the Defects4J Suite
Author: Yiğit Küçük, <a href="http://hackthology.com">Tim Henderson</a>, and <a href="http://engineering.case.edu/profiles/hap">Andy Podgurski</a>
Citation: Yiğit Küçük, <strong>Tim A. D. Henderson</strong>, and Andy Podgurski. <i>The Impact of Rare Failures on Statistical Fault Localization: the Case of the Defects4J Suite</i>. ICSME 2019.
CiteAuthor: Yiğit Küçük, <strong>Tim A. D. Henderson</strong>, and Andy Podgurski
Publication: ICSME 2019
Date: 2019-10-3
Category: Paper
MainPage: hide

Yiğit Küçük, **Tim A. D. Henderson**, and Andy Podgurski
*The Impact of Rare Failures on Statistical Fault Localization: the Case of the Defects4J Suite*.  [ICSME 2019](https://icsme2019.github.io/).
<br/>
[DOI](http://tba).
[PDF]({static}/pdfs/icsme-2019.pdf).
[WEB]({filename}/papers/2019-icsme.md).

#### Abstract

Statistical Fault Localization (SFL) uses coverage profiles (or "spectra")
collected from passing and failing tests, together with statistical metrics,
which are typically composed of simple estimators, to identify which elements of
a program are most likely to have caused observed failures. Previous SFL
research has not thoroughly examined how the effectiveness of SFL metrics is
related to the proportion of failures in test suites and related quantities. To
address this issue, we studied the Defects4J benchmark suite of programs and
test suites and found that if a test suite has very few failures, SFL performs
poorly. To better understand this phenomenon, we investigated the precision of
some statistical estimators of which SFL metrics are composed, as measured by
their coefficients of variation.  The precision of an embedded estimator, which
depends on the dataset, was found to correlate with the effectiveness of a
metric containing it: low precision is associated with poor effectiveness.
Boosting precision by adding test cases was found to improve overall SFL
effectiveness. We present our findings and discuss their implications for the
evaluation and use of SFL metrics.

([Read the rest of the paper as a pdf]({static}/pdfs/icsme-2019.pdf))
