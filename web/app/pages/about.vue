<template>
  <div class="py-16 md:py-24 px-6">
    <div class="max-w-3xl mx-auto">
      <p
        class="text-xs font-semibold text-cadet-500 uppercase tracking-[0.15em] mb-4"
      >
        About
      </p>
      <h1
        class="text-3xl font-serif font-semibold text-stone-900 tracking-tight"
      >
        Methodology
      </h1>

      <article class="mt-12 prose prose-stone prose-sm max-w-none">
        <p>
          Structured dataset of
          <a
            href="https://www.nice.org.uk/guidance/published?ngt=Technology+appraisal+guidance"
            >NICE Technology Appraisals</a
          >
          &mdash; the UK's health technology assessments that determine NHS drug
          funding. 826 appraisals indexed with 3,307 source documents. 555 have
          structured entity extraction from Final Appraisal Documents.
        </p>

        <h2>What's in the graph</h2>
        <ul>
          <li>
            <strong>Interventions</strong> (572 drugs) &mdash; generic name,
            drug class, mechanism, route, duration type
          </li>
          <li>
            <strong>Conditions</strong> (1,298) &mdash; name, therapeutic area,
            disease setting, biomarker
          </li>
          <li>
            <strong>Methodological decisions</strong> (9,509 across 23
            categories) &mdash; company position, ERG position, committee
            preference, ICER impact. Categories include survival extrapolation,
            utility source, comparator selection, crossover adjustment, model
            structure, and 18 others.
          </li>
          <li>
            <strong>ICER bands</strong> (926) &mdash; below &pound;20k,
            &pound;20&ndash;30k, &pound;30&ndash;50k, &pound;50&ndash;100k,
            above &pound;100k, dominant, confidential
          </li>
          <li>
            <strong>Clinical trials</strong> (2,206) &mdash; design, phase,
            blinding, crossover, generalisability
          </li>
          <li>
            <strong>Comparators</strong> (2,769) &mdash; type, established
            practice, committee preferred
          </li>
          <li>
            <strong>Economic models</strong> (675) &mdash; type, time horizon,
            health states
          </li>
          <li>
            <strong>Commercial arrangements</strong> (413) &mdash; PAS, MAA, CAA
          </li>
          <li>
            <strong>Evidence gaps</strong> (3,658) &mdash; type and description
          </li>
          <li>
            <strong>Cross-references</strong> (952) &mdash; TA-to-TA citations
            with relationship type
          </li>
        </ul>

        <h2>Pipeline</h2>
        <ol>
          <li>
            Scraped NICE website for all TA listings via the Next.js JSON API
            (894 TAs indexed)
          </li>
          <li>Downloaded 4,522 PDFs (7.3 GB)</li>
          <li>
            Converted to markdown with page-level markers using pymupdf4llm
            (3,307 files, 380K pages)
          </li>
          <li>
            Chunked into 10-page windows with 2-page overlap (2,314 FAD chunks)
          </li>
          <li>
            Extracted entities using Claude Haiku 4.5 with tool calling against a
            purpose-built ontology. 2,314/2,314 chunks processed, 0 errors.
          </li>
          <li>
            Normalised enums, deduplicated entities across overlapping chunks,
            built 14 typed SQLite tables
          </li>
          <li>
            Built FTS5 full-text search index across all 3,307 documents
          </li>
        </ol>

        <h2>Ontology development</h2>
        <p>
          The extraction schema was developed iteratively: two independent AI
          agents each proposed an ontology from 20 diverse TAs, then proposals
          were merged and refined over 5 rounds on 50 additional TAs. Stabilised
          at 9 entity types, 23 methodological decision categories, and 8 ICER
          bands, with a 3.5% &ldquo;other&rdquo; rate for decision categories.
          See
          <a
            href="https://github.com/shoulders-ai/nice-graph/blob/main/ontology/methods.md"
            >ontology/methods.md</a
          >.
        </p>

        <h2>Coverage and limitations</h2>
        <ul>
          <li>
            826 TAs have source documents; 555 have structured extraction
          </li>
          <li>
            Extraction targets Final Appraisal Documents only &mdash; not ERG
            reports, scope comments, or committee papers
          </li>
          <li>
            Numerical results (ICERs, QALYs, costs, hazard ratios) are
            deliberately not extracted &mdash; stored as categorical bands
            instead
          </li>
          <li>
            Older TAs (pre-2006) have lower extraction quality due to different
            document formats
          </li>
          <li>
            Extraction uses AI and is not perfect &mdash; verify against source
            documents for critical decisions
          </li>
        </ul>

        <h2>API</h2>
        <table>
          <thead>
            <tr>
              <th>Endpoint</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>/llms.txt</code></td>
              <td>Machine-readable project overview and API guide</td>
            </tr>
            <tr>
              <td><code>/llms-full.txt</code></td>
              <td>Full corpus index (all TAs with document counts)</td>
            </tr>
            <tr>
              <td><code>/api/search?q=...&amp;format=plain</code></td>
              <td>Full-text search</td>
            </tr>
            <tr>
              <td><code>/api/corpus/ta{N}/</code></td>
              <td>Document listing for a TA</td>
            </tr>
            <tr>
              <td><code>/api/corpus/ta{N}/{doc}.md</code></td>
              <td>Raw document markdown</td>
            </tr>
            <tr>
              <td><code>POST /api/chat</code></td>
              <td>Natural language &rarr; SQL &rarr; answer (SSE stream)</td>
            </tr>
          </tbody>
        </table>

        <h2>Source</h2>
        <p>
          <a href="https://github.com/shoulders-ai/nice-graph">GitHub</a>
          &middot; Data from
          <a href="https://www.nice.org.uk">NICE</a> &middot; Built by
          <a href="https://shoulde.rs">Shoulders</a>
        </p>
      </article>
    </div>
  </div>
</template>
