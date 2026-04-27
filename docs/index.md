---
title: Home
---

<section class="hero">
  <div>
    <div class="eyebrow">Frequency-domain ringdown toolkit</div>
    <h1><span class="gradient-text">GreyRing</span></h1>
    <p>
      Python tools for black-hole ringdown analyses based on greybody factors:
      from SXS validation to controlled injection-recovery tests and public gravitational-wave data.
    </p>
    <div class="actions">
      <a class="button" href="{{ '/installation/' | relative_url }}">Get started</a>
      <a class="button secondary" href="{{ '/sxs_fit/' | relative_url }}">See examples</a>
    </div>
  </div>

  <aside class="hero-card">
  <div class="hero-logo-panel">
    <img class="hero-logo" src="{{ '/assets/logo.svg' | relative_url }}" alt="GreyRing logo">
  </div>

  <div class="metric-grid">
    <div class="metric"><strong>SXS</strong><span>NR waveform fits</span></div>
    <div class="metric"><strong>Bilby</strong><span>Inference runs</span></div>
    <div class="metric"><strong>GF</strong><span>Greybody tables</span></div>
    <div class="metric"><strong>GW</strong><span>Real data workflows</span></div>
  </div>
  </aside>
</section>

<section class="section">
  <h2>What GreyRing does</h2>
  <p class="section-lead">
    GreyRing models the frequency-domain black-hole ringdown using greybody factors, with explicit examples for validation, injection studies, and event-level analyses.
  </p>

  <div class="card-grid">
    <a class="card" href="{{ '/sxs_fit/' | relative_url }}">
      <span class="tag">Validation</span>
      <h3>SXS fit</h3>
      <p>Fit numerical-relativity waveforms.</p>
    </a>
    <a class="card" href="{{ '/injection_recovery/' | relative_url }}">
      <span class="tag">Pipeline test</span>
      <h3>Injection-recovery</h3>
      <p>Inject a GreyRing signal and recover the remnant parameters with Bilby.</p>
    </a>
    <a class="card" href="{{ '/real_data/' | relative_url }}">
      <span class="tag">Data analysis</span>
      <h3>Real data</h3>
      <p>Run an event-level workflow with public strain data.</p>
    </a>
  </div>
</section>

<section class="section">
  <h2>Quick start</h2>
  <div class="callout">
    <pre><code class="language-bash">git clone https://github.com/romeofelicerosato-prog/GreyRing
cd GreyRing
pip install -e .
python -c "import greyring as gr; print(gr)"</code></pre>
  </div>
</section>

<section class="section">
  <h2>Repository structure</h2>

  <pre><code class="language-text">GreyRing/
├── greyring/     # importable Python package
└── examples/     # SXS fits, Bilby injections, real-data runs</code></pre>
</section>

<section class="section">
  <h2>Documentation map</h2>
  <div class="card-grid">
    <a class="card" href="{{ '/installation/' | relative_url }}">
      <h3>Installation</h3>
    </a>
    <a class="card" href="{{ '/theory_files/' | relative_url }}">
      <h3>Theory files</h3>
    </a>
    <a class="card" href="{{ '/kerr_gf_mathematica/' | relative_url }}">
      <h3>Kerr GFs Computation</h3>
    </a>
  </div>
</section>

<section class="section">
  <h2>Citation</h2>
  <p class="section-lead">
    If you use GreyRing in scientific works, please cite the relevant GreyRing papers and the external software packages used in your analysis.
  </p>

  <div class="citation-grid">
    <article class="citation-card">
      <span class="tag">GreyRing amplitude model</span>
      <h3>Modeling the frequency-domain ringdown amplitude of comparable-mass mergers with greybody factors</h3>
      <p class="citation-authors">Romeo Felice Rosato, Sophia Yi, Emanuele Berti, and Paolo Pani</p>
      <p class="citation-meta"><em>Physical Review D</em> <strong>113</strong>, 064060 (2026)</p>
      <p class="citation-links">
        <a href="https://arxiv.org/abs/2512.15877">arXiv:2512.15877</a>
        <span>·</span>
        <a href="https://doi.org/10.1103/jqgb-mfg1">DOI</a>
      </p>

      <details class="bibtex-box">
        <summary>BibTeX</summary>
        <pre><code class="language-bibtex">@article{Rosato:2025ulx,
  author = {Rosato, Romeo Felice and Yi, Sophia and Berti, Emanuele and Pani, Paolo},
  title = {Modeling the frequency-domain ringdown amplitude of comparable-mass mergers with greybody factors},
  eprint = {2512.15877},
  archivePrefix = {arXiv},
  primaryClass = {gr-qc},
  doi = {10.1103/jqgb-mfg1},
  journal = {Phys. Rev. D},
  volume = {113},
  number = {6},
  pages = {064060},
  year = {2026}
}</code></pre>
      </details>
    </article>

    <article class="citation-card">
      <span class="tag">GreyRing tests of GR</span>
      <h3>Novel ringdown tests of general relativity with black hole greybody factors</h3>
      <p class="citation-authors">Romeo Felice Rosato, Francesco Crescimbeni, Sophia Yi, Emanuele Berti, and Paolo Pani</p>
      <p class="citation-meta">arXiv preprint (2026)</p>
      <p class="citation-links">
        <a href="https://arxiv.org/abs/2604.11895">arXiv:2604.11895</a>
      </p>

      <details class="bibtex-box">
        <summary>BibTeX</summary>
        <pre><code class="language-bibtex">@article{Rosato:2026apq,
  author = {Rosato, Romeo Felice and Crescimbeni, Francesco and Yi, Sophia and Berti, Emanuele and Pani, Paolo},
  title = {Novel ringdown tests of general relativity with black hole greybody factors},
  eprint = {2604.11895},
  archivePrefix = {arXiv},
  primaryClass = {gr-qc},
  month = {4},
  year = {2026}
}</code></pre>
      </details>
    </article>
  </div>
</section>