# `thesis`

### Style Choices

- all rules can be broken to avoid barbarism
- British English
- "modeled" not "modelled"
- paragraph titles are Title Case
- "first-principles methods"
- no naked references [123], prefer "reference [123]"
- "potential energy surface"
- "ab initio" and "et al" are not italic
- "timestep" not "time-step"
- "hyperparameter" not "hyper-parameter"
- "machine-learning potential"

### Notes on PDF/A

TU Berlin requires the submissions of PDF/A compliant documents for the final, accepted, version of the thesis. As this is rather tedious, some compromises have been made: The PDF generated from the LaTeX code in this repository will generate a PDF/A that is somewhat, but not fully, compliant with PDF/A-2b. It is, however, compliant enough to be straightforward to convert with an automated tool. I used the tool by [callas](https://www.callassoftware.com/en) supplied by TU Berlin. Adobe Acrobat can also do it. The end result is a document that is PDF/A-2b compliant. (We take PDF/A-2b because it supports transparency.)

Note that PDF/A is particularly picky about fonts. While the used fonts are largely unproblematic, or fixable automatically, the `mathbb` fonts supplied by `newpxmath` report inconsistent widths and therefore break the conversion. For the thesis I decided to just redefine the commands to upright bold symbols, as the whole and natural numbers and unit matrix only appear a few times. The other big change from regular LaTeX (maybe familiar for those that submit to arXiv) is that all fonts must be embedded in PDF plots. This can be done easily with ghostscript, a python script is included here.

For technical reasons, a slightly modified copy of [`tufte-latex`](https://ctan.org/pkg/tufte-latex?lang=en) is included here; I do not claim copyright.

### Versions

`versions/` contains particular editions of the thesis. `da-2.0-pdfa.pdf` is the officially accepted and deposited version. This repository always corresponds to the newest one, which is *not* officially accepted. Versions since `2.0`, however, only contain extremely minor changes. The `-pdfa` suffix indicates that the PDF has been processed with a conversion tool, and is therefore PDF/A-2b compliant.

- `v2.1`: Fixed page headers. Likely final version. :)
- `v2.0`: Accepted version.
- `v1.0`: Version handed in to committee.
